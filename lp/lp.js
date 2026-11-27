/* Shield LP: qualificação -> WhatsApp. Sem armazenamento: os dados vão só na mensagem. */
(function () {
  var WA = '5512991346990';
  var PIXEL = document.documentElement.getAttribute('data-pixel') || '';
  var VAR = document.documentElement.getAttribute('data-var') || 'A';

  if (PIXEL) {
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', PIXEL);
    fbq('track', 'PageView');
  }

  var utm = new URLSearchParams(location.search);
  var origem = utm.get('utm_content') || utm.get('utm_campaign') || '';

  var form = document.getElementById('qualifica');
  var err = document.getElementById('err');
  var done = document.getElementById('done');
  var waLink = document.getElementById('walink');
  var started = false;

  form.addEventListener('input', function () {
    if (!started) { started = true; if (window.fbq) fbq('trackCustom', 'IniciouFormulario', { variante: VAR }); }
  });

  function val(name) {
    var el = form.elements[name];
    if (!el) return '';
    if (el.length && el[0] && el[0].type === 'radio') {
      for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value;
      return '';
    }
    return (el.value || '').trim();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    err.textContent = '';
    var d = {
      nome: val('nome'), cidade: val('cidade'), tipo: val('tipo'), situacao: val('situacao'),
      imovel: val('imovel'), credito: val('credito'), finalidade: val('finalidade'), docs: val('docs')
    };
    for (var k in d) if (!d[k]) { err.textContent = 'Preencha todos os campos para a gente analisar o seu caso.'; return; }
    if (!form.elements.lgpd.checked) { err.textContent = 'Marque a autorização para enviarmos a simulação.'; return; }

    var imovelIdx = form.elements.imovel.selectedIndex;   // 1 = até 500 mil ... 4 = acima de 2 mi
    var creditoIdx = form.elements.credito.selectedIndex; // 1 = até 200 mil ... 4 = acima de 1 mi
    var prioridade = (creditoIdx >= 3 || (imovelIdx >= 3 && d.situacao === 'quitado')) ? 'P1'
                   : (imovelIdx >= 2 ? 'P2' : 'P3');

    var docsTxt = d.docs === 'tudo' ? 'Tenho as fotos, o IPTU e a matrícula à mão.'
                : d.docs === 'parte' ? 'Tenho parte dos documentos (fotos, IPTU e matrícula).'
                : 'Ainda vou separar as fotos, o IPTU e a matrícula.';

    var msg = 'Olá, Shield! Quero uma simulação de crédito com garantia de imóvel.\n\n' +
      'Nome: ' + d.nome + '\n' +
      'Cidade do imóvel: ' + d.cidade + '\n' +
      'Imóvel: ' + d.tipo + ' (' + d.situacao + ')\n' +
      'Valor estimado do imóvel: ' + d.imovel + '\n' +
      'Crédito que busco: ' + d.credito + '\n' +
      'Para: ' + d.finalidade + '\n\n' +
      docsTxt + ' Vou enviar aqui as fotos do imóvel, o IPTU e a matrícula para a análise.\n\n' +
      '#' + prioridade + ' · LP ' + VAR + (origem ? ' · ' + origem : '');

    var url = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
    if (window.fbq) {
      fbq('track', 'Lead', { content_name: 'home-equity-lp-' + VAR, content_category: prioridade });
      fbq('trackCustom', 'Lead' + prioridade, { variante: VAR });
    }
    waLink.href = url;
    form.style.display = 'none';
    done.style.display = 'block';
    done.focus();
    setTimeout(function () { window.location.href = url; }, 700);
  });
})();
