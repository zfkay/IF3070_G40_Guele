import time
from neighbor import all_neighbors, copy_state
from objective import calculate_objective
from util import generate_random_state

def steepest_ascent(data, seed=None, max_iterations=1000):
    current_state = generate_random_state(data, seed)
    initial_state = copy_state(current_state)
    current_score = calculate_objective(current_state, data, detail=False)
    score_list = [current_score]
    iterations = 0
    neighbor_evaluated = 0
    start_time = time.perf_counter()
    stop_reason = "max_iterations"

    for i in range (max_iterations):
        neighbors = all_neighbors(current_state, data)
       
        if not neighbors:
            stop_reason = "no_neighbor"
            break

        best_state = None
        best_score = None

        for neighbor_state, neighbor_move in neighbors:
            neighbor_score = calculate_objective(neighbor_state, data, detail=False)
            neighbor_evaluated += 1
            if best_score is None or neighbor_score > best_score :
                best_state = neighbor_state
                best_score = neighbor_score

        if best_score > current_score :
            current_state = best_state
            current_score = best_score
            iterations += 1
            score_list.append(current_score)
        else :
            stop_reason = "local_optimum"
            break

    duration = time.perf_counter() - start_time
    final_detail = calculate_objective(current_state, data, detail=True)
    
    return {
        "algorithm" : "steepest_ascent",
        "seed" : seed,
        "max_iterations" : max_iterations,
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
            "neighbors_evaluated" : neighbor_evaluated,
            "stop_reason" : stop_reason
        } 
    }

