---
name: nytt-reisemal
description: Lag ett eller flere nye reisemål i reisemal/<ID>.json (klimanormaler, scorer, begrunnelser på norsk og engelsk, vinduer). Bruk når reisemål fra landliste.tsv skal fylles inn, eller når Pål vil ha et nytt reisemål.
---

# Nytt reisemål

Ett reisemål = én fil `reisemal/<ID>.json`. ID, region, land og sted står i `landliste.tsv` (vedtatt 11.11.2026).
Formatet er beskrevet i HANDOVER.md, Datamodell. Se på to–tre eksisterende filer i samme region før du begynner
(f.eks. `reisemal/LAO.json`, `reisemal/EGY.json`, `reisemal/CRI.json`), så scorer og tekster ligger på samme nivå.

## 1. Klima (12 måneder)

- Finn klimanormaler for én representativ stasjon: Wikipedias klimaboks i byens artikkel («Climate» / «Weather box»),
  helst WMO eller nasjonal met-tjeneste 1991–2020.
- `tmaks` = middel av døgnets maksimum (°C, én desimal). `nedbor` = middel nedbør per måned (mm, heltall).
- `kilde`: «Stasjon, institusjon periode, via Wikipedia», f.eks. «Yangon (Kaba-Aye), WMO 1991–2020, via Wikipedia».
  Er stasjonen en proxy (annet sted enn reisemålet) eller serien gammel (før 1991), si det i kilden og i svaret til Pål.
  Engelsk kilde i `en.kilde` (tusenskille med komma: «2,406 m»).
- Store ruter eller regioner: velg stasjonen som begrenser (den med verst regn eller hete), og nevn de andre i kilden.

## 2. Scorer 1–5 per måned (scoremodellen i CLAUDE.md; ikke endre den)

- `klima`: 5 = ideelt, 3 = akseptabelt, 1 = frarådes (monsun, syklon/tyfon, ekstrem hete eller kulde).
- `opplevelse`: 5 = toppsesong for det man reiser for (dyreliv, festivaler, sikt, snø, blomstring), 1 = stengt eller ikke gjennomførbart.
- `trengsel`: 5 = lite folk og lave priser, 1 = maks høysesong og utsolgt. Ta med lokale ferier (påske, sommerferie, Golden Week).
- Samlet = 0,4·klima + 0,4·opplevelse + 0,2·trengsel, med tak 1,5 hvis klima eller opplevelse er 1. Sjekk at de beste
  månedene havner på 4,0–4,8 og de dårligste under 3, slik som i eksisterende reisemål.

## 3. Tekster

- `no`/`en` per måned: én kort setning eller to (helst under 90 tegn), konkret: vær, hva som skjer, trengsel.
  Stil som i eksisterende filer: «Tørt, behagelig. Ballongsesong i Bagan. Høysesong.» Vis til et vindu med «(se Vinduer)»
  / «(see events)».
- `kategori` fra settet som finnes («Strand», «Kultur / natur», «By / kultur», «Safari», «Natur / trekking» …), engelsk i `en.kategori`.
- `merknad`: bare det som hjelper planleggingen. Land der UD fraråder reiser (se merknaden i `landliste.tsv`): «Sikkerhet: sjekk UDs reiseråd»
  / «Safety: check Norwegian MFA travel advice» (gir varselet i kartet).
- `kortnavn` bare når «land – sted» er 23 tegn eller mer, f.eks. «Sri Lanka øst» / «Sri Lanka east».
- `en.land` og `en.sted` alltid (engelske navn).

## 4. Resten av feltene

- `status`: «Ikke besøkt». `onskeliste`: false (Påls ønskeliste er de 40 som fantes 11.11.2026).
- `koord`: [bredde, lengde] for et punkt midt i det man reiser til (byen, nasjonalparken, øygruppen), to desimaler.
- `region`: fra `landliste.tsv`.

## 5. Vinduer

- Hendelser som bare gjelder dette reisemålet (festivaler, dyreliv, monsunstart, sesongåpning) i reisemålets fil.
  Faste datoer: `fra_uke`/`til_uke` uten `aar`. Bevegelige: `fra`/`til` som datoer, én per år 2026–2028. Usikker dato: «sjekk dato».
- Høytider som gjelder mange land (ramadan, påske/Semana Santa, kinesisk nyttår, Diwali, Golden Week) legges i
  `felles_vinduer.json`: legg ID-en til `gjelder` i vinduet som finnes, eller lag vinduet hvis det mangler.
  Annen justering eller tekst for ett reisemål: `{"id": "...", "justering": -1}` i `gjelder`.
- `justering` typisk ±0,3 til ±1. Ikke legg samme høytid både i fellesfila og i reisemålets fil (det stoppes med feilmelding).

## 6. Lagre og sjekke

- Skriv fila med `reisemal.skriv(sti, r)` (én måned og ett vindu per linje), f.eks. fra et lite Python-skript.
- Kjør `python3 lag_reisekart.py`: ingen feilmelding og ingen «Mangler engelsk». Den oppdaterer også `index.html` og `Reisemål.md`.
- Bygg regnearket (`python3 bygg_reisekalender.py`, krever openpyxl) og commit alt sammen. Data går rett til main (CLAUDE.md).
- Si fra om proxy-stasjoner, gamle serier og usikre datoer, og før dem opp under Åpne spørsmål i NOTES.md.
