# NOTES — løpende status

Kort og oppdatert. Varig datamodell, scoremodell og kartteknikk står i HANDOVER.md, og arbeidsreglene i CLAUDE.md.
Oppdateres ved slutten av hver økt (`/avslutt`).

## Status nå

Sist oppdatert: 11. november 2026.

- 11.11. kveld: Midtøsten er fylt inn som prøveregion (12 nye: BHR, ARE, JOR, KWT, OMN, QAT, SAU, IRQ, IRN, ISR, PSE, SYR),
  med `/nytt-reisemal`. Ramadan 2026–28 ligger i `felles_vinduer.json` for 13 reisemål; Iran har Nowruz, Israel pesach.
  Pål godkjente scorer og tone. Nord-Amerika er fylt inn samme kveld (9 nye: USA-NYC, USA-SOR, USA-FL, USA-SW, USA-RM, USA-AK,
  CAN-W, CAN-O, CAN-N; alle stasjoner 1991–2020), med Mardi Gras, Jazz Fest, Iditarod og Carnaval de Québec som vinduer.
  Resten (196 reisemål) ble fylt inn med en workflow (27 agenter etter /nytt-reisemal) samme kveld: alle 257 reisemål er nå på plass.
  Felles vinduer: ramadan (41 reisemål), påskeuka (58), ortodoks påske (3) og kinesisk nyttår (13), 2026–28, med egne justeringer
  og positiv tekst der høytiden er en opplevelse. Svakheter agentene meldte (183 av 196) står i `Kildesvakheter.md`.
  Kvalitetssjekk: ingen måneder over 38 °C med klima ≥ 4, koordinatene i riktig region, alle har engelsk.
- 11.11.: utvidelse mot alle FN-landene påbegynt. Steg 1 er gjort: dataene ligger i én JSON-fil per reisemål i `reisemal/`
  (norsk og engelsk side om side), lest av `reisemal.py`. `Reisemål.md` genereres. Alle 40 har `onskeliste: true`.
  Siden og regnearket har identiske data som før.
- 11.11.: steg 2 er flettet (PR #39): søkefelt i lista og «Vis: Alle reisemål / Ønskeliste» (skjult til det finnes
  reisemål utenfor ønskelisten). Testet med 250 oppdiktede reisemål; ni regioner gir fem rader med knapper.
- 5.11.: publiseringen er samlet og gjort robust. Én felles workflow for alle tre repoene (publiser.yml i paalstampe.github.io),
  som hopper over uendret innhold, og dokumentasjon og .claude/ publiseres ikke lenger (`.gitattributes`). Verifisert i alle tre:
  en commit som bare endrer dokumentasjon gir ingen ny publisering. Detaljer under Neste steg og i beslutningsloggen.
