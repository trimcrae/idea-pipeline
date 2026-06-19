#!/usr/bin/env python3
"""Exogenous-entropy idea engine v2 — wider worlds, bigger pool.

Usage:
  python entropy_engine.py                 # fresh random pool of N (default 180)
  python entropy_engine.py 12345           # reproduce a specific seed
  python entropy_engine.py --out pool.txt   # also write the pool to a file
  python entropy_engine.py --ledger pools/seen.tsv   # never re-draw a past combo
  python entropy_engine.py --mode combine   # collide TWO worlds (cross-niche transfer)
  N=300 python entropy_engine.py            # override pool size via env var
The randomness is from os.urandom (true system entropy), not the model.

The --ledger flag gives the engine cross-run memory: it loads every
(world, form, twist) combination already drawn in past runs, excludes them
from this pool, then appends the new ones back. This makes the pipeline's
"discard draws already seen" step machine-enforced instead of a manual
eyeball — important because each cloud run starts from a clean VM, so the
only memory is what's committed to the repo. Excluding past draws is pure
de-duplication; the randomness is still exogenous (os.urandom), so this does
not bias generation toward LLM-plausible ideas.

STEERING vs. randomness (doctrine #1, STRATEGY D12). The only exogenous-random
step is the COLLISION — which (world, form, twist) os.urandom happens to pick.
The vocabularies below are NOT random: they are a curated, deliberately weighted
*substrate*, tilted toward the structure that empirically survives the screen —
a payer with money/liability + PUBLIC (free) data + INBOUND search (the three
legs; see STRATEGY insight 2026-06-18). Tilting the urn raises the survivor
base-rate without predicting which idea wins: the collision stays unpredictable,
and the explicit WILDCARD tier keeps weird, low-base-rate worlds in play so draws
remain non-obvious and anti-consensus. This is substrate hygiene like the
ledger, NOT crowning. Curate by *structure* (who pays, is the data free, do they
search) — never toward a specific idea or market consensus.
"""
import random, os, sys


def _flag(name):
    """Return the value following --name on the command line, or None."""
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def load_ledger(path):
    """Load already-drawn (world, form, twist) keys from a TSV ledger.

    Missing file = empty ledger (first run). Blank/short lines are skipped so a
    hand-edited or partially written ledger can't crash a run."""
    keys = set()
    if not path or not os.path.exists(path):
        return keys
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3 and all(parts):
                keys.add(tuple(parts))
    return keys


