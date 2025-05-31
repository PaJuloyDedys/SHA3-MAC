import os, secrets, hashlib, pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import hmac_sha3

# === 1. Порожнє повідомлення, ключ 0x00 ===
def test_empty_msg():
    key = bytes(32)
    mac = hmac_sha3.compute_mac(key, b"", 256)
    assert mac.hex() == (
        "5c1634e61ae95317c017ba7717c9e1af"
        "d708a407f20821bbee8f90959c8e3f6f"
    )

# === 2. Довге повідомлення 1000 байт ===
def test_long_msg():
    key = bytes.fromhex("aa" * 20)
    msg = b"A" * 1000
    mac = hmac_sha3.compute_mac(key, msg, 256)
    assert mac.hex() == (
        "7feea65dbad8e252e7f0ec6288d92645"
        "3e2b50d972dc9697c8435c2a14dce773"
    )

# === 3. Інша довжина тега (384 біт) ===
def test_digest_384():
    key = secrets.token_bytes(48)
    msg = os.urandom(57)
    mac1 = hmac_sha3.compute_mac(key, msg, 384)
    # перевіряємо, що verify спрацьовує
    assert hmac_sha3.verify_mac(key, msg, mac1, 384)
    # і падає на зміненому байті
    tampered = bytearray(msg); tampered[-1] ^= 0x01
    assert not hmac_sha3.verify_mac(key, tampered, mac1, 384)
