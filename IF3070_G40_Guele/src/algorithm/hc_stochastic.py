import random
import time
from objective import calculate_objective
from neighbor import random_neighbor, copy_state
from util import generate_random_state

def stochastic_hill_climbing(data, seed=None, max_iterations=1000, patience=100):
    rng = random.Random(seed)
    current_state = generate_random_state(data, seed)
    initial_state = copy_state(current_state)
    current_score = calculate_objective(current_state, data, detail=False)
    score_list = [current_score]
    worse_move_count = 0
    iterations = 0
    start_time = time.perf_counter()
    stop_reason = "max_iterartios"
    accepted_moves = 0
    
    for i in range (max_iterations):
        neighbor_state, neighbor_move = random_neighbor(current_state, data, rng)
        neighbor_score = calculate_objective(neighbor_state, data, detail=False)

        if neighbor_score > current_score :
            current_state = neighbor_state 
            current_score = neighbor_score
            worse_move_count = 0
            accepted_moves += 1
        else :
            worse_move_count += 1

        score_list.append(current_score)
        iterations += 1
        
        if worse_move_count >= patience :
            stop_reason = "patience"
            break

    duration = time.perf_counter() - start_time
    final_detail = calculate_objective(current_state, data, detail=True)
    
    return {
        "algorithm" : "stochastic_hill_climbing",
        "seed" : seed,
        "max_iterations" : max_iterations,
        "patience" : patience,
        "initial_state" : initial_state,
        "final_state" : current_state,
        "initial_objective" : score_list[0],
        "final_objective" : current_score,
        "final_total_fee" : final_detail["total_fee"],
        "final_valid" : final_detail["valid"],
        "objective_history" : score_list,
        "iterations" : iterations,
        "duration_seconds" : duration,
        "extra" : {
            "stop_reason" : stop_reason,
            "accepted_moves" : accepted_moves,
            "final_worse_count" : worse_move_count,
            } 
    }
