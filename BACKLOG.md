# BACKLOG.md — Living Idea Store

Append-only store of screened ideas. Update every session. Statuses: `backlog` (passed screen, untested) · `probing` (a reality probe is live) · `signal` (probe returned interest) · `building` · `killed` (dead — keep here so it isn't regenerated).

Each entry: name · concept · shape · tags · demand · catch · next probe · status. The kebab `handle` in backticks is the stable reference used by filenames and the probe log — names are informative, not coded.

---

## Active

**Carrier fraud-risk check for small freight brokers/dispatchers** · `freight-fraud-check`
- Shape: pain + public data. Tags: `demand:proven crowd:med build:med reach:searchable maint:auto`
- Demand: PROVEN. Freight fraud up ~1,500% since 2021; a 2025 survey had 22% of respondents losing >$200k to fraud in six months; ~85% report direct double-brokering losses. Vetting is currently manual (Carrier411 + phone calls). Data is public (FMCSA SAFER/QCMobile).
- Concept: paste an MC number or broker email → instant risk flag (authority age, lapsed insurance, lookalike-domain clone, one-phone-to-many-authorities clustering).
- Catch: NOT greenfield at the top — Highway, Carrier411, Truckstop serve bigger brokerages. Wedge = the bottom of the market (one-truck operators, tiny dispatch shops) on price + one-click simplicity.
- Next probe (inbound only): one-button landing page for the check, driven by a single organic post in an owner-operator/dispatch community and/or a tiny ad on "carrier vetting / MC lookup" intent. Measure self-serve sign-ups (bar: ≥10). No cold outreach. Probe kit: `probes/freight-fraud-check.md`.
- Status: `backlog` (top candidate — only `demand:proven` entry)

**Card-grading "is it worth it?" gate** · `card-grading-gate`
- Shape: enumerable-ish + forced payment (moneyed hobby). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed-strong. Grading costs real money + months; people guess. Proven adjacent spend ($20–150/card).
- Concept: describe card + raw condition → expected graded value minus fees/turnaround → clear go/no-go.
- Catch: needs graded-sale comps (scraping = fragile, ToS-gray); Card Ladder etc. exist. Defensible slice = the narrow pre-submission decision, not another price DB.
- Next probe: post the calculator concept in a card-collecting forum/subreddit; measure clicks + "I'd use this." Probe kit: `probes/card-grading-gate.md`.
- Status: `backlog`

**Travel-nurse multi-state license navigator** · `travel-nurse-license-navigator`
- Shape: pain + public data. Tags: `demand:assumed crowd:med build:med reach:diffuse maint:auto`
- Catch: big but diffuse audience (hard to reach with no audience); Vivian etc. exist. Slice = the license/compact-requirements navigator, not another job board. Distribution is the weak leg — the probe specifically tests whether one community post converts.
- Next probe: thread in a travel-nurse community describing the license tool. Probe kit: `probes/travel-nurse-license-navigator.md`.
- Status: `backlog`

**Rare-houseplant restock alerts** · `houseplant-restock-alerts`
- Shape: proven-pattern (restock alerting) × uncrowded niche. Tags: `demand:proven-pattern crowd:low build:med reach:searchable maint:auto`
- Catch: scrapers break when shops change pages (agent-absorbable upkeep). Need to seed the watch-list of shops.
- Next probe: free alert for one cultivar across 5 shops; post in a plant community; measure sign-ups. Probe kit: `probes/houseplant-restock-alerts.md`.
- Status: `backlog`

**Per-jurisdiction court-filing rules validator for freelance paralegals** · `paralegal-filing-validator`
- Shape: pain + public data (one region first). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed. A rejected filing or missed format/service rule costs a refile and can blow a deadline (malpractice exposure for the attorney). Paralegals currently keep private checklists.
- Concept: pick a filing type + court → checklist/validator of format, service, and deadline rules for that one jurisdiction, kept current.
- Catch: rules vary by court and change, so staying current is real upkeep (maint:manual); start with one region. Audience is searchable but not tightly enumerable.
- Next probe: post the one-jurisdiction validator concept in a paralegal community/subreddit; count clicks + "I'd use this." Probe kit: `probes/paralegal-filing-validator.md`.
- Status: `backlog`

**Regulated-trade license/CE renewal + requirement navigator (pest-control first)** · `trade-license-renewal-navigator`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from draws #183 (pest-control + regulation deadline) and #190 (home-inspector deadline reminder); part of the "regulated-license navigator" cluster with `travel-nurse-license-navigator` and `paralegal-filing-validator` — same buildable engine, different niche.
- Concept: pick a trade + state → the renewal deadline, CE hours required, and the specific rules (e.g. which pesticide labels/uses are legal here), kept current. The thing the tech currently digs out of a state .gov PDF.
- Demand: assumed. License = livelihood; lapse/violation = fine or lost income. They actively search "[state] [trade] license renewal CE requirements" — inbound, no outreach needed.
- Catch: rules change and are per-state (real upkeep, `maint:manual`); some state boards publish this already (`crowd:med`) — wedge is aggregation + plain-language + reminders across states, one trade at a time.
- Next probe (inbound): a free single-state CE/renewal checker page for one trade, seeded to rank on the search term + one post in a trade forum; measure self-serve sign-ups (≥10). Probe kit: `probes/trade-license-renewal-navigator.md`.
- Status: `backlog`

**Cottage-food / mobile-food permit + rule navigator for tiny food businesses** · `cottage-food-permit-navigator`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from draws #34 (food-truck recall/notice) and #75 (cottage-baker decoder); JTBD reframe = "before I sell a single jar/plate, what does my state actually let me do, and what permit do I need?"
- Concept: pick state (+ county) and product → what's allowed under cottage-food/mobile-vendor law, the permit/inspection steps, and the limits (revenue caps, labeling). Plain-language over the health-dept rulebook.
- Demand: assumed. Selling without compliance = shutdown/fines; the laws are notoriously confusing and state-specific, and new sellers search them constantly.
- Catch: laws change and vary by county (`maint:manual`); blogs/Facebook groups cover this loosely (`crowd:med`) — wedge is a current, structured, per-state answer instead of scattered threads. Tiny-business payer = low price point.
- Next probe (inbound): a free one-state "can I sell this / what permit" checker, ranked on the search term + one post in a cottage-food community; measure sign-ups (≥10). Probe kit: `probes/cottage-food-permit-navigator.md`.
- Status: `backlog`

**Pre-purchase title/lien/theft check for used big-ticket non-car assets (trailers, RVs, boats, powersports, equipment)** · `used-asset-title-check`
- Shape: pain + public data (inbound) — the `freight-fraud-check` "verify before an expensive transaction" structure transposed. Tags: `demand:proven-pattern crowd:med build:med reach:searchable maint:manual`
- Concept: enter a VIN/HIN/serial → flag salvage/lien/theft/odometer issues before buying a used trailer, RV, boat, ATV, or piece of equipment. The check car buyers take for granted, for the asset classes that lack a Carfax.
- Demand: proven-pattern. Pre-purchase history checks are a proven paid behavior for cars (Carfax et al.); the pain (buying a stolen/lien-encumbered $10k+ asset) and the search intent transfer. Buyer pays per-check on a big purchase.
- Catch: data coverage is patchy by asset class and state (NMVTIS covers some; boats/equipment are fragmented) — `maint:manual`, and v1 must pick the asset class with the best public coverage. Cars are `crowd:high`; the wedge is the *non-car* assets nobody serves.
- Next probe (inbound): a landing page for one asset class ("check a used [trailer] before you buy"), driven by search-intent ad/SEO; measure sign-ups or pre-orders (≥10). Probe kit: `probes/used-asset-title-check.md`.
- Status: `backlog`

**Pre-purchase authenticity / serial-sanity check for used luxury watches** · `watch-authenticity-check`
- Shape: enumerable spend + verification (inbound) — verification-before-expensive-buy transposed to a moneyed market. Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from the watch-flipper/watch-modder draws; JTBD = "before I wire $3k for this watch, is the reference/serial/photo set internally consistent and not a known fake/franken?"
- Concept: enter brand + reference + serial (+ photos) → consistency checks against known reference data and common fake/franken tells; a go/slow-down gate, not an appraisal.
- Demand: assumed. Fakes and franken-watches are rife; buyers routinely ask "how do I spot a fake [brand]" before paying real money — strong inbound search intent on a high-ticket purchase.
- Catch: authoritative reference data is semi-public/community-held and brand-specific (`maint:manual`); forums and some apps partially serve this (`crowd:med`). Wedge = the 60-second pre-wire sanity gate for one brand first.
- Next probe (inbound): a one-brand "is this listing legit?" checker page + one post in a watch-buying community; measure sign-ups (≥10). Probe kit: `probes/watch-authenticity-check.md`.
- Status: `backlog`

**Visa-bulletin / priority-date + processing-time tracker for immigration practitioners** · `visa-bulletin-tracker`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:auto`
- Developed from draw #103 (immigration paralegals + monitoring/alert, "matters seasonally") and the immigration-paralegal pairs in the combine pool; part of the regulated-compliance-navigator cluster (with `travel-nurse-license-navigator`, `paralegal-filing-validator`, `trade-license-renewal-navigator`, `cottage-food-permit-navigator`).
- Concept: track a firm's cases against the monthly State Dept visa bulletin + USCIS processing times → alert when a priority date becomes current or a window/filing opportunity opens. The thing practitioners check obsessively by hand each month.
- Demand: assumed. Missing a date-becomes-current window delays a client's case by months and is a liability/relationship hit; the bulletin moves monthly and unpredictably. Public data (visa bulletin, USCIS processing-time pages), so `maint:auto`.
- Catch: consumer-facing predictors exist (VisaJourney, etc.) → `crowd:med`; the wedge is the *practitioner caseload* view (alert me about *my* cases), not another public forum. Solo/small immigration firms are the payer.
- Next probe (inbound): a free "is your priority date current?" + email-alert page targeting the search term, plus one post in an immigration-practitioner community; measure sign-ups (≥10). Probe kit: `probes/visa-bulletin-tracker.md`.
- Status: `backlog`

**"Am I being lowballed?" independent value-range gate for estate executors & heirs liquidating a collection** · `estate-lowball-gate`
- Shape: verification-before-irreversible-decision + forced payment (inbound) — the seller-side mirror of `freight-fraud-check` / `used-asset-title-check` / `watch-authenticity-check`. Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from the estate-executor / "selling a deceased relative's collection" niche, which the 2026-06-19 pool surfaced seven times across both modes (single #58, #102, #111, #131, #150, #154, #167; combine #166). Repeated independent draws on one niche = signal worth catching.
- Concept: heir/executor enters or photographs a collection (coins, stamps, records, tools, jewelry) → gets a defensible independent value *range* from recent sold-comps before accepting an estate-buyer's or auctioneer's offer. A "should I take this offer" gate, not a formal appraisal.
- Demand: assumed, but strong inbound logic — people actively search "how much is my late parent's [X] collection worth" and "how to value estate contents for probate"; probate often *requires* a valuation (money forces it); the market is trust-poor (heirs fear the estate-sale company is lowballing — that distrust is the wedge, since the incumbent is the party they don't trust).
- Catch: one-time use per customer (low LTV — must be cheap/SEO-fed, no retention), valuation borders on judgment (`maint:manual`), and v1 must pick the *one* category with the cleanest public sold-comp data (likely coins or records) rather than "any collection."
- Next probe (inbound): a single-category landing page — "Don't let the estate buyer lowball Grandpa's [coin] collection — get an independent value range" — driven by search intent; measure sign-ups/pre-orders (≥10). Probe kit: `probes/estate-lowball-gate.md`.
- Status: `backlog`

## Killed
Move dead ideas here with a one-line reason so the engine's survivors aren't re-litigated.

**Cylinder/gear-service expiry tracker for dive shops** · `dive-cylinder-expiry-tracker` — killed 2026-06-18: reachable only by cold-emailing dive shops (they don't search for this); no inbound path. Dealbreaker under CLAUDE.md #7 / D5. Revive only if a searchable or single-post community path exists.

**Asbestos-abatement regulatory-notice watcher** · `abatement-notice-watcher` — killed 2026-06-18: distribution is cold outreach to abatement contractors; no inbound demand or community to post once. Dealbreaker under #7. Revive only with an inbound path.

**Bond-deadline/forfeiture validator for bail bondsmen** · `bail-bond-deadline-validator` — killed 2026-06-18: bondsmen won't find this inbound; only route is cold outreach. Also county-by-county data upkeep. Dealbreaker under #7.

**FDA recall watcher for dental labs** · `dental-lab-recall-watcher` — killed 2026-06-18: weakest demand of the set and reachable only by cold-emailing labs; no inbound search/community pull. Dealbreaker under #7.

## Probe log
(date · idea handle · probe · result · decision)
