import random


def get_random_starting_state(alphabet, length, coprimes):
    starting_state = []
    for i in range(length):
        number = random.randint(0, alphabet.length * len(coprimes))
        starting_state.append((number % len(coprimes), number // len(coprimes)))
    return starting_state


def get_ith_neighbour(current, i, alphabet, coprimes):
    position_to_change = i // (alphabet.length * len(coprimes) - 1)
    change = i % (alphabet.length * len(coprimes) - 1)

    if change < alphabet.max_shift_length:
        key_update = (current[position_to_change][0], (current[position_to_change][1] + change + 1) % alphabet.length)
        return position_to_change, key_update

    change -= alphabet.max_shift_length

    if change < len(coprimes) - 1:
        key_update = ((current[position_to_change][0] + change + 1) % len(coprimes), current[position_to_change][1])
        return position_to_change, key_update
    change -= (len(coprimes) - 1)

    a_change = change % (len(coprimes) - 1)
    b_change = change // (len(coprimes) - 1)
    key_update = ((current[position_to_change][0] + a_change + 1) % len(coprimes), (current[position_to_change][1] +
                                                                                    b_change + 1) % alphabet.length)
    return position_to_change, key_update


def get_neighbours_number(current, alphabet, coprimes):
    return len(current) * (alphabet.length * len(coprimes) - 1)


def get_candidate(current, alphabet, coprimes):
    i = random.randint(0, get_neighbours_number(current, alphabet, coprimes) - 1)
    return get_ith_neighbour(current, i, alphabet, coprimes)
