import random


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
# potential small optimization - when selecting a candidate, current state 
def get_ith_neighbour_fixed(current, i, alphabet):
    position_to_change = i // alphabet.max_shift_length
    shift = i % alphabet.max_shift_length
    return current[:position_to_change] + \
           [(current[position_to_change] + shift + 1) % alphabet.length] + current[position_to_change + 1:]


def get_ith_neighbour_bounded2(current, i, boundary, alphabet):
    current_length = len(current)
    if current_length == 0:
        return [i]
    elif i < current_length:
        return current[:i] + current[i + 1:]

    no_deletion_i = i - current_length

    if current_length < boundary and no_deletion_i < (current_length + 1) * alphabet.length:
        position_to_insert = no_deletion_i // alphabet.length
        shift_to_insert = no_deletion_i % alphabet.length
        return current[:position_to_insert] + [shift_to_insert] + current[position_to_insert:]
    elif current_length >= boundary:
        return get_ith_neighbour_fixed(current, no_deletion_i, alphabet)

    no_insertion_i = no_deletion_i - (current_length + 1) * alphabet.length
    return get_ith_neighbour_fixed(current, no_insertion_i, alphabet)


## @brief function for getting ith neighbour of current in bounded-length Vigenere cipher
# @param current - current state
# @param i - number of neighbour to be selected
# @param boundary - maximum code (state) length
# @param alphabetic - alphabetic used
def get_ith_neighbour_bounded(current, i, boundary, alphabet):
    current_length = len(current)

    if i == 0 and current_length != 1:
        return current[:-1]
    if current_length > 1:
        i -= 1

    if i < len(current)*alphabet.max_shift_length:
        return get_ith_neighbour_fixed(current, i, alphabet)

    i -= len(current)*alphabet.max_shift_length
    res = current[:]
    res.append(i)
    return res

def get_ith_neighbour_bounded3(current, i, boundary, alphabet):
    current_length = len(current)
    if i <= boundary - current_length:
        return current + [random.randint(0, alphabet.length) for j in range(i)]

    i -= (boundary - current_length)
    if i < current_length and i > 0:
        return current[:(current_length - i)]

    i -= (current_length - 1)

    return get_ith_neighbour_fixed(current, i, alphabet)

def get_ith_neighbour_bounded4(current, i, boundary, alphabet):
    if i == 0:
        new_key = []
        for k in range(random.randint(1,boundary)):
            new_key.append(random.randint(0, alphabet.length))
        return new_key
    return get_ith_neighbour_fixed(current, i-1, alphabet)



## @brief function for getting a number of neighbours of a given current state in fixed-length
# Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_neighbours_number_fixed(current, alphabet):
    return len(current) * alphabet.max_shift_length


## @brief function for getting a number of neighbours of a given current state in bounded-length
# Vigenere cipher
# @param current - current state
# @param boundary - maximum code (state) length
# @param alphabetic - alphabetic used
def get_neighbours_number_bounded(current, boundary, alphabet):
    # only alphabetic length will be enough to pass
    if boundary == 1:
        return alphabet.max_shift_length
    elif len(current) == 1:
        return alphabet.max_shift_length + alphabet.length
    elif len(current) == boundary:
        return 1 + len(current) * alphabet.max_shift_length
    else:
        return 1 + len(current) * alphabet.max_shift_length + alphabet.length

def get_neighbours_number_bounded2(current, boundary, alphabet):
    if len(current) == boundary:
        return len(current) * (alphabet.max_shift_length + 1)
    elif len(current) == 0:
        return alphabet.length
    else:
        return (len(current) + 1) * alphabet.length + len(current) * (alphabet.max_shift_length + 1)

def get_neighbours_number_bounded3(current, boundary, alphabet):
    return boundary - 1 + len(current)*alphabet.max_shift_length

def get_neighbours_number_bounded4(current, boundary, alphabet):
    return 1 + len(current)*alphabet.max_shift_length


## @brief function for generating a candidate from a given current state
# in fixed-length Vigenere cipher
# @param current - current state
# @param alphabetic - alphabetic used
def get_candidate_fixed(current, alphabet):
    i = random.randint(0, get_neighbours_number_fixed(current, alphabet) - 1)
    return get_ith_neighbour_fixed(current, i, alphabet)


## @brief function for getting a number of neighbours of a given current state in
# bounded-length Vigenere cipher version algorithm 1 extension
# @param current - current state
# @param boundary - maximum code (state) length
# @param alphabetic - alphabetic used
def get_candidate_bounded(current, boundary, alphabet):
    i = random.randint(0, get_neighbours_number_bounded(current, boundary, alphabet) - 1)
    return get_ith_neighbour_bounded(current, i, boundary, alphabet)

def get_candidate_bounded2(current, boundary, alphabet):
    i = random.randint(0, get_neighbours_number_bounded2(current, boundary, alphabet) - 1)
    return get_ith_neighbour_bounded2(current, i, boundary, alphabet)

def get_candidate_bounded3(current, boundary, alphabet):
    i = random.randint(0, get_neighbours_number_bounded3(current, boundary, alphabet) - 1)
    return get_ith_neighbour_bounded3(current, i, boundary, alphabet)

def get_candidate_bounded4(current, boundary, alphabet):
    i = random.randint(0, get_neighbours_number_bounded4(current, boundary, alphabet) - 1)
    return get_ith_neighbour_bounded4(current, i, boundary, alphabet)