def append_ledger(path, keys):
    """Append newly drawn keys to the TSV ledger, creating parent dirs."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "a") as fh:
        for w, f, t in keys:
            fh.write(f"{w}\t{f}\t{t}\n")

# WORLDS — a curated, deliberately weighted substrate (NOT random; see the
# docstring's "STEERING vs. randomness"). Tilted toward the two structures that
# empirically survive the screen — regulated/licensed operators who search their
# own compliance pain, and verification-before-an-expensive-buy markets — both of
# which tend to have the three legs (money/liability payer + free public data +
# inbound search). Pruned the worlds that only ever produced dead ideas under the
# rules: cold-outreach-only enumerable niches (dive shops, abatement crews,
# bondsmen, dental labs — all killed) and passion-without-money hobbies with no
# payer and no public data. A WILDCARD tier is kept on purpose (group F).
worlds = [
 # --- A. regulated / licensed small operators: public rules, they SEARCH the
 #     compliance pain, money/liability forces payment (the proven
 #     "compliance-navigator" engine). Bias factual deadlines/permits/registration
 #     over judgment — information, not advice (doctrine #8).
 "long-haul truckers","owner-operator truckers","freight dispatchers",
 "import/export small brokers","customs brokers","freight forwarders",
 "DOT-regulated fleet operators","commercial drone pilots","private pilots",
 "home inspectors","septic installers","well drillers","arborists",
 "pest-control techs","locksmiths","commercial fishers","wildland firefighters",
 "court reporters","freelance paralegals","immigration paralegals","medical billers",
 "mobile notaries","loan-signing notaries","process servers","wedding officiants",
 "funeral home directors","cemetery operators","veterinary practice managers",
 "short-term-rental hosts","food-truck operators","cottage bakers","small distilleries",
 "cidermakers","small commercial beekeepers","tax preparers / enrolled agents",
 "licensed childcare / daycare operators","solar installers","EV-charger installers",
 "general contractors pulling permits","HOA / community-association managers",
 "self-storage facility owners","laundromat owners","car-wash owners",
 "vending-machine operators","ATM route operators","sober-living home operators",
 # --- B. pre-purchase / pre-transaction VERIFICATION of an expensive thing:
 #     buyer pays per-check on a big spend, the data is public-ish, they SEARCH
 #     "how do I not get burned" (the proven "verification" engine).
 "used heavy-equipment buyers","used farm-equipment buyers","used-RV buyers",
 "used-boat buyers","powersports / ATV buyers","classic-car buyers",
 "used-camera-gear buyers","horse buyers","breeding-dog buyers","domain-name buyers",
 "used-restaurant-equipment buyers","whisky cask investors","watch flippers",
 "watch modders","sneaker resellers","trading-card graders","comic-book graders",
 "vintage synth collectors","vintage-guitar flippers","luxury-handbag resellers",
 "Lego set investors","coin roll hunters","estate executors",
 "people selling a deceased relative's collection","estate-sale companies",
 "scrap metal haulers","livestock auction buyers",
 # --- C. moneyed / supplied hobbies: proven spend, reachable inbound in their
 #     own communities; the SUPPLIERS are a payer when the hobbyist isn't.
 "rare houseplant traders","reef-tank aquarists","carnivorous plant growers",
 "mushroom cultivators","home roasters","homebrewers","kombucha brewers",
 "mechanical keyboard builders","fountain pen collectors","vinyl record diggers",
 "tabletop miniature painters","model railroad builders","amateur astronomers",
 "bonsai growers","pinball restorers","drone racers","saltwater fly fishers",
 "metal detectorists","tarot deck collectors","competitive bird photography",
 "cosplay armor makers","historical reenactors",
 # --- D. small supply-side trades & services: a business pays; many carry
 #     liability / licensing / public-data hooks.
 "specialty coffee roasters","independent bookstore owners","mobile dog groomers",
 "small-farm CSA operators","indie tattoo studios","luthiers / instrument repair",
 "antique clock restorers","knife sharpeners","upholstery shops","picture framers",
 "sign painters","microgreens growers","pottery studios","letterpress printers",
 "taxidermists","boat detailers","pool-service operators","window cleaners",
 "chimney sweeps","junk-removal operators",
 # --- E. life-event / under-tooled logistics: acute, searchable pain; the payer
 #     leg is the weak one here — screen it hard.
 "caregivers for aging parents","hospice families","NICU parents",
 "competitive youth sports parents","RV full-timers","van-lifers","liveaboard sailors",
 "off-grid homesteaders","expat retirees","cross-border commuters","traveling nurses",
 "oil-rig rotation workers","Etsy sellers in one craft","Amazon FBA resellers",
 # --- F. WILDCARD / long-shot: deliberately weird, low-base-rate worlds kept IN
 #     the urn so collisions stay non-obvious and anti-consensus (doctrine #1).
 #     Do NOT prune these for "looking unpromising" — that's exactly the point.
 "ham radio operators","competitive memory athletes","speedcubers",
 "escape-room designers","ultralight backpackers","aquascapers","disc golfers",
 "airsoft milsim teams",
]

forms = [
 "a single-purpose calculator","a curated auto-updating directory","a converter",
 "a constraint-checker / validator","a monitoring + alert service","an aggregator",
 "a one-email-in / one-email-out bot","a browser extension","a template / preset pack",
 "a tiny public dataset","a comparison explorer","a 'is it worth it' estimator",
 "a printable generator","a search engine for one narrow thing","an availability tracker",
 "a price/condition tracker","a compatibility matrix","a deadline/season reminder",
 "a 'find the nearest X' map","an anomaly flagger","a naming/ID/serial decoder",
 "a swap/match board","a checklist generator","a unit/format translator",
 "a restock alerter","a fee/cost auditor","a counterfeit/fake detector",
 "a 'what's this worth' appraiser","a route/sequence optimizer","a recall/notice watcher",
 "a lightweight CRM for one workflow","a quote/estimate generator",
]

twists = [
 "works fully offline","targets the 5 minutes RIGHT BEFORE the activity",
 "for people who actively hate the incumbent tool","combines two unrelated data sources",
 "does the reverse of what every existing tool does","operates entirely over SMS/email",
 "uses a constraint everyone else ignores","serves the SUPPLIERS, not the hobbyists",
 "only does the one step everything else skips","is intentionally read-only / no accounts",
 "exploits a rule/regulation deadline","monetizes the data exhaust, not the tool",
 "targets the moment something breaks / fails","is for the spouse/parent/heir of the enthusiast",
 "works from a single photo as input","focuses on end-of-life / disposal / resale",
 "is built for one specific region first","surfaces what's secretly out of stock everywhere",
 "catches the expensive mistake before it's made","translates pro jargon for newcomers",
 "tracks a thing that only matters seasonally","is the 'should I even bother' gate",
 "aggregates what's scattered across 20 forums","watches prices across closed/auction markets",
 "is a verification layer for a trust-poor market","does the boring compliance nobody wants",
]

wildcards = ["tide tables","expiration dates","seating charts","weather fronts","serial numbers",
 "postal codes","moon phases","warranty windows","grading scales","shipping containers",
 "color codes","frequencies","auction lots","migration patterns","tax deadlines","VIN numbers",
 "batch numbers","license classes","grading rubrics","blackout dates","lot numbers","watermarks"]

def draw(rng):
    return (rng.choice(worlds), rng.choice(forms), rng.choice(twists), rng.choice(wildcards))


def draw_combine(rng):
    """Collide TWO different worlds — a cross-niche transfer ('a tool that serves
    both X and Y'). Worlds are sorted so (X,Y) and (Y,X) are the same idea."""
    a = rng.choice(worlds)
    b = rng.choice(worlds)
    while b == a:
        b = rng.choice(worlds)
    lo, hi = sorted((a, b))
    return (lo, hi, rng.choice(forms), rng.choice(twists), rng.choice(wildcards))


def unique_space(mode="single"):
    """Distinct combinations the engine can emit in a given mode."""
    W, F, T = len(worlds), len(forms), len(twists)
    if mode == "combine":
        return (W * (W - 1) // 2) * F * T   # unordered world pairs
    return W * F * T


def main():
    # First positional arg that is a plain integer is treated as the seed.
    seed_arg = next((a for a in sys.argv[1:] if a.lstrip("-").isdigit() and not a.startswith("--")), None)
    seed = int(seed_arg) if seed_arg else int.from_bytes(os.urandom(8), "big")
    rng = random.Random(seed)

    mode = (_flag("--mode") or "single").lower()   # "single" (default) or "combine"
    N = int(os.environ.get("N", "180"))
    # A draw is unique on its key; cap N at the space still available so an
    # over-large N (or a near-exhausted ledger) can't spin the loop forever.
    space = unique_space(mode)
    ledger_path = _flag("--ledger")
    seen = load_ledger(ledger_path)          # past-run keys to exclude (empty if no ledger)
    remaining = space - len(seen)
    if N > remaining:
        print(f"[N={N} exceeds remaining unique space {remaining:,} "
              f"(ledger holds {len(seen):,}); capping]", file=sys.stderr)
        N = max(remaining, 0)
    new_keys = []; out = []
    while len(out) < N:
        if mode == "combine":
            a,b,f,t,wc = draw_combine(rng)
            key = (f"{a} + {b}", f, t)       # ledger col 1 holds the world pair
            line_body = f"{f} serving BOTH {a} AND {b} — {t}.  [{wc}]"
        else:
            w,f,t,wc = draw(rng)
            key = (w, f, t)
            line_body = f"{f} for {w} — {t}.  [{wc}]"
        if key in seen: continue
        seen.add(key); new_keys.append(key); out.append(line_body)

    header = (f"seed={seed}  mode={mode}  worlds={len(worlds)} forms={len(forms)} "
              f"twists={len(twists)}  space={space:,}\n")
    lines = [f"{i:>3}. {body}" for i, body in enumerate(out, 1)]
    text = header + "\n".join(lines) + "\n"
    print(text, end="")

    # Optional: write the raw pool to a file for the audit trail (--out PATH)
    out_path = _flag("--out")
    if out_path:
        parent = os.path.dirname(out_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(out_path, "w") as fh:
            fh.write(text)
        print(f"\n[wrote pool to {out_path}]")

    # Record this run's new keys so future runs never re-surface them (--ledger PATH).
    if ledger_path:
        append_ledger(ledger_path, new_keys)
        print(f"[ledger {ledger_path}: +{len(new_keys)} keys, {len(seen)} total]")


if __name__ == "__main__":
    main()
