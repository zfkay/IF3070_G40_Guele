import json

def load_input(path):
    with open(path) as f:
        return json.load(f)


def get_size(vehicle, orientation):
    w, l = vehicle["Dimensions"]["w"], vehicle["Dimensions"]["l"]
    return (w, l) if orientation == "Horizontal" else (l, w)

def calculate_weights(data):
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]
    n = len(data["Vehicles"])
    if any(v["ETA"] < 1 for v in data["Vehicles"]):
        raise ValueError("ETA harus bilangan bulat minimal 1")
    penalty = sum(v["ShippingFee"] for v in data["Vehicles"]) + 1
    eta_scale = 1 / (2 * n)          # total suku ETA paling besar 0.5
    epsilon = 1 / (2 * n * (W + L))  # total suku posisi di bawah 0.5
    return penalty, eta_scale, epsilon

def calculate_objective(state, data, detail=False):
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]
    capacity = data["Ship"]["MaxCapacity"]
    vehicles = {v["id"]: v for v in data["Vehicles"]}
    penalty, eta_scale, epsilon = calculate_weights(data)

    grid = [[0] * L for _ in range(W)]
    total_fee = 0
    eta_sum = 0
    total_eta = 0
    loaded = 0
    total_weight = 0
    out_of_bound_cells = 0
    position_sum = 0
    for vid, s in state.items():
        if not s["in_ship"]:
            continue
        v = vehicles[vid]
        width, length = get_size(v, s["Orientation"])
        total_fee += v["ShippingFee"]
        eta_sum += 1 / v["ETA"]
        total_eta += v["ETA"]
        loaded += 1
        total_weight += v["Weight"]
        position_sum += s["x"] + s["y"]
        for i in range(s["x"], s["x"] + width):
            for j in range(s["y"], s["y"] + length):
                if 0 <= i < W and 0 <= j < L:
                    grid[i][j] += 1
                else:
                    out_of_bound_cells += 1

    overlap_cells = sum(max(0, c - 1) for col in grid for c in col)
    overweight = max(0, total_weight - capacity)

    violation = overlap_cells + out_of_bound_cells + overweight
    eta_term = eta_scale * eta_sum
    objective = total_fee - penalty * violation + eta_term - epsilon * position_sum 
    if detail:
        return {
            "total_fee": total_fee,
            "eta_term": eta_term,
            "loaded_vehicles": loaded,
            "average_eta": total_eta / loaded if loaded else 0,
            "total_weight": total_weight,
            "overlap_cells": overlap_cells,
            "out_of_bound_cells": out_of_bound_cells,
            "overweight": overweight,
            "penalty_weight": penalty,
            "epsilon": epsilon,
            "position_sum": position_sum,
            "valid": violation == 0,
            "objective": objective,
        }
    return objective
