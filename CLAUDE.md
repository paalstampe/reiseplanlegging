Gjeldende status (lastes inn automatisk):
@NOTES.md

# Reiseplanlegging — arbeidsregler for Claude

Påls reisekart og reisekalender: beste reisetid per reisemål, ned mot ukenummer. 259 reisemål som dekker alle FN-land
(`Landliste.md`); Påls egne 44 er på ønskelisten. Kjente svakheter i kildene: `Kildesvakheter.md`.
Live på https://stam.pe/reiseplanlegging/.
Løpende status, neste steg, åpne spørsmål og beslutningslogg: NOTES.md (oppdateres ved slutten av hver økt).
Les HANDOVER.md før større endringer — den har datamodell, scoremodell og kartteknikk.
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
  legg til «hel» for hele siden og «mork» for mørk modus. Tillatt: https://stam.pe/... og http://localhost:<port>/... (eller 127.0.0.1)
  (kjør python3 -m http.server 8001 --bind 127.0.0.1 i repoet først — gir rask sjekk før push). Virker i skyen og på Macen;
  på Macen kreves Node og Playwright (installasjon øverst i skriptet). Kartet tegnes med ECharts og krever
  ingen nøkkel, så det virker også fra localhost.
- iPhone-spesifikt (liggende, notch/Dynamic Island, safe area, Safaris verktøylinje, rotasjon): bruk
  iOS-simulatoren (Xcode er installert på Macen) via simulatorverktøyet, f.eks. åpne URL i Safari og rotere.
  Playwright holder for vanlige layoutsjekker og er raskere; simulatoren er sluttsjekken for iPhone. Ikke i skyøkter.
- Test samspill (hover, klikk, trykk, pinch) med Playwright, også på mobilbredde. zrender krever
  mousedown/mouseup før click.
- UI-endringer: kjør axe-core i nettleserpanelet før fletting (last https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js
  med javascript_tool, så `axe.run()`), i lys og mørk modus. Rett brudd; kontrast som krever nye farger tas med Pål.
- Før fletting av kodeendringer: kjør /code-review (standardnivå) og /simplify på grenen selv, uten at Pål ber om det.
  Rett funnene som holder, nevn kort i PR-beskrivelsen hva som ble funnet og rettet. Gjelder ikke rene data- og tekstendringer.
- Fletting: Kan du selv verifisere at alt er i orden (skjermbilder mobil + desktop, ingen JS-feil),
  åpne PR og flett uten å spørre. Er det noe Pål bør se på (designvalg, smak, scorer, usikkerhet), push grenen,
  oppgi forhåndsvisningen og vent — flett når han sier ok.
- Lokal økt på Påls Mac: skal Pål se på noe, start serveren selv om den ikke kjører
  (python3 -m http.server 8001 --bind 127.0.0.1, i bakgrunnen) og åpne siden for ham med
  open http://localhost:8001/ (generer index.html først). Stopp serveren når han er ferdig. I skyøkter: bruk forhåndsvisningen.
- Desktop-appen: .claude/launch.json starter serveren på port 8001 i appens innebygde nettleser
  (preview_start), der du kan se, klikke og lese konsollen selv. Portene er 8000 byguider, 8001 reiseplanlegging,
  8002 stam.pe, så alle tre kan kjøre samtidig.
- Hooks i .claude/settings.json: ved oppstart sjekker .claude/oppstart.sh om grenen ligger bak eller foran origin
  (henter selv med pull --ff-only når det er trygt) og om felles filer avviker fra claude-oppsett — følg det den sier. oppstart.sh, valider.sh, sky-push.sh og /avslutt
  er kopier: endre originalen i claude-oppsett og kjør synk-repoer.sh der.
  .claude/valider.sh sjekker JSON/GeoJSON/YAML/Python (også dupliserte nøkler) etter hver Write/Edit, og etter Bash-kommandoer filene git ser som endret.
  I skyøkter stopper .claude/sky-push.sh ikke før committede endringer er pushet.
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
- Bevegelse skal føles som MapLibre i byguidene. Touch (hover: none): tooltip av, trykk åpner detaljkortet, egen pinch/pan
  (`touchRoam`) som følger fingrene 1:1, glir videre etter sveip (`GLI_TID`) og zoomer inn ved dobbelttrykk. Under gesten
  flyttes/skaleres bildet med CSS-transform, og kartet tegnes på nytt ved slipp. PC: trinnløs hjul-/styreflatezoom rundt pekeren
  (`hjulZoom`), ECharts tar bare panorering. Knappene zoomer animert (`animerZoom`, `ZOOM_TID`).
  `animation:false`. iOS trenger `cursor:pointer` på body for at trykk gir klikk.
- PC: tooltip etter `HOVER_FORSINKELSE` (400 ms). Treff = nærmeste prikk innen 12 px (PC) / 24 px (touch).
- Zoomknapper i samme stil som byguidenes MapLibre-kontroller (`zoomKnapper()`).
- Kartet går rundt jorda øst–vest (tre kopier, `KOPIER`) og stopper nord–sør (`holdInnenfor()`).
  Ikke jordklode (begrunnelse i beslutningsloggen). På touch tegnes kartet tre skjermbredder bredt.
- Mobil: stående har «Liste ↓»/«Kart ↑» (`#til-lista`), liggende har panelet ved siden av kartet (`LIGGENDE`),
  begge som i byguidene. Mobil er under 700 px; 700–1023 px er nettbrett med panelet ved siden av kartet.
  Test layoutendringer i stående og liggende.
- Delingskort (`deling.png`, luftpost) og hjemskjermikon (frimerke med «r») lages med `.claude/delingsbilder.sh`;
  `delingsbilder.html` er en identisk kopi fra byguider. og:-taggene står i malen.
- Ikoner og delingsbilder som byttes, får nytt filnavn (iOS husker gamle bilder etter adresse). Se HANDOVER.
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
- Mørk modus følger enheten: @media i reisekart_mal.html (papir #1B1814, tekst #ECE5D8, dempet #A6987F,
  kobber #C99158). Nye farger skal være CSS-variabler i begge utgaver.

## Miniatyrer (gjelder alle tre repoene)
Småbildene finnes flere steder, alle i en lys og en mørk utgave (`-mork.webp`, vises i mørk modus):
- stam.pe-forsiden og 404-siden (repo `paalstampe.github.io`): `bilder/byguider(-mork).webp` (tatt av Nice-guiden,
  `/byguider/nice/`) og `bilder/reiseplanlegging(-mork).webp`.
- Byguide-forsiden (repo `byguider`): `bilder/<by>(-mork).webp` for hver by, laget med `.claude/miniatyrer.sh`
  (lager begge utgavene).
Når et småbilde oppdateres — en app eller by har endret utseende, eller en ny by eller app kommer til —
oppdater alle bildene som viser den, i alle repoene og i begge utgavene, og sjekk forsidene i lys og mørk modus.
Oppskrift: viewport 1300×900, deviceScaleFactor 2, beskjær 1200×900 fra venstre, skaler til 360×270 webp,
Playwright med `colorScheme: 'light'` og `'dark'`. Ta bildene fra stam.pe etter at endringen er publisert.

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
