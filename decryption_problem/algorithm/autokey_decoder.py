import decryption_problem.common.common as common
import decryption_problem.ciphers.autokey as cipher
import decryption_problem.algorithm.vigenere_neighbours as neighbours
import decryption_problem.algorithm.autokey_calculator as calculator
import random
from math import log


def get_max_monogram_state_coord(encryption, coordinate, monogram_log_distribution, key_length, alphabet):
    max_state = cipher.get_zero_mono_key()
    max_weight = float("-inf")
    for j in cipher.get_all_mono_keys(alphabet):
        k = j
        weight = 0
        for i in range(coordinate, len(encryption), key_length):
            k = cipher.encrypt_decrypt_single(encryption[i], k, alphabet)
            weight += monogram_log_distribution[k]
            k = -alphabet.letters_to_position[k]
        if weight > max_weight:
            max_state = j
            max_weight = weight
    return max_state, max_weight


def get_max_monogram_state(encryption, monogram_log_distribution, key_length, alphabet):
    max_monogram_key = []
    max_weight = 0
    for coordinate in range(key_length):
        max_coord = get_max_monogram_state_coord(encryption, coordinate, monogram_log_distribution,
                                                 key_length, alphabet)
        max_monogram_key.append(max_coord[0])
        max_weight += max_coord[1]
    return max_monogram_key, max_weight


def get_bigram_part_weight(encryption, part, coord, key_length, bigram_log_distribution, alphabet):
    weight = 0
    for i in range(coord, len(encryption) - 1, key_length):
        if i == key_length - 1:
            part = (part[0],
                    -alphabet.letters_to_position[cipher.encrypt_decrypt_single(encryption[0], part[1], alphabet)])
        encryption[i] = cipher.encrypt_decrypt_single(encryption[i], part[0], alphabet)
        encryption[i + 1] = cipher.encrypt_decrypt_single(encryption[i + 1], part[1], alphabet)
        new_bigram = (-alphabet.letters_to_position[encryption[i]], -alphabet.letters_to_position[encryption[i + 1]])
        grams = common.get_bigrams_in_coords(encryption, i)
        for gram in grams:
            try:
                weight += bigram_log_distribution[gram]
            except KeyError:
                pass
        encryption[i] = cipher.encrypt_decrypt_single(encryption[i], -part[0], alphabet)
        encryption[i + 1] = cipher.encrypt_decrypt_single(encryption[i + 1], -part[1], alphabet)
        part = new_bigram
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
    all_mono_keys = cipher.get_all_mono_keys(alphabet)
    codes = {a: {b: [cipher.get_zero_mono_key() for i in range(key_length - 1)] for b in all_mono_keys}
             for a in all_mono_keys}
    values = {a: {b: get_bigram_part_weight(encryption, (a, b), 0, key_length, bigram_log_distribution, alphabet)
                  for b in all_mono_keys} for a in all_mono_keys}
    new_values = {a: {b: 0 for b in all_mono_keys} for a in all_mono_keys}
    for r in range(1, key_length):
        for i in all_mono_keys:
            for j in codes[i]:
                max_func = float("-inf")
                max_arg = cipher.get_zero_mono_key()
                for k in codes[i]:
                    func = values[i][k] + get_bigram_part_weight(encryption, (k, j), r, key_length,
                                                                 bigram_log_distribution, alphabet)
                    if func > max_func:
                        max_func = func
                        max_arg = k
                new_values[i][j] = max_func
                codes[i][j][r - 1] = max_arg
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
        state_weight += common.calculate_n_gram_log_weight(partial_frequencies, log_distributions[index]) * coefs[index]
        index += 1

    return frequencies, state_weight


def generate_frequency_and_weight_change(current_state, candidate, n_list, coefs, log_distributions, decryption,
                                         alphabet):
    frequencies_change = []
    weight_change = 0
    index = 0
    for n in n_list:
        freq_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                       decryption, alphabet)
        frequencies_change.append(freq_change)
        weight_change += common.calculate_log_weight_change(freq_change, log_distributions[index]) * coefs[index]
        index += 1
    return frequencies_change, weight_change


