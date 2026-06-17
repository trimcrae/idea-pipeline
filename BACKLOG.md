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
- Next probe: landing page describing the one-click check + 10 cold DMs/emails to small dispatch shops and owner-operators; measure replies/signups.
- Status: `backlog` (top candidate)

**C-01 — "Should I grade this card?" expected-value gate**
- Shape: enumerable-ish + forced payment (moneyed hobby). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed-strong. Grading costs real money + months; people guess. Proven adjacent spend ($20–150/card).
- Concept: describe card + raw condition → expected graded value minus fees/turnaround → clear go/no-go.
- Catch: needs graded-sale comps (scraping = fragile, ToS-gray); Card Ladder etc. exist. Defensible slice = the narrow pre-submission decision, not another price DB.
- Next probe: post the calculator concept in a card-collecting forum/subreddit; measure clicks + "I'd use this."
- Status: `backlog`

**D-01 — Cylinder-inspection / gear-service expiry tracker for dive shops**
- Shape: enumerable + forced payment (safety/liability). Tags: `demand:assumed crowd:low build:easy reach:enumerable maint:auto`
- Demand: assumed. Tanks have hard hydro/visual dates; gear has service intervals; misses are safety+liability events.
- Concept: track per-asset inspection/service dates; alert before expiry.
- Catch: small TAM, low ceiling. Virtue = entire customer list is enumerable and cold-emailable (you can reach 100% by hand).
- Next probe: email 20 dive shops describing it; measure replies.
- Status: `backlog`

**N-01 — Travel-nurse multi-state license navigator**
- Shape: pain + public data. Tags: `demand:assumed crowd:med build:med reach:diffuse maint:auto`
- Catch: big but diffuse audience (hard to reach with no audience); Vivian etc. exist. Slice = the license/compact-requirements navigator, not another job board.
- Next probe: thread in a travel-nurse community describing the license tool.
- Status: `backlog`

**A-01 — Abatement/regulated-trade regulatory-notice watcher**
- Shape: enumerable + forced payment (compliance). Tags: `demand:assumed crowd:low build:med reach:enumerable maint:auto`
- Catch: tiny audience; hard to find at scale — but enumerable and compliance-driven.
- Next probe: 15 cold emails to abatement contractors.
- Status: `backlog`

**H-01 — Rare-houseplant restock alerts**
- Shape: proven-pattern (restock alerting) × uncrowded niche. Tags: `demand:proven-pattern crowd:low build:med reach:searchable maint:auto`
- Catch: scrapers break when shops change pages (agent-absorbable upkeep). Need to seed the watch-list of shops.
- Next probe: free alert for one cultivar across 5 shops; post in a plant community; measure sign-ups.
- Status: `backlog`

**B-01 — Bond-deadline / forfeiture-risk validator for bail bondsmen**
- Shape: enumerable + forced payment (liability). Tags: `demand:assumed crowd:low build:med reach:enumerable maint:manual`
- Demand: assumed. A missed court date / paperwork slip can forfeit the whole bond — direct, large money loss. Bondsmen track this in spreadsheets and memory.
- Concept: log each bond's court dates and conditions → validate the paperwork against the jurisdiction's rules and alert before a deadline that would trigger forfeiture.
- Catch: small, slow-adopting TAM; court-rule/calendar data is per-county and not uniformly public, so "maint:manual" until a region is wired up. Enumerable upside: state-licensed bondsman lists are public, so the whole customer list is cold-reachable.
- Next probe: 15 cold emails/calls to bondsmen in one state describing the forfeiture-alert tool; count "yes, I'd use this" replies.
- Status: `backlog`

**P-01 — Per-jurisdiction court-filing rules validator for freelance paralegals**
- Shape: pain + public data (one region first). Tags: `demand:assumed crowd:med build:med reach:searchable maint:manual`
- Demand: assumed. A rejected filing or missed format/service rule costs a refile and can blow a deadline (malpractice exposure for the attorney). Paralegals currently keep private checklists.
- Concept: pick a filing type + court → checklist/validator of format, service, and deadline rules for that one jurisdiction, kept current.
- Catch: rules vary by court and change, so staying current is real upkeep (maint:manual); start with one region. Audience is searchable but not tightly enumerable.
- Next probe: post the one-jurisdiction validator concept in a paralegal community/subreddit; count clicks + "I'd use this."
- Status: `backlog`

**DL-01 — FDA recall / material-notice watcher for dental labs**
- Shape: pain + public data (compliance). Tags: `demand:assumed crowd:low build:easy reach:enumerable maint:auto`
- Demand: assumed. Labs use regulated materials/devices; a recall or safety notice they miss is a liability and remake-cost event. The FDA recall/enforcement data is public and machine-pullable.
- Concept: per-lab watchlist of the materials/devices they use → alert when a matching FDA recall or notice posts.
- Catch: unproven that labs feel this acutely enough to pay; ceiling is low. Virtue: data is public + re-pullable (maint:auto) and dental labs are enumerable (directories/NADL).
- Next probe: email 20 dental labs describing the recall-alert; count replies that say they'd use/pay.
- Status: `backlog`

## Killed
(none yet — move dead ideas here with a one-line reason so the engine's survivors aren't re-litigated)

## Probe log
(date · idea id · probe · result · decision)
