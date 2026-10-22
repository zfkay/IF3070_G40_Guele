import random
import time

from objective import calculate_objective, get_size
from neighbor import all_neighbors, copy_state
from util import generate_random_state

TIE_TOLERANCE = 1e-9


def layout_key(state, vehicles):
    loaded = frozenset(vid for vid, s in state.items() if s["in_ship"])
    rects = frozenset(
        (s["x"], s["y"]) + get_size(vehicles[vid], s["Orientation"])
        for vid, s in state.items() if s["in_ship"]
    )
    return loaded, rects


def hill_climbing_sideways(data, initial_state=None, seed=None, max_sideways=100, max_iterations=10000):
    rng = random.Random(seed)
    vehicles = {v["id"]: v for v in data["Vehicles"]}
    if initial_state is None:
        initial_state = generate_random_state(data, seed=seed)

    current = copy_state(initial_state)
    current_value = calculate_objective(current, data)

    history = [current_value]  
    moves = []    
    iteration = 0             
    sideways_count = 0
    uphill_count = 0
    stop_reason = "max_iterations"
    plateau_visited = {layout_key(current, vehicles)}

    start = time.perf_counter()
    while iteration < max_iterations:
        neighbors = all_neighbors(current, data)
        if not neighbors:
            stop_reason = "no_neighbor"
            break

        scored = [(calculate_objective(state, data), state, move) for state, move in neighbors]
        best_value = max(value for value, _, _ in scored)
        best_candidates = [(s, m) for v, s, m in scored if abs(v - best_value) <= TIE_TOLERANCE]

        if best_value > current_value + TIE_TOLERANCE:
            best_state, best_move = rng.choice(best_candidates)
            uphill_count += 1
            move_kind = "uphill"
            plateau_visited = {layout_key(best_state, vehicles)}
        elif abs(best_value - current_value) <= TIE_TOLERANCE:
            if sideways_count >= max_sideways:
                stop_reason = "max_sideways"
                break
            fresh = [(s, m) for s, m in best_candidates if layout_key(s, vehicles) not in plateau_visited]
            if not fresh:
                stop_reason = "plateau_exhausted"
                break
            best_state, best_move = rng.choice(fresh)
            sideways_count += 1
            move_kind = "sideways"
            plateau_visited.add(layout_key(best_state, vehicles))
        else:
            stop_reason = "local_optimum"
            break

        current, current_value = best_state, best_value
        iteration += 1
        history.append(current_value)
        moves.append((move_kind, best_move))
    duration = time.perf_counter() - start

    return {
        "initial_state": initial_state,
        "final_state": current,
        "initial_detail": calculate_objective(initial_state, data, detail=True),
        "final_detail": calculate_objective(current, data, detail=True),
        "final_objective": current_value,
        "history": history,
        "moves": moves,
        "iterations": iteration,
        "uphill_moves": uphill_count,
        "sideways_moves": sideways_count,
        "max_sideways": max_sideways,
        "stop_reason": stop_reason,
        "duration": duration,
        "seed": seed,
    }