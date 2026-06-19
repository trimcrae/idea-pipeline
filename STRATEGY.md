# STRATEGY.md — Central planning & strategy

Living doc, committed like everything else (the repo is memory). This is the
meta-layer above `BACKLOG.md`:

- **`BACKLOG.md`** tracks individual *ideas*.
- **`STRATEGY.md`** tracks the state of the *loop itself* — what phase we're in,
  standing decisions, and insights that are true about the **system**, not any
  one idea.

Read this at the start of every run. When a run surfaces something true about
the system (not just an idea), append it to the **Insight log**.

Ideas are referenced by an informative **handle** (kebab-case, e.g.
`freight-fraud-check`), not an opaque code. The handle is the stable key shared
by `BACKLOG.md`, the probe kit filename, and the probe log.

---

## Current phase

**PROBE + the bench is probe-ready (DEVELOP).** (updated 2026-06-19)

Two things run in parallel now:
1. **Probe** — the only real progress is testing an idea against real people.
   `freight-fraud-check` is the natural first probe (the only `demand:proven`
   entry), kit at `probes/freight-fraud-check.md`, inbound, pass bar set. As of
   2026-06-19 **every** active idea has a drafted probe kit in `probes/`, so the
   operator can pick any one and ship in minutes — maturity is no longer the
   blocker; choosing-and-shipping is.
2. **Develop** — the operator wants a deep bench, and the inbound constraint
   (D5) is brutal, so we must *consider* many ideas to find few that survive.
   Generation is exogenous + anchored development (`DEVELOP.md`); the screen
   stays tight. Volume is fine; padding the backlog with crowded consensus is
   not.

Still true: a deep bench is worthless until one idea is probed. Don't let
generation become an excuse to avoid the probe.

## The one metric that matters right now

Run `python engine/status.py`.

