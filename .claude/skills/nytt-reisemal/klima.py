# Henter klimaboksen («Climate data for …») fra en engelsk Wikipedia-side og skriver T maks (°C) og nedbør (mm) per måned.
# Bruk: python3 -I .claude/skills/nytt-reisemal/klima.py Muscat [Climate_of_Dubai …]
# Siden lastes ned til en midlertidig mappe og leses som data (ikke kjørt). Mangler nedbør, finnes den ofte i «Climate of …».
import sys, re, html, tempfile, urllib.request, os

def tabeller(side):
    url = "https://en.wikipedia.org/wiki/" + side
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (reiseplanlegging)"})
    with tempfile.TemporaryDirectory() as d:
        sti = os.path.join(d, "side.html")
        with urllib.request.urlopen(req, timeout=30) as svar, open(sti, "wb") as f:
            f.write(svar.read())
        t = open(sti, encoding="utf-8").read()
    for tab in re.findall(r'<table[^>]*>.*?</table>', t, re.S):
        if "Climate data for" in tab:
            yield tab

def rens(c): return " ".join(html.unescape(re.sub(r'<[^>]+>', '', c)).split())

for side in sys.argv[1:]:
    print("===", side)
    for tab in tabeller(side):
        tittel = rens(re.search(r'Climate data for.*?</th>', tab, re.S).group(0))
        normaler = re.search(r'\d{4}\s*[–−-]\s*\d{4}\)?\s*normals', tittel)
        print(tittel.split("Climate ID")[0].split("WMO ID")[0][:120], "|", normaler.group(0) if normaler else "periode: se tittel")
        for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', tab, re.S):
            c = [rens(x) for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', tr, re.S)]
            if len(c) < 13: continue
            # Amerikanske sider har «°F (°C)» og «inches (mm)»: da står °C/mm i parentesen.
            i_parentes = "°F (°C)" in c[0] or "inches (mm)" in c[0]
            tall = [(x.split("(")[1].rstrip(")") if i_parentes and "(" in x else x.split("(")[0]).replace("−", "-").replace(",", "") for x in c[1:13]]
            if ("Mean daily maximum" in c[0] or "Average high" in c[0]) and "°C" in c[0]: print("  tmaks ", tall)
            if ("precipitation" in c[0].lower() or "rainfall" in c[0].lower()) and "mm" in c[0] and "days" not in c[0].lower():
                print("  nedbor" if "precipitation" in c[0].lower() else "  regn  ", tall)
        kilde = re.search(r'Source[^<]*?:(.*?)</td>', tab, re.S)
        if kilde: print("  kilde ", rens(kilde.group(1))[:200])
