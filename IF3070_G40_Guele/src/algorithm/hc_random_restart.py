import random
import time

from objective import calculate_objective
from neighbor import all_neighbors, copy_state
from util import generate_random_state

TIE_TOLERANCE = 1e-9 


def steepest_ascent(initial_state, data, rng, max_iterations=10000):
    current = copy_state(initial_state)
    current_value = calculate_objective(current, data)
    history = [current_value]
    iteration = 0

    while iteration < max_iterations:
        neighbors = all_neighbors(current, data)
        if not neighbors:
            break
        scored = [(calculate_objective(state, data), state) for state, _ in neighbors]
        best_value = max(value for value, _ in scored)
        if best_value <= current_value + TIE_TOLERANCE:
            break 
        best_candidates = [state for value, state in scored if abs(value - best_value) <= TIE_TOLERANCE]
        current, current_value = rng.choice(best_candidates), best_value
        iteration += 1
        history.append(current_value)

    return current, current_value, history, iteration


def random_restart_hill_climbing(data, initial_state=None, seed=None, max_restart=10, max_iterations=10000):
    rng = random.Random(seed)
    if initial_state is None:
        initial_state = generate_random_state(data, seed=seed)

    best_state, best_value = None, float("-inf")
    runs = []                
    history = []            
    best_history = []         
    restart_count = 0
    start_state = initial_state

    start = time.perf_counter()
    while True:
        run_start = time.perf_counter()
        final_state, final_value, run_history, run_iterations = steepest_ascent(start_state, data, rng, max_iterations)

        running_best = best_value
        for value in run_history:
            running_best = max(running_best, value)
            history.append(value)
            best_history.append(running_best)

        if final_value > best_value:
            best_state, best_value = final_state, final_value

        runs.append({
            "restart": restart_count,
            "initial_state": start_state,
            "final_state": final_state,
            "final_objective": final_value,
            "final_fee": calculate_objective(final_state, data, detail=True)["total_fee"],
            "iterations": run_iterations,
            "history": run_history,
            "duration": time.perf_counter() - run_start,
        })

        if restart_count >= max_restart:
            break
        restart_count += 1
        start_state = generate_random_state(data, seed=rng.randint(0, 10**9))
    duration = time.perf_counter() - start

    return {
        "initial_state": initial_state,
        "final_state": best_state,
        "initial_detail": calculate_objective(initial_state, data, detail=True),
        "final_detail": calculate_objective(best_state, data, detail=True),
        "final_objective": best_value,
        "history": history,
        "best_history": best_history,
        "runs": runs,
        "restarts": restart_count,
        "max_restart": max_restart,
        "iterations_per_restart": [r["iterations"] for r in runs],
        "total_iterations": sum(r["iterations"] for r in runs),
        "best_restart": max(runs, key=lambda r: r["final_objective"])["restart"],
        "duration": duration,
        "seed": seed,
    }