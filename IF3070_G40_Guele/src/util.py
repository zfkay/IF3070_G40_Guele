import random
from objective import get_size

ORIENTATIONS = ["Horizontal", "Vertical"]


def fits_in_deck(vehicle, orientation, W, L):
    width, length = get_size(vehicle, orientation)
    return width <= W and length <= L


def generate_random_state(data, seed=None):
    rng = random.Random(seed)
    W = data["Ship"]["Dimensions"]["w"]
    L = data["Ship"]["Dimensions"]["l"]

    state = {}
    for v in data["Vehicles"]:
        orientation = rng.choice(ORIENTATIONS)

        if not fits_in_deck(v, orientation, W, L):
            orientation = "Vertical" if orientation == "Horizontal" else "Horizontal"

        if rng.random() < 0.5 and fits_in_deck(v, orientation, W, L):
            width, length = get_size(v, orientation)
            x = rng.randint(0, W - width)
            y = rng.randint(0, L - length)
            state[v["id"]] = {"in_ship": True, "x": x, "y": y, "Orientation": orientation}
        else:
            state[v["id"]] = {"in_ship": False, "x": None, "y": None, "Orientation": orientation}

    return state
