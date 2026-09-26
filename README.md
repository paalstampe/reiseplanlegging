# Reiseplanlegging

Pål sin oversikt over beste reisetid per reisemål – kart-app og reisekalender.

**Publisert:** https://paalstampe.github.io/reiseplanlegging/

## Innhold

- `index.html` – Reisekart (generert, ikke rediger direkte)
- `reisekart_mal.html` – mal for kart-appen
- `reisedata.py` – all data (månedsscorer, vinduer, koordinater m.m.)
- `lag_reisekart.py` – bygger `index.html` fra mal + data
- `bygg_reisekalender.py` – bygger `Reisekalender.xlsx`
- `Reise - utenfor Europa.md` – masterliste over reisemål
- `HANDOVER.md` – status og design for videre arbeid med Claude

## Oppdatere siden

```
python3 lag_reisekart.py
```

Deretter commit og *Push origin* i GitHub Desktop. Siden oppdateres etter 1–2 minutter.
