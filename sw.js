/* Offline for reiseplanleggingen (service worker). Registreres fra reisekart_mal.html (index.html).

   Med nett er alt som før: egne filer (index.html med alle data) hentes fra nettet først, så
   endringer vises straks. Uten nett, eller når nettet ikke svarer innen NETT_FRIST, brukes siste
   lagrede kopi. ECharts, verdenskartet og Google Fonts tas fra lageret når de finnes der
   (faste versjoner på jsDelivr, så de endres ikke). Alt lagres ved første besøk med nett.

   Ved endring i strategi eller lagerformat: øk VERSJON, så ryddes gamle lagre bort. */
const VERSJON = 'v1';
const LAGER = 'reiseplanlegging-' + VERSJON;
const NETT_FRIST = 4000;
const OMFANG = new URL('./', self.location).href;
const FILER = ['./', 'apple-touch-icon.png',
  'https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js',    // samme som KILDER i malen
  'https://cdn.jsdelivr.net/npm/echarts@4.9.0/map/js/world.js',
  'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Work+Sans:wght@400;500;600&display=swap'];
const FREMMEDE = /^https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net)\//;
const SOK = { ignoreVary: true };

const egen = url => url.startsWith(OMFANG);

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const lager = await caches.open(LAGER);
    await Promise.all(FILER.map(f => lagre(lager, new URL(f, OMFANG).href).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const navn = await caches.keys();
    await Promise.all(navn.filter(n => n.startsWith('reiseplanlegging-') && n !== LAGER).map(n => caches.delete(n)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (egen(req.url)) e.respondWith(nettForst(req));
  else if (FREMMEDE.test(req.url)) e.respondWith(lagerForst(req));
});

async function nettForst(req) {
  const lager = await caches.open(LAGER);
  const nett = fetch(req).then(r => {
    if (r.ok) lager.put(req, r.clone());
    return r;
  });
  const frist = new Promise(res => setTimeout(res, NETT_FRIST));
  try {
    const r = await Promise.race([nett, frist.then(() => lager.match(req, SOK).then(k => k || nett))]);
    if (r) return r;
  } catch (err) { /* uten nett */ }
  // ?lang=en o.l.: samme side uten parametre er godt nok uten nett
  const kopi = await lager.match(req, SOK) || await lager.match(req, { ignoreVary: true, ignoreSearch: true });
  if (kopi) return kopi;
  return nett;
}

async function lagerForst(req) {
  const lager = await caches.open(LAGER);
  const kopi = await lager.match(req.url, SOK);
  if (kopi) return kopi;
  const r = await fetch(req);
  if (r.ok || r.type === 'opaque') lager.put(req.url, r.clone());
  return r;
}

async function lagre(lager, url) {
  let r;
  try { r = await fetch(url, url.startsWith(OMFANG) ? { cache: 'no-store' } : { mode: 'cors' }); }
  catch (err) { r = await fetch(url, { mode: 'no-cors' }); }
  if (r.ok || r.type === 'opaque') await lager.put(url, r);
}

/* Fra siden: { type: 'forhandslast', adresser: [...] } — det siden har lastet (fontfilene),
   så de også finnes første gang siden åpnes uten nett. Henter bare det som mangler. */
self.addEventListener('message', e => {
  const m = e.data || {};
  if (m.type !== 'forhandslast' || !Array.isArray(m.adresser)) return;
  e.waitUntil((async () => {
    const lager = await caches.open(LAGER);
    for (const url of new Set(m.adresser)) {
      if (!egen(url) && !FREMMEDE.test(url)) continue;
      if (await lager.match(url, SOK)) continue;
      await lagre(lager, url).catch(() => {});
    }
  })());
});
