Gjeldende status (lastes inn automatisk):
@NOTES.md

# Reiseplanlegging — arbeidsregler for Claude

Påls reisekart og reisekalender: beste reisetid per reisemål, ned mot ukenummer. 259 reisemål som dekker alle FN-land
(`Landliste.md`); Påls egne 44 er på ønskelisten. Kjente svakheter i kildene: `Kildesvakheter.md`.
Live på https://stam.pe/reiseplanlegging/.
Løpende status, neste steg, åpne spørsmål og beslutningslogg: NOTES.md (oppdateres ved slutten av hver økt).
Les HANDOVER.md før større endringer — den har datamodell, scoremodell og kartteknikk.
Løsninger som deles med byguidene (kartbevegelse, søk, detaljkort, språk, offline m.m.) skal være like: se HANDOVER, «Felles med byguidene», og endre begge.
Hold HANDOVER.md oppdatert når noe vesentlig endres (filer, besluttet design, navneendringer).
Spar kontekst: NOTES.md holdes under ca. 10 KB (den lastes i hver økt); eldre status og beslutningslogg ligger i ARKIV.md.
Les aldri genererte eller store filer hele: `index.html` (~700 KB, generert), `Reisekalender.xlsx`, `Kildesvakheter.md` (~40 KB),
`reisekart_mal.html` (~64 KB). Finn stedet med grep og les utsnitt (offset/limit); data leses fra `reisemal/<ID>.json`.

## Språk
- Svar Pål på norsk, direkte og konsist. Ikke forklar grunnleggende git- eller webbegreper.
- Commit-meldinger, PR-titler og -beskrivelser på norsk. Commit-stil: «Område: hva som er endret»
  (f.eks. «Kart: trykk på tomt kart lukker detaljkortet»).
- Kode: norske navn på variabler og funksjoner, som i resten av koden.
- Siden finnes på norsk og engelsk (NO / EN i brødsmulene). Faste tekster står i `TEKST` i malen,
  innholdet står med norsk og engelsk side om side i `reisemal/<ID>.json`. Nye UI-tekster og nye data skal alltid ha begge språk.

## Filer og generering
- `reisemal/<ID>.json` — all data, én fil per reisemål: region, land, sted, status, ønskeliste, kategori, merknad,
  koordinater, klimakilde, 12 måneder (scorer, T maks, nedbør, begrunnelse) og vinduer. Norsk (`no`) og engelsk (`en`)
  står side om side. Endres en norsk tekst, endre den engelske også. `lag_reisekart.py` skriver «Mangler engelsk: …» for hull.
  Format og felter: HANDOVER.md, Datamodell. Filene skrives med `reisemal.skriv()` (én måned og ett vindu per linje).
- `reisemal.py` — leser og sjekker filene (`last()`, med vinduene fra `felles_vinduer.json`), regner vinduer om til uker (`vindu()`).
  Brukes av begge skriptene. Nye regioner legges inn i `REGIONER` der, med engelsk navn.
- `Reisemål.md` — oversikt over reisemålene, generert av `lag_reisekart.py`. Rediger ikke; endre JSON-filene.
- `reisekart_mal.html` — malen for kart-appen. `python3 lag_reisekart.py` skriver `index.html` fra mal + data.
- `index.html` er generert — rediger aldri direkte. Endre malen eller dataene og kjør skriptet.
  Generert `index.html` committes alltid sammen med endringen den kommer fra.
- `python3 bygg_reisekalender.py` bygger `Reisekalender.xlsx` (krever openpyxl). Bygg på nytt når
  dataene endres, og commit den sammen med dataendringen.

## Arbeidsflyt
- Endringer som ikke trenger forhåndsvisning — data (`reisemal/`) med generert `Reisemål.md`, `index.html` og `Reisekalender.xlsx`, og dokumentasjon
  (CLAUDE.md, HANDOVER.md, README.md) — pushes rett til main, uten gren og PR.
- Kodeendringer (`reisekart_mal.html`, `lag_reisekart.py`, `bygg_reisekalender.py`, `reisemal.py`, `.github/`, `.claude/`)
  på egen gren. Push grenen; forhåndsvisningen er https://stam.pe/reiseplanlegging/forhandsvisning/<gren>/
  (klar 1–2 min etter push, bygges av .github/workflows/pages.yml). Husk at `index.html` må være generert
  og committet på grenen.
