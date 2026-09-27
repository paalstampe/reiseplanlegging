# Handover: Reisekalender – beste reisetid per destinasjon

Overført fra claude.ai-chat (Project «Reise») 25.09.2026. Språk: norsk. Pål vil ha direkte, konsise svar uten innledninger/oppsummeringer.

## Mål
Oversikt over når på året (ned mot ukenummer) det er best å reise til hvert reisemål på Påls liste, brukt til å planlegge konkrete reiser i gitte tidsvinduer.

## Filer (alle i `/Users/palstampe/Documents/GitHub/reiseplanlegging/` – git-repo `paalstampe/reiseplanlegging`, flyttet fra `Privat/Dokumenter/Reise/Reiseplanlegging` 26.09.2026)
- `Reise - utenfor Europa.md` – **master-liste** over destinasjoner (avkrysning = besøkt). Besluttet: .md-filen er master.
- `Gammel - Reiseidéer og reisekalender.xlsx` – Påls gamle planleggingsark (T/N per måned, kalenderark per dag). Kun referanse; erstattes av ny struktur.
- `reisedata.py` – **all data** (månedsscorer, T/N, begrunnelser, klimakilde, kategori, merknader, vinduer). Bevegelige datoer angis som datoer og regnes om til ISO-uker.
- `bygg_reisekalender.py` – Python-skript (openpyxl) som bygger `Reisekalender.xlsx` fra destinasjonslisten i skriptet + `reisedata.py`. Kjør: `python3 bygg_reisekalender.py [utfil.xlsx]`. Skal fungere som kilde ved videre iterasjon på struktur; når strukturen er låst og data fylles inn, kan man jobbe direkte i xlsx.
- Ferdig regneark: `Reisekalender.xlsx`.

- `reisekart_mal.html` + `lag_reisekart.py` – kart-app (Reisekart). `python3 lag_reisekart.py` skriver `index.html` fra `reisedata.py` (inkl. `KOORD`). Publiseres på GitHub Pages: https://paalstampe.github.io/reiseplanlegging/ – oppdateres ved å kjøre skriptet, committe og pushe (GitHub Desktop). Tidligere artifact «Reisekart» (https://claude.ai/artifact/GUxGBFFo5dFxVg5u4f5jvA) oppdateres ikke lenger automatisk. Malen er et komplett HTML-dokument (doctype + viewport-meta – uten viewport blir alt bitte lite på mobil). Interaksjon: på touch (hover:none) er tooltip av, trykk åpner detaljkortet, og pinch/pan er egen dempet implementasjon (`touchRoam`, `PINCH_DEMPING` 0,6); på PC vises tooltip etter 400 ms hover (`HOVER_FORSINKELSE`) og skjules ved klikk/for valgt punkt. Treff (hover/klikk/trykk) avgjøres av nærmeste prikk innen 12 px (PC) / 24 px (touch) – serien er `silent`, så etiketter ikke stjeler treff. Testing: Chrome på Mac via AppleScript («Tillat JavaScript fra Apple Events» er slått på); koden kjører i isolert kontekst, så injiser et <script> og les resultat via `document.body.dataset`; zrender krever mousedown/mouseup før click. Kart: ECharts 5.5.1 (jsDelivr; cdnjs ga 404) + echarts@4.9.0 world.js (jsDelivr), lastes dynamisk med AMD skjult. `style.css` er kun referanse (stil fra Pål's London) – brukes ikke av appen.
- `github-pages-oppsett-reiseplanlegger.md` – oppsettnotat for GitHub Pages (samme mønster som nabolag-london).

