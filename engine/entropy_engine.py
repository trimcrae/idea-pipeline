#!/usr/bin/env python3
"""Exogenous-entropy idea engine v2 — wider worlds, bigger pool.

Usage:
  python entropy_engine.py                 # fresh random pool of N (default 180)
  python entropy_engine.py 12345           # reproduce a specific seed
  python entropy_engine.py --out pool.txt   # also write the pool to a file
  N=300 python entropy_engine.py            # override pool size via env var
The randomness is from os.urandom (true system entropy), not the model.
"""
import random, os, sys

# First positional arg that is a plain integer is treated as the seed.
_seed_arg = next((a for a in sys.argv[1:] if a.lstrip("-").isdigit() and not a.startswith("--")), None)
seed = int(_seed_arg) if _seed_arg else int.from_bytes(os.urandom(8), "big")
rng = random.Random(seed)

# WORLDS — heavily expanded. Mix of: passionate-spend hobbies, small-business /
# supply-side, regulatory/professional edges, life-event logistics. Money and
# supply side over-weighted because that's where willingness-to-pay concentrates.
worlds = [
 # passionate hobbyist spend
 "competitive bird photography","small-batch cheesemaking","vintage synth collectors",
 "tabletop miniature painters","rare houseplant traders","reef-tank aquarists",
 "model railroad builders","amateur astronomers","bonsai growers","pinball restorers",
 "mechanical keyboard builders","fountain pen collectors","vinyl record diggers",
 "competitive jigsaw puzzlers","disc golfers","metal detectorists","drone racers",
 "saltwater fly fishers","ultralight backpackers","home roasters","mushroom cultivators",
 "historical reenactors","cosplay armor makers","tarot deck collectors","watch modders",
 "competitive memory athletes","speedcubers","escape-room designers","airsoft milsim teams",
 "homebrew brewers","kombucha brewers","aquascapers","carnivorous plant growers",
 # small business / supply side
 "specialty coffee roasters","independent bookstore owners","mobile dog groomers",
 "food-truck operators","estate-sale companies","small-farm CSA operators",
 "indie tattoo studios","luthiers / instrument repair","antique clock restorers",
 "knife sharpeners","upholstery shops","picture framers","sign painters",
 "small commercial beekeepers","microgreens growers","cottage bakers","cidermakers",
 "small distilleries","pottery studios","letterpress printers","taxidermists",
 "boat detailers","pool-service operators","window cleaners","chimney sweeps",
 "junk-removal operators","mobile notaries","process servers","bail bondsmen",
 "self-storage facility owners","laundromat owners","vending-machine operators",
 "ATM route operators","car-wash owners","sober-living home operators",
 # regulatory / professional edges
 "long-haul truckers","commercial drone pilots","ham radio operators",
 "private pilots","scuba dive operators","commercial fishers","beekeeping inspectors",
 "home inspectors","septic installers","well drillers","asbestos abatement crews",
 "wildland firefighters","arborists","pest-control techs","locksmiths",
 "court reporters","freelance paralegals","medical billers","dental lab techs",
 "veterinary practice managers","funeral home directors","cemetery operators",
 "wedding officiants","immigration paralegals","patent illustrators","actuary students",
 # life-event / logistics / under-tooled
 "estate executors","caregivers for aging parents","NICU parents","hospice families",
 "people selling a deceased relative's collection","competitive youth sports parents",
 "RV full-timers","van-lifers","liveaboard sailors","off-grid homesteaders",
 "expat retirees","cross-border commuters","traveling nurses","oil-rig rotation workers",
 "competitive eaters","whisky cask investors","watch flippers","sneaker resellers",
 "Lego set investors","trading-card graders","coin roll hunters","scrap metal haulers",
 "freight dispatchers","owner-operator truckers","import/export small brokers",
 "Etsy sellers in one craft","Amazon FBA resellers","livestock auction buyers",
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

def draw():
    return (rng.choice(worlds), rng.choice(forms), rng.choice(twists), rng.choice(wildcards))

N = int(os.environ.get("N", "180"))
# A draw is unique on (world, form, twist); cap N at that space so an
# over-large N (or a trimmed list) can't spin the dedup loop forever.
unique_space = len(worlds) * len(forms) * len(twists)
if N > unique_space:
    print(f"[N={N} exceeds unique space {unique_space:,}; capping]", file=sys.stderr)
    N = unique_space
seen=set(); out=[]
while len(out) < N:
    w,f,t,wc = draw()
    key=(w,f,t)
    if key in seen: continue
    seen.add(key); out.append((w,f,t,wc))

header = f"seed={seed}  worlds={len(worlds)} forms={len(forms)} twists={len(twists)}  space={len(worlds)*len(forms)*len(twists):,}\n"
lines = [f"{i:>3}. {f} for {w} — {t}.  [{wc}]" for i,(w,f,t,wc) in enumerate(out,1)]
text = header + "\n".join(lines) + "\n"
print(text, end="")

# Optional: write the raw pool to a file for the audit trail (--out PATH)
if "--out" in sys.argv:
    path = sys.argv[sys.argv.index("--out") + 1]
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)
    print(f"\n[wrote pool to {path}]")
