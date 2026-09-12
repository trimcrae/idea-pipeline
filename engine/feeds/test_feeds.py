#!/usr/bin/env python3
"""Offline tests for the feed pipeline: python engine/feeds/test_feeds.py"""
import datetime as dt, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build, registry, socrata  # noqa: E402
import feedcrypto as crypto  # noqa: E402


def test_where_clause():
    since, until = build.window(dt.date(2026, 9, 12))
    assert (since, until) == (dt.date(2026, 9, 5), dt.date(2026, 9, 12))
    w = build.where_clause({"date_field": "add_date", "date_format": "yyyymmdd"}, since, until)
    assert w == "add_date >= '20260905' AND add_date < '20260912'", w
    w = build.where_clause({"date_field": "d", "where": "x=1"}, since, until)
    assert w == "d >= '2026-09-05T00:00:00' AND d < '2026-09-12T00:00:00' AND (x=1)", w


def test_query_paginates():
    calls = []

    def fake(url):
        calls.append(url)
        # first page full (limit=2), second page short
        return [{"a": 1}, {"a": 2}] if "%24offset=0" in url else [{"a": 3}]

    socrata.PAGE_SAVE = socrata.PAGE
    socrata.PAGE = 2
    try:
        rows = socrata.query("h", "ds", where="x", order="a", fetch=fake)
    finally:
        socrata.PAGE = socrata.PAGE_SAVE
    assert [r["a"] for r in rows] == [1, 2, 3]
    assert len(calls) == 2 and "%24where=x" in calls[0] and "%24order=a" in calls[0]


def test_mask():
    assert build.mask("owner@acmehauling.com", "email") == "o***@acmehauling.com"
    assert build.mask("(214) 555-0101", "phone") == "***-***-**01"
    assert build.mask("512", "phone") == "***"
    assert build.mask("", "phone") == ""


def test_build_fixture_preview_and_published():
    tmp = tempfile.mkdtemp()
    try:
        site, data = os.path.join(tmp, "site"), os.path.join(tmp, "data")
        feed = registry.BY_ID["us-new-trucking-carriers"]
        rows = json.load(open(os.path.join(HERE, "fixtures", feed["id"] + ".json")))
        # preview mode: no secret -> samples/stats only
        st = build.build_feed(feed, dt.date(2026, 9, 12), site, data, None, rows=rows)
        assert st["rows"] == 3, st  # duplicate usdot collapsed
        assert st["published"] is False
        plain = open(os.path.join(data, feed["id"], "latest.csv")).read()
        assert "owner@acmehauling.com" in plain  # free beta: full rows in the clear
        man = json.load(open(os.path.join(data, feed["id"], "manifest.json")))
        assert man["encrypted"] is False and man["weeks"][0]["file"].endswith(".csv")
        sample = open(os.path.join(site, "feeds", feed["id"], "sample.csv")).read()
        assert "o***@acmehauling.com" in sample and "owner@acmehauling.com" not in sample
        assert "***-***-**01" in sample and "2145550101" not in sample
        assert "2026-09-08" in sample  # yyyymmdd normalised
        stats = json.load(open(os.path.join(site, "feeds", feed["id"], "stats.json")))
        assert stats["groups"][0] == ["TX", 2], stats["groups"]
        assert stats["week_start"] == "2026-09-05" and stats["week_end"] == "2026-09-11"
        hist = json.load(open(os.path.join(site, "feeds", feed["id"], "history.json")))
        assert len(hist) == 1 and hist[0]["rows"] == 3

        # published mode: encrypted full feed + manifest, decryptable with the feed key
        st = build.build_feed(feed, dt.date(2026, 9, 12), site, data, "s3cret", rows=rows)
        ddir = os.path.join(data, feed["id"])
        man = json.load(open(os.path.join(ddir, "manifest.json")))
        assert man["latest"] == "2026-09-11.csv.enc" and len(man["weeks"]) == 1 and man["encrypted"]
        assert not os.path.exists(os.path.join(ddir, "latest.csv"))  # plain copy removed once encrypted
        blob = open(os.path.join(ddir, "latest.csv.enc"), "rb").read()
        plain = crypto.decrypt(blob, crypto.feed_key("s3cret", feed["id"])).decode()
        assert "owner@acmehauling.com" in plain and plain.count("\n") == 4  # header + 3 rows
        # history de-duplicates the same week on rebuild
        hist = json.load(open(os.path.join(site, "feeds", feed["id"], "history.json")))
        assert len(hist) == 1
        # a later week is retained alongside; old weeks pruned beyond KEEP_WEEKS
        for i in range(1, build.KEEP_WEEKS + 2):
            build.build_feed(feed, dt.date(2026, 9, 12) + dt.timedelta(days=7 * i), site, data, "s3cret", rows=rows)
        man = json.load(open(os.path.join(ddir, "manifest.json")))
        assert len(man["weeks"]) == build.KEEP_WEEKS
        files = [f for f in os.listdir(ddir) if f.endswith(".csv.enc") and f != "latest.csv.enc"]
        assert len(files) == build.KEEP_WEEKS, files
    finally:
        shutil.rmtree(tmp)


