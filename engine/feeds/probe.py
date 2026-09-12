#!/usr/bin/env python3
"""Dataset probe: print columns, counts and samples for candidate feeds.

Edit engine/feeds/probe_queries.json and push — the `probe` workflow runs this
on a runner (the dev sandbox has no egress to the portals) and the answers are
in the job log. Used when adding or repairing a registry entry.
"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "idea-pipeline-probe/1.0"}


def get(url, timeout=90):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def fetch_text(url, timeout=60):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.status, dict(r.headers), r.read().decode("utf-8", "replace")


def main():
    queries = json.load(open(os.path.join(HERE, "probe_queries.json")))
    for q in queries:
        if "url" in q:  # raw HTTP probe (any host the runner can reach)
            print("=" * 100)
            print(f"## {q.get('note', '')} :: {q['url']}")
            for _ in range(q.get("times", 1)):
                try:
                    st, hdr, body = fetch_text(q["url"])
                    print(f"  HTTP {st} {hdr.get('Content-Type', '')} | {body[:600].replace(chr(10), ' ')}")
                except Exception as e:  # noqa: BLE001
                    print("  error:", str(e)[:200])
            sys.stdout.flush()
            continue
        domain, ds = q["domain"], q["dataset"]
        print("=" * 100)
        print(f"## {q.get('note', '')} :: https://{domain}/resource/{ds}.json")
        if q.get("meta", True):
            try:
                meta = get(f"https://{domain}/api/views/{ds}.json")
                cols = [(c.get("fieldName"), c.get("dataTypeName")) for c in meta.get("columns", [])]
                print("  name:", meta.get("name"))
                print("  cols:", ", ".join(f"{n}:{t}" for n, t in cols if n and not n.startswith(":@"))[:3000])
            except Exception as e:  # noqa: BLE001
                print("  meta error:", str(e)[:200])
        for params in q.get("queries", []):
            url = f"https://{domain}/resource/{ds}.json?" + urllib.parse.urlencode(params)
            try:
                out = get(url)
                print(f"  Q {json.dumps(params)}")
                for row in out[:5]:
                    print("    ", json.dumps(row)[:700])
                if len(out) > 5:
                    print(f"     ... {len(out)} rows")
            except Exception as e:  # noqa: BLE001
                print(f"  Q {json.dumps(params)} -> error {str(e)[:200]}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
