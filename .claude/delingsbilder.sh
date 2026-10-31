#!/bin/bash
# Lager delingsbildet (og:image, 1200×630) og hjemskjermikonet fra .claude/delingsbilder.html:
#   deling.png            luftpostkonvolutt med klode-frimerke og «Reiseplanlegging»
#   apple-touch-icon.png  frimerke med «r» (180×180)
# delingsbilder.html er en identisk kopi av den i byguider; endres den, kopier til begge.
# Bruk: .claude/delingsbilder.sh   (fra roten av repoet; krever Node og Playwright, se skjermbilde.sh)
set -euo pipefail
cd "$(dirname "$0")/.."

NODE_PATH="$(npm root -g)" node - <<'JS'
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const side0 = 'file://' + path.resolve('.claude/delingsbilder.html');
  const nettleser = await chromium.launch();
  const side = await nettleser.newPage({ viewport: { width: 1200, height: 630 } });
  const feil = [];
  side.on('pageerror', f => feil.push('JS: ' + f.message));
  const ta = async (parametre, fil) => {
    await side.goto(side0 + '?' + new URLSearchParams(parametre), { waitUntil: 'networkidle' });
    await side.evaluate(() => document.fonts.ready);
    await side.locator('#flate > *').screenshot({ path: fil });
    console.log('Lagret ' + fil);
  };
  await ta({ motiv: 'luftpost', tittel: 'Reiseplanlegging', kicker: 'stam.pe',
    under: 'Hvor er det best å reise, uke for uke?' }, 'deling.png');
  await ta({ motiv: 'ikon', bokstav: 'r' }, 'apple-touch-icon.png');
  await nettleser.close();
  for (const f of feil) console.error('Feil: ' + f);
  if (feil.length) process.exit(1);
})().catch(f => { console.error(f.message); process.exit(1); });
JS
