/* Contador da Loja do Imigrante: só conta cliques, sem dados pessoais. */
(function () {
  var URL = '/contador/c.php';
  function conta(e) {
    try {
      var body = 'e=' + encodeURIComponent(e);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(URL, new Blob([body], { type: 'application/x-www-form-urlencoded' }));
      } else {
        var x = new XMLHttpRequest(); x.open('POST', URL, true);
        x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); x.send(body);
      }
    } catch (err) {}
  }
  // conta uma vez por visita (sessão do navegador)
  function contaUmaVez(e) {
    var k = 'lc_' + e;
    try { if (sessionStorage.getItem(k)) return; sessionStorage.setItem(k, '1'); } catch (err) {}
    conta(e);
  }
  // cliques em links: Stripe, WhatsApp, e links marcados com data-c
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a,[data-c]');
    if (!a) return;
    var pg = window.LC_PAGINA || 'site';
    if (a.dataset && a.dataset.c) { conta(pg + '_' + a.dataset.c); return; }
    var h = a.getAttribute('href') || '';
    if (h.indexOf('4gM8wR3RE3671J93pD0VO0a') > -1) conta(pg + '_pagar_checklist');
    else if (h.indexOf('28E6oJ73QeOPcnNbW90VO0b') > -1) conta(pg + '_pagar_consultoria');
    else if (h.indexOf('buy.stripe.com') > -1) conta(pg + '_pagar_outro');
    else if (h.indexOf('wa.me') > -1 || h.indexOf('whatsapp') > -1) conta(pg + '_whatsapp');
  }, true);
  // origem: links com ?de=nome (ex.: automações do ManyChat), sem dados pessoais
  var DE = '';
  try {
    var m = /[?&]de=([a-z0-9]{2,16})/i.exec(location.search);
    if (m) { DE = m[1].toLowerCase(); try { sessionStorage.setItem('lc_de', DE); } catch (err) {} }
    else { try { DE = sessionStorage.getItem('lc_de') || ''; } catch (err) {} }
    if (m) contaUmaVez('de_' + DE + '_abriu_' + (window.LC_PAGINA || 'site').slice(0, 10));
  } catch (err) {}
  document.addEventListener('click', function (ev) {
    if (!DE) return;
    var a = ev.target.closest && ev.target.closest('a');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('buy.stripe.com') > -1 || /\/curriculo\/[12]/.test(h)) conta('de_' + DE + '_pagamento');
    else if (h.indexOf('ig.me') > -1 || h.indexOf('wa.me') > -1) conta('de_' + DE + '_mensagem');
  }, true);
  window.LC = { conta: conta, contaUmaVez: contaUmaVez };
})();
