import json

def load_input(path):
    with open(path) as f:
        return json.load(f)


def get_size(vehicle, orientation):
    w, l = vehicle["Dimensions"]["w"], vehicle["Dimensions"]["l"]
    return (w, l) if orientation == "Horizontal" else (l, w)


def get_value(vehicle, mode="fee"):
    if mode == "urgency":
        return vehicle["ShippingFee"] * (1 + 1 / vehicle["ETA"])
    return vehicle["ShippingFee"]


def calculate_penalty_weights(data, mode="fee"):
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]
    n = len(data["Vehicles"])
    penalty = sum(get_value(v, mode) for v in data["Vehicles"]) + 1
    if mode == "urgency":
        epsilon = 1 / (100 * n * (W + L))
    else:
        epsilon = 1 / (n * (W + L))
    return penalty, epsilon


def calculate_objective(state, data, detail=False, mode="fee"):
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]
    capacity = data["Ship"]["MaxCapacity"]
    vehicles = {v["id"]: v for v in data["Vehicles"]}
    penalty, epsilon = calculate_penalty_weights(data, mode)

    grid = [[0] * L for _ in range(W)]
    total_fee = 0
    total_value = 0 
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
        total_value += get_value(v, mode)
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
    objective = total_value - penalty * violation - epsilon * position_sum

    if detail:
        return {
            "mode": mode,
            "total_fee": total_fee,
            "total_value": total_value,
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
