#!/usr/bin/env python3
"""Pipeline status — coverage of the combination space + backlog composition.

Run: python engine/status.py
No deps, no network. Reads pools/seen.tsv (the dedup ledger) and BACKLOG.md.

This exists to support one recurring decision (see RUBRIC.md / TASK.md): when
the backlog fills with unproven `demand:assumed` ideas, the screen should
tighten or the engine's `worlds` list should widen. A glance at the numbers
here tells you which — it does not rank ideas or pick a winner.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(ROOT, "pools", "seen.tsv")
BACKLOG = os.path.join(ROOT, "BACKLOG.md")

sys.path.insert(0, HERE)
import entropy_engine as engine  # import-safe: importing does not generate a pool


def ledger_count(path=LEDGER):
    if not os.path.exists(path):
        return 0
    with open(path) as fh:
        return sum(1 for line in fh if line.strip())


def parse_backlog(path=BACKLOG):
    """Return (active_entries, killed_count). Each active entry is a dict with
    its status and demand tag, parsed from the entry's text block."""
    if not os.path.exists(path):
        return [], 0
    text = open(path).read()
    # Sections are delimited by level-2 headers (## Active / ## Killed / ...).
    sections = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"##\s+(.*)", line)
        if m:
            current = m.group(1).strip().lower()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    def entry_blocks(lines):
        # An entry starts at a bold header line (**ID — ...**); keep its body.
        blocks, cur = [], None
        for line in lines:
            if line.startswith("**"):
                if cur is not None:
                    blocks.append(cur)
                cur = [line]
            elif cur is not None:
                cur.append(line)
        if cur is not None:
            blocks.append(cur)
        return ["\n".join(b) for b in blocks]

    active = []
    for block in entry_blocks(sections.get("active", [])):
        demand = re.search(r"demand:(proven-pattern|proven|assumed)", block)
        status = re.search(r"[Ss]tatus:\s*`?(\w+)`?", block)
        active.append({
            "demand": demand.group(1) if demand else "unspecified",
            "status": status.group(1) if status else "unspecified",
        })

    killed = sum(
        1 for line in sections.get("killed", [])
        if line.startswith("**")
    )
    return active, killed


def main():
    space = engine.unique_space()
    drawn = ledger_count()
    remaining = space - drawn
    pct = (drawn / space * 100) if space else 0

    print("Idea pipeline status")
    print("====================")
    print(f"Combination space : {space:,}  "
          f"({len(engine.worlds)} worlds x {len(engine.forms)} forms x {len(engine.twists)} twists)")
    print(f"Drawn (ledger)    : {drawn:,}  "
          f"({pct:.2f}% burned, {remaining:,} remaining)")

    active, killed = parse_backlog()
    print()
    print("Backlog")
    if not active and not killed:
        print("  (empty)")
        return

    from collections import Counter
    statuses = Counter(e["status"] for e in active)
    demands = Counter(e["demand"] for e in active)
    status_str = " / ".join(f"{k} {v}" for k, v in sorted(statuses.items()))
    demand_str = " / ".join(f"{k} {v}" for k, v in sorted(demands.items()))
    print(f"  Active : {len(active)}   ({status_str})")
    print(f"  Killed : {killed}")
    print(f"  Demand : {demand_str}")

    # The honesty check this tool exists for.
    untested = [e for e in active if e["status"] == "backlog"]
    assumed = [e for e in untested if e["demand"] != "proven"]
    if untested and len(assumed) / len(untested) >= 0.6:
        print(f"  -> {len(assumed)} of {len(untested)} untested ideas are not demand:proven.")
        print("     Probe or prune before adding more, or tighten the screen / widen worlds.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # Reader closed early (e.g. `| head`); exit quietly like a good CLI.
        try:
            sys.stdout.close()
        except Exception:
            pass
