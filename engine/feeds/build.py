#!/usr/bin/env python3
"""Build the weekly public-records feeds.

For every feed in registry.FEEDS:
  1. pull the rows whose date field falls in the trailing 7-day window,
  2. project + normalise the columns,
  3. write the free artefacts into the site tree (feeds/<id>/sample.csv,
     stats.json, history.json — committed to main, served by Pages),
  4. write the paid artefacts into the data tree (<data-out>/<id>/latest.csv.enc,
     <week>.csv.enc, manifest.json — force-pushed to the orphan `feeds-data`
     branch and read by feeds/get/ over raw.githubusercontent.com).

Usage (Actions runner):  python engine/feeds/build.py --data-out out/feeds-data
Local, offline:          python engine/feeds/build.py --fixture engine/feeds/fixtures --week-end 2026-09-12
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import feedcrypto as crypto  # noqa: E402
import registry  # noqa: E402
import socrata  # noqa: E402

SAMPLE_ROWS = 25
KEEP_WEEKS = 8          # weekly files retained on the data branch
HISTORY_WEEKS = 52      # digest entries retained in history.json


# ---------- window + query -------------------------------------------------

def window(week_end, days=7):
    """[since, until) as dates; week_end is exclusive (the build day)."""
    return week_end - dt.timedelta(days=days), week_end


def date_literal(d, fmt):
    if fmt == "yyyymmdd":
        return d.strftime("'%Y%m%d'")
    return d.strftime("'%Y-%m-%dT00:00:00'")


def day_literals(since, until, fmt):
    """Every day in [since, until) as quoted text literals, for portals whose
    'dates' are free text (FMCSA L&I: MM/DD/YYYY; NYC DOB: a mix of both)."""
    out, d = [], since
    while d < until:
        if fmt in ("mmddyyyy", "mixed"):
            out.append(d.strftime("'%m/%d/%Y'"))
        if fmt in ("isodate", "mixed"):
            out.append(d.strftime("'%Y-%m-%d'"))
        d += dt.timedelta(days=1)
    return out


def where_clause(source, since, until):
    f, fmt = source["date_field"], source.get("date_format", "iso")
    if fmt in ("mmddyyyy", "isodate", "mixed"):
        parts = [f"{f} in ({', '.join(day_literals(since, until, fmt))})"]
    else:
        parts = [f"{f} >= {date_literal(since, fmt)}", f"{f} < {date_literal(until, fmt)}"]
    if source.get("where"):
        parts.append("(" + source["where"] + ")")
    return " AND ".join(parts)


def fetch_rows(feed, since, until, fetch=None):
    src = feed["source"]
    kw = {"where": where_clause(src, since, until), "order": src.get("order")}
    if fetch:
        kw["fetch"] = fetch
    return socrata.query(src["domain"], src["dataset"], **kw)


# ---------- normalise -------------------------------------------------------

_ws = re.compile(r"\s+")


def clean(v):
    if v is None:
        return ""
    if isinstance(v, dict):  # Socrata point / nested objects
        v = v.get("human_address") or json.dumps(v, sort_keys=True)
    return _ws.sub(" ", str(v)).strip()


def project(rows, feed):
    cols = feed["columns"]
    out = []
    for r in rows:
        rec = {dst: clean(r.get(src)) for src, dst in cols}
        if feed.get("derive"):
            feed["derive"](r, rec)
        out.append(rec)
    return out


def enrich(recs, spec, fetch=None):
    """Fill columns from another dataset, joined on one key (chunked IN queries)."""
    key_src, key_field, chunk = spec["key_src"], spec["key_field"], spec.get("chunk", 100)
    tf = spec.get("key_transform")
    def norm(v):
        v = clean(v)
        return v.lstrip("0") or "0" if tf == "lstrip0" else v
    keys = sorted({norm(r.get(key_src)) for r in recs if clean(r.get(key_src))})
    lookup = {}
    for i in range(0, len(keys), chunk):
        lits = ", ".join("'" + k.replace("'", "''") + "'" for k in keys[i:i + chunk])
        kw = {"where": f"{key_field} in ({lits})"}
        if fetch:
            kw["fetch"] = fetch
        for row in socrata.query(spec["domain"], spec["dataset"], **kw):
            lookup.setdefault(norm(row.get(key_field)), row)
    for r in recs:
        row = lookup.get(norm(r.get(key_src)), {})
        for src, dst in spec["columns"]:
            r[dst] = clean(row.get(src))
    return recs


def dedupe(recs, key):
    seen, out = set(), []
    for r in recs:
        k = r.get(key) or json.dumps(r, sort_keys=True)
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def mask(value, kind):
    v = clean(value)
    if not v:
        return ""
    if kind == "email":
        local, _, dom = v.partition("@")
        return (local[:1] + "***@" + dom) if dom else "***"
    if kind == "phone":
        digits = re.sub(r"\D", "", v)
        return ("***-***-**" + digits[-2:]) if len(digits) >= 4 else "***"
    return v[:2] + "***"


def sample_of(recs, feed):
    contact = feed.get("contact", {})
    out = []
    for r in recs[:SAMPLE_ROWS]:
        s = dict(r)
        for col, kind in contact.items():
            if col in s:
                s[col] = mask(s[col], kind)
        out.append(s)
    return out


# ---------- stats -----------------------------------------------------------

def top_groups(recs, field, n=15):
    if not field:
        return []
    counts = {}
    for r in recs:
        k = r.get(field) or "(blank)"
        counts[k] = counts.get(k, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


# ---------- io --------------------------------------------------------------

def csv_bytes(recs, header):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=header, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in recs:
        w.writerow(r)
    return buf.getvalue().encode("utf-8")


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as fh:
        fh.write(data)


def load_json(path, default):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


# ---------- one feed --------------------------------------------------------

def build_feed(feed, week_end, site_root, data_out, secret, fetch=None, rows=None):
    since, until = window(week_end, feed.get("window_days", 7))
    offline = rows is not None and fetch is None  # fixture run: no network for joins
    if rows is None:
        rows = fetch_rows(feed, since, until, fetch=fetch)
    header = [dst for _, dst in feed["columns"]]
    if feed.get("extra_key") and feed["extra_key"] not in header:
        header.append(feed["extra_key"])
    for spec in feed.get("enrich", []):
        header += [dst for _, dst in spec["columns"]]
    recs = dedupe(project(rows, feed), feed["source"].get("id_field"))
    if feed.get("post_filter"):
        recs = [r for r in recs if feed["post_filter"](r)]
    for spec in feed.get("enrich", []):
        if offline:
            continue
        enrich(recs, spec, fetch=fetch)
    if feed.get("sort"):
        recs.sort(key=feed["sort"])

    fid = feed["id"]
    site_dir = os.path.join(site_root, "feeds", fid)
    generated = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    groups = top_groups(recs, feed.get("group_by"))
    stats = {
        "id": fid, "week_start": since.isoformat(), "week_end": (until - dt.timedelta(days=1)).isoformat(),
        "rows": len(recs), "columns": header, "group_by": feed.get("group_by"),
        "groups": groups, "generated_at": generated, "sample_rows": min(len(recs), SAMPLE_ROWS),
        "published": bool(secret),
    }
    write(os.path.join(site_dir, "sample.csv"), csv_bytes(sample_of(recs, feed), header))
    write(os.path.join(site_dir, "stats.json"), json.dumps(stats, indent=1))

    hist_path = os.path.join(site_dir, "history.json")
    history = [h for h in load_json(hist_path, []) if h.get("week_end") != stats["week_end"]]
    history.append({"week_start": stats["week_start"], "week_end": stats["week_end"],
                    "rows": len(recs), "groups": groups[:8]})
    history = sorted(history, key=lambda h: h["week_end"])[-HISTORY_WEEKS:]
    write(hist_path, json.dumps(history, indent=1))

    # Paid artefacts. With a secret the CSV is encrypted (subscriber-only); with
    # none (preview mode, before payments exist) it is published in the clear as
    # a free beta — a real demand probe, and the same page/JS handles both.
    ddir = os.path.join(data_out, fid)
    plain = csv_bytes(recs, header)
    if secret:
        blob = crypto.encrypt(plain, crypto.feed_key(secret, fid))
        weekfile, latest = f"{stats['week_end']}.csv.enc", "latest.csv.enc"
    else:
        blob, weekfile, latest = plain, f"{stats['week_end']}.csv", "latest.csv"
    write(os.path.join(ddir, weekfile), blob)
    for stale in ("latest.csv", "latest.csv.enc"):
        if stale != latest:
            try:
                os.remove(os.path.join(ddir, stale))
            except OSError:
                pass
    write(os.path.join(ddir, latest), blob)
    manifest = load_json(os.path.join(ddir, "manifest.json"), {"id": fid, "weeks": []})
    weeks = [w for w in manifest.get("weeks", []) if w.get("file") != weekfile and w.get("encrypted", True) == bool(secret)]
    weeks.append({"week_start": stats["week_start"], "week_end": stats["week_end"],
                  "file": weekfile, "rows": len(recs), "bytes": len(blob), "encrypted": bool(secret),
                  "sha256": hashlib.sha256(blob).hexdigest()})
    weeks = sorted(weeks, key=lambda w: w["week_end"])
    for old in weeks[:-KEEP_WEEKS]:
        try:
            os.remove(os.path.join(ddir, old["file"]))
        except OSError:
            pass
    manifest = {"id": fid, "title": feed["title"], "columns": header, "generated_at": generated,
                "encrypted": bool(secret), "latest": weekfile, "weeks": weeks[-KEEP_WEEKS:]}
    write(os.path.join(ddir, "manifest.json"), json.dumps(manifest, indent=1))
    return stats


# ---------- main ------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--week-end", help="build date (UTC, exclusive), default today")
    ap.add_argument("--only", action="append", help="feed id(s) to build")
    ap.add_argument("--site-root", default=ROOT)
    ap.add_argument("--data-out", default=os.path.join(ROOT, "out", "feeds-data"))
    ap.add_argument("--fixture", help="dir with <feed id>.json row dumps (offline)")
    ap.add_argument("--fail-fast", action="store_true")
    a = ap.parse_args(argv)

    week_end = dt.date.fromisoformat(a.week_end) if a.week_end else dt.datetime.now(dt.timezone.utc).date()
    secret = crypto.secret_from_env()
    if not secret:
        print("!! no FEED_SECRET / STRIPE_SECRET_KEY: preview mode (samples + stats only, no full feeds)")

    results, failures = [], []
    for feed in registry.FEEDS:
        if a.only and feed["id"] not in a.only:
            continue
        rows = None
        if a.fixture:
            rows = load_json(os.path.join(a.fixture, feed["id"] + ".json"), None)
            if rows is None:
                print(f"-- {feed['id']}: no fixture, skipped")
                continue
        try:
            st = build_feed(feed, week_end, a.site_root, a.data_out, secret, rows=rows)
            print(f"ok {feed['id']}: {st['rows']} rows for {st['week_start']}..{st['week_end']}")
            results.append(st)
        except Exception as e:  # noqa: BLE001 — one broken portal must not sink the run
            print(f"FAIL {feed['id']}: {type(e).__name__}: {str(e)[:300]}")
            failures.append(feed["id"])
            if a.fail_fast:
                raise
    summary = {"built_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
               "week_end": week_end.isoformat(), "feeds": [r["id"] for r in results], "failed": failures,
               "published": bool(secret)}
    write(os.path.join(a.site_root, "feeds", "build.json"), json.dumps(summary, indent=1))
    print(json.dumps(summary))
    return 1 if (failures and not results) else 0


if __name__ == "__main__":
    sys.exit(main())
