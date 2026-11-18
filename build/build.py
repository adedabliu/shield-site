"""Gera o site estático da Shield (uma página por URL) a partir de index.html + data.json.
Uso: python3 build.py prod   -> ../dist  (URLs limpas, para hospedar no domínio)
     python3 build.py preview -> ../preview (links com index.html, para a prévia no Claude)
"""
import json, re, sys, html, shutil, pathlib, datetime

SITE = 'https://shieldcredito.com.br'   # <- trocar pelo domínio definitivo e rodar de novo
WA = '5512991346990'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'prod'
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / ('dist' if MODE == 'prod' else 'preview')
SRC = (ROOT / 'index.html').read_text()
D = json.loads((ROOT / 'build' / 'data.json').read_text())
P, SIT, FAQ, ART = D['P'], D['SIT'], D['FAQ'], D['ART']
TODAY = datetime.date(2026, 11, 18)
E = html.escape

# ---- rotas -------------------------------------------------------------
SLUG = {'home-equity': 'emprestimo-com-garantia-de-imovel', 'consorcio': 'consorcio-e-cartas-contempladas',
        'financiamento': 'financiamento-imobiliario', 'construcao': 'credito-para-construcao',
        'capital-de-giro': 'capital-de-giro-com-garantia-de-imovel', 'consorcio-empresarial': 'consorcio-empresarial',
        'imovel-comercial': 'financiamento-de-imovel-comercial'}
PAGE = {'inicio': '', 'voce': 'para-voce', 'empresas': 'para-empresas', 'simular': 'simulador', 'parceiros': 'parceiros',
        'sobre': 'sobre', 'duvidas': 'duvidas', 'conteudo': 'conteudo', 'links': 'links', 'contato': 'contato'}
PATH = {**PAGE, **SLUG}

H1 = {'home-equity': 'Empréstimo com garantia de imóvel: troque a dívida cara por uma parcela que cabe',
      'consorcio': 'Consórcio e cartas contempladas: compre sem juros ou sem esperar',
      'financiamento': 'Financiamento imobiliário com entrada e parcela comparadas antes de assinar',
      'construcao': 'Crédito para construção liberado em etapas, no ritmo da obra',
      'capital-de-giro': 'Capital de giro com garantia de imóvel e prazo de anos, não de meses',
      'consorcio-empresarial': 'Consórcio empresarial para frota, máquinas e sede sem juros',
      'imovel-comercial': 'Financiamento de imóvel comercial e crédito com a sede como garantia'}
EXTRA_Q = {'home-equity': [
    ['É a mesma coisa que hipoteca ou refinanciamento de imóvel?', 'Muita gente chama assim. Hoje a operação é feita por alienação fiduciária (Lei 9.514/97): o imóvel fica registrado como garantia na matrícula até a quitação, e você continua dono e morando nele. Também é conhecida como home equity ou CGI, crédito com garantia de imóvel.'],
    ['Dá para usar um imóvel que ainda está financiado?', 'Depende da instituição e do saldo devedor. Em alguns casos o novo crédito quita o financiamento atual e o restante fica com você. A gente avalia no diagnóstico.'],
    ['Qual é a taxa de juros?', 'Depende da instituição, do imóvel, do prazo e da análise de crédito. Costuma ficar bem abaixo do crédito pessoal e do cartão. Compare sempre pelo CET, o custo efetivo total, que a Shield mostra antes de você assinar.']]}

