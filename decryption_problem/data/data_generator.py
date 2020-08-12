import decryption_problem.alphabetic.alphabetic as alphabetic
import random
from math import log, gcd
import re
import json


def generate_log_distribution_from_file(filename, alphabet, n_gram_length, additional_chars=""):
    new_alphabet = alphabetic.Alphabet(alphabet.complete_alphabet + list(additional_chars))
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = log(float(i.split()[1]))

    for i in alphabetic.n_gram_dict(new_alphabet, n_gram_length):
        if i not in freqs:
            freqs[i] = 0

    return freqs


def generate_log_distribution_from_learning_set(filenames_or_strings, alphabet, n_gram_length):
    freq_dict = alphabetic.n_gram_dict(alphabet, n_gram_length)
    for filename_or_string in filenames_or_strings:
        learning_set = filename_or_string
        try:
            if len(filename_or_string) < 100:
                f = open(filename_or_string, "r")
                learning_set = f.read()
                f.close()
        except FileNotFoundError:
            pass
        current_gram = ""
        for i in range(len(learning_set)):
            if learning_set[i] not in alphabet:
                current_gram = ""
                continue
            current_gram += learning_set[i]
            if len(current_gram) > n_gram_length:
                current_gram = current_gram[1:]
            if len(current_gram) == n_gram_length:
                freq_dict[current_gram] += 1
    for record in freq_dict:
        try:
            freq_dict[record] = log(freq_dict[record])
        except ValueError:
            freq_dict[record] = -1
    return freq_dict


def generate_random_excerpt(filename_or_string, length):
    excerpt = filename_or_string
    try:
        if len(filename_or_string) < 100:
            f = open(filename_or_string, "r")
            excerpt = f.read()
            f.close()
    except FileNotFoundError:
        pass
    begin = random.randint(0, len(excerpt) - length - 1)
    return excerpt[begin:begin+length]


def generate_random_vigenere_key_fixed(alphabet, key_length):
    key = []
    for i in range(key_length):
        key.append(random.randint(0, alphabet.length - 1))
    return key


def generate_random_vigenere_key_bounded(alphabet, bound):
    key_length = random.randint(1,bound)
    return generate_random_vigenere_key_fixed(alphabet, key_length)


def get_coprimes(length):
    return [i for i in range(length) if gcd(i, length) == 1]


def generate_random_extended_key_fixed(alphabet, key_length):
    key = []
    coprimes = get_coprimes(alphabet.length)
    for i in range(key_length):
        number = random.randint(0, alphabet.length * len(coprimes))
        key.append((number % len(coprimes), number // len(coprimes)))
    return key


def generate_random_extended_key(alphabet, bound):
    key_length = random.randint(1, bound)
    return generate_random_extended_key_fixed(alphabet, key_length)


def white_characters_to_spaces(string):
    return re.sub(r"\s+", " ", string)


def get_string_cleared(filename_or_string):
    to_clean = filename_or_string
    try:
        if len(filename_or_string) < 100:
            f = open(filename_or_string, "r")
            to_clean = f.read()
            f.close()
    except FileNotFoundError:
        pass
    return white_characters_to_spaces(to_clean)


def get_log_distribution_from_json(json_file):
    json_file = open(json_file, "r")
    return json.load(json_file)
