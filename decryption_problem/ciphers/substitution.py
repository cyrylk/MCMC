#file for potential future development, currently it is not a part of the project
#testing of potential possibilities for resolving convolution of vigenere
#and substitution cipher


import decryption_problem.alphabetic.alphabetic as alphabetic
from random import choice, randint, random
import random as rand
import decryption_problem.data.data_generator as data_generator
import string
import decryption_problem.common.common as common
from math import log
import copy
import decryption_problem.ciphers.vigenere as cipher
import decryption_problem.algorithm.vigenere_decoder as decoder
from timeit import default_timer as time

rand.seed(time())

#
# scrabble = open("../data/scrabble_words.txt", "r")
# lines = scrabble.readlines()
# print(lines[0][:-1])
# scrabble.close()
# sccrables = set([line[:-1] for line in lines])


def create_stripped_encryption_decryption(text, encryption_decryption, alphabet):
    result = alphabetic.StrippedText(encryption_decryption, alphabet)
    result.set_ends_of_words(text.ends_of_words)
    result.set_stripped_part(text.stripped_part)
    return result


def encrypt_decrypt_text(text, alphabet1, alphabet2):
    encryption_decryption = []
    for i in range(len(text)):
        if text[i] in alphabet1:
            encryption_decryption.append(alphabet2[alphabet1.letters_to_position[text[i]]])
        else:
            encryption_decryption.append(text[i])
    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encryption_decryption, alphabet1)
    return encryption_decryption


def generate_random_permutation(alphabet):
    permutation = copy.deepcopy(alphabet)
    to_choose = list(range(permutation.length))
    letters_to_position = []
    while to_choose:
        element = choice(to_choose)
        letters_to_position.append(element)
        to_choose.remove(element)
    index = 0
    for i in permutation.letters_to_position:
        permutation.letters_to_position[i] = letters_to_position[index]
        index += 1
    for letter in permutation.letters_to_position:
        permutation.alphabet[permutation.letters_to_position[letter]] = letter

    return permutation


def get_random_swapp(ordered):
    proposition = randint(0, len(ordered) - 2)
    # to_change = randint(proposition+1, len(ordered) - 1)

    return proposition, proposition+1
    # elif los == 1 or proposition == len(ordered) - 3:
    #     return proposition, proposition + 2
    # return proposition, proposition + 3



def get_swap(ordered, swap):
    # print(current[normal.letters_to_position[ordered[smaller]]], current[normal.letters_to_position[ordered[smaller+1]]])
    return ordered[swap[0]], ordered[swap[1]]


def swap_permutation_and_update_decryption(current_decryption, current_permuted_alphabet, swap):
    to_write_swap_1 = current_decryption.positions[swap[0]].copy()
    to_write_swap_0 = current_decryption.positions[swap[1]].copy()
    for i in to_write_swap_1:
        current_decryption[i] = swap[1]
    for i in to_write_swap_0:
        current_decryption[i] = swap[0]
    aux0 = current_permuted_alphabet.letters_to_position[swap[0]]
    aux1 = current_permuted_alphabet.letters_to_position[swap[1]]
    current_permuted_alphabet.letters_to_position[swap[0]] = aux1
    current_permuted_alphabet.letters_to_position[swap[1]] = aux0
    current_permuted_alphabet.alphabet[aux0] = swap[1]
    current_permuted_alphabet.alphabet[aux1] = swap[0]


def swap_permutation(current_permuted_alphabet, swap):
    aux0 = current_permuted_alphabet.letters_to_position[swap[0]]
    aux1 = current_permuted_alphabet.letters_to_position[swap[1]]
    current_permuted_alphabet.letters_to_position[swap[0]] = aux1
    current_permuted_alphabet.letters_to_position[swap[1]] = aux0
    current_permuted_alphabet.alphabet[aux0] = swap[1]
    current_permuted_alphabet.alphabet[aux1] = swap[0]

def shift_alphabet(alphabet, shift):
    shifted = copy.deepcopy(alphabet)
    for i in shifted.alphabet:
        shifted.alphabet[i] = alphabet[(i+shift)%alphabet.length]
        shifted.letters_to_position[shifted.alphabet[i]] = i
    return shifted



def update_freq_change(bigram1, bigram2, freqs, freq_change):
    freq_change[bigram1] = 0
    try:
        freq_change[bigram1] -= freqs[bigram1]
    except KeyError:
        pass
    try:
        freq_change[bigram1] += freqs[bigram2]
    except KeyError:
        pass


