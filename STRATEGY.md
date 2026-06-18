# STRATEGY.md — Central planning & strategy

Living doc, committed like everything else (the repo is memory). This is the
meta-layer above `BACKLOG.md`:

- **`BACKLOG.md`** tracks individual *ideas*.
- **`STRATEGY.md`** tracks the state of the *loop itself* — what phase we're in,
  standing decisions, and insights that are true about the **system**, not any
  one idea.

Read this at the start of every run. When a run surfaces something true about
the system (not just an idea), append it to the **Insight log**.

---

## Current phase

**PROBE F-01 + build the inbound bench (DEVELOP).** (updated 2026-06-18)

Two things run in parallel now:
1. **Probe** — the only real progress is testing an idea against real people.
   F-01 is teed up (`probes/F-01-freight-fraud.md`), inbound, pass bar set.
2. **Develop** — the operator wants a deep bench, and the inbound constraint
   (D5) is brutal, so we must *consider* many ideas to find few that survive.
   Generation is exogenous + anchored development (`DEVELOP.md`); the screen
   stays tight. Volume is fine; padding the backlog with crowded consensus is
   not.

Still true: a deep bench is worthless until one idea is probed. Don't let
generation become an excuse to avoid the probe.

## The one metric that matters right now

Run `python engine/status.py`.

Snapshot 2026-06-18: 101,504-combo space, 0.18% burned · 9 active ideas, 8 of 9
**not** `demand:proven`, **0 probed**. The number to move is **probed count**,
not active count. Active count going up while probed count stays at 0 is the
failure mode, not progress.

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
  search/SEO, a landing page, a paid ad, a marketplace listing, or at most a
  single broadcast post the operator doesn't have to babysit. **Consequence:**
  an idea whose only path to its customers is cold outreach is dead on
  distribution, however good the concept — even if the niche is perfectly
  enumerable. This guts the "reach them by hand" reading of doctrine shape (b):
  an enumerable niche now only counts if it is *also* inbound-reachable (the
  customers search for the problem, or gather somewhere you can post once).
  Four backlog ideas (D-01, A-01, B-01, DL-01) were killed under this rule.
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

## Probe pass bar (set; do not move)

A probe passes **only** on real, self-serve action — never on compliments or
replies-in-principle. Default bar (the model owns this; doctrine #3, operator
delegated): **≥10 self-serve sign-ups or paid pre-orders from a single
low-effort inbound traffic push** (one organic post, an SEO-able free tool, or a
~$20 ad), within about a week. Below that = no signal → kill or reshape, log it,
move on. Set per-idea bars in the `probes/` kit *before* shipping so enthusiasm
can't move the goalposts after.

## Insight log (append-only; newest first)

- **2026-06-18 — Per-pass yield is ~1 survivor; volume must come from cadence,
  not bigger single passes.** A second 340-draw pass (240 single + 100 combine)
  produced exactly one new inbound survivor (IM-01, immigration visa-bulletin
  tracker) — everything else was noise, overlapped existing entries, or failed
  the inbound/payer legs. Combine again yielded no standalone survivor. Takeaway:
  the inbound + three-leg screen is correctly brutal, so "keep generating" is
  best served by a **scheduled Routine running many small passes over time**
  (the ledger guarantees no repeats), not by cranking N higher in one sitting.
  This is the validated prompt now in `TASK.md` → Recurring routine prompt.
- **2026-06-18 — F-01's shape is rare: it has all three legs.** Ran a 450-draw
  development pass (300 single + 150 `--mode combine`) and developed survivors
  with `DEVELOP.md` techniques. Yield under the inbound screen was ~1% (4 kept:
  L-01, FB-01, V-01, W-01). The transpositions taught the real lesson: F-01
  works because it has **public data + a bleeding *business* payer + inbound
  search** all at once. Most transpositions lose a leg — BEC/vendor-fraud checks
  fail "public data" (bank ownership isn't public); rental/contractor/job-scam
  checks fail "payer" (the searcher is a broke consumer). **Screen for all three
  legs, not two.** Survivors clustered into two reusable engines: a
  "regulated-compliance navigator" (public rules people search — L-01, FB-01,
  N-01, P-01) and "pre-purchase verification" (V-01, W-01, F-01).
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
- **2026-06-18 — The backlog regresses toward `demand:assumed`.** 8 of 9 active
  ideas are unproven; only F-01 (freight fraud) cites real evidence. This is
  expected — the screen forbids the model from inventing demand — but it means
  the backlog's value is concentrated in the few evidence-backed entries. Treat
  proven-demand ideas as the default probe targets; treat assumed ones as raw
  material, not a roadmap.
- **2026-06-18 — Generation had no cross-run memory (fixed).** Each stateless
  cloud run re-drew and re-screened the same combinations. Added the
  `pools/seen.tsv` ledger so the funnel never re-litigates dead noise.

## Next actions (operator-owned)

1. **Ship the F-01 inbound probe.** F-01 is the only `demand:proven` idea and is
   inbound-reachable (brokers/dispatchers search "check carrier fraud / MC
   lookup"). Kit: `probes/F-01-freight-fraud.md` — a one-button landing page
   plus one organic post or a tiny ad. No cold outreach, no replies to babysit.
   Pass bar is set (≥10 self-serve sign-ups). The model can revise copy; you
   press publish.
2. **Log the result** in `BACKLOG.md` → Probe log, and append any *system*-level
   insight here.

The two earlier open questions are resolved: probe target = F-01 (cold-outreach
alternatives D-01/A-01 are killed under D5), and the pass bar is set above.
