import decryption_problem.common.common as common
import decryption_problem.ciphers.vigenere_extended as cipher
import decryption_problem.algorithm.extended_neighbours as neighbours
import decryption_problem.algorithm.extended_calculator as calculator
import random
from math import log

def get_max_monogram_state_coord(encryption, coordinate, monogram_log_distribution, key_length, alphabet, coprimes):
    max_state = cipher.get_zero_mono_key()
    max_weight = float("-inf")
    for j in cipher.get_all_mono_keys(alphabet, coprimes):
        weight = 0
        for i in range(coordinate, len(encryption), key_length):
            weight += monogram_log_distribution[cipher.encrypt_decrypt_single(encryption[i], j, alphabet, coprimes)]
        if weight > max_weight:
            max_state = j
            max_weight = weight
    return max_state


def get_max_monogram_state(encryption, monogram_log_distribution, key_length, alphabet):
    coprimes = cipher.get_coprimes(alphabet.length)
    return [get_max_monogram_state_coord(encryption, coordinate, monogram_log_distribution, key_length, alphabet, coprimes) for coordinate in
            range(key_length)]


def get_bigram_part_weight(encryption, part, coord, key_length, bigram_log_distribution, alphabet, coprimes):
    weight = 0
    for i in range(coord, len(encryption) - 1, key_length):
        old_text0 = encryption[i]
        old_text1 = encryption[i + 1]
        encryption[i] = cipher.encrypt_decrypt_single(encryption[i], part[0], alphabet, coprimes)
        encryption[i + 1] = cipher.encrypt_decrypt_single(encryption[i + 1], part[1], alphabet, coprimes)
        gram = common.get_n_gram_at_i(encryption, 2, i)
        try:
            weight += bigram_log_distribution[gram]
        except KeyError:
            pass
        encryption[i] = old_text0
        encryption[i + 1] = old_text1
    return weight


def get_max_bigram_key_and_weight(values, codes, all_mono_keys):
    max_bigram_weight_value = -float("inf")
    max_state = cipher.get_zero_mono_key()
    for i in all_mono_keys:
        if values[i][i] > max_bigram_weight_value:
            max_bigram_weight_value = values[i][i]
            max_state = i
    bigram_maximizer = []
    t = len(codes[max_state][max_state]) - 1
    current = max_state
    for i in range(len(codes[max_state][max_state])):
        current = codes[max_state][current][t]
        bigram_maximizer.append(current)
        t -= 1
    bigram_maximizer.append(max_state)
    bigram_maximizer.reverse()
    return bigram_maximizer, max_bigram_weight_value


def get_max_bigram_state(encryption, bigram_log_distribution, key_length, alphabet):
    coprimes = cipher.get_coprimes(alphabet.length)
    all_mono_keys = cipher.get_all_mono_keys(alphabet, coprimes)
    codes = {a: {b: [cipher.get_zero_mono_key() for i in range(key_length - 1)] for b in all_mono_keys} for a in all_mono_keys}
    values = {a: {b: get_bigram_part_weight(encryption, (a, b), 0, key_length, bigram_log_distribution, alphabet, coprimes) for b in
                  all_mono_keys} for a in all_mono_keys}
    new_values = {a: {b: 0 for b in all_mono_keys} for a in all_mono_keys}
    for r in range(1, key_length):
        for i in all_mono_keys:
            for j in codes[i]:
                max_func = values[i][all_mono_keys[0]] + get_bigram_part_weight(encryption, (all_mono_keys[0], j), r,
                                                                                key_length, bigram_log_distribution,
                                                                                alphabet, coprimes)
                max_val = 0
                for k in codes[i]:
                    func = values[i][k] + get_bigram_part_weight(encryption, (k, j), r, key_length,
                                                                 bigram_log_distribution, alphabet, coprimes)
                    if func > max_func:
                        max_func = func
                        max_val = k
                new_values[i][j] = max_func
                codes[i][j][r-1] = max_val

        aux = values
        values = new_values
        new_values = aux

    return get_max_bigram_key_and_weight(values, codes, all_mono_keys)


