# Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial 2026/2027

**Kelompok G40 - Guele**

Implementasi algoritma *local search* untuk permasalahan **penataan kendaraan pada geladak kapal kargo**. Program memilih kendaraan yang diangkut serta menentukan posisi dan orientasinya di geladak, dengan tujuan memaksimalkan total *ShippingFee* tanpa melanggar batasan berikut:

1. Kendaraan tidak boleh saling bertumpuk.
2. Seluruh bagian kendaraan harus berada di dalam geladak.
3. Total berat kendaraan tidak boleh melebihi kapasitas kapal.

## Algoritma yang Diimplementasikan

1. Steepest Ascent Hill-Climbing
2. Stochastic Hill-Climbing
3. Hill-Climbing with Sideways Move
4. Random Restart Hill-Climbing
5. Simulated Annealing
6. Genetic Algorithm

## Struktur Folder

```
src/
├── algorithm/
│   ├── hc_steepest_ascent.py      
│   ├── hc_stochastic.py          
│   ├── hc_sideways_move.py       
│   ├── hc_random_restart.py       
│   ├── simulated_annealing.py     
│   └── genetic_algorithm.py       
├── data/
│   ├── input1.json               
│   └── input2.json                20
├── run/
│   ├── run_steepest_ascent.py
│   ├── run_stochastic_move.py
│   ├── run_sideways_move.py
│   ├── run_random_restart.py
│   ├── run_simulated_annealing.py
│   └── run_genetic_algorithm.py
├── main.py                        # menu utama program
├── objective.py                   # objective function
├── neighbor.py                    # fungsi tetangga (swap, move, rotate)
├── util.py                        # pembangkitan state awal acak
├── visualize.py                   # visualisasi state dan grafik
└── report.py                      # cetak state ke terminal
```

## Kebutuhan

- Python 3.10 atau lebih baru
- matplotlib

Pasang matplotlib dengan:

```
python -m pip install matplotlib
```

## Cara Menjalankan

### Melalui menu utama

Dari folder `src`, jalankan:

```
python main.py
```

Lalu ikuti menu di terminal:

1. Pilih file input. Daftar diambil otomatis dari seluruh file `.json` di folder `data`.
2. Pilih algoritma.
3. Isi parameter algoritma, atau tekan Enter untuk memakai nilai *default*.
4. Isi *seed* dipisahkan koma, atau tekan Enter untuk memakai `1, 2, 3`.
5. Hasil dicetak di terminal dan jendela visualisasi akan muncul. Tutup seluruh jendela visualisasi untuk kembali ke menu.
6. Pilih `y` untuk menjalankan lagi atau `n` untuk keluar.

### Menjalankan satu algoritma secara langsung

Setiap file di folder `run` dapat dijalankan sendiri, misalnya:

```
python run/run_simulated_annealing.py
```

File input untuk cara ini diatur pada baris paling bawah file `run` yang bersangkutan.

## Parameter Algoritma

| Algoritma | Parameter | Default |
|---|---|---|
| Steepest Ascent Hill-Climbing | `max_iterations` | 1000 |
| Stochastic Hill-Climbing | `max_iterations`, `patience` | 3000, 300 |
| Hill-Climbing with Sideways Move | `max_sideways` | 50 |
| Random Restart Hill-Climbing | `max_restart` | 10 |
| Simulated Annealing | `initial_temp`, `cooling_rate`, `max_iterations`, `min_temp` | 50.0, 0.999, 10000, 0.01 |
| Genetic Algorithm | `population_size`, `iterations`, `mutation_rate` | 50, 200, 0.5 |

*Seed* yang sama selalu menghasilkan state awal dan hasil yang sama, sehingga setiap eksperimen dapat diulang dan seluruh algoritma dapat dibandingkan dari titik awal yang sama.

## Keluaran Program

1. **Terminal:** ringkasan hasil setiap *seed* (total *ShippingFee*, status valid, durasi, serta informasi khusus tiap algoritma), lalu state awal dan state akhir berupa tabel posisi seluruh kendaraan dan gambar geladak dalam bentuk teks.
2. **Jendela visualisasi:** gambar state awal dan state akhir, grafik nilai *objective function* terhadap iterasi untuk setiap *seed*, grafik e^(ΔE/T) untuk Simulated Annealing, serta grafik nilai maksimum dan rata-rata populasi untuk Genetic Algorithm.

## Pembagian Tugas

| Nama | NIM | Tugas |
|---|---|---|
| Zhafira Kayla Nafisa | 18224018 | Steepest Ascent, Stochastic |
| Kayla Fiyaza Nawal Zaghbi | 18224054 | Simulated Annealing, Genetic Algorithm |
| Nabilla Eka Putri Sunarto | 18224056 | Random Restart, Sideways Move |