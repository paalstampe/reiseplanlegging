# Handover: Reisekalender – beste reisetid per destinasjon

Referansedokument. Løpende status står i NOTES.md. Overført fra claude.ai-chat (Project «Reise») 25.09.2026. Språk: norsk. Pål vil ha direkte, konsise svar uten innledninger/oppsummeringer.

## Mål
Oversikt over når på året (ned mot ukenummer) det er best å reise til hvert reisemål på Påls liste, brukt til å planlegge konkrete reiser i gitte tidsvinduer.

## Filer (alle i `~/Developer/reiseplanlegging/` – git-repo `paalstampe/reiseplanlegging`, flyttet fra `Privat/Dokumenter/Reise/Reiseplanlegging` 26.09.2026)
- `Reise - utenfor Europa.md` – **master-liste** over destinasjoner (avkrysning = besøkt). Besluttet: .md-filen er master.
- `reisedata.py` – **all data** (månedsscorer, T/N, begrunnelser, klimakilde, kategori, merknader, vinduer). Bevegelige datoer angis som datoer og regnes om til ISO-uker.
- `bygg_reisekalender.py` – Python-skript (openpyxl) som bygger `Reisekalender.xlsx` fra destinasjonslisten i skriptet + `reisedata.py`. Kjør: `python3 bygg_reisekalender.py [utfil.xlsx]`. Skal fungere som kilde ved videre iterasjon på struktur; når strukturen er låst og data fylles inn, kan man jobbe direkte i xlsx.
- Ferdig regneark: `Reisekalender.xlsx`.

- `reisekart_mal.html` + `lag_reisekart.py` – kart-app (Reisekart). `python3 lag_reisekart.py` skriver `index.html` fra `reisedata.py` (inkl. `KOORD`). Publiseres på GitHub Pages: https://stam.pe/reiseplanlegging/ – oppdateres ved å kjøre skriptet, committe og pushe (GitHub Desktop). Tidligere artifact «Reisekart» (https://claude.ai/artifact/GUxGBFFo5dFxVg5u4f5jvA) oppdateres ikke lenger automatisk. Malen er et komplett HTML-dokument (doctype + viewport-meta – uten viewport blir alt bitte lite på mobil). Interaksjon: på touch (hover:none) er tooltip av, trykk åpner detaljkortet, og pinch/pan er egen dempet implementasjon (`touchRoam`, `PINCH_DEMPING` 0,6) som under gesten kun flytter/skalerer kartbildet med CSS-transform og tegner ECharts på nytt én gang ved slipp (omtegning per frame var for tregt på iPhone); `animation:false` så prikkene ikke sklir etter; på PC vises tooltip etter 400 ms hover (`HOVER_FORSINKELSE`) og skjules ved klikk/for valgt punkt. Treff (hover/klikk/trykk) avgjøres av nærmeste prikk innen 12 px (PC) / 24 px (touch) – serien er `silent`, så etiketter ikke stjeler treff. Testing: Chrome på Mac via AppleScript («Tillat JavaScript fra Apple Events» er slått på); koden kjører i isolert kontekst, så injiser et <script> og les resultat via `document.body.dataset`; zrender krever mousedown/mouseup før click. Zoomknapper øverst til venstre (+/− med faktor 2 rundt kartets midte, og «Vis hele kartet» tilbake til startvisning) i samme stil som byguidenes MapLibre-kontroller (`zoomKnapper()`); − er deaktivert på zoom 1, + på `ZOOM_MAX`. Detaljkortet lukkes med ×, Escape, trykk på tomt kart eller klikk utenfor (unntatt listeoppslag, knapper/filtre og kortet selv). iOS krever `cursor:pointer` på body (kun `hover:none`) for at trykk på tekst/tom flate skal gi klikk; på mobil er kortet lavere enn kartet så en stripe kart alltid synes over. Kart: ECharts 5.5.1 (jsDelivr; cdnjs ga 404) + echarts@4.9.0 world.js (jsDelivr), lastes dynamisk med AMD skjult. Hjemskjerm-ikon: `apple-touch-icon.png` (180×180, kobber «r» i Playfair Display på papir, samme stil som «s» på stam.pe og «b» i byguidene); navnet under ikonet er «Reisekart» (`apple-mobile-web-app-title` i malen). Offline: `sw.js` (service worker, registreres fra malen) lagrer `index.html` (med alle data), ECharts, world.js og Google Fonts ved første besøk med nett. `index.html` hentes fra nettet først (lagret kopi uten nett eller etter 4 s), bibliotekene og fontene fra lageret. Bytter du versjon på ECharts eller world.js i `KILDER`, oppdater også `FILER` i `sw.js` og øk `VERSJON`. Siden sender `{ type: 'lagre', adresser }` til `sw.js` ved hver lasting; når alt er lagret, melder `sw.js` `{ type: 'lagret', app: 'reiseplanlegging' }` til alle åpne sider, og siden viser «Tilgjengelig offline · 13. okt» under ingressen (dato i localStorage, nøkkel `reiseplanlegging-offline:/reiseplanlegging/`). «Lagre alt for bruk offline» på stam.pe bruker samme melding og nøkkel.