def get_frequency_change(swap, extended_alphabet, current_frequencies):
    frequency_change = {}
    update_freq_change(swap[0] + swap[0], swap[1] + swap[1],
                       current_frequencies, frequency_change)
    update_freq_change(swap[1] + swap[1], swap[0] + swap[0],
                       current_frequencies, frequency_change)
    update_freq_change(swap[0] + swap[1], swap[1] + swap[0],
                       current_frequencies, frequency_change)
    update_freq_change(swap[1] + swap[0], swap[0] + swap[1],
                       current_frequencies, frequency_change)
    for l in extended_alphabet.letters():
        if not (l == swap[0] or l == swap[1]):
            update_freq_change(swap[0] + l, swap[1] + l,
                               current_frequencies, frequency_change)
            update_freq_change(l + swap[0], l + swap[1],
                               current_frequencies, frequency_change)
            update_freq_change(swap[1] + l, swap[0] + l,
                               current_frequencies, frequency_change)
            update_freq_change(l + swap[1], l + swap[0],
                               current_frequencies, frequency_change)

    return frequency_change


def get_optimal_mono_permutation(original, dist_apriori, dist_aposteriori):
    sorted_apriori = sorted(original.alphabet.values(), key=lambda x: dist_apriori[x] if x in dist_apriori else -1)
    sorted_aposteriori = sorted(original.alphabet.values(), key=lambda x: dist_aposteriori[x] if x in dist_aposteriori else -1)
    result = copy.deepcopy(original)
    for i in range(len(sorted_apriori)):
        result.letters_to_position[sorted_aposteriori[i]] = original.letters_to_position[sorted_apriori[i]]
        result.alphabet[original.letters_to_position[sorted_apriori[i]]] = sorted_aposteriori[i]

    return result

def get_reverse_permutation(base, permutation):
    result = copy.deepcopy(base)
    for letter in base.letters_to_position:
        result.letters_to_position[letter] = base.letters_to_position[permutation.alphabet
                                            [base.letters_to_position[letter]]]
        result.alphabet[result.letters_to_position[letter]] = letter
    return result


# def get_frequency(frequencies)

# def get_max_mono_permutation(encryption, normal_alphabet, key_length, mono_dist):
#     encryption0 = common.get_piece_on_i_coordinate(encryption, 0, key_length)
#     max_weight = float("-inf")
#     max_state = copy.deepcopy(normal_alphabet)
#     for i in range(len(normal_alphabet.length)):
#         enc = cipher.encrypt_decrypt_text(encryption0, [i], key_length)
#         dist_aposteriori = common.calculate_n_gram_frequencies(enc, 1)
#         candidate = get_optimal_mono_permutation(normal_alphabet, mono_dist, dist_aposteriori)
#         freqs = {}
#         for i in dist_aposteriori:
#             freqs[normal_alphabet[candidate.letters_to_position[i]]] = dist_aposteriori[i]
#         print(freqs)
#
#         z = encrypt_decrypt_text(encryption, alphabett, reverser).get_non_stripped_text()



def break_mcmc(encryption, alphabet, extended_alphabet, log_distribution, steps, monogram_log_distribution):

    dist_aposteriori = common.calculate_n_gram_frequencies(encryption, 1)
    current_guessed_decoding_key = get_reverse_permutation(alphabet,
                                                           get_optimal_mono_permutation(alphabet,
                                                                                        monogram_log_distribution, dist_aposteriori))
    current_decryption = encrypt_decrypt_text(encryption, alphabet, current_guessed_decoding_key)
    current_frequencies = common.calculate_n_gram_frequencies(current_decryption, 2)
    current_decoding_key = copy.deepcopy(current_guessed_decoding_key)
    current_dist = common.calculate_n_gram_log_weight(current_frequencies, log_distribution)

    current_order = sorted(alphabet.letters(), key=lambda i: monogram_log_distribution[i] if i in monogram_log_distribution else -1)
    print(current_order)

    max_dist = current_dist
    max_state = copy.deepcopy(current_decoding_key)
    for i in range(steps):
        swapp = get_random_swapp(current_order)
        swap = get_swap(current_order, swapp)
        frequency_change = get_frequency_change(swap, extended_alphabet, current_frequencies)
        dist_change = common.calculate_log_weight_change(frequency_change, log_distribution)
        if dist_change > log(random()):
            swap_permutation_and_update_decryption(current_decryption, current_decoding_key, swap)
            common.update_frequency(current_frequencies, frequency_change)
            current_dist += dist_change
            # aux = current_order[swapp[0]]
            # current_order[swapp[0]] = current_order[swapp[1]]
            # current_order[swapp[1]] = aux

            if current_dist > max_dist:
                max_dist = current_dist
                max_state = copy.deepcopy(current_decoding_key)
                print(current_order)
    return max_state

