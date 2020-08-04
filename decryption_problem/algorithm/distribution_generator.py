import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.common.common as common
from math import log

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

def generate_from_file_log(filename, alphabet, n_gram_length):
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = log(float(i.split()[1]))

    for i in alphabetic.n_gram_dict(alphabet, n_gram_length):
        if i not in freqs:
            freqs[i] = 0

    return freqs

def generate_from_file_rooted(filename, alphabet, n_gram_length, root):
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = int(i.split()[1])

    normalizer = 0
    for i in freqs:
        freqs[i] = freqs[i]**(1/root)
    min_val = common.get_zero_frequency(freqs)
    for i in alphabetic.n_gram_dict(alphabet, n_gram_length):
        if i not in freqs:
            freqs[i] = min_val
    return freqs

def generate_from_file_max(filename, alphabet, n_gram_length):
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = int(i.split()[1])

    min_val = common.get_zero_frequency(freqs)
    for i in alphabetic.n_gram_dict(alphabet, n_gram_length):
        if i not in freqs:
            freqs[i] = min_val
    divisor = max(freqs.values())
    for i in freqs:
        freqs[i] /= divisor

    return freqs