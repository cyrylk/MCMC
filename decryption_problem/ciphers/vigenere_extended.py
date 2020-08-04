import decryption_problem.alphabetic.alphabetic as alphabetic
from math import gcd


## @brief package containing functions for encrypting and decrypting texts with Vigenere cipher


## @brief function for encrypting/decrypting single letter in Vigenere cipher
# @param letter – letter to be encrypted/decrypted
# @param shift – how many places letter is to be shifted in the alphabetic
# alphabetic - alphabetic used
def encrypt_decrypt_single(letter, key, alphabet):
    if letter not in alphabet:
        return letter
    return alphabet[(key[0] * alphabet.letters_to_position[letter] + key[1]) % alphabet.length]


def create_stripped_encryption_decryption(text, encryption_decryption, alphabet):
    result = alphabetic.StrippedText(encryption_decryption, alphabet)
    result.set_ends_of_words(text.ends_of_words)
    result.set_stripped_part(text.stripped_part)
    return result


## @brief function for coding/decoding text in given Vigenere cipher
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabetic - alphabetic used
def encrypt_decrypt_text(text, shift_key, alphabet):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr = (current_key_ptr + 1) % key_length
    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)
    return encrypted_decrypted


## @brief function for coding/decoding text in given Vigenere cipher version 2
# key is now aligned with non-alphabetic characters as well
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabetic - alphabetic used
def encrypt_decrypt_text_v2(text, shift_key, alphabet):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        if text[index] in alphabet:
            current_key_ptr = (current_key_ptr + 1) % key_length
    return encrypted_decrypted


def update_decryption_by_key_index(decryption, changed_index, shift, key_length, alphabet):
    for index in range(changed_index, len(decryption), key_length):
        decryption[index] = encrypt_decrypt_single(decryption[index], shift, alphabet)


def coprimes(length):
    return [i for i in range(length) if gcd(i, length) == 1]


print(coprimes(12))