## Forhåndsvisning av grener
`.github/workflows/pages.yml` publiserer `main` på `stam.pe/reiseplanlegging/` og hver annen gren på `stam.pe/reiseplanlegging/forhandsvisning/<gren>/`, ett–to minutter etter push (samme oppsett som byguidene). Slettede grener forsvinner ved neste publisering. Pages-kilden er «GitHub Actions». Husk at `index.html` må være generert (`python3 lag_reisekart.py`) og committet på grenen.

## Sjekke design
Før Claude sier at en endring er ferdig, tar Claude skjermbilder og ser på dem — av forhåndsvisningen eller en lokal kopi for grener, ellers av den publiserte siden: `.claude/skjermbilde.sh https://stam.pe/reiseplanlegging/ <fil.png> 390 844` (mobil) og `1300 900` (desktop); legg til `hel` for hele siden. Tillatt: `https://stam.pe/...` og `http://localhost:<port>/...`. Virker både i skyøkter og lokalt på Macen (der kreves Node og Playwright, se toppen av skriptet). Lokal kopi: `python3 lag_reisekart.py`, så `python3 -m http.server 8000 --bind 127.0.0.1` i repoet (bind hindrer at andre på samme nett ser mappen). I lokale økter starter Claude serveren og åpner siden for Pål når han bør se på noe. Kjøretillatelsen står i `.claude/settings.json`.

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

## Mørk modus
Følger enhetens innstilling. `@media (prefers-color-scheme: dark)` i `reisekart_mal.html` bytter CSS-variablene til samme mørke palett som stam.pe og byguidene. Kartet (ECharts) leser fargene fra variablene med `css("--…")` når det tegnes. Nye farger skal derfor alltid være variabler, ikke faste verdier.

## Ikke søkbar
`reisekart_mal.html` har `<meta name="robots" content="noindex, nofollow, noarchive">`, så den følger med inn i `index.html`. KI-innsamlere stenges ute av `robots.txt` i `paalstampe.github.io`, som gjelder hele stam.pe.

## Status
Se NOTES.md (Status nå og Åpne spørsmål).

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

## Navneendringer (27.09.2026)
- USA-WC → «USA Nordvestkyst – San Francisco til Vancouver»; USA-HI → «Hawaii»; MEX-CDMX → «Mexico City»; EGY → «Egypt – Kairo, Luxor»; SILK → «Sentral-Asia – Silkeveien»; SGP → «Singapore».
- USA-CHS → «USA – Savannah-Charleston»: dekker Georgia/South Carolina-kysten generelt; klima = snitt av Charleston og Savannah/Hilton Head (NOAA 1991–2020), koordinat midt mellom byene.
- Kartetiketter bruker nå tankestrek mellom land og sted (f.eks. «Brasil – Rio og nordover»).
- Brødsmuler øverst i sidepanelet («stam.pe / Reiseplanlegging», stam.pe lenker til landingssiden) erstatter kickeren «Reisekalender · 40 reisemål» – samme stil som i byguidene.
- Sidepanelet på desktop (04.10.2026): hele panelet ruller (ett rullefelt, listen har ikke eget), tellerlinjen «N av 40 grønne …» ligger fast øverst. Alternativet med kompakte filtre (månedene på én rad osv.) ble prøvd på grenen `sidepanel-kompakt`, men ikke valgt.

## Neste steg
Se NOTES.md.
