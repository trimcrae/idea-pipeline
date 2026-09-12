#!/usr/bin/env python3
"""Generate the static site (GitHub Pages, served from `main`).

  /                     hub: the feed catalogue (indexable)
  /feeds/<id>/          product page: masked sample, this week's stats, price, subscribe
  /feeds/<id>/weeks/    weekly digest pages (aggregate stats only — SEO freshness)
  /feeds/get/           subscriber download page (decrypts in the browser)
  /experiments/         the older "would you use this?" idea probes (noindex)
  /<probe handle>/      those probe pages (unchanged)
  sitemap.xml, robots.txt, /<indexnow key>.txt

Inputs: engine/feeds/registry.py, feeds/<id>/{stats,history}.json + sample.csv
(written by engine/feeds/build.py), config/payments.json (written by
engine/feeds/stripe_links.py). Run from anywhere:  python engine/build_pages.py
"""
import csv
import datetime as dt
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine", "feeds"))
import registry  # noqa: E402

SITE = "https://trimcrae.github.io/idea-pipeline"
SITE_NAME = "Fresh Filings"
HITS_BASE = "https://hits.sh/trimcrae.github.io/idea-pipeline"
DATA_RAW = "https://raw.githubusercontent.com/trimcrae/idea-pipeline/feeds-data"

# --------------------------------------------------------------------- assets

CSS = """:root { --ink:#11161c; --muted:#5a6470; --line:#e4e8ee; --accent:#1463ff; --bg:#fbfcfe; --soft:#f1f5ff; }
* { box-sizing:border-box; }
body { margin:0; font:17px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--ink); background:var(--bg); -webkit-font-smoothing:antialiased; }
.wrap { max-width:560px; margin:0 auto; padding:40px 22px 64px; }
.wide { max-width:760px; }
.kicker { font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); font-weight:700; margin:0 0 14px; }
h1 { font-size:30px; line-height:1.18; margin:0 0 16px; letter-spacing:-.01em; }
h2 { font-size:20px; margin:34px 0 10px; }
.sub { font-size:18px; color:var(--muted); margin:0 0 28px; }
.one { background:#fff; border:1px solid var(--line); border-radius:14px; padding:18px 20px; margin:0 0 28px; font-weight:500; }
.one b { color:var(--accent); }
form { display:flex; flex-direction:column; gap:12px; margin:0 0 14px; }
input[type=email] { width:100%; padding:15px 16px; font-size:17px; border:1px solid var(--line); border-radius:11px; background:#fff; }
input[type=email]:focus { outline:none; border-color:var(--accent); box-shadow:0 0 0 3px rgba(20,99,255,.12); }
button, .btn { display:block; width:100%; padding:16px; font-size:17px; font-weight:700; color:#fff; background:var(--accent); border:0; border-radius:11px; cursor:pointer; text-align:center; text-decoration:none; }
button:active, .btn:active { transform:translateY(1px); }
button:disabled { opacity:.6; }
.btn.secondary { background:#fff; color:var(--accent); border:1px solid var(--accent); }
.msg { font-size:15px; margin:6px 0 0; min-height:20px; }
.ok { color:#0a7d33; } .err { color:#c0392b; }
ul.checks { list-style:none; padding:0; margin:8px 0 28px; }
ul.checks li { padding:7px 0 7px 26px; position:relative; color:var(--ink); }
ul.checks li::before { content:"\\2713"; position:absolute; left:0; color:var(--accent); font-weight:700; }
.foot { font-size:14px; color:var(--muted); border-top:1px solid var(--line); padding-top:18px; margin-top:8px; }
.foot a, a { color:var(--accent); text-decoration:none; }
.hub { list-style:none; padding:0; margin:6px 0 28px; display:flex; flex-direction:column; gap:12px; }
.hub a { display:block; background:#fff; border:1px solid var(--line); border-radius:12px; padding:16px 18px; text-decoration:none; color:var(--ink); }
.hub a:active { transform:translateY(1px); }
.hub b { display:block; font-size:17px; margin-bottom:3px; }
.hub span { color:var(--muted); font-size:15px; }
.hub .meta { display:block; margin-top:6px; font-size:13px; color:var(--accent); font-weight:600; }
nav.top { font-size:14px; margin:0 0 22px; color:var(--muted); }
nav.top a { font-weight:700; }
.facts { display:grid; grid-template-columns:1fr; gap:12px; margin:0 0 24px; }
.fact { background:#fff; border:1px solid var(--line); border-radius:12px; padding:14px 16px; font-size:15px; }
.fact b { display:block; font-size:13px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin-bottom:4px; }
.stat { display:flex; gap:18px; flex-wrap:wrap; background:var(--soft); border-radius:12px; padding:14px 16px; margin:0 0 24px; }
.stat div { min-width:120px; } .stat .n { font-size:26px; font-weight:800; line-height:1.1; } .stat .l { font-size:13px; color:var(--muted); }
.tbl { overflow-x:auto; border:1px solid var(--line); border-radius:12px; background:#fff; margin:0 0 10px; }
table { border-collapse:collapse; font-size:13px; min-width:100%; }
th, td { padding:8px 10px; border-bottom:1px solid var(--line); text-align:left; white-space:nowrap; max-width:260px; overflow:hidden; text-overflow:ellipsis; }
th { background:#f6f8fb; font-weight:700; position:sticky; top:0; }
.small { font-size:14px; color:var(--muted); }
.price { background:#fff; border:2px solid var(--accent); border-radius:14px; padding:20px; margin:8px 0 28px; }
.price .amt { font-size:34px; font-weight:800; } .price .per { color:var(--muted); font-size:15px; }
.price ul { margin:10px 0 16px; padding-left:20px; font-size:15px; }
.groups { list-style:none; padding:0; margin:0 0 24px; font-size:15px; }
.groups li { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px dashed var(--line); }
details { margin:0 0 10px; } summary { cursor:pointer; font-weight:600; }
.cols { font-size:13px; color:var(--muted); word-break:break-word; }
code { background:#eef1f6; padding:2px 5px; border-radius:5px; font-size:.92em; }
.pill { display:inline-block; font-size:12px; font-weight:700; padding:3px 8px; border-radius:99px; background:var(--soft); color:var(--accent); margin-left:6px; vertical-align:middle; }
"""

