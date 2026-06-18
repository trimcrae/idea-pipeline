# TASK.md — One pipeline run

Paste this into a Claude Code on the web session (or set it as a scheduled remote routine) pointed at this repo.

---

Run one pass of the idea pipeline. Follow `CLAUDE.md` doctrine strictly.

0. Read `STRATEGY.md` and run `python engine/status.py`. If the current phase is PROBE (or status warns that most untested ideas are not `demand:proven` and none are probed), the bottleneck is probing, not generation — do the minimum here: add at most 1 idea, or skip appending entirely, and say so. Do not pad the backlog.
1. Read `CLAUDE.md`, `RUBRIC.md`, and the current `BACKLOG.md` (both Active and Killed sections).
2. Generate a fresh pool: `python engine/entropy_engine.py --out pools/pool_$(date +%Y%m%d_%H%M).txt --ledger pools/seen.tsv`. Keep the printed seed. The `--ledger` flag makes the engine skip every (world, form, twist) it has emitted in a past run, so the pool is already deduped against history — commit the updated `pools/seen.tsv` alongside the pool. For a deeper pass, also generate a collision pool with `--mode combine` and develop survivors per `DEVELOP.md` (recombine / vary / invert / transpose — anchored, never free-floating).
3. The engine has handled combination-level dedup. Still discard any draw whose idea is substantively the same as something already in `BACKLOG.md` (Active or Killed), even if the exact triple differs.
4. Screen the rest with `RUBRIC.md`: apply the kill criteria (including the inbound-distribution kill), cluster near-duplicates, and tag survivors. Do **not** rank by predicted success and do **not** pick a winner.
5. Append the strongest survivors to the **Active** section of `BACKLOG.md`, using the existing entry format (id · concept · shape · tags · demand · catch · next probe · status: backlog). Use `demand:assumed` unless you can cite real, checkable evidence. **Cap:** if the Active section already holds **8 or more untested** (`status: backlog`) ideas that are not `demand:proven`, append **at most 1** this run — adding more assumed ideas to an unprobed pile is hoarding. **Exception:** when the operator explicitly requests a generation/development push, the cap is lifted and the only gate is the inbound screen (RUBRIC) — append every genuine inbound survivor, but never pad with `crowd:high` consensus ideas to hit a count.
6. If this run learned anything about the *system* (not just an idea) — the screen letting through noise, a world that's over/under-sampled, the backlog stalling at the probe step — append it to `STRATEGY.md`'s Insight log and adjust the Current phase if it changed.
7. Commit the updated `BACKLOG.md`, the new `pools/` file, the updated `pools/seen.tsv` ledger, and `STRATEGY.md` if touched. Message: `pipeline run <date>: +N candidates`. Open a PR per the cloud workflow.

In the PR summary (blunt, ≤5 sentences): list the new ids and one-liners, and flag if the backlog is filling with weak `demand:assumed` ideas — if so, say the screen should tighten or the engine's `worlds` list should widen.

Hard limits: do not build anything, do not deploy anything, do not create landing pages in this run. Output is backlog + audit trail only.
