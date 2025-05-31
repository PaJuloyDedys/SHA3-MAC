# bench/bench_hmac.py
import os, timeit, csv, pathlib, secrets, sys
sys.path.append(str(pathlib.Path(__file__).parents[1] / "src"))
import hmac_sha3

KEY = secrets.token_bytes(32)
SIZES = [2**n for n in range(0, 16)]   # 1..32768 B
ROUNDS = 300

rows = []
for size in SIZES:
    msg = os.urandom(size)
    t = timeit.timeit(
        lambda: hmac_sha3.compute_mac(KEY, msg, 256),
        number=ROUNDS
    )
    rows.append((size, (size*ROUNDS) / t))   # bytes per second

with open("bench_sha3_256.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)
print("CSV written: bench_sha3_256.csv")
