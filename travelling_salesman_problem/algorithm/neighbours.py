import random


def get_random_starting_state(size):
    selection = list(range(size))
    starting_state = []
    while selection:
        next_on_circuit = random.choice(selection)
        starting_state.append(next_on_circuit)
        selection.remove(next_on_circuit)
    return starting_state


def get_random_swap(size):
    smaller = random.randint(0, size-1)
    return smaller, random.randint(smaller+1, smaller + size - 1) % size