def generate_frequencies_and_state_weight(decryption, n_list, coefs, log_distributions):
    frequencies = []
    state_weight = 0
    index = 0
    for n in n_list:
        partial_frequencies = common.calculate_n_gram_frequencies(decryption, n)
        frequencies.append(partial_frequencies)
        state_weight += common.calculate_log_n_gram_function(partial_frequencies, log_distributions[index])*coefs[index]
        index += 1

    return frequencies, state_weight


def generate_frequency_and_weight_change(current_state, candidate, n_list, coefs, log_distributions, decryption, text,
                                         alphabet, coprimes):
    frequencies_change = []
    weight_change = 0
    index = 0
    for n in n_list:
        freq_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                       decryption, text, alphabet, coprimes)
        frequencies_change.append(freq_change)
        weight_change += common.calculate_log_function_change(freq_change, log_distributions[index]) * coefs[index]
        index += 1
    return frequencies_change, weight_change


def break_fixed_length_code_with_mcmc(encryption, alphabet, starting_state, n_list, coefs, distributions, steps):
    coprimes = cipher.get_coprimes(alphabet.length)
    current_state = starting_state
    current_decryption = cipher.encrypt_decrypt_text(encryption, current_state, alphabet, coprimes)
    start = generate_frequencies_and_state_weight(current_decryption, n_list, coefs, distributions)
    current_frequencies = start[0]
    current_state_weight = start[1]
    max_weight = current_state_weight
    max_state = current_state
    for step in range(steps):
        candidate = neighbours.get_candidate(current_state, alphabet, coprimes)
        frequency_and_weight_change = generate_frequency_and_weight_change(current_state, candidate, n_list, coefs,
                                                                           distributions, current_decryption,
                                                                           encryption, alphabet, coprimes)
        frequencies_change = frequency_and_weight_change[0]
        weight_change = frequency_and_weight_change[1]
        changed_index = common.find_change_in_key(current_state, candidate)
        u = random.random()
        if log(u) < weight_change:
            cipher.update_decryption_by_key_index(current_decryption, encryption, changed_index, candidate[changed_index],
                                                  len(current_state),
                                                  alphabet, coprimes)
            current_state = candidate
            for f in range(len(frequencies_change)):
                common.update_frequency(current_frequencies[f], frequencies_change[f])
            current_state_weight += weight_change
            if current_state_weight > max_weight:
                max_state = candidate
                max_weight = current_state_weight
    return max_state, max_weight

def break_bounded_length_code_with_mcmc(encryption, alphabet, n_list, coefs, log_distributions, steps, boundary,
                                        monogram_log_distribution):
    max_weight = float("-inf")
    max_state = [cipher.get_zero_mono_key()]
    for length in range(1, boundary+1):
        start = get_max_monogram_state(encryption, monogram_log_distribution, length, alphabet)
        break_attempt = break_fixed_length_code_with_mcmc(encryption, alphabet, start, n_list, coefs,
                                                          log_distributions, steps)
        if break_attempt[1] > max_weight:
            max_state = break_attempt[0]
            max_weight = break_attempt[1]
    return max_state, max_weight


def break_bounded_length_code_with_mcmc_optimized(encryption, alphabet, n_list, coefs, log_distributions, steps,
                                                  boundary, monogram_log_distribution):
    max_weight = float("-inf")
    max_state = [cipher.get_zero_mono_key()]
    for length in range(1, boundary+1):
        start = get_max_monogram_state(encryption, monogram_log_distribution, length, alphabet)
        optimized_steps = int(length/boundary * steps)
        break_attempt = break_fixed_length_code_with_mcmc(encryption, alphabet, start, n_list, coefs,
                                                          log_distributions, optimized_steps)
        if break_attempt[1] > max_weight:
            max_state = break_attempt[0]
            max_weight = break_attempt[1]
    return max_state, max_weight

