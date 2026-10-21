import random
import time

from objective import calculate_objective
from neighbor import copy_state, random_neighbor
from util import generate_random_state


def crossover(parent_a, parent_b, rng):
    child = {}
    for vid in parent_a:
        source = parent_a if rng.random() < 0.5 else parent_b
        child[vid] = dict(source[vid])
    return child

def mutate(state, mutation_rate, rng):
    if rng.random() < mutation_rate:
        state, _ = random_neighbor(state, data, rng)
    return state

def genetic_algorithm(data, population_size=50, iterations=200, seed=none, mutation_rate=0.5):
    rng = random.Random(seed)
    start_time = time.perf_counter()
    states = [generate_random_state(data, seed)]
    while len(states) < population_size:
        states.append(generate_random_state(data, rng, random.randrange(10**9)))
    population = [(calculate_objective(s, data), s) for s in states]
    population.sort(key=lambda p: p[0], reverse=True)

    history = {
        "algorithm": "Genetic Algorithm",
        "population_size": population_size,
        "iterations": iterations,
        "seed": seed,
        "initial_state": copy_state(population[0][1]),
        "initial_objective": population[0][0],
        "iteration_list": [0],
        "max_objectives": [population[0][0]],
        "avg_objectives": [sum(p[0] for p in population) / population_size],
    }

    for generation in range(1, iterations + 1):
        survivors = population[:population_size // 2]
        new_population = list(survivors)

        while len(new_population) < population_size:
            parent_a = rng.choice(survivors)[1]
            parent_b = rng.choice(survivors)[1]
            child = mutate(crossover(parent_a, parent_b, rng), data, mutation_rate, rng)
            new_population.append((calculate_objective(child, data), child))

        population = sorted(new_population, key=lambda p: p[0], reverse=True)
        history["iteration_list"].append(generation)
        history["max_objectives"].append(population[0][0])
        history["avg_objectives"].append(sum(p[0] for p in population) / population_size)

    best_score, best_state = population[0]
    history["final_state"] = copy_state(best_state)
    history["final_objective"] = best_score
    history["final_detail"] = calculate_objective(best_state, data, detail=True)
    history["final_total_fee"] = history["final_detail"]["total_fee"]
    history["final_valid"] = history["final_detail"]["valid"]
    history["objective_history"] = history["max_objectives"]
    history["duration_seconds"] = time.perf_counter() - start_time
    return history["final_state"], history