PROBE_JS = """(function () {
  // Counter keys derive from the URL path, so every page tracks itself.
  var path = location.pathname.replace(/index\\.html$/, '');
  var slug = (location.host + path).replace(/\\/+$/, '');
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
      msg.textContent = "Noted \\u2014 you're early. There's no product yet; email signup is coming soon.";
      return;
    }
    msg.className = 'msg'; msg.textContent = 'Sending\\u2026';
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
    }).catch(function () { msg.className = 'msg err'; msg.textContent = 'Something went wrong \\u2014 try again in a moment.'; });
  });
})();
"""

FEEDS_JS = """(function () {
  // Pageview + CTA click counters (hits.sh, no account). Keys derive from the path.
  var path = location.pathname.replace(/index\\.html$/, '');
  var slug = (location.host + path).replace(/\\/+$/, '');
  function ping(k) { try { new Image().src = 'https://hits.sh/' + slug + '/' + k + '.svg?_=' + Date.now(); } catch (e) {} }
  ping('view');
  document.querySelectorAll('[data-cta]').forEach(function (el) {
    el.addEventListener('click', function () { ping(el.getAttribute('data-cta')); });
  });
})();
"""

GET_JS = """(function () {
  var RAW = '%(raw)s';
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
    say('Fetching ' + w.file + '\\u2026');
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
  say('Loading the file list\\u2026');
  fetch(RAW + '/' + feed + '/manifest.json?_=' + Date.now(), { cache: 'no-store' }).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function (m) {
    title.textContent = m.title || feed;
    var weeks = (m.weeks || []).slice().reverse();
    if (!weeks.length) { say('No files published yet \\u2014 the first weekly build has not run. Check back Monday.', 'err'); return; }
    if (m.encrypted && keyHex.length !== 64) {
      say('These files are subscriber-only. Subscribe on the product page; Stripe then sends you here with your access key. Bookmark that link.', 'err');
    } else {
      say(m.encrypted ? 'Bookmark this page \\u2014 the link carries your access key. A new file lands every Monday.' : 'Free beta: full files, no key needed. A new file lands every Monday.', 'ok');
    }
    weeks.forEach(function (w, i) {
      var li = document.createElement('li');
      var b = document.createElement('button'); b.type = 'button';
      b.textContent = (i === 0 ? 'Download latest \\u2014 ' : 'Download \\u2014 ') + w.week_start + ' to ' + w.week_end + ' (' + w.rows + ' rows)';
      if (m.encrypted && keyHex.length !== 64) b.disabled = true;
      b.addEventListener('click', function () { download(w).catch(function (e) { say(String(e.message || e), 'err'); }); });
      li.appendChild(b); list.appendChild(li);
    });
    var cols = document.createElement('p'); cols.className = 'cols';
    cols.textContent = 'Columns: ' + (m.columns || []).join(', ');
    list.parentNode.appendChild(cols);
  }).catch(function (e) { say('Could not load the file list (' + (e.message || e) + '). If this feed was just added, the first build has not run yet.', 'err'); });
})();
"""

