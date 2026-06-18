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

**PROBE, not GENERATE.** (set 2026-06-18)

The generator works and the backlog is stocked. The bottleneck is that **zero
ideas have been tested against a real person.** Generating more candidates now
is hoarding — it grows the pile without reducing the only uncertainty that
matters (does anyone pay?). The next real progress is one cheap probe, shipped
by the operator, returning a real signal.

Exit condition for this phase: at least one idea has a logged probe result in
`BACKLOG.md` → then re-assess (promote on signal, kill on silence, and only
*then* consider topping up the backlog).

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

## Insight log (append-only; newest first)

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

1. **Pick one idea to probe.** Default: **F-01** — the only `demand:proven`
   idea, and already marked top candidate. A probe kit is drafted at
   `probes/F-01-freight-fraud.md` (copy only — nothing is live). Swap targets
   if you have a reason; the model isn't crowning F-01, the *evidence* is.
2. **Ship the probe.** You, not the model: stand up the one-button page or send
   the cold DMs in the kit. The model can revise copy; it can't press send.
3. **Log the result** in `BACKLOG.md` → Probe log (date · id · probe · result ·
   decision), and append any *system*-level insight here.

## Open questions for the operator

- Is F-01 the right first probe, or do you want to probe an enumerable/forced-
  payment idea (D-01 dive shops, A-01 abatement) where the customer list is
  cold-emailable even though demand is only assumed?
- What's your real bar for "this probe passed"? Suggest: ≥3 cold replies saying
  "yes, I'd pay," or ≥10 landing-page sign-ups. Set it *before* shipping so
  enthusiasm can't move the goalposts.