META = {
 'inicio': ('Empréstimo com garantia de imóvel e consórcio | Shield', 'Empréstimo com garantia de imóvel, consórcio e financiamento em São José dos Campos e região. Compare as parceiras pelo custo total e simule grátis.'),
 'voce': ('Crédito para você com garantia de imóvel | Shield', 'Empréstimo com garantia de imóvel, consórcio, financiamento imobiliário e crédito para construção. Escolha pelo que quer resolver e simule.'),
 'empresas': ('Crédito para empresas com garantia de imóvel | Shield', 'Capital de giro com garantia de imóvel, consórcio empresarial e financiamento de imóvel comercial, com prazo de até 240 meses. Simule grátis.'),
 'simular': ('Simulador de empréstimo com garantia de imóvel | Shield', 'Simule empréstimo com garantia de imóvel, consórcio ou financiamento em um minuto. Um consultor responde pelo WhatsApp com o custo total.'),
 'parceiros': ('Seja parceiro: indique crédito com garantia | Shield', 'Corretores, contadores e advogados: indiquem clientes para empréstimo com garantia de imóvel e consórcio e acompanhem cada etapa.'),
 'sobre': ('Sobre a Shield Soluções Financeiras', 'A Shield compara instituições parceiras, mostra o custo total e acompanha o cliente até o registro em cartório. Unidade franqueada Velox.'),
 'duvidas': ('Dúvidas sobre crédito com garantia de imóvel | Shield', 'Respostas diretas sobre empréstimo com garantia de imóvel, CET, consórcio, score e segurança. Saiba o que perguntar antes de assinar.'),
 'conteudo': ('Crédito explicado sem letra miúda | Shield', 'Artigos sobre empréstimo com garantia de imóvel, cartas contempladas, LTV e como trocar dívida cara por barata, escritos sem letra miúda.'),
 'links': ('Links | Shield Soluções Financeiras', 'Simule seu crédito, fale no WhatsApp e conheça a Shield.'),
 'contato': ('Contato | Shield Soluções Financeiras', 'Fale com um consultor da Shield pelo WhatsApp (12) 99134-6990. Escritório na Av. Salmão, 663, Parque Residencial Aquarius, São José dos Campos/SP.'),
 'home-equity': ('Empréstimo com garantia de imóvel: como funciona | Shield', 'Empréstimo com garantia de imóvel com até 60% do valor do imóvel e prazo de até 240 meses. Troque dívida cara e continue morando. Simule.'),
 'consorcio': ('Consórcio e cartas contempladas de imóvel | Shield', 'Consórcio imobiliário sem juros para quem planeja e cartas de crédito contempladas para quem tem pressa. Compare com a Shield e simule.'),
 'financiamento': ('Financiamento imobiliário com comparação | Shield', 'Financiamento imobiliário com até 240 meses e comparação entre linhas, inclusive com FGTS quando fizer sentido. Simule a entrada e a parcela.'),
 'construcao': ('Crédito para construção em etapas | Shield', 'Crédito para construção de até 50% do imóvel pronto, liberado conforme a obra avança, com carência de até 3 meses. Simule com a Shield.'),
 'capital-de-giro': ('Capital de giro com garantia de imóvel | Shield', 'Capital de giro com garantia de imóvel da empresa ou dos sócios, prazo de até 240 meses e parcela que cabe no caixa. Simule com a Shield.'),
 'consorcio-empresarial': ('Consórcio empresarial: frota, máquinas e sede | Shield', 'Consórcio para empresas renovarem frota, comprarem máquinas ou a sede própria sem juros, com cartas contempladas para quem tem pressa.'),
 'imovel-comercial': ('Financiamento de imóvel comercial | Shield', 'Financiamento de sala, loja ou galpão e crédito usando o imóvel comercial da empresa como garantia, com prazo de até 240 meses. Simule.'),
}

def href(key, depth, frag=''):
    p = PATH[key]
    pre = '../' * depth
    if MODE == 'preview':
        url = pre + (p + '/' if p else '') + 'index.html'
    else:
        url = pre + (p + '/' if p else '') if (pre or p) else './'
    return url + (('#' + frag) if frag else '')

def canon(key):
    p = PATH[key]
    return SITE + '/' + (p + '/' if p else '')

