# Leser reisemålene i reisemal/<ID>.json. Brukes av lag_reisekart.py og bygg_reisekalender.py.
# Én fil per reisemål, med norsk og engelsk side om side. Format og felter: se HANDOVER.md (Datamodell).
import glob, json, os
from datetime import date

HER = os.path.dirname(os.path.abspath(__file__))
MAPPE = os.path.join(HER, "reisemal")
# Vinduer som gjelder mange reisemål (ramadan, påske, kinesisk nyttår …) står én gang her, med lista over reisemålene.
FELLES = os.path.join(HER, "felles_vinduer.json")
# Rekkefølgen regionene vises i (regneark og md-liste). Ny region legges inn her og i TEKST.regioner i malen.
REGIONER = ["Europa", "Midtøsten", "Afrika", "Asia", "Oseania", "Nord-Amerika", "Mellom-Amerika og Karibia", "Sør-Amerika"]
FELT = ("id", "region", "land", "sted", "status", "onskeliste", "kategori", "merknad", "koord", "kilde", "en", "maneder", "vinduer")
MANEDSFELT = ("klima", "opplevelse", "trengsel", "tmaks", "nedbor", "no")
VINDUSFELT = ("type", "justering", "no")
NORSK = str.maketrans({"æ": "{", "ø": "|", "å": "}"})  # æ, ø, å sorteres etter z

def sorteringsnokkel(r):
    return (REGIONER.index(r["region"]), (r["land"] + " " + r["sted"]).casefold().translate(NORSK))

def last():
    """Alle reisemål, sortert på region og navn. Stopper med feilmelding hvis en fil er ufullstendig."""
    alle = []
    for sti in glob.glob(os.path.join(MAPPE, "*.json")):
        with open(sti, encoding="utf-8") as fil:
            r = json.load(fil)
        feil = sjekk(r, os.path.basename(sti))
        if feil:
            raise SystemExit(os.path.basename(sti) + ": " + "; ".join(feil))
        alle.append(r)
    leggTilFelles({r["id"]: r for r in alle})
    return sorted(alle, key=sorteringsnokkel)

def leggTilFelles(per_id):
    """Legger de felles vinduene til hvert reisemål de gjelder. Et element i «gjelder» er en ID, eller
    {"id": …} med felter som overstyrer (f.eks. annen justering eller tekst for det reisemålet).
    Vinduene merkes «felles», så skriv() ikke lagrer dem i reisemålets egen fil."""
    if not os.path.exists(FELLES): return
    with open(FELLES, encoding="utf-8") as fil:
        felles = json.load(fil)["vinduer"]
    for i, v in enumerate(felles, 1):
        feil = sjekk_vindu(v, i) + ([] if v.get("gjelder") else [f"vindu {i} mangler gjelder"])
        if feil:
            raise SystemExit(f"felles_vinduer.json («{v.get('no', '')}»): " + "; ".join(feil))
        for g in v["gjelder"]:
            idd, overstyr = (g, {}) if isinstance(g, str) else (g.get("id"), {k: x for k, x in g.items() if k != "id"})
            if idd not in per_id:
                raise SystemExit(f"felles_vinduer.json («{v['no']}»): ukjent reisemål {idd}")
            ny = {**{k: x for k, x in v.items() if k != "gjelder"}, **overstyr, "felles": True}
            # Samme vindu to ganger (dobbelt i gjelder, eller også i reisemålets egen fil) ville gitt dobbel justering.
            if any((w.get("fra"), w.get("fra_uke"), w["type"]) == (ny.get("fra"), ny.get("fra_uke"), ny["type"]) for w in per_id[idd]["vinduer"]):
                raise SystemExit(f"felles_vinduer.json («{v['no']}»): {idd} har allerede et {ny['type'].lower()}svindu med samme start")
            per_id[idd]["vinduer"].append(ny)

def sjekk_vindu(v, i):
    feil = [f"vindu {i} mangler {f}" for f in VINDUSFELT if f not in v]
    if not ("fra" in v and "til" in v or "fra_uke" in v and "til_uke" in v):
        feil.append(f"vindu {i} mangler fra/til eller fra_uke/til_uke")
    return feil

def sjekk(r, navn):
    """Liste over feil i ett reisemål (tom = i orden)."""
    feil = [f"mangler {f}" for f in FELT if f not in r]
    if feil: return feil
    if r["id"] + ".json" != navn: feil.append(f"id er {r['id']}")
    if r["region"] not in REGIONER: feil.append(f"ukjent region {r['region']} (legg den inn i REGIONER)")
    if len(r["koord"]) != 2: feil.append("koord skal være [bredde, lengde]")
    if len(r["maneder"]) != 12: feil.append(f"{len(r['maneder'])} måneder")
    for i, m in enumerate(r["maneder"], 1):
        feil += [f"måned {i} mangler {f}" for f in MANEDSFELT if f not in m]
    for i, v in enumerate(r["vinduer"], 1):
        feil += sjekk_vindu(v, i)
    return feil

def uke(iso):
    return date.fromisoformat(iso).isocalendar()[1]

def vindu(r, v):
    """Vinduet som (id, fra uke, til uke, type, justering, kun år, beskrivelse). Datoer regnes om til ISO-uker."""
    if "fra" in v:
        fra, til, aar = uke(v["fra"]), uke(v["til"]), date.fromisoformat(v["fra"]).isocalendar()[0]
    else:
        fra, til, aar = v["fra_uke"], v["til_uke"], v.get("aar")
    return (r["id"], fra, til, v["type"], v["justering"], aar, v["no"])

def skriv(sti, r):
    """Lagrer ett reisemål med én måned og ett vindu per linje, så endringer er lette å lese i git."""
    linjer = []
    r = {**r, "vinduer": [v for v in r.get("vinduer", []) if not v.get("felles")]}
    for k, v in r.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            verdi = "[\n" + ",\n".join("    " + json.dumps(x, ensure_ascii=False) for x in v) + "\n  ]"
        else:
            verdi = json.dumps(v, ensure_ascii=False)
        linjer.append(f"  {json.dumps(k)}: {verdi}")
    with open(sti, "w", encoding="utf-8") as fil:
        fil.write("{\n" + ",\n".join(linjer) + "\n}\n")
