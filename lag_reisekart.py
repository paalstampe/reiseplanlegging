# Lager index.html (kart-app) fra reisedata.py + destinasjonslisten i bygg_reisekalender.py.
# Bruk: python3 lag_reisekart.py   → skriver index.html ved siden av. Publiseres via GitHub Pages (commit + push).
import json, os, sys, datetime
HER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HER)
import reisedata as RD, reisedata_en as EN
s = open(os.path.join(HER, "bygg_reisekalender.py"), encoding="utf-8").read()
i = s.index("dest=["); j = s.index("\n]\n", i) + 2
AS="Asia, Oseania og Midt-Østen"; NA="Nord-Amerika"; SA="Sør- og Mellom-Amerika"; AF="Afrika"
dest = eval(s[i+5:j])
# Engelsk: vindusbeskrivelsen legges til sist i hvert vindu (w[7]), resten under d["en"]. Hull meldes, og norsk vises.
hull = [w[6] for w in RD.VINDUER if w[6] not in EN.VINDUER_EN]
data = {"dest": [], "win": [list(w) + [EN.VINDUER_EN.get(w[6], w[6])] for w in RD.VINDUER], "weights": [0.4, 0.4, 0.2], "cap": 1.5,
        "koord": RD.KOORD, "dato": datetime.date.today().strftime("%d.%m.%Y")}
for idd, reg, land, sted, stat, kat, var, mer in dest:
    data["dest"].append({"id": idd, "region": reg, "land": land, "sted": sted, "status": stat or "Ikke besøkt",
        "kategori": kat or RD.KATEGORI.get(idd, ""), "merknad": mer or RD.MERKNAD.get(idd, ""),
        "kilde": RD.MANED[idd][0], "en": EN.EN.get(idd, {}),
        # «se Vinduer» viser til arket i regnearket; i kartet heter det «Hendelser».
        "m": [list(x[:5]) + [x[5].replace("se Vinduer", "se hendelser")] for x in RD.MANED[idd][1]]})
    e = EN.EN.get(idd, {})
    if len(e.get("m", [])) != 12: hull.append(idd + ": månedstekster")
    for felt, verdi in (("sted", sted), ("merknad", data["dest"][-1]["merknad"]), ("kategori", data["dest"][-1]["kategori"])):
        if verdi and felt not in e: hull.append(idd + ": " + felt)
for h in hull: print("Mangler engelsk:", h)
mal = open(os.path.join(HER, "reisekart_mal.html"), encoding="utf-8").read()
ut = mal.replace("__DATA__", json.dumps(data, ensure_ascii=False))
open(os.path.join(HER, "index.html"), "w", encoding="utf-8").write(ut)
print("Lagret index.html", len(data["dest"]), "reisemål")