def break_fixed_length_code_with_mcmc(encryption, alphabet, starting_state, n_list, coefs, log_distributions, steps,
                                      true_decrypting_code=[], consistency_thresholds=[]):
    consistency_index = 0
    consistency_list = []
    current_state = starting_state
    current_decryption = cipher.decrypt_text(encryption, current_state, alphabet)
    start = generate_frequencies_and_state_weight(current_decryption, n_list, coefs, log_distributions)
    current_frequencies = start[0]
    current_state_weight = start[1]
    max_weight = current_state_weight
    max_state = current_state
    for step in range(steps):
        candidate = neighbours.get_candidate(current_state, alphabet)
        frequency_and_weight_change = generate_frequency_and_weight_change(current_state, candidate, n_list, coefs,
                                                                           log_distributions, current_decryption,
                                                                           alphabet)
        frequencies_change = frequency_and_weight_change[0]
        weight_change = frequency_and_weight_change[1]
        changed_index = candidate[0]
        shift = candidate[1]
        u = random.random()
        if log(u) < weight_change:
            cipher.update_decryption_by_key_index(current_decryption, changed_index, shift, len(current_state),
                                                  alphabet)
            current_state[changed_index] = (current_state[changed_index] + candidate[1]) % alphabet.length
            for f in range(len(frequencies_change)):
                common.update_frequency(current_frequencies[f], frequencies_change[f])
            current_state_weight += weight_change
            if current_state_weight > max_weight:
                max_state = current_state[:]
                max_weight = current_state_weight
                if true_decrypting_code and \
                        common.consistency(current_state, true_decrypting_code, alphabet) >= \
                        consistency_thresholds[consistency_index]:
                    consistency_index += 1
                    consistency_list.append(step)
                    if consistency_index >= len(consistency_thresholds):
                        return max_state, max_weight, consistency_list
    return max_state, max_weight, consistency_list


def break_bounded_length_code_with_mcmc(encryption, alphabet, n_list, coefs, distributions, steps, boundary,
                                        monogram_log_distribution):
    max_weight = float("-inf")
    max_state = [cipher.get_zero_mono_key()]
    for length in range(1, boundary+1):
        start = get_max_monogram_state(encryption, monogram_log_distribution, length, alphabet)[0]
        break_attempt = break_fixed_length_code_with_mcmc(encryption, alphabet, start, n_list, coefs,
                                                          distributions, steps)
        if break_attempt[1] > max_weight:
            max_state = break_attempt[0]
            max_weight = break_attempt[1]
    return max_state, max_weight


def break_bounded_length_code_with_mcmc_optimized(encryption, alphabet, n_list, coefs, log_distributions, steps,
                                                  boundary, monogram_log_distribution):
    max_weight = float("-inf")
    max_state = [cipher.get_zero_mono_key()]
    steps = steps//20
    for length in range(1, boundary+1):
        start = get_max_monogram_state(encryption, monogram_log_distribution, length, alphabet)[0]
        optimized_steps = int(length/boundary * steps)
        break_attempt = break_fixed_length_code_with_mcmc(encryption, alphabet, start, n_list, coefs,
                                                          log_distributions, optimized_steps)
        if break_attempt[1] > max_weight:
            max_state = break_attempt[0]
            max_weight = break_attempt[1]

    return break_fixed_length_code_with_mcmc(encryption, alphabet, max_state, n_list, coefs,
                                             log_distributions, 20*steps)


def break_bounded_length_code_with_mcmc_monogram_criteria(encryption, alphabet, n_list, coefs, log_distributions,
                                                          steps_constant,
                                                          lower_bound, upper_bound, monogram_log_distribution,
                                                          scrabble):
    max_weight = float("-inf")
    max_state = [cipher.get_zero_mono_key()]
    for length in range(lower_bound, upper_bound+1):
        state = get_max_monogram_state(encryption, monogram_log_distribution, length, alphabet)[0]
        if length > (lower_bound + upper_bound) / 2:
            state = break_fixed_length_code_with_mcmc(encryption, alphabet, state, n_list, coefs,
                                              log_distributions, int(steps_constant * alphabet.length * length *
                                                                     (2 + log(length))))[0]
        words_list = cipher.encrypt_decrypt_text(encryption, state, alphabet).get_words_list()
        weight = sum([word in scrabble for word in words_list])/len(words_list)
        if weight > max_weight:
            max_weight = weight
            max_state = state
        if max_weight > 0.5:
            break
    return break_fixed_length_code_with_mcmc(encryption, alphabet, max_state, n_list, coefs,
                                             log_distributions, int(steps_constant*alphabet.length*len(max_state) *
                                             (10+log(len(max_state)))))
