import decryption_problem.alphabetic.alphabetic as alphabetic
from math import gcd
from sympy import mod_inverse


## @brief function for encrypting/decrypting single letter in Vigenere cipher
# @param letter – letter to be encrypted/decrypted
# @param shift – how many places letter is to be shifted in the alphabetic
# alphabetic - alphabetic used
def encrypt_decrypt_single(letter, key, alphabet, coprimes):
    if letter not in alphabet:
        return letter
    return alphabet[(coprimes[key[0]] * alphabet.letters_to_position[letter] + key[1]) % alphabet.length]


def create_stripped_encryption_decryption(text, encryption_decryption, alphabet):
    result = alphabetic.StrippedText(encryption_decryption, alphabet)
    result.set_ends_of_words(text.ends_of_words)
    result.set_stripped_part(text.stripped_part)
    return result


## @brief function for coding/decoding text in given Vigenere cipher
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabetic - alphabetic used
def encrypt_decrypt_text(text, shift_key, alphabet, coprimes):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet, coprimes))
        current_key_ptr = (current_key_ptr + 1) % key_length
    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)
    return encrypted_decrypted


def update_decryption_by_key_index(decryption, text, changed_index, key, key_length, alphabet, coprimes):
    for index in range(changed_index, len(decryption), key_length):
        decryption[index] = encrypt_decrypt_single(text[index], key, alphabet, coprimes)


def get_coprimes(length):
    return [i for i in range(length) if gcd(i, length) == 1]


def reverse_mono_key(key, alphabet, coprimes, coprimes_mapping):
    reverse_a = mod_inverse(coprimes[key[0]], alphabet.length)
    reverse_b = (-reverse_a * key[1]) % alphabet.length
    return coprimes_mapping[reverse_a], reverse_b


def reverse_key(key, alphabet, coprimes, coprimes_mapping):
    return [reverse_mono_key(a, alphabet, coprimes, coprimes_mapping) for a in key]


def get_coprimes_mapping(coprimes):
    mapping = {}
    for i in range(len(coprimes)):
        mapping[coprimes[i]] = i
    return mapping


def get_zero_mono_key():
    return 0, 0


def get_all_mono_keys(alphabet, coprimes):
    return [(i, j) for i in range(len(coprimes)) for j in range(alphabet.length)]