def break_mcmc_double(encryption, alphabet, steps, length,
                      monogram_log_distribution, bigram_log_distribution, extended_alphabet):
    max_letter = max(alphabet.letters(),
                           key=lambda i: monogram_log_distribution[i] if i in monogram_log_distribution else -1)
    max_position = alphabet.letters_to_position[max_letter]
    for j in range(length):
        dist_aposteriori = common.calculate_n_gram_frequencies(common.get_piece_on_i_coordinate(encryption, j, length), 1)
        current_guessed_encoding_key = get_optimal_mono_permutation(alphabet, monogram_log_distribution, dist_aposteriori)
        decoding_vigenere = []
        for i in range(0, length):
            dist_aposteriori = common.calculate_n_gram_frequencies(common.get_piece_on_i_coordinate(encryption, i, length), 1)
            ith_guessed_encoding_key = get_optimal_mono_permutation(alphabet, monogram_log_distribution, dist_aposteriori)
            decoding_vigenere.append(current_guessed_encoding_key.letters_to_position[ith_guessed_encoding_key[max_position]]
                                     - current_guessed_encoding_key.letters_to_position[current_guessed_encoding_key[max_position]])

        current_decryption = cipher.encrypt_decrypt_text(encryption, decoding_vigenere, current_guessed_encoding_key)
        current_order = sorted(alphabet.letters(),
                               key=lambda i: dist_aposteriori[i] if i in dist_aposteriori else -1)
        current_guessed_decoding_key = copy.deepcopy(get_reverse_permutation(alphabet, current_guessed_encoding_key))
        current_decryption = encrypt_decrypt_text(current_decryption, alphabet, current_guessed_decoding_key)
        current_frequencies = common.calculate_n_gram_frequencies(current_decryption, 2)
        current_dist = common.calculate_n_gram_log_weight(current_frequencies, bigram_log_distribution)
        max_dist = current_dist
        max_state = copy.deepcopy(current_guessed_decoding_key)
        for i in range(steps):
            swapp = get_random_swapp(current_order)
            swap = get_swap(current_order, swapp)
            frequency_change = get_frequency_change(swap, extended_alphabet, current_frequencies)
            dist_change = common.calculate_log_weight_change(frequency_change, bigram_log_distribution)
            if dist_change > log(random()):
                swap_permutation_and_update_decryption(current_decryption, current_guessed_encoding_key, swap)
                common.update_frequency(current_frequencies, frequency_change)
                current_dist += dist_change
                aux = current_order[swapp[0]]
                current_order[swapp[0]] = current_order[swapp[1]]
                current_order[swapp[1]] = aux

                if current_dist > max_dist:
                    max_dist = current_dist
                    max_state = copy.deepcopy(current_guessed_decoding_key)
                    print(current_decryption.get_non_stripped_text())
    return get_reverse_permutation(alphabet, max_state)


alphabett = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plain = alphabetic.StrippedText(
    data_generator.get_string_cleared
    (data_generator.generate_random_excerpt("../data/1984.txt", 20000)).upper(),
                                alphabett)

standard2 = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions_uppercase.json")
standard1 = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions_uppercase.json")

all_printable = data_generator.get_string_cleared(string.printable + " ")
upper_printable = all_printable[:10] + all_printable[36:]
complete_alphabet = alphabetic.Alphabet(data_generator.get_string_cleared(string.printable + " "))
upper_alphabet = alphabetic.Alphabet(upper_printable)

freqs = common.calculate_n_gram_frequencies(plain, 1)

weight = common.calculate_n_gram_log_weight(freqs, standard1)
print(weight)

permuted_alphabet = generate_random_permutation(alphabett)

encryption = encrypt_decrypt_text(plain, alphabett, permuted_alphabet)
# x = get_optimal_mono_permutation(alphabett, standard1,
#                                  common.calculate_n_gram_frequencies(encryption, 1))
# reverser = get_reverse_permutation(alphabett, x)
#
# z = plain.get_non_stripped_text()
# D = {}
# for i in z:
#     try:
#         if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#             D[i]+=1
#     except:
#         D[i] = 1
# print(sorted(D, key=lambda i: D[i] if i in D else -1))
#
code = data_generator.generate_random_vigenere_key_fixed(permuted_alphabet, 100)
print(code)
encryption = cipher.encrypt_decrypt_text(plain, code,
                                         permuted_alphabet)
# print(cipher.encrypt_decrypt_text(encryption, decoder.get_max_monogram_state(encryption, standard1, 2, permuted_alphabet)[0], permuted_alphabet)
#       .get_non_stripped_text())


x = break_mcmc_double(encryption, alphabett, 20000, 100, standard1, standard2, upper_alphabet)

# decrypted = cipher.encrypt_decrypt_text(encryption, x[1], x[0])
# print(decrypted.get_non_stripped_text())
# print(get_reverse_permutation(alphabett, permuted_alphabet).alphabet)
# x = break_mcmc(encryption, alphabett, upper_alphabet, standard2, 5000, standard1)
for i in range(10):
    freqs = common.calculate_n_gram_frequencies(common.get_piece_on_i_coordinate(plain, i, 10), 1)
    print(max(freqs, key=lambda l: freqs[l]))
    # print(min(freqs, key=lambda l: freqs[l]))
# print(encrypt_decrypt_text(encryption, alphabett, x).get_non_stripped_text())
# freqs = common.calculate_n_gram_frequencies(encrypt_decrypt_text(encryption, alphabett, x), 2)
# print(common.calculate_n_gram_log_weight(freqs, standard2))
# print(plain.get_non_stripped_text())
# freqs = common.calculate_n_gram_frequencies(plain, 2)
# print(common.calculate_n_gram_log_weight(freqs, standard2))

