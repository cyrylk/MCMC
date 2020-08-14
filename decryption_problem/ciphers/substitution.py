import decryption_problem.alphabetic.alphabetic as alphabetic
from random import choice, randint, random
import decryption_problem.data.data_generator as data_generator
import string
import decryption_problem.common.common as common
from math import log
import copy
import decryption_problem.ciphers.vigenere as cipher
import decryption_problem.algorithm.vigenere_neighbours as neighbours
import decryption_problem.algorithm.vigenere_calculator as calculator
import decryption_problem.algorithm.vigenere_decoder as decoder


def create_stripped_encryption_decryption(text, encryption_decryption, alphabet):
    result = alphabetic.StrippedText(encryption_decryption, alphabet)
    result.set_ends_of_words(text.ends_of_words)
    result.set_stripped_part(text.stripped_part)
    return result


def encrypt_decrypt_text(text, permuted_alphabet, normal_alphabet):
    encryption_decryption = []
    for i in range(len(text)):
        if text[i] in permuted_alphabet:
            encryption_decryption.append(permuted_alphabet[normal_alphabet.letters_to_position[text[i]]])
        else:
            encryption_decryption.append(text[i])
    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encryption_decryption, permuted_alphabet)
    return encryption_decryption


def generate_random_permutation(alphabet):
    to_choose = list(range(alphabet.length))
    letters_to_position = []
    while to_choose:
        element = choice(to_choose)
        letters_to_position.append(element)
        to_choose.remove(element)
    index = 0
    for i in alphabet.letters_to_position:
        alphabet.letters_to_position[i] = letters_to_position[index]
        index += 1
    permuted = {}
    for i in range(alphabet.length):
        permuted[i] = alphabet[alphabet.letters_to_position[alphabet[i]]]
    alphabet.alphabet = permuted

def get_random_swap(alphabet):
    smaller = randint(0, alphabet.length-2)
    return alphabet[smaller], alphabet[randint(smaller+1, alphabet.length-1)]


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
            update_freq_change(l+ swap[0], l+swap[1],
                               current_frequencies, frequency_change)
            update_freq_change(swap[1] + l, swap[0] + l,
                               current_frequencies, frequency_change)
            update_freq_change(l+ swap[1], l+swap[0],
                               current_frequencies, frequency_change)

    return frequency_change


def break_mcmc(encryption, alphabet, extended_alphabet, log_distribution, steps):
    current_frequencies = common.calculate_n_gram_frequencies(encryption, 2)
    current_decryption = encryption
    current_decoding_key = alphabet
    current_dist = common.calculate_n_gram_log_weight(current_frequencies, log_distribution)

    max_dist = current_dist
    max_state = copy.deepcopy(current_decoding_key)
    for i in range(steps):
        swap = get_random_swap(current_decoding_key)
        frequency_change = get_frequency_change(swap, extended_alphabet, current_frequencies)
        dist_change = common.calculate_log_weight_change(frequency_change, log_distribution)
        if dist_change > log(random()):
            swap_permutation_and_update_decryption(current_decryption, current_decoding_key, swap)
            common.update_frequency(current_frequencies, frequency_change)
            current_dist += dist_change

            if current_dist > max_dist:
                max_dist = current_dist
                max_state = copy.deepcopy(current_decoding_key)

    return max_state


def break_mcmc_double(encryption, alphabet, log_distribution, steps, length,
                      monogram_log_distribution):
    normal_alphabet = copy.deepcopy(alphabet)
    current_guessed_encoding_key = alphabet
    vigenere = decoder.get_max_monogram_state(encryption, monogram_log_distribution, length, alphabet)
    current_decryption = cipher.encrypt_decrypt_text(encryption, vigenere, current_guessed_encoding_key)
    current_frequencies = common.calculate_n_gram_frequencies(current_decryption, 2)
    current_dist = common.calculate_n_gram_log_weight(current_frequencies, log_distribution)
    max_dist = current_dist
    max_state = copy.deepcopy(current_guessed_encoding_key)
    for i in range(steps):
        swap = get_random_swap(current_guessed_encoding_key)
        swap_permutation(current_guessed_encoding_key, swap)
        vigenere = decoder.get_max_monogram_state(encryption, monogram_log_distribution, length,
                                                  current_guessed_encoding_key)
        current_decryption = cipher.encrypt_decrypt_text(encryption, vigenere, current_guessed_encoding_key)
        current_decryption = encrypt_decrypt_text(encryption, normal_alphabet, current_guessed_encoding_key, )
        current_frequencies = common.calculate_n_gram_frequencies(cipher.encrypt_decrypt_text(current_decryption,
                                                                                              vigenere,
                                                                                              alphabet), 2)
        dist_change = common.calculate_n_gram_log_weight(current_frequencies, log_distribution) - current_dist
        if dist_change > log(random()):
            current_dist += dist_change
            if current_dist > max_dist:
                max_dist = current_dist
                max_state = copy.deepcopy(current_guessed_encoding_key)
        else:
            swap_permutation(current_guessed_encoding_key, (swap[1], swap[0]))
    return max_state


alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plain = alphabetic.StrippedText(data_generator.generate_random_excerpt("../data/war_and_peace.txt", 1300).upper(),
                                alphabet)

standard2 = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions_uppercase.json")
standard1 = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions_uppercase.json")

all_printable = data_generator.get_string_cleared(string.printable + " ")
upper_printable = all_printable[:10] + all_printable[36:]
complete_alphabet = alphabetic.Alphabet(data_generator.get_string_cleared(string.printable + " "))
upper_alphabet = alphabetic.Alphabet(upper_printable)

# print(plain.get_non_stripped_text())
# freqs = common.calculate_n_gram_frequencies(plain, 2)
# print(get_frequency_change(alphabet, ("A", "B"), upper_alphabet, freqs))
# swap_permutation_and_update_decryption(plain, alphabet, ("A", "B"))
# print(get_frequency_change(alphabet, ("B", "C"), upper_alphabet, freqs))
# swap_permutation_and_update_decryption(plain, alphabet, ("B", "C"))
# print(get_frequency_change(alphabet, ("C", "D"), upper_alphabet, freqs))

# print(plain.get_non_stripped_text())
# swap_permutation_and_update_decryption(plain, alphabet, ("B", "C"))
# print(plain.get_non_stripped_text())
permuted_alphabet = copy.deepcopy(alphabet)
generate_random_permutation(permuted_alphabet)

encryption = encrypt_decrypt_text(plain, permuted_alphabet, alphabet)
print(encryption.get_non_stripped_text())
# swap_permutation_and_update_decryption(encryption, alphabet, get_random_swap(alphabet))
# print(encryption.get_non_stripped_text())

another = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
encryption2 = copy.deepcopy(encryption)
x = break_mcmc(encryption, another, upper_alphabet, standard2, 25000)

another = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# print(another.letters_to_position)
print(encrypt_decrypt_text(encryption2, x, alphabet).get_non_stripped_text())

encryption2 = copy.deepcopy(encryption)
encryption2 = cipher.encrypt_decrypt_text(encryption2, [0,1,2,3,4,5,6,7,8,9], permuted_alphabet)
y = break_mcmc_double(encryption2, another, standard2, 1000, 10, standard1)

key = decoder.get_max_monogram_state(encryption2, standard1, 10, y)
encryption3 = cipher.encrypt_decrypt_text(encryption2, key, y)
encryption3 = encrypt_decrypt_text(encryption3, alphabet, y)
print(encryption3.get_non_stripped_text())