- Publiseringen er felles for stam.pe, byguider og reiseplanlegging: `.github/workflows/pages.yml` kaller `publiser.yml` i
  paalstampe.github.io (endres der, gjelder alle tre). Den hopper over uendret innhold (`publisert.txt`), rydder Pages-publiseringer
  som henger og prøver tre ganger. Filer som ikke skal på nettsiden (dokumentasjon, .claude/), merkes `export-ignore` i `.gitattributes`.
- Etter push av en gren: vent på publiseringen før skjermbilder av forhåndsvisningen, i bakgrunnen med
  `gh run watch $(gh run list --commit $(git rev-parse HEAD) -L1 --json databaseId -q '.[0].databaseId') --exit-status`
  (kjøringen dukker opp noen sekunder etter push).
- Sjekk designet selv: .claude/skjermbilde.sh <url> <fil.png> 390 844 (mobil) og 1300 900 (desktop);
  legg til «hel» for hele siden, «mork» for mørk modus, «kart=zoom,lon,lat» for et kartutsnitt og «mnd=1–12» for måned
  (f.eks. `kart=12,6,6 mnd=12`: Vest-Afrika på dypeste zoom i desember). Tillatt: https://stam.pe/... og http://localhost:<port>/... (eller 127.0.0.1)
  (kjør python3 -m http.server 8001 --bind 127.0.0.1 i repoet først — gir rask sjekk før push). Virker i skyen og på Macen;
  på Macen kreves Node og Playwright (installasjon øverst i skriptet). Kartet tegnes med ECharts og krever
  ingen nøkkel, så det virker også fra localhost.
- iPhone-spesifikt (liggende, notch/Dynamic Island, safe area, Safaris verktøylinje, rotasjon): bruk
  iOS-simulatoren (Xcode er installert på Macen) via simulatorverktøyet, f.eks. åpne URL i Safari og rotere.
  Playwright holder for vanlige layoutsjekker og er raskere; simulatoren er sluttsjekken for iPhone. Ikke i skyøkter.
  En nyoppstartet simulator kan henge i Safari (openurl gir tidsavbrudd); da er Playwright med WebKit (`devices['iPhone 13']`)
  reserven. Touch-hendelser lages der med `new Event('touchstart')` og `touches` lagt på, siden `new Touch()` ikke finnes.
- Kartvisning i nettleserpanelet: `settVisning(zoom, [lon, lat])` med javascript_tool hopper rett til et utsnitt (samme som `kart=` over).
- Test samspill (hover, klikk, trykk, pinch) med Playwright, også på mobilbredde. zrender krever
  mousedown/mouseup før click.
  Endres kartbevegelsen (touchRoam, hjulZoom, animerZoom, zoomRundt), kjør `.claude/bevegelsestest.sh [url]`: hjul, knapper,
  pinch, glid og dobbelttrykk i Chromium og WebKit, med OK/FEIL per sjekk.
- UI-endringer: kjør `.claude/axe.sh <url> [bredde høyde] [js=<kode>]` før fletting (axe-core via Playwright, lys og mørk modus).
  Detaljkortet sjekkes med f.eks. `"js=state.mnd=0; oppdater(); visDetalj('JPN-HOK')"`. Rett brudd; kontrast som krever nye farger tas med Pål.
- Før fletting av kodeendringer: kjør /code-review (standardnivå) og /simplify på grenen selv, uten at Pål ber om det.
  Rett funnene som holder, nevn kort i PR-beskrivelsen hva som ble funnet og rettet. Gjelder ikke rene data- og tekstendringer.
- Fletting: Kan du selv verifisere at alt er i orden (skjermbilder mobil + desktop, ingen JS-feil),
  åpne PR og flett uten å spørre. Er det noe Pål bør se på (designvalg, smak, scorer, usikkerhet), push grenen,
  oppgi forhåndsvisningen og vent — flett når han sier ok.
