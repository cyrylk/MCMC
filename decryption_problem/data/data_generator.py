import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.common.common as common
import random
from math import log
import re

def generate_from_file(filename, alphabet, n_gram_length, divisor):
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = int(i.split()[1])

    normalizer = 0
    for i in freqs:
        normalizer += freqs[i]
    for i in freqs:
        freqs[i] /= normalizer
        freqs[i] *= divisor

    min_val = common.get_zero_frequency(freqs)
    for i in alphabetic.n_gram_dict(alphabet, n_gram_length):
        if i not in freqs:
            freqs[i] = min_val

    return freqs


def generate_from_file_log(filename, alphabet, n_gram_length, additional_chars=""):
    new_alphabet = alphabetic.Alphabet(alphabet.alphabet + list(additional_chars))
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = log(float(i.split()[1]))

    for i in alphabetic.n_gram_dict(new_alphabet, n_gram_length):
        if i not in freqs:
            freqs[i] = 0

    return freqs


def generate_from_learning_set_log(filename_or_string, alphabet, n_gram_length, additional_chars=""):
    new_alphabet = alphabetic.Alphabet(alphabet.alphabet + list(additional_chars))
    freq_dict = alphabetic.n_gram_dict(new_alphabet, n_gram_length)
    try:
        f = open(filename_or_string, "r")
        learning_set = f.read()
        f.close()
    except FileNotFoundError:
        learning_set = filename_or_string
    current_gram = ""
    for i in range(len(learning_set)):
        if learning_set[i] not in new_alphabet:
            current_gram = ""
            continue
        current_gram += learning_set[i]
        if len(current_gram) > n_gram_length:
            current_gram = current_gram[1:]
        if len(current_gram) == n_gram_length:
            freq_dict[current_gram] += 1

    return freq_dict


def generate_random_excerpt(filename_or_string, length):
    try:
        f = open(filename_or_string, "r")
        excerpt = f.read()
        f.close()
    except FileNotFoundError:
        excerpt = filename_or_string
    begin = random.randint(0, len(excerpt) - length - 1)
    return excerpt[begin:begin+length]




def generate_random_vigenere_key(alphabet, key_length):
    key = []
    for i in range(key_length):
        key.append(random.randint(0, alphabet.length - 1))
    return key

def generate_random_vigenere_key(alphabet):
    key_length = random.randint(1,1000)
    return generate_random_vigenere_key(alphabet, key_length)


def get_coprimes(length):
    return [i for i in range(length) if gcd(i, length) == 1]

#
# def reverse_key(key, alphabet):
#     reverse_a = mod_inverse(key[0], alphabet.length)
#     reverse_b = (-reverse_a * key[1]) % alphabet.length
#     return reverse_a, reverse_b

def generate_random_extended_key(alphabet, key_length):
    key = []
    coprimes = get_coprimes(alphabet.length)
    for i in range(key_length):
        number = random.randint(0, alphabet.length * len(coprimes))
        key.append((number % len(coprimes), number // len(coprimes)))
    return key

def generate_random_vigenere_key(alphabet):
    key_length = random.randint(1, 1000)
    return generate_random_extended_key(alphabet, key_length)

def white_characters_to_spaces(string):
    return re.sub(r"\s+", " ", string)



print(generate_from_learning_set_log("war_and_peace", alphabetic.Alphabet("abc"), 2, [","]))
print(generate_random_excerpt("war_and_peace", 4))
print(white_characters_to_spaces("1\n\n  241   4"))

