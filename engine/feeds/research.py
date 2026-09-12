#!/usr/bin/env python3
"""One-off research helper: discover Socrata datasets for candidate feed niches.

Runs on a GitHub Actions runner (the dev sandbox has no egress to these hosts).
Prints, per query: dataset id, name, last-updated, row count, and columns.
No deps (urllib only).
"""
import json, sys, urllib.parse, urllib.request

CATALOG = "https://api.us.socrata.com/api/catalog/v1"

QUERIES = [
    # (domain, search text, limit)
    ("data.transportation.gov", "company census file", 3),
    ("data.transportation.gov", "authority history", 3),
    ("data.transportation.gov", "active pending insurance", 3),
    ("data.transportation.gov", "carrier licensing insurance", 3),
    ("data.transportation.gov", "revocation", 3),
    ("data.cityofnewyork.us", "restaurant inspection results", 2),
    ("data.cityofnewyork.us", "legally operating businesses license", 2),
    ("data.cityofnewyork.us", "DOB permit issuance", 2),
    ("data.cityofchicago.org", "food inspections", 2),
    ("data.cityofchicago.org", "business licenses", 2),
    ("data.cityofchicago.org", "shared housing registration", 2),
    ("data.ny.gov", "liquor authority licenses", 3),
    ("data.texas.gov", "TABC license pending", 3),
    ("data.texas.gov", "TDLR license", 3),
    ("data.austintexas.gov", "short term rental license", 2),
    ("data.austintexas.gov", "food establishment inspection", 2),
    ("data.nola.gov", "short term rental permit", 2),
    ("data.sfgov.org", "registered business locations", 2),
    ("data.sfgov.org", "restaurant inspection", 2),
    ("data.lacity.org", "business registration", 2),
    ("data.seattle.gov", "business license", 2),
    ("data.wa.gov", "business license", 2),
    ("data.colorado.gov", "business entities", 2),
    ("data.cityofdallas.gov", "restaurant inspection", 2),
    ("data.lacounty.gov", "restaurant inspection", 2),
    ("data.kingcounty.gov", "food establishment inspection", 2),
    ("data.louisvilleky.gov", "restaurant inspection", 2),
    ("data.nashville.gov", "short term rental permit", 2),
    ("data.cityofnewyork.us", "short term rental registration", 2),
    ("data.sfgov.org", "short term rental", 2),
    ("data.oregon.gov", "business registry", 2),
    ("data.ct.gov", "business registration", 2),
    ("data.ny.gov", "active corporations", 2),
    ("data.cityofnewyork.us", "new business", 2),
]


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "idea-pipeline-research/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def rowcount(domain, dsid):
    try:
        u = f"https://{domain}/resource/{dsid}.json?$select=count(*)"
        j = json.loads(get(u))
        return j[0].get("count") if j else "?"
    except Exception as e:  # noqa: BLE001
        return f"err:{type(e).__name__}"


def main():
    for domain, q, limit in QUERIES:
        params = urllib.parse.urlencode({"domains": domain, "q": q, "only": "datasets", "limit": limit})
        print("=" * 100)
        print(f"## {domain} :: {q}")
        try:
            data = json.loads(get(f"{CATALOG}?{params}"))
        except Exception as e:  # noqa: BLE001
            print("  catalog error:", e)
            continue
        for r in data.get("results", []):
            res = r["resource"]
            dsid = res["id"]
            cols = list(zip(res.get("columns_field_name", []), res.get("columns_datatype", [])))
            print(f"- {dsid} | {res.get('name')} | updated {res.get('updatedAt')} | rows {rowcount(domain, dsid)}")
            print(f"    url: https://{domain}/resource/{dsid}.json")
            print("    cols:", ", ".join(f"{n}:{t}" for n, t in cols)[:1500])
    # CORS check on one Socrata domain (browser use later)
    try:
        req = urllib.request.Request(
            "https://data.transportation.gov/resource/az4n-8mr2.json?$limit=1",
            headers={"Origin": "https://trimcrae.github.io", "User-Agent": "idea-pipeline-research/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            print("=" * 100)
            print("CORS header on data.transportation.gov:", r.headers.get("Access-Control-Allow-Origin"))
            print("sample row:", r.read().decode()[:1500])
    except Exception as e:  # noqa: BLE001
        print("CORS check error:", e)


if __name__ == "__main__":
    main()
