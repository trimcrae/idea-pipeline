# BACKLOG.md — Living Idea Store

Append-only store of screened ideas. Update every session. Statuses: `backlog` (passed screen, untested) · `probing` (a reality probe is live) · `signal` (probe returned interest) · `building` · `killed` (dead — keep here so it isn't regenerated).

Each entry: name · concept · shape · tags · demand · catch · next probe · status. The kebab `handle` in backticks is the stable reference used by filenames and the probe log — names are informative, not coded.

---

## Active

**Weekly public-records feeds for the vendors who sell to newly registered businesses** · `public-records-feeds`
- Shape: pain + public data × forced-payment niche (inbound) — pick-and-shovel on the bench's own worlds (trucking, food service, bars, STR hosts, new businesses). Tags: `demand:proven-pattern crowd:med build:easy reach:searchable maint:auto`
- Demand: proven-pattern — lead vendors already sell FMCSA new-authority lists, "new business" lists and restaurant-opening data (Apify actors, restaurantdata.com, state list brokers); the pattern pays, the specific niches are `demand:assumed` until a download or a subscription says otherwise.
- Concept: one generic pipeline (`engine/feeds/`) pulls the past 7 days from a public open-data portal, normalises it, and publishes a masked sample + stats + a weekly digest page (SEO) and the full CSV (free beta now; encrypted for Stripe subscribers once the key exists). 15 feeds live at https://trimcrae.github.io/idea-pipeline/ — FMCSA carrier registrations, NYC + Chicago restaurant pest citations and openings, NY + Texas liquor-license applications and issuances, Chicago/CT/NY/CO new businesses, NYC permits, New Orleans + Chicago STR permits (3 FMCSA licensing feeds parked: the source snapshots lag months).
- Catch: the trucking-lead niche is crowded (price is the wedge: $29 vs $50–200); state new-business lists are a commodity; small feeds (Chicago pest 23/wk, NOLA STR 46/wk) may be too thin to pay for; a leaked subscriber link keeps working (accepted, D14); buyers do outreach with it — we don't (D15: businesses only, no individuals).
- Advice line (#8): pure public records, republished as-is with a disclaimer; nothing is a determination about anyone.
- $0 (#9): clean — Socrata portals are free and keyless; GitHub Actions + Pages + raw branch hosting; Stripe has no fixed fee.
- Probe (running): free-beta full downloads per feed (`PROBE-PAGES.md`), then Stripe subscriptions. Kill any feed with 0 downloads after 8 live weeks.
- Status: `probing` (live since 2026-09-12; payments pending the operator's Stripe key — `OPERATOR.md`)

**Carrier fraud-risk check for small freight brokers/dispatchers** · `freight-fraud-check`
- Shape: pain + public data. Tags: `demand:proven crowd:med build:med reach:searchable maint:auto`
- Demand: PROVEN. Freight fraud up ~1,500% since 2021; a 2025 survey had 22% of respondents losing >$200k to fraud in six months; ~85% report direct double-brokering losses. Vetting is currently manual (Carrier411 + phone calls). Data is public (FMCSA SAFER/QCMobile).
- Concept: paste an MC number or broker email → instant risk flag (authority age, lapsed insurance, lookalike-domain clone, one-phone-to-many-authorities clustering).
- Catch: NOT greenfield at the top — Highway, Carrier411, Truckstop serve bigger brokerages. Wedge = the bottom of the market (one-truck operators, tiny dispatch shops) on price + one-click simplicity.
- Advice line (#8): outside professional advice — surfaces public risk *signals* (authority age, insurance lapse, lookalike domains), not a verdict that a carrier "is fraudulent"; the user decides.
- $0 (#9): clean — FMCSA SAFER/QCMobile is a free public API.
- Next probe (inbound only): one-button landing page for the check, driven by a single organic post in an owner-operator/dispatch community plus an SEO-able free check page on "carrier vetting / MC lookup" intent (no paid ads, #9). Measure self-serve sign-ups (bar: ≥10). No cold outreach. Probe kit: `probes/freight-fraud-check.md`.
- 2026-09-12 update: the free-lookup slice is now `crowd:high` — at least five AI-built free FMCSA lookup/chameleon-detection sites launched since June. The demand-proven *data* behind it now ships as the trucking feed in `public-records-feeds` (new FMCSA registrations with phone + email; authority-grant/revocation/insurance-cancellation feeds are parked until a diff-based build exists — those would double as a broker's risk watchlist). Keep this entry only as the "risk-flag UI" idea; do not build it as a standalone tool.
- Status: `backlog` (superseded in practice by `public-records-feeds`; probe page kept at `/experiments/`)

**Card-grading "is it worth it?" gate** · `card-grading-gate`
- Shape: enumerable-ish + forced payment (moneyed hobby). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed-strong. Grading costs real money + months; people guess. Proven adjacent spend ($20–150/card).
- Concept: describe card + raw condition → expected graded value minus fees/turnaround → clear go/no-go.
- Catch: needs graded-sale comps (scraping = fragile, ToS-gray); Card Ladder etc. exist. Defensible slice = the narrow pre-submission decision, not another price DB.
- $0 risk (#9/D11): Card Ladder and the comp DBs are paid — v1's comp source must be free (e.g. public eBay sold listings), or it's dead on cost.
- Advice line (#8/D10): an informational estimate from public comps (KBB-style), not financial/appraisal advice — show the comps + range and let the collector decide; never "submit this, it's worth $X."
- Next probe: post the calculator concept in a card-collecting forum/subreddit; measure clicks + "I'd use this." Probe kit: `probes/card-grading-gate.md`.
- Status: `backlog`

**Travel-nurse multi-state license navigator** · `travel-nurse-license-navigator`
- Shape: pain + public data. Tags: `demand:assumed crowd:med build:med reach:diffuse maint:auto`
- Catch: big but diffuse audience (hard to reach with no audience); Vivian etc. exist. Slice = the license/compact-requirements navigator, not another job board. Distribution is the weak leg — the probe specifically tests whether one community post converts.
- Advice line (#8/D10): present the published board requirements + links and let the nurse verify; never certify "you're licensed/cleared to practice in state X."
- $0 (#9): clean — state nursing boards / NURSYS / compact data are public.
- Next probe: thread in a travel-nurse community describing the license tool. Probe kit: `probes/travel-nurse-license-navigator.md`.
- Status: `backlog`

**Rare-houseplant restock alerts** · `houseplant-restock-alerts`
- Shape: proven-pattern (restock alerting) × uncrowded niche. Tags: `demand:proven-pattern crowd:low build:med reach:searchable maint:auto`
- Catch: scrapers break when shops change pages (agent-absorbable upkeep). Need to seed the watch-list of shops.
- Advice line (#8): outside professional domains — retail restock alerts, no determination of any kind.
- $0 (#9): clean — scrapes free public shop pages; fragile, but no paid feed/infra.
- Next probe: free alert for one cultivar across 5 shops; post in a plant community; measure sign-ups. Probe kit: `probes/houseplant-restock-alerts.md`.
- Status: `backlog`

**Regulated-trade license/CE renewal + requirement navigator (pest-control first)** · `trade-license-renewal-navigator`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from draws #183 (pest-control + regulation deadline) and #190 (home-inspector deadline reminder); part of the "regulated-license navigator" cluster with `travel-nurse-license-navigator` — same buildable engine, different niche.
- Concept: pick a trade + state → the renewal deadline, CE hours required, and the specific rules (e.g. which pesticide labels/uses are legal here), kept current. The thing the tech currently digs out of a state .gov PDF.
- Demand: assumed. License = livelihood; lapse/violation = fine or lost income. They actively search "[state] [trade] license renewal CE requirements" — inbound, no outreach needed.
- Catch: rules change and are per-state (real upkeep, `maint:manual`); some state boards publish this already (`crowd:med`) — wedge is aggregation + plain-language + reminders across states, one trade at a time.
- Advice line (#8/D10): aggregate the published deadlines/CE hours/rules + source links and let the licensee verify; never certify "you're compliant / legally allowed to do X." Deadlines and CE counts are facts; legality of a specific practice is not the product's call.
- $0 (#9): clean — state .gov license/CE pages are public.
- Next probe (inbound): a free single-state CE/renewal checker page for one trade, seeded to rank on the search term + one post in a trade forum; measure self-serve sign-ups (≥10). Probe kit: `probes/trade-license-renewal-navigator.md`.
- Status: `backlog`

**Cottage-food / mobile-food permit + rule navigator for tiny food businesses** · `cottage-food-permit-navigator`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from draws #34 (food-truck recall/notice) and #75 (cottage-baker decoder); JTBD reframe = "before I sell a single jar/plate, what does my state actually let me do, and what permit do I need?"
- Concept: pick state (+ county) and product → what's allowed under cottage-food/mobile-vendor law, the permit/inspection steps, and the limits (revenue caps, labeling). Plain-language over the health-dept rulebook.
- Demand: assumed. Selling without compliance = shutdown/fines; the laws are notoriously confusing and state-specific, and new sellers search them constantly.
- Catch: laws change and vary by county (`maint:manual`); blogs/Facebook groups cover this loosely (`crowd:med`) — wedge is a current, structured, per-state answer instead of scattered threads. Tiny-business payer = low price point.
- Advice line (#8/D10): summarize what the published statute says + link it and point to the health dept; never issue a reliance-grade "yes, you're legally allowed to sell this." The wording is "here's the rule," not "you're cleared."
- $0 (#9): clean — state cottage-food statutes / health-dept pages are public.
- Next probe (inbound): a free one-state "can I sell this / what permit" checker, ranked on the search term + one post in a cottage-food community; measure sign-ups (≥10). Probe kit: `probes/cottage-food-permit-navigator.md`.
- Status: `backlog`

**Pre-purchase authenticity / serial-sanity check for used luxury watches** · `watch-authenticity-check`
- Shape: enumerable spend + verification (inbound) — verification-before-expensive-buy transposed to a moneyed market. Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from the watch-flipper/watch-modder draws; JTBD = "before I wire $3k for this watch, is the reference/serial/photo set internally consistent and not a known fake/franken?"
- Concept: enter brand + reference + serial (+ photos) → consistency checks against known reference data and common fake/franken tells; a go/slow-down gate, not an appraisal.
- Demand: assumed. Fakes and franken-watches are rife; buyers routinely ask "how do I spot a fake [brand]" before paying real money — strong inbound search intent on a high-ticket purchase.
- Catch: authoritative reference data is semi-public/community-held and brand-specific (`maint:manual`); forums and some apps partially serve this (`crowd:med`). Wedge = the 60-second pre-wire sanity gate for one brand first.
- Advice line (#8): outside professional advice — a consistency / known-fake-tells *signal*, explicitly not an appraisal or an authentication guarantee; the buyer decides.
- $0 (#9): free but fragile — reference data is community-held (hand-gathered, no paid feed); no paid source required, but upkeep is manual.
- Next probe (inbound): a one-brand "is this listing legit?" checker page + one post in a watch-buying community; measure sign-ups (≥10). Probe kit: `probes/watch-authenticity-check.md`.
- Status: `backlog`

**Visa-bulletin / priority-date + processing-time tracker for immigration practitioners** · `visa-bulletin-tracker`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:auto`
- Developed from draw #103 (immigration paralegals + monitoring/alert, "matters seasonally") and the immigration-paralegal pairs in the combine pool; part of the regulated-compliance-navigator cluster (with `travel-nurse-license-navigator`, `trade-license-renewal-navigator`, `cottage-food-permit-navigator`).
- Concept: track a firm's cases against the monthly State Dept visa bulletin + USCIS processing times → alert when a priority date becomes current or a window/filing opportunity opens. The thing practitioners check obsessively by hand each month.
- Demand: assumed. Missing a date-becomes-current window delays a client's case by months and is a liability/relationship hit; the bulletin moves monthly and unpredictably. Public data (visa bulletin, USCIS processing-time pages), so `maint:auto`.
- Catch: consumer-facing predictors exist (VisaJourney, etc.) → `crowd:med`; the wedge is the *practitioner caseload* view (alert me about *my* cases), not another public forum. Solo/small immigration firms are the payer.
- Advice line (#8/D10): clean fit — this is monitoring/alerting over public data (the bulletin moved, your date is current), not legal advice. Keep it factual ("X happened"); the practitioner makes the legal call. Don't drift into "file now" recommendations.
- $0 (#9): clean — State Dept visa bulletin + USCIS processing-time pages are public.
- Next probe (inbound): a free "is your priority date current?" + email-alert page targeting the search term, plus one post in an immigration-practitioner community; measure sign-ups (≥10). Probe kit: `probes/visa-bulletin-tracker.md`.
- Status: `backlog`

**"Am I being lowballed?" independent value-range gate for estate executors & heirs liquidating a collection** · `estate-lowball-gate`
- Shape: verification-before-irreversible-decision + forced payment (inbound) — the seller-side mirror of `freight-fraud-check` / `used-asset-title-check` / `watch-authenticity-check`. Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from the estate-executor / "selling a deceased relative's collection" niche, which the 2026-06-19 pool surfaced seven times across both modes (single #58, #102, #111, #131, #150, #154, #167; combine #166). Repeated independent draws on one niche = signal worth catching.
- Concept: heir/executor enters or photographs a collection (coins, stamps, records, tools, jewelry) → gets a defensible independent value *range* from recent sold-comps before accepting an estate-buyer's or auctioneer's offer. A "should I take this offer" gate, not a formal appraisal.
- Demand: assumed, but strong inbound logic — people actively search "how much is my late parent's [X] collection worth" and "how to value estate contents for probate"; probate often *requires* a valuation (money forces it); the market is trust-poor (heirs fear the estate-sale company is lowballing — that distrust is the wedge, since the incumbent is the party they don't trust).
- Catch: one-time use per customer (low LTV — must be cheap/SEO-fed, no retention), valuation borders on judgment (`maint:manual`), and v1 must pick the *one* category with the cleanest public sold-comp data (likely coins or records) rather than "any collection."
- Advice line (#8/D10): show the sold-comps and a range from them (the evidence), explicitly not a formal appraisal or financial advice — the heir decides whether to take the offer. The "borders on judgment" catch is exactly the line to not cross: surface comps, don't certify a number.
- $0 (#9): free but fragile — comps come from scraping public sold listings (eBay / auction results); free, but ToS-gray and breakable. No paid comp DB.
- Next probe (inbound): a single-category landing page — "Don't let the estate buyer lowball Grandpa's [coin] collection — get an independent value range" — driven by search intent; measure sign-ups/pre-orders (≥10). Probe kit: `probes/estate-lowball-gate.md`.
- Status: `backlog`

**Small-fleet / owner-operator DOT & FMCSA compliance-deadline tracker** · `fleet-compliance-tracker`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:auto`
- Developed from draws #17/#35/#149/#153 (DOT-regulated fleet operators × constraint-checker / regulation-deadline) and owner-operator-trucker draws; the `trade-license-renewal-navigator` compliance-navigator engine transposed to the trucking niche `freight-fraud-check` already reaches.
- Concept: enter your DOT/MC number (+ drivers) → one calendar of the recurring federal/state deadlines a 1–5 truck operation must not miss: MCS-150 biennial update, UCR annual, IFTA quarterly, IRP, CDL medical-card expiry, drug-&-alcohol program dates, annual vehicle inspection — with a reminder before each. What a big fleet gets from a TMS and the one-truck operator tracks on a wall calendar.
- Demand: assumed (strong logic). A missed MCS-150 deactivates your operating authority; a missed IFTA/UCR is a fine; lapses cost money and downtime. Operators search "MCS-150 due / DOT compliance deadlines / UCR renewal." Public data (FMCSA SAFER/L&I, IFTA/IRP, state), so `maint:auto`.
- Catch: the FMCSA portal and TMS suites touch this (`crowd:med`), but the 1–5 truck owner-operator has no TMS and finds the portals confusing — wedge is a dead-simple single-purpose deadline calendar + reminders for the bottom of the market (same wedge + same inbound community as `freight-fraud-check`).
- Advice line (#8): surfaces the published deadline + the .gov link; never "you are compliant." Deadlines are facts, not a determination.
- $0 (#9): clean — FMCSA / IFTA / state data is public.
- Next probe (inbound, $0): a free "when is your MCS-150 / UCR / IFTA due?" checker page seeded on the search term + one post in an owner-operator/dispatch community; measure self-serve sign-ups (≥10). Probe kit: `probes/fleet-compliance-tracker.md`.
- Status: `backlog`

**Short-term-rental host local-rule, permit & lodging-tax-deadline navigator** · `str-rule-navigator`
- Shape: pain + public data (inbound). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Developed from short-term-rental-host draws (× boring-compliance / regulation-deadline twists); the compliance-navigator engine transposed to the Airbnb/STR-host niche.
- Concept: pick your city/county → what the local STR law requires before and while you list: a permit or registration number, transient-occupancy/lodging-tax registration + filing cadence, primary-residence or night caps, zoning/HOA limits, and the renewal/tax deadlines. Plain-language over the city ordinance, one metro at a time.
- Demand: assumed (strong inbound logic). Cities are cracking down — operating unpermitted risks fines/delisting; hosts have revenue and search "[city] short-term rental rules / permit / registration / lodging tax" constantly. Public data (municipal ordinances, tax pages).
- Catch: hyper-local and changes (`maint:manual`), so v1 picks one metro; the platforms show only a generic line and compliance vendors (Granicus/Deckard) serve the *cities*, not hosts (`crowd:med`) — wedge is the host-side, plain-language, deadline-reminder view for one city first. Low-ish price point, SEO-fed.
- Advice line (#8): summarizes the published ordinance + links the source; never "you're legal to operate." The host verifies.
- $0 (#9): clean — municipal ordinances + tax pages are public.
- Next probe (inbound, $0): a free one-city "do you need an STR permit here?" checker page ranked on the search term + one post in an STR/Airbnb-host community; measure sign-ups (≥10). Probe kit: `probes/str-rule-navigator.md`.
- Status: `backlog`

## Killed
Move dead ideas here with a one-line reason so the engine's survivors aren't re-litigated.

**Cylinder/gear-service expiry tracker for dive shops** · `dive-cylinder-expiry-tracker` — killed 2026-06-18: reachable only by cold-emailing dive shops (they don't search for this); no inbound path. Dealbreaker under CLAUDE.md #7 / D5. Revive only if a searchable or single-post community path exists.

**Asbestos-abatement regulatory-notice watcher** · `abatement-notice-watcher` — killed 2026-06-18: distribution is cold outreach to abatement contractors; no inbound demand or community to post once. Dealbreaker under #7. Revive only with an inbound path.

**Bond-deadline/forfeiture validator for bail bondsmen** · `bail-bond-deadline-validator` — killed 2026-06-18: bondsmen won't find this inbound; only route is cold outreach. Also county-by-county data upkeep. Dealbreaker under #7.

**FDA recall watcher for dental labs** · `dental-lab-recall-watcher` — killed 2026-06-18: weakest demand of the set and reachable only by cold-emailing labs; no inbound search/community pull. Dealbreaker under #7.

**Pre-purchase title/lien/theft check for used big-ticket non-car assets** · `used-asset-title-check` — killed 2026-06-19 under #9 ($0), after researching the flagged free-data question. The comprehensive "Carfax for non-car assets" needs **NMVTIS**, which has *no* free consumer API — only paid approved providers (~$2–13/report) — so the differentiated product requires spend #9 forbids. The layers that *are* free are already free, self-serve consumer tools the buyer can use directly: NICB VINCheck (free stolen+salvage, but 5 searches/IP/day + ToS → not automatable into a product), the USCG vessel-documentation search (free ownership lookup; liens need a paid $25 Abstract of Title), and Secretary-of-State UCC lien searches (free but name-based and 50-state-fragmented). Squeezed on both sides — the free wedge is a thin wrapper over already-free tools (no willingness to pay, weak defensibility), and the only payable value (aggregated NMVTIS) is the forbidden spend. Revive only if (a) a free, automatable, aggregatable data feed appears, or (b) the operator ever relaxes $0 — then the documented-boat slice (free USCG ownership lookup + a customer-paid USCG abstract) is the least-bad re-entry. Sources: NICB VINCheck (nicb.org/vincheck), NMVTIS approved-provider list (vehiclehistory.bja.ojp.gov), USCG/NVDC abstract, state SoS UCC search.

**Per-jurisdiction court-filing rules validator for freelance paralegals** · `paralegal-filing-validator` — killed 2026-06-19: a filing *validator* sold on malpractice/refile exposure is a reliance-grade legal determination by design — its whole value is the customer acting on "your filing is valid." That's the unauthorized practice of law and an existential liability; it collapses if reduced to a non-reliance checklist. Dealbreaker under #8 / D10. Revive only as a pure public-rules reference no one is told to rely on (and then the edge is gone).

## Probe log
(date · idea handle · probe · result · decision)

- 2026-09-12 · `public-records-feeds` · 15 live weekly feeds with free-beta full downloads counted per feed (`PROBE-PAGES.md`); Stripe subscriptions once the operator pastes the key · result: pending — first Monday build 2026-09-14; first read after 8 live weeks (≈2026-11-09) · decision: keep; 3 FMCSA licensing feeds parked (source lags months); kill feeds with 0 downloads at the 8-week read.
- 2026-09-12 · the 11 June probe pages · lived 12 weeks with no post and no distribution · result: hub counter read 31 hits total (read from a runner) — effectively no real traffic · decision: kept as `/experiments/` (noindex); superseded as a strategy by real feeds.
- 2026-09-12 · `public-records-feeds` · operator decision: stay free, measure visitors weekly (`TRAFFIC.md`), act on silence per STRATEGY D17 · result: baseline snapshot pending Monday 2026-09-14 · decision: traffic gate armed; payments deferred until the bar is met.
