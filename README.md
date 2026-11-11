# Reiseplanlegging

Pål sin oversikt over beste reisetid per reisemål – kart-app og reisekalender.

**Publisert:** https://paalstampe.github.io/reiseplanlegging/

## Innhold

- `index.html` – Reisekart (generert, ikke rediger direkte)
- `reisekart_mal.html` – mal for kart-appen
- `reisemal/<ID>.json` – all data, én fil per reisemål (norsk og engelsk)
- `reisemal.py` – leser dataene for begge skriptene
- `lag_reisekart.py` – bygger `index.html` fra mal + data
- `bygg_reisekalender.py` – bygger `Reisekalender.xlsx`
- `Reisemål.md` – oversikt over reisemålene (generert)
- `HANDOVER.md` – status og design for videre arbeid med Claude

## Oppdatere siden

```
python3 lag_reisekart.py
```

Deretter commit og *Push origin* i GitHub Desktop. Siden oppdateres etter 1–2 minutter.
