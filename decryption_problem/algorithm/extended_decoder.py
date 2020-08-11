import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.common.common as common
import decryption_problem.ciphers.vigenere_extended as extended
import decryption_problem.algorithm.extended_neighbours as neighbours
import decryption_problem.algorithm.extended_calculator as calculator
import random
from math import log

from timeit import default_timer as time
random.seed(time())

def get_max_monogram_state_coord(text, coordinate, monogram_dist, key_length, alphabet, coprimes):
    max_state = 0
    max_func = 0
    for j in extended.get_all_mono_keys(alphabet, coprimes):
        func = 0
        for i in range(coordinate, len(text), key_length):
            func += monogram_dist[extended.encrypt_decrypt_single(text[i], j, alphabet)]
        if func > max_func:
            max_state = j
            max_func = func
    return max_state


def get_max_monogram_state(text, monogram_dist, key_length, alphabet, coprimes):
    return [get_max_monogram_state_coord(text, coordinate, monogram_dist, key_length, alphabet, coprimes) for coordinate in
            range(key_length)]


def get_bigram_weight(text, bigram, coord, key_length, bigram_dist, alphabet, coprimes):
    weight = 0
    for i in range(coord, len(text) - 1, key_length):
        old_text0 = text[i]
        old_text1 = text[i+1]
        text[i] = extended.encrypt_decrypt_single(text[i], bigram[0], alphabet, coprimes)
        text[i+1] = extended.encrypt_decrypt_single(text[i+1], bigram[1], alphabet, coprimes)
        gram = common.get_n_gram_at_i(text, 2, i)
        try:
            weight += bigram_dist[gram]
        except KeyError:
            pass
        text[i] = old_text0
        text[i + 1] = old_text1
    return weight


def get_max_bigram_state(text, bigram_dist, key_length, alphabet, coprimes):
    all_single_keys = extended.get_all_mono_keys(alphabet, coprimes)
    codes = {a: {b: [extended.get_zero_mono_key() for i in range(key_length-1)] for b in all_single_keys} for a in all_single_keys}
    values = {a: {b: get_bigram_weight(text, (a, b), 0, key_length, bigram_dist, alphabet, coprimes) for b in
                  all_single_keys} for a in all_single_keys}
    new_values = {a: {b: 0 for b in all_single_keys} for a in all_single_keys}
    for r in range(1, key_length):
        for i in all_single_keys:
            for j in codes[i]:
                max_func = values[i][all_single_keys[0]] + get_bigram_weight(text, (all_single_keys[0], j), r, key_length, bigram_dist, alphabet,
                                                                             coprimes)
                max_val = 0
                for k in codes[i]:
                    func = values[i][k] + get_bigram_weight(text, (k, j), r, key_length, bigram_dist, alphabet, coprimes)
                    if func > max_func:
                        max_func = func
                        max_val = k
                new_values[i][j] = max_func
                codes[i][j][r-1] = max_val

        aux = values
        values = new_values
        new_values = aux

    maxi = values[all_single_keys[0]][all_single_keys[0]]
    max_state = 0
    for i in all_single_keys:
        if values[i][i] > maxi:
            maxi = values[i][i]
            max_state = i

    print("MAXIMIZADO", maxi)
    res = []
    t = len(codes[max_state][max_state]) - 1
    current = max_state
    for i in range(len(codes[max_state][max_state])):
        current = codes[max_state][current][t]
        res.append(current)
        t -= 1
    res.append(max_state)
    res.reverse()
    return res

