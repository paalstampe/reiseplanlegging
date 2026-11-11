# Lager index.html (kart-app) fra reisemålene i reisemal/<ID>.json, og masterlista «Reisemål.md».
# Bruk: python3 lag_reisekart.py   → skriver index.html ved siden av. Publiseres via GitHub Pages (commit + push).
import json, os, sys, datetime
HER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HER)
import reisemal

alle = reisemal.last()
hull = []
data = {"dest": [], "win": [], "weights": [0.4, 0.4, 0.2], "cap": 1.5,
        "koord": {r["id"]: r["koord"] for r in alle}, "dato": datetime.date.today().strftime("%d.%m.%Y")}
for r in alle:
    idd, en = r["id"], r["en"]
    # Engelsk: vindusbeskrivelsen legges til sist i hvert vindu (w[7]), resten under d["en"]. Hull meldes, og norsk vises.
    data["win"] += [list(reisemal.vindu(r, v)) + [v.get("en") or v["no"]] for v in r["vinduer"]]
    hull += [f"{idd}: vindu «{v['no']}»" for v in r["vinduer"] if not v.get("en")]
    en_m = [m.get("en", "") for m in r["maneder"]]
    data["dest"].append({"id": idd, "region": r["region"], "land": r["land"], "sted": r["sted"], "status": r["status"], "onskeliste": r["onskeliste"],
        "kategori": r["kategori"], "merknad": r["merknad"], "kilde": r["kilde"],
        "en": {**en, "m": en_m},  # tom månedstekst = norsk vises for den måneden
        # «se Vinduer» viser til arket i regnearket; i kartet heter det «Hendelser».
        "m": [[m[f] for f in reisemal.MANEDSFELT[:-1]] + [m["no"].replace("se Vinduer", "se hendelser")] for m in r["maneder"]]})
    if not all(en_m): hull.append(idd + ": månedstekster")
    for felt in ("sted", "merknad", "kategori"):
        if r[felt] and felt not in en: hull.append(idd + ": " + felt)
for h in hull: print("Mangler engelsk:", h)
mal = open(os.path.join(HER, "reisekart_mal.html"), encoding="utf-8").read()
ut = mal.replace("__DATA__", json.dumps(data, ensure_ascii=False))
open(os.path.join(HER, "index.html"), "w", encoding="utf-8").write(ut)
print("Lagret index.html", len(data["dest"]), "reisemål")

# Masterlista lages fra dataene (avkrysning = besøkt). Rediger reisemal/<ID>.json, ikke md-fila.
md = ["# Reisemål", "", "Generert av lag_reisekart.py fra reisemal/. ★ = ønskeliste.", ""]
for region in reisemal.REGIONER:
    rr = [r for r in alle if r["region"] == region]
    if not rr: continue
    md += ["## " + region, ""]
    md += [f"- [{'x' if r['status'] == 'Besøkt' else ' '}] {r['land']}{': ' + r['sted'] if r['sted'] else ''}"
           f"{' ★' if r['onskeliste'] else ''} ({r['id']})" for r in rr]
    md.append("")
open(os.path.join(HER, "Reisemål.md"), "w", encoding="utf-8").write("\n".join(md))
