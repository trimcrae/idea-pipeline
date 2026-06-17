#!/usr/bin/env python3
"""Smoke tests for entropy_engine.py — guards the invariants the pipeline relies on.

Run: python engine/test_entropy_engine.py
No deps, no network. Exits non-zero on failure.
"""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "entropy_engine.py")


def run(args=None, env=None, expect_ok=True):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([sys.executable, ENGINE] + (args or []),
                       capture_output=True, text=True, env=e)
    if expect_ok:
        assert p.returncode == 0, f"non-zero exit: {p.returncode}\n{p.stderr}"
    return p


def test_seed_is_deterministic():
    a = run(["12345"]).stdout
    b = run(["12345"]).stdout
    assert a == b, "same seed must reproduce the same pool"


def test_default_count_and_dedup():
    out = run(env={"N": "50"}).stdout
    lines = [l for l in out.splitlines() if l[:4].strip().rstrip(".").isdigit()]
    assert len(lines) == 50, f"expected 50 idea lines, got {len(lines)}"
    # Dedup is on (world, form, twist) — the text before the wildcard bracket.
    concepts = [l.split("[")[0] for l in lines]
    assert len(set(concepts)) == len(concepts), "pool contains duplicate concepts"


def test_oversized_n_is_capped_not_hung():
    # Huge N must cap to the unique space and finish, not spin forever.
    p = run(env={"N": "10000000"})
    assert "capping" in p.stderr, "expected a cap notice on stderr"


def test_out_creates_missing_dirs(tmp="/tmp/_ep_test_out/sub/pool.txt"):
    if os.path.exists(tmp):
        os.remove(tmp)
    run(["--out", tmp], env={"N": "5"})
    assert os.path.exists(tmp), "--out should create missing parent dirs"
    os.remove(tmp)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
