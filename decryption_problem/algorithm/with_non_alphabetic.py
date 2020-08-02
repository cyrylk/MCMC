## @package vigenereCiphering
#  Documentation for this module.
#
#  More details.

import unittest
import random
import mock

MIN_FREQUENCY_FACTOR = 1e-50


def calculate_min_frequency_factor(distribution):
    return 1e-50


## @brief class containing information about the alphabet used
class Alphabet:

    def __init__(self, alphabet_in_string):
        ## @brief alphabet used
        self.alphabet = list(alphabet_in_string)
        ## @brief mapping of letters to their positions
        self.letters_to_position = {self.alphabet[i]: i for i in range(len(self.alphabet))}
        ## @brief length of the alphabet
        self.length = len(self.alphabet)
        ## @brief number of different letters in alphabet (equiv number of shifts that will change a letter)
        self.max_shift_length = self.length - 1

    def __getitem__(self, key):
        return self.alphabet[key]


class StrippedText:

    def __init__(self, non_stripped_text, alphabet):
        length = len(non_stripped_text)
        self.alphabetic_signs = []
        self.non_alphabetic_segments = []
        self.ends_of_words = []
        self.alphabet = alphabet
        non_alphabet = ""
        end_of_word = 0
        for i in range(length):
            if non_stripped_text[i] in self.alphabet.letters_to_position:
                self.alphabetic_signs.append(non_stripped_text[i])
                end_of_word += 1
                if non_alphabet:
                    self.non_alphabetic_segments.append(non_alphabet)
                    non_alphabet = ""
                if i + 1 == length or non_stripped_text[i + 1] not in self.alphabet.letters_to_position:
                    self.ends_of_words.append(True)
                else:
                    self.ends_of_words.append(False)
            else:
                non_alphabet += non_stripped_text[i]
                if i + 1 == length:
                    self.non_alphabetic_segments.append(non_alphabet)
        self.non_alphabetic_segments.append("")

    def __getitem__(self, key):
        return self.alphabetic_signs[key]

    def __setitem__(self, key, value):
        self.alphabetic_signs[key] = value

    def __len__(self, ):
        return len(self.alphabetic_signs)

    def get_non_stripped_text(self):
        text = ""
        word_index = 0
        for i in range(len(self.alphabetic_signs)):
            text += self.alphabetic_signs[i]
            if self.ends_of_words[i]:
                text += self.non_alphabetic_segments[word_index]
                word_index += 1
        return text


def alphabets_product(alphabet1, alphabet2):
    return {i + j: 0 for i in alphabet1 for j in alphabet2}


## @brief function generating a dictionary of all n-grams of given alphabet
# to frequencies - initially all frequencies set to zero
def n_gram_dict(alphabet, n):
    result = [""]
    for i in range(n):
        result = alphabets_product(alphabet, result)
    return result


## @brief function for encrypting/decrypting single letter in Vigenere cipher
# @param letter – letter to be encrypted/decrypted
# @param shift – how many places letter is to be shifted in the alphabet
# alphabet - alphabet used
def encrypt_decrypt_single(letter, shift, alphabet):
    return alphabet[(alphabet.letters_to_position[letter] + shift) % alphabet.length]


## @brief function for coding text in given Vigenere cipher in
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabet - alphabet used
def encrypt_decrypt_text(text, shift_key):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], text.alphabet))
        current_key_ptr = (current_key_ptr + 1) % key_length

    return encrypted_decrypted

