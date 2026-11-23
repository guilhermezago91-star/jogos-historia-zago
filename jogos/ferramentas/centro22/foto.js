// Tira a "foto" do centro de 1922 depois que todos os remendos terminam.
// uso: node foto.js <url> <pasta_saida> [espera_min_s] [extraInitJS]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [url, outDir, esperaMin = '80', extra] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(path.join(outDir, 'spr'), { recursive: true });
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  const p = await ctx.newPage();
  const erros = [];
  p.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 300)));
  p.on('console', m => { const t = m.text(); if ((m.type() === 'error' || m.type() === 'warning') && !/willReadFrequently|TUNNEL/.test(t)) erros.push(m.type() + ': ' + t.slice(0, 300)); });
  if (extra) await p.addInitScript(extra);
  if (process.env.RATE) { const cdp0 = await ctx.newCDPSession(p); await cdp0.send('Emulation.setCPUThrottlingRate', { rate: Number(process.env.RATE) }); }
  await p.goto(url, { waitUntil: 'load', timeout: 180000 });
  await p.waitForFunction(() => window.__G && window.__G.start && window.__T, null, { timeout: 180000 });
  await p.evaluate(() => { window.__tLoad = performance.now(); window.__G.start(); window.__G.startEra4(); });
  await p.waitForFunction(() => window.__G.cur === 'm_centro22' && !window.__G.fade, null, { timeout: 120000 });
  // espera tudo assentar: impressão digital igual 3 vezes seguidas, e pelo menos esperaMin s
  const digital = () => p.evaluate(() => {
    const G = window.__G, T = window.__T; let h = 0; const add = s => { for (let i = 0; i < s.length; i++)h = (h * 31 + s.charCodeAt(i)) | 0; };
    add(G.SCN.m_centro22.map.map(r => Array.isArray(r) ? r.join('') : r).join('|'));
    for (const o of T.objects) if (o.scene === 'm_centro22') add(o.id + ',' + o.x + ',' + o.y + ',' + o.w + ',' + o.h + ',' + o.door + ',' + o.room + ',' + o.name);
    for (const n of T.npcs) if (n.scene === 'm_centro22') add(n.id + ',' + n.x + ',' + n.y);
    for (const i of T.ITEMS) add(i.id + ',' + i.scene + ',' + i.x + ',' + i.y);
    add(String(T.objects.length) + ',' + T.npcs.length + ',' + T.ITEMS.length + ',' + T.walkers.length);
    return h;
  });
  const t0 = Date.now(); let ult = null, iguais = 0;
  while (true) {
    await p.waitForTimeout(5000);
    // mantém o jogador no centro, sem diálogo aberto
    await p.evaluate(() => { const G = window.__G; if (G.cur !== 'm_centro22' && !G.fade && !G.dialog) G.setScene('m_centro22'); });
    const d = await digital();
    if (d === ult) iguais++; else { iguais = 0; ult = d; }
    if (iguais >= 3 && Date.now() - t0 > Number(esperaMin) * 1000) break;
    if (Date.now() - t0 > 300000) { erros.push('NAO ASSENTOU em 300 s'); break; }
  }
  const assentou = (Date.now() - t0) / 1000;
  // ---- dados ----
  const dados = await p.evaluate(() => {
    const G = window.__G, T = window.__T, K = 'm_centro22';
    const hs = s => { let h = 0; for (let i = 0; i < s.length; i++)h = (h * 31 + s.charCodeAt(i)) | 0; return (h >>> 0).toString(36); };
    const ser = (v, d, vis) => {
      if (v === null || v === undefined) return v === null ? null : '∅undef';
      const ty = typeof v;
      if (ty === 'function') return 'ƒ' + hs(v.toString());
      if (ty !== 'object') return (ty === 'number' && !isFinite(v)) ? '∅' + String(v) : v;
      if (typeof HTMLCanvasElement !== 'undefined' && (v instanceof HTMLCanvasElement || v instanceof HTMLImageElement)) return '[img ' + (v.width || 0) + 'x' + (v.height || 0) + ']';
      if (v instanceof Map) return '[Map ' + v.size + ']'; if (v instanceof Set) return '[Set ' + v.size + ']';
      if (ArrayBuffer.isView(v)) return '[' + v.constructor.name + ' ' + v.length + ']';
      if (vis.has(v)) return '[ciclo]'; if (d > 4) return '[fundo]';
      vis.add(v);
      let r;
      if (Array.isArray(v)) r = v.map(x => ser(x, d + 1, vis));
      else { r = {}; for (const k of Object.keys(v)) r[k] = ser(v[k], d + 1, vis); }
      vis.delete(v); return r;
    };
    const S = x => ser(x, 0, new Set());
    const antes = window.__drawAntes, objAntes = window.__objAntes;
    const objs = T.objects.map((o, i) => { const r = S(o); r.__i = i; r.__novo = !objAntes.has(o); r.__cena0 = window.__cenaAntes.has(o) ? window.__cenaAntes.get(o) : null; r.__drawIgual = antes && antes.has(o) ? antes.get(o) === o.draw : null; return r; });
    const sc = T.SCN[K];
    return {
      mapa: sc.map.map(r => Array.isArray(r) ? r.join('') : r),
      mapaTipo: Array.isArray(sc.map[0]) ? 'array' : 'string',
      cena: Object.fromEntries(Object.keys(sc).filter(k => k !== 'map').map(k => [k, S(sc[k])])),
      centro22: S(window.__centro22),
      objetos: objs,
      npcs: T.npcs.map((n, i) => { const r = S(n); r.__i = i; r.__cena0 = window.__npcAntes.has(n) ? window.__npcAntes.get(n) : null; return r; }),
      itens: T.ITEMS.map(n => { const r = S(n); r.__cena0 = window.__itAntes.has(n) ? window.__itAntes.get(n) : null; return r; }),
      walkers: T.walkers.filter(w => w.scene === K).map(S),
      walkersPorCena: T.walkers.reduce((a, w) => (a[w.scene] = (a[w.scene] || 0) + 1, a), {}),
      QT: S(T.QT), Q: S(T.Q), ROTEIRO4: S(T.ROTEIRO[4]), GIVER: S(T.GIVER),
      FONTES: T.FONTES ? Object.keys(T.FONTES).sort() : null, fontesV: T.FONTES ? Object.fromEntries(Object.keys(T.FONTES).filter(k => !window.__fontesAntes.has(k)).map(k => [k, S(T.FONTES[k])])) : null, fontesAntes: [...window.__fontesAntes].sort(), comp: (() => { const C = window.__centro22; if (!C || !C.naRede) return null; let s = ''; for (let y = 0; y < C.H; y++)for (let x = 0; x < C.W; x++)s += C.naRede(x, y) ? '1' : '0'; return s; })(), glob: Object.fromEntries(Object.keys(window).filter(k => /^__(jm|placas|plq|merc|vale|semVale|ruaG|gente|CIT|interiores|transito)/.test(k)).map(k => [k, S(window[k])])),
      cenas: Object.keys(T.SCN).sort(), INT: Object.keys(T.INT).sort(),
      placas22: S(window.__placas22), plq22: S(window.__plq22), ruaG: window.__ruaG ? window.__ruaG.map(r => Array.isArray(r) ? r.map(c => c || '0').join('') : String(r)) : null,
      janela: Object.keys(window).filter(k => /^__/.test(k)).sort(),
      jmTeste: S(window.__jmTeste), minhas: S(window.__MINHAS_get && window.__MINHAS_get()),
    };
  });
  fs.writeFileSync(path.join(outDir, 'dados.json'), JSON.stringify(dados));
  // ---- chão e foto inteira ----
  await p.evaluate(() => { const G = window.__G, T = window.__T, K = 'm_centro22'; G.setScene(K); const sc = G.SCN[K], ex = sc.exp, g = ex.slice(); ex.fill(1); const cv = document.createElement('canvas'); cv.width = sc.map[0].length * 16; cv.height = sc.map.length * 16; try { T.drawSceneInto(cv.getContext('2d'), K, 0, true); } catch (e) { } ex.set(g); G.setScene(K); });
  await p.waitForTimeout(4000);
  const imgs = await p.evaluate(() => {
    const G = window.__G, T = window.__T, K = 'm_centro22';
    G.setScene(K);
    const chao = T.stat.toDataURL('image/png');
    const sc = G.SCN[K], ex = sc.exp, guarda = ex.slice(); ex.fill(1);
    const W = sc.map[0].length * 16, H = sc.map.length * 16;
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const c = cv.getContext('2d'); c.imageSmoothingEnabled = false;
    try { T.drawSceneInto(c, K, 0, true); } catch (e) { return { erro: String(e) }; }
    ex.set(guarda); G.setScene(K);
    return { chao, foto: cv.toDataURL('image/png') };
  });
  if (imgs.erro) erros.push('foto: ' + imgs.erro);
  else {
    fs.writeFileSync(path.join(outDir, 'chao.png'), Buffer.from(imgs.chao.split(',')[1], 'base64'));
    fs.writeFileSync(path.join(outDir, 'foto.png'), Buffer.from(imgs.foto.split(',')[1], 'base64'));
  }
  // ---- desenho de cada objeto do centro (para saber o que é parado e o que se mexe) ----
  const passe = (tag) => p.evaluate((tag) => {
    const T = window.__T, K = 'm_centro22', M = 128, MT = 288;
    const hs = d => { let h = 2166136261; for (let i = 0; i < d.length; i += 1) { h ^= d[i]; h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); };
    const r = {};
    for (const o of T.objects) {
      if (o.scene !== K) continue;
      const w = o.w * 16 + 2 * M, h = o.h * 16 + MT + M;
      const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const c = cv.getContext('2d'); c.imageSmoothingEnabled = false;
      const dx = tag === 'xy' ? 48 : 0, dy = tag === 'xy' ? 80 : 0;
      let err = null; try { o.draw(c, M + dx, MT + dy); } catch (e) { err = String(e).slice(0, 120); }
      const d = c.getImageData(0, 0, w, h).data;
      let x0 = w, y0 = h, x1 = -1, y1 = -1;
      for (let y = 0; y < h; y++)for (let x = 0; x < w; x++)if (d[(y * w + x) * 4 + 3]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (x1 < 0) { r[o.__i ?? T.objects.indexOf(o)] = { vazio: 1, err }; continue; }
      const cw = x1 - x0 + 1, ch = y1 - y0 + 1; const cd = c.getImageData(x0, y0, cw, ch).data;
      const key = hs(cd) + '_' + cw + 'x' + ch;
      const cg = document.createElement('canvas'); cg.width = w; cg.height = h; const g2 = cg.getContext('2d'); g2.fillStyle = '#7f8a79'; g2.fillRect(0, 0, w, h); try { o.draw(g2, M + dx, MT + dy); } catch (e) { }
      const kc = hs(g2.getImageData(x0, y0, cw, ch).data);
      const out = { k: key, kc, ox: x0 - M - dx, oy: y0 - MT - dy, w: cw, h: ch, err };
      if (tag === 'a') { const c2 = document.createElement('canvas'); c2.width = cw; c2.height = ch; c2.getContext('2d').putImageData(c.getImageData(x0, y0, cw, ch), 0, 0); out.png = c2.toDataURL('image/png'); }
      r[T.objects.indexOf(o)] = out;
    }
    return r;
  }, tag);
  fs.mkdirSync(path.join(outDir, 'spr2'), { recursive: true });
  const A2 = await p.evaluate(() => {
    const T = window.__T, K = 'm_centro22', M = 128, MT = 288, r = {};
    const hs = d => { let h = 2166136261; for (let i = 0; i < d.length; i += 1) { h ^= d[i]; h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); };
    for (const o of T.objects) {
      if (o.scene !== K) continue;
      const w = (o.w * 16 + 2 * M) * 2, h = (o.h * 16 + MT + M) * 2;
      const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const c = cv.getContext('2d'); c.setTransform(2, 0, 0, 2, 0, 0); c.imageSmoothingEnabled = false;
      try { o.draw(c, M, MT); } catch (e) { }
      const d = c.getImageData(0, 0, w, h).data; let x0 = w, y0 = h, x1 = -1, y1 = -1;
      for (let y = 0; y < h; y++)for (let x = 0; x < w; x++)if (d[(y * w + x) * 4 + 3]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (x1 < 0) continue;
      const cw = x1 - x0 + 1, ch = y1 - y0 + 1; const im = c.getImageData(x0, y0, cw, ch);
      const c2 = document.createElement('canvas'); c2.width = cw; c2.height = ch; c2.getContext('2d').putImageData(im, 0, 0);
      r[T.objects.indexOf(o)] = { k: hs(im.data) + '_' + cw + 'x' + ch, ox: x0 - 2 * M, oy: y0 - 2 * MT, w: cw, h: ch, png: c2.toDataURL('image/png') };
    }
    return r;
  });
  const spr2 = {}; for (const i of Object.keys(A2)) { const a = A2[i]; spr2[i] = { k: a.k, ox: a.ox, oy: a.oy, w: a.w, h: a.h }; const f = path.join(outDir, 'spr2', a.k + '.png'); if (!fs.existsSync(f)) fs.writeFileSync(f, Buffer.from(a.png.split(',')[1], 'base64')); }
  fs.writeFileSync(path.join(outDir, 'desenhos2.json'), JSON.stringify(spr2));
  const A = await passe('a');
  await p.waitForTimeout(1700);
  const B = await passe('b');
  const xy = await passe('xy');
  const gm = await p.evaluate(() => window.__T.gmin);
  await p.evaluate(() => { window.__T.gmin = 23 * 60; });
  await p.waitForTimeout(600);
  const N = await passe('n');
  await p.evaluate((g) => { window.__T.gmin = g; }, gm);
  const spr = {}; const pngs = {};
  for (const i of Object.keys(A)) {
    const a = A[i], bb = B[i], n = N[i], q = xy[i];
    if (a.vazio) { spr[i] = { vazio: 1, err: a.err }; continue; }
    const vivo = !bb || bb.k !== a.k, noite = !n || n.k !== a.k, posicao = !q || q.k !== a.k || q.ox !== a.ox || q.oy !== a.oy;
    spr[i] = { k: a.k, kc: a.kc, ox: a.ox, oy: a.oy, w: a.w, h: a.h, vivo, noite, posicao, err: a.err };
    if (!pngs[a.k]) { pngs[a.k] = 1; fs.writeFileSync(path.join(outDir, 'spr', a.k + '.png'), Buffer.from(a.png.split(',')[1], 'base64')); }
  }
  fs.writeFileSync(path.join(outDir, 'desenhos.json'), JSON.stringify(spr));
  fs.writeFileSync(path.join(outDir, 'info.json'), JSON.stringify({ url, assentou, erros }, null, 1));
  console.log(JSON.stringify({ assentou, erros: erros.slice(0, 20), objetosCentro: Object.keys(spr).length, desenhosUnicos: Object.keys(pngs).length, vivos: Object.values(spr).filter(s => s.vivo).length, noite: Object.values(spr).filter(s => s.noite).length, posicao: Object.values(spr).filter(s => s.posicao).length }, null, 1));
  await b.close();
})().catch(e => { console.error('FALHOU', e); process.exit(1); });
