# NOTES — løpende status

Kort og oppdatert. Varig datamodell, scoremodell og kartteknikk står i HANDOVER.md, og arbeidsreglene i CLAUDE.md.
Oppdateres ved slutten av hver økt (`/avslutt`).
Eldre status per dato og eldre beslutninger ligger i ARKIV.md (lastes ikke automatisk; grep der ved behov).

## Status nå

Sist oppdatert: 12. november 2026.

- 12.11.: kartet zoomer og panorerer som byguidene (PR #51): pinch 1:1, glid etter sveip, dobbelttrykk zoomer inn, trinnløs
  hjul-/styreflatezoom på PC og animerte +/−. Testet i Chromium og WebKit; iOS-simulatoren hang og ble ikke brukt.
  Dette rettet også at kartnavn skjult i verdensvisningen (f.eks. «Etiopia») forble skjult når man zoomet inn. Gamle
  appvinduer viser feilen til siden lastes på nytt.
- 12.11.: ønskelisten følger samme navn og deling som resten: Vietnam delt i tre, Brasil i Rio og Nordøstkysten, USA-vestkysten i
  California og Nordvest; Lowcountry inn i Sørstatene og Rote inn i Nusa Tenggara. 259 reisemål, 44 på ønskelisten (detaljer i HANDOVER, Navneendringer).
  Scorene for de nye delene er Claudes vurdering.
- 12.11.: `omorganiser.py` i skillen `/nytt-reisemal` (steg 7) deler, slår sammen og gir ny ID til reisemål og oppdaterer
  felles vinduer, landlista, antallene i CLAUDE.md og alt generert (PR #48). `Landliste.md`-tabellene lages nå fra `landliste.tsv`.

- 11.11.: **alle FN-land er med – 257 reisemål** (før 40). Slik ble det gjort, i rekkefølge:
  - Datamodell (PR #38): én JSON-fil per reisemål i `reisemal/`, norsk og engelsk side om side, lest av `reisemal.py`.
    `Reisemål.md` genereres og erstatter «Reise - utenfor Europa.md» som master.
  - Søk og «Vis: Alle reisemål / Ønskeliste» (PR #39). Påls 40 er ønskelisten (`onskeliste: true`).
  - Detaljkortet kan dras etter toppen, som infoboksen i byguidene (PR #40).
  - Landlista vedtatt (`Landliste.md` / `landliste.tsv`): 195 land, 31 delt, mikrostater i naboen, Hongkong, Taiwan, Grønland
    og Færøyene som ekstra, krigsland med varsel.
  - Åtte regioner, `felles_vinduer.json`, `kortnavn` og navnerettelser (USA – Hawaii, Mexico – Mexico City, SILK → UZB) (PR #41).
  - Skillen `/nytt-reisemal` med `klima.py`, som henter klimaboksen fra Wikipedia (PR #42–#44).
  - Midtøsten (12) og Nord-Amerika (9) fylt inn her i økta; Pål godkjente nivået. De resterende 196 med en workflow (27 agenter).
  - Felles vinduer 2026–28: ramadan (41 reisemål), påskeuka (58), ortodoks påske (3) og kinesisk nyttår (13), med justering per
    reisemål og positiv tekst der høytiden er en opplevelse. Kildesvakheter (183 av 196) står i `Kildesvakheter.md`.
  - Miniatyrene og forsideteksten på stam.pe er oppdatert, og delingskortet sier «alle land» (PR #45).
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

- 2026-11-12: All zoom skal gå gjennom `setOption` (`zoomRundt`/`settVisning`), ikke ECharts' egen roam-zoom. Ellers regnes `hideOverlap` ikke på nytt, og navn skjult i verdensvisningen forblir skjult innzoomet.
- 2026-11-12: Kartets bevegelse skal føles som MapLibre i byguidene: pinch følger fingrene 1:1 (dempingen fra PR #21 er fjernet), glid etter sveip, dobbelttrykk zoomer inn, og ECharts' egen hjulzoom er byttet ut med trinnløs zoom. Pål syntes zoomen gikk i for store steg og føltes dårlig på mobil.
- 2026-11-12: `landliste.tsv` er master for landlista; tabellene i `Landliste.md` lages fra den av `omorganiser.py`. Før måtte begge rettes for hånd ved hver deling.
- 2026-11-12: Ønskelisten følger samme regel som resten: ett reisemål = én klimaprofil, mest generelle navn («X og Y», region med eksempler i parentes). Vietnam og Brasil hadde to–tre klimaprofiler i ett reisemål; Lowcountry og Rote var smalere enn nabodelene med samme beste reisetid. Ønskelisten har derfor 44 reisemål, ikke 40.
- 2026-11-11: Kontekst spares ved oppstart: NOTES.md holdes under ca. 10 KB (/avslutt passer på det), eldre status og beslutninger ligger i ARKIV.md. Før lastet reiseplanlegging ca. 27 KB i hver økt.
- 2026-11-11: `Read` er sperret for `index.html` (~700 KB, generert), `Reisekalender.xlsx` og `__pycache__/` i `.claude/settings.json` (PR #46).
- 2026-11-11: Alle 195 FN-land er med (Europa og Norge også). Mikrostatene nevnes i naboen, ikke egne reisemål. Hongkong, Taiwan,
  Grønland og Færøyene er med som egne reiser. Ett reisemål = én reise med én klimaprofil; land deles der beste reisetid er ulik.
- 2026-11-11: Åtte regioner (Europa, Midtøsten, Afrika, Asia, Oseania, Nord-Amerika, Mellom-Amerika og Karibia, Sør-Amerika),
  som knapper som før.
- 2026-11-11: Ønskelisten vises i egen visning (alle reisemål som standard), motsatt av byguidene der den er skjult.
- 2026-11-11: Høytider som gjelder mange land står én gang i `felles_vinduer.json`. Ortodoks påske har egne datoer.
- 2026-11-11: Detaljkortet dras etter toppen også med mus (i byguidene fra hele boksen), så kortet kan rulles og tekst markeres.
- 2026-11-11: De 196 siste reisemålene ble fylt inn med en workflow etter at Midtøsten og Nord-Amerika var godkjent som mal.
- 2026-11-11: Land med reiseråd vises som andre land, med varselet «Sjekk reiseråd». De skjules ikke og sorteres ikke lavere,
  selv om de kan havne øverst i lista (Pål valgte dette framfor et filter).
- 2026-11-11: Dataene ligger i én JSON-fil per reisemål (`reisemal/<ID>.json`), med norsk og engelsk side om side.
  Før måtte et reisemål legges inn fem steder, noe som ikke holder når lista skal utvides til alle FN-landene. JSON fordi det ikke krever
  avhengigheter og valideres av hooken. `Reisemål.md` genereres og er ikke lenger master. Alle dagens 40 har `onskeliste: true`.
- Eldre beslutninger (til 5.11.2026) står i ARKIV.md.
