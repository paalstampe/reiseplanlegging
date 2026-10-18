# NOTES — løpende status

Kort og oppdatert. Varig datamodell, scoremodell og kartteknikk står i HANDOVER.md, og arbeidsreglene i CLAUDE.md.
Oppdateres ved slutten av hver økt (`/avslutt`).

## Status nå

Sist oppdatert: 18. oktober 2026.

- Reisekartet er live på https://stam.pe/reiseplanlegging/, og Reisekalender.xlsx bygges fra de samme dataene.
- Alle 40 reisemål er fylt ut med klimanormaler, delscorer, begrunnelser og 49 vinduer. Vinduene dekker
  bevegelige høytider for 2026–28, festivaler og dyrelivshendelser.
- Kartet har hjemskjermikon, virker offline (også «Lagre alt» fra stam.pe), har mørk modus og er ikke søkbart.
  Siste kodeendring var mørk modus (PR #9, 15.10.).
- Det finnes ingen åpne grener utenom `main`.

## Neste steg

- Finjuster scorene etter Påls vurdering.
- Legg inn nye bevegelige datoer hvert år (Tet/kinesisk nyttår, påske, ramadan, tsechu) i `reisedata.py`, og bygg på nytt.
  Vinduene dekker 2026–28, så 2029 må inn i løpet av 2028.
- Oppdater miniatyrene på stam.pe når kartet endrer utseende merkbart (CLAUDE.md, Miniatyrer).

## Åpne spørsmål

- Svake klimaserier: noen stasjoner har gamle serier (Dili, Beirut, Galápagos, Hwange, São Tomé, Maun 1961–1990),
  og noen er proxy (Rote→Kupang, USA-WC→Vancouver, CRI→Liberia, ZWE→Hwange). Skal de byttes når bedre kilder finnes?
- Noen festivaldatoer er merket «sjekk dato».
- HANDOVER nevner en «HTML-visning generert fra Excel» som mulig neste steg. Er den fortsatt aktuell, nå som reisekartet finnes?

## Beslutningslogg

- 2026-09-25: Vektene er 40/40/20, og vetoet er myket opp til et tak på 1,5. Trengsel/pris er én dimensjon.
- 2026-09-25: `Reise - utenfor Europa.md` er masterlisten over reisemål.
- 2026-09-25: Sri Lanka er delt i LKA-SV og LKA-O. Stan-landene er slått sammen med Silkeveien (SILK).
- 2026-09-27: Navnene er endret (USA Nordvestkyst, Hawaii, Mexico City, Savannah-Charleston m.fl.), og kartetikettene har tankestrek mellom land og sted.
- 2026-10-04: Hele sidepanelet ruller på desktop. Varianten med kompakte filtre ble prøvd, men ikke valgt.
- 2026-10-15: Mørk modus følger enheten, og siden er ikke søkbar (noindex).
- 2026-10-18: Løpende status føres i NOTES.md, og HANDOVER.md er referanse.
- 2026-10-18: Ubrukte filer er slettet: det gamle regnearket («Gammel - Reiseidéer og reisekalender.xlsx»), style.css (bare forbilde) og det utdaterte oppsettnotatet for GitHub Pages.