- Lokalt: generer index.html og start serveren (preview_start i desktop-appen via .claude/launch.json, ellers
  python3 -m http.server 8001 --bind 127.0.0.1 i bakgrunnen og open http://localhost:8001/). Stopp den når Pål er ferdig.
  Portene er 8000 byguider, 8001 reiseplanlegging, 8002 stam.pe. I skyøkter: bruk forhåndsvisningen.
- Hooks (.claude/settings.json): oppstart.sh sjekker grenen mot origin og felles filer mot claude-oppsett — følg det den sier.
  valider.sh sjekker JSON/YAML/Python etter endringer; sky-push.sh krever push i skyøkter. Hookene og /avslutt er kopier:
  endre originalen i claude-oppsett og kjør synk-repoer.sh der.
- Kode- og designoppgaver i en skyøkt: si fra tidlig at de egner seg bedre lokalt (fortsett hvis Pål vil).
- GitHub sletter grenen ved fletting; slett den selv bare hvis den ligger igjen (git ls-remote --heads origin).
- Én endring per gren. Små, selvstendige commits.

## Teknikk (kort — detaljer i HANDOVER.md)
- Ingen rammeverk, ingen npm. Eneste byggesteg er Python-skriptene over (standardbibliotek + openpyxl).
- Kart: ECharts 5.5.1 + echarts@4.9.0 world.js fra jsDelivr (cdnjs ga 404), lastes dynamisk med AMD skjult.
- Malen er et komplett HTML-dokument med doctype og viewport-meta — uten viewport blir alt bitte lite på mobil.
- Bevegelse skal føles som MapLibre i byguidene: egen pinch/pan på touch (`touchRoam`, CSS-transform under gesten, omtegning
  ved slipp), trinnløs hjulzoom på PC (`hjulZoom`), animerte knapper (`animerZoom`). Detaljer i HANDOVER.
  iOS trenger `cursor:pointer` på body for at trykk gir klikk. Treff = nærmeste prikk innen 12 px (PC) / 24 px (touch).
- Kartet går rundt jorda øst–vest (tre kopier, `KOPIER`) og stopper nord–sør (`holdInnenfor()`).
  Ikke jordklode (begrunnelse i beslutningsloggen). På touch tegnes kartet tre skjermbredder bredt.
- Mobil er under 700 px; 700–1023 px er nettbrett med panelet ved siden av kartet. Test layoutendringer i stående og liggende.
- Delingskort og hjemskjermikon lages med `.claude/delingsbilder.sh` (kopi fra byguider). Bilder som byttes, får nytt filnavn
  (iOS husker gamle bilder etter adresse).
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
- Mørk modus følger enheten: @media i reisekart_mal.html (papir #1B1814, tekst #ECE5D8, dempet #A6987F,
  kobber #C99158). Nye farger skal være CSS-variabler i begge utgaver.

## Miniatyrer
Småbildene av reisekartet på stam.pe (lys og mørk) oppdateres når kartet endrer utseende merkbart.
Oppskrift og alle stedene de finnes: byguidenes CLAUDE.md, «Miniatyrer (gjelder alle tre repoene)».

## Data
- Nye reisemål: følg skillen `/nytt-reisemal` (`.claude/skills/nytt-reisemal/`). Ny fil `reisemal/<ID>.json` (ID = ISO3-landkode, med suffiks for deler av land: `IND-GOA`).
  Hvilke reisemål som skal finnes, står i `landliste.tsv` (vedtatt 11.11.2026).
  Deling, sammenslåing og ny ID: `omorganiser.py` i samme skill (steg 7). `Landliste.md`-tabellene lages fra `landliste.tsv`.
  Klimanormaler fra én representativ stasjon (helst WMO/nasjonal met-tjeneste, 1991–2020); oppgi kilde og periode.
  Si fra hvis stasjonen er en proxy eller serien er gammel.
- Bevegelige datoer (Tet/kinesisk nyttår, påske, ramadan, tsechu, festivaler) legges inn per år. Gjelder de mange reisemål,
  legges de i `felles_vinduer.json` med `gjelder`-liste, ikke i hver fil.
  Merk usikre datoer «sjekk dato».

## Ikke gjør
- Ikke rediger `index.html` direkte.
- Ikke legg inn avhengigheter, byggeverktøy eller rammeverk.
- Ikke slett uflettede grener eller force-push uten at Pål ber om det.
