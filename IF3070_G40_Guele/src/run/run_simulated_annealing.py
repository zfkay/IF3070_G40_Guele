import os
import sys

import matplotlib.pyplot as plt

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SRC)

import visualize
from report import cetak_state
from objective import load_input
from algorithm.simulated_annealing import simulated_annealing, STUCK_TRESHOLD

NAMA = "Simulated Annealing"


def plot_prob_per_seed(results, judul):
    """Plot e^(ΔE/T) terhadap iterasi, satu grafik per seed."""
    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4), squeeze=False)
    for ax, r in zip(axes[0], results):
        ax.scatter(range(1, len(r["prob_history"]) + 1), r["prob_history"], s=2, alpha=0.5)
        ax.set_ylim(-0.05, 1.05)
        ax.set_title(f"seed {r['seed']}")
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("e^(ΔE/T), bernilai 1 jika ΔE > 0")
        ax.grid(True, linewidth=0.3)
    fig.suptitle(judul)
    fig.tight_layout()


def run(input_file="input1.json", seeds=(1, 2, 3), initial_temp=50.0, cooling_rate=0.999,
        max_iterations=10000, min_temp=0.01):
    data = load_input(os.path.join(SRC, "data", input_file))
    results = []

    for seed in seeds:
        r = simulated_annealing(data, initial_temp=initial_temp, cooling_rate=cooling_rate,
                                max_iterations=max_iterations, min_temp=min_temp, seed=seed)
        results.append(r)
        frekuensi = r["stuck_events"] / r["iterations"] if r["iterations"] else 0
        print(f"seed {seed}: fee {r['final_total_fee']}, valid {r['final_valid']}, "
              f"durasi {r['duration_seconds']:.3f}s")
        print(f"  iterasi                   : {r['iterations']}")
        print(f"  suhu akhir                : {r['temp_history'][-1]:.4f}" if r["temp_history"] else "")
        print(f"  frekuensi stuck           : {r['stuck_events']} kali "
              f"(ditolak {STUCK_TRESHOLD} kali berturut-turut), {frekuensi:.4f} per iterasi")
        print(f"  total tetangga ditolak    : {r['stuck_count']}")
        cetak_state(data, r["initial_state"], f"State awal (seed {seed})")
        cetak_state(data, r["final_state"], f"State akhir (seed {seed})")
        print()
        visualize.tampilkan_run(data, r, f"{input_file} | stuck {r['stuck_events']}")

    fees = [r["final_total_fee"] for r in results]
    durasi = [r["duration_seconds"] for r in results]
    print(f"\n[{input_file}] fee rata-rata {sum(fees) / len(fees):.1f}, min {min(fees)}, max {max(fees)}, "
          f"durasi rata-rata {sum(durasi) / len(durasi):.3f}s")

    visualize.plot_history_per_seed(results, f"{NAMA} - {input_file}: objective vs iterasi")
    plot_prob_per_seed(results, f"{NAMA} - {input_file}: e^(ΔE/T) vs iterasi")
    plt.show()
    return results


if __name__ == "__main__":
    run(input_file="input1.json")   