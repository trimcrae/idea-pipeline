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

**The meta-layer lives in `STRATEGY.md`.** `BACKLOG.md` is the ideas; `STRATEGY.md` is the state of the loop — current phase, standing decisions, and the insight log. Drafted probe assets (landing-page copy, community-post copy, ad copy — all inbound) live in `probes/` as copy only; you ship them, the model doesn't.

## Reality-probe playbook (cheap, fast, real — inbound only)
The operator does **no cold outreach** (CLAUDE.md #7). Every probe must pull the
customer in, not chase them. Pick the lightest one:
- **Landing page** describing the thing as if it exists, with a single "notify me / sign up" button. Count sign-ups. (The base of every probe.)
- **One broadcast post** — a single honest post in the subreddit/forum/Discord where the niche already gathers, pointing at the page. Post once; don't run a sales thread. Count clicks + sign-ups.
- **Intent search / SEO** — a free single-purpose tool or page targeting what the niche already googles; let it rank/get found. Best for `reach:searchable` ideas.
- **Tiny ad** (a few dollars) — point a small spend at the landing page on the niche's search/interest terms; measure click-through + sign-ups.
- **Not allowed:** cold emails, DMs, or calls to named prospects; any probe whose result depends on the operator working a 1:1 conversation.
A probe "passes" only on real self-serve action (sign-up, pre-order, click-through) — never on compliments. **Bar: ≥10 self-serve sign-ups from one low-effort push** (see `STRATEGY.md` → Probe pass bar).

## The product line (since 2026-09-12)
The weekly public-records feeds are the pipeline's live product: `engine/feeds/`
builds them, `.github/workflows/feeds.yml` runs every Monday, the site is
https://trimcrae.github.io/idea-pipeline/. The operator's only jobs are in
`OPERATOR.md` (paste a Stripe key; optionally Search Console). The model's
recurring jobs are the SELL-phase prompt in `TASK.md`: keep the build green,
add feeds through the probe → registry → screen path, kill feeds nobody
downloads. Full files for subscribers live on the `feeds-data` branch and are
decrypted in the buyer's browser with the key from Stripe's redirect.

## Do not
- Treat the model's enthusiasm as evidence.
- Skip the probe and go straight to building — a feed's probe is its free beta.
- Add data about private individuals to any feed (D15).

## Where you work
- **Generation + screening:** automated via `TASK.md` in Claude Code on the web (cloud, phone-driven). Reads this repo, writes survivors back to `BACKLOG.md`, opens a PR.
- **Probing + deciding:** yours, always. The model builds the test asset; you ship it and read the real signal. No automation removes this step.
- **State:** lives in the repo (`BACKLOG.md`, `pools/`), never in the disposable cloud VM.
