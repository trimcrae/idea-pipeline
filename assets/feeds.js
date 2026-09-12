(function () {
  // Pageview + CTA click counters (hits.sh, no account). Keys derive from the path.
  var path = location.pathname.replace(/index\.html$/, '');
  var slug = (location.host + path).replace(/\/+$/, '');
  function ping(k) { try { new Image().src = 'https://hits.sh/' + slug + '/' + k + '.svg?_=' + Date.now(); } catch (e) {} }
  ping('view');
  document.querySelectorAll('[data-cta]').forEach(function (el) {
    el.addEventListener('click', function () { ping(el.getAttribute('data-cta')); });
  });
})();
