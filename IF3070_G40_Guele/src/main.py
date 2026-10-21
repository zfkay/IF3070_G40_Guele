import os
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)

from run import run_stochastic_move, run_sideways_move, run_random_restart

DATA_DIR = os.path.join(SRC, "data")

ALGORITHMS = [
    ("Stochastic Hill-Climbing", run_stochastic_move.run, {"max_iterations": 3000, "patience": 300}),
    ("Hill-Climbing with Sideways Move", run_sideways_move.run, {"max_sideways": 50}),
    ("Random Restart Hill-Climbing", run_random_restart.run, {"max_restart": 10}),
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
    while True:
        jawaban = input(f"  {nama} [default {default}]: ").strip()
        if jawaban == "":
            return default
        if jawaban.isdigit() and int(jawaban) >= 0:
            return int(jawaban)
        print("  Masukkan bilangan bulat, atau tekan Enter untuk default.")


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