# NOTES — løpende status

Kort og oppdatert. Varig datamodell, scoremodell og kartteknikk står i HANDOVER.md, og arbeidsreglene i CLAUDE.md.
Oppdateres ved slutten av hver økt (`/avslutt`).

## Status nå

Sist oppdatert: 4. november 2026.

- 4.11. kveld: verktøyoversikten (claude-oppsett#1). `.claude/valider.sh` sjekker nå også filer endret i Bash
  (sed, skript): JSON/GeoJSON/Python som git ser som endret siden forrige godkjenning, og melder en ødelagt fil til den er rettet.
  Stop-hooken `sky-push.sh` har `onFailure: block`. CLAUDE.md: vent med `gh run watch` før skjermbilder av forhåndsvisningen,
  og kjør axe-core ved UI-endringer. `/doctor prompt-audit` er kjørt på reglene og funnene er rettet. Ferdig flettede lokale grener er slettet.
  Tilgjengelighet: kartflaten har role=main (PR #29), og «best» i mørk modus er mørkere grønn #23804A (PR #30), så hvit tekst
  får kontrast 4,9:1 (før 3,88:1). Dokumentasjonen bruker port 8001 for lokal server. Hooks: PR #28.
- 4.11.: Claude-oppsett. `.claude/launch.json` lar Claude-appen starte serveren i den innebygde nettleseren (8000 byguider,
  8001 reiseplanlegging, 8002 stam.pe). Hooks: `.claude/oppstart.sh` sjekker ved oppstart om repoet ligger bak eller foran origin
  (henter selv når det er trygt) og om /avslutt avviker fra claude-oppsett; `.claude/valider.sh` sjekker JSON/GeoJSON/Python
  etter hver filendring; `.claude/sky-push.sh` holder skyøkter igjen til committede endringer er pushet.
  Claude kjører /code-review og /simplify selv før fletting av kodeendringer.
- 4.11.: liggende iPhone testet i iOS-simulatoren. Kartet går nå helt ut til skjermkantene (`viewport-fit=cover`, PR #23);
  før lot Safari 68 pt stå tomt på hver side. Panelet vokser med innfellingen ved Dynamic Island, og detaljkortet
  holdes over hjemlinjen.
- 4.11.: nettbrett (PR #24). Stående iPad og ⅔ delt skjerm (700–1023 px) har panelet på 340 px ved siden av kartet.
  Mobilbrytepunktet er flyttet fra 900 til 699 px. Testet i simulatoren (iPad Air 11" stående, og rotert til liggende og tilbake med siden åpen) og med Playwright.
- 4.11.: mobil (PR #22). Stående har «Liste ↓» i kartet og fast «Kart ↑» når kartet er rullet bort, som i byguidene.
  Liggende har panelet i en smal kolonne til venstre og kartet i full høyde. Testet i Playwright, ikke på iPhone.
- 4.11.: kartet går rundt jorda øst–vest og kan ikke dras ut av bildet nord–sør (PR #21). Zoom 1 fyller nå hele
  bredden av kartflaten (før ca. 80 %). Ekte jordklode ble vurdert og valgt bort, se beslutningsloggen.
  Miniatyrene på stam.pe er tatt på nytt i lys og mørk (paalstampe.github.io).
- 1.11.: frimerke-ikonet heter nå `ikon-frimerke.png` (PR #20). Med samme filnavn kunne iOS vise det gamle
  «r»-ikonet ved deling. `apple-touch-icon.png` ligger igjen som kopi for gamle lenker.
- Reisekartet er live på https://stam.pe/reiseplanlegging/, og Reisekalender.xlsx bygges fra de samme dataene.
- Alle 40 reisemål er fylt ut med klimanormaler, delscorer, begrunnelser og 49 vinduer. Vinduene dekker
  bevegelige høytider for 2026–28, festivaler og dyrelivshendelser.
- Kartet har hjemskjermikon, virker offline (også «Lagre alt» fra stam.pe), har mørk modus og er ikke søkbart.
- 28.10.: kartet finnes på engelsk (PR #12). Bryteren NO / EN står i brødsmulene, og valget deles med byguidene
  og stam.pe. Innholdet er oversatt i `reisedata_en.py`. Ingressen og bunnteksten nevner ikke lenger regnearket,
  og «se Vinduer» vises som «se hendelser» i kartet (PR #13–#14). Kartet bytter farger med en gang når
  enheten bytter mellom lys og mørk modus (PR #15).
- 31.10.: egen 404-side (kopi av den på stam.pe, PR #18). Ukjente adresser under stam.pe/reiseplanlegging/ viste før
  GitHubs standardside. Endres 404.html, gjøres det i paalstampe.github.io og kopieres hit.
- 31.10.: delingskort (PR #19). `deling.png` er en luftpostkonvolutt med klode-frimerke, malen har og:-tagger, og hjemskjermikonet er
  et frimerke med «r». Lages med `.claude/delingsbilder.sh`.
- Det finnes ingen åpne grener utenom `main`.

## Neste steg

- Finjuster scorene etter Påls vurdering.
- Legg inn nye bevegelige datoer hvert år (Tet/kinesisk nyttår, påske, ramadan, tsechu) i `reisedata.py`, og bygg på nytt.
  Vinduene dekker 2026–28, så 2029 må inn i løpet av 2028.
- Oppdater miniatyrene på stam.pe når kartet endrer utseende merkbart (CLAUDE.md, Miniatyrer).
- Kjenn på sveip og pinch (PR #21) på en ekte iPhone. I simulatoren virker begge (testet 4.11.), men følelsen må sjekkes på telefonen.
- Sjekk at delingskortet vises i Meldinger, Slack og e-post (bildet er live, men ikke sett i en app ennå).
- Nye eller endrede tekster i `reisedata.py` trenger engelsk i `reisedata_en.py`. `lag_reisekart.py` melder hull.

## Åpne spørsmål

- Svake klimaserier: noen stasjoner har gamle serier (Dili, Beirut, Galápagos, Hwange, São Tomé, Maun 1961–1990),
  og noen er proxy (Rote→Kupang, USA-WC→Vancouver, CRI→Liberia, ZWE→Hwange). Skal de byttes når bedre kilder finnes?
- Noen festivaldatoer er merket «sjekk dato».
- HANDOVER nevner en «HTML-visning generert fra Excel» som mulig neste steg. Er den fortsatt aktuell, nå som reisekartet finnes?
- Noen merknader er personlige planleggingsnotater («Rute avklares», «Evt. kombinert med …»). Sikkerhetsmerknadene
  viser til UDs reiseråd, på engelsk «Norwegian MFA travel advice». Skal de skrives om for andre brukere?
- De engelske tekstene er oversatt av Claude og ikke gjennomlest av Pål.

## Beslutningslogg

- 2026-11-04: «Best» i mørk modus er #23804A med hvit tekst (variant B). Alternativet med mørk tekst på dagens grønn ble valgt bort:
  da ble «best» og «bra» for like, og lys modus har hvit tekst.
- 2026-11-04: valider.sh kjører også etter Bash, siden auto mode ofte endrer filer med sed og skript, som før gikk utenom sjekken.
- 2026-11-04: UI-endringer sjekkes med axe-core (lys og mørk) før fletting. Brudd som krever nye farger tas med Pål.
- 2026-11-04: Claude kjører /code-review og /simplify selv før fletting av kodeendringer, så Pål slipper å be om det.
- 2026-11-04: Git-sjekk ved oppstart og push-vakt i sky ligger som hooks i repoet (ikke bare som regel), så de virker både lokalt og i skyøkter.
- 2026-11-04: Nettbrett (700–1023 px) får panelet ved siden av kartet (340 px), som byguidene. Stående iPad fikk
  telefonoppsettet med et høyt kart og lista i full bredde under.
- 2026-11-04: `viewport-fit=cover` i malen, så kartet går ut til kantene i liggende og safe-area-verdiene virker.

- 2026-11-04: Liggende mobil får panelet ved siden av kartet, som byguidene. Stående får «Liste ↓»/«Kart ↑».
  Kartet fylte nesten hele skjermen når telefonen lå, og man ble fortapt i det.

- 2026-11-04: Flatt kart som går rundt jorda øst–vest, ikke jordklode. En klode viser bare halve jorda om gangen
  (oversikten over alle mål er poenget) og ville krevd echarts-gl eller MapLibre med kartfliser.

- 2026-11-01: Et ikon eller delingsbilde som byttes, får nytt filnavn (se HANDOVER). iOS viste det gamle bokstavikonet
  ved deling, fordi frimerket hadde overtatt samme fil.
- 2026-10-31: Delingsbildet er luftpost, i samme postale familie som stam.pe (konvolutt med PS-frimerke) og byguidene (postkort).
- 2026-09-25: Vektene er 40/40/20, og vetoet er myket opp til et tak på 1,5. Trengsel/pris er én dimensjon.
- 2026-09-25: `Reise - utenfor Europa.md` er masterlisten over reisemål.
- 2026-09-25: Sri Lanka er delt i LKA-SV og LKA-O. Stan-landene er slått sammen med Silkeveien (SILK).
- 2026-09-27: Navnene er endret (USA Nordvestkyst, Hawaii, Mexico City, Savannah-Charleston m.fl.), og kartetikettene har tankestrek mellom land og sted.
- 2026-10-04: Hele sidepanelet ruller på desktop. Varianten med kompakte filtre ble prøvd, men ikke valgt.
- 2026-10-15: Mørk modus følger enheten, og siden er ikke søkbar (noindex).
- 2026-10-18: Løpende status føres i NOTES.md, og HANDOVER.md er referanse.
- 2026-10-18: Ubrukte filer er slettet: det gamle regnearket («Gammel - Reiseidéer og reisekalender.xlsx»), style.css (bare forbilde) og det utdaterte oppsettnotatet for GitHub Pages.
- 2026-10-28: Kartet finnes på norsk og engelsk med samme språkbryter og nøkkel som byguidene. Regnearket er bare på norsk.
- 2026-10-28: Siden viser ikke til regnearket (ingress, bunntekst, «se Vinduer»). Andre brukere kjenner det ikke.
