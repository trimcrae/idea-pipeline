# RUBRIC.md — The Screen

This is a **filter and tagger**, not a success predictor. Use it to triage a raw pool down to a shortlist worth a human look. It cannot tell you what will work — only the market can.

## Kill criteria (auto-reject; do not pass to shortlist)
- No one plausibly pays or no acute recurring pain ("nice-to-have for hobbyists who won't pay").
- Requires a large diffuse audience to find it (operator has none).
- **Reachable only by cold outreach.** If the customer won't find it inbound — they don't search for the pain and don't gather anywhere you can post once, so the only route is cold-emailing/DMing/calling them — it's dead on distribution. The operator does no cold outreach (CLAUDE.md #7). An enumerable customer list is *not* enough on its own.
- Needs ongoing human support per customer (operator can't staff that).
- Needs meaningful upfront capital or inventory.
- **Costs the operator money to set up, probe, or run.** $0 is a hard rule (CLAUDE.md #9 / D11): no paid ads, no paid data/API access, no paid SaaS, no hosting beyond a free tier. If the v1 or its probe *requires* spend with no free path — a paid data feed, paid scraping infra, a paid ad to get traffic — it's dead on cost, even if customers would later pay. Free public data + free tiers + organic/SEO/community distribution only.
- Sits squarely on top of a funded incumbent with no price/simplicity wedge underneath.
- Legally or ethically fraught, or requires licenses the operator lacks.
- **Renders licensed-professional advice (legal / medical / financial / tax).** If the core value is an individualized determination the customer relies on — is my filing valid, am I compliant/cleared, what should I do legally, what's it worth so I take the deal — it's the unauthorized practice of a licensed profession and an existential liability (CLAUDE.md #8 / D10). Allowed **only** as an *information / navigation tool* over public rules/data/comps where the customer decides and verifies, disclaimer-forward. An idea that collapses without giving the reliance-grade determination is dead.

## The five tests (a survivor should pass most, strongly)
1. **Demand signal** — proven willingness to pay, OR acute/expensive pain. Prefer evidence (real data, surveys, visible spend) over assumption. Tag: `demand:proven` / `demand:assumed`.
2. **Uncrowded** — would 1,000 people prompting an LLM land here? If yes, drop it. Tag: `crowd:low/med/high`.
3. **Solo-buildable at $0** — one person + an LLM can ship a v1 on free tiers + free public data, no paid feeds/infra (CLAUDE.md #9). A thin layer over public data or a single clear function. Tag: `build:easy/med/hard`.
4. **Inbound-reachable without an audience** — the customer finds *it*, the operator never chases *them*. Best: they actively search for the pain (SEO-able) or self-serve via a free tool / marketplace. Acceptable: one broadcast post where the niche already gathers. Not acceptable: reachable only by cold outreach, even if the list is enumerable. Tag: `reach:searchable/community/diffuse` (drop `enumerable` as a virtue — an enumerable list you can only cold-email is a liability, not an asset, under CLAUDE.md #7).
5. **Maintenance an agent can absorb** — upkeep is re-pulling data / re-running rules, not bespoke human judgment. Tag: `maint:auto/manual`.

## The two winning shapes (bias toward these)
- **Pain + public data:** urgent, expensive problem where the needed data is publicly available (regulatory, fraud, compliance, deadlines). Best when the sufferer *searches* for the problem (inbound).
- **Inbound-reachable + forced payment:** small niche where liability or money makes paying non-optional **and** the niche finds you inbound — they search for the pain or gather where you can post once. (This is the old "enumerable + forced payment" shape, narrowed: an enumerable list reachable only by cold outreach no longer qualifies — see kill criteria and CLAUDE.md #7.)

## Output format when screening a pool
For each survivor: one-line concept · shape · tags · demand evidence (or "assumed") · the honest catch · a candidate next probe. Then stop. Do not pick the winner — hand the shortlist to the operator.
