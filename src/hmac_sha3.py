#!/usr/bin/env python3
"""
CLI-утиліта для HMAC-SHA-3.
  ▸  gen    – згенерувати тег
  ▸  verify – перевірити повідомлення + тег
"""
from __future__ import annotations
import argparse, sys, pathlib, base64, logging
from typing import Literal

from Crypto.Hash import HMAC, SHA3_224, SHA3_256, SHA3_384, SHA3_512

# ------------------------------------------------------------

_DIGEST_MAP: dict[int, object] = {
    224: SHA3_224,
    256: SHA3_256,
    384: SHA3_384,
    512: SHA3_512,
}


def compute_mac(key: bytes, msg: bytes, bits: int = 256) -> bytes:
    """Повертає raw-тег HMAC-SHA3-<bits>."""
    h = HMAC.new(key, msg, _DIGEST_MAP[bits])
    return h.digest()


def verify_mac(key: bytes, msg: bytes, mac: bytes, bits: int = 256) -> bool:
    """True, якщо mac коректний."""
    try:
        h = HMAC.new(key, msg, _DIGEST_MAP[bits])
        h.verify(mac)                     # constant-time
        return True
    except ValueError:
        return False

#  CLI-інтерфейс

def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="hmac_sha3",
        description="HMAC-SHA-3 generator / verifier",
    )
    p.add_argument("-k", "--key", required=True,
                   help="секретний ключ у hex чи base64 (авто-детект)")
    p.add_argument("-d", "--digest", type=int, choices=(224, 256, 384, 512),
                   default=256, help="розмір тега (біт) [256]")
    p.add_argument("--format", choices=("hex", "base64"), default="hex",
                   help="формат виводу тега [hex]")

    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen", help="згенерувати тег")
    g.add_argument("-i", "--infile", type=pathlib.Path,
                   help="вхідний файл (якщо нема — stdin)")

    v = sub.add_parser("verify", help="перевірити тег")
    v.add_argument("tag",
                   help="файл із тегом або сам тег у hex/base64")
    v.add_argument("-i", "--infile", type=pathlib.Path,
                   help="вхідний файл (якщо нема — stdin)")

    return p.parse_args(argv)


def _decode_data(s: str | bytes) -> bytes:
    """auto-detect hex / base64 / literal bytes"""
    if isinstance(s, bytes):
        return s
    s = s.strip()
    try:
        return bytes.fromhex(s)
    except ValueError:
        return base64.b64decode(s)


def _read_msg(path: pathlib.Path | None) -> bytes:
    if path:
        return path.read_bytes()
    return sys.stdin.buffer.read()


def _main(argv: list[str]) -> None:
    args = _parse_args(argv)

    key = _decode_data(args.key)

    if args.cmd == "gen":
        msg = _read_msg(args.infile)
        mac = compute_mac(key, msg, args.digest)
        out = mac.hex() if args.format == "hex" else base64.b64encode(mac).decode()
        print(out)

    elif args.cmd == "verify":
        msg = _read_msg(args.infile)
        if pathlib.Path(args.tag).is_file():
            tag_str = pathlib.Path(args.tag).read_text().strip()
            tag_bytes = _decode_data(tag_str)     
        else:
            tag_bytes = _decode_data(args.tag)
        ok = verify_mac(key, msg, tag_bytes, args.digest)
        print("OK" if ok else "FAIL", file=sys.stderr)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    _main(sys.argv[1:])
