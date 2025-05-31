# tests/test_hmac_sha3.py
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import hmac_sha3


KEY = bytes.fromhex('0b' * 16)
MSG = b'Hi There'
REF = bytes.fromhex(
    '874d1d4e6e8302439bf707052e5d787d'
    '92bffcf0715853784e30da740a81e198'
)


def test_nist_vector():
    """Перевірка еталонного NIST-вектора."""
    assert hmac_sha3.compute_mac(KEY, MSG) == REF


def test_tamper_msg():
    """Тег НЕ має збігтися, якщо повідомлення підмінено."""
    mac_ok = hmac_sha3.compute_mac(KEY, MSG)

    # підміняємо один байт (фліп останнього біта)
    evil = MSG[:-1] + bytes([MSG[-1] ^ 0x01])

    assert hmac_sha3.compute_mac(KEY, evil) != mac_ok

