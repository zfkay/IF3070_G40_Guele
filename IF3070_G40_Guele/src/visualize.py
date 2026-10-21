import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from objective import get_size, calculate_objective


def draw_state(ax, state, data, title):
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]
    vehicles = {v["id"]: v for v in data["Vehicles"]}

    cell_count = {}   
    outside = []     

    for vid, s in state.items():
        if not s["in_ship"]:
            outside.append(vid)
            continue
        w, l = get_size(vehicles[vid], s["Orientation"])
        ax.add_patch(Rectangle((s["x"], s["y"]), w, l,
                               facecolor="#9FE1CB", edgecolor="#0F6E56", linewidth=1.2))
        ax.text(s["x"] + w / 2, s["y"] + l / 2, vid, ha="center", va="center", fontsize=8)
        for cx in range(s["x"], s["x"] + w):
            for cy in range(s["y"], s["y"] + l):
                cell_count[(cx, cy)] = cell_count.get((cx, cy), 0) + 1

    for (cx, cy), n in cell_count.items():
        if n > 1:
            ax.add_patch(Rectangle((cx, cy), 1, 1, facecolor="red", alpha=0.6))

    ax.set_xlim(0, W)
    ax.set_ylim(L, 0)           
    ax.set_aspect("equal")
    ax.set_xticks(range(W + 1))
    ax.set_yticks(range(L + 1))
    ax.grid(True, linewidth=0.3)
    ax.set_title(title, fontsize=10)
    teks_luar = "Di luar kapal: " + (", ".join(outside) if outside else "-")
    ax.set_xlabel(textwrap.fill(teks_luar, 45), fontsize=8)   


def tampilkan_run(data, result, label=""):
    awal = calculate_objective(result["initial_state"], data, detail=True)
    akhir = calculate_objective(result["final_state"], data, detail=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    draw_state(axes[0], result["initial_state"], data,
               f"State awal (fee={awal['total_fee']}, valid={awal['valid']})")
    draw_state(axes[1], result["final_state"], data,
               f"State akhir (fee={akhir['total_fee']}, valid={akhir['valid']})")

    axes[2].plot(result["objective_history"])
    axes[2].set_yscale("symlog", linthresh=100)   
    axes[2].set_title("Objective vs iterasi")
    axes[2].set_xlabel("Iterasi")
    axes[2].set_ylabel("Objective")
    axes[2].grid(True, linewidth=0.3)

    fig.suptitle(f"[{label}] {result['algorithm']}  seed={result['seed']}  "
                 f"({result['iterations']} iterasi, {result['duration_seconds']:.3f} detik)")
    fig.tight_layout()


def plot_history_semua_run(results, judul):
    fig, ax = plt.subplots(figsize=(8, 5))
    for r in results:
        ax.plot(r["objective_history"], label=f"seed {r['seed']}")
    ax.set_yscale("symlog", linthresh=100)
    ax.set_title(judul)
    ax.set_xlabel("Iterasi")
    ax.set_ylabel("Objective")
    ax.grid(True, linewidth=0.3)
    ax.legend()
    fig.tight_layout()