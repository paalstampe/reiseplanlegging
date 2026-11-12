#!/bin/bash
# Tester kartets bevegelse (zoom og panorering) automatisk: PC (hjul, knapper) og touch (pinch, sveip med glid,
# dobbelttrykk) i Chromium, og touch i WebKit (Safaris motor, iPhone 13) hvis den er installert.
# Kjør etter endringer i touchRoam, hjulZoom, animerZoom, zoomRundt eller zoomKnapper.
# Bruk: .claude/bevegelsestest.sh [url]   (standard http://127.0.0.1:8001/)
# Lokalt: kjør «python3 lag_reisekart.py» og start serveren på 8001 først (preview_start eller python3 -m http.server).
# Krever Node og Playwright med Chromium (se skjermbilde.sh). WebKit, én gang: npx playwright install webkit
# Avslutter med kode 1 hvis en sjekk feiler. Testen måler tilstand, ikke følelse — den erstatter ikke en ekte iPhone.
set -euo pipefail

url="${1:-http://127.0.0.1:8001/}"
case "$url" in
  https://stam.pe/*|http://localhost:*|http://127.0.0.1:*) ;;
  *) echo "Bare https://stam.pe/... og http://localhost:<port>/... er tillatt" >&2; exit 1 ;;
esac

if ! command -v node >/dev/null || ! NODE_PATH="$(npm root -g)" node -e "require('playwright')" 2>/dev/null; then
  echo "Mangler Node eller Playwright — se installasjon øverst i .claude/skjermbilde.sh" >&2
  exit 1
fi

# Skyen: samme proxyoppsett som skjermbilde.sh (se forklaringen der).
proxy=""
spki=""
ca=/root/.ccr/ca-bundle.crt
if [ -n "${HTTPS_PROXY:-}" ] && [ -f "$ca" ]; then
  proxy="$HTTPS_PROXY"
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  csplit -s -z -f "$tmp/ca-" "$ca" '/-----BEGIN CERTIFICATE-----/' '{*}'
  spki=$(for f in "$tmp"/ca-*; do
    if openssl x509 -in "$f" -noout -subject 2>/dev/null | grep -q 'O = Anthropic'; then
      openssl x509 -in "$f" -pubkey -noout | openssl pkey -pubin -outform der \
        | openssl dgst -sha256 -binary | base64
    fi
  done | sort -u | paste -sd, -)
fi

