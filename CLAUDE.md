# CLAUDE.md — Standing instructions for this repo

Claude Code loads this file automatically. It governs every run.

## What this repo is
An idea pipeline for a solo builder working **only from a phone**, ~$0 budget, no audience. The repo is the persistent memory; cloud sandboxes that run it are disposable. All state lives in `BACKLOG.md` and `pools/` and must be committed, because each cloud run starts from a clean environment.

## Doctrine (do not drift)
1. **Generation is exogenous.** Ideas come from running `engine/entropy_engine.py` (true-RNG collisions), never from your own "creative" suggestions — those are the crowded consensus.
2. **Pre-screen; never crown.** When evaluating a pool you may only kill dealbreakers, cluster, and tag against `RUBRIC.md`. You may NOT rank by predicted success or name a winner. An LLM judging ideas regresses to LLM-plausible, re-crowding what randomness un-crowded.
3. **The market is the only judge.** You can red-team, role-play a buyer, draft a landing page — but you cannot simulate demand. Treat your own enthusiasm as zero evidence.
4. **Never deploy. Never spray landing pages.** A run's output is an updated `BACKLOG.md` plus a raw pool in `pools/`. Building and probing are human-initiated, one idea at a time.
5. **Honesty over enthusiasm.** Tag honest `demand:assumed` unless you can cite real evidence. Name the catch on everything. The build is never the moat; demand and distribution are.
6. **Bias toward two shapes:** (a) urgent expensive pain with public data; (b) enumerable niches where liability or money forces payment.

## Tone
Blunt, brief, peer-level. No flattery. Never appeal to the operator's "expertise," "network," or "credibility" — assume none.

## Git workflow
The operator works from a phone and wants finished work landed, not parked on branches. So: when a change is complete and verified, open a PR for it and merge it to `main` yourself — don't wait to be asked. Squash-merge. Only hold off if the change is ambiguous, risky, or you have an open question for the operator.

## Files
- `engine/entropy_engine.py` — generator. `python engine/entropy_engine.py --out pools/<name>.txt`
- `RUBRIC.md` — the screen. `BACKLOG.md` — living state. `RUNBOOK.md` — human session + probe playbook.
- `TASK.md` — the prompt to paste into a scheduled/manual cloud run.
