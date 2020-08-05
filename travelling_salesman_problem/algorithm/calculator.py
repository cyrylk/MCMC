

def get_function_update1(distances, current_state, swap, anneal):
    size = len(current_state)
    update = 0

    update += distances[current_state[swap[0]]][current_state[(swap[0] + 1) % size]]
    update += distances[current_state[swap[0]]][current_state[(swap[0] - 1) % size]]
    update += distances[current_state[swap[1]]][current_state[(swap[1] + 1) % size]]
    update += distances[current_state[swap[1]]][current_state[(swap[1] - 1) % size]]

    update_state(current_state, swap)

    update -= distances[current_state[swap[0]]][current_state[(swap[0] + 1) % size]]
    update -= distances[current_state[swap[0]]][current_state[(swap[0] - 1) % size]]
    update -= distances[current_state[swap[1]]][current_state[(swap[1] + 1) % size]]
    update -= distances[current_state[swap[1]]][current_state[(swap[1] - 1) % size]]

    update_state(current_state, (swap[1], swap[0]))

    return update/anneal


def update_state(current_state, swap):
    aux = current_state[swap[0]]
    current_state[swap[0]] = current_state[swap[1]]
    current_state[swap[1]] = aux




def calculate_distance(state, distances):
    dist = 0
    for j in range(len(state)):
        dist += distances[state[j]][state[(j+1) % len(state)]]
    return dist

