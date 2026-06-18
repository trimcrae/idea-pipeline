# idea-pipeline

A phone-only idea pipeline. Exogenous randomness generates candidates, an LLM pre-screens them (filter, never crown), and a human runs cheap reality probes on the best one or two. The repo is the memory; cloud sandboxes are throwaway compute.

## Layout
```
idea-pipeline/
├── CLAUDE.md            # doctrine, auto-loaded by Claude Code
├── STRATEGY.md          # central planning & strategy: phase, decisions, insight log
├── DEVELOP.md           # idea-development playbook (variants, recombination, transposition)
├── TASK.md              # the prompt for one pipeline run
├── RUBRIC.md            # the screen (filter + tags)
├── RUNBOOK.md           # human session guide + reality-probe playbook
├── BACKLOG.md           # living ranked state (committed every run)
├── probes/              # drafted probe assets (copy only; operator ships them)
├── engine/
│   ├── entropy_engine.py
│   ├── status.py                # dashboard: python engine/status.py (space burn-down + backlog mix)
│   └── test_entropy_engine.py   # smoke tests (no deps): python engine/test_entropy_engine.py
└── pools/               # raw generated pools (audit trail)
    └── seen.tsv         # ledger of every (world,form,twist) ever drawn — cross-run dedup
```

## Setup from a phone (no laptop needed)
1. **Make the repo.** On github.com (in your mobile browser, switch to "Desktop site" for an easier time), create a new repository, e.g. `idea-pipeline`.
2. **Add the files.** Use **Add file → Create new file**. To make a folder, just type the path in the filename box — e.g. `engine/entropy_engine.py` — and GitHub creates the folder for you. Paste each file's contents and commit. (Do this for `pools/.gitkeep` too so the empty folder exists.)
3. **Connect Claude Code on the web.** Open Claude Code on the web (research preview), connect your GitHub account, and select this repo. It runs in an Anthropic-managed cloud VM — nothing runs on your phone.
4. **Run a pass.** Paste `TASK.md` into a session. It generates a pool, screens it, appends survivors to `BACKLOG.md`, and opens a PR. Review the PR on your phone and merge.
5. **Automate (recommended).** Create a **Claude Code Routine** at [claude.ai/code/routines](https://claude.ai/code/routines), point it at this repo, add a **Schedule** trigger set to **daily, late evening / overnight in your local time** (so your daytime quota stays free for normal chat and the pipeline burns leftover usage overnight — pick a non-:00 minute since runs stagger a few minutes), and paste the **Recurring routine prompt** from the bottom of `TASK.md`. It runs unattended in the cloud on your account's usage quota — no need to sit in the app or wait out a phone rate limit. Each run is stateless (reads the repo, writes back, VM is destroyed), so state must live here; the `pools/seen.tsv` ledger is what stops runs from repeating. Note: a cron job inside the sandbox would NOT persist (the container is ephemeral) — use a Routine. "Claude Dispatch" is a separate feature (hand a task to Claude from your phone), not scheduling.

## What this does and doesn't do
- **Does:** keep a never-empty, deduped, screened backlog of uncrowded candidates with honest tags and a suggested probe for each.
- **Doesn't:** decide what will work, build products, or deploy anything. Those are human moves. The only real test of an idea is a cheap probe against real people — see `RUNBOOK.md`.

## The loop in one line
generate (random) → dedupe → pre-screen + tag → *you* pick 1–2 → *you* probe reality → log the signal → repeat.
