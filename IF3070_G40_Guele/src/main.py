import matplotlib.pyplot as plt

from objective import load_input
from algorithm import hc_stochastic
import visualize

DATASETS = {
    "kecil": "src/data/input1.json",
    "besar": "src/data/input2.json",
}
SEEDS = [1, 2, 3]
PARAMS = {"max_iterations": 3000, "patience": 300}


def jalankan_stochastic(data, label):
    hasil = []
    for seed in SEEDS:
        result = hc_stochastic.stochastic_hill_climbing(data, seed=seed, **PARAMS)
        hasil.append(result)
        print(f"{label:<6} seed={seed}  fee={result['final_total_fee']}  "
              f"valid={result['final_valid']}  iterasi={result['iterations']}  "
              f"durasi={result['duration_seconds']:.3f}s")
    return hasil


def cetak_ringkasan(hasil, label):
    fees = [r["final_total_fee"] for r in hasil]
    durasi = [r["duration_seconds"] for r in hasil]
    print(f"[{label}] fee rata-rata={sum(fees) / len(fees):.1f}, min={min(fees)}, max={max(fees)}, "
          f"durasi rata-rata={sum(durasi) / len(durasi):.3f}s\n")


if __name__ == "__main__":
    for label, path in DATASETS.items():
        data = load_input(path)

        hasil = jalankan_stochastic(data, label)
        cetak_ringkasan(hasil, label)

        visualize.tampilkan_run(data, hasil[0], label)          
        visualize.plot_history_semua_run(
            hasil, f"[{label}] Stochastic hill-climbing: objective vs iterasi")

    plt.show()