from travelling_salesman_problem.data.data_generator import get_data_from_file
from travelling_salesman_problem.algorithm.neighbours import get_random_swap, get_random_starting_state
import travelling_salesman_problem.algorithm.calculator as calculator
import random
from math import log, log2


def annealing1(i):
    return 1


def annealing2(i, c):
    return c/log(i+2)


def solve_max_steps1(filename_or_distances, steps):
    try:
        distances = get_data_from_file(filename_or_distances)
    except:
        distances = filename_or_distances
    size = len(distances)
    current_state = get_random_starting_state(size)
    current_state_func = calculator.calculate_distance(current_state, distances)
    best_state = current_state[:]
    best_func = current_state_func
    best_step = 0
    for step in range(0, steps):
        swap = get_random_swap(size)
        update = calculator.get_state_function_update1(distances, current_state, swap)
        u = log(random.random())
        if u < update / annealing1(step):
            calculator.update_state(current_state, swap)
            current_state_func -= update
            if current_state_func < best_func:
                best_step = step
                best_func = current_state_func
    return best_func, best_step


def solve_convergence1(filename_or_distances, c):
    try:
        distances = get_data_from_file(filename_or_distances)
    except:
        distances = filename_or_distances
    size = len(distances)
    current_state = get_random_starting_state(size)
    current_state_func = calculator.calculate_distance(current_state, distances)
    best_func = current_state_func
    best_step = 0
    step = 0
    current_stay = 0
    while current_stay < 0.9*size*log2(size) and step < min(10*size*size, 10000000):
        step += 1
        swap = get_random_swap(size)
        update = calculator.get_state_function_update1(distances, current_state, swap)
        u = log(random.random())
        if u < update / annealing2(step, c):
            current_stay = 0
            calculator.update_state(current_state, swap)
            current_state_func -= update
            if current_state_func < best_func:
                best_func = current_state_func
                best_step = step
        else:
            current_stay += 1
    return best_func, best_step, current_state_func, step


def solve_max_steps2(filename_or_distances, steps):
    try:
        distances = get_data_from_file(filename_or_distances)
    except:
        distances = filename_or_distances
    size = len(distances)
    current_state = get_random_starting_state(size)
    current_state_func = calculator.calculate_distance(current_state, distances)
    best_func = current_state_func
    best_step = 0
    for step in range(0, steps):
        swap = get_random_swap(size)
        update = calculator.get_state_function_update2(distances, current_state, swap)
        u = log(random.random())
        if u < update / annealing1(step):
            calculator.update_state_reverse_swap(current_state, swap)
            current_state_func -= update
            if current_state_func < best_func:
                best_step = step
                best_func = current_state_func
    return best_func, best_step


def solve_convergence2(filename_or_distances, c):
    try:
        distances = get_data_from_file(filename_or_distances)
    except:
        distances = filename_or_distances
    size = len(distances)
    current_state = get_random_starting_state(size)
    current_state_func = calculator.calculate_distance(current_state, distances)
    best_func = current_state_func
    best_step = 0
    step = 0
    current_stay = 0
    while current_stay < 0.9*size*log(size) and step < min(10*size*size, 10000000):
        step += 1
        swap = get_random_swap(size)
        update = calculator.get_state_function_update2(distances, current_state, swap)
        u = log(random.random())
        if u < update / annealing2(step, c):
            current_stay = 0
            calculator.update_state_reverse_swap(current_state, swap)
            current_state_func -= update
            if current_state_func < best_func:
                best_func = current_state_func
                best_step = step
        else:
            current_stay += 1
    return best_func, best_step, current_state_func, step
