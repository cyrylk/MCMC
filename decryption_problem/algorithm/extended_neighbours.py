import random


def get_random_starting_state(alphabet, length, coprimes):
    starting_state = []
    for i in range(length):
        number = random.randint(0, alphabet.length * len(coprimes))
        starting_state.append((number % len(coprimes), number // len(coprimes)))
    return starting_state


## @brief function for getting ith neighbour of current in fixed-length Vigenere cipher
# @param current - current state
# @param i - number of neighbour to be selected
# @param alphabetic - alphabetic used
def get_ith_neighbour(current, i, alphabet, coprimes):
    position_to_change = i // (alphabet.length * len(coprimes) - 1)
    change = i % (alphabet.length * len(coprimes) - 1)

    if change < alphabet.max_shift_length:
        key_update = (current[position_to_change][0], (current[position_to_change][1] + change + 1) % alphabet.length)
        return current[:position_to_change] + [key_update] + current[position_to_change + 1:]

    change -= alphabet.max_shift_length

    if change < len(coprimes) - 1:
        key_update = ((current[position_to_change][0] + change + 1) % len(coprimes), current[position_to_change][1])
        return current[:position_to_change] + [key_update] + current[position_to_change + 1:]
    change -= (len(coprimes) - 1)

    a_change = change % (len(coprimes) - 1)
    b_change = change // (len(coprimes) - 1)
    key_update = ((current[position_to_change][0] + a_change + 1) % len(coprimes), (current[position_to_change][1] +
                                                                                    b_change + 1) % alphabet.length)
    return current[:position_to_change] + [key_update] + current[position_to_change + 1:]


## @brief function for getting a number of neighbours of a given current state in fixed-length
# Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_neighbours_number(current, alphabet, coprimes):
    return len(current) * (alphabet.length * len(coprimes) - 1)


## @brief function for generating a candidate from a given current state
# in fixed-length Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_candidate(current, alphabet, coprimes):
    i = random.randint(0, get_neighbours_number(current, alphabet, coprimes) - 1)
    return get_ith_neighbour(current, i, alphabet, coprimes)
