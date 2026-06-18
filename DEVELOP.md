# DEVELOP.md — The idea-development playbook

Generation (the entropy engine) gives raw, un-crowded collisions. Most are
noise. This playbook is how you turn the screen's survivors — and known real
pains — into **more** candidates worth screening, on purpose, at volume. The
operator wants a deep bench, so consider many; the screen (RUBRIC.md) and the
inbound constraint (CLAUDE.md #7) keep the bench honest.

## The one rule that keeps this from regressing to consensus

**Every developed idea must stay anchored.** Anchored = it traces back to either
(a) an **exogenous draw** from the engine, or (b) a **real, citable pain** with
evidence. You may recombine, vary, invert, and transpose those anchors. You may
**not** free-associate "what's a good startup" — that path lands on the crowded
consensus the randomness exists to escape (doctrine #1, #2). And you still never
crown: development widens the shortlist, it does not pick a winner.

A fast self-check before adding a developed idea: *"Could 1,000 people prompting
an LLM 'give me a SaaS idea' have produced this?"* If yes, it's crowded — tag
`crowd:high` and probably drop it. Anchored transposition of a specific evidenced
pain into a specific niche usually survives this; generic "AI tool for X" doesn't.

## Techniques (each anchored; each must still pass the inbound + payment screen)

1. **Recombination (collision).** Run `engine/entropy_engine.py --mode combine`
   to collide two worlds, or hand-pair two backlog niches. Ask: is there a tool
   both share that neither's incumbents serve? Anchor: two exogenous worlds.
2. **Variation (neighbors).** Take one survivor and swap exactly one axis —
   same world, different form; or same form, different twist. Generates a small
   family around a promising draw. Anchor: the original draw.
3. **Proven-pain transposition (highest value).** Take an idea with *real
   evidence* and move its structure to an adjacent market that shares the same
   structural pain AND is inbound-reachable. Example anchor: F-01 (freight fraud
   is proven, data is public, victims *search* "how to check"). The pattern =
   "public-data verification/risk check before an expensive transaction the
   worried party googles." Transposes to other searched-for 'is this a scam /
   is this safe' checks. Tag the *pattern* `demand:proven-pattern`, the specific
   market `demand:assumed`, and be honest about `crowd:` — some of these are
   obvious and already served.
4. **Inversion.** Take a draw and do the literal opposite (serve the supplier
   not the hobbyist; read-only not interactive; the moment-it-breaks not the
   happy path). The engine's twists already encode several inversions — apply
   them deliberately to a survivor.
5. **Pick-and-shovel.** Don't serve the gold-rush crowd; serve whoever sells to
   them, or the data exhaust they leave. Anchor: a drawn world + "who profits
   when this niche acts?"
6. **Jobs-to-be-done reframe.** Restate a draw as the job the customer is
   hiring it for ("when X happens, I need to Y so that Z"). Often reveals the
   real, narrower, more-searched pain hiding inside a vague draw.

## How to run a development pass (volume, then screen hard)

1. Generate broadly: a large single-mode pool (`N=300`) **and** a combine pool
   (`--mode combine`), both with `--ledger pools/seen.tsv`. Commit the pools.
2. Skim for the rare draws that already smell of acute pain + public data or a
   forced-payment niche that is **inbound-reachable**. Kill the rest fast.
3. Develop the survivors with the techniques above to spin off neighbors and
   transpositions. Add proven-pain transpositions from the evidenced backlog
   entries.
4. Screen *everything* through RUBRIC.md, including the new inbound kill
   criterion. Tag honestly — most will be `demand:assumed`, and that's fine as
   long as the distribution is inbound and the catch is named.
5. Append the survivors to `BACKLOG.md`. Volume is allowed during an explicit
   development push, but quality is gated by the screen, not by a target count.
   Do not pad with `crowd:high` consensus ideas to hit a number.

## What development does NOT change

- It does not let you crown or rank by predicted success (doctrine #2).
- It does not simulate demand — your enthusiasm is still zero evidence (#3).
- It does not relax the inbound constraint (#7) or the "name the catch" rule.
- The market is still the only judge; a deep bench is worthless until one idea
  is probed. Generate widely, but keep pushing the best toward a real probe.
