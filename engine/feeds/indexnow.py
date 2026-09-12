#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver) with every URL in sitemap.xml.
Free, no account: the key file /<key>.txt on the site proves ownership."""
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOST = "trimcrae.github.io"


def main():
    key = open(os.path.join(ROOT, "config", "indexnow.txt")).read().strip()
    xml = open(os.path.join(ROOT, "sitemap.xml")).read()
    urls = re.findall(r"<loc>(.*?)</loc>", xml)[:10000]
    body = json.dumps({"host": HOST, "key": key, "keyLocation": f"https://{HOST}/idea-pipeline/{key}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "idea-pipeline-feeds/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("indexnow:", r.status, len(urls), "urls")
    except Exception as e:  # noqa: BLE001 — best effort
        print("indexnow failed (ignored):", str(e)[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
