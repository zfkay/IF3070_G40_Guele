from objective import get_size, calculate_objective


def cetak_state(data, state, judul):
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]
    vehicles = {v["id"]: v for v in data["Vehicles"]}
    d = calculate_objective(state, data, detail=True)

    print(f"\n  ===== {judul} =====")
    status = "VALID" if d["valid"] else (
        f"TIDAK VALID (tumpuk {d['overlap_cells']} sel, keluar {d['out_of_bound_cells']} sel, "
        f"lebih berat {d['overweight']})")
    print(f"  Fee {d['total_fee']} juta | berat {d['total_weight']}/{data['Ship']['MaxCapacity']} | "
          f"objective {d['objective']:.4f} | {status}")

    print(f"  {'ID':<5}{'Status':<14}{'x':>3}{'y':>4}  {'Orientasi':<11}{'Ukuran':<8}{'Fee':>4}{'Berat':>7}{'ETA':>5}")
    for vid, s in state.items():
        v = vehicles[vid]
        w, l = get_size(v, s["Orientation"])
        if s["in_ship"]:
            posisi = f"{'di dalam':<14}{s['x']:>3}{s['y']:>4}"
        else:
            posisi = f"{'di luar kapal':<14}{'-':>3}{'-':>4}"
        print(f"  {vid:<5}{posisi}  {s['Orientation']:<11}{f'{w}x{l}':<8}"
              f"{v['ShippingFee']:>4}{v['Weight']:>7}{v['ETA']:>5}")

    # gambar geladak
    grid = [["." for _ in range(W)] for _ in range(L)]
    for vid, s in state.items():
        if not s["in_ship"]:
            continue
        w, l = get_size(vehicles[vid], s["Orientation"])
        for x in range(s["x"], s["x"] + w):
            for y in range(s["y"], s["y"] + l):
                if 0 <= x < W and 0 <= y < L:
                    grid[y][x] = vid if grid[y][x] == "." else "##"
    lebar = max(len(v["id"]) for v in data["Vehicles"]) + 1
    print("\n  Geladak (kolom = x, baris = y):")
    print("      " + "".join(f"{x:>{lebar}}" for x in range(W)))
    for y, baris in enumerate(grid):
        print(f"  {y:>3} " + "".join(f"{c:>{lebar}}" for c in baris))