Snapshot 2026-06-19: 11 active ideas (12 after the generation push, then
`used-asset-title-check` killed under #9 once its free-data path was researched),
10 of 11 **not** `demand:proven`, **0 probed**, all probe-kit-ready. The number to
move is **probed count**, not active count or kit count. Active/kit count going up
while probed count stays at 0 is the failure mode, not progress — the bench is
deep enough that the only thing that matters is shipping one probe.

## Standing decisions

- **D1 — Generation has cross-run memory.** The engine dedups against
  `pools/seen.tsv` (`--ledger`). Stateless cloud runs no longer re-surface the
  same combos. Pure de-dup, so generation stays exogenous.
- **D2 — Assumed-idea cap.** When Active holds ≥8 untested, not-`proven` ideas,
  a run appends at most 1 (see `TASK.md`). The constraint is probing, not
  generation.
- **D3 — The model never crowns and never probes.** It screens (kill/cluster/
  tag), drafts probe assets, and red-teams. Picking which idea to probe and
  shipping the probe are the operator's, always. Model enthusiasm = zero
  evidence (doctrine #2, #3).
- **D4 — Nothing is deployed from a run.** Probe assets are drafted into
  `probes/` as copy only; the operator ships them (doctrine #4).
- **D5 — No cold outreach. Distribution must be inbound. (Hard dealbreaker.)**
  The operator will not cold-email, DM, or call prospects, will not run sales
  conversations, and will not do sustained 1:1 customer contact. This is a
  constraint, not a preference. Viable distribution is **inbound / self-serve**:
  search/SEO, a free landing page, a marketplace listing, or at most a single
  broadcast post the operator doesn't have to babysit. (Paid ads are out under
  the $0 rule, D11.) **Consequence:**
  an idea whose only path to its customers is cold outreach is dead on
  distribution, however good the concept — even if the niche is perfectly
  enumerable. This guts the "reach them by hand" reading of doctrine shape (b):
  an enumerable niche now only counts if it is *also* inbound-reachable (the
  customers search for the problem, or gather somewhere you can post once).
  Four backlog ideas (`dive-cylinder-expiry-tracker`, `abatement-notice-watcher`,
  `bail-bond-deadline-validator`, `dental-lab-recall-watcher`) were killed under
  this rule.
- **D6 — Development is allowed, anchored, and never crowns.** Beyond raw draws,
  the model may recombine (`--mode combine`), vary, invert, and transpose to
  generate more candidates — but every one must trace to an exogenous draw or a
  real, citable pain (`DEVELOP.md`), never free-floating ideation. During an
  explicit operator-requested generation/development push, the TASK.md
  assumed-idea cap is lifted; quality is gated by the inbound screen, not a
  count. Still no crowning, no demand simulation.
- **D7 — Model policy: cheapest that screens honestly.** There is no automatic
  per-task model router in Claude Code; the model is chosen per Routine (and per
  subagent). The nightly Routine runs on **Sonnet** by default — fully capable of
  rubric-driven screening, ~3× cheaper than Opus, so the same quota buys more
  runs. Drop to **Haiku** for max volume at the cost of screening quality; reserve
  **Opus** for genuinely hard one-off judgment (a routine rarely needs it). This
  is separate from the operator's interactive/daytime model, which stays full
  power — set it on the Routine, not in committed `settings.json`, so daytime chat
  isn't downgraded. Mechanical sub-steps (engine runs, git) can be pinned to
  `haiku` via subagents; the screening judgment uses the Routine's model.
- **D8 — Always push; PRs are pre-authorized; never park a diff.** The operator
  works from a phone and wants completed, verified changes committed, pushed, and
  merged — never sitting as an unpushed local diff (CLAUDE.md "Git workflow").
  Standing authorization (2026-06-19, reinforced same day): **commit and push the
  moment work is complete and verified, without asking** — never end a turn with
  completed work unpushed, and never ask "want me to push?". Then open a PR and
  **squash-merge to `main`** yourself. Only hold off *merging* if the change is
  ambiguous, risky, or has an open question — but push to the branch regardless;
  the question is about merging, not pushing. Overrides any default "don't push /
  don't open a PR unless asked" posture for this repo.
- **D9 — Ideas get informative names, not codes.** Every idea is referenced by a
  readable kebab handle (e.g. `freight-fraud-check`, `estate-lowball-gate`), used
  identically in `BACKLOG.md`, the `probes/` filename, and the probe log. No
  opaque `X-01` codes — a glance at the handle should tell you what the idea is.
- **D10 — No licensed-professional advice. Sell information, not a
  determination. (Hard dealbreaker.)** The product surfaces public rules,
  deadlines, data, and comps and lets the *customer* decide and verify; it must
  never render an individualized **legal, medical, financial, or tax**
  determination the customer relies on ("your filing is valid," "you're
  compliant," "this is what you're allowed to do," "it's worth $X, take the
  deal"). That is the unauthorized practice of a licensed profession and an
  existential liability for a $0 solo operator — wrong advice someone relies on
  is a lawsuit. **Consequence:** the regulated-compliance navigators
  (`travel-nurse-license-navigator`, `trade-license-renewal-navigator`,
  `cottage-food-permit-navigator`, `visa-bulletin-tracker`) and the valuation
  gates (`estate-lowball-gate`, `card-grading-gate`) survive **only** as
  information/navigation tools — present the published rule / deadline / comp +
  the source, disclaimer-forward — never as a reliance-grade verdict. An idea
  whose core value *is* the professional judgment is dead, like cold outreach
  (D5). Killed `paralegal-filing-validator` under this rule: a court-filing
  *validator* sold on malpractice exposure is reliance-grade legal advice by
  design — its value collapses without crossing the line.
- **D11 — $0 to set up, probe, and run. No spend, ever. (Hard dealbreaker.)**
  The operator will not pay money to stand this up — no paid ads, no paid
  data/API access, no paid SaaS, no hosting beyond a free tier, no domain if
  avoidable. Every probe and v1 runs on **free tiers + free public data only**.
  **Consequences:** (a) probe traffic is organic (SEO-able free tool or one
  community post), never a paid ad — this removes the "~$20 ad" option from the
  probe bar and "paid ad" from D5's distribution list; (b) an idea whose v1
  *requires* a paid data feed, paid scraping infra, or paid hosting with no free
  path is dead on cost, even if customers would later pay (the operator can't
  front setup). The operator accepts a higher kill rate and offsets it with
  **more generation** (steering + cadence, D12), not money. Screen build-cost as
  hard as demand and distribution.
- **D12 — Generation steering is substrate hygiene, not crowning.** The only
  exogenous-random step in `entropy_engine.py` is the *collision* (which world ×
  form × twist `os.urandom` picks). The vocabularies are a curated, weighted
  *substrate* — and we deliberately tilt them toward the structure that
  empirically survives the screen: a money/liability payer + free public data +
  inbound search (the three legs), i.e. the two proven engines (the
  compliance-navigator and pre-purchase-verification clusters). Tilting the urn
  raises the survivor base-rate **without predicting which idea wins** — the
  collision stays unpredictable and a deliberate **WILDCARD tier** keeps weird,
  low-base-rate worlds in play so draws remain non-obvious and anti-consensus
  (doctrine #1). This is hygiene like the ledger (which prunes *seen* combos);
  here we prune *structurally-dead* worlds (cold-outreach-only niches, passion-
  without-money hobbies) and widen into survivor-structural-siblings. Curate by
  *structure* (who pays, is the data free, do they search) — **never** toward a
  specific idea or market consensus. Re-tunable: edit the `worlds` groups in the
  engine, don't add a model-judgment step to the draw.

## Probe pass bar (set; do not move)

A probe passes **only** on real, self-serve action — never on compliments or
replies-in-principle. Default bar (the model owns this; doctrine #3, operator
delegated): **≥10 self-serve sign-ups or paid pre-orders from a single
low-effort, $0 inbound traffic push** (one organic post or an SEO-able free
tool — **no paid ads**, D11), within about a week. Below that = no signal → kill or reshape, log it,
move on. Set per-idea bars in the `probes/` kit *before* shipping so enthusiasm
can't move the goalposts after.

## Insight log (append-only; newest first)

- **2026-06-19 — Researched `used-asset-title-check`'s free-data path (the one #9
  AT-RISK flag) and killed it; the $0 rule has a sharp, non-obvious edge.** The
  finding: a thing can be "built on public data" and still fail #9 if the *useful*
  layer is paid and the *free* layer is already a free self-serve tool. NMVTIS
  (the comprehensive title/lien/theft data) has no free API — paid providers only
  — so the differentiated product needs forbidden spend. The free pieces (NICB
  VINCheck, USCG vessel search, SoS UCC search) are each already free direct-to-
  consumer, so wrapping them has no willingness-to-pay and weak defensibility, and
  the strongest one (NICB VINCheck) is rate-limited + ToS-bound so you can't even
  automate it. Squeezed both ways → killed (revivable only if a free automatable
  feed appears or $0 relaxes). **Generalized screen rule:** for any "verification
  over public data" idea, ask *before* maturing it — (1) is the high-value data
  free *and automatable*, or is the free part already a self-serve consumer tool?
  If the payable value requires a paid feed, it's a #9 kill, not a build detail.
  This would have caught it at screen time; fold it into the verification-engine
  checklist. (Net: the "1 at risk" from the bench re-screen is now resolved by
  removal; bench is 11, and every survivor is genuinely $0 or free-but-fragile.)
- **2026-06-19 — Re-screened the whole bench against #8/#9; the older entries
  were never filtered and the probe kits were stale.** New rules (#8 advice, #9
  $0) were added *after* 10 of 12 candidates existed, so "12 that passed the $0
  filter" was false — only the 2 newest were screened at creation. Re-screened all
  12 and made it explicit: every entry now carries an `Advice line (#8)` + `$0 (#9)`
  bullet. Verdict: **8 clean $0** (public-data tools), **3 free-but-fragile**
  (`card-grading-gate`, `estate-lowball-gate`, `watch-authenticity-check` — clean
  comp/reference source is paid, free path = scrape sold-listings, ToS-gray and
  breakable), **1 at real risk** (`used-asset-title-check` — NMVTIS has no free
  API; free path unproven, must be confirmed before any build). Also found the #9
  rule had never reached the **probe kits**: 9 of them still had a paid-"tiny ad"
  Asset C — converted every one to an SEO-able free-page ($0) stand-in, and
  scrubbed stale `paralegal-filing-validator` cluster mentions (killed under #8).
  Lesson: when a doctrine rule lands, sweep *all* artifacts (backlog + probes),
  not just the doctrine files — a filter that isn't applied to existing state is
  just a claim.
- **2026-06-19 — 750-draw generation push: 2 survivors, both from worlds the
  steering had just added; the #8/#9 kills bit visibly.** Ran 300+300 single +
  150 combine. Net 2 inbound survivors — `fleet-compliance-tracker` (DOT/FMCSA
  deadlines for tiny fleets) and `str-rule-navigator` (STR-host permit/tax rules),
  both the compliance-navigator engine, and both drawn from `DOT-regulated fleet
  operators` / `short-term-rental hosts` — worlds *added* in the D12 steering
  change hours earlier. Honest read: yield (~2/750) is comparable to past passes,
  NOT a proven base-rate lift from one push — but the survivors landing squarely
  in the newly-added groups is the mechanism working as intended. The new rules
  did real filtering: killed survivor-shaped draws for professional advice (#8) —
  horse/breeding-dog pre-purchase *health* checks (veterinary determination),
  sales-tax-nexus and customs-classification tools (tax/customs advice, also
  crowded), whisky-cask "is it legit" (financial advice). Most other
  survivor-shaped draws *duplicated* existing bench (verification-engine draws →
  `used-asset-title-check`; estate/food-truck → `estate-lowball-gate` /
  `cottage-food-permit-navigator`) — a sign the bench is saturating, not that
  generation failed. Combine mode again produced no standalone survivor.
- **2026-06-19 — Added a $0 hard rule (D11) and steered the generator's substrate
  (D12) to offset it.** The operator will not spend money to set this up — no paid
  ads, data, SaaS, or hosting beyond free tiers. That kills the "~$20 ad" probe
  option (probes go organic-only) and any idea whose v1 needs a paid feed/infra
  with no free path; the operator accepts the higher kill rate and pays for it in
  *generation*, not dollars. To raise the survivor base-rate without losing
  randomness, recognized that the engine's randomness is only the *collision* —
  the `worlds`/`forms`/`twists` lists are already a curated substrate — so we
  tilted `worlds` toward the two empirically-surviving structures (regulated
  compliance-navigators + pre-purchase verification), pruned the worlds that only
  ever produced dead ideas (cold-outreach-only niches, passion-without-money
  hobbies), and kept an explicit WILDCARD tier so draws stay anti-consensus.
  Worlds 122 → 137; space 101,504 → 113,984. Substrate hygiene, not crowning.
- **2026-06-19 — Squash-merge leaves stale local history; reset to `main` after
  each merge.** Two PRs this session (#11, #12) hit phantom merge conflicts because
  the dev branch retained the pre-squash commits already collapsed into `main`,
  forcing rebase-onto-main gymnastics. Rule (now in CLAUDE.md "Git workflow"):
  after every squash-merge, `git reset --hard origin/main` and force-push so the
  next change starts clean. Also reaffirmed: always commit+push completed work
  immediately, never park a diff, never ask permission to push (D8).
- **2026-06-19 — Added a hard "no licensed-professional advice" rule; it's a
  sibling of the cold-outreach dealbreaker (D10).** Over half the bench was
  regulated-compliance / valuation, which sits on the unauthorized-practice line
  (legal/medical/financial/tax). Codified that the product may only be an
  *information/navigation tool* over public rules and comps — the customer
  decides and verifies — never a reliance-grade determination it carries
  liability for. The distinction that saves the cluster: presenting *published
  bright-line rules, deadlines, and comps* (information) vs *certifying a
  specific case/filing/value the customer acts on* (advice/UPL). The navigators
  present rules; the one idea whose whole value was certifying a filing
  (`paralegal-filing-validator`, pitched on malpractice exposure) couldn't comply
  and was killed. Like D5, this is a *distribution/liability* constraint, not an
  idea-quality one — screen for it at the same altitude.
- **2026-06-19 — The whole bench is now probe-ready; switched ideas from codes
  to names.** Drafted a probe kit for every active idea (was only
  `freight-fraud-check`), so the operator can ship any one without further prep —
  this is the most maturity the pipeline can reach *without the operator picking
  an idea to build* (D3 bars the model from picking). Also retired the opaque
  `X-01` codes for informative handles (D9): the codes carried no information and
  made the backlog harder to scan from a phone. Net: maturity is no longer the
  bottleneck; the single operator decision of *which* probe to ship is.
- **2026-06-18 — Per-pass yield is ~1 survivor; volume must come from cadence,
  not bigger single passes.** A second 340-draw pass (240 single + 100 combine)
  produced exactly one new inbound survivor (`visa-bulletin-tracker`) — everything
  else was noise, overlapped existing entries, or failed the inbound/payer legs.
  Combine again yielded no standalone survivor. Takeaway: the inbound + three-leg
  screen is correctly brutal, so "keep generating" is best served by a
  **scheduled Routine running many small passes over time** (the ledger guarantees
  no repeats), not by cranking N higher in one sitting. This is the validated
  prompt now in `TASK.md` → Recurring routine prompt. (Confirmed again 2026-06-19:
  a 360-draw pass yielded exactly one survivor, `estate-lowball-gate`.)
- **2026-06-18 — `freight-fraud-check`'s shape is rare: it has all three legs.**
  Ran a 450-draw development pass (300 single + 150 `--mode combine`) and
  developed survivors with `DEVELOP.md` techniques. Yield under the inbound screen
  was ~1% (4 kept: `trade-license-renewal-navigator`, `cottage-food-permit-navigator`,
  `used-asset-title-check`, `watch-authenticity-check`). The transpositions taught
  the real lesson: it works because it has **public data + a bleeding *business*
  payer + inbound search** all at once. Most transpositions lose a leg —
  BEC/vendor-fraud checks fail "public data" (bank ownership isn't public);
  rental/contractor/job-scam checks fail "payer" (the searcher is a broke
  consumer). **Screen for all three legs, not two.** Survivors clustered into two
  reusable engines: a "regulated-compliance navigator" (public rules people
  search — `trade-license-renewal-navigator`, `cottage-food-permit-navigator`,
  `travel-nurse-license-navigator`, `paralegal-filing-validator`, `visa-bulletin-tracker`)
  and "pre-purchase verification" (`used-asset-title-check`, `watch-authenticity-check`,
  `freight-fraud-check`, and the seller-side mirror `estate-lowball-gate`).
- **2026-06-18 — Combine mode is high-variance spice, not the main generator.**
  150 two-world collisions produced no standalone survivor this pass (the two
  worlds rarely share a real pain). Keep it for the occasional cross-niche
  spark; lean on single-mode + anchored development for yield.
- **2026-06-18 — Cold outreach is a hard dealbreaker; it reshapes the screen.**
  The operator will not do cold outreach or 1:1 selling (see D5). This isn't a
  tweak — it kills a whole class of otherwise-sensible ideas: enumerable niches
  (dive shops, abatement, bondsmen, dental labs) whose only realistic route to
  the buyer is emailing them one by one. Four backlog ideas died on this. The
  surviving shape is **inbound-reachable**: the customer already searches for
  the pain or gathers somewhere you can post once. Net: distribution, not
  build, is the binding constraint, and the operator's distribution surface is
  narrow (inbound only) — so screen for it hard.
- **2026-06-18 — The bottleneck is probing, not generation.** With the ledger in
  place, idea supply is effectively infinite and free. The scarce, decision-
  relevant resource is *real demand signal*, which only the operator can get.
  The whole system should be tuned to push toward one probe, not more pools.
- **2026-06-18 — The backlog regresses toward `demand:assumed`.** Only
  `freight-fraud-check` cites real evidence; the rest are unproven. This is
  expected — the screen forbids the model from inventing demand — but it means
  the backlog's value is concentrated in the few evidence-backed entries. Treat
  proven-demand ideas as the default probe targets; treat assumed ones as raw
  material, not a roadmap.
- **2026-06-18 — Generation had no cross-run memory (fixed).** Each stateless
  cloud run re-drew and re-screened the same combinations. Added the
  `pools/seen.tsv` ledger so the funnel never re-litigates dead noise.
- **2026-06-19 — A live $0 probe has exactly three operator-only floors; the
  rest is automatable.** Standing up `freight-fraud-check` as a real page proved
  the model can build the page, host it (GitHub Pages, main/root), and measure
  it (hits.sh no-account counters) entirely in-repo — but three steps need a
  real-world identity no tool can fake: (a) repo **visibility** flip, (b) **Pages
  enablement** (the Actions token can't create the Pages site —
  `Resource not accessible by integration`), (c) an **inbox** for an email-capture
  key. Plan probes around those three toggles; everything else is code.
- **2026-06-19 — Views/clicks are a distribution test, not a demand test.** With
  no inbox, the live probe measures pageviews + CTA clicks (hits.sh). That tells
  you whether the channel moved anyone (necessary) — it does NOT measure demand
  (#3/#5). A click is not a sale. Real demand still needs the email key and the
  ≥10-sign-up bar; don't promote an idea to `signal` on traffic alone.

- **2026-06-19 — "Never spray landing pages" retired (operator call).** Doctrine
  #4 no longer forbids deploying many probe pages at once. The whole active bench
  now has a live $0 landing page (`engine/build_pages.py` generates them; hub at
  the site root, per-idea pages at `/<handle>/`, counters in `PROBE-PAGES.md`).
  This does **not** weaken #2/#3/#5: a wall of undistributed pages reads ~0 and a
  view/click still isn't demand. The pages are a cheap standing net for organic/SEO
  traffic; each still needs its one post or a search ranking to become a real test.

## Next actions (operator-owned)

1. **Ship one inbound probe.** Natural first pick: `freight-fraud-check` — the
   only `demand:proven` idea and inbound-reachable (brokers/dispatchers search
   "check carrier fraud / MC lookup"). Kit: `probes/freight-fraud-check.md`. But
   every active idea now has a ready kit in `probes/`, so you can ship whichever
   you want to learn from first. No cold outreach, no replies to babysit; pass
   bar is set (≥10 self-serve sign-ups). The model can revise copy; you press
   publish.
2. **Log the result** in `BACKLOG.md` → Probe log, and append any *system*-level
   insight here.

The earlier open questions are resolved: probe target leans `freight-fraud-check`
(cold-outreach-only alternatives are killed under D5), the pass bar is set above,
and the whole bench is probe-ready.
