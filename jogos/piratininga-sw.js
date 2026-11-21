/* Piratininga — guarda o jogo no aparelho (v216, 21/11/2026, pedido do professor)
   Da segunda vez em diante o jogo abre do que ficou guardado, sem esperar a internet,
   e funciona até sem internet. Quando há versão nova no GitHub, ela é baixada por trás
   e só passa a valer quando está inteira (página + todos os desenhos), na vez seguinte.
   Só cuida de piratininga.html, dos pacotes de arte (arte/pac_*.js?v=...) e da fonte.
   Os outros jogos da pasta não passam por aqui. */
const CACHE = 'piratininga-1';
const HTML = new URL('piratininga.html', self.registration.scope).href;
const ehHtml = u => u.origin === location.origin && /\/piratininga\.html$/.test(u.pathname);
const ehArte = u => u.origin === location.origin && /\/arte\/pac_[a-z0-9_]+\.js$/.test(u.pathname) && /^\?v=/.test(u.search);
const ehFonte = u => u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim().then(() => atualiza(true)).catch(() => {})));

self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  let u; try { u = new URL(r.url); } catch (_) { return; }
  if (ehHtml(u) && (r.mode === 'navigate' || r.destination === 'document')) e.respondWith(pagina(e));
  else if (ehArte(u)) e.respondWith(guardado(r, true));
  else if (ehFonte(u)) e.respondWith(guardado(r, false));
});

/* página: abre a guardada na hora e confere por trás se há versão nova */
async function pagina(e) {
  const c = await caches.open(CACHE);
  const velha = await c.match(HTML);
  e.waitUntil(atualiza(!velha).catch(() => {}));
  if (velha) return velha;
  return fetch(e.request); /* primeira vez: da internet; a página só é guardada quando todos os desenhos estiverem guardados */
}

/* desenhos e fonte: o que já foi guardado não muda (cada pacote tem a "impressão digital" ?v=) */
async function guardado(r, imutavel) {
  const c = await caches.open(CACHE);
  const tem = await c.match(r);
  if (tem) { if (!imutavel) fetch(r).then(n => { if (n && (n.ok || n.type === 'opaque')) c.put(r, n); }).catch(() => {}); return tem; }
  const n = await fetch(r);
  if (n && (n.ok || n.type === 'opaque')) c.put(r, n.clone()).catch(() => {});
  return n;
}

const html = t => new Response(t, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
/* a lista de pacotes fica escrita na página pela ferramenta abertura_rapida.py: {"f":"pac_e1.js?v=5c00e677",...} */
const pacotes = t => [...new Set([...t.matchAll(/"f":"(pac_[a-z0-9_]+\.js\?v=[0-9a-f]+)"/g)].map(m => m[1]))].map(p => new URL('arte/' + p, HTML).href);

let rodando = null;
function atualiza(primeira) { if (!rodando) rodando = atualiza1(primeira).finally(() => { rodando = null; }); return rodando; }
async function atualiza1(primeira) {
  const c = await caches.open(CACHE);
  const r = await fetch(HTML, { cache: 'no-cache' });
  if (!r.ok) return;
  const t = await r.text();
  const velha = await c.match(HTML);
  const tv = velha ? await velha.text() : null;
  const precisa = pacotes(t);
  if (!precisa.length) return; /* sem a lista de pacotes não dá para guardar com segurança */
  /* baixa primeiro todos os desenhos da versão nova; só depois troca a página guardada */
  for (const p of precisa) { if (!(await c.match(p))) { const n = await fetch(p); if (!n.ok) return; await c.put(p, n); } }
  if (tv !== t) await c.put(HTML, html(t));
  /* apaga desenhos de versões antigas */
  const quer = new Set(precisa);
  for (const k of await c.keys()) { const u = new URL(k.url); if (ehArte(u) && !quer.has(k.url)) await c.delete(k); }
  const cl = await self.clients.matchAll({ type: 'window' });
  for (const x of cl) x.postMessage({ pira: 'guardado', nova: !!tv && tv !== t, primeira: !!primeira || !tv });
}
