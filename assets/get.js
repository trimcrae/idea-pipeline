(function () {
  var RAW = 'https://raw.githubusercontent.com/trimcrae/idea-pipeline/feeds-data';
  var q = new URLSearchParams(location.search);
  var frag = new URLSearchParams((location.hash || '').replace(/^#/, ''));
  var feed = q.get('f') || frag.get('f');
  var keyHex = q.get('k') || frag.get('k') || '';
  var el = function (id) { return document.getElementById(id); };
  var status = el('status'), list = el('weeks'), title = el('title');
  function say(t, cls) { status.className = 'msg ' + (cls || ''); status.textContent = t; }
  if (!feed || !/^[a-z0-9-]+$/.test(feed)) { say('No feed selected. Open this page from a product page or your receipt link.', 'err'); return; }
  title.textContent = 'Downloads: ' + feed;
  var hits = 'https://hits.sh/' + location.host + '/idea-pipeline/feeds/get/' + feed + '/';
  function ping(k) { try { new Image().src = hits + k + '.svg?_=' + Date.now(); } catch (e) {} }
  ping('view');
  function hexToBytes(h) { var a = new Uint8Array(h.length / 2); for (var i = 0; i < a.length; i++) a[i] = parseInt(h.substr(i * 2, 2), 16); return a; }
  function save(bytes, name) {
    var blob = new Blob([bytes], { type: 'text/csv' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
  }
  async function download(w) {
    var url = RAW + '/' + feed + '/' + w.file + '?v=' + (w.sha256 || '').slice(0, 8);
    say('Fetching ' + w.file + '\u2026');
    var r = await fetch(url, { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    var buf = new Uint8Array(await r.arrayBuffer());
    if (w.encrypted) {
      if (keyHex.length !== 64) throw new Error('This file is subscriber-only. Use the link from your Stripe receipt (it carries your access key).');
      var key = await crypto.subtle.importKey('raw', hexToBytes(keyHex), 'AES-GCM', false, ['decrypt']);
      var plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: buf.slice(0, 12) }, key, buf.slice(12));
      buf = new Uint8Array(plain);
    }
    save(buf, feed + '-' + w.week_end + '.csv');
    ping('download');
    say('Saved ' + feed + '-' + w.week_end + '.csv (' + w.rows + ' rows).', 'ok');
  }
  say('Loading the file list\u2026');
  fetch(RAW + '/' + feed + '/manifest.json?_=' + Date.now(), { cache: 'no-store' }).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function (m) {
    title.textContent = m.title || feed;
    var weeks = (m.weeks || []).slice().reverse();
    if (!weeks.length) { say('No files published yet \u2014 the first weekly build has not run. Check back Monday.', 'err'); return; }
    if (m.encrypted && keyHex.length !== 64) {
      say('These files are subscriber-only. Subscribe on the product page; Stripe then sends you here with your access key. Bookmark that link.', 'err');
    } else {
      say(m.encrypted ? 'Bookmark this page \u2014 the link carries your access key. A new file lands every Monday.' : 'Free beta: full files, no key needed. A new file lands every Monday.', 'ok');
    }
    weeks.forEach(function (w, i) {
      var li = document.createElement('li');
      var b = document.createElement('button'); b.type = 'button';
      b.textContent = (i === 0 ? 'Download latest \u2014 ' : 'Download \u2014 ') + w.week_start + ' to ' + w.week_end + ' (' + w.rows + ' rows)';
      if (m.encrypted && keyHex.length !== 64) b.disabled = true;
      b.addEventListener('click', function () { download(w).catch(function (e) { say(String(e.message || e), 'err'); }); });
      li.appendChild(b); list.appendChild(li);
    });
    var cols = document.createElement('p'); cols.className = 'cols';
    cols.textContent = 'Columns: ' + (m.columns || []).join(', ');
    list.parentNode.appendChild(cols);
  }).catch(function (e) { say('Could not load the file list (' + (e.message || e) + '). If this feed was just added, the first build has not run yet.', 'err'); });
})();
