import travelling_salesman_problem.algorithm.solver as solver
import travelling_salesman_problem.data.data_generator as data_generator
import os
from timeit import default_timer as time
import random


solutions_dict = {element.split(":")[0][:-1]: float(element.split(":")[1][:-1]) for element in
                  open("../data/solutions.txt", "r").readlines()}


def get_instance_name(filename):
    return filename.split(".")[0]


random.seed(time())

results_file = open("results.txt", "w")


counter = 1
for instance in os.listdir("../../../TSPLIB"):
    print(counter)
    counter += 1
    distances = data_generator.get_data_from_file("../../../TSPLIB/"+instance)
    instance_size = len(distances)
    instance_name = get_instance_name(instance)
    optimal_solution = solutions_dict[instance_name]
    max_steps = min(10*instance_size*instance_size, 10000000)
    results_file.write(instance_name + "\n optimal solution: " + str(optimal_solution) + "\n\n")
    for retry in range(1, 3):
        results_file.write("ATTEMPT " + str(retry) + "\n")
        results_file.write("MATRIX 1, HOMOGENOUS\n")
        start = time()
        results_file.write(str(solver.solve_max_steps1(distances, max_steps)) + " time: " + str(time() - start) + "\n\n")
        results_file.write("MATRIX 2, HOMOGENOUS\n")
        start = time()
        results_file.write(str(solver.solve_max_steps2(distances, max_steps)) + " time: " + str(time() - start) + "\n\n")
        results_file.write("MATRIX 1, ANNEALING\n")
        start = time()
        results_file.write(str(solver.solve_convergence1(distances, 3)) + " time: " + str(time() - start) + "\n\n")
        results_file.write("MATRIX 2, ANNEALING\n")
        start = time()
        results_file.write(str(solver.solve_convergence2(distances, 3)) + " time: " + str(time() - start) + "\n\n")

results_file.close()

