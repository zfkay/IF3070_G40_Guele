import random
from objective import get_size

MOVE_OUT_PROBABILITY = 0.3


def copy_state(state):
    return {vid: dict(s) for vid, s in state.items()}


def _deck(data):
    return data["Ship"]["Dimensions"]["w"], data["Ship"]["Dimensions"]["l"]


def _vehicle_map(data):
    return {v["id"]: v for v in data["Vehicles"]}


def _fit_inside(vehicle, orientation, x, y, W, L):
    for ori in (orientation, "Vertical" if orientation == "Horizontal" else "Horizontal"):
        width, length = get_size(vehicle, ori)
        if width <= W and length <= L:
            return ori, min(max(x, 0), W - width), min(max(y, 0), L - length)
    return None


def swap_vehicles(state, data, vid_a, vid_b):
    W, L = _deck(data)
    vehicles = _vehicle_map(data)
    new = copy_state(state)
    a, b = state[vid_a], state[vid_b]

    for vid, target in ((vid_a, b), (vid_b, a)):
        if target["in_ship"]:
            placed = _fit_inside(vehicles[vid], new[vid]["Orientation"], target["x"], target["y"], W, L)
            if placed:
                ori, x, y = placed
                new[vid] = {"in_ship": True, "x": x, "y": y, "Orientation": ori}
                continue
        new[vid] = {"in_ship": False, "x": None, "y": None, "Orientation": new[vid]["Orientation"]}
    return new


def move_vehicle(state, data, vid, rng=random):
    W, L = _deck(data)
    vehicle = _vehicle_map(data)[vid]
    new = copy_state(state)
    s = new[vid]

    if s["in_ship"] and rng.random() < MOVE_OUT_PROBABILITY:
        new[vid] = {"in_ship": False, "x": None, "y": None, "Orientation": s["Orientation"]}
        return new

    placed = _fit_inside(vehicle, s["Orientation"], 0, 0, W, L)
    if placed is None:
        return new
    ori, _, _ = placed
    width, length = get_size(vehicle, ori)

    for _ in range(20):
        x = rng.randint(0, W - width)
        y = rng.randint(0, L - length)
        if not (s["in_ship"] and x == s["x"] and y == s["y"] and ori == s["Orientation"]):
            break
    new[vid] = {"in_ship": True, "x": x, "y": y, "Orientation": ori}
    return new

def move_to(state, vid, x, y, orientation):
    new = copy_state(state)
    new[vid] = {"in_ship": True, "x": x, "y": y, "Orientation": orientation}
    return new


def move_out(state, vid):
    new = copy_state(state)
    new[vid] = {"in_ship": False, "x": None, "y": None, "Orientation": state[vid]["Orientation"]}
    return new


def rotate_vehicle(state, data, vid):
    W, L = _deck(data)
    vehicle = _vehicle_map(data)[vid]
    new = copy_state(state)
    s = new[vid]
    new_ori = "Vertical" if s["Orientation"] == "Horizontal" else "Horizontal"

    if not s["in_ship"]:
        new[vid]["Orientation"] = new_ori
        return new

    width, length = get_size(vehicle, new_ori)
    if width > W or length > L:
        return new  

    x = min(s["x"], W - width)
    y = min(s["y"], L - length)
    new[vid] = {"in_ship": True, "x": x, "y": y, "Orientation": new_ori}
    return new


def _one_neighbor(state, data, rng):
    ids = list(state.keys())
    in_ship = [vid for vid in ids if state[vid]["in_ship"]]
    move_type = rng.choice(["swap", "move", "rotate"])

    if move_type in ("swap", "rotate") and not in_ship:
        move_type = "move"
    if move_type == "swap" and len(ids) < 2:
        move_type = "move"

    if move_type == "swap":
        vid_a = rng.choice(in_ship)
        vid_b = rng.choice([vid for vid in ids if vid != vid_a])
        return swap_vehicles(state, data, vid_a, vid_b), ("swap", vid_a, vid_b)

    if move_type == "rotate":
        vid = rng.choice(in_ship)
        return rotate_vehicle(state, data, vid), ("rotate", vid)

    vid = rng.choice(ids)
    return move_vehicle(state, data, vid, rng), ("move", vid)


def random_neighbor(state, data, rng=random, max_try=20):
    for _ in range(max_try):
        new, move = _one_neighbor(state, data, rng)
        if new != state:
            return new, move
    return new, move

def sample_neighbors(state, data, k, rng=random):
    return [random_neighbor(state, data, rng) for _ in range(k)]

def all_neighbors(state, data):
    W, L = _deck(data)
    vehicles = _vehicle_map(data)
    ids = list(state.keys())
    result = []

    for a in ids:
        if not state[a]["in_ship"]:
            continue
        for b in ids:
            if b == a or (state[b]["in_ship"] and b < a): 
                continue
            new = swap_vehicles(state, data, a, b)
            if new != state:
                result.append((new, ("swap", a, b)))

    for vid in ids:
        if state[vid]["in_ship"]:
            new = rotate_vehicle(state, data, vid)
            if new != state:
                result.append((new, ("rotate", vid)))

    for vid in ids:
        s = state[vid]
        placed = _fit_inside(vehicles[vid], s["Orientation"], 0, 0, W, L)
        if placed is not None:
            ori, _, _ = placed
            width, length = get_size(vehicles[vid], ori)
            for x in range(W - width + 1):
                for y in range(L - length + 1):
                    if s["in_ship"] and (x, y, ori) == (s["x"], s["y"], s["Orientation"]):
                        continue
                    result.append((move_to(state, vid, x, y, ori), ("move", vid, x, y)))
        if s["in_ship"]:
            result.append((move_out(state, vid), ("move_out", vid)))

    return result