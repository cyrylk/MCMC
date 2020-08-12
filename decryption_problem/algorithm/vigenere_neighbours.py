import random


def get_random_starting_state(alphabet, key_length):
    starting_state = []
    for i in range(key_length):
        starting_state.append(random.randint(0, alphabet.length-1))
    return starting_state


## @brief function for getting ith neighbour of current in fixed-length Vigenere cipher
# @param current - current state
# @param i - number of neighbour to be selected
# @param alphabetic - alphabetic used
# potential small optimization - when selecting a candidate, current state 
def get_ith_neighbour(current, i, alphabet):
    position_to_change = i // alphabet.max_shift_length
    shift = i % alphabet.max_shift_length
    return current[:position_to_change] + \
           [(current[position_to_change] + shift + 1) % alphabet.length] + current[position_to_change + 1:]


## @brief function for getting a number of neighbours of a given current state in fixed-length
# Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_neighbours_number(current, alphabet):
    return len(current) * alphabet.max_shift_length


## @brief function for generating a candidate from a given current state
# in fixed-length Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_candidate(current, alphabet):
    i = random.randint(0, get_neighbours_number(current, alphabet) - 1)
    return get_ith_neighbour(current, i, alphabet)
