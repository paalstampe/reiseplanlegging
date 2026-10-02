# Reiseplanlegging — arbeidsregler for Claude

Påls reisekart og reisekalender: beste reisetid per reisemål (ca. 40 steder utenfor Europa), ned mot ukenummer.
Live på https://stam.pe/reiseplanlegging/.
Les HANDOVER.md før større endringer — den har datamodell, scoremodell, kartteknikk og status.
Hold HANDOVER.md oppdatert når noe vesentlig endres (filer, besluttet design, status, navneendringer).

## Språk
- Svar Pål på norsk, direkte og konsist. Ikke forklar grunnleggende git- eller webbegreper.
- Commit-meldinger, PR-titler og -beskrivelser på norsk. Commit-stil: «Område: hva som er endret»
  (f.eks. «Kart: trykk på tomt kart lukker detaljkortet»).
- Kode: norske navn på variabler og funksjoner, som i resten av koden.
- Siden er bare på norsk.

## Filer og generering
- `reisedata.py` — all data: månedsscorer, T maks/nedbør, begrunnelser, klimakilde, kategori, merknader,
  vinduer (VINDUER) og koordinater (KOORD). Bevegelige datoer angis som datoer og regnes om til ISO-uker.
- Destinasjonslisten (`dest=[...]`) står i `bygg_reisekalender.py` og leses også av `lag_reisekart.py`.
- `Reise - utenfor Europa.md` — masterliste over reisemål (avkrysning = besøkt). Hold den i takt med `dest`.
- `reisekart_mal.html` — malen for kart-appen. `python3 lag_reisekart.py` skriver `index.html` fra mal + data.
- `index.html` er generert — rediger aldri direkte. Endre malen eller dataene og kjør skriptet.
  Generert `index.html` committes alltid sammen med endringen den kommer fra.
- `python3 bygg_reisekalender.py` bygger `Reisekalender.xlsx` (krever openpyxl). Bygg på nytt når
  dataene endres, og commit den sammen med dataendringen.
- `style.css` er bare referanse — brukes ikke av appen.

## Arbeidsflyt
- Endringer som ikke trenger forhåndsvisning — data (`reisedata.py`, destinasjonslisten,
  `Reise - utenfor Europa.md`) med generert `index.html` og `Reisekalender.xlsx`, og dokumentasjon
  (CLAUDE.md, HANDOVER.md, README.md) — pushes rett til main, uten gren og PR.
- Kodeendringer (`reisekart_mal.html`, `lag_reisekart.py`, `bygg_reisekalender.py`, `.github/`, `.claude/`)
  på egen gren. Push grenen; forhåndsvisningen er https://stam.pe/reiseplanlegging/forhandsvisning/<gren>/
  (klar 1–2 min etter push, bygges av .github/workflows/pages.yml). Husk at `index.html` må være generert
  og committet på grenen.
- Sjekk designet selv: .claude/skjermbilde.sh <url> <fil.png> 390 844 (mobil) og 1300 900 (desktop);
  legg til «hel» for hele siden. Tillatt: https://stam.pe/... og http://localhost:<port>/... (eller 127.0.0.1)
  (kjør python3 -m http.server 8000 --bind 127.0.0.1 i repoet først — gir rask sjekk før push). Virker i skyen og på Macen;
  på Macen kreves Node og Playwright (installasjon øverst i skriptet). Kartet tegnes med ECharts og krever
  ingen nøkkel, så det virker også fra localhost.
- Test samspill (hover, klikk, trykk, pinch) med Playwright, også på mobilbredde. zrender krever
  mousedown/mouseup før click.
- Fletting: Kan du selv verifisere at alt er i orden (skjermbilder mobil + desktop, ingen JS-feil),
  åpne PR og flett uten å spørre. Er det noe Pål bør se på (designvalg, smak, scorer, usikkerhet), push grenen,
  oppgi forhåndsvisningen og vent — flett når han sier ok.
- Lokal økt på Påls Mac: skal Pål se på noe, start serveren selv om den ikke kjører
  (python3 -m http.server 8000 --bind 127.0.0.1, i bakgrunnen) og åpne siden for ham med
  open http://localhost:8000/ (generer index.html først). Stopp serveren når han er ferdig. I skyøkter: bruk forhåndsvisningen.
