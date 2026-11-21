# NOTES — løpende status

Kort og oppdatert. Varig datamodell, scoremodell og kartteknikk står i HANDOVER.md, og arbeidsreglene i CLAUDE.md.
Oppdateres ved slutten av hver økt (`/avslutt`).
Eldre status per dato og eldre beslutninger ligger i ARKIV.md (lastes ikke automatisk; grep der ved behov).

## Status nå

Sist oppdatert: 20. november 2026.

- 20.11.: tilbakeknappen (Android, sveip tilbake, nettleserens ←) lukker detaljkortet i stedet for å forlate siden (PR #63);
  likt i byguidene (`tilbakeLukker`, se «Felles med byguidene» i HANDOVER).
- 20.11.: pinch, dra og dobbelttrykk virker på PC med både mus og berøringsskjerm (`OGSA_TOUCH`, PR #64). Før zoomet pinch ikke der.
- 20.11.: Android (Galaxy S24, Pixel 10, Galaxy Tab S9) og Windows (faste rullefelt, musehjul, berøringsskjerm) er simulert med
  Playwright/Chromium mot stam.pe: layout, kort, tilbakeknapp og JS-feil OK. Ett hjulhakk zoomer ×1,35. Ikke sett på ekte enheter.

- 13.11.: toppsesong markeres uten å endre scoren (PR #57): opplevelse 5, klima ≤ 3 og samlet under 4,0 gir grønn ring på kartet,
  «Toppsesong» i lista, tooltip og kort og grønn rand i årsstripen. axe: ingen brudd.
- 13.11.: `.claude/axe.sh` kjører axe-core via Playwright i lys og mørk modus (axe i nettleserpanelet ble avvist i auto-modus).
  Felles fil fra claude-oppsett (synkes som hookene); `js=` kjører kode før sjekken, f.eks. for å åpne et kort.
- 11.11.: alle FN-land kom med (257 reisemål, nå 259); detaljer i ARKIV.md.
- Reisekartet er live på https://stam.pe/reiseplanlegging/, og Reisekalender.xlsx bygges fra de samme dataene.
- Kartet har hjemskjermikon, virker offline (også «Lagre alt» fra stam.pe), har mørk modus og er ikke søkbart.
- Det finnes ingen åpne grener utenom `main`.

## Neste steg

- Se over scorene for de ni nye eller endrede ønskelistereisemålene (VNM-N/C/S, BRA-RIO, BRA-NE, USA-CA, USA-NW, USA-SOR, IDN-KOM).
- Stikkprøver av scorene for de 217 nye: Pål tar dem når han bruker kartet og melder tilbake. Opplevelse kan være satt høyt
  for land få reiser til.
- Gå gjennom `Kildesvakheter.md` etter hvert (proxy-stasjoner, eldre serier, datoer merket «sjekk dato»).
- Regnearket har 259 rader; kalenderformlene (COUNTIFS/SUMIFS/SUMPRODUCT per celle) kan bli trege i Excel.
  Blir det et problem: regn ukescorene i Python og skriv verdier.
- Mulige forbedringer fra byguidene (ikke avtalt): lenke og «Del» til ett reisemål (`?sted=`, gjerne med måned), kategorifilter,
  og en jevnlig skyjobb som sjekker UDs reiseråd og oppdaterer sikkerhetsmerknadene. Venners egne ønskelister venter.
- Finjuster scorene etter Påls vurdering.
- Legg inn nye bevegelige datoer hvert år: felles høytider (ramadan, påske, ortodoks påske, kinesisk nyttår) i `felles_vinduer.json`,
  resten (Tet, tsechu, festivaler) i `reisemal/<ID>.json`, og bygg på nytt.
  Vinduene dekker 2026–28, så 2029 må inn i løpet av 2028.
- Oppdater miniatyrene på stam.pe når kartet endrer utseende merkbart (CLAUDE.md, Miniatyrer).
- Kjenn på zoom og panorering (PR #51) på en ekte iPhone og på Macens styreflate. Glidelengden (`GLI_TID`) og hjulfarten
  (0,003/0,01 i `hjulZoom`) er lette å justere.
- Sjekk at delingskortet vises i Meldinger, Slack og e-post (bildet er live, men ikke sett i en app ennå).
- Nye eller endrede tekster trenger engelsk (`en` ved siden av `no` i `reisemal/<ID>.json`). `lag_reisekart.py` melder hull.

- Firefox er aldri testet: Playwrights Firefox (v155) starter ikke på denne Macen («Could not find profile folder», også direkte).
  Prøv igjen etter en Playwright-oppdatering, eller test på en maskin med Firefox.
- Ikke sett på ekte Android eller Windows (bare simulert 20.11.). Tilbakeknappen og pinch på PC med berøringsskjerm er det som bør kjennes på.

## Åpne spørsmål

- Scorene for de 196 er Claudes vurdering, ikke gjennomgått av Pål. Opplevelse kan være satt høyt for lite besøkte land.
- Midtøsten (11.11.): Palestina bruker Betlehems temperatur (periode ikke oppgitt) og Jerusalems nedbør (proxy, 10 km).
  Jordan er Amman 1989–2018 (Petra omtrent likt). Saudi-Arabia er Riyadh (AlUla litt kjøligere), Oman er Muscat (Salalah har khareef om sommeren).
- Svake klimaserier: noen stasjoner har gamle serier (Dili, Rio 1981–2010, Da Nang og Saigon uten oppgitt periode, Beirut, Galápagos, Hwange, São Tomé, Maun 1961–1990),
  og noen er proxy (Rote→Kupang, CRI→Liberia, ZWE→Hwange). Skal de byttes når bedre kilder finnes?
- Noen festivaldatoer er merket «sjekk dato».
- HANDOVER nevner en «HTML-visning generert fra Excel» som mulig neste steg. Er den fortsatt aktuell, nå som reisekartet finnes?
- Noen merknader er personlige planleggingsnotater («Rute avklares», «Evt. kombinert med …»). Sikkerhetsmerknadene
  viser til UDs reiseråd, på engelsk «Norwegian MFA travel advice». Skal de skrives om for andre brukere?
- De engelske tekstene er oversatt av Claude og ikke gjennomlest av Pål.

## Beslutningslogg

- 2026-11-20: Et åpent kort er et eget steg i nettleserhistorikken (`kort` i history.state), så tilbakeknappen på Android lukker kortet i stedet for å forlate siden. Lukkes kortet på annen måte, går siden ett steg tilbake så historikken ikke fylles opp.
- 2026-11-20: PC med mus og berøringsskjerm får touch-styringen i tillegg til musestyringen, med touch-hendelsene stoppet før ECharts. Å la ECharts ta én finger og vår kode ta pinch ble forkastet: overgangen 1→2 fingre ville gitt to som panorerer samtidig.
- 2026-11-16: På mobil (stående) starter kartet under statuslinja (`.app` padding-top = safe-area-inset-top, `html` scroll-padding-top). Med viewport-fit=cover lå kartet under klokka, og iOS 26 Safari demper det området, inkludert +-knappen. Gjort likt i byguidene og reiseplanleggingen.
- 2026-11-13: Toppsesong (opplevelse 5, klima ≤ 3, samlet < 4,0) vises med grønn ring, merke og rand i årsstripen i stedet for å endre formelen eller klimascoren: grønt skal fortsatt bety samlet ≥ 4,0 overalt. Kravet klima ≤ 3 holder ute steder som bare trekkes ned av trengsel/pris (sommer i Europa).
- 2026-11-12: Kartnavn plasseres av egen kode (`plasserEtikett`) i stedet for ECharts' `hideOverlap`: navn som kolliderer, flyttes til ledig side og skjules bare når ingen plass er ledig. Grå prikker kan dekkes, ellers ble verdensvisningen for tom.
- 2026-11-12: Løsninger som finnes i både reisekartet og byguidene, skal være like; lista står i HANDOVER, «Felles med byguidene», med henvisning fra byguidene. Endres én, endres begge. Søkekrysset manglet her selv om byguidene hadde det.
- 2026-11-12: CLAUDE.md kortet ned til 134 linjer: det som står i HANDOVER eller i lista over felles løsninger, er tatt ut; miniatyroppskriften viser til byguidenes CLAUDE.md.
- 2026-11-12: All zoom skal gå gjennom `setOption` (`zoomRundt`/`settVisning`), ikke ECharts' egen roam-zoom. Ellers regnes `hideOverlap` ikke på nytt, og navn skjult i verdensvisningen forblir skjult innzoomet.
- 2026-11-12: Kartets bevegelse skal føles som MapLibre i byguidene: pinch følger fingrene 1:1 (dempingen fra PR #21 er fjernet), glid etter sveip, dobbelttrykk zoomer inn, og ECharts' egen hjulzoom er byttet ut med trinnløs zoom. Pål syntes zoomen gikk i for store steg og føltes dårlig på mobil.
- 2026-11-12: `landliste.tsv` er master for landlista; tabellene i `Landliste.md` lages fra den av `omorganiser.py`. Før måtte begge rettes for hånd ved hver deling.
- 2026-11-12: Ønskelisten følger samme regel som resten: ett reisemål = én klimaprofil, mest generelle navn («X og Y», region med eksempler i parentes). Vietnam og Brasil hadde to–tre klimaprofiler i ett reisemål; Lowcountry og Rote var smalere enn nabodelene med samme beste reisetid. Ønskelisten har derfor 44 reisemål, ikke 40.
- Eldre beslutninger (til 11.11.2026) står i ARKIV.md.