# ---- CSS ---------------------------------------------------------------
css = SRC[SRC.index('<style>') + 7: SRC.index('</style>')]
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css += """
.lead{font-size:clamp(17px,1.6vw,19px)}
.upd{font-size:13.5px;color:var(--aco);margin-top:14px}
.prod h1{font-size:clamp(32px,4.2vw,52px)}
section{display:block}
"""
FONT = ("@font-face{font-family:Inter;src:url(%sassets/fonts/inter.woff2) format('woff2');font-weight:400 800;font-display:swap}"
        "@font-face{font-family:Michroma;src:url(%sassets/fonts/michroma.woff2) format('woff2');font-weight:400;font-display:swap}")

def mincss(c):
    c = re.sub(r'\s+', ' ', c)
    c = re.sub(r'\s*([{};,>])\s*', r'\1', c)
    return c.replace(';}', '}').strip()

# ---- pedaços do index.html --------------------------------------------
def section(name):
    m = re.search(r'<section data-p="%s">(.*?)</section>' % name, SRC, re.S)
    return m.group(1)

def fix_links(h, depth):
    def rep(m):
        k = m.group(1)
        if k in PATH: return 'href="%s"' % href(k, depth)
        return m.group(0)
    h = re.sub(r'href="#([\w-]+)"', rep, h)
    h = h.replace('src="assets/logo.png"', 'src="%sassets/logo-150.webp" srcset="%sassets/logo-150.webp 150w, %sassets/logo.webp 300w" sizes="134px" width="300" height="98"' % (('../' * depth,)*3))
    h = h.replace('src="assets/simbolo.png"', 'src="%sassets/simbolo.webp" width="192" height="204"' % ('../' * depth))
    h = h.replace('src="assets/logo-claro.png"', 'src="%sassets/logo-claro-150.webp" srcset="%sassets/logo-claro-150.webp 150w, %sassets/logo-claro.webp 300w" sizes="160px" width="300" height="98" loading="lazy"' % (('../' * depth,)*3))
    return h

def faq_html(items):
    return ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)

WIN = ''.join('<rect x="%d" y="%d" width="10" height="13" rx="1"/>' % (300 + c * 18, 166 + r * 24) for r in range(5) for c in range(3))

def body_inicio(d):
    h = section('inicio').replace('<g fill="#9FB0C4" id="win"></g>', '<g fill="#9FB0C4">%s</g>' % WIN)
    h = h.replace('<div class="faq" data-n="3"></div>', '<div class="faq">%s</div>' % faq_html(FAQ[:3]))
    h = h.replace('Crédito com garantia · Consórcio · Financiamento', 'Empréstimo com garantia de imóvel · Consórcio')
    h = h.replace('<p class="lead">Para você e para a sua empresa. A gente coloca',
                  '<p class="lead">Empréstimo com garantia de imóvel, consórcio e financiamento para você e para a sua empresa. A gente coloca')
    return fix_links(h, d)

def trilha(t, d):
    h = section('voce' if t == 'pf' else 'empresas')
    sit = ''.join('<a href="%s"><span>%s</span><b>%s →</b></a>' % (href(s, d), E(a), E(next(p['k'] for p in P if p['s'] == s))) for a, s in SIT[t])
    cards = ''.join('<a class="card" href="%s"><h3>%s</h3><p>%s</p><span class="go">Ver detalhes →</span></a>' % (href(p['s'], d), E(p['n']), E(p['h'])) for p in P if p['t'] == t)
    h = h.replace('id="sit-%s" style="margin-top:12px"></div>' % t, 'id="sit-%s" style="margin-top:12px">%s</div>' % (t, sit))
    h = h.replace('<div class="cards" id="cards-%s"></div>' % t, '<div class="cards" id="cards-%s">%s</div>' % (t, cards))
    return fix_links(h, d)

