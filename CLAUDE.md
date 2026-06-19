# CLAUDE.md — Standing instructions for this repo

Claude Code loads this file automatically. It governs every run.

## What this repo is
An idea pipeline for a solo builder working **only from a phone**, ~$0 budget, no audience, and **no cold outreach** (the operator will not cold-email, DM, call, or do 1:1 selling — see doctrine #7). The repo is the persistent memory; cloud sandboxes that run it are disposable. All state lives in `BACKLOG.md` and `pools/` and must be committed, because each cloud run starts from a clean environment.

## Doctrine (do not drift)
1. **Generation is exogenous; development must stay anchored.** New ideas start from running `engine/entropy_engine.py` (true-RNG collisions), never from free-floating "what's a good startup" ideation — that lands on the crowded consensus the randomness exists to escape. You *may* develop draws at volume — recombine (`--mode combine`), vary, invert, transpose — but every developed idea must trace back to an **exogenous draw** or a **real, citable pain** (see `DEVELOP.md`). Anchored, not invented.
2. **Pre-screen; never crown.** When evaluating a pool you may only kill dealbreakers, cluster, and tag against `RUBRIC.md`. You may NOT rank by predicted success or name a winner. An LLM judging ideas regresses to LLM-plausible, re-crowding what randomness un-crowded.
3. **The market is the only judge.** You can red-team, role-play a buyer, draft a landing page — but you cannot simulate demand. Treat your own enthusiasm as zero evidence.
4. **Never deploy. Never spray landing pages.** A run's output is an updated `BACKLOG.md` plus a raw pool in `pools/`. Building and probing are human-initiated, one idea at a time.
5. **Honesty over enthusiasm.** Tag honest `demand:assumed` unless you can cite real evidence. Name the catch on everything. The build is never the moat; demand and distribution are.
6. **Bias toward two shapes:** (a) urgent expensive pain with public data; (b) enumerable niches where liability or money forces payment — **but only if the niche is also inbound-reachable** (they search for the pain or gather where you can post once). An enumerable niche reachable *only* by cold-emailing it one shop at a time is dead on distribution here (see #7).
7. **No cold outreach; distribution must be inbound.** The operator does near-zero human interaction to acquire customers: no cold email/DM/calls, no sales conversations. Viable distribution is inbound/self-serve — search/SEO, a landing page, a paid ad, a marketplace, or a single broadcast post. An idea whose only customer-acquisition path is outreach is a dealbreaker, however good the build. Distribution is the binding constraint; screen for it as hard as for demand.

## Tone
Blunt, brief, peer-level. No flattery. Never appeal to the operator's "expertise," "network," or "credibility" — assume none.

## Git workflow
The operator works from a phone and wants finished work landed, not parked on branches and not sitting as an unpushed local diff. So:
- **Always commit and push without asking.** The moment a change is complete and verified, commit it and push it. Never end a turn with completed work uncommitted or unpushed, and never ask "want me to push?" — just push. A large diff left local is a bug.
- **Open the PR and squash-merge to `main` yourself** — don't wait to be asked.
- Only hold off if the change is genuinely ambiguous, risky, or you have an open question for the operator. Even then, commit and push the work to the branch first; the open question is about merging, not about whether to push.
- **Reset the dev branch to `main` after every squash-merge.** Squash-merging collapses the branch's commits into one new commit on `main`, but the local branch keeps the *originals* — stack the next change on top and the next PR hits phantom merge conflicts. So immediately after a merge: `git fetch origin main && git reset --hard origin/main`, then force-push the branch, so the next change starts clean from `main`. (Learned the hard way 2026-06-19: two PRs needed rebase gymnastics because the branch carried pre-squash history.)

## Files
- `STRATEGY.md` — central planning & strategy: current phase, standing decisions, and the append-only insight log. Read it first; update its insight log when a run learns something about the *system* (not just an idea).
- `engine/entropy_engine.py` — generator. `python engine/entropy_engine.py --out pools/<name>.txt --ledger pools/seen.tsv` (add `--mode combine` to collide two worlds).
- `DEVELOP.md` — the idea-development playbook: how to turn draws + real pains into more candidates at volume without regressing to consensus.
- `engine/status.py` — dashboard: space burn-down + backlog composition. `python engine/status.py`
- `RUBRIC.md` — the screen. `BACKLOG.md` — living state. `RUNBOOK.md` — human session + probe playbook.
- `probes/` — drafted probe assets (copy only; the operator ships them). `TASK.md` — the prompt to paste into a scheduled/manual cloud run.
