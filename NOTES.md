# NOTES — løpende status

Kort og oppdatert. Varig datamodell, scoremodell og kartteknikk står i HANDOVER.md, og arbeidsreglene i CLAUDE.md.
Oppdateres ved slutten av hver økt (`/avslutt`).

## Status nå

Sist oppdatert: 28. oktober 2026.

- Reisekartet er live på https://stam.pe/reiseplanlegging/, og Reisekalender.xlsx bygges fra de samme dataene.
- Alle 40 reisemål er fylt ut med klimanormaler, delscorer, begrunnelser og 49 vinduer. Vinduene dekker
  bevegelige høytider for 2026–28, festivaler og dyrelivshendelser.
- Kartet har hjemskjermikon, virker offline (også «Lagre alt» fra stam.pe), har mørk modus og er ikke søkbart.
- 28.10.: kartet finnes på engelsk (PR #12). Bryteren NO / EN står i brødsmulene, og valget deles med byguidene
  og stam.pe. Innholdet er oversatt i `reisedata_en.py`. Ingressen og bunnteksten nevner ikke lenger regnearket,
  og «se Vinduer» vises som «se hendelser» i kartet (PR #13–#14). Kartet bytter farger med en gang når
  enheten bytter mellom lys og mørk modus (PR #15).
- Det finnes ingen åpne grener utenom `main`.

## Neste steg

- Finjuster scorene etter Påls vurdering.
- Legg inn nye bevegelige datoer hvert år (Tet/kinesisk nyttår, påske, ramadan, tsechu) i `reisedata.py`, og bygg på nytt.
  Vinduene dekker 2026–28, så 2029 må inn i løpet av 2028.
- Oppdater miniatyrene på stam.pe når kartet endrer utseende merkbart (CLAUDE.md, Miniatyrer).
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
