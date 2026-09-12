# OPERATOR.md — the toggles only you can flip

Everything else is automated. Each item below is a one-time, phone-sized task
(no human interaction with customers, no spend). Until you do them the site
runs in **free-beta mode**: every feed publishes its full weekly CSV for free
and the pages count downloads — a real demand probe, but no revenue.

> **Status 2026-09-12: payments are on hold by your call.** Everything stays free
> until real visitors show up; the weekly build measures traffic into
> `TRAFFIC.md` and the Routine acts if nobody comes (STRATEGY.md D17). When the
> Routine's summary says the traffic bar is met, §1 below is the next step.

## 1. Turn on payments (≈10 minutes, once) — the only mandatory toggle

1. Create a Stripe account at https://dashboard.stripe.com/register (identity +
   bank details; Stripe is free to open, 2.9% + 30¢ per charge).
2. In Stripe: **Developers → API keys → Create restricted key**. Name it
   `feeds-bot`. Give **Write** on *Products*, *Prices* and *Payment Links*
   (Stripe adds the reads those need). Copy the `rk_live_…` key.
3. In GitHub: **repo → Settings → Secrets and variables → Actions → New
   repository secret** → name `STRIPE_SECRET_KEY`, value = the key.
4. In GitHub: **Actions → feeds → Run workflow**. That run creates one Product,
   one monthly Price and one Payment Link per feed, writes the links into
   `config/payments.json`, switches every page from "free beta" to
   "Subscribe — $N/month", and starts publishing the full files encrypted
   (the key travels only in Stripe's post-payment redirect).
5. Optional but recommended: **Stripe → Settings → Billing → Customer portal →
   Activate link**, then paste the `https://billing.stripe.com/p/login/…` URL
   into `config/payments.json` as `"portal_url"` (or tell the model to). Buyers
   can then cancel themselves; nobody has to answer email.

Rotating the key later changes the per-feed encryption keys: existing
subscribers would need a new link. Don't rotate casually.

## 2. Get indexed by Google (≈3 minutes, once)

Bing/Yandex are pinged automatically (IndexNow). Google needs a Search Console
property: https://search.google.com/search-console → add property
`https://trimcrae.github.io/idea-pipeline/` (URL-prefix) → verify with the
"HTML tag" method: paste the tag into `engine/build_pages.py`'s `HEAD` template
(or hand it to the model) → then submit `sitemap.xml`. Nothing else to do; the
sitemap is regenerated every week.

## 3. Optional: a Socrata app token (≈2 minutes)

Public portals throttle keyless clients. If a weekly build logs `HTTP 429`,
register a free app token at https://evergreen.data.socrata.com/signup (any
Socrata login works) and add it as the GitHub secret `SOCRATA_APP_TOKEN`. The
builder sends it automatically.

## What to look at, when you look

- **Traffic:** `TRAFFIC.md` on `main`, regenerated every Monday — views per page,
  files saved, week-over-week change. (`PROBE-PAGES.md` lists the raw counter
  URLs, but opening one adds a hit, so prefer the file.)
- **Money:** the Stripe dashboard. That's the only demand signal that counts.
- **Health:** `feeds/build.json` on `main` — `built_at` older than 8 days or a
  non-empty `failed` list means a portal changed; the weekly Routine fixes the
  registry entry on its next pass. Runs are designed to stay green on flaky
  portals, so you are not emailed about them.

## Notifications (you asked for no emails)

- The `feeds` workflow never commits to a dev branch (bot pushes on an open PR
  are what emailed you on 2026-09-12); it publishes only on `main`, and its
  network steps can't turn a run red. If GitHub still emails you about a failed
  workflow, switch it off once at github.com/settings/notifications → Actions.
- The weekly Claude Routine sends a push notification only, no email. Change or
  disable it at claude.ai/code/routines.
