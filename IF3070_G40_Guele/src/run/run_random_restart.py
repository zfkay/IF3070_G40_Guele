import os
import sys

import matplotlib.pyplot as plt

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SRC)

import visualize
from objective import load_input
from algorithm.hc_random_restart import random_restart_hill_climbing

NAMA = "Random Restart Hill-Climbing"


def samakan_kunci(result):
    result["algorithm"] = NAMA
    result["objective_history"] = result["history"]
    result["duration_seconds"] = result["duration"]
    result["iterations"] = result["total_iterations"]
    return result


def run(input_file="input1.json", seeds=(1, 2, 3), max_restart=10):
    data = load_input(os.path.join(SRC, "data", input_file))
    results = []

    for seed in seeds:
        r = samakan_kunci(random_restart_hill_climbing(data, seed=seed, max_restart=max_restart))
        results.append(r)
        fees = [run_["final_fee"] for run_ in r["runs"]]
        print(f"seed {seed}: fee {r['final_detail']['total_fee']}, valid {r['final_detail']['valid']}, "
              f"durasi {r['duration']:.2f}s")
        print(f"  banyak restart       : {r['restarts']} (maks {max_restart})")
        print(f"  iterasi per restart  : {r['iterations_per_restart']}")
        print(f"  fee akhir per restart: {fees}")
        print(f"  terbaik dari restart ke-{r['best_restart']}")
        visualize.tampilkan_run(data, r, f"{input_file} | {r['restarts']} restart")

    visualize.plot_history_per_seed(results, f"{NAMA} - {input_file}")
    plt.show()
    return results


if __name__ == "__main__":
    run(input_file="input1.json") 