## Besluttet design
- **Format:** Excel. Normalisert datamodell + generert visning. (HTML-visning evt. senere, generert fra Excel.)
- **Enhet:** destinasjon/region, ikke land (f.eks. Vietnam langs ruten, Goa ≠ India, Sri Lanka kan måtte splittes pga. to monsunsystemer).
- **Oppløsning:** klima per måned (finnes ikke bedre data); ukespresisjon kun via avgrensede *vinduer* (monsunstart, dyrelivshendelser, helligdager som Tet, festivaler, sesongåpning).
- **Ark:**
  1. *Les meg* – forklaring, scoreskala, vekter (input).
  2. *Kalender* – heatmap destinasjon × ISO-uke 1–52 for valgt år (B2). Rad 7: Pål markerer tilgjengelige uker med «x»; kolonnene «Snitt mine uker» og «Laveste mine uker» brukes til å sortere kandidater.
  3. *Destinasjoner* – ID (nøkkel), region, land, sted/fokus, visningsnavn (formel), status, kategori, varighet, «Data i Måned» (formel), merknad. Alle 40 destinasjoner fra .md er lagt inn.
  4. *Måned* – 12 rader per destinasjon: Klima, Opplevelse, Trengsel/pris (1–5), Samlet (formel), T maks °C, nedbør mm, begrunnelse.
  5. *Vinduer* – ID, fra uke, til uke, type, justering (±), «kun år» (tom = hvert år), beskrivelse.
- **Samlet månedsscore** = 0,4·Klima + 0,4·Opplevelse + 0,2·Trengsel/pris (vekter i Les meg). **Veto-tak:** Klima eller Opplevelse = 1 ⇒ samlet = min(1,5; vektet snitt). Taket er input i Les meg.
- **Ukescore** = månedsscore for måneden torsdagen i uken faller i (ISO) + sum vindusjusteringer, begrenset til [1, 5]. Fra > Til = vindu over nyttår. Uke 53 vises ikke.
- **Konvensjoner:** Arial; blå tekst/gul fylling = input, svart = formel. Bare Excel-2007-funksjoner + `_xlfn.MINIFS` (ingen XLOOKUP/FILTER o.l.).

## Status (25.09.2026)
- **Alle 40 destinasjoner populert:** klimanormaler fra én representativ stasjon per destinasjon (kilde og periode i Destinasjoner kol. K, hovedsakelig WMO/nasjonale met-tjenester via Wikipedia), delscorer, begrunnelser og 49 vinduer (bevegelige høytider 2026–28, festivaler, dyrelivshendelser).
- BWA (Maun, DWD 1961–1990) og ATA (Esperanza-basen, SMN 1991–2020) er nå verifisert.
- Kalender: lysegrønn for uker ≥ 4,0 (input B3), mørkegrønn ≥ 4,4 (input B4), ellers uten farge. Ghana/Benin/Togo strammet inn (26.09) så kun nov–des (+ aug for Ghana) blir grønne.
- Kalender: tynn loddrett strek ved hvert månedsskifte (betinget formatering, følger valgt år) og månedsnavn i fet skrift kun ved første uke i måneden.
- Svakheter: noen gamle serier (Dili, Beirut, Galápagos, Hwange, São Tomé, Maun 1961–1990); enkelte stasjoner er proxy (Rote→Kupang, USA-WC→Vancouver, CRI→Liberia/Guanacaste, ZWE→Hwange); noen festivaldatoer «sjekk dato».
- Sikkerhetsmerknader: Myanmar, Yemen/Socotra, Libanon, PNG, Etiopia, Benin, Togo.

## Avklart med Pål (25.09.2026)
- Vekter 40/40/20 beholdes. Veto myket opp til tak 1,5.
- Trengsel/pris beholdes som én dimensjon.
- «Timbuktu» var feil – skal være Katmandu (Nepal: Katmandu, Pokhara).
- «Stan-land» slått sammen med Silkeveien (ID SILK). Rute avklares ved populering.
- Sri Lanka splittet: LKA-SV (vest/sør + høylandet) og LKA-O (østkysten).
- Hawaii og Charleston på egne rader (også i .md).
- Dubletter ryddet i .md (Etiopia, Egypt, São Tomé og Príncipe).
- Destinasjoner som kun fantes i det gamle arket droppes.
- Filer flyttet til undermappen Reiseplanlegging; «Delt med Claude» og gamle versjoner slettet.

## Neste steg
1. ~~Få svar på åpne spørsmål, juster struktur/skript.~~ Gjort 25.09.
2. ~~Populer alle destinasjoner~~ Gjort 25.09. Videre: finjuster scorer etter Påls vurdering.
3. Årlig: legg inn nye bevegelige datoer (Tet/kinesisk nyttår, påske, ramadan, tsechu) i `reisedata.py` og bygg på nytt.
4. Evt. HTML-visning generert fra Excel.
