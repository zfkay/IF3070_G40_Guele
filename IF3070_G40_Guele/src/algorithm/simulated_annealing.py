import math
import random
import time

from objective import calculate_objective
from neighbor import copy_state, random_neighbor
from util import generate_random_state

STUCK_TRESHOLD = 50

def simulated_annealing(data, initial_temp=50, cooling_rate=0.999, max_iterations=10000, min_temp=0.01, seed=None):
    rng = random.Random(seed)
    current_state = generate_random_state(data, seed)
    initial_state = copy_state(current_state)
    current_score = calculate_objective(current_state, data)
    best_state, best_score = copy_state(current_state), current_score

    temp = initial_temp
    history = [current_score]
    prob_history = []
    temp_history = []
    rejected_streak = 0
    stuck_count = 0
    stuck_events = 0
    iterations = 0

    start = time.perf_counter()
    while temp > min_temp and iterations < max_iterations:
        neighbor_state, _ = random_neighbor(current_state, data, rng)
        neighbor_score = calculate_objective(neighbor_state, data)
        delta = neighbor_score - current_score

        prob = 1.0 if delta > 0 else math.exp(delta / temp)
        prob_history.append(prob)
        temp_history.append(temp)

        if delta > 0 or rng.random() < prob:
            current_state, current_score = neighbor_state, neighbor_score
            rejected_streak = 0
            if current_score > best_score:
                best_state, best_score = copy_state(current_state), current_score
        else:
            rejected_streak += 1
            stuck_count += 1
            if rejected_streak == STUCK_TRESHOLD:
                stuck_events += 1

        history.append(current_score)
        temp *= cooling_rate
        iterations += 1
    duration = time.perf_counter() - start

    final_detail = calculate_objective(best_state, data, detail=True)
    return {
        "algorithm": "Simulated Annealing",
        "seed": seed,
        "initial_temp": initial_temp,
        "cooling_rate": cooling_rate,
        "initial_state": initial_state,
        "final_state": best_state,
        "initial_objective": history[0],
        "final_objective": best_score,
        "final_total_fee": final_detail["total_fee"],
        "final_valid": final_detail["valid"],
        "objective_history": history,
        "prob_history": prob_history,
        "temp_history": temp_history,
        "iterations": iterations,
        "stuck_count": stuck_count,
        "stuck_events": stuck_events,
        "duration_seconds": duration,
    }