def test_nyc_fixture_iso_dates():
    tmp = tempfile.mkdtemp()
    try:
        feed = registry.BY_ID["nyc-restaurant-pest-violations"]
        rows = json.load(open(os.path.join(HERE, "fixtures", feed["id"] + ".json")))
        st = build.build_feed(feed, dt.date(2026, 9, 12), tmp, os.path.join(tmp, "d"), None, rows=rows)
        assert st["rows"] == 2
        sample = open(os.path.join(tmp, "feeds", feed["id"], "sample.csv")).read()
        assert "2026-09-09" in sample and "T00:00" not in sample
    finally:
        shutil.rmtree(tmp)


def test_text_date_in_lists_and_enrich():
    since, until = build.window(dt.date(2026, 9, 12))
    w = build.where_clause({"date_field": "d", "date_format": "mmddyyyy", "where": "x"}, since, until)
    assert w.startswith("d in ('09/05/2026', '09/06/2026'") and w.endswith("'09/11/2026') AND (x)"), w
    w = build.where_clause({"date_field": "d", "date_format": "mixed"}, since, until)
    assert "'09/05/2026', '2026-09-05'" in w and w.count(",") == 13, w
    recs = [{"docket": "MC000123", "usdot": "00004567"}, {"docket": "MC000999", "usdot": ""}]
    calls = []

    def fake(url):
        calls.append(url)
        if "6eyk-hxee" in url:
            return [{"docket_number": "MC000123", "legal_name": "ACME", "bus_telno": "5551234"}]
        return [{"dot_number": "4567", "email_address": "a@b.c"}]

    build.enrich(recs, registry.LI_CARRIER, fetch=fake)
    build.enrich(recs, registry.CENSUS_EMAIL, fetch=fake)
    assert recs[0]["legal_name"] == "ACME" and recs[0]["phone"] == "5551234" and recs[0]["email"] == "a@b.c"
    assert recs[1]["legal_name"] == "" and recs[1]["email"] == ""
    assert "dot_number+in+%28%274567%27%29" in calls[-1], calls[-1]  # zero-padded key normalised


def test_main_prunes_stale_data_dirs():
    tmp = tempfile.mkdtemp()
    try:
        site, data = os.path.join(tmp, "site"), os.path.join(tmp, "data")
        os.makedirs(os.path.join(data, "some-killed-feed"))
        open(os.path.join(data, "some-killed-feed", "latest.csv"), "w").write("x")
        rc = build.main(["--fixture", os.path.join(HERE, "fixtures"), "--week-end", "2026-09-12",
                         "--site-root", site, "--data-out", data])
        assert rc == 0
        assert not os.path.exists(os.path.join(data, "some-killed-feed"))
        assert os.path.exists(os.path.join(data, "us-new-trucking-carriers", "latest.csv"))
    finally:
        shutil.rmtree(tmp)


def test_secret_derivation():
    assert crypto.secret_from_env({}) is None
    assert crypto.secret_from_env({"FEED_SECRET": "x"}) == "x"
    d = crypto.secret_from_env({"STRIPE_SECRET_KEY": "sk_test_1"})
    assert d and d == crypto.secret_from_env({"STRIPE_SECRET_KEY": "sk_test_1"})
    assert crypto.feed_key("a", "f") != crypto.feed_key("a", "g")


def test_registry_shape():
    ids = set()
    for f in registry.FEEDS + registry.PARKED:
        assert f["id"] not in ids; ids.add(f["id"])
        for k in ("title", "short", "buyers", "price", "source", "columns", "attribution", "source_url"):
            assert k in f, (f["id"], k)
        exported = [d for _, d in f["columns"]] + [f.get("extra_key")]
        for spec in f.get("enrich", []):
            exported += [d for _, d in spec["columns"]]
        assert f["source"]["id_field"] in exported, f["id"]
        assert f.get("group_by") in exported, f["id"]
        for c in f.get("contact", {}):
            assert c in exported, (f["id"], c)
        assert f.get("disclaimer", "x") and f["price"] in (19, 29)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok", fn.__name__)
    print(f"{len(fns)} tests passed")