- 4.11. kveld: publiseringen feilet gjentatte ganger fordi Pages regnet en publisering som pågående lenge etter at den var
  ferdig («in progress deployment … Please cancel <sha> first»), eller hang til tidsavbruddet. GitHub hadde hendelser med
  Actions og Pages samme kveld. Alle tre repoene har nå kø (`cancel-in-progress: false`), rydding av Pages-publiseringer som
  henger, og tre forsøk med 5 min pause (byguider #102, reiseplanlegging #32, paalstampe.github.io #22).
  Ryddingen kan tørrkjøres med `RYDD_TORR=1`, og `.claude/valider.sh` sjekker YAML og avviser dupliserte nøkler i JSON og YAML
  (byguider #103–#104, reiseplanlegging #33–#34, paalstampe.github.io #24–#25).
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

- Utvidelse til alle FN-land (avtalt 11.11.; steg 1–2 ferdig, flyttbart kort PR #40): (3) landlista er vedtatt 11.11. (`Landliste.md` / `landliste.tsv`)
  (257 reisemål, 217 nye, 31 land delt, åtte regioner); regioner, felles vinduer og kortnavn er på plass (PR #41),
  og skillen `/nytt-reisemal` er oppskriften for datafyllingen;
  (4) fylle data per region. Regioninndelingen avgjøres med landlista, og da også knapper eller nedtrekksliste for regionene. Standardvalg til Pål sier noe annet: Europa er med, regnearket bygges fortsatt, venners egne
  ønskelister venter. Felles vinduer (ramadan, påske o.l. for mange land) bør inn i `reisemal.py` før datafyllingen.
  Kalenderformlene i regnearket (COUNTIFS/SUMIFS/SUMPRODUCT per celle) blir trege ved ~250 reisemål; vurder å regne ukescorene i Python.
- Publiseringen er felles for alle tre: `pages.yml` kaller `paalstampe/paalstampe.github.io/.github/workflows/publiser.yml@main`
  (paalstampe.github.io #23, byguider #105, reiseplanlegging #35). Endringer gjøres der og gjelder alle tre fra neste kjøring.
  Byguiders delingssider lages av `.github/etter-sammensetting.sh`. Første publisering på stam.pe ble blokkert i rundt 30 min
  (21:22–ca. 21:55) av en publisering som ifølge API-et var ferdig og ikke kunne avbrytes; tredje forsøk gikk gjennom.
- Publiseringen hopper over når innholdet er det samme som det som ligger ute (paalstampe.github.io #26, 5.11.): et avtrykk av
  alle filene ligger som `publisert.txt` og sammenlignes. Verifisert: første kjøring publiserte og neste hoppet over, i alle tre;
  ved fletting publiserte push-kjøringen og sletting av grenen hoppet over. Pages kan likevel henge på én enkelt publisering:
  4.11. kl. 22:20 tidsavbrøt alle tre forsøkene på stam.pe (en NOTES-commit). Fikk dette ofte, er neste skritt lengre ventetid.
- Dokumentasjon og Claude-oppsett (CLAUDE.md, NOTES.md, HANDOVER.md, SMAK.md, README.md, .claude/, .github/) publiseres ikke
  lenger, heller ikke i forhåndsvisningene (paalstampe.github.io #27, 5.11.). En commit som bare endrer dokumentasjon gir da ingen
  ny publisering. Byguidenes data/*.md publiseres som før. Hvert repo bestemmer selv hva som ikke publiseres, med `export-ignore` i `.gitattributes`
  (byguider #106, reiseplanlegging #36, paalstampe.github.io #28); ny fil som ikke skal på nettsiden legges inn der.
- Finjuster scorene etter Påls vurdering.
- Legg inn nye bevegelige datoer hvert år (Tet/kinesisk nyttår, påske, ramadan, tsechu) i `reisemal/<ID>.json`, og bygg på nytt.
  Vinduene dekker 2026–28, så 2029 må inn i løpet av 2028.
- Oppdater miniatyrene på stam.pe når kartet endrer utseende merkbart (CLAUDE.md, Miniatyrer).
- Kjenn på sveip og pinch (PR #21) på en ekte iPhone. I simulatoren virker begge (testet 4.11.), men følelsen må sjekkes på telefonen.
- Sjekk at delingskortet vises i Meldinger, Slack og e-post (bildet er live, men ikke sett i en app ennå).
- Nye eller endrede tekster trenger engelsk (`en` ved siden av `no` i `reisemal/<ID>.json`). `lag_reisekart.py` melder hull.

## Åpne spørsmål

- Scorene for de 196 er Claudes vurdering, ikke gjennomgått av Pål. Opplevelse kan være satt høyt for lite besøkte land.
- Midtøsten (11.11.): Palestina bruker Betlehems temperatur (periode ikke oppgitt) og Jerusalems nedbør (proxy, 10 km).
  Jordan er Amman 1989–2018 (Petra omtrent likt). Saudi-Arabia er Riyadh (AlUla litt kjøligere), Oman er Muscat (Salalah har khareef om sommeren).
- Svake klimaserier: noen stasjoner har gamle serier (Dili, Beirut, Galápagos, Hwange, São Tomé, Maun 1961–1990),
  og noen er proxy (Rote→Kupang, USA-WC→Vancouver, CRI→Liberia, ZWE→Hwange). Skal de byttes når bedre kilder finnes?
- Noen festivaldatoer er merket «sjekk dato».
- HANDOVER nevner en «HTML-visning generert fra Excel» som mulig neste steg. Er den fortsatt aktuell, nå som reisekartet finnes?
- Noen merknader er personlige planleggingsnotater («Rute avklares», «Evt. kombinert med …»). Sikkerhetsmerknadene
  viser til UDs reiseråd, på engelsk «Norwegian MFA travel advice». Skal de skrives om for andre brukere?
- De engelske tekstene er oversatt av Claude og ikke gjennomlest av Pål.

## Beslutningslogg

- 2026-11-11: Land med reiseråd vises som andre land, med varselet «Sjekk reiseråd». De skjules ikke og sorteres ikke lavere,
  selv om de kan havne øverst i lista (Pål valgte dette framfor et filter).
- 2026-11-11: Dataene ligger i én JSON-fil per reisemål (`reisemal/<ID>.json`), med norsk og engelsk side om side.
  Før måtte et reisemål legges inn fem steder, noe som ikke holder når lista skal utvides til alle FN-landene. JSON fordi det ikke krever
  avhengigheter og valideres av hooken. `Reisemål.md` genereres og er ikke lenger master. Alle dagens 40 har `onskeliste: true`.
- 2026-11-05: Hva som ikke publiseres, står i hvert repos `.gitattributes` (`export-ignore`), ikke i den felles workflowen.
  git archive respekterer det, også for forhåndsvisningene. Bieffekt: GitHubs «Download ZIP» mangler dokumentasjonen.
- 2026-11-05: Dokumentasjonen publiseres ikke. Det er ikke for å skjule noe (repoene er offentlige), men så commits som bare
  endrer dokumentasjon ikke gir nye publiseringer, som er det som henger hos Pages.
- 2026-11-05: Publiseringen hopper over når innholdet er likt det som er ute (avtrykk i `publisert.txt`). Gjentatte
  publiseringer av samme innhold var det som oftest hang hos Pages 4.11.
- 2026-11-04: Publiseringen bruker den felles workflowen i paalstampe.github.io (`publiser.yml@main`), så kø, rydding og forsøk
  bare vedlikeholdes ett sted. Ulempen er at en feil der rammer alle tre.
- 2026-11-04: Publiseringen rydder Pages-publiseringer som henger og prøver tre ganger med 5 min pause. Ferdige publiseringer
  («succeed») kan ikke avbrytes, selv når Pages sier de blokkerer; da hjelper bare venting. Lengre pauser er ikke lagt inn, siden
  blokkeringen 4.11. varte over 22 min og må løses ved årsaken.
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
- 2026-09-25: `Reise - utenfor Europa.md` er masterlisten over reisemål (erstattet 11.11.2026 av `reisemal/`).
- 2026-09-25: Sri Lanka er delt i LKA-SV og LKA-O. Stan-landene er slått sammen med Silkeveien (SILK).
- 2026-09-27: Navnene er endret (USA Nordvestkyst, Hawaii, Mexico City, Savannah-Charleston m.fl.), og kartetikettene har tankestrek mellom land og sted.
- 2026-10-04: Hele sidepanelet ruller på desktop. Varianten med kompakte filtre ble prøvd, men ikke valgt.
- 2026-10-15: Mørk modus følger enheten, og siden er ikke søkbar (noindex).
- 2026-10-18: Løpende status føres i NOTES.md, og HANDOVER.md er referanse.
- 2026-10-18: Ubrukte filer er slettet: det gamle regnearket («Gammel - Reiseidéer og reisekalender.xlsx»), style.css (bare forbilde) og det utdaterte oppsettnotatet for GitHub Pages.
- 2026-10-28: Kartet finnes på norsk og engelsk med samme språkbryter og nøkkel som byguidene. Regnearket er bare på norsk.
- 2026-10-28: Siden viser ikke til regnearket (ingress, bunntekst, «se Vinduer»). Andre brukere kjenner det ikke.
