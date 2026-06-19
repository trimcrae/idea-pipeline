# Probe kit — visa-bulletin-tracker: priority-date + processing-time tracker for immigration practitioners

**Status: DRAFT. Nothing here is live.** Model drafts; operator ships (D3/D4).
**Inbound only — no cold outreach** (doctrine #7). See `BACKLOG.md` →
`visa-bulletin-tracker`. Cluster sibling of `trade-license-renewal-navigator` /
`travel-nurse-license-navigator` / `cottage-food-permit-navigator` — same engine,
different niche. Best `maint:auto`
of the cluster (data is fully public and updates on a schedule).

## What the probe tests
One question: **will a solo/small immigration practitioner give an email for an
alert when one of *their* cases' priority dates becomes current?** They check the
monthly visa bulletin by hand today; missing a window delays a client months and
is a liability/relationship hit.

## Pass bar (SET — do not move)
**≥10 self-serve sign-ups** from search-intent traffic and/or one
practitioner-community post, ~one week. Below that = no signal → reshape or kill,
log, move.

## Asset A — landing page (one button; no product behind it)
> **Headline:** Stop checking the visa bulletin by hand. Get an alert the month
> your client's priority date becomes current.
>
> **Sub:** Add your cases' categories and priority dates once. We watch the
> monthly State Dept visa bulletin and USCIS processing times and email you the
> moment a date becomes current or a filing window opens.
>
> **The one thing it does:** the obsessive monthly check, automated, for *your*
> caseload — not another public predictor forum.
>
> **CTA:** Alert me when my dates are current · [email field]
>
> **Honest footer:** Early. No product yet — confirming small firms want this
> before building.

## Asset B — one broadcast community post (post once; don't work the thread)
An immigration-practitioner community (a paralegal/attorney subreddit or
listserv-style forum that allows it).
> Title: A "your client's priority date is now current" alert for your caseload — useful?
>
> Body: I'm checking if practitioners want their own caseload tracked against the
> monthly bulletin + processing times, with an email when a date goes current —
> instead of checking by hand. Not built yet. Would your firm use it? [page]

## Asset C — SEO-able free page (the $0 stand-in for an ad, #9)
Paid ads are out (#9/D11). Publish the free "is your priority date current?" tool
as a page ranking on "visa bulletin [category] current / priority date tracker"
intent — organic, zero spend; note it also pulls consumers, so the page must speak
to practitioners (caseload view).

## Honest note / catch
Consumer-facing predictors exist (VisaJourney etc.) → `crowd:med`; the wedge is
the **practitioner caseload view** ("alert me about *my* cases"), not another
public forum. Solo/small immigration firms are the payer. Data is public and
scheduled, so upkeep is `maint:auto`.

## After the probe
Log in `BACKLOG.md` → Probe log: `date · visa-bulletin-tracker · <probe> ·
<result> · <decision>`. Promote to `signal` only on real sign-ups. Add system
insight to `STRATEGY.md`.