def produto(p, d):
    tri = ('voce', 'Para você') if p['t'] == 'pf' else ('empresas', 'Para sua empresa')
    outros = [x for x in P if x['t'] == p['t'] and x['s'] != p['s']]
    qs = p['o'] + EXTRA_Q.get(p['s'], [])
    sim = href('simular', d, SLUG[p['s']])
    li = lambda xs: ''.join('<li>%s</li>' % E(x) for x in xs)
    return f'''<article class="prod"><div class="band"><div class="wrap">
  <nav class="crumb" aria-label="Você está em"><a href="{href('inicio', d)}">Início</a> / <a href="{href(tri[0], d)}">{tri[1]}</a> / {E(p['n'])}</nav>
  <span class="mi">{E(p['n'])}</span>
  <h1 style="margin-top:14px;max-width:24ch">{E(H1[p['s']])}</h1>
  <p class="lead" style="margin-top:18px">{E(p['r'])}</p>
  <div class="row" style="margin-top:22px"><a class="btn cta" href="{sim}">Simular {E(p['k'].lower())}</a><a class="btn" href="https://wa.me/{WA}?text={E(__import__('urllib.parse').parse.quote('Olá, quero saber sobre ' + p['n'] + '.'))}" target="_blank" rel="noopener">Tirar dúvida no WhatsApp</a></div>
  <div class="facts">{''.join(f'<div class="fact"><span class="mi">{E(a)}</span><b>{E(b)}</b></div>' for a, b in p['f'])}</div>
  <p class="note">{E(p['fn'])}</p>
  <p class="upd">Atualizado em novembro de 2026 · Condições sujeitas à análise de crédito e às regras de cada instituição.</p>
 </div></div>
 <div class="band" style="padding-top:0"><div class="wrap split">
  <div><h2 style="font-size:28px">Para quando faz sentido</h2><ul class="list">{li(p['q'])}</ul>
   <h2 style="font-size:28px;margin-top:36px">Documentos que costumam pedir</h2><ul class="list">{li(p['d'])}</ul>
   <p class="note">A lista final depende da instituição. A gente manda por etapa, para você não juntar papel à toa.</p></div>
  <div><h2 style="font-size:28px;margin-bottom:12px">Perguntas sobre {E(p['n'][0].lower() + p['n'][1:])}</h2>{faq_html(qs)}</div>
 </div></div>
 <div class="band dark"><div class="wrap split">
  <div><h2>Quer ver a conta do seu caso?</h2><p style="margin-top:14px">Um consultor responde pelo WhatsApp com as opções e o custo total.</p><a class="btn cta" href="{sim}">Simular agora</a></div>
  <div><span class="mi">Outras opções {'para você' if p['t'] == 'pf' else 'para empresas'}</span><div class="sit lst">{''.join(f'<a href="{href(o["s"], d)}" style="background:var(--navy2);border-color:#2C4A72;color:var(--ala)">{E(o["n"])}<b style="color:#8FB0FF">→</b></a>' for o in outros)}</div></div>
 </div></div></article>''', qs

def body_simular(d):
    h = section('simular')
    opts = ''.join('<option value="%s" data-t="%s">%s</option>' % (SLUG[p['s']], p['t'], E(p['n'])) for p in P)
    h = h.replace('<select id="s-obj" name="obj"></select>', '<select id="s-obj" name="obj">%s<option value="outro" data-t="*">Ainda não sei, quero orientação</option></select>' % opts)
    h = h.replace('<h1 style="margin-top:14px">Conte o plano. A gente volta com a conta.</h1>',
                  '<h1 style="margin-top:14px">Simulador de empréstimo com garantia de imóvel, consórcio e financiamento</h1>')
    h = h.replace('<p style="margin-top:18px;font-size:18px">Leva um minuto.', '<p style="margin-top:18px;font-size:18px">Conte o plano e a gente volta com a conta. Leva um minuto.')
    return fix_links(h, d)

def body_parceiros(d):
    h = section('parceiros')
    h = h.replace('<select id="i-prod"></select>', '<select id="i-prod">%s</select>' % ''.join('<option>%s%s</option>' % (E(p['n']), ' (empresa)' if p['t'] == 'pj' else '') for p in P))
    return fix_links(h, d)

def body_duvidas(d):
    return fix_links(section('duvidas').replace('<div class="faq" data-n="99"></div>', '<div class="faq">%s</div>' % faq_html(FAQ)), d)

