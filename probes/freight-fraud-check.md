# Probe kit — freight-fraud-check: Carrier fraud-risk checker for small freight brokers/dispatchers

**Status: DRAFT. Nothing here is live.** This is the test asset the model
drafts; the operator ships it (doctrine #4, STRATEGY.md D3/D4). **Inbound only —
no cold outreach** (doctrine #7). Do not deploy until you've set the pass bar
(it's set below) and decided to run it.

Why freight-fraud-check first: it's the only `demand:proven` idea in the backlog (freight
fraud up ~1,500% since 2021; survey respondents losing >$200k in six months;
vetting is manual today) **and** it's inbound-reachable — brokers and
dispatchers actively search "check carrier fraud," "MC number lookup,"
"double brokering" — so you can be found instead of chasing anyone. See
`BACKLOG.md` → freight-fraud-check.

## What the probe is testing

One question: **will a small dispatch shop / owner-operator, who found this on
their own, give you their email for a one-click carrier fraud check?** Not "is
the idea good." Not compliments. Self-serve action only.

## Pass bar (SET — do not move)

**≥10 self-serve sign-ups from one low-effort, $0 inbound push** (a single
community post or an SEO-able free tool — no paid ads, D11), within about a week. Below that = no signal → kill or
reshape freight-fraud-check, log it, move on. No replies-in-principle, no "looks useful" — only
sign-ups count.

## Asset A — landing page (single "notify me" button; no product behind it)

> **Headline:** Check a carrier for fraud before you book the load.
>
> **Sub:** Paste an MC number or a broker email. Get an instant risk flag —
> authority age, lapsed insurance, lookalike-domain clones, and one-phone-
> across-many-authorities clustering. Built for one-truck operators and small
> dispatch shops, not enterprise brokerages.
>
> **The one thing it does:** the 30-second check you currently do by hand across
> SAFER, a phone call, and a gut feeling — in one click.
>
> **CTA button:** Notify me when it's live  · [email field]
>
> **Honest footer:** Early. No product yet — checking if small shops want this
> before building it.

## Asset B — one broadcast community post (post once; don't work the thread)

Drop a single honest post where owner-operators/dispatchers already gather
(e.g. an owner-operator subreddit or a dispatch Facebook group that allows it),
linking the landing page. Not a DM campaign — one post, then watch sign-ups.

> Title: A one-click "is this carrier/broker a fraud risk?" check — would you use it?
>
> Body: Small shops eat double-brokering and identity-cloned-carrier hits that
> the big brokerages have $$$ tools for. I'm checking if a dead-simple version
> is worth building: paste an MC# or broker email, get back authority age,
> insurance lapse, lookalike-domain clones, phone-number clustering. Not built
> yet, nothing to buy. If it existed for ~$X/mo, would you use it? Link if you
> want to be notified: [page]

## Asset C — an SEO-able free mini-tool (the $0 stand-in for an ad)

Paid ads are out ($0 rule, #9/D11). Instead, publish the one-click check itself
as a free page targeting the terms the niche already googles ("carrier vetting,"
"MC number lookup," "double brokering check") so it can be *found* — organic
intent traffic, zero spend. Measure visit → sign-up. Same "pay only for intent"
logic as an ad, but the currency is SEO, not dollars.

## SHIP IT — phone, $0, ~10 minutes (the model drafted this; you press publish)

Everything above is the *what*. This is the *do it now from your phone* version.
One landing page that is also the email capture and the sign-up counter, plus one
post. No code, no host, no spend, no account you have to pay for.

### Stack (all free-tier, phone-buildable, no spend)
- **Page + capture + counter: Tally.so free plan.** Unlimited forms, unlimited
  responses, build and edit from a phone browser, gives you a hosted page URL
  (`tally.so/r/...`). The response count *is* your pass-bar metric — no analytics
  to wire up. Sign up free, no card.
- **Fallback if Tally annoys you: Google Forms.** Rock-solid $0, phone-native,
  responses land in a Google Sheet. Less landing-page-like, but it works.
- **Distribution: one organic post** in a community owner-operators/dispatchers
  already read. No DMs, no thread-working.

### Step 1 — build the page (Tally), ~5 min
New form → make it a single page. Paste these blocks in order:

- **Title:** `Check a carrier for fraud before you book the load.`
- **Text block (sub):** `Paste an MC number or a broker email, get an instant risk flag — authority age, lapsed insurance, lookalike-domain clones, and one-phone-across-many-authorities clustering. Built for one-truck operators and small dispatch shops, not enterprise brokerages.`
- **Text block (the one thing):** `The 30-second check you do today by hand across SAFER, a phone call, and a gut feeling — in one click.`
- **Email field** (required), label: `Email — get notified when it's live`
- **Submit button label:** `Notify me`
- **Thank-you message:** `You're on the list. Early — no product yet. I'm checking if small shops want this before building it.`
- **Honest footer (text block at bottom):** `Early. No product yet — testing whether small shops want this before building it.`

Publish → copy the page URL.

### Step 2 — post once, ~3 min
Pick **one** venue where the niche already gathers and that allows a "would you
use this" question (check the sub's self-promo rule first; frame as a question,
not a link-drop, to stay inside ToS):
- Reddit: `r/freightbrokers`, `r/Truckers`, `r/dispatcher`, `r/owneroperators`
- or a dispatch / owner-operator Facebook group that permits it.

Paste (put the Tally URL where `[page]` is):

> **Title:** A one-click "is this carrier/broker a fraud risk?" check — would you use it?
>
> **Body:** Small shops eat double-brokering and identity-cloned-carrier hits that the big brokerages have $$$ tools for. I'm checking if a dead-simple version is worth building: paste an MC# or broker email, get back authority age, insurance lapse, lookalike-domain clones, phone-number clustering. Not built yet, nothing to buy. If it existed, would you use it? Link if you want to be notified: [page]

Post once. Don't work the thread (answer genuine questions if you feel like it,
but it's not required — you're watching sign-ups, not running a conversation).

### Step 3 — wait ~a week, read the number
Open Tally → the response count. **≥10 sign-ups = pass** (build it next). **<10 =
no signal** → kill or reshape, log it, move on. Don't move the bar; don't count
"looks useful" comments. The number is the verdict.

### If the post gets removed (ToS) before it gets traffic
That's the SEO route's cue (Asset C): the page itself is the free tool, ranked on
"carrier vetting / MC lookup / double brokering check" — slower, but no
gatekeeper. For a *first* probe, try the single post first; it's the 10-minute
test. Fall back to SEO only if every community blocks the question.

## After the probe

Log it in `BACKLOG.md` → Probe log: `date · freight-fraud-check · <probe> · <result> ·
<decision>`. Promote to `signal` only on real sign-ups (≥ the bar above). Add
any system insight to `STRATEGY.md`.
