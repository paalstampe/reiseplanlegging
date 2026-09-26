# Lager index.html (kart-app) fra reisedata.py + destinasjonslisten i bygg_reisekalender.py.
# Bruk: python3 lag_reisekart.py   → skriver index.html ved siden av. Publiseres via GitHub Pages (commit + push).
import json, os, sys, datetime
HER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HER)
import reisedata as RD
s = open(os.path.join(HER, "bygg_reisekalender.py"), encoding="utf-8").read()
i = s.index("dest=["); j = s.index("\n]\n", i) + 2
AS="Asia, Oseania og Midt-Østen"; NA="Nord-Amerika"; SA="Sør- og Mellom-Amerika"; AF="Afrika"
dest = eval(s[i+5:j])
data = {"dest": [], "win": [list(w) for w in RD.VINDUER], "weights": [0.4, 0.4, 0.2], "cap": 1.5,
        "koord": RD.KOORD, "dato": datetime.date.today().strftime("%d.%m.%Y")}
for idd, reg, land, sted, stat, kat, var, mer in dest:
    data["dest"].append({"id": idd, "region": reg, "land": land, "sted": sted, "status": stat or "Ikke besøkt",
        "kategori": kat or RD.KATEGORI.get(idd, ""), "merknad": mer or RD.MERKNAD.get(idd, ""),
        "kilde": RD.MANED[idd][0], "m": [list(x) for x in RD.MANED[idd][1]]})
mal = open(os.path.join(HER, "reisekart_mal.html"), encoding="utf-8").read()
ut = mal.replace("__DATA__", json.dumps(data, ensure_ascii=False))
open(os.path.join(HER, "index.html"), "w", encoding="utf-8").write(ut)
print("Lagret index.html", len(data["dest"]), "reisemål")
