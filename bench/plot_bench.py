import matplotlib.pyplot as plt, csv, pathlib

BASE = pathlib.Path(__file__).parent        # ← директорія bench/

def read(name):                             # name = "bench_sha3_256.csv"
    with (BASE / name).open() as f:
        return list(csv.reader(f, quoting=1))

# --- SHA-3 ---
sizes3, speed3 = zip(*[(int(r[0]), float(r[1])) for r in read("bench_sha3_256.csv")])
plt.plot(sizes3, speed3, marker="o", label="SHA-3-256")

# --- SHA-2 ---
sizes2, speed2 = zip(*[(int(r[0]), float(r[1])) for r in read("bench_sha2_256.csv")])
plt.plot(sizes2, speed2, marker="x", linestyle="--", label="SHA-2-256")

plt.xscale("log"); plt.yscale("log")
plt.xlabel("Message size, bytes"); plt.ylabel("Throughput, bytes/s")
plt.title("HMAC throughput: SHA-3-256 vs SHA-2-256")
plt.legend()
plt.savefig(BASE / "throughput_sha3_vs_sha2.png", dpi=150)
plt.show()
