"""Minimal Socrata (SODA 2.x) client — stdlib only.

Used by the feed builder on GitHub Actions runners (open internet). Every
public dataset on a Socrata portal exposes
  https://<domain>/resource/<dataset>.json?$where=...&$limit=...&$offset=...
No key is required for moderate use; an app token (free, optional) raises the
throttle. Set SOCRATA_APP_TOKEN in the environment to send one.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

PAGE = 50000  # SODA 2.1 max page size
UA = "idea-pipeline-feeds/1.0 (+https://github.com/trimcrae/idea-pipeline)"


class SocrataError(RuntimeError):
    pass


def _get(url, timeout=120, retries=4):
    headers = {"User-Agent": UA, "Accept": "application/json"}
    tok = os.environ.get("SOCRATA_APP_TOKEN")
    if tok:
        headers["X-App-Token"] = tok
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:  # 429 / 5xx: back off
            last = e
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:500]
            except Exception:  # noqa: BLE001
                pass
            raise SocrataError(f"HTTP {e.code} for {url}: {body}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            if attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
    raise SocrataError(f"failed after {retries} tries: {url}: {last}")


def query(domain, dataset, where=None, select=None, order=None, limit=None, fetch=_get):
    """Return all rows matching `where` (auto-paginated). `fetch` is injectable
    for tests."""
    rows = []
    offset = 0
    page = min(limit, PAGE) if limit else PAGE
    while True:
        params = {"$limit": page, "$offset": offset}
        if where:
            params["$where"] = where
        if select:
            params["$select"] = select
        if order:
            params["$order"] = order
        url = f"https://{domain}/resource/{dataset}.json?" + urllib.parse.urlencode(params)
        batch = fetch(url)
        rows.extend(batch)
        if len(batch) < page or (limit and len(rows) >= limit):
            break
        offset += page
    return rows[:limit] if limit else rows


def count(domain, dataset, where=None, fetch=_get):
    params = {"$select": "count(*) as n"}
    if where:
        params["$where"] = where
    url = f"https://{domain}/resource/{dataset}.json?" + urllib.parse.urlencode(params)
    out = fetch(url)
    return int(out[0]["n"]) if out else 0


def soda_ts(dt):
    """Format a datetime as a SODA floating timestamp literal."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S")