def body_conteudo(d):
    arts = ''.join('<article class="card"><h2 style="font-size:21px;letter-spacing:-.01em">%s</h2><p>%s</p><a class="go" href="%s" style="text-decoration:none">Fazer a conta do meu caso →</a></article>' % (E(t), E(x), href('simular', d)) for t, x in ART)
    return fix_links(section('conteudo').replace('<div class="cards" id="arts"></div>', '<div class="cards">%s</div>' % arts), d)

# ---- moldura (cabeçalho, rodapé, scripts) -----------------------------
HEADER = SRC[SRC.index('<header>'): SRC.index('</header>') + 9]
FOOTER = SRC[SRC.index('<footer>'): SRC.index('</footer>') + 9]
WABTN = SRC[SRC.index('<a class="wa"'): SRC.index('</a>', SRC.index('<a class="wa"')) + 4]

JS_MENU = "{const m=document.getElementById('menu'),n=document.getElementById('nav');m&&m.addEventListener('click',()=>{const o=n.classList.toggle('open');m.setAttribute('aria-expanded',o)})}"
JS_FORM = r"""const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],WA='%s';
const digits=v=>v.replace(/\D/g,'');
function done(box,form,title,msg){form.style.display='none';box.style.display='block';box.innerHTML='<h3>'+title+'</h3><p style="margin-top:10px">Toque no botão para enviar pelo WhatsApp. O consultor responde por lá.</p><a class="btn cta" href="https://wa.me/'+WA+'?text='+encodeURIComponent(msg)+'" target="_blank" rel="noopener">Enviar pelo WhatsApp</a><p style="margin-top:16px"><button class="btn" type="button" data-back>Corrigir os dados</button></p>';box.querySelector('[data-back]').onclick=()=>{box.style.display='none';form.style.display='grid'};box.querySelector('a').focus()}
function need(ids,ok,err){for(const i of ids){if(!$(i).value.trim()){$(err).textContent='Preencha os campos para continuar.';$(i).focus();return false}}const t=ids.find(i=>/tel/.test(i));if(digits($(t).value).length<10){$(err).textContent='Confira o número de WhatsApp com DDD.';$(t).focus();return false}if(!$(ok).checked){$(err).textContent='Marque a autorização para continuar.';return false}$(err).textContent='';return true}
""" % WA
JS_SIM = r"""{%s
const all=[...$('#s-obj').options].map(o=>o.cloneNode(true));
function fill(sel){const t=document.querySelector('input[name=tri]:checked').value;const s=$('#s-obj');s.innerHTML='';all.filter(o=>o.dataset.t===t||o.dataset.t==='*').forEach(o=>s.appendChild(o.cloneNode(true)));if(sel)s.value=sel}
const h=location.hash.slice(1),pre=all.find(o=>o.value===h&&h);if(pre)document.querySelector('input[name=tri][value='+pre.dataset.t+']').checked=true;fill(pre&&h);
$$('input[name=tri]').forEach(r=>r.addEventListener('change',()=>fill()));
$('#f-sim').addEventListener('submit',e=>{e.preventDefault();if(!need(['#s-nome','#s-tel','#s-cid'],'#s-ok','#s-err'))return;
const o=$('#s-obj').selectedOptions[0].textContent,t=document.querySelector('input[name=tri]:checked').value==='pf'?'para mim':'para minha empresa';
const m='Olá, sou '+$('#s-nome').value.trim()+', de '+$('#s-cid').value.trim()+'. Quero simular: '+o+' ('+t+').'+($('#s-val').value?' Valor: R$ '+$('#s-val').value+'.':'')+($('#s-imo').value?' Imóvel de R$ '+$('#s-imo').value+'.':'')+' Vim pelo site.';
done($('#d-sim'),$('#f-sim'),'Pronto, sua simulação está preparada.',m)})}""" % JS_FORM
JS_PAR = r"""{%s
$$('input[name=pt]').forEach(r=>r.addEventListener('change',()=>{const c=$('input[name=pt]:checked').value==='cad';$('#f-cad').style.display=c?'grid':'none';$('#f-ind').style.display=c?'none':'grid';$('#d-par').style.display='none'}));
$('#f-cad').addEventListener('submit',e=>{e.preventDefault();if(!need(['#c-nome','#c-tel','#c-cid'],'#c-ok','#c-err'))return;
done($('#d-par'),$('#f-cad'),'Cadastro preparado.','Olá, sou '+$('#c-nome').value.trim()+' ('+$('#c-prof').value+($('#c-emp').value?', '+$('#c-emp').value.trim():'')+'), de '+$('#c-cid').value.trim()+'. Quero ser parceiro da Shield.')});
$('#f-ind').addEventListener('submit',e=>{e.preventDefault();if(!need(['#i-par','#i-cli','#i-tel'],'#i-ok','#i-err'))return;
done($('#d-par'),$('#f-ind'),'Indicação preparada.','Indicação do parceiro '+$('#i-par').value.trim()+': cliente '+$('#i-cli').value.trim()+', WhatsApp '+$('#i-tel').value.trim()+'. Precisa de: '+$('#i-prod').value+'. '+$('#i-obs').value.trim())})}""" % JS_FORM

