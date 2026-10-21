import os
import sys

import matplotlib.pyplot as plt

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SRC)

import visualize
from objective import load_input
from algorithm.genetic_algorithm import genetic_algorithm

NAMA = "Genetic Algorithm"


def plot_max_avg_per_seed(results, judul):
    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4), squeeze=False)
    for ax, r in zip(axes[0], results):
        ax.plot(r["iteration_list"], r["max_objectives"], label="maksimum")
        ax.plot(r["iteration_list"], r["avg_objectives"], label="rata-rata")
        ax.set_yscale("symlog", linthresh=100)
        ax.set_title(f"seed {r['seed']}")
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("Objective")
        ax.grid(True, linewidth=0.3)
        ax.legend(fontsize=8)
    fig.suptitle(judul)
    fig.tight_layout()


def run(input_file="input1.json", seeds=(1, 2, 3), population_size=50, iterations=200, mutation_rate=0.5):
    data = load_input(os.path.join(SRC, "data", input_file))
    results = []

    for seed in seeds:
        _, r = genetic_algorithm(data, population_size=population_size, iterations=iterations,
                                 seed=seed, mutation_rate=mutation_rate)
        results.append(r)
        print(f"seed {seed}: fee {r['final_total_fee']}, valid {r['final_valid']}, "
              f"durasi {r['duration_seconds']:.3f}s")
        print(f"  jumlah populasi: {population_size}, banyak iterasi: {iterations}, mutation rate: {mutation_rate}")
        visualize.tampilkan_run(data, r, f"{input_file} | populasi {population_size}")

    fees = [r["final_total_fee"] for r in results]
    durasi = [r["duration_seconds"] for r in results]
    print(f"\n[{input_file}] fee rata-rata {sum(fees) / len(fees):.1f}, min {min(fees)}, max {max(fees)}, "
          f"durasi rata-rata {sum(durasi) / len(durasi):.3f}s")

    plot_max_avg_per_seed(
        results, f"{NAMA} - {input_file} (populasi {population_size}, iterasi {iterations})")
    plt.show()
    return results


if __name__ == "__main__":
    run(input_file="input1.json") 