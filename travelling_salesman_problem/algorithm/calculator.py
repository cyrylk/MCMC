

def get_function_update1(distances, current_state, swap):
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

    update_state(current_state, swap)

    return update


def get_function_update2(distances, current_state, swap):
    size = len(current_state)
    update = 0

    update += distances[current_state[swap[0]]][current_state[(swap[0] - 1) % size]]
    update += distances[current_state[swap[1]]][current_state[(swap[1] + 1) % size]]

    update_state(current_state, swap)
    update -= distances[current_state[swap[0]]][current_state[(swap[0] - 1) % size]]
    update -= distances[current_state[swap[1]]][current_state[(swap[1] + 1) % size]]
    update_state(current_state, swap)

    return update


def update_state(current_state, swap):
    aux = current_state[swap[0]]
    current_state[swap[0]] = current_state[swap[1]]
    current_state[swap[1]] = aux


def update_state_reverse_swap(current_state, swap):
    distance = (swap[1] - swap[0]) % len(current_state)
    for i in range(distance):
        if i > distance//2:
            return
        aux = current_state[(swap[0] + i) % len(current_state)]
        current_state[(swap[0] + i) % len(current_state)] = current_state[(swap[1] - i) % len(current_state)]
        current_state[(swap[1] - i) % len(current_state)] = aux


state = [0, 1, 2, 3, 4, 5]
update_state_reverse_swap(state, (3, 0))
update_state_reverse_swap(state, (3, 0))
update_state_reverse_swap(state, (3, 0))
print(state)


def calculate_distance(state, distances):
    dist = 0
    for j in range(len(state)):
        dist += distances[state[j]][state[(j+1) % len(state)]]
    return dist
