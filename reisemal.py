# Leser reisemålene i reisemal/<ID>.json. Brukes av lag_reisekart.py og bygg_reisekalender.py.
# Én fil per reisemål, med norsk og engelsk side om side. Format og felter: se HANDOVER.md (Datamodell).
import glob, json, os
from datetime import date

MAPPE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reisemal")
# Rekkefølgen regionene vises i (regneark og md-liste). Ny region legges inn her og i TEKST.regioner i malen.
REGIONER = ["Asia, Oseania og Midt-Østen", "Nord-Amerika", "Sør- og Mellom-Amerika", "Afrika"]
FELT = ("id", "region", "land", "sted", "status", "onskeliste", "kategori", "merknad", "koord", "kilde", "en", "maneder", "vinduer")
NORSK = str.maketrans({"æ": "{", "ø": "|", "å": "}"})  # æ, ø, å sorteres etter z

def sorteringsnokkel(r):
    return (REGIONER.index(r["region"]), (r["land"] + " " + r["sted"]).casefold().translate(NORSK))

def last():
    """Alle reisemål, sortert på region og navn. Stopper med feilmelding hvis en fil er ufullstendig."""
    alle = []
    for sti in glob.glob(os.path.join(MAPPE, "*.json")):
        with open(sti, encoding="utf-8") as fil:
            r = json.load(fil)
        navn = os.path.basename(sti)
        mangler = [f for f in FELT if f not in r]
        assert not mangler, f"{navn}: mangler {', '.join(mangler)}"
        assert r["id"] + ".json" == navn, f"{navn}: id er {r['id']}"
        assert r["region"] in REGIONER, f"{navn}: ukjent region {r['region']} (legg den inn i REGIONER)"
        assert len(r["maneder"]) == 12, f"{navn}: {len(r['maneder'])} måneder"
        alle.append(r)
    return sorted(alle, key=sorteringsnokkel)

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
    for k, v in r.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            verdi = "[\n" + ",\n".join("    " + json.dumps(x, ensure_ascii=False) for x in v) + "\n  ]"
        else:
            verdi = json.dumps(v, ensure_ascii=False)
        linjer.append(f"  {json.dumps(k)}: {verdi}")
    with open(sti, "w", encoding="utf-8") as fil:
        fil.write("{\n" + ",\n".join(linjer) + "\n}\n")
