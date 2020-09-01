import travelling_salesman_problem.algorithm.solver as solver
import travelling_salesman_problem.data.data_generator as data_generator
import os
from timeit import default_timer as time
import random


solutions_dict = {element.split(":")[0][:-1]: float(element.split(":")[1][:-1]) for element in
                  open("../data/solutions.txt", "r").readlines()}


def get_instance_name(filename):
    return filename.split(".")[0]


'''Test case 1:
various instances of the problem with different methods.
For homogenous chains result written down in results1.txt is of form:
(shortest_path_length, step_when_achieved)
For simulated annealing chains:
(shortest_path_length, step_when_achieved, last_path_length, walk_duration).
Due to a small bug "step_when_achieved" in no-convergence version is 1 smaller than the actual one.
Results in results1.txt
'''

# random.seed(time())
#
# results_file = open("results1.txt", "w")
#
#
# counter = 1
# for instance in os.listdir("../../../TSPLIB"):
#     print(counter)
#     counter += 1
#     distances = data_generator.get_data_from_file("../../../TSPLIB/"+instance)
#     instance_size = len(distances)
#     instance_name = get_instance_name(instance)
#     optimal_solution = solutions_dict[instance_name]
#     max_steps = min(10*instance_size*instance_size, 10000000)
#     results_file.write(instance_name + "\n optimal solution: " + str(optimal_solution) + "\n\n")
#     for retry in range(1, 3):
#         results_file.write("ATTEMPT " + str(retry) + "\n")
#         results_file.write("MATRIX 1, HOMOGENOUS\n")
#         start = time()
#         results_file.write(str(solver.solve_max_steps1(distances, max_steps)) + " time: " + str(time() - start) + "\n\n")
#         results_file.write("MATRIX 2, HOMOGENOUS\n")
#         start = time()
#         results_file.write(str(solver.solve_max_steps2(distances, max_steps)) + " time: " + str(time() - start) + "\n\n")
#         results_file.write("MATRIX 1, ANNEALING\n")
#         start = time()
#         results_file.write(str(solver.solve_convergence1(distances, 3)) + " time: " + str(time() - start) + "\n\n")
#         results_file.write("MATRIX 2, ANNEALING\n")
#         start = time()
#         results_file.write(str(solver.solve_convergence2(distances, 3)) + " time: " + str(time() - start) + "\n\n")
#
# results_file.close()
#


'''Test case 2:
Instances selected to be included in the thesis. Results of MCMC generated in the form of latex
tables. Additionally the best result obtained by drawing uniformly from all permutations 10000 times
included.
'''

results_file = open("results2.txt", "w")

random.seed(time())

list_of_instances = ["dsj1000.xml", "att532.xml", "kroA150.xml", "berlin52.xml"]
table_header = '''\\begin{center}\\begin{small}\\begin{longtable}{|c|c|c|c|c|c|c|c|} 
\\hline \\makecell{NR} &  \\makecell{$t_n$} & \\makecell{ROZW.\\\\UZYSKANE\\\\ W KROKU} & 
\\makecell{ROZW.} &  \\makecell{ROZW./\\\\OPTYMALNE} & \\makecell{L.\\\\KROKÓW} & 
\\makecell{ZBIEŻNOŚĆ\\\\DO} & \\makecell{CZAS}\\\\ \\hline \n'''

counter = 1
for instance in os.listdir("../../../TSPLIB"):
    if instance not in list_of_instances:
        continue
    print(counter)
    counter += 1
    distances = data_generator.get_data_from_file("../../../TSPLIB/"+instance)
    instance_size = len(distances)
    instance_name = get_instance_name(instance)
    optimal_solution = solutions_dict[instance_name]
    max_steps = min(10*instance_size*instance_size, 10000000)
    results_file.write(instance_name+"\n")

    results_file.write("K1\n" + table_header)
    for retry in range(1, 3):
        start = time()
        solution = solver.solve_max_steps1(distances, max_steps)
        duration = time() - start
        results_file.write(str(retry) + " & $=1$ & " + str(solution[1]) + " & " + "{:.2f}".format(solution[0])
                           + " & " +
                           str(solution[0]/optimal_solution)[:4] + " & " + str(max_steps) + " & - & " +
                           str(duration)[:4] + "s \\\\ \\hline \n")
        start = time()
        solution = solver.solve_convergence1(distances, 3)
        duration = time() - start
        convergence_state_function = "{:.2f}".format(solution[2]) if solution[3] < max_steps else "-"
        results_file.write(str(retry) + " & $=\\frac{3}{\\log(n+2)}$ & " + str(solution[1]) + " & " +
                           "{:.2f}".format(solution[0]) + " & " +
                           str(solution[0]/optimal_solution)[:4] + " & " + str(solution[3]) + " & " +
                           convergence_state_function + " & " +
                           str(duration)[:4] + "s \\\\  \\hline \n")
    results_file.write("\\end{longtable}\\end{small}\\end{center}" + "\n")

    results_file.write("\n\n" + "K2\n" + table_header)
    for retry in range(1, 3):
        start = time()
        solution = solver.solve_max_steps2(distances, max_steps)
        duration = time() - start
        results_file.write(str(retry) + " & $=1$ & " + str(solution[1]) + " & " + "{:.2f}".format(solution[0])
                           + " & " +
                           str(solution[0] / optimal_solution)[:4] + " & " + str(max_steps) + " & - & " +
                           str(duration)[:4] + "s \\\\ \\hline \n")
        start = time()
        solution = solver.solve_convergence2(distances, 3)
        duration = time() - start
        convergence_state_function = "{:.2f}".format(solution[2]) if solution[3] < max_steps else "-"
        results_file.write(str(retry) + " & $=\\frac{3}{\\log(n+2)}$ & " + str(solution[1]) + " & " +
                           "{:.2f}".format(solution[0]) + " & " +
                           str(solution[0] / optimal_solution)[:4] + " & " + str(solution[3]) + " & " +
                           convergence_state_function + " & " +
                           str(duration)[:4] + "s \\\\  \\hline \n")
    results_file.write("\\end{longtable}\\end{small}\\end{center}" + "\n")


    results_file.write("\n\n")
    results_file.write("COMPLETELY RANDOM\n")
    start = time()
    results_file.write(str(solver.solve3(distances, 10000)) + "\n\n")
    results_file.write(str(time() - start))
    results_file.write("\n\n\n\n")

results_file.close()
