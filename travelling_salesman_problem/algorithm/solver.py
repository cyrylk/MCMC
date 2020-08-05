from travelling_salesman_problem.data.data_generator import get_data_from_file
from travelling_salesman_problem.algorithm.neighbours import get_random_swap
import travelling_salesman_problem.algorithm.calculator as calculator
import random
from math import log


def procedure(filename, steps):
    distances = get_data_from_file(filename)
    size = len(distances)
    current_state = list(range(size))
    current_func = calculator.calculate_distance(current_state, distances)
    best_state = current_state[:]
    best_func = current_func
    for i in range(steps):
        swap = get_random_swap(size)
        update = calculator.get_function_update1(distances, current_state, swap)
        u = log(random.random())
        if u < update/log(i+2):
            calculator.update_state(current_state, swap)
            current_func -= update
            if current_func < best_func:
                best_func = current_func
                best_state = current_state[:]

    print(best_state, best_func, calculator.calculate_distance(best_state, distances))


procedure("../data/burma14.xml", 10000)

