# TASK.md — One pipeline run

Paste this into a Claude Code on the web session (or set it as a scheduled remote routine) pointed at this repo.

---

Run one pass of the idea pipeline. Follow `CLAUDE.md` doctrine strictly.

0. Run `python engine/status.py` to see combination-space burn-down and backlog composition. If it warns that most untested ideas are not `demand:proven`, treat the demand bar as *tight* for this run: add fewer, only the strongest, and prefer killing to appending.
1. Read `CLAUDE.md`, `RUBRIC.md`, and the current `BACKLOG.md` (both Active and Killed sections).
2. Generate a fresh pool: `python engine/entropy_engine.py --out pools/pool_$(date +%Y%m%d_%H%M).txt --ledger pools/seen.tsv`. Keep the printed seed. The `--ledger` flag makes the engine skip every (world, form, twist) it has emitted in a past run, so the pool is already deduped against history — commit the updated `pools/seen.tsv` alongside the pool.
3. The engine has handled combination-level dedup. Still discard any draw whose idea is substantively the same as something already in `BACKLOG.md` (Active or Killed), even if the exact triple differs.
4. Screen the rest with `RUBRIC.md`: apply the kill criteria, cluster near-duplicates, and tag survivors. Do **not** rank by predicted success and do **not** pick a winner.
5. Append **at most 5** of the strongest survivors to the **Active** section of `BACKLOG.md`, using the existing entry format (id · concept · shape · tags · demand · catch · next probe · status: backlog). Use `demand:assumed` unless you can cite real, checkable evidence. **Cap:** if the Active section already holds **8 or more untested** (`status: backlog`) ideas that are not `demand:proven`, append **at most 1** this run — the bottleneck is probing, not generation. Adding more assumed ideas to an unprobed pile is just hoarding.
6. Commit the updated `BACKLOG.md`, the new `pools/` file, and the updated `pools/seen.tsv` ledger. Message: `pipeline run <date>: +N candidates`. Open a PR per the cloud workflow.

In the PR summary (blunt, ≤5 sentences): list the new ids and one-liners, and flag if the backlog is filling with weak `demand:assumed` ideas — if so, say the screen should tighten or the engine's `worlds` list should widen.

Hard limits: do not build anything, do not deploy anything, do not create landing pages in this run. Output is backlog + audit trail only.
