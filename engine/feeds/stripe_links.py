#!/usr/bin/env python3
"""Keep one Stripe Product + monthly Price + Payment Link per feed, idempotently.

Runs on the Actions runner when STRIPE_SECRET_KEY is set (a *restricted* key
with write access to Products, Prices and Payment Links is enough). Writes the
public links to config/payments.json, which the page generator reads. With no
key it exits 0 and leaves the config untouched, so the site keeps working in
preview mode.

After a successful checkout Stripe redirects the buyer to
  <SITE>/feeds/get/?f=<feed id>&k=<per-feed AES key>
— the only place the decryption key ever appears (see feedcrypto.py).

Stdlib only; the Stripe API is plain form-encoded HTTPS.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import feedcrypto  # noqa: E402
import registry  # noqa: E402

SITE = "https://trimcrae.github.io/idea-pipeline"
CONFIG = os.path.join(ROOT, "config", "payments.json")
API = "https://api.stripe.com"


class StripeError(RuntimeError):
    pass


def make_api(secret_key):
    auth = base64.b64encode((secret_key + ":").encode()).decode()

    def api(method, path, params=None):
        data = None
        url = API + path
        if params and method == "GET":
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        elif params:
            data = urllib.parse.urlencode(params, doseq=True).encode()
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": "Basic " + auth,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "idea-pipeline-feeds/1.0",
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:600]
            raise StripeError(f"{method} {path} -> HTTP {e.code}: {body}") from e
    return api


def get_url(feed_id, secret):
    key_hex = feedcrypto.feed_key(secret, feed_id).hex()
    return f"{SITE}/feeds/get/?f={feed_id}&k={key_hex}"


def ensure_product(api, feed):
    found = api("GET", "/v1/products/search", {"query": f"metadata['feed_id']:'{feed['id']}'", "limit": 1})
    if found.get("data"):
        return found["data"][0]
    return api("POST", "/v1/products", {
        "name": feed["title"], "description": feed["short"][:500],
        "url": f"{SITE}/feeds/{feed['id']}/", "metadata[feed_id]": feed["id"],
    })


def ensure_price(api, feed, product):
    amount = int(round(feed["price"] * 100))
    prices = api("GET", "/v1/prices", {"product": product["id"], "active": "true", "limit": 100})
    for p in prices.get("data", []):
        rec = p.get("recurring") or {}
        if p.get("currency") == "usd" and p.get("unit_amount") == amount and rec.get("interval") == "month":
            return p
    return api("POST", "/v1/prices", {
        "product": product["id"], "unit_amount": amount, "currency": "usd",
        "recurring[interval]": "month", "metadata[feed_id]": feed["id"],
    })


def list_links(api):
    out, after = [], None
    while True:
        params = {"active": "true", "limit": 100}
        if after:
            params["starting_after"] = after
        page = api("GET", "/v1/payment_links", params)
        out.extend(page.get("data", []))
        if not page.get("has_more") or not page.get("data"):
            return out
        after = page["data"][-1]["id"]


def link_price_id(api, link):
    items = api("GET", f"/v1/payment_links/{link['id']}/line_items", {"limit": 1})
    data = items.get("data", [])
    return (data[0].get("price") or {}).get("id") if data else None


def ensure_link(api, feed, price, redirect_url, existing):
    for link in existing:
        if (link.get("metadata") or {}).get("feed_id") != feed["id"]:
            continue
        if link_price_id(api, link) != price["id"]:
            api("POST", f"/v1/payment_links/{link['id']}", {"active": "false"})  # price changed: retire
            continue
        after = link.get("after_completion") or {}
        if (after.get("redirect") or {}).get("url") != redirect_url:
            link = api("POST", f"/v1/payment_links/{link['id']}", {
                "after_completion[type]": "redirect", "after_completion[redirect][url]": redirect_url})
        return link
    return api("POST", "/v1/payment_links", {
        "line_items[0][price]": price["id"], "line_items[0][quantity]": 1,
        "after_completion[type]": "redirect", "after_completion[redirect][url]": redirect_url,
        "metadata[feed_id]": feed["id"], "subscription_data[metadata][feed_id]": feed["id"],
        "allow_promotion_codes": "true", "billing_address_collection": "auto",
        "tax_id_collection[enabled]": "true",
    })


def load_config(path=CONFIG):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {"portal_url": "", "feeds": {}}


def sync(api, secret, feeds=None, config=None):
    config = config if config is not None else load_config()
    config.setdefault("portal_url", "")
    config.setdefault("feeds", {})
    existing = list_links(api)
    for feed in feeds or registry.FEEDS:
        product = ensure_product(api, feed)
        price = ensure_price(api, feed, product)
        link = ensure_link(api, feed, price, get_url(feed["id"], secret), existing)
        config["feeds"][feed["id"]] = {
            "payment_link": link["url"], "payment_link_id": link["id"],
            "product_id": product["id"], "price_id": price["id"], "price_usd": feed["price"],
        }
        print(f"ok {feed['id']}: {link['url']}")
    return config


def main():
    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key:
        print("no STRIPE_SECRET_KEY: payment links not synced (preview mode)")
        return 0
    secret = feedcrypto.secret_from_env()
    config = sync(make_api(key), secret)
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    with open(CONFIG, "w") as fh:
        json.dump(config, fh, indent=1, sort_keys=True)
    print("wrote", os.path.relpath(CONFIG, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