def encrypt_text(text, shift_key, alphabet):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = ""
    for index in range(len(text)):
        encrypted_decrypted += (encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr = (current_key_ptr + 1) % key_length

    return encrypted_decrypted


## @brief function for getting ith neighbour of current in fixed-length Vigenere cipher
# @param current - current state
# @param i - number of neighbour to be selected
# @param alphabet - alphabet used
def get_ith_neighbour_fixed(current, i, alphabet):
    position_to_change = i // alphabet.max_shift_length
    shift = i % alphabet.max_shift_length
    return current[:position_to_change] + \
           [(current[position_to_change] + shift + 1) % alphabet.length] + \
           current[position_to_change + 1:]


## @brief function for getting ith neighbour of current in bounded-length Vigenere cipher
# @param current - current state
# @param i - number of neighbour to be selected
# @param boundary - maximum code (state) length
# @param alphabet - alphabet used
def get_ith_neighbour_bounded(current, i, boundary, alphabet):
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


## @brief function for getting a number of neighbours of a given current state in fixed-length
# Vigenere cipher
# @param current - current state
# @param alphabet - alphabet used
def get_neighbours_number_fixed(current, alphabet):
    return len(current) * alphabet.max_shift_length


## @brief function for getting a number of neighbours of a given current state in bounded-length
# Vigenere cipher
# @param current - current state
# @param boundary - maximum code (state) length
# @param alphabet - alphabet used
def get_neighbours_number_bounded(current, boundary, alphabet):
    if len(current) == boundary:
        return len(current) * (alphabet.max_shift_length + 1)
    elif len(current) == 0:
        return alphabet.length
    else:
        return (len(current) + 1) * alphabet.length + len(current) * (alphabet.max_shift_length + 1)


## @brief function for generating a candidate from a given current state
# in fixed-length Vigenere cipher
# @param current - current state
# @param alphabet - alphabet used
def get_candidate_fixed(current, alphabet):
    i = random.randint(0, get_neighbours_number_fixed(current, alphabet) - 1)
    return get_ith_neighbour_fixed(current, i, alphabet)


## @brief function for getting a number of neighbours of a given current state in
# bounded-length Vigenere cipher version algorithm 1 extension
# @param current - current state
# @param boundary - maximum code (state) length
# @param alphabet - alphabet used
def get_candidate_bounded(current, boundary, alphabet):
    i = random.randint(0, get_neighbours_number_bounded(current, boundary, alphabet) - 1)
    return get_ith_neighbour_bounded(current, i, boundary, alphabet)


def find_n_gram_at_i(original_text, n, j, i, shift):
    if j < 0 or j+n > len(original_text):
        return None
    gram = ""
    for k in range(j, j + n):
        if original_text.ends_of_words[k] and k + 1 < j + n:
            return None
        if k == i:
            gram += encrypt_decrypt_single(original_text[k], shift, original_text.alphabet)
        else:
            gram += original_text[k]
    return gram


def calculate_initial_frequencies(text, gram_length):
    frequencies_dict = n_gram_dict(text.alphabet, gram_length)
    current_gram = ""
    for i in range(len(text)):
        current_gram += text[i]
        if len(current_gram) > gram_length:
            current_gram = current_gram[1:]
        if len(current_gram) == gram_length:
            frequencies_dict[current_gram] += 1
        if text.ends_of_words[i]:
            current_gram = ""

    return frequencies_dict

def calculate_frequencies(original_text, encrypted_decrypted, gram_length):
    frequencies_dict = n_gram_dict(original_text.alphabet, gram_length)
    current_gram = ""
    for i in range(len(original_text)):
        current_gram += encrypted_decrypted[i]
        if len(current_gram) > gram_length:
            current_gram = current_gram[1:]
        if len(current_gram) == gram_length:
            frequencies_dict[current_gram] += 1
        if original_text.ends_of_words[i]:
            current_gram = ""

    return frequencies_dict


def calculate_candidate_function(old, frequencies_change, distribution):
    change = 1
    for i in frequencies_change:
        if i not in distribution or not distribution[i]:
            change *= MIN_FREQUENCY_FACTOR**frequencies_change[i]
        else:
            change *= distribution[i]**frequencies_change[i]
    return change*old


def calculate_candidate_change(frequencies_change, distribution):
    return calculate_candidate_function(1, frequencies_change, distribution)


def find_change_in_key(old_key, new_key):
    for i in range(len(old_key)):
        if old_key[i] != new_key[i]:
            return i

def get_frequencies_change(old_frequencies, new_frequencies):
    frequencies_change = {}
    for i in old_frequencies:
        if old_frequencies[i] != new_frequencies[i]:
            frequencies_change[i] = new_frequencies[i] - old_frequencies[i]
    return frequencies_change


def get_frequency_change_fixed(old_key, new_key, n, text):
    change = find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    old_shift = old_key[change]
    new_shift = new_key[change]
    for i in range(change, len(text), key_length):
        for j in range(i - n + 1, i + 1):
            old_gram = find_n_gram_at_i(text, n, j, i, old_shift)
            new_gram = find_n_gram_at_i(text, n, j, i, new_shift)
            if old_gram and new_gram:
                try:
                    frequencies_change[old_gram] -= 1
                    frequencies_change[new_gram] += 1
                except KeyError:
                    frequencies_change[old_gram] = -1
                    frequencies_change[new_gram] = 1

    return frequencies_change


def get_frequency_change_bounded(old_key, new_key, n, frequencies, text):
    if len(old_key) == len(new_key):
        return get_frequency_change_fixed(old_key, new_key, n, text)
    else:
        new_frequencies = calculate_frequencies(text, encrypt_decrypt_text(text, new_key), n)
        frequencies_change = get_frequencies_change(frequencies, new_frequencies)

        return frequencies_change


def update_frequency(frequency, frequency_change):
    for i in frequency_change:
        frequency[i] += frequency_change[i]




## @brief unit tests for Vigenere encryption and decryption
class TestVigenereEncryptionDecryption(unittest.TestCase):

    def setUp(self):
        self.alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def patchRandint(self, min_value, max_value):
        return max_value // 2

    def test_single_letter_encrypt_decrypt(self):
        self.assertEqual(encrypt_decrypt_single("Z", 4, self.alphabet), "D")

    def test_stripped_text_properties(self):
        self.assertTrue(StrippedText("M C MC", self.alphabet).ends_of_words[0])
        self.assertTrue(StrippedText("M C MC", self.alphabet).ends_of_words[1])
        self.assertFalse(StrippedText("M C MC", self.alphabet).ends_of_words[2])
        self.assertTrue(StrippedText("M C MC", self.alphabet).ends_of_words[3])
        self.assertEqual(StrippedText("MCMC ARE THE BEST.", self.alphabet).alphabetic_signs,
                         list("MCMCARETHEBEST"))
        self.assertEqual(StrippedText("MCMC ARE -> THE BEST", self.alphabet).non_alphabetic_segments,
                         [" ", " -> ", " ", ""])
        self.assertEqual(StrippedText("MCMC ARE THE BEST.", self.alphabet).get_non_stripped_text(),
                         "MCMC ARE THE BEST.")

        text = StrippedText("MCMC ARE THE BEST.", self.alphabet)
        text[1] = "B"
        self.assertEqual(text[1], "B")
        self.assertEqual(text.alphabetic_signs, list("MBMCARETHEBEST"))

    def test_text_encrypt_decrypt(self):
        text = StrippedText("YEARGREATYEAR", self.alphabet)
        self.assertEqual(encrypt_decrypt_text(text, [3, 2, 1, 0]), list("BGBRJTFAWAFAU"))
        self.assertEqual(encrypt_text("YEARGREATYEAR", [3, 2, 1, 0], self.alphabet), "BGBRJTFAWAFAU")

    def test_ith_fixed_neighbour(self):
        self.assertEqual(
            get_ith_neighbour_fixed([0, 1, 2, 3, 4, 5], 3 * self.alphabet.max_shift_length + 2, self.alphabet),
            [0, 1, 2, 6, 4, 5])

    def test_ith_bounded_neighbour(self):
        # deletion
        self.assertEqual(get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 4, 10, self.alphabet), [0, 1, 2, 3, 5])

        # insertion at the beginning
        self.assertEqual(get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 8, 10, self.alphabet), [2, 0, 1, 2, 3, 4, 5])

        # insertion in the middle
        self.assertEqual(
            get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 2 * self.alphabet.length + 7, 10, self.alphabet),
            [0, 1, 7, 2, 3, 4, 5])
        # insertion at the end
        self.assertEqual(
            get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 6 * self.alphabet.length + 1, 10, self.alphabet),
            [0, 1, 2, 3, 4, 5, 1])

        # substituting a letter
        self.assertEqual(get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 7 * self.alphabet.length +
                                                   2 * self.alphabet.max_shift_length + 23, 10, self.alphabet),
                         [0, 1, 0, 3, 4, 5])

        # boundary size
        self.assertEqual(
            get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 5 * self.alphabet.max_shift_length + 2, 6, self.alphabet),
            [0, 1, 2, 3, 4, 8])

        # zero size
        self.assertEqual(get_ith_neighbour_bounded([], 6, 6, self.alphabet),
                         [6])

    def test_neighbours_number_fixed(self):
        self.assertEqual(get_neighbours_number_fixed([0, 1, 2, 3, 4, 5], self.alphabet),
                         6 * self.alphabet.max_shift_length)

    def test_neighbours_number_bounded(self):
        # middle size
        self.assertEqual(get_neighbours_number_bounded([0, 1, 2, 3, 4, 5], 10, self.alphabet),
                         6 * self.alphabet.max_shift_length +
                         6 + 7 * self.alphabet.length)
        # boundary size
        self.assertEqual(get_neighbours_number_bounded([0, 1, 2, 3, 4, 5], 6, self.alphabet),
                         6 * self.alphabet.max_shift_length + 6)

        # zero size
        self.assertEqual(get_neighbours_number_bounded([], 6, self.alphabet), self.alphabet.length)

    def test_candidate_fixed(self):
        with mock.mock.patch('random.randint', self.patchRandint):
            current_state = [0, 1, 2, 3, 4, 5]
            max_value = get_neighbours_number_fixed(current_state, self.alphabet) - 1
            self.assertEqual(get_candidate_fixed(current_state, self.alphabet),
                             get_ith_neighbour_fixed(current_state, max_value // 2, self.alphabet))

    def test_candidate_bounded(self):
        with mock.mock.patch('random.randint', self.patchRandint):
            current_state = [0, 1, 2, 3, 4, 5]
            max_value = get_neighbours_number_bounded(current_state, 10, self.alphabet) - 1
            self.assertEqual(get_candidate_bounded(current_state, 10, self.alphabet),
                             get_ith_neighbour_bounded(current_state, max_value // 2, 10, self.alphabet))

    def test_alphabets_product(self):
        self.assertEqual(alphabets_product("AB", "C"), {"AC": 0, "BC": 0})

    def test_n_gram_dict(self):
        self.assertEqual(n_gram_dict("AB", 2), {"AA": 0, "AB": 0, "BA": 0, "BB": 0})

    def test_calculate_initial_frequencies(self):
        init_frequencies = calculate_initial_frequencies(StrippedText("ABCCC, DE", self.alphabet), 2)
        self.assertEqual(init_frequencies["AB"], 1)
        self.assertEqual(init_frequencies["BC"], 1)
        self.assertEqual(init_frequencies["DE"], 1)
        self.assertEqual(init_frequencies["CC"], 2)
        self.assertEqual(init_frequencies["CD"], 0)

    def test_calculate_change_fixed(self):
        original_text = StrippedText("ABCD", self.alphabet)
        self.assertEqual(get_frequency_change_fixed([0, 1], [0, 2], 2, original_text),
                         {"AC": -1, "AD": 1, "CC": -1, "DC": 1, "CE": -1, "CF": 1})

    def test_calculate_change_bounded(self):
        text = StrippedText("ABCD", self.alphabet)
        frequencies = calculate_frequencies(text, encrypt_decrypt_text(text, [0, 1]), 2)
        self.assertEqual(get_frequency_change_bounded([0, 1], [0, 1, 0], 2, frequencies, text),
                         {"CE": -1, "CD": 1})

    def test_update_frequency(self):
        frequency = {"AB": 1, "BC": 2, "CD": 0}
        frequency_change = {"AB": -1, "BC": -2, "CD": 3}
        update_frequency(frequency, frequency_change)
        self.assertEqual(frequency, {"AB": 0, "BC": 0, "CD": 3})

    def test_update_frequency(self):
        frequency = {"AB": 1, "BC": 2, "CD": 0}
        frequency_change = {"AB": -1, "BC": -2, "CD": 3}
        update_frequency(frequency, frequency_change)
        self.assertEqual(frequency, {"AB": 0, "BC": 0, "CD": 3})

    def test_calculate_candidate_function(self):
        self.assertEqual(calculate_candidate_function(2, {"AB": 2, "CD": -1}, {"AB": 0.5, "CD": 0.25}), 2*4*0.25)



def fixed_procedure(text, distribution, starting_state, n, steps):
    alphabet = text.alphabet
    current_state = starting_state
    current_decryption = encrypt_decrypt_text(text, current_state)
    current_frequencies = calculate_frequencies(text, current_decryption, n)
    current_state_function = calculate_candidate_function(1, current_frequencies, distribution)

    max_function = current_state_function
    max_state = current_state

    for i in range(steps):
        candidate = get_candidate_fixed(current_state, alphabet)
        frequency_change = get_frequency_change_fixed(current_state, candidate, n, text)
        dist_change = calculate_candidate_change(frequency_change, distribution)
        u = random.random()
        if u < dist_change:
            current_state = candidate
            update_frequency(current_frequencies, frequency_change)
            current_state_function *= dist_change
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function


    text.alphabetic_signs = encrypt_decrypt_text(text, max_state)
    print(text.get_non_stripped_text())

from distribution_generator import generate_from_file

random.seed(20)

standard = generate_from_file("encrypting_and_decrypting/english_bigrams_standard.txt")
alphabeto = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plain = '''THIS IS THE FIRST TRY OF THE TEXT DECODING PROGRAM HERE I HOPE FOR GOOD RESULTS BECAUSE IT IS DESIRED AND OTHERWISE
I WILL BE UNHAPPY'''

stripped = StrippedText(plain, alphabeto)
encrypted = encrypt_decrypt_text(stripped, [4, 3, 2, 11, 4])
stripped.alphabetic_signs = encrypted

print(stripped.get_non_stripped_text())


fixed_procedure(stripped, standard, [1, 20, 20, 14, 4], 2, 10000)
if __name__ == '__main__':
    unittest.main()