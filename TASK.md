# TASK.md — One pipeline run

Paste this into a Claude Code on the web session pointed at this repo — or, to run it unattended on a schedule, paste the **Recurring routine prompt** at the bottom of this file into a Claude Code Routine (claude.ai/code/routines) with a Schedule trigger.

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

---

## Recurring routine prompt (paste into a Claude Code Routine)

This is the prompt to paste into a **Claude Code Routine** (claude.ai/code/routines),
so generation keeps moving while the operator is away. When creating the Routine:

- **Schedule trigger:** daily, **late evening / overnight in your local time** — keeps
  daytime quota free for normal chat; the run uses leftover overnight usage. Pick a
  non-:00 minute (runs stagger a few minutes).
- **Model selector:** **Sonnet** — the cost/quality sweet spot for rubric screening
  (~3× cheaper than Opus, so more runs per quota). Use **Haiku** if you want maximum
  volume and accept rougher screening; use Opus only if you want top-quality judgment.
  (Claude Code has no automatic per-task model router — the model is whatever you pick
  here for the whole run. Within a run you can still pin mechanical helper subagents to
  `haiku`; only the screen/develop judgment needs the routine's model.)

It runs unattended in the cloud; the ledger guarantees each run explores new ground.
(A cron job inside the sandbox would NOT work — the container is ephemeral. Use a
Routine.)

> Autonomous recurring development pass for this idea-pipeline repo. No human is
> present. Follow `CLAUDE.md` doctrine exactly. Do ONE focused pass, then stop.
>
> 1. Read `CLAUDE.md`, `STRATEGY.md`, `DEVELOP.md`, `RUBRIC.md`, and `BACKLOG.md`
>    (Active + Killed). Run `python engine/status.py`.
> 2. This invocation IS an explicit generation/development push — the assumed-idea
>    cap is lifted; the inbound screen is the only gate.
> 3. Generate, both with the ledger, and commit the pool files + updated ledger:
>    - `N=240 python engine/entropy_engine.py --out pools/pool_$(date +%Y%m%d_%H%M)_single.txt --ledger pools/seen.tsv`
>    - `N=100 python engine/entropy_engine.py --mode combine --out pools/pool_$(date +%Y%m%d_%H%M)_combine.txt --ledger pools/seen.tsv`
> 4. Develop survivors with `DEVELOP.md` techniques (recombine / vary / invert /
>    transpose / pick-and-shovel / JTBD). Every candidate must trace to a draw or
>    a real, citable pain — never free-float.
> 5. Screen hard against `RUBRIC.md`: the inbound-distribution kill (doctrine #7)
>    and the three-leg test (public data + a real payer + inbound search). Kill
>    dealbreakers. Do not rank, do not crown.
> 6. Append every genuine inbound survivor to `BACKLOG.md` Active (existing format;
>    honest tags; named catch; an inbound probe). `demand:assumed` unless you can
>    cite real evidence. **If the pass yields zero inbound survivors, append
>    nothing and say so — a zero-survivor pass is a success, not a failure.**
> 7. Append any system-level insight to `STRATEGY.md`'s Insight log; keep Current
>    phase accurate.
> 8. Run `python engine/test_entropy_engine.py` and `python engine/status.py` —
>    both must succeed.
> 9. Commit `BACKLOG.md`, the new `pools/` files, `pools/seen.tsv`, and
>    `STRATEGY.md`. Open a PR titled `scheduled dev pass <date>: +N candidates`
>    and, if tests pass and the diff is only backlog/pool/strategy/audit changes,
>    squash-merge it to `main` yourself (per `CLAUDE.md` git workflow).
> 10. Hard limits: never deploy, never create live landing pages, never cold
>    outreach, never crown, never rewrite engine logic in this run. Output is
>    backlog + audit trail only.
>
> Stop after one pass. The next run picks up where this one left off.
