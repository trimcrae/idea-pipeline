"""Feed encryption — AES-256-GCM, WebCrypto-compatible.

The full weekly CSV is published as ciphertext on a public branch; the key is
delivered only through the payment provider's post-purchase redirect
(`feeds/get/?f=<id>&k=<hex key>`), and the browser decrypts with WebCrypto.
Nothing committed to either branch contains a key.

File format: 12-byte random IV || AES-GCM ciphertext || 16-byte tag
(exactly what `crypto.subtle.decrypt({name:'AES-GCM', iv}, key, data)` expects).

Key per feed = SHA-256("feeds:" + secret + ":" + feed_id). `secret` comes from
FEED_SECRET, or is derived from STRIPE_SECRET_KEY so the operator only has to
add one GitHub secret. With neither, `secret_from_env()` returns None and the
builder runs in preview mode (no full feeds are published).
"""
import hashlib
import os

try:  # third-party, installed on the Actions runner (pip install cryptography)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except BaseException:  # noqa: BLE001 — a broken system install raises a PanicException
    AESGCM = None


def secret_from_env(env=os.environ):
    s = env.get("FEED_SECRET")
    if s:
        return s
    sk = env.get("STRIPE_SECRET_KEY")
    if sk:
        return hashlib.sha256(("feeds-secret:" + sk).encode()).hexdigest()
    return None


def feed_key(secret, feed_id):
    """32-byte AES key for one feed (stable as long as the secret is)."""
    return hashlib.sha256(f"feeds:{secret}:{feed_id}".encode()).digest()


def encrypt(plaintext, key):
    if AESGCM is None:
        raise RuntimeError("pip install cryptography (needed to publish full feeds)")
    iv = os.urandom(12)
    return iv + AESGCM(key).encrypt(iv, plaintext, None)


def decrypt(blob, key):
    if AESGCM is None:
        raise RuntimeError("pip install cryptography")
    return AESGCM(key).decrypt(blob[:12], blob[12:], None)
