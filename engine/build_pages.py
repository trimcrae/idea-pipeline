#!/usr/bin/env python3
"""Build the probe landing pages from a single content table.

One folder per idea (served at /idea-pipeline/<handle>/), a root hub, and shared
assets. hits.sh view/click counters are derived from the URL path at runtime
(see assets/probe.js), so a new page needs no per-page wiring — just a row here.

Run from repo root:  python engine/build_pages.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HITS_BASE = "https://hits.sh/trimcrae.github.io/idea-pipeline"

CSS = """:root { --ink:#11161c; --muted:#5a6470; --line:#e4e8ee; --accent:#1463ff; --bg:#fbfcfe; }
* { box-sizing:border-box; }
body { margin:0; font:17px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--ink); background:var(--bg); -webkit-font-smoothing:antialiased; }
.wrap { max-width:560px; margin:0 auto; padding:40px 22px 64px; }
.kicker { font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); font-weight:700; margin:0 0 14px; }
h1 { font-size:30px; line-height:1.18; margin:0 0 16px; letter-spacing:-.01em; }
.sub { font-size:18px; color:var(--muted); margin:0 0 28px; }
.one { background:#fff; border:1px solid var(--line); border-radius:14px; padding:18px 20px; margin:0 0 28px; font-weight:500; }
.one b { color:var(--accent); }
form { display:flex; flex-direction:column; gap:12px; margin:0 0 14px; }
input[type=email] { width:100%; padding:15px 16px; font-size:17px; border:1px solid var(--line); border-radius:11px; background:#fff; }
input[type=email]:focus { outline:none; border-color:var(--accent); box-shadow:0 0 0 3px rgba(20,99,255,.12); }
button { padding:16px; font-size:17px; font-weight:700; color:#fff; background:var(--accent); border:0; border-radius:11px; cursor:pointer; }
button:active { transform:translateY(1px); }
button:disabled { opacity:.6; }
.msg { font-size:15px; margin:6px 0 0; min-height:20px; }
.ok { color:#0a7d33; } .err { color:#c0392b; }
ul.checks { list-style:none; padding:0; margin:8px 0 28px; }
ul.checks li { padding:7px 0 7px 26px; position:relative; color:var(--ink); }
ul.checks li::before { content:"\\2713"; position:absolute; left:0; color:var(--accent); font-weight:700; }
.foot { font-size:14px; color:var(--muted); border-top:1px solid var(--line); padding-top:18px; margin-top:8px; }
.foot a { color:var(--accent); text-decoration:none; }
.hub { list-style:none; padding:0; margin:6px 0 28px; display:flex; flex-direction:column; gap:12px; }
.hub a { display:block; background:#fff; border:1px solid var(--line); border-radius:12px; padding:16px 18px; text-decoration:none; color:var(--ink); }
.hub a:active { transform:translateY(1px); }
.hub b { display:block; font-size:17px; margin-bottom:3px; }
.hub span { color:var(--muted); font-size:15px; }
"""

JS = """(function () {
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

# handle: dict of page content. Order here = order on the hub.
PAGES = [
  ("freight-fraud-check", {
    "kicker": "For small dispatch shops & owner-operators",
    "title": "Check a carrier for fraud before you book the load",
    "desc": "Paste an MC number or a broker email and get an instant fraud-risk flag — authority age, lapsed insurance, lookalike-domain clones, phone clustering. For small dispatch shops and one-truck operators.",
    "h1": "Check a carrier for fraud before you book the load.",
    "sub": "Paste an MC number or a broker email. Get an instant risk flag — not enterprise software, not a phone-tree of calls.",
    "one": "The 30-second check you do today by hand across SAFER, a phone call, and a gut feeling — in <b>one click</b>.",
    "checks": ["Authority age &amp; recent reactivations", "Lapsed or missing insurance", "Lookalike-domain clones of real carriers", "One phone number across many authorities"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Surfaces public risk <em>signals</em> from FMCSA data; you decide. Not a verdict that a carrier is fraudulent.",
    "hub": "Check a carrier for fraud before you book the load.",
  }),
  ("card-grading-gate", {
    "kicker": "For collectors weighing a grading submission",
    "title": "Is grading this card worth the fees and the wait?",
    "desc": "Describe a card and its raw condition and get an expected graded value minus fees and turnaround — a clear go/no-go before you submit. Built on public sold comps.",
    "h1": "Is grading this card worth the fees and the wait?",
    "sub": "Describe the card and its condition. Get an expected graded value minus fees and turnaround — a clear go/no-go before you mail it off.",
    "one": "The “should I even submit this?” math you guess at today — comps, fees, months of wait — in <b>one answer</b>.",
    "checks": ["Expected grade range from recent sold comps", "Grading fee + turnaround netted out", "Break-even vs. selling it raw", "Public eBay sold data, not a paid database"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. An informational estimate from public sold comps, not an appraisal or financial advice — you decide whether to submit.",
    "hub": "Is grading this card worth the fees and the wait?",
  }),
  ("travel-nurse-license-navigator", {
    "kicker": "For travel nurses working across states",
    "title": "Which states can you work in — and what does each license require?",
    "desc": "Pick your license and target states. See NLC compact coverage, what each non-compact state requires, fees, timelines, and renewal dates — without digging through every board site.",
    "h1": "Which states can you work in — and what does each license require?",
    "sub": "Pick your license and your target states. See compact coverage, what each non-compact state requires, and the steps — in one place.",
    "one": "The compact-vs-single-state license maze, mapped for your states, in <b>one place</b>.",
    "checks": ["NLC compact coverage for your home state", "Per-state requirements for non-compact states", "Fees, timelines, and renewal dates", "Published board rules + links to verify"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Presents published board requirements + source links; it never certifies you're licensed — you verify with the board.",
    "hub": "Which states can you work in, and what does each license require?",
  }),
  ("houseplant-restock-alerts", {
    "kicker": "For rare-plant collectors who keep missing drops",
    "title": "Get an alert the moment that rare plant is back in stock",
    "desc": "Pick a cultivar and the shops you watch. We check their pages and email you the moment it restocks — before it sells out again. Free public shop pages, no insider access.",
    "h1": "Get an alert the moment that rare plant is back in stock.",
    "sub": "Pick a cultivar and the shops you watch. We check their pages and email you when it restocks — before it sells out again.",
    "one": "The five tabs you refresh all day, watched for you — a ping instead of FOMO, in <b>one alert</b>.",
    "checks": ["Watch one cultivar across multiple shops", "Restock and price-drop detection", "Email the moment it goes live", "Free public shop pages, no insider access"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. A retail restock alert, no advice of any kind. Shop pages change, so coverage is best-effort.",
    "hub": "Get an alert the moment a rare plant restocks.",
  }),
  ("trade-license-renewal-navigator", {
    "kicker": "For licensed trades — pest control first",
    "title": "Never miss a license renewal or CE deadline again",
    "desc": "Pick your trade and state. Get your renewal date, the CE hours you need, and the rules that apply — kept current, with a reminder before it's due. Built on public .gov pages.",
    "h1": "Never miss a license renewal or CE deadline again.",
    "sub": "Pick your trade and state. Get your renewal date, the CE hours you need, and the rules that apply — with a reminder before it's due.",
    "one": "The renewal date and CE rules buried in a state .gov PDF, pulled out and tracked for you, in <b>one place</b>.",
    "checks": ["Renewal deadline + CE hours for your state", "The specific rules that apply (e.g. legal pesticide uses)", "A reminder before the deadline", "Published .gov rules + links to verify"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Aggregates published deadlines/CE hours + source links; it never certifies you're compliant — you verify.",
    "hub": "Never miss a trade license renewal or CE deadline.",
  }),
  ("cottage-food-permit-navigator", {
    "kicker": "For home &amp; mobile food sellers",
    "title": "Before you sell a single jar, know what your state lets you do",
    "desc": "Pick your state and product. See what cottage-food / mobile-vendor law allows, the permit and inspection steps, and the limits — in plain language over the health-dept rulebook.",
    "h1": "Before you sell a single jar, know what your state lets you do.",
    "sub": "Pick your state and product. See what cottage-food / mobile-vendor law allows, the permit and inspection steps, and the limits — in plain language.",
    "one": "The health-department rulebook for your state and product, in plain English, in <b>one answer</b>.",
    "checks": ["What you can legally sell under cottage-food law", "Permit + inspection steps", "Revenue caps and labeling rules", "Published statute + link to your health dept"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Summarizes what the published statute says + links it; it never clears you to sell — confirm with your health dept.",
    "hub": "What your state lets you sell, before you make the first jar.",
  }),
  ("watch-authenticity-check", {
    "kicker": "For used-watch buyers about to wire real money",
    "title": "Before you wire $3k, does this watch add up?",
    "desc": "Enter brand, reference, and serial (and photos). Get a consistency check against known reference data and common fake/franken tells — a sanity gate before you pay, not an appraisal.",
    "h1": "Before you wire $3k, does this watch add up?",
    "sub": "Enter the brand, reference, and serial (and photos). Get a consistency check against known reference data and common fake/franken tells — a sanity gate, not an appraisal.",
    "one": "The 60-second “is this listing legit?” gut-check you wish you had before paying, in <b>one check</b>.",
    "checks": ["Reference + serial internal consistency", "Known fake / franken-watch tells", "Photo-set sanity flags", "Community reference data, one brand first"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. A consistency / known-fake-tells signal, explicitly not an appraisal or authentication guarantee — you decide.",
    "hub": "Before you wire $3k, does this used watch add up?",
  }),
  ("visa-bulletin-tracker", {
    "kicker": "For immigration practitioners",
    "title": "Know the moment a priority date goes current",
    "desc": "Track your caseload against the monthly visa bulletin and USCIS processing times. Get alerted when a date becomes current or a filing window opens — without checking by hand.",
    "h1": "Know the moment a priority date goes current.",
    "sub": "Track your caseload against the monthly visa bulletin and USCIS processing times. Get alerted when a date becomes current or a window opens.",
    "one": "The visa bulletin you re-check every month, watching your cases for you, in <b>one alert</b>.",
    "checks": ["Your cases vs. the monthly visa bulletin", "Priority-date-current alerts", "USCIS processing-time changes", "Public State Dept + USCIS data"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Monitoring/alerting over public data (“your date is current”), not legal advice — you make the legal call.",
    "hub": "Know the moment a priority date goes current.",
  }),
  ("estate-lowball-gate", {
    "kicker": "For executors &amp; heirs selling a collection",
    "title": "Don't let an estate buyer lowball the collection",
    "desc": "Enter or photograph a collection and get an independent value range from recent sold comps before you accept an offer — so you know if it's fair. Independent of any buyer or auctioneer.",
    "h1": "Don't let an estate buyer lowball the collection.",
    "sub": "Enter or photograph the collection. Get an independent value range from recent sold comps before you accept an offer — so you know if it's fair.",
    "one": "The independent second opinion the estate-sale company won't give you, from real sold comps, in <b>one range</b>.",
    "checks": ["Value range from recent sold listings", "The comps behind the number, shown", "One category at a time, cleanest data first", "Independent of any buyer or auctioneer"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Shows sold comps and a range from them, not a formal appraisal or financial advice — you decide whether to take the offer.",
    "hub": "Don't let an estate buyer lowball the collection.",
  }),
  ("fleet-compliance-tracker", {
    "kicker": "For 1–5 truck owner-operators",
    "title": "Every DOT deadline a small fleet can't afford to miss — on one calendar",
    "desc": "Enter your DOT/MC number and drivers. Get the recurring federal and state deadlines a small operation must hit — MCS-150, UCR, IFTA, medical cards — with a reminder before each.",
    "h1": "Every DOT deadline a small fleet can't afford to miss — on one calendar.",
    "sub": "Enter your DOT/MC number and drivers. Get the recurring federal and state deadlines a small operation must hit, with a reminder before each.",
    "one": "What a big fleet's TMS tracks automatically — MCS-150, UCR, IFTA, medical cards — for the one-truck operator, in <b>one calendar</b>.",
    "checks": ["MCS-150 biennial + UCR annual", "IFTA quarterly + IRP", "CDL medical-card + drug-&amp;-alcohol dates", "Public FMCSA / IFTA / state data"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Surfaces the published deadline + the .gov link; it never certifies you're compliant — you verify.",
    "hub": "Every DOT deadline a small fleet can't miss, on one calendar.",
  }),
  ("str-rule-navigator", {
    "kicker": "For short-term-rental hosts",
    "title": "Do you need a permit to list here — and what are the deadlines?",
    "desc": "Pick your city or county. See what the local short-term-rental law requires before and while you list — permit, lodging tax, caps, zoning — plus the renewal and tax deadlines.",
    "h1": "Do you need a permit to list here — and what are the deadlines?",
    "sub": "Pick your city or county. See what the local STR law requires before and while you list — permit, lodging tax, caps, zoning — plus the deadlines.",
    "one": "The city ordinance and tax rules for your listing, in plain language, in <b>one answer</b>.",
    "checks": ["Permit / registration requirement", "Lodging-tax registration + filing cadence", "Primary-residence or night caps, zoning", "Published ordinance + link to verify"],
    "cta": "Notify me when it's live",
    "foot": "Early — no product yet. Summarizes the published ordinance + links the source; it never says you're legal to operate — you verify with the city.",
    "hub": "Do you need a permit to list your short-term rental here?",
  }),
]

PAGE_TMPL = """<!doctype html>
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
  <p class="foot"><a href="../">&larr; All the checks I'm testing</a></p>
</div>

<noscript><img src="{hits}/{handle}/view.svg" alt="" width="1" height="1" style="position:absolute;left:-9999px;top:-9999px"></noscript>
<script src="../assets/probe.js"></script>
</body>
</html>
"""

HUB_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Early experiments — which of these is worth building?</title>
<meta name="description" content="A handful of dead-simple tools I'm thinking about building. None exists yet. Tap any that hits a nerve.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="wrap">
  <p class="kicker">Early — nothing here is built yet</p>
  <h1>Which of these is worth building?</h1>
  <p class="sub">A handful of dead-simple checks and trackers I'm weighing. Each one solves a specific, annoying problem. Tap any that hits a nerve — that's the only signal I'm after.</p>
  <ul class="hub">
{items}
  </ul>
  <p class="foot">No product, no pitch, no spam. Just testing which problems are real.</p>
</div>
<noscript><img src="{hits}/view.svg" alt="" width="1" height="1" style="position:absolute;left:-9999px;top:-9999px"></noscript>
<script src="assets/probe.js"></script>
</body>
</html>
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)


def main():
    write("assets/style.css", CSS)
    write("assets/probe.js", JS)

    for handle, c in PAGES:
        checks = "\n".join("    <li>%s</li>" % x for x in c["checks"])
        html = PAGE_TMPL.format(
            title=c["title"], desc=c["desc"], kicker=c["kicker"], h1=c["h1"],
            sub=c["sub"], one=c["one"], checks=checks, cta=c["cta"], foot=c["foot"],
            hits=HITS_BASE, handle=handle,
        )
        write("%s/index.html" % handle, html)

    items = "\n".join(
        '    <li><a href="%s/"><b>%s</b><span>%s</span></a></li>' % (h, c["title"], c["hub"])
        for h, c in PAGES
    )
    write("index.html", HUB_TMPL.format(items=items, hits=HITS_BASE))

    # Operator's read-the-counts reference.
    lines = ["# Probe pages — live counters\n",
             "Each idea has a $0 landing page that tracks **pageviews** and **CTA clicks** via",
             "hits.sh (no account). Open a counter URL in a browser to read its running total.",
             "Email capture is off until a Web3Forms key is set in `assets/probe.js`.\n",
             "Hub: https://trimcrae.github.io/idea-pipeline/ (lists them all)\n",
             "| Idea | Page | Views | Clicks |",
             "| --- | --- | --- | --- |"]
    for h, c in PAGES:
        page = "https://trimcrae.github.io/idea-pipeline/%s/" % h
        v = "%s/%s/view.svg" % (HITS_BASE, h)
        k = "%s/%s/cta.svg" % (HITS_BASE, h)
        lines.append("| %s | %s | %s | %s |" % (c["title"], page, v, k))
    write("PROBE-PAGES.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
