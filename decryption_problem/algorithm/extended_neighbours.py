import random
import decryption_problem.ciphers.vigenere_extended as extended


def get_starting_state_fixed(alphabet, length):
    starting_state = []
    for i in range(length):
        starting_state.append(random.randint(0, alphabet.length-1))
    return starting_state


def get_starting_state_bounded(alphabet, boundary):
    starting_state = []
    length = random.randint(1, boundary)
    for i in range(length):
        starting_state.append(random.randint(0, alphabet.length-1))
    return starting_state


## @brief function for getting ith neighbour of current in fixed-length Vigenere cipher
# @param current - current state
# @param i - number of neighbour to be selected
# @param alphabetic - alphabetic used
def get_ith_neighbour_fixed(current, i, alphabet, coprimes):
    position_to_change = i // (alphabet.length * len(coprimes) - 1)
    change = i % (alphabet.length * len(coprimes) - 1)
    if change < alphabet.max_shift_length:
        return current[:position_to_change] + \
           [(current[position_to_change](current[position_to_change] + shift + 1) % alphabet.length)] + current[position_to_change + 1:]




## @brief function for getting a number of neighbours of a given current state in fixed-length
# Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_neighbours_number_fixed(current, alphabet):
    return len(current) * alphabet.max_shift_length


## @brief function for generating a candidate from a given current state
# in fixed-length Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_candidate_fixed(current, alphabet):
    i = random.randint(0, get_neighbours_number_fixed(current, alphabet) - 1)
    return get_ith_neighbour_fixed(current, i, alphabet)


