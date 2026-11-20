#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABERTURA RAPIDA do Piratininga
==============================
Rode DEPOIS de montar o jogo e ANTES de subir para o GitHub:

    python3 jogos/ferramentas/abertura_rapida.py

O que faz (pode rodar quantas vezes quiser):
  1. Le jogos/piratininga.html e os 5 arquivos jogos/arte/arte_*.js (a saida normal da montagem).
  2. Reparte a arte em pacotes por epoca (jogos/arte/pac_*.js), usando o mapa de uso
     jogos/ferramentas/uso_arte.json (quais imagens cada epoca usa).
  3. Troca, no piratininga.html, a carga dos 5 arquivos por um carregador que baixa so
     os pacotes da epoca que a pessoa vai jogar. O resto chega depois, por tras.
Se alguem esquecer de rodar, o jogo continua funcionando do jeito antigo (mais lento).
Com #teste no endereco o jogo carrega TUDO, como antes (para os testes automaticos).
"""
import json, re, os, sys, hashlib, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
JOGOS = os.path.dirname(AQUI)
HTML = os.path.join(JOGOS, 'piratininga.html')
ARTE = os.path.join(JOGOS, 'arte')
ERA_DO_ARQ = {'1554': 1, '1830': 2, '1888': 3, '1922': 4}
ADIA_KB = 25  # imagem "solta" (nunca usada na largada) maior que isto fica para depois

def le_arte(nome):
    s = open(os.path.join(ARTE, 'arte_%s.js' % nome), encoding='utf-8').read()
    return json.loads(s[s.index('=') + 1:].rstrip().rstrip(';'))

def era_pelo_nome(k):
    if re.search(r'(?<!\d)(1922|22|1914|1930)(?!\d)', k): return 4
    if re.search(r'(?<!\d)(1888|88)(?!\d)', k): return 3
    if re.search(r'(?<!\d)(1830|30)(?!\d)', k): return 2
    return 0

def planeja(arq, uso):
    """devolve {nome_do_pacote: {chave: valor}}"""
    P = {}
    for nome, d in arq.items():
        for k, v in d.items():
            F = set(uso.get(k, ())) - {'pre'}
            E = {int(x[1]) for x in F if re.fullmatch(r'e\d', x)}
            if nome != 'comum':
                eras = E | {ERA_DO_ARQ[nome]}
            elif k not in uso:
                eras = {1, 2, 3, 4}                      # imagem nova, ainda sem mapa: vai no pacote geral
            elif 'ini' in F:
                eras = {1, 2, 3, 4}
            elif 'boot' in F:                            # o jogo confere esta imagem na largada
                e0 = era_pelo_nome(k)
                eras = set(range(e0, 5)) if e0 else {1, 2, 3, 4}
                eras |= E
            elif E and E != {1, 4}:                      # ({1,4} sozinho = so apareceu ao abrir o Diario)
                eras = E
            else:
                e0 = era_pelo_nome(k)
                eras = set() if len(v) >= ADIA_KB * 1024 else (set(range(e0, 5)) if e0 else {1, 2, 3, 4})
            if not eras:
                b = 'depois_b' if re.match(r'(AUD_|REC_)', k) or re.fullmatch(r'[A-Z]{1,3}', k) else 'depois_a'
            else:
                b = 'e' + ''.join(str(e) for e in sorted(eras))
            P.setdefault(b, {})[k] = v
    return P

LOADER = r'''<script>/*ABERTURA_RAPIDA*/(function(){
var P=__LISTA__;
function eraDe(sc){sc=String(sc);return (sc==='sp22'||sc.indexOf('m_')===0)?4:(sc==='sp88'||sc==='faz'||sc==='santos'||sc.indexOf('k_')===0)?3:(sc==='sp'||sc==='arr'||sc.indexOf('i_')===0)?2:1;}
var era=1,tudo=false,pend=null;
try{pend=JSON.parse(sessionStorage.getItem('pira_boot')||'null');sessionStorage.removeItem('pira_boot');}catch(e){}
try{var m=/[?&]pb=([^&#]+)/.exec(location.search);if(!pend&&m)pend=JSON.parse(decodeURIComponent(m[1]));}catch(e){}
try{if(pend&&pend.era)era=pend.era;else{var sv=JSON.parse(localStorage.getItem('piratininga1554_v2')||'null');if(sv&&sv.scene)era=eraDe(sv.scene);}}catch(e){}
if(location.hash==='#teste'){tudo=true;try{if(localStorage.getItem('pira_teste_rapido'))tudo=false;}catch(e){}}
var boot=[];for(var i=0;i<P.length;i++){if(tudo||(!P[i].d&&(P[i].m&(1<<(era-1)))))boot.push(P[i]);}
window.__ARTE={};window.__PAC={lista:P,era:era,tudo:tudo,boot:{},pend:pend,falhou:[]};
var n=0;
window.__pacOk=function(f){window.__PAC.boot[f]=1;n++;try{window.__carrega&&window.__carrega(0.2+0.7*n/boot.length,'Carregando a arte do jogo... ('+n+' de '+boot.length+')');}catch(e){}};
window.__pacErro=function(f){window.__PAC.falhou.push(f);};
window.__pacFim=function(){window.__ARTE_comum=window.__ARTE;window.__ARTE_1554={};window.__ARTE_1830={};window.__ARTE_1888={};window.__ARTE_1922={};
 if(window.__PAC.falhou.length){document.body.insertAdjacentHTML('afterbegin','<div id="pacAviso" style="position:fixed;left:0;right:0;top:0;z-index:99999;margin:0;padding:14px;background:#fff3cd;color:#141b1b;font:600 16px/1.4 system-ui,sans-serif;text-align:center">A internet falhou e uma parte dos desenhos não chegou. <button type="button" onclick="location.reload()" style="font:inherit;padding:8px 14px;margin-left:8px;border-radius:8px;border:2px solid #141b1b;background:#f09a4e;cursor:pointer">Tentar de novo</button></div>');}};
var h='';for(var j=0;j<boot.length;j++){h+='<script src="arte/'+boot[j].f+'" onload="__pacOk(\''+boot[j].f+'\')" onerror="__pacErro(\''+boot[j].f+'\')"><\/script>';}
h+='<script>__pacFim()<\/script>';
try{window.__carrega&&window.__carrega(0.15,'Carregando a arte do jogo...');}catch(e){}
document.write(h);
})();</script>'''

RUNTIME = r'''/*ABERTURA_RAPIDA_FIM*/;(function(){
if(!window.__PAC)return;const PAC=window.__PAC,P=PAC.lista,ANO={1:1554,2:1830,3:1888,4:1922};
const bit=e=>1<<(e-1);
const naBoot=e=>PAC.tudo||P.every(p=>p.d||!(p.m&bit(e))||PAC.boot[p.f]);
PAC.naBoot=naBoot;
if(!PAC.tudo){const pr=CanvasRenderingContext2D.prototype,di=pr.drawImage;pr.drawImage=function(im){if(!im){PAC.faltou=(PAC.faltou||0)+1;if(window.__PACDBG){const t=(new Error().stack.split('\n')[2]||'').trim().slice(-30);window.__PACDBG[t]=(window.__PACDBG[t]||0)+1;}return;}try{return di.apply(this,arguments);}catch(e){PAC.quebrou=(PAC.quebrou||0)+1;}};try{const po=OffscreenCanvasRenderingContext2D.prototype,dj=po.drawImage;po.drawImage=function(im){if(!im)return;try{return dj.apply(this,arguments);}catch(e){}};}catch(_){}}
const tarde={};PAC.tarde=tarde;
function junta(){try{const N=window.__ARTE;for(const k in N)if(!(k in A))A[k]=N[k];}catch(_){}}
function carrega(p){return new Promise((res,rej)=>{if(PAC.boot[p.f]||tarde[p.f])return res();const s=document.createElement('script');s.src='arte/'+p.f;s.async=true;
  s.onload=()=>{junta();tarde[p.f]=1;res();};s.onerror=()=>{s.remove();rej(new Error(p.f));};document.head.appendChild(s);});}
/* ---------- tela de espera (com um brinquedo para distrair) ---------- */
let tela=null,grãos=0;
function mostra(e,txt){if(tela)return;const st=document.createElement('style');
 st.textContent='#pacTela{position:fixed;inset:0;z-index:99998;background:#141b1b;color:#f6f0e4;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:20px;font:600 18px/1.4 Inter,system-ui,sans-serif;text-align:center}#pacTela .b{width:min(320px,80vw);height:16px;border:3px solid #f6f0e4;border-radius:4px;overflow:hidden}#pacTela .b i{display:block;height:100%;width:8%;background:repeating-linear-gradient(45deg,#f1c471 0 10px,#d99a3e 10px 20px);transition:width .3s}#pacTela small{font-weight:500;color:#cfc7b6;font-size:15px}#pacGrao{width:64px;height:64px;border-radius:50%;border:3px solid #f6f0e4;background:#8a4b2a;cursor:pointer;position:relative;animation:pacPula 1s ease-in-out infinite;-webkit-tap-highlight-color:transparent}#pacGrao::after{content:"";position:absolute;left:50%;top:10%;bottom:10%;width:4px;margin-left:-2px;background:#4a2412;border-radius:2px}#pacGrao.t{animation:pacGira .35s linear}@keyframes pacPula{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}@keyframes pacGira{to{transform:rotate(360deg) scale(1.15)}}#pacTela button.r{font:inherit;padding:10px 16px;border-radius:10px;border:3px solid #f6f0e4;background:#f09a4e;color:#141b1b;cursor:pointer}';
 document.head.appendChild(st);tela=document.createElement('div');tela.id='pacTela';
 tela.innerHTML='<div id="pacTit"></div><div class="b"><i id="pacBar"></i></div><small id="pacTxt"></small><button type="button" id="pacGrao" aria-label="Grão de café: toque para girar"></button><small id="pacCont">Enquanto espera, toque no grão de café!</small><button type="button" class="r" id="pacDeNovo" hidden>Tentar de novo</button>';
 document.body.appendChild(tela);document.getElementById('pacTit').textContent=txt||('Viajando para '+ANO[e]+'...');document.getElementById('pacTxt').textContent='Buscando os desenhos desta época.';
 const g=document.getElementById('pacGrao');g.addEventListener('click',()=>{grãos++;g.classList.remove('t');void g.offsetWidth;g.classList.add('t');document.getElementById('pacCont').textContent=grãos===1?'1 giro!':grãos+' giros!';});}
function some(){if(tela){tela.remove();tela=null;}}
function prog(a,b){const i=document.getElementById('pacBar');if(i)i.style.width=Math.max(8,Math.round(100*a/Math.max(1,b)))+'%';}
async function garante(e){const need=P.filter(p=>!p.d&&(p.m&bit(e))&&!PAC.boot[p.f]);
 for(let i=0;i<need.length;i++){for(;;){try{await carrega(need[i]);break;}catch(_){
   const t=document.getElementById('pacTxt'),b=document.getElementById('pacDeNovo');if(t)t.textContent='A internet falhou. Confira a conexão e toque em "Tentar de novo".';
   await new Promise(r=>{if(!b)return setTimeout(r,4000);b.hidden=false;b.onclick=()=>{b.hidden=true;if(t)t.textContent='Buscando os desenhos desta época.';r();};});}}
  prog(i+1,need.length);}}
let trocando=false;
function troca(e,extra){if(trocando)return;trocando=true;const dados=Object.assign({era:e},extra||{});let ok=false;
 try{sessionStorage.setItem('pira_boot',JSON.stringify(dados));ok=sessionStorage.getItem('pira_boot')!==null;}catch(_){}
 mostra(e);garante(e).then(()=>{if(ok)location.reload();else location.replace(location.pathname+'?pb='+encodeURIComponent(JSON.stringify(dados))+location.hash);});}
PAC.troca=troca;
/* ---------- 1) botões de começar ---------- */
const BT={btnStart:1,btn1830:2,btn1888:3,btn1922:4};
document.addEventListener('click',ev=>{const b=ev.target&&ev.target.closest&&ev.target.closest('#btnStart,#btn1830,#btn1888,#btn1922');if(!b)return;const e=BT[b.id];if(naBoot(e))return;
 ev.stopImmediatePropagation();ev.preventDefault();try{localStorage.removeItem(SKEY);}catch(_){}troca(e,{auto:b.id});},true);
/* ---------- 2) portais entre as épocas ---------- */
let pronto=false,retomando=false;
const o2=startEra2,o3=startEra3,o4=startEra4;
const portal=(e,o)=>function(){if(naBoot(e))return o.apply(this,arguments);try{save();}catch(_){}troca(e,{portal:e});};
startEra2=portal(2,o2);startEra3=portal(3,o3);startEra4=portal(4,o4);
/* ---------- 3) qualquer outra ida para uma época que ainda não foi carregada (código, viagem) ---------- */
const ss=setScene;
setScene=function(n){const r=ss.apply(this,arguments);try{const e=eraOf(n);if(pronto&&!trocando&&!retomando&&!naBoot(e)){mostra(e);setTimeout(()=>{try{save();}catch(_){}troca(e,{cont:1});},60);}}catch(_){}return r;};
/* ---------- depois de recarregar: continua de onde a pessoa estava ---------- */
const pend=PAC.pend;if(pend&&(pend.auto||pend.portal||pend.cont))mostra(pend.era,'Chegando em '+ANO[pend.era]+'...');
function entra(){const sp=document.getElementById('btnSplash');if(sp)sp.click();}
function retoma(){const sv=loadSave();if(sv){applySave(sv);}ovStart.hidden=true;started=true;try{updQuest();checkZone();reveal(player.x,player.y);}catch(_){}}
let n=0;const iv=setInterval(()=>{n++;const sp=document.getElementById('btnSplash');if(sp&&sp.disabled&&n<300)return;clearInterval(iv);pronto=true;
 try{if(pend&&pend.auto){entra();setTimeout(()=>{const b=document.getElementById(pend.auto);if(b)b.click();some();},250);}
  else if(pend&&pend.portal){entra();setTimeout(()=>{retomando=true;try{retoma();}finally{retomando=false;}({2:o2,3:o3,4:o4})[pend.portal]();setTimeout(some,1300);},250);}
  else if(pend&&pend.cont){entra();setTimeout(()=>{retoma();some();},250);}
  else some();}catch(e){some();console.warn('abertura rapida',e);}
 /* o resto da arte chega por trás: primeiro o que ficou "para depois", depois as outras épocas */
 let semFundo=false;try{semFundo=!!localStorage.getItem('pira_teste_semfundo');}catch(_){}
 if(!PAC.tudo&&!semFundo)setTimeout(async()=>{const fila=P.filter(p=>p.d).concat(P.filter(p=>!p.d).sort((a,b)=>{const pa=(a.m&bit(Math.min(4,PAC.era+1)))?0:1,pb=(b.m&bit(Math.min(4,PAC.era+1)))?0:1;return pa-pb;}));
  for(const p of fila){for(let t=0;t<4;t++){try{await carrega(p);break;}catch(_){await new Promise(r=>setTimeout(r,5000*(t+1)));}}}},1500);
},200);
})();/*FIM_ABERTURA_RAPIDA*/'''

def main():
    s = open(HTML, encoding='utf-8').read()
    uso = json.load(open(os.path.join(AQUI, 'uso_arte.json'), encoding='utf-8'))
    arq = {n: le_arte(n) for n in ['comum', '1554', '1830', '1888', '1922']}
    plano = planeja(arq, uso)
    for velho in glob.glob(os.path.join(ARTE, 'pac_*.js')): os.remove(velho)
    lista = []
    for b in sorted(plano, key=lambda x: (x.startswith('depois'), x)):
        corpo = "(window.__ARTE=window.__ARTE||{});Object.assign(window.__ARTE," + json.dumps(plano[b], ensure_ascii=False, separators=(',', ':')) + ");\n"
        nome = 'pac_%s.js' % b
        open(os.path.join(ARTE, nome), 'w', encoding='utf-8').write(corpo)
        h = hashlib.md5(corpo.encode('utf-8')).hexdigest()[:8]
        item = {'f': nome + '?v=' + h, 'kb': len(corpo) // 1024}
        if b.startswith('depois'): item.update(m=0, d=1)
        else: item['m'] = sum(1 << (int(c) - 1) for c in b[1:])
        lista.append(item)
        print('%-16s %4d imagens %6d KB' % (nome, len(plano[b]), item['kb']))
    loader = LOADER.replace('__LISTA__', json.dumps(lista, separators=(',', ':')))
    if '/*ABERTURA_RAPIDA*/' in s:   # ja estava aplicado: troca so os dois blocos
        s, n1 = re.subn(r'<script>/\*ABERTURA_RAPIDA\*/.*?</script>', lambda m: loader, s, count=1, flags=re.S)
        s, n2 = re.subn(r'/\*ABERTURA_RAPIDA_FIM\*/.*?/\*FIM_ABERTURA_RAPIDA\*/', lambda m: RUNTIME, s, count=1, flags=re.S)
        assert n1 == 1 and n2 == 1, 'blocos da abertura rapida nao encontrados'
    else:
        a = s.index('<script src="arte/arte_comum.js')
        fim = "if(!window.__ARTE_comum)f.push('arte_comum.js')"
        b = s.index(fim, a); b = s.index('</script>', b) + len('</script>')
        s = s[:a] + loader + s[b:]
        fecho = '\n})();\n</script>'
        z = s.rindex(fecho)          # fim do script grande do jogo (o runtime entra dentro dele)
        s = s[:z] + '\n' + RUNTIME + s[z:]
    open(HTML, 'w', encoding='utf-8').write(s)
    for e in (1, 2, 3, 4):
        print('epoca %d na largada: %d KB' % (ANO[e], sum(i['kb'] for i in lista if i['m'] & (1 << (e - 1)))))
    print('pronto: piratininga.html com a abertura rapida')

ANO = {1: 1554, 2: 1830, 3: 1888, 4: 1922}
if __name__ == '__main__':
    main()
