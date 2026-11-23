# Insere um "gancho de teste" no fim do código principal (só para testes; não vai para o GitHub)
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf8').read()
k=s.rfind('})();/*FIM_ABERTURA_RAPIDA*/')
assert k>0
j=s.index('\n',k)+1
assert s[j:j+5]=='})();', s[j:j+20]
hook="""try{window.__T={get stat(){return stat;},get sc(){return sc;},get t(){return t;},set t(v){t=v;},bs:()=>buildStatic(),bo:()=>buildOcc(),
get walkers(){return walkers;},get objects(){return objects;},get npcs(){return npcs;},get ITEMS(){return ITEMS;},SCN,INT,QT,get FONTES(){return typeof FONTES!=='undefined'?FONTES:null;},
get ROTEIRO(){return ROTEIRO;},get GIVER(){return typeof GIVER!=='undefined'?GIVER:null;},get Q(){return Q;},player,get camX(){return camX;},get camY(){return camY;},
get TILE_INFO(){return TILE_INFO;},T,get VW(){return VW;},get VH(){return VH;},setScene,get A(){return typeof A!=='undefined'?A:null;},drawSceneInto,walkersRender,drawChar,here,get gmin(){return gmin;},set gmin(v){gmin=v;},get era(){return era;}};}catch(e){console.warn('gancho',e);}
"""
s=s[:j]+hook+s[j:]
m=s.rfind('/* =====',0,s.index('CENTRO DE 1922 VIRA MAPA FIXO')) if 'CENTRO DE 1922 VIRA MAPA FIXO' in s else s.index('/* =========================================================\n   CENTRO AMPLIADO DE 1922')
s=s[:m]+"try{window.__drawAntes=new Map(objects.map(o=>[o,o.draw]));window.__objAntes=new Set(objects);window.__cenaAntes=new Map(objects.map(o=>[o,o.scene]));window.__npcAntes=new Map(npcs.map(n=>[n,n.scene]));window.__itAntes=new Map(ITEMS.map(n=>[n,n.scene]));window.__fontesAntes=new Set(typeof FONTES!=='undefined'?Object.keys(FONTES):[]);}catch(e){}\n"+s[m:]
s=s.replace("const K='m_centro22';let MINHAS=null,cx=0,cy=0;","const K='m_centro22';let MINHAS=null,cx=0,cy=0;window.__MINHAS_get=()=>MINHAS;",1)
open(dst,'w',encoding='utf8').write(s)
print('ok')
