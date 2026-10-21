import os
import sys

import matplotlib.pyplot as plt

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SRC)

import visualize
from report import cetak_state
from objective import load_input
from algorithm.hc_sideways_move import hill_climbing_sideways

NAMA = "Hill-Climbing with Sideways Move"


def samakan_kunci(result):
    """Menyesuaikan nama kunci hasil algoritma dengan yang dibaca visualize.py."""
    result["algorithm"] = NAMA
    result["objective_history"] = result["history"]
    result["duration_seconds"] = result["duration"]
    return result


def run(input_file="input1.json", seeds=(1, 2, 3), max_sideways=50):
    data = load_input(os.path.join(SRC, "data", input_file))
    results = []

    for seed in seeds:
        r = samakan_kunci(hill_climbing_sideways(data, seed=seed, max_sideways=max_sideways))
        results.append(r)
        print(f"seed {seed}: fee {r['final_detail']['total_fee']}, valid {r['final_detail']['valid']}, "
              f"durasi {r['duration']:.2f}s")
        print(f"  iterasi hingga berhenti: {r['iterations']} "
              f"(uphill {r['uphill_moves']}, sideways {r['sideways_moves']} dari maks {max_sideways})")
        print(f"  alasan berhenti        : {r['stop_reason']}")
        cetak_state(data, r["initial_state"], f"State awal (seed {seed})")
        cetak_state(data, r["final_state"], f"State akhir (seed {seed})")
        print()
        visualize.tampilkan_run(data, r, f"{input_file} | sideways {r['sideways_moves']}/{max_sideways}")

    visualize.plot_history_per_seed(results, f"{NAMA} - {input_file}")
    plt.show()
    return results


if __name__ == "__main__":
    run(input_file="input1.json")  