(function () {
  // Counter keys derive from the URL path, so every page tracks itself.
  var path = location.pathname.replace(/index\.html$/, '');
  var slug = (location.host + path).replace(/\/+$/, '');
  var VIEW = 'https://hits.sh/' + slug + '/view.svg';
  var CTA  = 'https://hits.sh/' + slug + '/cta.svg';
  function ping(u) { try { new Image().src = u + '?_=' + Date.now(); } catch (e) {} }
  ping(VIEW); // pageview

  // Email capture is OFF until a Web3Forms key is set. Paste one to enable it
  // (https://web3forms.com -> confirm an email). One key works for every page.
  var ACCESS_KEY = 'REPLACE_WITH_WEB3FORMS_KEY';
  var CAPTURE_ON = ACCESS_KEY.indexOf('REPLACE') !== 0;

  var form = document.getElementById('signup');
  if (!form) return;
  var msg = document.getElementById('msg');
  var email = form.querySelector('input[type=email]');
  var button = form.querySelector('button');
  // No key yet -> clicks-only: hide the field so nothing is collected and lost.
  if (!CAPTURE_ON && email) { email.required = false; email.style.display = 'none'; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    ping(CTA); // intent click, counted in both modes
    if (!CAPTURE_ON) {
      if (button) button.disabled = true;
      msg.className = 'msg ok';
      msg.textContent = "Noted \u2014 you're early. There's no product yet; email signup is coming soon.";
      return;
    }
    msg.className = 'msg'; msg.textContent = 'Sending\u2026';
    var data = {}; new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.access_key = ACCESS_KEY;
    data.subject = document.title;
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) {
      if (r.ok) { form.reset(); msg.className = 'msg ok'; msg.textContent = "You're on the list. I'll email you when it's live."; }
      else { throw new Error('bad'); }
    }).catch(function () { msg.className = 'msg err'; msg.textContent = 'Something went wrong \u2014 try again in a moment.'; });
  });
})();
