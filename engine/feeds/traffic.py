#!/usr/bin/env python3
"""Weekly traffic snapshot from the hits.sh counters every page pings.

Runs on the Actions runner (the dev sandbox cannot reach hits.sh). Reads each
counter, appends a dated snapshot to feeds/traffic.json (kept 52 weeks) and
renders TRAFFIC.md. The Routine reads these files to decide whether the site
is getting real visitors (STRATEGY.md D17) — no human has to open a counter.

Reading strategy (probe 2026-09-12): hits.sh has no JSON endpoint; the `.svg`
badge carries the count in `aria-label="hits: N"`, and every badge read is
itself counted as a hit. `monitor_reads` therefore records how many reads this
monitor has made per key; TRAFFIC.md subtracts it to show real traffic. Runs on
`main` only (a dry run would inflate the counters for nothing).
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import registry  # noqa: E402

HOST = "trimcrae.github.io/idea-pipeline"
HITS = "https://hits.sh/" + HOST
KEEP = 52
UA = {"User-Agent": "idea-pipeline-traffic/1.0"}


def counters():
    """(label, url-without-extension) for every counter the site pings."""
    out = [("hub · view", f"{HITS}/view")]
    for f in registry.FEEDS:
        fid = f["id"]
        out += [(f"{fid} · view", f"{HITS}/feeds/{fid}/view"),
                (f"{fid} · download-click", f"{HITS}/feeds/{fid}/download"),
                (f"{fid} · subscribe-click", f"{HITS}/feeds/{fid}/subscribe"),
                (f"{fid} · sample", f"{HITS}/feeds/{fid}/sample"),
                (f"{fid} · file-saved", f"{HITS}/feeds/get/{fid}/download")]
    out.append(("experiments · view", f"{HITS}/experiments/view"))
    return out


def fetch(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def parse_badge(svg):
    m = re.search(r'aria-label="hits:\s*([\d,]+)"', svg) or re.search(r"<title>hits:\s*([\d,]+)</title>", svg)
    if m:
        return int(m.group(1).replace(",", ""))
    nums = [int(x.replace(",", "")) for x in re.findall(r">\s*([\d,]+)\s*<", svg)]
    return nums[-1] if nums else None


def read_count(base):
    """Return (count, method) or (None, reason). Each read is one hit on the key."""
    try:
        n = parse_badge(fetch(base + ".svg"))
        return (n, "svg") if n is not None else (None, "svg-unparsed")
    except Exception as e:  # noqa: BLE001
        return None, f"error:{type(e).__name__}"


def prev_net(prev_snapshot, reads_now):
    """Net (monitor-excluded) counts of the previous snapshot. Older snapshots
    without a stored `net` are reconstructed: the monitor had made one read fewer
    per key at that time."""
    if "net" in prev_snapshot:
        return prev_snapshot["net"]
    return {k: v - max(reads_now.get(k, 0) - 1, 0) for k, v in prev_snapshot["counts"].items()}


def load_json(path, default):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def main():
    path = os.path.join(ROOT, "feeds", "traffic.json")
    state = load_json(path, {"snapshots": [], "monitor_reads": {}})
    today = dt.date.today().isoformat()
    counts, methods = {}, {}
    for label, base in counters():
        n, how = read_count(base)
        if n is not None:
            counts[label] = n
            methods[label] = how
            if how == "svg":  # a badge read is itself a hit
                state["monitor_reads"][label] = state["monitor_reads"].get(label, 0) + 1
    reads = state["monitor_reads"]
    net = {k: v - reads.get(k, 0) for k, v in counts.items()}  # real traffic
    snap = {"date": today, "counts": counts, "net": net}
    state["snapshots"] = [s for s in state["snapshots"] if s["date"] != today] + [snap]
    state["snapshots"] = state["snapshots"][-KEEP:]
    state["methods"] = methods
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)

    prev = prev_net(state["snapshots"][-2], reads) if len(state["snapshots"]) > 1 else {}
    lines = ["# TRAFFIC.md — weekly counter snapshot (generated; do not edit)\n",
             f"Snapshot {today}. Counts are cumulative hits.sh totals with this monitor's own badge reads",
             "subtracted; Δ is the change since the previous snapshot. A *view* is a page load with JS;",
             "*download-click* is the main button on a feed page; *file-saved* is a CSV actually saved from",
             "the download page — the number that means demand.\n",
             "| Counter | Total | Δ week |", "| --- | ---: | ---: |"]
    for label, base in counters():
        if label not in counts:
            continue
        total = net[label]
        delta = total - prev[label] if label in prev else total
        lines.append(f"| {label} | {total} | {delta:+d} |")
    site_views = sum(v for k, v in net.items() if k.endswith("· view"))
    saved = sum(v for k, v in net.items() if k.endswith("file-saved"))
    feed_views = sum(v for k, v in net.items() if k.endswith("· view") and k not in ("hub · view", "experiments · view"))
    prev_feed_views = sum(v for k, v in prev.items() if k.endswith("· view") and k not in ("hub · view", "experiments · view"))
    gate = {"date": today, "feed_page_views_week": feed_views - prev_feed_views if prev else feed_views,
            "files_saved_total": saved, "bar_met": (feed_views - prev_feed_views if prev else feed_views) >= 20 or saved > 0}
    state["gate"] = [g for g in state.get("gate", []) if g["date"] != today] + [gate]
    state["gate"] = state["gate"][-KEEP:]
    with open(path, "w") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)
    lines += ["", f"**Site views (all pages): {site_views} · files saved: {saved} · feed-page views this week: {gate['feed_page_views_week']} · D17 bar met: {'yes' if gate['bar_met'] else 'no'}**", "",
              "Traffic gate (STRATEGY.md D17): bar = ≥ 20 feed-page views in the week, or any file saved.",
              "The Routine acts when four consecutive weekly snapshots miss it (`gate` in feeds/traffic.json)."]
    with open(os.path.join(ROOT, "TRAFFIC.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(json.dumps({"date": today, "counters_read": len(counts), "site_views": site_views, "files_saved": saved, "gate": gate}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
