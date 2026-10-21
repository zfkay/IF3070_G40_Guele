import os
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)

from run import run_steepest_ascent, run_stochastic_move, run_sideways_move, run_random_restart, run_simulated_annealing, run_genetic_algorithm

DATA_DIR = os.path.join(SRC, "data")

ALGORITHMS = [
    ("Steepest Ascent Hill-Climbing", run_steepest_ascent.run, {"max_iterations": 1000}),
    ("Stochastic Hill-Climbing", run_stochastic_move.run, {"max_iterations": 3000, "patience": 300}),
    ("Hill-Climbing with Sideways Move", run_sideways_move.run, {"max_sideways": 50}),
    ("Random Restart Hill-Climbing", run_random_restart.run, {"max_restart": 10}),
    ("Simulated Annealing", run_simulated_annealing.run,
     {"initial_temp": 50.0, "cooling_rate": 0.999, "max_iterations": 10000, "min_temp": 0.01}),
    ("Genetic Algorithm", run_genetic_algorithm.run,
     {"population_size": 50, "iterations": 200, "mutation_rate": 0.5}),
]


def pilih(judul, pilihan):
    print(f"\n{judul}")
    for i, teks in enumerate(pilihan, start=1):
        print(f"  {i}. {teks}")
    while True:
        jawaban = input(f"Pilih nomor (1-{len(pilihan)}): ").strip()
        if jawaban.isdigit() and 1 <= int(jawaban) <= len(pilihan):
            return int(jawaban) - 1
        print("  Pilihan tidak valid, coba lagi.")


def minta_angka(nama, default):
    tipe = float if isinstance(default, float) else int
    while True:
        jawaban = input(f"  {nama} [default {default}]: ").strip().replace(",", ".")
        if jawaban == "":
            return default
        try:
            nilai = tipe(jawaban)
        except ValueError:
            contoh = "0.5" if tipe is float else "100"
            print(f"  Masukkan angka seperti {contoh}, atau tekan Enter untuk default.")
            continue
        if nilai < 0:
            print("  Angka tidak boleh negatif.")
            continue
        return nilai


def minta_seed(default=(1, 2, 3)):
    teks_default = ", ".join(str(s) for s in default)
    while True:
        jawaban = input(f"  seed, pisahkan dengan koma [default {teks_default}]: ").strip()
        if jawaban == "":
            return tuple(default)
        try:
            return tuple(int(s) for s in jawaban.split(",") if s.strip() != "")
        except ValueError:
            print("  Format salah. Contoh: 1, 2, 3")


def main():
    print("=" * 60)
    print(" Penataan Kendaraan pada Geladak Kapal - Local Search")
    print("=" * 60)

    while True:
        input_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".json"))
        if not input_files:
            print(f"Tidak ada file input .json di {DATA_DIR}")
            return

        input_file = input_files[pilih("File input:", input_files)]
        nama, run_func, defaults = ALGORITHMS[pilih("Algoritma:", [a[0] for a in ALGORITHMS])]

        print("\nParameter (tekan Enter untuk memakai nilai default):")
        params = {key: minta_angka(key, value) for key, value in defaults.items()}
        seeds = minta_seed()

        print(f"\nMenjalankan {nama} pada {input_file} dengan seed {seeds} dan parameter {params}")
        print("Tutup semua jendela gambar untuk kembali ke menu.\n")
        run_func(input_file=input_file, seeds=seeds, **params)

        lagi = input("\nJalankan lagi? (y/n): ").strip().lower()
        if lagi != "y":
            print("Selesai.")
            break


if __name__ == "__main__":
    main()