URL="$url" PROXY="$proxy" SPKI="$spki" NODE_PATH="$(npm root -g)" node - <<'JS'
const pw = require('playwright');
const e = process.env;
const args = e.PROXY
  ? ['--proxy-server=' + e.PROXY, '--proxy-bypass-list=localhost;127.0.0.1',
     '--ignore-certificate-errors-spki-list=' + e.SPKI,
     '--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
  : [];
let feilet = 0;
const sjekk = (navn, ok, verdi) => {
  console.log(`${ok ? 'OK  ' : 'FEIL'} ${navn}: ${JSON.stringify(verdi)}`);
  if (!ok) feilet++;
};
const naer = (a, b, tol) => Math.abs(a - b) <= tol;

async function aapne(ctx, navn) {
  const side = await ctx.newPage();
  side.on('pageerror', f => sjekk(navn + ': JS-feil', false, f.message));
  await side.goto(e.URL, { waitUntil: 'networkidle', timeout: 60000 });
  await side.waitForFunction(() => window.kart);
  return side;
}
const tilstand = side => side.evaluate(() => {
  const g = kart.getOption().geo[0];
  return { zoom: g.zoom || 1, senter: g.center, transform: kart.getDom().style.transform, valgt: state.valgt };
});

// Touch-sekvensene, felles for begge motorene. `send(type, punkter)` gir fingre i kartets koordinater.
async function touchSekvens(navn, side, send) {
  await send('touchStart', [[150, 300], [250, 300]]);   // pinch: avstand 100 → 200 px skal gi zoom × 2 (1:1)
  for (let i = 1; i <= 10; i++) { await send('touchMove', [[150 - 5 * i, 300], [250 + 5 * i, 300]]); await side.waitForTimeout(16); }
  await send('touchEnd', []);
  await side.waitForTimeout(100);
  let t = await tilstand(side);
  sjekk(navn + ': pinch følger fingrene', naer(t.zoom, 2, 0.02), t.zoom);

  const lon0 = t.senter[0];   // sveip 160 px mot venstre: kartet skal gli videre etter slipp og tegnes ferdig
  await send('touchStart', [[300, 300]]);
  for (let i = 1; i <= 8; i++) { await send('touchMove', [[300 - 20 * i, 300]]); await side.waitForTimeout(16); }
  await send('touchEnd', []);
  await side.waitForTimeout(80);
  const underveis = await tilstand(side);
  await side.waitForTimeout(1600);
  t = await tilstand(side);
  // Grader østover (lengdegraden går rundt). Glidet stopper senest én skjermbredde fra start, som er 180° ved zoom 2 på 390 px.
  const flytt = (((t.senter[0] - lon0) % 360) + 360) % 360;
  sjekk(navn + ': sveip glir videre', underveis.transform !== '' && flytt > 80 && flytt <= 180.5,{ underveis: underveis.transform, grader: flytt });
  sjekk(navn + ': ingen transform igjen etter glid', t.transform === '', t.transform);

  const z0 = t.zoom;   // dobbelttrykk der ingen prikk er nær (ellers åpner første trykk et kort): zoom × 2
  const tomt = await side.evaluate(() => {
    const lag = kart.getDom(), prikker = kart.getOption().series[0].data
      .map(v => kart.convertToPixel({ geoIndex: 0 }, v.value.slice(0, 2))).map(([x, y]) => [x + lag.offsetLeft, y]);
    for (let y = 200; y <= 500; y += 20) for (let x = 120; x <= 340; x += 20)
      if (prikker.every(([px, py]) => Math.hypot(px - x, py - y) > 50)) return [x, y];
    return [200, 350];
  });
  for (let k = 0; k < 2; k++) { await send('touchStart', [tomt]); await send('touchEnd', []); await side.waitForTimeout(120); }
  await side.waitForTimeout(500);
  t = await tilstand(side);
  sjekk(navn + ': dobbelttrykk zoomer inn', naer(t.zoom, Math.min(12, z0 * 2), 0.02) && t.transform === '', { fra: z0, til: t.zoom });

  await side.click('#zoom-ut');   // animert utzoom med CSS-transform, så én omtegning
  await side.waitForTimeout(500);
  t = await tilstand(side);
  sjekk(navn + ': − halverer zoomen', naer(t.zoom, z0, 0.02) && t.transform === '', t.zoom);
}

(async () => {
  const chromium = await pw.chromium.launch({ args });

  // PC: hjul zoomer trinnløst rundt pekeren, knappene dobler/nullstiller.
  const pc = await aapne(await chromium.newContext({ viewport: { width: 1300, height: 900 } }), 'PC');
  const geoUnder = (x, y) => pc.evaluate(([x, y]) => {
    const r = document.getElementById('kart').getBoundingClientRect();
    return kart.convertFromPixel({ geoIndex: 0 }, [x - r.left, y - r.top]);
  }, [x, y]);
  await pc.mouse.move(900, 450);
  const foer = await geoUnder(900, 450);
  for (let i = 0; i < 3; i++) { await pc.mouse.wheel(0, -100); await pc.waitForTimeout(30); }
  await pc.waitForTimeout(800);
  let t = await tilstand(pc);
  const etter = await geoUnder(900, 450);
  sjekk('PC: tre hjulhakk zoomer inn', t.zoom > 1.8 && t.zoom < 3.5, t.zoom);
  sjekk('PC: stedet under pekeren blir liggende', naer(foer[0], etter[0], 0.05) && naer(foer[1], etter[1], 0.05), { foer, etter });
  const zHjul = t.zoom;
  await pc.click('#zoom-inn');
  await pc.waitForTimeout(500);
  t = await tilstand(pc);
  sjekk('PC: + dobler zoomen', naer(t.zoom, Math.min(12, zHjul * 2), 0.02), t.zoom);
  await pc.click('#zoom-hjem');
  t = await tilstand(pc);
  sjekk('PC: «Vis hele kartet» går til zoom 1', t.zoom === 1, t.zoom);

  // Touch i Chromium: ekte touch-hendelser via CDP, så også zrenders klikk er med (dobbelttrykk skal ikke åpne kort).
  const mobilCtx = await chromium.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const mobil = await aapne(mobilCtx, 'Chromium touch');
  const cdp = await mobilCtx.newCDPSession(mobil);
  const boks = await mobil.evaluate(() => { const r = document.getElementById('kart').getBoundingClientRect(); return [r.left, r.top]; });
  await touchSekvens('Chromium touch', mobil, (type, pts) => cdp.send('Input.dispatchTouchEvent',
    { type, touchPoints: pts.map(([x, y], id) => ({ x: boks[0] + x, y: boks[1] + y, id })) }));
  const valgt = (await tilstand(mobil)).valgt;
  sjekk('Chromium touch: dobbelttrykk åpnet ikke detaljkort', valgt == null, valgt);
  await chromium.close();

  // Touch i WebKit: `new Touch()` finnes ikke der, så hendelsene lages med `touches` lagt på.
  let webkit;
  try { webkit = await pw.webkit.launch(); }
  catch { console.log('HOPPET OVER WebKit (ikke installert: npx playwright install webkit)'); }
  if (webkit) {
    const side = await aapne(await webkit.newContext({ ...pw.devices['iPhone 13'] }), 'WebKit touch');
    await touchSekvens('WebKit touch', side, (type, pts) => side.evaluate(([type, pts]) => {
      const el = document.getElementById('kart'), r = el.getBoundingClientRect();
      const ev = new Event(type.toLowerCase(),{ bubbles: true, cancelable: true });
      Object.defineProperty(ev, 'touches', { value: pts.map(([x, y], i) => ({ identifier: i, clientX: r.left + x, clientY: r.top + y })) });
      el.dispatchEvent(ev);
    }, [type, pts]));
    await webkit.close();
  }

  console.log(feilet ? `${feilet} sjekk(er) feilet` : 'Alle sjekker OK');
  process.exit(feilet ? 1 : 0);
})().catch(f => { console.error(f.message); process.exit(1); });
JS
