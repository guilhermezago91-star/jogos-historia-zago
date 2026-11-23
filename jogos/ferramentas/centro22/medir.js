// Mede o tempo de entrada no centro de 1922, até parar de engasgar, e a volta de uma loja.
// uso: node medir.js <url> <cpu_rate> <saida.json> [extraJS]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const [url, rate, out, extra] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  const p = await ctx.newPage();
  const erros = [];
  p.on('pageerror', e => erros.push(String(e)));
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') erros.push(m.type() + ': ' + m.text().slice(0, 200)); });
  if (extra) await p.addInitScript(extra);
  await p.goto(url, { waitUntil: 'load', timeout: 180000 });
  await p.waitForFunction(() => window.__G && window.__G.start, null, { timeout: 180000 });
  await p.waitForTimeout(4000);
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: Number(rate) });
  // registrador de quadros
  await p.evaluate(() => { window.__fr = []; const f = () => { window.__fr.push([performance.now(), window.__G.cur]); requestAnimationFrame(f); }; requestAnimationFrame(f); });
  const t0 = await p.evaluate(() => { window.__G.start(); window.__G.startEra4(); return performance.now(); });
  const limite = Number(rate) > 1 ? 150000 : 60000;
  await p.waitForTimeout(limite);
  const r1 = await p.evaluate((t0) => {
    const F = window.__fr; let chegou = null; for (const [t, c] of F) if (c === 'm_centro22' && t > t0) { chegou = t; break; }
    let maior = 0, ultimoEngasgo = null, bloqueado = 0;
    for (let i = 1; i < F.length; i++) { const g = F[i][0] - F[i - 1][0]; if (F[i][0] < t0) continue; if (g > maior) maior = g; if (g > 150) { ultimoEngasgo = F[i][0]; bloqueado += g; } }
    return { chegou: chegou && (chegou - t0) / 1000, maiorCongelamento: maior / 1000, tempoBloqueado: bloqueado / 1000, paraDeEngasgar: ultimoEngasgo && (ultimoEngasgo - t0) / 1000, cur: window.__G.cur, rodadas: Object.keys(window.__jmTeste || {}).filter(k => /^r\d/.test(k)).join(',') };
  }, t0);
  // volta ao centro saindo de uma loja
  const r2 = await p.evaluate(async () => {
    const G = window.__G; const o = G.objects.find(o => o.scene === 'm_centro22' && o.enter && o.room && G.SCN[o.room]);
    if (!o) return { erro: 'sem loja' };
    const R = G.SCN[o.room]; G.setScene(o.room); await new Promise(r => setTimeout(r, 1500));
    window.__fr = []; const a = performance.now();
    G.setScene('m_centro22'); const b = performance.now();
    await new Promise(r => setTimeout(r, 4000));
    const F = window.__fr; let maior = 0; for (let i = 1; i < F.length; i++) maior = Math.max(maior, F[i][0] - F[i - 1][0]);
    return { loja: o.name, voltaSetScene: (b - a) / 1000, maiorQuadroDepois: maior / 1000 };
  });
  const res = { url, rate: Number(rate), entrada: r1, voltaLoja: r2, erros: erros.slice(0, 30) };
  require('fs').writeFileSync(out, JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
  await b.close();
})().catch(e => { console.error('FALHOU', e); process.exit(1); });
