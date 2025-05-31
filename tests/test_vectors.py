# tests/test_vectors.py
import os, secrets, pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import hmac_sha3

# бере еталон прямо з PyCryptodome
from Crypto.Hash import HMAC, SHA3_256, SHA3_384


# === 1. Порожнє повідомлення, ключ 0x00 ===
def test_empty_msg():
    key = bytes(32)
    msg = b""
    ref = HMAC.new(key, msg, SHA3_256).digest()            # ← еталон
    assert hmac_sha3.compute_mac(key, msg, 256) == ref


# === 2. Довге повідомлення 1000 байт ===
def test_long_msg():
    key = bytes.fromhex("aa" * 20)
    msg = b"A" * 1000
    ref = HMAC.new(key, msg, SHA3_256).digest()
    assert hmac_sha3.compute_mac(key, msg, 256) == ref


# === 3. Інша довжина тега (384 біт) ===
def test_digest_384():
    key = secrets.token_bytes(48)
    msg = os.urandom(57)
    ref = HMAC.new(key, msg, SHA3_384).digest()    # ← SHA3_384, без slice
    assert hmac_sha3.compute_mac(key, msg, 384) == ref