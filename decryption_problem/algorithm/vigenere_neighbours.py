import random


def get_random_starting_state(alphabet, key_length):
    starting_state = []
    for i in range(key_length):
        starting_state.append(random.randint(0, alphabet.length-1))
    return starting_state


def get_ith_neighbour(current, i, alphabet):
    position_to_change = i // alphabet.max_shift_length
    shift = i % alphabet.max_shift_length
    return position_to_change, (shift + 1) % alphabet.length


def get_neighbours_number(current, alphabet):
    return len(current) * alphabet.max_shift_length


def get_candidate(current, alphabet):
    i = random.randint(0, get_neighbours_number(current, alphabet) - 1)
    return get_ith_neighbour(current, i, alphabet)
