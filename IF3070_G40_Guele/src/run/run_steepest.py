import os
import sys

import matplotlib.pyplot as plt

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SRC)

import visualize
from objective import load_input
from algorithm.hc_steepest_ascent import steepest_ascent

NAMA = "Steepest Ascent Hill-Climbing"


def run(input_file="input1.json", seeds=(1, 2, 3), max_iterations=1000):
    data = load_input(os.path.join(SRC, "data", input_file))
    results = []

    for seed in seeds:
        r = steepest_ascent(data, seed=seed, max_iterations=max_iterations)
        r["algorithm"] = NAMA
        results.append(r)
        print(f"seed {seed}: fee {r['final_total_fee']}, valid {r['final_valid']}, "
              f"durasi {r['duration_seconds']:.3f}s")
        print(f"  iterasi hingga berhenti : {r['iterations']}")
        print(f"  tetangga dievaluasi     : {r['extra']['neighbors_evaluated']}")
        print(f"  alasan berhenti         : {r['extra']['stop_reason']}")
        visualize.tampilkan_run(data, r, input_file)

    fees = [r["final_total_fee"] for r in results]
    durasi = [r["duration_seconds"] for r in results]
    print(f"\n[{input_file}] fee rata-rata {sum(fees) / len(fees):.1f}, min {min(fees)}, max {max(fees)}, "
          f"durasi rata-rata {sum(durasi) / len(durasi):.3f}s")

    visualize.plot_history_per_seed(results, f"{NAMA} - {input_file}")
    plt.show()
    return results


if __name__ == "__main__":
    run(input_file="input1.json")   