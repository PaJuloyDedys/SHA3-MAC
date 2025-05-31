# bench/bench_hmac_sha2.py
import os, timeit, csv, pathlib, secrets, hmac, hashlib

KEY     = secrets.token_bytes(32)
SIZES   = [2**n for n in range(0, 16)]      # 1 … 32768 байт
ROUNDS  = 300

rows = []
for size in SIZES:
    msg = os.urandom(size)
    t = timeit.timeit(
        lambda: hmac.new(KEY, msg, hashlib.sha256).digest(),
        number=ROUNDS
    )
    rows.append((size, (size * ROUNDS) / t))        # байт/сек

out = pathlib.Path(__file__).with_name("bench_sha2_256.csv")
with out.open("w", newline="") as f:
    csv.writer(f).writerows(rows)

print("CSV written:", out)