# --------------------------------------------------------- probe pages (old)
# The 2026-06 "would you use this?" idea probes. Unchanged, still served at /<handle>/.
PROBES = [
  ("freight-fraud-check", {"kicker": "For small dispatch shops & owner-operators", "title": "Check a carrier for fraud before you book the load", "desc": "Paste an MC number or a broker email and get an instant fraud-risk flag — authority age, lapsed insurance, lookalike-domain clones, phone clustering. For small dispatch shops and one-truck operators.", "h1": "Check a carrier for fraud before you book the load.", "sub": "Paste an MC number or a broker email. Get an instant risk flag — not enterprise software, not a phone-tree of calls.", "one": "The 30-second check you do today by hand across SAFER, a phone call, and a gut feeling — in <b>one click</b>.", "checks": ["Authority age &amp; recent reactivations", "Lapsed or missing insurance", "Lookalike-domain clones of real carriers", "One phone number across many authorities"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Surfaces public risk <em>signals</em> from FMCSA data; you decide. Not a verdict that a carrier is fraudulent.", "hub": "Check a carrier for fraud before you book the load."}),
  ("card-grading-gate", {"kicker": "For collectors weighing a grading submission", "title": "Is grading this card worth the fees and the wait?", "desc": "Describe a card and its raw condition and get an expected graded value minus fees and turnaround — a clear go/no-go before you submit. Built on public sold comps.", "h1": "Is grading this card worth the fees and the wait?", "sub": "Describe the card and its condition. Get an expected graded value minus fees and turnaround — a clear go/no-go before you mail it off.", "one": "The “should I even submit this?” math you guess at today — comps, fees, months of wait — in <b>one answer</b>.", "checks": ["Expected grade range from recent sold comps", "Grading fee + turnaround netted out", "Break-even vs. selling it raw", "Public eBay sold data, not a paid database"], "cta": "Notify me when it's live", "foot": "Early — no product yet. An informational estimate from public sold comps, not an appraisal or financial advice — you decide whether to submit.", "hub": "Is grading this card worth the fees and the wait?"}),
  ("travel-nurse-license-navigator", {"kicker": "For travel nurses working across states", "title": "Which states can you work in — and what does each license require?", "desc": "Pick your license and target states. See NLC compact coverage, what each non-compact state requires, fees, timelines, and renewal dates — without digging through every board site.", "h1": "Which states can you work in — and what does each license require?", "sub": "Pick your license and your target states. See compact coverage, what each non-compact state requires, and the steps — in one place.", "one": "The compact-vs-single-state license maze, mapped for your states, in <b>one place</b>.", "checks": ["NLC compact coverage for your home state", "Per-state requirements for non-compact states", "Fees, timelines, and renewal dates", "Published board rules + links to verify"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Presents published board requirements + source links; it never certifies you're licensed — you verify with the board.", "hub": "Which states can you work in, and what does each license require?"}),
  ("houseplant-restock-alerts", {"kicker": "For rare-plant collectors who keep missing drops", "title": "Get an alert the moment that rare plant is back in stock", "desc": "Pick a cultivar and the shops you watch. We check their pages and email you the moment it restocks — before it sells out again. Free public shop pages, no insider access.", "h1": "Get an alert the moment that rare plant is back in stock.", "sub": "Pick a cultivar and the shops you watch. We check their pages and email you when it restocks — before it sells out again.", "one": "The five tabs you refresh all day, watched for you — a ping instead of FOMO, in <b>one alert</b>.", "checks": ["Watch one cultivar across multiple shops", "Restock and price-drop detection", "Email the moment it goes live", "Free public shop pages, no insider access"], "cta": "Notify me when it's live", "foot": "Early — no product yet. A retail restock alert, no advice of any kind. Shop pages change, so coverage is best-effort.", "hub": "Get an alert the moment a rare plant restocks."}),
  ("trade-license-renewal-navigator", {"kicker": "For licensed trades — pest control first", "title": "Never miss a license renewal or CE deadline again", "desc": "Pick your trade and state. Get your renewal date, the CE hours you need, and the rules that apply — kept current, with a reminder before it's due. Built on public .gov pages.", "h1": "Never miss a license renewal or CE deadline again.", "sub": "Pick your trade and state. Get your renewal date, the CE hours you need, and the rules that apply — with a reminder before it's due.", "one": "The renewal date and CE rules buried in a state .gov PDF, pulled out and tracked for you, in <b>one place</b>.", "checks": ["Renewal deadline + CE hours for your state", "The specific rules that apply (e.g. legal pesticide uses)", "A reminder before the deadline", "Published .gov rules + links to verify"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Aggregates published deadlines/CE hours + source links; it never certifies you're compliant — you verify.", "hub": "Never miss a trade license renewal or CE deadline."}),
  ("cottage-food-permit-navigator", {"kicker": "For home &amp; mobile food sellers", "title": "Before you sell a single jar, know what your state lets you do", "desc": "Pick your state and product. See what cottage-food / mobile-vendor law allows, the permit and inspection steps, and the limits — in plain language over the health-dept rulebook.", "h1": "Before you sell a single jar, know what your state lets you do.", "sub": "Pick your state and product. See what cottage-food / mobile-vendor law allows, the permit and inspection steps, and the limits — in plain language.", "one": "The health-department rulebook for your state and product, in plain English, in <b>one answer</b>.", "checks": ["What you can legally sell under cottage-food law", "Permit + inspection steps", "Revenue caps and labeling rules", "Published statute + link to your health dept"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Summarizes what the published statute says + links it; it never clears you to sell — confirm with your health dept.", "hub": "What your state lets you sell, before you make the first jar."}),
  ("watch-authenticity-check", {"kicker": "For used-watch buyers about to wire real money", "title": "Before you wire $3k, does this watch add up?", "desc": "Enter brand, reference, and serial (and photos). Get a consistency check against known reference data and common fake/franken tells — a sanity gate before you pay, not an appraisal.", "h1": "Before you wire $3k, does this watch add up?", "sub": "Enter the brand, reference, and serial (and photos). Get a consistency check against known reference data and common fake/franken tells — a sanity gate, not an appraisal.", "one": "The 60-second “is this listing legit?” gut-check you wish you had before paying, in <b>one check</b>.", "checks": ["Reference + serial internal consistency", "Known fake / franken-watch tells", "Photo-set sanity flags", "Community reference data, one brand first"], "cta": "Notify me when it's live", "foot": "Early — no product yet. A consistency / known-fake-tells signal, explicitly not an appraisal or authentication guarantee — you decide.", "hub": "Before you wire $3k, does this used watch add up?"}),
  ("visa-bulletin-tracker", {"kicker": "For immigration practitioners", "title": "Know the moment a priority date goes current", "desc": "Track your caseload against the monthly visa bulletin and USCIS processing times. Get alerted when a date becomes current or a filing window opens — without checking by hand.", "h1": "Know the moment a priority date goes current.", "sub": "Track your caseload against the monthly visa bulletin and USCIS processing times. Get alerted when a date becomes current or a window opens.", "one": "The visa bulletin you re-check every month, watching your cases for you, in <b>one alert</b>.", "checks": ["Your cases vs. the monthly visa bulletin", "Priority-date-current alerts", "USCIS processing-time changes", "Public State Dept + USCIS data"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Monitoring/alerting over public data (“your date is current”), not legal advice — you make the legal call.", "hub": "Know the moment a priority date goes current."}),
  ("estate-lowball-gate", {"kicker": "For executors &amp; heirs selling a collection", "title": "Don't let an estate buyer lowball the collection", "desc": "Enter or photograph a collection and get an independent value range from recent sold comps before you accept an offer — so you know if it's fair. Independent of any buyer or auctioneer.", "h1": "Don't let an estate buyer lowball the collection.", "sub": "Enter or photograph the collection. Get an independent value range from recent sold comps before you accept an offer — so you know if it's fair.", "one": "The independent second opinion the estate-sale company won't give you, from real sold comps, in <b>one range</b>.", "checks": ["Value range from recent sold listings", "The comps behind the number, shown", "One category at a time, cleanest data first", "Independent of any buyer or auctioneer"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Shows sold comps and a range from them, not a formal appraisal or financial advice — you decide whether to take the offer.", "hub": "Don't let an estate buyer lowball the collection."}),
  ("fleet-compliance-tracker", {"kicker": "For 1–5 truck owner-operators", "title": "Every DOT deadline a small fleet can't afford to miss — on one calendar", "desc": "Enter your DOT/MC number and drivers. Get the recurring federal and state deadlines a small operation must hit — MCS-150, UCR, IFTA, medical cards — with a reminder before each.", "h1": "Every DOT deadline a small fleet can't afford to miss — on one calendar.", "sub": "Enter your DOT/MC number and drivers. Get the recurring federal and state deadlines a small operation must hit, with a reminder before each.", "one": "What a big fleet's TMS tracks automatically — MCS-150, UCR, IFTA, medical cards — for the one-truck operator, in <b>one calendar</b>.", "checks": ["MCS-150 biennial + UCR annual", "IFTA quarterly + IRP", "CDL medical-card + drug-&amp;-alcohol dates", "Public FMCSA / IFTA / state data"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Surfaces the published deadline + the .gov link; it never certifies you're compliant — you verify.", "hub": "Every DOT deadline a small fleet can't miss, on one calendar."}),
  ("str-rule-navigator", {"kicker": "For short-term-rental hosts", "title": "Do you need a permit to list here — and what are the deadlines?", "desc": "Pick your city or county. See what the local short-term-rental law requires before and while you list — permit, lodging tax, caps, zoning — plus the renewal and tax deadlines.", "h1": "Do you need a permit to list here — and what are the deadlines?", "sub": "Pick your city or county. See what the local STR law requires before and while you list — permit, lodging tax, caps, zoning — plus the deadlines.", "one": "The city ordinance and tax rules for your listing, in plain language, in <b>one answer</b>.", "checks": ["Permit / registration requirement", "Lodging-tax registration + filing cadence", "Primary-residence or night caps, zoning", "Published ordinance + link to verify"], "cta": "Notify me when it's live", "foot": "Early — no product yet. Summarizes the published ordinance + links the source; it never says you're legal to operate — you verify with the city.", "hub": "Do you need a permit to list your short-term rental here?"}),
]

PROBE_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<div class="wrap">
  <p class="kicker">{kicker}</p>
  <h1>{h1}</h1>
  <p class="sub">{sub}</p>

  <div class="one">{one}</div>

  <ul class="checks">
{checks}
  </ul>

  <form id="signup">
    <input type="email" name="email" placeholder="you@example.com" required autocomplete="email">
    <button type="submit">{cta}</button>
    <p class="msg" id="msg" aria-live="polite"></p>
  </form>

  <p class="foot">{foot}</p>
  <p class="foot"><a href="../experiments/">&larr; All the checks I'm testing</a> &middot; <a href="../">Weekly public-records feeds</a></p>
</div>

<noscript><img src="{hits}/{handle}/view.svg" alt="" width="1" height="1" style="position:absolute;left:-9999px;top:-9999px"></noscript>
<script src="../assets/probe.js"></script>
</body>
</html>
"""

EXPERIMENTS_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Early experiments — which of these is worth building?</title>
<meta name="description" content="A handful of dead-simple tools I'm thinking about building. None exists yet. Tap any that hits a nerve.">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<div class="wrap">
  <p class="kicker">Early — nothing here is built yet</p>
  <h1>Which of these is worth building?</h1>
  <p class="sub">A handful of dead-simple checks and trackers I'm weighing. Each one solves a specific, annoying problem. Tap any that hits a nerve — that's the only signal I'm after.</p>
  <ul class="hub">
{items}
  </ul>
  <p class="foot">No product, no pitch, no spam. Just testing which problems are real. The live products are the <a href="../">weekly public-records feeds</a>.</p>
</div>
<noscript><img src="{hits}/experiments/view.svg" alt="" width="1" height="1" style="position:absolute;left:-9999px;top:-9999px"></noscript>
<script src="../assets/probe.js"></script>
</body>
</html>
"""

# ------------------------------------------------------------ feed templates

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{extra_head}<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<div class="wrap {wide}">
<nav class="top"><a href="{rel}">{site}</a> &middot; weekly public-records feeds</nav>
"""

TAIL = """
<p class="foot">Compiled from public government open-data portals and republished as-is, with no warranty of accuracy, completeness or timeliness. A public record is information, not a determination about anyone. You are responsible for how you use it — including telemarketing, do-not-call, anti-spam and privacy laws where you and your contacts are. Not affiliated with any government agency. Cancel any subscription at any time. <a href="{rel}">All feeds</a> &middot; <a href="{rel}experiments/">Experiments</a></p>
</div>
<noscript><img src="{hits_view}" alt="" width="1" height="1" style="position:absolute;left:-9999px;top:-9999px"></noscript>
<script src="{rel}assets/feeds.js"></script>
</body>
</html>
"""

GET_TMPL = HEAD + """
  <p class="kicker">Subscriber downloads</p>
  <h1 id="title">Downloads</h1>
  <p class="msg" id="status" aria-live="polite"></p>
  <ul class="hub" id="weeks"></ul>
  <p class="small">Files are CSV (UTF-8) and open in Excel, Google Sheets or any CRM import. Subscriber files are decrypted in your browser with the key in your link; nothing is sent anywhere. Problems? Reply to your Stripe receipt.</p>
  {portal}
""" + TAIL.replace('<script src="{rel}assets/feeds.js"></script>', '<script src="{rel}assets/get.js"></script>')


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def fmt_date(s):
    try:
        return dt.date.fromisoformat(s).strftime("%b %-d, %Y")
    except (TypeError, ValueError):
        return s or ""


def week_label(st):
    a, b = st.get("week_start", ""), st.get("week_end", "")
    try:
        da, db = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
        if da.month == db.month:
            return f"{da.strftime('%b %-d')}–{db.strftime('%-d, %Y')}"
        return f"{da.strftime('%b %-d')} – {db.strftime('%b %-d, %Y')}"
    except ValueError:
        return f"{a} – {b}"


def read_json(path, default):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def read_sample(path, limit=10):
    try:
        with open(path, newline="") as fh:
            rows = list(csv.DictReader(fh))
    except OSError:
        return [], []
    header = list(rows[0].keys()) if rows else []
    return header, rows[:limit]


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)


def sample_table(header, rows, max_cols=9):
    if not rows:
        return '<p class="small">Sample rows appear here after the first weekly build.</p>'
    cols = header[:max_cols]
    th = "".join(f"<th>{esc(c)}</th>" for c in cols)
    trs = "".join("<tr>" + "".join(f"<td>{esc(r.get(c, ''))}</td>" for c in cols) + "</tr>" for r in rows)
    more = f' <span class="small">(+{len(header) - len(cols)} more columns in the file)</span>' if len(header) > len(cols) else ""
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div><p class="small">Contact columns are masked in the sample; the paid file is complete.{more}</p>'


def groups_list(stats):
    groups = stats.get("groups") or []
    if not groups:
        return ""
    label = (stats.get("group_by") or "group").replace("_", " ")
    items = "".join(f"<li><span>{esc(k)}</span><b>{n:,}</b></li>" for k, n in groups[:8])
    return f"<h2>This week by {esc(label)}</h2><ul class=\"groups\">{items}</ul>"


def product_page(feed, payments):
    fid = feed["id"]
    d = os.path.join(ROOT, "feeds", fid)
    stats = read_json(os.path.join(d, "stats.json"), {})
    history = read_json(os.path.join(d, "history.json"), [])
    header, rows = read_sample(os.path.join(d, "sample.csv"))
    pay = (payments.get("feeds") or {}).get(fid) or {}
    link = pay.get("payment_link")
    price = feed["price"]
    rel = "../../"
    canonical = f"{SITE}/feeds/{fid}/"
    n = stats.get("rows")
    wk = week_label(stats) if stats else "first build pending"

    if link:
        cta = (f'<a class="btn" href="{esc(link)}" data-cta="subscribe">Subscribe — ${price}/month</a>'
               f'<p class="small">Secure checkout by Stripe. After payment you land on your download page — bookmark it; a new file is there every Monday.</p>')
        beta = ""
    else:
        cta = (f'<a class="btn" href="{rel}feeds/get/?f={fid}" data-cta="download">Download this week\'s full CSV — free during beta</a>'
               f'<p class="small">Paid subscriptions (${price}/month) open soon; until then the full file is free. No sign-up.</p>')
        beta = '<span class="pill">free beta</span>'

    facts = (f'<div class="facts"><div class="fact"><b>Who buys this</b>{esc(feed["buyers"])}</div>'
             f'<div class="fact"><b>Why it works</b>{esc(feed.get("why", ""))}</div></div>')
    statbox = ""
    if stats:
        statbox = (f'<div class="stat"><div><div class="n">{n:,}</div><div class="l">rows, {esc(wk)}</div></div>'
                   f'<div><div class="n">{len(header) or len(stats.get("columns", []))}</div><div class="l">columns</div></div>'
                   f'<div><div class="n">Mon</div><div class="l">new file every week</div></div></div>')
    faq = "".join(f"<details><summary>{esc(q)}</summary><p class=\"small\">{esc(a)}</p></details>" for q, a in feed.get("faq", []))
    faq += ("<details><summary>How is the file delivered?</summary><p class=\"small\">A download page, refreshed every Monday morning (UTC) with the previous 7 days. The last 8 weeks stay available. CSV, UTF-8, one header row.</p></details>"
            "<details><summary>Can I cancel?</summary><p class=\"small\">Any time, from the link in your Stripe receipt. No minimum term.</p></details>"
            "<details><summary>Where does the data come from?</summary><p class=\"small\">" + esc(feed["attribution"]) + f". It is pulled from the agency's public open-data portal every week, filtered to the rows that are new, and normalised into one flat table. Source: <a href=\"{esc(feed['source_url'])}\" rel=\"nofollow\">{esc(feed['source_url'])}</a></p></details>")
    weeks_links = ""
    if history:
        items = "".join(f'<li><a href="weeks/{esc(h["week_end"])}.html"><b>{esc(week_label(h))}</b><span>{h["rows"]:,} rows</span></a></li>' for h in reversed(history[-6:]))
        weeks_links = f'<h2>Past weeks</h2><ul class="hub">{items}</ul><p class="small"><a href="weeks/">All weeks</a></p>'
    columns = ", ".join(header or stats.get("columns", []))
    jsonld = {
        "@context": "https://schema.org", "@type": "Product", "name": feed["title"],
        "description": feed["short"], "url": canonical, "brand": {"@type": "Brand", "name": SITE_NAME},
        "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "USD", "url": link or canonical,
                   "availability": "https://schema.org/InStock", "category": "subscription"},
    }
    extra_head = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>\n'
    terms = feed.get("search_terms") or []
    page_title = (terms[0][:1].upper() + terms[0][1:] + " — " + feed["title"]) if terms else feed["title"] + " — weekly CSV"
    desc = feed["short"] + (" Also: " + ", ".join(terms[1:4]) + "." if len(terms) > 1 else "")
    body = HEAD.format(title=esc(page_title[:120]), desc=esc(desc[:300]), canonical=canonical,
                       extra_head=extra_head, rel=rel, wide="wide", site=SITE_NAME)
    body += f"""
  <p class="kicker">Weekly feed &middot; {esc(registry_category_label(feed))}{beta}</p>
  <h1>{esc(feed["title"])}</h1>
  <p class="sub">{esc(feed["short"])}</p>
  {('<p class="small">Searched for as: ' + esc(", ".join(terms)) + '.</p>') if terms else ''}
  {statbox}
  {facts}
  <h2>Sample from the latest file</h2>
  {sample_table(header, rows)}
  <p><a class="btn secondary" href="sample.csv" data-cta="sample" download>Download the free sample (25 rows)</a></p>
  <div class="price"><span class="amt">${price}</span> <span class="per">per month &middot; cancel anytime</span>
    <ul><li>New CSV every Monday with the previous 7 days ({n:,} rows this week)</li><li>Every column, unmasked; last 8 weeks kept</li><li>Straight from the public record — no scraping, no guessing</li></ul>
    {cta}
  </div>
  {groups_list(stats)}
  <h2>What's in the file</h2>
  <p class="cols">{esc(columns)}</p>
  <p class="small">{esc(feed.get("disclaimer", "Rows are public records as published by the agency; a record is not a finding about anyone."))}</p>
  <h2>Questions</h2>
  {faq}
  {weeks_links}
""" if stats else body + f"""
  <p class="kicker">Weekly feed &middot; {esc(registry_category_label(feed))}</p>
  <h1>{esc(feed["title"])}</h1>
  <p class="sub">{esc(feed["short"])}</p>
  {facts}
  <p class="small">The first weekly build has not run yet — sample rows and counts appear here after it does.</p>
  <div class="price"><span class="amt">${price}</span> <span class="per">per month &middot; cancel anytime</span>{cta}</div>
  <h2>Questions</h2>
  {faq}
"""
    body += TAIL.format(rel=rel, hits_view=f"{HITS_BASE}/feeds/{fid}/view.svg")
    return body


def registry_category_label(feed):
    for key, label, _ in registry.CATEGORIES:
        if key == feed.get("category"):
            return label
    return "Public records"


def digest_page(feed, h):
    fid = feed["id"]
    rel = "../../../"
    canonical = f"{SITE}/feeds/{fid}/weeks/{h['week_end']}.html"
    label = (feed.get("group_by") or "group").replace("_", " ")
    groups = "".join(f"<li><span>{esc(k)}</span><b>{n:,}</b></li>" for k, n in (h.get("groups") or [])[:8])
    title = f"{week_label(h)}: {h['rows']:,} rows — {feed['title']}"
    body = HEAD.format(title=esc(title), desc=esc(f"Weekly digest for {feed['title'].lower()}: {h['rows']:,} new records between {h['week_start']} and {h['week_end']}."),
                       canonical=canonical, extra_head="", rel=rel, wide="", site=SITE_NAME)
    body += f"""
  <p class="kicker">Weekly digest &middot; {esc(week_label(h))}</p>
  <h1>{h['rows']:,} new records — {esc(feed['title'].lower())}</h1>
  <p class="sub">Between {esc(fmt_date(h['week_start']))} and {esc(fmt_date(h['week_end']))}, {h['rows']:,} rows entered the public record covered by this feed ({esc(feed['attribution'])}).</p>
  {f'<h2>By {esc(label)}</h2><ul class="groups">{groups}</ul>' if groups else ''}
  <p><a class="btn" href="../" data-cta="product">Get this week's file — ${feed['price']}/month</a></p>
  <p class="small"><a href="./">All weeks</a> &middot; <a href="../">About this feed</a></p>
"""
    body += TAIL.format(rel=rel, hits_view=f"{HITS_BASE}/feeds/{fid}/weeks/view.svg")
    return body


def weeks_index(feed, history):
    fid = feed["id"]
    rel = "../../../"
    items = "".join(f'<li><a href="{esc(h["week_end"])}.html"><b>{esc(week_label(h))}</b><span>{h["rows"]:,} rows</span></a></li>' for h in reversed(history))
    body = HEAD.format(title=esc(f"Weekly archive — {feed['title']}"), desc=esc(f"Every weekly digest for {feed['title'].lower()}."),
                       canonical=f"{SITE}/feeds/{fid}/weeks/", extra_head="", rel=rel, wide="", site=SITE_NAME)
    body += f"""
  <p class="kicker">Weekly archive</p>
  <h1>{esc(feed['title'])}</h1>
  <p class="sub">One digest per week, aggregate counts only. The full rows are in the <a href="../">weekly CSV</a>.</p>
  <ul class="hub">{items or '<li class="small">No weeks yet.</li>'}</ul>
"""
    body += TAIL.format(rel=rel, hits_view=f"{HITS_BASE}/feeds/{fid}/weeks/index/view.svg")
    return body


def hub_page(payments):
    rel = ""
    sections = ""
    for key, label, blurb in registry.CATEGORIES:
        feeds = [f for f in registry.FEEDS if f.get("category") == key]
        if not feeds:
            continue
        items = ""
        for f in feeds:
            st = read_json(os.path.join(ROOT, "feeds", f["id"], "stats.json"), {})
            meta = f"{st['rows']:,} rows this week" if st else "first build pending"
            paid = (payments.get("feeds") or {}).get(f["id"], {}).get("payment_link")
            meta += f" &middot; ${f['price']}/mo" + ("" if paid else " &middot; free beta")
            items += f'<li><a href="feeds/{f["id"]}/"><b>{esc(f["title"])}</b><span>{esc(f["short"])}</span><span class="meta">{meta}</span></a></li>'
        sections += f'<h2>{esc(label)}</h2><p class="small">{esc(blurb)}</p><ul class="hub">{items}</ul>'
    build = read_json(os.path.join(ROOT, "feeds", "build.json"), {})
    built = fmt_date((build.get("built_at") or "")[:10]) if build else ""
    body = HEAD.format(title=esc(f"{SITE_NAME} — weekly feeds of new public filings, for sales teams"),
                       desc=esc("Weekly CSV feeds of businesses that just entered the public record — new trucking registrations, liquor-license applications, restaurant inspections, business formations — straight from government open-data portals, for the vendors who serve them."),
                       canonical=f"{SITE}/", extra_head="", rel=rel, wide="wide", site=SITE_NAME)
    body += f"""
  <p class="kicker">Weekly public-records feeds</p>
  <h1>Businesses that just entered the public record — every Monday, as a CSV.</h1>
  <p class="sub">Government portals publish new registrations, licenses, permits and inspections within a day. Each feed below pulls the past week's new rows from one of them, cleans them into a flat table, and delivers it weekly. A free 25-row sample is on every page.{' Last build: ' + esc(built) + '.' if built else ''}</p>
  {sections}
  <h2>How it's made</h2>
  <p class="small">Every feed reads a public open-data portal (NYC, Chicago, New York State, Texas, Colorado, Connecticut, New Orleans, US DOT) through its official API, keeps the rows dated in the trailing 7 days, and publishes them as-is. No scraping, no enrichment from private sources, no personal contact details beyond what the business itself filed with the agency. Feeds describe businesses and licensed premises, not private individuals.</p>
"""
    body += TAIL.format(rel=rel, hits_view=f"{HITS_BASE}/view.svg")
    return body


def get_page(payments):
    portal = payments.get("portal_url") or ""
    portal_html = f'<p class="small">Manage or cancel your subscription: <a href="{esc(portal)}">customer portal</a>.</p>' if portal else ""
    body = GET_TMPL.format(title="Your downloads — " + SITE_NAME, desc="Subscriber download page for weekly public-records feeds.",
                           canonical=f"{SITE}/feeds/get/", extra_head='<meta name="robots" content="noindex">\n', rel="../../",
                           wide="", site=SITE_NAME, portal=portal_html, hits_view=f"{HITS_BASE}/feeds/get/view.svg")
    return body


def sitemap(urls):
    today = dt.date.today().isoformat()
    items = "".join(f"<url><loc>{esc(u)}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>\n'


def main():
    payments = read_json(os.path.join(ROOT, "config", "payments.json"), {"portal_url": "", "feeds": {}})
    write("assets/style.css", CSS)
    write("assets/probe.js", PROBE_JS)
    write("assets/feeds.js", FEEDS_JS)
    write("assets/get.js", GET_JS % {"raw": DATA_RAW})

    urls = [f"{SITE}/"]
    # old idea probes (unchanged URLs) + their index moved to /experiments/
    for handle, c in PROBES:
        checks = "\n".join("    <li>%s</li>" % x for x in c["checks"])
        write(f"{handle}/index.html", PROBE_TMPL.format(hits=HITS_BASE, handle=handle, checks=checks, **{k: v for k, v in c.items() if k != "checks"}))
        urls.append(f"{SITE}/{handle}/")
    items = "\n".join(f'    <li><a href="../{h}/"><b>{c["title"]}</b><span>{c["hub"]}</span></a></li>' for h, c in PROBES)
    write("experiments/index.html", EXPERIMENTS_TMPL.format(items=items, hits=HITS_BASE))

    # feeds
    for feed in registry.FEEDS:
        fid = feed["id"]
        write(f"feeds/{fid}/index.html", product_page(feed, payments))
        urls.append(f"{SITE}/feeds/{fid}/")
        history = read_json(os.path.join(ROOT, "feeds", fid, "history.json"), [])
        if history:
            for h in history:
                write(f"feeds/{fid}/weeks/{h['week_end']}.html", digest_page(feed, h))
                urls.append(f"{SITE}/feeds/{fid}/weeks/{h['week_end']}.html")
            write(f"feeds/{fid}/weeks/index.html", weeks_index(feed, history))
            urls.append(f"{SITE}/feeds/{fid}/weeks/")
    write("feeds/get/index.html", get_page(payments))
    write("index.html", hub_page(payments))
    write("sitemap.xml", sitemap(urls))
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /feeds/get/\nSitemap: {SITE}/sitemap.xml\n")
    key = open(os.path.join(ROOT, "config", "indexnow.txt")).read().strip()
    write(f"{key}.txt", key)

    # Operator's counter reference (kept for the probe pages + feeds)
    lines = ["# Probe pages — live counters\n",
             "Every page pings **hits.sh** (no account) for pageviews and CTA clicks. Open a counter URL to read it.",
             "Feed pages count `view`, `subscribe`/`download` (main button) and `sample`; the download page counts `view` and `download` per feed.\n",
             f"Hub: {SITE}/ — views: {HITS_BASE}/view.svg\n",
             "| Feed | Page | Views | Main CTA |", "| --- | --- | --- | --- |"]
    for f in registry.FEEDS:
        paid = (payments.get("feeds") or {}).get(f["id"], {}).get("payment_link")
        cta = "subscribe" if paid else "download"
        lines.append(f"| {f['title']} | {SITE}/feeds/{f['id']}/ | {HITS_BASE}/feeds/{f['id']}/view.svg | {HITS_BASE}/feeds/{f['id']}/{cta}.svg |")
    lines += ["", "| Idea probe | Page | Views | Clicks |", "| --- | --- | --- | --- |"]
    for h, c in PROBES:
        lines.append(f"| {c['title']} | {SITE}/{h}/ | {HITS_BASE}/{h}/view.svg | {HITS_BASE}/{h}/cta.svg |")
    write("PROBE-PAGES.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