- Lokal eller sky velges når Pål starter økta. Kode- og designarbeid går raskest lokalt på Macen;
  data og dokumentasjon går like bra i sky. Får du en kode- eller designoppgave i en skyøkt,
  si fra tidlig at den egner seg bedre lokalt (fortsett hvis Pål vil).
- GitHub sletter grenen automatisk ved fletting. Sjekk bare at den er borte (git ls-remote --heads origin);
  slett den selv bare hvis den likevel ligger igjen.
- Én endring per gren. Små, selvstendige commits.

## Teknikk (kort — detaljer i HANDOVER.md)
- Ingen rammeverk, ingen npm. Eneste byggesteg er Python-skriptene over (standardbibliotek + openpyxl).
- Kart: ECharts 5.5.1 + echarts@4.9.0 world.js fra jsDelivr (cdnjs ga 404), lastes dynamisk med AMD skjult.
- Malen er et komplett HTML-dokument med doctype og viewport-meta — uten viewport blir alt bitte lite på mobil.
- Touch (hover: none): tooltip av, trykk åpner detaljkortet, egen dempet pinch/pan (`touchRoam`,
  `PINCH_DEMPING`) som bare flytter/skalerer med CSS-transform under gesten og tegner på nytt ved slipp.
  `animation:false`. iOS trenger `cursor:pointer` på body for at trykk gir klikk.
- PC: tooltip etter `HOVER_FORSINKELSE` (400 ms). Treff = nærmeste prikk innen 12 px (PC) / 24 px (touch).
- Zoomknapper i samme stil som byguidenes MapLibre-kontroller (`zoomKnapper()`).
- Brødsmuler øverst i sidepanelet: «stam.pe / Reiseplanlegging», stam.pe lenker til landingssiden.
- Mobil er like viktig som desktop. Hover-effekter bare under (hover: hover) and (pointer: fine).
  Respekter prefers-reduced-motion.

## Scoremodell (ikke endre uten at Pål ber om det)
- Delscorer 1–5: Klima, Opplevelse, Trengsel/pris. Samlet = 0,4·Klima + 0,4·Opplevelse + 0,2·Trengsel/pris.
- Veto-tak: Klima eller Opplevelse = 1 ⇒ samlet = min(1,5; vektet snitt).
- Ukescore = månedsscore for måneden torsdagen i ISO-uken faller i + sum vindusjusteringer, begrenset til [1, 5].
  Vindu med Fra > Til går over nyttår. Uke 53 vises ikke.
- Enhet er destinasjon/region, ikke land (f.eks. Goa ≠ India, Sri Lanka splittet i LKA-SV og LKA-O).
- Kartetiketter: tankestrek mellom land og sted («Brasil – Rio og nordover»).

## Regneark (Reisekalender.xlsx)
- Arial; blå tekst/gul fylling = input, svart = formel.
- Bare Excel 2007-funksjoner + `_xlfn.MINIFS` (ingen XLOOKUP, FILTER o.l.).

## Design (samme som byguidene og stam.pe)
- Playfair Display til navn og titler, Work Sans til brødtekst.
- Papirflate #F7F4EE, tekst #241F19, dempet #6B5D4A, aksent kobber #8A5A2B.
- Ingen skygger, ingen avrundede kort — kantlinjer og luft.

## Data
- Nye reisemål: legg inn i `dest`, `reisedata.py` (scorer, kilde, KOORD) og masterlisten i .md.
  Klimanormaler fra én representativ stasjon (helst WMO/nasjonal met-tjeneste, 1991–2020); oppgi kilde og periode.
  Si fra hvis stasjonen er en proxy eller serien er gammel.
- Bevegelige datoer (Tet/kinesisk nyttår, påske, ramadan, tsechu, festivaler) legges inn per år.
  Merk usikre datoer «sjekk dato».

## Ikke gjør
- Ikke rør «Gammel - Reiseidéer og reisekalender.xlsx» (referanse).
- Ikke rediger `index.html` direkte.
- Ikke legg inn avhengigheter, byggeverktøy eller rammeverk.
- Ikke slett uflettede grener eller force-push uten at Pål ber om det.
