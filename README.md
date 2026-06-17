# idea-pipeline

A phone-only idea pipeline. Exogenous randomness generates candidates, an LLM pre-screens them (filter, never crown), and a human runs cheap reality probes on the best one or two. The repo is the memory; cloud sandboxes are throwaway compute.

## Layout
```
idea-pipeline/
├── CLAUDE.md            # doctrine, auto-loaded by Claude Code
├── TASK.md              # the prompt for one pipeline run
├── RUBRIC.md            # the screen (filter + tags)
├── RUNBOOK.md           # human session guide + reality-probe playbook
├── BACKLOG.md           # living ranked state (committed every run)
├── engine/
│   └── entropy_engine.py
└── pools/               # raw generated pools (audit trail)
```

## Setup from a phone (no laptop needed)
1. **Make the repo.** On github.com (in your mobile browser, switch to "Desktop site" for an easier time), create a new repository, e.g. `idea-pipeline`.
2. **Add the files.** Use **Add file → Create new file**. To make a folder, just type the path in the filename box — e.g. `engine/entropy_engine.py` — and GitHub creates the folder for you. Paste each file's contents and commit. (Do this for `pools/.gitkeep` too so the empty folder exists.)
3. **Connect Claude Code on the web.** Open Claude Code on the web (research preview), connect your GitHub account, and select this repo. It runs in an Anthropic-managed cloud VM — nothing runs on your phone.
4. **Run a pass.** Paste `TASK.md` into a session. It generates a pool, screens it, appends survivors to `BACKLOG.md`, and opens a PR. Review the PR on your phone and merge.
5. **Automate (optional).** Set the same prompt as a scheduled remote routine so passes run while you're away. Each run is stateless — it reads the repo, writes back to the repo, and the VM is destroyed. That's why state must live here, not in the sandbox.

## What this does and doesn't do
- **Does:** keep a never-empty, deduped, screened backlog of uncrowded candidates with honest tags and a suggested probe for each.
- **Doesn't:** decide what will work, build products, or deploy anything. Those are human moves. The only real test of an idea is a cheap probe against real people — see `RUNBOOK.md`.

## The loop in one line
generate (random) → dedupe → pre-screen + tag → *you* pick 1–2 → *you* probe reality → log the signal → repeat.
