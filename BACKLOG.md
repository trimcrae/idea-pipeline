# BACKLOG.md — Living Idea Store

Append-only store of screened ideas. Update every session. Statuses: `backlog` (passed screen, untested) · `probing` (a reality probe is live) · `signal` (probe returned interest) · `building` · `killed` (dead — keep here so it isn't regenerated).

Each entry: id · concept · shape · tags · demand · catch · next probe · status.

---

## Active

**F-01 — Carrier fraud-risk checker for freight brokers/dispatchers**
- Shape: pain + public data. Tags: `demand:proven crowd:med build:med reach:searchable maint:auto`
- Demand: PROVEN. Freight fraud up ~1,500% since 2021; a 2025 survey had 22% of respondents losing >$200k to fraud in six months; ~85% report direct double-brokering losses. Vetting is currently manual (Carrier411 + phone calls). Data is public (FMCSA SAFER/QCMobile).
- Concept: paste an MC number or broker email → instant risk flag (authority age, lapsed insurance, lookalike-domain clone, one-phone-to-many-authorities clustering).
- Catch: NOT greenfield at the top — Highway, Carrier411, Truckstop serve bigger brokerages. Wedge = the bottom of the market (one-truck operators, tiny dispatch shops) on price + one-click simplicity.
- Next probe (inbound only): one-button landing page for the check, driven by a single organic post in an owner-operator/dispatch community and/or a tiny ad on "carrier vetting / MC lookup" intent. Measure self-serve sign-ups (bar: ≥10). No cold outreach. See `probes/F-01-freight-fraud.md`.
- Status: `backlog` (top candidate)

**C-01 — "Should I grade this card?" expected-value gate**
- Shape: enumerable-ish + forced payment (moneyed hobby). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed-strong. Grading costs real money + months; people guess. Proven adjacent spend ($20–150/card).
- Concept: describe card + raw condition → expected graded value minus fees/turnaround → clear go/no-go.
- Catch: needs graded-sale comps (scraping = fragile, ToS-gray); Card Ladder etc. exist. Defensible slice = the narrow pre-submission decision, not another price DB.
- Next probe: post the calculator concept in a card-collecting forum/subreddit; measure clicks + "I'd use this."
- Status: `backlog`

**N-01 — Travel-nurse multi-state license navigator**
- Shape: pain + public data. Tags: `demand:assumed crowd:med build:med reach:diffuse maint:auto`
- Catch: big but diffuse audience (hard to reach with no audience); Vivian etc. exist. Slice = the license/compact-requirements navigator, not another job board.
- Next probe: thread in a travel-nurse community describing the license tool.
- Status: `backlog`

**H-01 — Rare-houseplant restock alerts**
- Shape: proven-pattern (restock alerting) × uncrowded niche. Tags: `demand:proven-pattern crowd:low build:med reach:searchable maint:auto`
- Catch: scrapers break when shops change pages (agent-absorbable upkeep). Need to seed the watch-list of shops.
- Next probe: free alert for one cultivar across 5 shops; post in a plant community; measure sign-ups.
- Status: `backlog`

**P-01 — Per-jurisdiction court-filing rules validator for freelance paralegals**
- Shape: pain + public data (one region first). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed. A rejected filing or missed format/service rule costs a refile and can blow a deadline (malpractice exposure for the attorney). Paralegals currently keep private checklists.
- Concept: pick a filing type + court → checklist/validator of format, service, and deadline rules for that one jurisdiction, kept current.
- Catch: rules vary by court and change, so staying current is real upkeep (maint:manual); start with one region. Audience is searchable but not tightly enumerable.
- Next probe: post the one-jurisdiction validator concept in a paralegal community/subreddit; count clicks + "I'd use this."
- Status: `backlog`

**L-01 — Regulated-trade license/CE renewal + requirement navigator (pest-control techs first)**
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from draws #183 (pest-control + regulation deadline) and #190 (home-inspector deadline reminder); part of the "regulated-license navigator" cluster with N-01 and P-01 — same buildable engine, different niche.
- Concept: pick a trade + state → the renewal deadline, CE hours required, and the specific rules (e.g. which pesticide labels/uses are legal here), kept current. The thing the tech currently digs out of a state .gov PDF.
- Demand: assumed. License = livelihood; lapse/violation = fine or lost income. They actively search "[state] [trade] license renewal CE requirements" — inbound, no outreach needed.
- Catch: rules change and are per-state (real upkeep, `maint:manual`); some state boards publish this already (`crowd:med`) — wedge is aggregation + plain-language + reminders across states, one trade at a time.
- Next probe (inbound): a free single-state CE/renewal checker page for one trade, seeded to rank on the search term + one post in a trade forum; measure self-serve sign-ups (≥10).
- Status: `backlog`

**FB-01 — Cottage-food / mobile-food permit + rule navigator for tiny food businesses**
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from draws #34 (food-truck recall/notice) and #75 (cottage-baker decoder); JTBD reframe = "before I sell a single jar/plate, what does my state actually let me do, and what permit do I need?"
- Concept: pick state (+ county) and product → what's allowed under cottage-food/mobile-vendor law, the permit/inspection steps, and the limits (revenue caps, labeling). Plain-language over the health-dept rulebook.
- Demand: assumed. Selling without compliance = shutdown/fines; the laws are notoriously confusing and state-specific, and new sellers search them constantly.
- Catch: laws change and vary by county (`maint:manual`); blogs/Facebook groups cover this loosely (`crowd:med`) — wedge is a current, structured, per-state answer instead of scattered threads. Tiny-business payer = low price point.
- Next probe (inbound): a free one-state "can I sell this / what permit" checker, ranked on the search term + one post in a cottage-food community; measure sign-ups (≥10).
- Status: `backlog`

**V-01 — Pre-purchase title/lien/theft check for used big-ticket non-car assets (trailers, RVs, boats, powersports, equipment)**
- Shape: pain + public data (inbound) — F-01's "verify before an expensive transaction" structure transposed. Tags: `demand:proven-pattern crowd:med build:med reach:searchable maint:manual`
- Concept: enter a VIN/HIN/serial → flag salvage/lien/theft/odometer issues before buying a used trailer, RV, boat, ATV, or piece of equipment. The check car buyers take for granted, for the asset classes that lack a Carfax.
- Demand: proven-pattern. Pre-purchase history checks are a proven paid behavior for cars (Carfax et al.); the pain (buying a stolen/lien-encumbered $10k+ asset) and the search intent transfer. Buyer pays per-check on a big purchase.
- Catch: data coverage is patchy by asset class and state (NMVTIS covers some; boats/equipment are fragmented) — `maint:manual`, and v1 must pick the asset class with the best public coverage. Cars are `crowd:high`; the wedge is the *non-car* assets nobody serves.
- Next probe (inbound): a landing page for one asset class ("check a used [trailer] before you buy"), driven by search-intent ad/SEO; measure sign-ups or pre-orders (≥10).
- Status: `backlog`

**W-01 — Pre-purchase authenticity / serial-sanity check for used luxury watches**
- Shape: enumerable spend + verification (inbound) — verification-before-expensive-buy transposed to a moneyed market. Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from the watch-flipper/watch-modder draws; JTBD = "before I wire $3k for this watch, is the reference/serial/photo set internally consistent and not a known fake/franken?"
- Concept: enter brand + reference + serial (+ photos) → consistency checks against known reference data and common fake/franken tells; a go/slow-down gate, not an appraisal.
- Demand: assumed. Fakes and franken-watches are rife; buyers routinely ask "how do I spot a fake [brand]" before paying real money — strong inbound search intent on a high-ticket purchase.
- Catch: authoritative reference data is semi-public/community-held and brand-specific (`maint:manual`); forums and some apps partially serve this (`crowd:med`). Wedge = the 60-second pre-wire sanity gate for one brand first.
- Next probe (inbound): a one-brand "is this listing legit?" checker page + one post in a watch-buying community; measure sign-ups (≥10).
- Status: `backlog`

## Killed
Move dead ideas here with a one-line reason so the engine's survivors aren't re-litigated.

**D-01 — Cylinder/gear-service expiry tracker for dive shops** — killed 2026-06-18: reachable only by cold-emailing dive shops (they don't search for this); no inbound path. Dealbreaker under CLAUDE.md #7 / D5. Revive only if a searchable or single-post community path exists.

**A-01 — Abatement regulatory-notice watcher** — killed 2026-06-18: distribution is cold outreach to abatement contractors; no inbound demand or community to post once. Dealbreaker under #7. Revive only with an inbound path.

**B-01 — Bond-deadline/forfeiture validator for bail bondsmen** — killed 2026-06-18: bondsmen won't find this inbound; only route is cold outreach. Also county-by-county data upkeep. Dealbreaker under #7.

**DL-01 — FDA recall watcher for dental labs** — killed 2026-06-18: weakest demand of the set and reachable only by cold-emailing labs; no inbound search/community pull. Dealbreaker under #7.

## Probe log
(date · idea id · probe · result · decision)