def fixed_procedure(text, distributions, starting_state, n_list, steps, alphabet, coefs, coprimes):
    current_state = starting_state
    current_decryption = extended.encrypt_decrypt_text(text, current_state, alphabet, coprimes)

    current_frequencies = []
    current_state_function = 0
    index = 0
    #one function it should be from list of freqs
    for n in n_list:
        freqs = common.calculate_n_gram_frequencies(current_decryption, n)
        current_frequencies.append(freqs)
        current_state_function += common.calculate_log_n_gram_function(freqs, distributions[index])*coefs[index]
        index += 1

    max_function = current_state_function
    max_state = current_state
    for i in range(steps):
        candidate = neighbours.get_candidate_fixed(current_state, alphabet, coprimes)
        frequencies_change = []
        dist_change = 0
        index = 0
        for n in n_list:
            freq_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                   current_decryption, text, alphabet, coprimes)
            frequencies_change.append(freq_change)

            dist_change += common.calculate_log_function_change(freq_change, distributions[index])*coefs[index]
            index += 1
        changed_index = calculator.find_change_in_key(current_state, candidate)
        u = random.random()
        if log(u) < dist_change:
            extended.update_decryption_by_key_index(current_decryption, text, changed_index, candidate[changed_index],
                                                    len(current_state),
                                                    alphabet, coprimes)
            current_state = candidate
            for f in range(len(frequencies_change)):
                common.update_frequency(current_frequencies[f], frequencies_change[f])
            current_state_function += dist_change
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function
    return max_state, max_function


from decryption_problem.algorithm.distribution_generator import generate_from_file_log


alphabeto = alphabetic.Alphabet("ABCDEFGH")
standard3 = generate_from_file_log("../data/english_trigrams.txt", alphabeto, 3)
standard2 = generate_from_file_log("../data/english_bigrams.txt", alphabeto, 2)
standard1 = generate_from_file_log("../data/english_monograms.txt", alphabeto, 1)

plain = alphabetic.StrippedText('''IF YOUTH, THROUGHOUT ALL HISTORY, HAD HAD A CHAMPION TO STAND UP FOR IT; 
TO SHOW A DOUBTING WORLD THAT A CHILD CAN THINK; AND, POSSIBLY''', alphabeto)



coprimess = extended.get_coprimes(alphabeto.length)
code = neighbours.get_random_starting_state(alphabeto, len(plain) // 11, coprimess)

encrypted = extended.encrypt_decrypt_text(plain, code, alphabeto, coprimess)
res = fixed_procedure(encrypted, [standard2], neighbours.get_random_starting_state(alphabeto, len(code), coprimess),
                      [2], 15000, alphabeto, [1.0], coprimess)
maxx_state = res[0]
maxx_function = res[1]
# bounded_procedure(encrypted, standard2, neighbours.get_starting_state_bounded(alphabeto, 20), 2, 10000, alphabeto, 20)

# maxx_state = []
# maxx_function = 0
#
# for proc in range(1, 21):
#     curr = fixed_procedure(encrypted, standard, neighbours.get_starting_state_fixed(alphabeto, proc), 2,
#                            900, alphabeto)
#     if curr[1] > maxx_function:
#         maxx_state = curr[0]
#         maxx_function = curr[1]
#
print(maxx_function)
decrypted1 = extended.encrypt_decrypt_text(encrypted, maxx_state, alphabeto, coprimess)

# decrypted2 = extended.decrypt_text(encrypted, [-i for i, j in code], alphabeto)
# state_function = 0
# frequencies = common.calculate_n_gram_frequencies(decrypted2, 1, alphabeto)
# state_function += common.calculate_log_n_gram_function(frequencies, standard1)*0.2
# frequencies = common.calculate_n_gram_frequencies(decrypted2, 2, alphabeto)
# state_function += common.calculate_log_n_gram_function(frequencies, standard2)*0.6
# frequencies = common.calculate_n_gram_frequencies(decrypted2, 3, alphabeto)
# state_function += common.calculate_log_n_gram_function(frequencies, standard3)*0.2
# print(state_function)

print(decrypted1.get_non_stripped_text())
# print()
# print(decrypted2.get_non_stripped_text())

print("TESTTTTTTTT")
maximizer = get_max_bigram_state(encrypted, standard2, len(code), alphabeto, coprimess)
decrypted3 = extended.encrypt_decrypt_text(encrypted, maximizer,
                                           alphabeto, coprimess)
frequencies = common.calculate_n_gram_frequencies(decrypted3, 2)
state_function = common.calculate_log_n_gram_function(frequencies, standard2)
print(decrypted3.get_non_stripped_text())
print(state_function)

frequencies = common.calculate_n_gram_frequencies(plain, 2)
state_function = common.calculate_log_n_gram_function(frequencies, standard2)
print([extended.reverse_key((coprimess[k[0]], k[1]), alphabeto) for k in code], state_function)
print(maximizer)
print(maxx_state)

