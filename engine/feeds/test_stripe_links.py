#!/usr/bin/env python3
"""Offline test of the Stripe sync against a fake API: python engine/feeds/test_stripe_links.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import stripe_links as S  # noqa: E402


class Fake:
    """Records calls; simulates search/list/create with minimal state."""
    def __init__(self, links=None, prices=None, products=None):
        self.calls, self.links, self.prices, self.products = [], links or [], prices or [], products or []
        self.n = 0

    def __call__(self, method, path, params=None):
        self.calls.append((method, path, dict(params or {})))
        self.n += 1
        if path == "/v1/products/search":
            fid = params["query"].split("'")[3]
            return {"data": [p for p in self.products if p["metadata"]["feed_id"] == fid][:1]}
        if path == "/v1/products" and method == "POST":
            p = {"id": f"prod_{self.n}", "metadata": {"feed_id": params["metadata[feed_id]"]}}
            self.products.append(p); return p
        if path == "/v1/prices" and method == "GET":
            return {"data": [p for p in self.prices if p["product"] == params["product"]]}
        if path == "/v1/prices" and method == "POST":
            p = {"id": f"price_{self.n}", "product": params["product"], "currency": "usd",
                 "unit_amount": params["unit_amount"], "recurring": {"interval": "month"}}
            self.prices.append(p); return p
        if path == "/v1/payment_links" and method == "GET":
            return {"data": self.links, "has_more": False}
        if path.startswith("/v1/payment_links/") and path.endswith("/line_items"):
            lid = path.split("/")[3]
            l = next(l for l in self.links if l["id"] == lid)
            return {"data": [{"price": {"id": l["_price"]}}]}
        if path == "/v1/payment_links" and method == "POST":
            l = {"id": f"plink_{self.n}", "url": f"https://buy.stripe.com/test_{self.n}",
                 "metadata": {"feed_id": params["metadata[feed_id]"]}, "_price": params["line_items[0][price]"],
                 "after_completion": {"type": "redirect", "redirect": {"url": params["after_completion[redirect][url]"]}}}
            self.links.append(l); return l
        if path.startswith("/v1/payment_links/") and method == "POST":
            lid = path.split("/")[3]
            l = next(l for l in self.links if l["id"] == lid)
            if params.get("active") == "false":
                l["active"] = False
            if "after_completion[redirect][url]" in params:
                l["after_completion"] = {"type": "redirect", "redirect": {"url": params["after_completion[redirect][url]"]}}
            return l
        raise AssertionError(f"unexpected call {method} {path}")


FEED = {"id": "demo-feed", "title": "Demo", "short": "Demo feed", "price": 19}


def test_creates_everything_first_time():
    api = Fake()
    cfg = S.sync(api, "secret", feeds=[FEED], config={"portal_url": "", "feeds": {}})
    entry = cfg["feeds"]["demo-feed"]
    assert entry["payment_link"].startswith("https://buy.stripe.com/") and entry["price_usd"] == 19
    posts = [(m, p) for m, p, _ in api.calls if m == "POST"]
    assert posts == [("POST", "/v1/products"), ("POST", "/v1/prices"), ("POST", "/v1/payment_links")], posts
    create = next(prm for m, p, prm in api.calls if (m, p) == ("POST", "/v1/payment_links"))
    assert create["after_completion[redirect][url]"] == S.get_url("demo-feed", "secret")
    assert "&k=" in create["after_completion[redirect][url]"]


def test_idempotent_second_run():
    api = Fake()
    S.sync(api, "secret", feeds=[FEED], config={"feeds": {}})
    n_links = len(api.links)
    api.calls.clear()
    S.sync(api, "secret", feeds=[FEED], config={"feeds": {}})
    assert len(api.links) == n_links and not [c for c in api.calls if c[0] == "POST"], api.calls


def test_price_change_retires_old_link():
    api = Fake()
    S.sync(api, "secret", feeds=[FEED], config={"feeds": {}})
    dearer = dict(FEED, price=29)
    cfg = S.sync(api, "secret", feeds=[dearer], config={"feeds": {}})
    active = [l for l in api.links if l.get("active", True)]
    assert len(api.links) == 2 and len(active) == 1 and active[0]["url"] == cfg["feeds"]["demo-feed"]["payment_link"]


def test_redirect_update_when_secret_rotates():
    api = Fake()
    S.sync(api, "secret", feeds=[FEED], config={"feeds": {}})
    S.sync(api, "newsecret", feeds=[FEED], config={"feeds": {}})
    assert len(api.links) == 1 and api.links[0]["after_completion"]["redirect"]["url"] == S.get_url("demo-feed", "newsecret")


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print(f"{len(fns)} tests passed")
