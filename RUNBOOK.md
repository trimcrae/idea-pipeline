# RUNBOOK.md — How to Run the Pipeline

## A session, start to finish
1. **Generate.** Run `python engine/entropy_engine.py --out pools/pool_<date>.txt --ledger pools/seen.tsv` for a fresh pool (default 180). The `--ledger` flag gives the engine cross-run memory: it never re-emits a (world, form, twist) it has drawn before, so every pool is genuinely new and you stop re-screening the same noise. Re-run with a different seed for more. Widen the `worlds` list in the script for more uncrowded reach — that axis has the most leverage.
2. **Dedupe + skim.** The ledger has already removed past combinations; you only need to drop draws that *substantively* duplicate something in `BACKLOG.md` (active or killed). Expect ~90% of draws to be noise — that's the funnel working.
3. **Pre-screen + tag.** Run survivors through `RUBRIC.md`. Kill dealbreakers, cluster, tag. Do NOT rank by predicted success.
4. **Human eyeball.** Operator reads the shortlist and picks 1–2 to probe. The model does not crown a winner.
5. **Probe reality** on the chosen 1–2 (see playbook below). The model builds the test asset; the operator ships it.
6. **Log + re-rank.** Record the probe and its result in `BACKLOG.md`. Promote anything with signal; move dead ideas to Killed with a reason.

Repeat whenever the backlog runs thin. The point of the loop is to never face a blank page, not to mint winners automatically.

**Check the dashboard first.** `python engine/status.py` prints how much of the combination space the ledger has burned through and the backlog's composition (how many ideas are untested vs. `demand:proven`). If untested-and-unproven ideas are piling up, the bottleneck is *probing*, not generation — probe or prune before adding more. This is the signal to tighten the screen or widen the engine's `worlds` list, not to crank out another pool.

## Reality-probe playbook (cheap, fast, real)
Pick the lightest probe that returns a real demand signal:
- **Landing page** describing the thing as if it exists, with a single "notify me / sign up" button. Count sign-ups.
- **Cold outreach** — 10–20 emails or DMs to named potential customers (best for enumerable niches like dive shops, abatement, small dispatch). Count replies that say "yes, I'd use/pay."
- **Community post** — one honest post in the subreddit/forum/Discord where the niche gathers. Count clicks + "I want this."
- **Tiny ad** (only if you have a few dollars) — point a small spend at the landing page; measure click-through.
A probe "passes" only on real action (sign-up, reply, click) — never on compliments.

## Do not
- Auto-deploy multiple products.
- Treat the model's enthusiasm as evidence.
- Skip the probe and go straight to building.

## Where you work
- **Generation + screening:** automated via `TASK.md` in Claude Code on the web (cloud, phone-driven). Reads this repo, writes survivors back to `BACKLOG.md`, opens a PR.
- **Probing + deciding:** yours, always. The model builds the test asset; you ship it and read the real signal. No automation removes this step.
- **State:** lives in the repo (`BACKLOG.md`, `pools/`), never in the disposable cloud VM.
