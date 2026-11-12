"""Deler, slår sammen eller gir ny ID til reisemål, og oppdaterer alt som peker på dem.

Skriv de nye reisemal/<ID>.json først (med reisemal.skriv), og kjør så fra repoet:
  python3 .claude/skills/nytt-reisemal/omorganiser.py VNM=VNM-N,VNM-C,VNM-S   # deling
  python3 .claude/skills/nytt-reisemal/omorganiser.py USA-CHS=USA-SOR         # sammenslåing eller ny ID
Flere endringer kan gis i samme kjøring. Skriptet
- sletter reisemal/<gammel>.json når den gamle ID-en ikke er blant de nye,
- bytter ID-en i «gjelder» i felles_vinduer.json (overstyringer følger med til hver ny ID),
- erstatter raden i landliste.tsv med de nye (land og sted fra JSON-filene) og lager tabellene og tallene øverst i Landliste.md på nytt,
- retter antall reisemål og ønskelistereisemål i CLAUDE.md,
- bygger index.html, Reisemål.md og Reisekalender.xlsx, og viser hvor de gamle ID-ene ellers står (rett dem for hånd).
"""
import csv, json, os, re, subprocess, sys

ROT = os.getcwd()
sys.path.insert(0, ROT)
import reisemal

TSV, MD, FELLES = "landliste.tsv", "Landliste.md", "felles_vinduer.json"
FELT = ["region", "id", "land", "sted", "status", "merknad"]


def les_reisemal(id):
    sti = os.path.join("reisemal", id + ".json")
    if not os.path.exists(sti):
        sys.exit(f"Mangler {sti}: skriv de nye reisemålene før du kjører skriptet.")
    return json.load(open(sti, encoding="utf-8"))


def bytt_felles(endringer):
    data = json.load(open(FELLES, encoding="utf-8"))
    for v in data["vinduer"]:
        ny = []
        for g in v["gjelder"]:
            gid = g["id"] if isinstance(g, dict) else g
            for id in endringer.get(gid, [gid]):
                if any(id == (x["id"] if isinstance(x, dict) else x) for x in ny):
                    if isinstance(g, dict):
                        print(f"Merk: overstyringen for {gid} i «{v['no']}» er ikke flyttet; {id} står der fra før.")
                    continue
                ny.append({**g, "id": id} if isinstance(g, dict) else id)
        v["gjelder"] = ny
    with open(FELLES, "w", encoding="utf-8") as f:
        f.write('{\n  "_om": ' + json.dumps(data["_om"], ensure_ascii=False) + ',\n  "vinduer": [\n'
                + ",\n".join("    " + json.dumps(v, ensure_ascii=False) for v in data["vinduer"]) + "\n  ]\n}\n")


def bytt_landliste(endringer):
    rader = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
    finnes = {r["id"] for r in rader}
    ut = []
    for r in rader:
        if r["id"] not in endringer:
            ut.append(r)
            continue
        for id in endringer[r["id"]]:
            if id in finnes and id != r["id"]:
                continue  # raden står allerede; land og sted oppdateres under
            ut.append({**r, "id": id})
    nye = {id for ids in endringer.values() for id in ids}
    for r in ut:
        if r["id"] in nye:
            d = les_reisemal(r["id"])
            r.update(region=d["region"], land=d["land"], sted=d["sted"])
    with open(TSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FELT, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(ut)
    return ut


def lag_landliste_md(rader, onske):
    md = open(MD, encoding="utf-8").read()
    land = [r["land"] for r in rader]
    delt = len({l for l in land if land.count(l) > 1})
    md = re.sub(r"Nå: \*\*\d+ reisemål\*\*, \d+ land er delt opp og \d+ er på ønskelisten",
                f"Nå: **{len(rader)} reisemål**, {delt} land er delt opp og {onske} er på ønskelisten", md)
    regioner = list(dict.fromkeys(r["region"] for r in rader))
    tabeller = []
    for reg in regioner:
        rr = [r for r in rader if r["region"] == reg]
        tabeller.append(f"## {reg} ({len(rr)})\n\n| ID | Land | Del | | Merknad |\n|---|---|---|---|---|\n" + "".join(
            f"| {r['id']} | {r['land']} | {r['sted']} | {'finnes' if r['status'] == 'finnes' else ''} | {r['merknad']} |\n"
            for r in rr))
    with open(MD, "w", encoding="utf-8") as f:
        f.write(md[:md.index("## " + regioner[0])] + "\n".join(tabeller))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    endringer = {}
    for a in argv:
        gammel, _, nye = a.partition("=")
        if not nye:
            sys.exit(__doc__)
        endringer[gammel] = nye.split(",")
    # Sjekk alt før noe endres, så en feil ikke etterlater et halvt omorganisert repo.
    i_landliste = {r["id"] for r in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t")}
    for gammel, nye in endringer.items():
        if gammel not in i_landliste:
            sys.exit(f"{gammel} står ikke i {TSV}.")
        for id in nye:
            les_reisemal(id)
    for gammel, nye in endringer.items():
        if gammel not in nye and os.path.exists(f"reisemal/{gammel}.json"):
            os.remove(f"reisemal/{gammel}.json")
    bytt_felles(endringer)
    rader = bytt_landliste(endringer)

    alle = reisemal.last()
    antall, onske = len(alle), sum(1 for r in alle if r["onskeliste"])
    lag_landliste_md(rader, onske)
    claude = open("CLAUDE.md", encoding="utf-8").read()
    claude = re.sub(r"\d+ reisemål som dekker", f"{antall} reisemål som dekker", claude)
    claude = re.sub(r"Påls egne \d+ er på ønskelisten", f"Påls egne {onske} er på ønskelisten", claude)
    open("CLAUDE.md", "w", encoding="utf-8").write(claude)

    subprocess.run([sys.executable, "lag_reisekart.py"], check=True)
    subprocess.run([sys.executable, "bygg_reisekalender.py"], check=True)
    print(f"{antall} reisemål, {onske} på ønskelisten.", flush=True)
    borte = [g for g, nye in endringer.items() if g not in nye]
    if borte:
        print("Gamle ID-er som fortsatt står i dokumentasjonen (rett for hånd der det trengs):", flush=True)
        # Bindestrek hører til ID-en (VNM skal ikke treffe VNM-N), så -w holder ikke.
        monster = r"(^|[^A-Z0-9-])(" + "|".join(borte) + r")([^A-Z0-9-]|$)"
        subprocess.run(["grep", "-nE", monster, "CLAUDE.md", "HANDOVER.md", "NOTES.md",
                        "Kildesvakheter.md", ".claude/skills/nytt-reisemal/SKILL.md"])


if __name__ == "__main__":
    main(sys.argv[1:])