ORG = {"@type": ["FinancialService", "Organization"], "@id": SITE + "/#org", "name": "Shield Soluções Financeiras",
       "alternateName": "Shield Crédito", "url": SITE + "/", "logo": SITE + "/assets/icon-512.png", "image": SITE + "/assets/og.png",
       "telephone": "+55-12-99134-6990", "legalName": "Shield Soluções Financeiras e Energéticas Ltda", "taxID": "53.741.431/0001-75", "foundingDate": "2024-01-31",
       "address": {"@type": "PostalAddress", "streetAddress": "Av. Salmão, 663, sala 65", "addressLocality": "São José dos Campos", "addressRegion": "SP", "postalCode": "12246-260", "addressCountry": "BR"}, "areaServed": {"@type": "Country", "name": "Brasil"},
       "sameAs": ["https://www.instagram.com/shieldcredito/"],
       "description": "Consultoria em empréstimo com garantia de imóvel, consórcio e financiamento para pessoas e empresas.",
       "parentOrganization": {"@type": "Organization", "name": "Velox Soluções Financeiras"}}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def faqld(qs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}

def page(key, body, depth, ld=None, js='', noindex=False, header=True):
    title, desc = META[key]
    pre = '../' * depth
    hd = fix_links(HEADER, depth)
    navkey = {'voce': 'voce', 'empresas': 'empresas'}.get(key) or next((('voce' if p['t'] == 'pf' else 'empresas') for p in P if p['s'] == key), key)
    if navkey in PATH:
        hd = hd.replace('<a href="%s">' % href(navkey, depth), '<a href="%s" class="on" aria-current="page">' % href(navkey, depth), 1)
    hd = hd.replace('<a class="logo"', '<a class="logo"', 1).replace('<img src', '<img fetchpriority="high" src', 1)
    ft = fix_links(FOOTER, depth)
    for old, new in SLUG.items():
        ft = ft.replace('href="#%s"' % old, 'href="%s"' % href(old, depth))
    graph = [ORG, {"@type": "WebPage", "@id": canon(key), "url": canon(key), "name": title, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Shield Soluções Financeiras", "publisher": {"@id": SITE + "/#org"}}}] + (ld or [])
    css_page = mincss(FONT % (pre, pre) + css)
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon(key)}">
{'<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta name="theme-color" content="#0F2A4C">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Shield Soluções Financeiras">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon(key)}">
<meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/favicon.png" type="image/png"><link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<style>{css_page}</style>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
<a href="#conteudo-principal" class="skip">Pular para o conteúdo</a>
{hd if header else ''}
<main id="conteudo-principal">
{body}
</main>
{ft}
{WABTN}
<script>{JS_MENU}{js}</script>
</body>
</html>'''

css += ".skip{position:absolute;left:-999px;top:8px;z-index:50;background:var(--navy);color:#fff;padding:10px 16px;border-radius:8px}.skip:focus{left:8px}\n"

# ---- montar ------------------------------------------------------------
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(ROOT / 'dist_assets', OUT / 'assets')
pages = {}
home = canon('inicio')
pages['inicio'] = page('inicio', body_inicio(0), 0)
for t, k in (('pf', 'voce'), ('pj', 'empresas')):
    pages[k] = page(k, trilha(t, 1), 1, [crumbs([('Início', home), (META[k][0].split(' |')[0], canon(k))])])
for p in P:
    b, qs = produto(p, 1)
    tri = 'voce' if p['t'] == 'pf' else 'empresas'
    ld = [crumbs([('Início', home), ('Para você' if p['t'] == 'pf' else 'Para empresas', canon(tri)), (p['n'], canon(p['s']))]),
          faqld(qs), {"@type": "Service", "name": p['n'], "serviceType": p['n'], "provider": {"@id": SITE + "/#org"}, "areaServed": "BR", "url": canon(p['s']), "description": p['r']}]
    pages[p['s']] = page(p['s'], b, 1, ld)
pages['simular'] = page('simular', body_simular(1), 1, js=JS_SIM)
pages['parceiros'] = page('parceiros', body_parceiros(1), 1, js=JS_PAR)
pages['sobre'] = page('sobre', fix_links(section('sobre'), 1), 1)
pages['duvidas'] = page('duvidas', body_duvidas(1), 1, [faqld(FAQ)])
pages['conteudo'] = page('conteudo', body_conteudo(1), 1)
pages['contato'] = page('contato', fix_links(section('contato'), 1), 1)
pages['links'] = page('links', fix_links(section('links'), 1), 1, noindex=True, header=False)

for k, h in pages.items():
    d = OUT / PATH[k] if PATH[k] else OUT
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(h)

# 404
nf = page('inicio', f'<div class="band"><div class="wrap" style="min-height:40vh"><span class="mi">Erro 404</span><h1 style="margin-top:14px">Esta página não existe.</h1><p class="lead" style="margin-top:18px">Talvez o link tenha mudado. Comece por uma das trilhas:</p><div class="row" style="margin-top:22px"><a class="btn cta" href="/{PATH["simular"]}/">Simular crédito</a><a class="btn" href="/para-voce/">Para você</a><a class="btn" href="/para-empresas/">Para empresas</a></div></div></div>', 0, noindex=True)
nf = nf.replace('href="./', 'href="/').replace('src="assets/', 'src="/assets/').replace("url(assets/", "url(/assets/").replace('href="assets/', 'href="/assets/')
nf = re.sub(r'href="(?!/|https?:|#)([\w-]+/)', r'href="/\1', nf)
(OUT / '404.html').write_text(nf)

if MODE == 'prod':
    urls = [k for k in pages if k != 'links']
    pri = lambda k: '1.0' if k == 'inicio' else '0.9' if k in SLUG else '0.8' if k in ('voce', 'empresas', 'simular') else '0.5'
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{canon(k)}</loc><lastmod>{TODAY}</lastmod><priority>{pri(k)}</priority></url>\n' for k in urls) + '</urlset>\n'
    (OUT / 'sitemap.xml').write_text(sm)
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /links/\n\nSitemap: {SITE}/sitemap.xml\n')
    (OUT / 'CNAME').write_text(SITE.split('//')[1] + '\n'); (OUT / '.nojekyll').write_text('')
    if False: (OUT / '_headers').write_text("""/assets/*
  Cache-Control: public, max-age=31536000, immutable
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
""")
    if False: (OUT / '_redirects').write_text('/home-equity/ /emprestimo-com-garantia-de-imovel/ 301\n/simular/ /simulador/ 301\n')
print('ok', MODE, len(pages), 'páginas ->', OUT)
for k in META:
    t, dsc = META[k]
    if len(t) > 60 or not (120 <= len(dsc) <= 158): print('  meta fora do padrão:', k, len(t), len(dsc))
