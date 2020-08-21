from travelling_salesman_problem.data.data_generator import get_data_from_file
from travelling_salesman_problem.algorithm.neighbours import get_random_swap, get_random_swap2
import travelling_salesman_problem.algorithm.calculator as calculator
import random
from math import log, sqrt
from timeit import default_timer as time


def annealing1(i):
    return 1


def annealing2(i):
    return 3/log(i)


def annealing3(i):
    return sqrt(log(i))


def procedure(filename, steps):
    distances = get_data_from_file(filename)
    size = len(distances)
    current_state = list(range(size))
    current_state_func = calculator.calculate_distance(current_state, distances)
    best_state = current_state[:]
    best_func = current_state_func
    print (current_state_func)
    for i in range(2, steps+2):
        swap = get_random_swap2(size)
        update = calculator.get_state_function_update2(distances, current_state, swap)
        u = log(random.random())
        if u < update / annealing2(i):
            calculator.update_state_reverse_swap(current_state, swap)
            current_state_func -= update
            if current_state_func < best_func:
                best_func = current_state_func
                best_state = current_state[:]

    print(best_func, calculator.calculate_distance(best_state, distances))


random.seed(time())
procedure("../data/eil76.xml", 100000)
