# TASK.md — One pipeline run

Paste this into a Claude Code on the web session pointed at this repo — or, to run it unattended on a schedule, paste the **Recurring routine prompt** at the bottom of this file into a Claude Code Routine (claude.ai/code/routines) with a Schedule trigger.

---

Run one pass of the idea pipeline. Follow `CLAUDE.md` doctrine strictly.

0. Read `STRATEGY.md` and run `python engine/status.py`. If the current phase is PROBE (or status warns that most untested ideas are not `demand:proven` and none are probed), the bottleneck is probing, not generation — do the minimum here: add at most 1 idea, or skip appending entirely, and say so. Do not pad the backlog.
1. Read `CLAUDE.md`, `RUBRIC.md`, and the current `BACKLOG.md` (both Active and Killed sections).
2. Generate a fresh pool: `python engine/entropy_engine.py --out pools/pool_$(date +%Y%m%d_%H%M).txt --ledger pools/seen.tsv`. Keep the printed seed. The `--ledger` flag makes the engine skip every (world, form, twist) it has emitted in a past run, so the pool is already deduped against history — commit the updated `pools/seen.tsv` alongside the pool. For a deeper pass, also generate a collision pool with `--mode combine` and develop survivors per `DEVELOP.md` (recombine / vary / invert / transpose — anchored, never free-floating).
3. The engine has handled combination-level dedup. Still discard any draw whose idea is substantively the same as something already in `BACKLOG.md` (Active or Killed), even if the exact triple differs.
4. Screen the rest with `RUBRIC.md`: apply the kill criteria (including the inbound-distribution kill #7, the no-licensed-professional-advice kill #8, and the $0 build-cost kill #9 — v1 must run on free public data + free tiers), cluster near-duplicates, and tag survivors. Do **not** rank by predicted success and do **not** pick a winner.
5. Append the strongest survivors to the **Active** section of `BACKLOG.md`, using the existing entry format (id · concept · shape · tags · demand · catch · next probe · status: backlog). Use `demand:assumed` unless you can cite real, checkable evidence. **Cap:** if the Active section already holds **8 or more untested** (`status: backlog`) ideas that are not `demand:proven`, append **at most 1** this run — adding more assumed ideas to an unprobed pile is hoarding. **Exception:** when the operator explicitly requests a generation/development push, the cap is lifted and the only gate is the inbound screen (RUBRIC) — append every genuine inbound survivor, but never pad with `crowd:high` consensus ideas to hit a count.
6. If this run learned anything about the *system* (not just an idea) — the screen letting through noise, a world that's over/under-sampled, the backlog stalling at the probe step — append it to `STRATEGY.md`'s Insight log and adjust the Current phase if it changed.
7. Commit the updated `BACKLOG.md`, the new `pools/` file, the updated `pools/seen.tsv` ledger, and `STRATEGY.md` if touched. Message: `pipeline run <date>: +N candidates`. Open a PR per the cloud workflow.

In the PR summary (blunt, ≤5 sentences): list the new ids and one-liners, and flag if the backlog is filling with weak `demand:assumed` ideas — if so, say the screen should tighten or the engine's `worlds` list should widen.

Hard limits for a *generation* run: do not touch `engine/feeds/` or the site; output is backlog + audit trail only. (The product line has its own recurring prompt below.)

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

> Autonomous recurring pass for this idea-pipeline repo (SELL phase, doctrine
> #10). No human is present. Follow `CLAUDE.md` exactly. Do ONE focused pass,
> then stop. Work on the dev branch, open a PR, squash-merge it yourself when
> tests pass, then reset the branch to `main` (CLAUDE.md git workflow).
>
> 1. Read `CLAUDE.md`, `STRATEGY.md`, `OPERATOR.md`, `RUBRIC.md`, `BACKLOG.md`,
>    `engine/feeds/registry.py`, and `feeds/build.json`. Run `python engine/status.py`.
> 2. **Keep the product alive first.** Check the latest `feeds` workflow run on
>    GitHub Actions (the GitHub tools can list runs and read job logs). If it is
>    red, or a feed shows 0 rows two weeks running, or `feeds/build.json` lists a
>    failure: diagnose it with the probe job (edit `engine/feeds/probe_queries.json`,
>    push, read the log), fix the registry entry, and re-run the workflow. The
>    sandbox cannot reach the portals itself — Actions runners can.
> 3. **Grow the catalogue by at most 2 feeds per pass.** A feed is (a public
>    registry that publishes new entrants daily, on a free keyless portal) × (a
>    vendor class that provably buys such lists). Anchor it to a drawn world or a
>    citable vendor market; screen it with `RUBRIC.md` (#7 inbound, #8 information
>    not advice, #9 $0, three legs) and D15 (**businesses and licensed premises
>    only — never private individuals; drop personal-name/contact columns**).
>    Probe the dataset first (columns, date field, weekly count ≥ ~20), then add
>    the entry, run `python engine/feeds/test_feeds.py`, push, and read the
>    `feeds` run log. Zero viable candidates is a fine outcome — say so.
> 4. **Read the market, never crown.** From `PROBE-PAGES.md` counters (if
>    reachable) or the Stripe dashboard notes the operator leaves: note downloads
>    / subscriptions per feed in `BACKLOG.md`'s probe log. Kill any feed with 0
>    downloads after 8 live weeks (remove it from the registry; log why).
> 5. **Generation stays on, at low volume, as substrate:** every 3rd pass run
>    `N=120 python engine/entropy_engine.py --out pools/pool_$(date +%Y%m%d_%H%M).txt --ledger pools/seen.tsv`,
>    skim for registry-shaped worlds (a licensing/permit/inspection body that
>    publishes data), and treat survivors as feed candidates for step 3. Commit
>    the pool + ledger.
> 6. Append any system-level insight to `STRATEGY.md`'s log; keep Current phase
>    accurate; keep `OPERATOR.md` truthful about what is and isn't switched on.
> 7. Run `python engine/feeds/test_feeds.py`, `python engine/feeds/test_stripe_links.py`,
>    `python engine/test_entropy_engine.py`, `python engine/build_pages.py`,
>    `python engine/status.py` — all must succeed before the PR.
> 8. Hard limits: never spend money; never add data about private individuals;
>    never cold-outreach anyone; never crown; never rotate or print secrets;
>    never rewrite `engine/feeds/feedcrypto.py` or the payment-link logic
>    without a test proving the old links still resolve.
>
> Stop after one pass. The next run picks up where this one left off.
