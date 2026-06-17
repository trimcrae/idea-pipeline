# RUBRIC.md — The Screen

This is a **filter and tagger**, not a success predictor. Use it to triage a raw pool down to a shortlist worth a human look. It cannot tell you what will work — only the market can.

## Kill criteria (auto-reject; do not pass to shortlist)
- No one plausibly pays or no acute recurring pain ("nice-to-have for hobbyists who won't pay").
- Requires a large diffuse audience to find it (operator has none).
- Needs ongoing human support per customer (operator can't staff that).
- Needs meaningful upfront capital or inventory.
- Sits squarely on top of a funded incumbent with no price/simplicity wedge underneath.
- Legally or ethically fraught, or requires licenses the operator lacks.

## The five tests (a survivor should pass most, strongly)
1. **Demand signal** — proven willingness to pay, OR acute/expensive pain. Prefer evidence (real data, surveys, visible spend) over assumption. Tag: `demand:proven` / `demand:assumed`.
2. **Uncrowded** — would 1,000 people prompting an LLM land here? If yes, drop it. Tag: `crowd:low/med/high`.
3. **Solo-buildable** — one person + an LLM can ship a v1; thin layer over public data or a single clear function. Tag: `build:easy/med/hard`.
4. **Findable without an audience** — reachable via narrow search, one post where the niche gathers, or (best) an enumerable, cold-emailable customer list. Tag: `reach:enumerable/searchable/diffuse`.
5. **Maintenance an agent can absorb** — upkeep is re-pulling data / re-running rules, not bespoke human judgment. Tag: `maint:auto/manual`.

## The two winning shapes (bias toward these)
- **Pain + public data:** urgent, expensive problem where the needed data is publicly available (regulatory, fraud, compliance, deadlines).
- **Enumerable + forced payment:** small niche whose entire customer list is reachable by hand, where liability or money makes paying non-optional.

## Output format when screening a pool
For each survivor: one-line concept · shape · tags · demand evidence (or "assumed") · the honest catch · a candidate next probe. Then stop. Do not pick the winner — hand the shortlist to the operator.
