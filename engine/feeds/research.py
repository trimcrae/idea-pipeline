#!/usr/bin/env python3
"""Research pass 2: per candidate dataset, print columns, latest sample rows,
and 7-/30-day counts for every date-like column. Runs on an Actions runner."""
import datetime as dt, json, sys, urllib.parse, urllib.request

CANDS = [
    # domain, id, note, optional where-filter probes
    ("data.transportation.gov", "az4n-8mr2", "FMCSA company census", ["add_date >= '20260905'", "add_date >= '20260813'"]),
    ("data.transportation.gov", "6eyk-hxee", "FMCSA L&I carrier", []),
    ("data.transportation.gov", "qh9u-swkp", "FMCSA L&I ActPendInsur", []),
    ("data.transportation.gov", "9mw4-x3tu", "FMCSA L&I AuthHist", []),
    ("data.cityofnewyork.us", "43nn-pn8j", "NYC restaurant inspections",
     ["inspection_date >= '2026-09-05T00:00:00' AND (upper(violation_description) like '%RATS%' OR upper(violation_description) like '%MICE%' OR upper(violation_description) like '%ROACH%' OR upper(violation_description) like '%FLIES%' OR upper(violation_description) like '%VERMIN%')",
      "inspection_date >= '2026-09-05T00:00:00' AND inspection_type like 'Pre-permit%'"]),
    ("data.cityofnewyork.us", "w7w3-xahh", "NYC DCWP issued licenses", []),
    ("data.cityofnewyork.us", "ipu4-2q9a", "NYC DOB permit issuance", []),
    ("data.cityofchicago.org", "4ijn-s7e5", "Chicago food inspections",
     ["inspection_date >= '2026-09-05T00:00:00' AND upper(violations) like '%RODENT%'",
      "inspection_date >= '2026-09-05T00:00:00' AND inspection_type like 'License%'"]),
    ("data.cityofchicago.org", "r5kz-chrr", "Chicago business licenses", ["license_start_date >= '2026-09-05T00:00:00' AND application_type='ISSUE'"]),
    ("data.cityofchicago.org", "qfyy-956j", "Chicago shared housing", []),
    ("data.ny.gov", "f8i8-k2gm", "NY SLA pending licenses", []),
    ("data.ny.gov", "9s3h-dpkz", "NY SLA active licenses", []),
    ("data.texas.gov", "mxm5-tdpj", "TABC pending original apps", []),
    ("data.texas.gov", "7hf9-qc9f", "TABC license info", []),
    ("data.nola.gov", "en36-xvxg", "NOLA STR permit applications", []),
    ("data.kingcounty.gov", "r878-4sxa", "King County food inspections", []),
    ("data.ct.gov", "n7gp-d28j", "CT business registry", []),
    ("data.ny.gov", "n9v6-gdp6", "NY active corporations", []),
    ("data.colorado.gov", "4ykn-tg5h", "CO business entities", []),
    ("data.oregon.gov", "esjy-u4fc", "OR new businesses last month", []),
    ("data.sfgov.org", "g8m3-pdis", "SF registered businesses (guess id)", []),
    ("data.wa.gov", "ucdg-xgbj", "WA DOL transport licenses", []),
]


def get(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": "idea-pipeline-research/2.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def cnt(domain, dsid, where):
    try:
        u = f"https://{domain}/resource/{dsid}.json?" + urllib.parse.urlencode({"$select": "count(*) as n", "$where": where})
        return get(u)[0]["n"]
    except Exception as e:  # noqa: BLE001
        return f"err:{str(e)[:80]}"


def main():
    d7 = (dt.date.today() - dt.timedelta(days=7)).isoformat()
    d30 = (dt.date.today() - dt.timedelta(days=30)).isoformat()
    for domain, dsid, note, probes in CANDS:
        print("=" * 100)
        print(f"## {note} :: https://{domain}/resource/{dsid}.json")
        try:
            meta = get(f"https://{domain}/api/views/{dsid}.json")
        except Exception as e:  # noqa: BLE001
            print("  meta error:", str(e)[:200])
            continue
        cols = [(c.get("fieldName"), c.get("dataTypeName")) for c in meta.get("columns", [])]
        print("  name:", meta.get("name"), "| rowsUpdatedAt:", dt.datetime.utcfromtimestamp(meta.get("rowsUpdatedAt", 0)).isoformat())
        print("  cols:", ", ".join(f"{n}:{t}" for n, t in cols if n and not n.startswith(":@"))[:2500])
        datecols = [n for n, t in cols if n and (t in ("calendar_date", "floating_timestamp") or "date" in (n or "").lower() or n.lower().endswith("_dt"))]
        for f in datecols[:8]:
            typ = dict(cols).get(f)
            if typ in ("calendar_date", "floating_timestamp"):
                c7 = cnt(domain, dsid, f"{f} >= '{d7}T00:00:00'")
                c30 = cnt(domain, dsid, f"{f} >= '{d30}T00:00:00'")
            else:
                c7 = cnt(domain, dsid, f"{f} >= '{d7.replace('-', '')}'")
                c30 = cnt(domain, dsid, f"{f} >= '{d30.replace('-', '')}'")
            print(f"  date {f} ({typ}): last7={c7} last30={c30}")
        for p in probes:
            print(f"  probe [{p[:90]}...]: {cnt(domain, dsid, p)}")
        try:
            order = datecols[0] + " DESC" if datecols else None
            params = {"$limit": 2}
            if order:
                params["$order"] = order
            rows = get(f"https://{domain}/resource/{dsid}.json?" + urllib.parse.urlencode(params))
            for r in rows:
                print("  sample:", json.dumps(r)[:1400])
        except Exception as e:  # noqa: BLE001
            print("  sample error:", str(e)[:200])
        sys.stdout.flush()


if __name__ == "__main__":
    main()
