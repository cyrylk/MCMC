import decryption_problem.alphabetic.alphabetic as alphabetic


## @brief function for encrypting/decrypting single letter in autokey cipher
# @param letter – letter to be encrypted/decrypted
# @param shift – how many places letter is to be shifted in the alphabetic
# alphabetic - alphabetic used
def encrypt_decrypt_single(letter, shift, alphabet):
    if letter not in alphabet:
        return letter
    return alphabet[(alphabet.letters_to_position[letter] + shift) % alphabet.length]


def create_stripped_encryption_decryption(text, encryption_decryption, alphabet):
    result = alphabetic.StrippedText(encryption_decryption, alphabet)
    result.set_ends_of_words(text.ends_of_words)
    result.set_stripped_part(text.stripped_part)
    return result


# by assumption stripped text has to be an argument here
def encrypt_text(text, shift_key, alphabet):
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(shift_key)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr += 1

    coding_index = 0
    for index in range(len(shift_key), len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], alphabet.letters_to_position[text[coding_index]],
                                                          alphabet))
        coding_index += 1

    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)

    return encrypted_decrypted

# by assumption stripped text has to be an argument here
def decrypt_text(text, shift_key, alphabet):
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(shift_key)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr += 1

    coding_index = 0

    for index in range(len(shift_key), len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index],
                                                          -alphabet.letters_to_position[encrypted_decrypted[coding_index]],
                                                          alphabet))
        coding_index += 1

    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)

    return encrypted_decrypted


# by assumption stripped text has to be an argument here
def encrypt_text_v2(text, shift_key, alphabet):
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(shift_key)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr += 1

    coding_index = 0
    for index in range(len(shift_key), len(text)):
        if (text[index] in alphabet and text[coding_index] in alphabet):
            encrypted_decrypted.append(encrypt_decrypt_single(text[index], alphabet.letters_to_position[text[coding_index]],
                                                          alphabet))
            coding_index += 1
        else:
            encrypted_decrypted.append(text[index])

    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)

    return encrypted_decrypted

# by assumption stripped text has to be an argument here
def decrypt_text_v2(text, shift_key, alphabet):
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(shift_key)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr += 1

    coding_index = 0

    for index in range(len(shift_key), len(text)):
        if (text[index] in alphabet and text[coding_index] in alphabet):
            encrypted_decrypted.append(encrypt_decrypt_single(text[index], -alphabet.letters_to_position[text[coding_index]],
                                                          alphabet))
            coding_index += 1
        else:
            encrypted_decrypted.append(text[index])

    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)

    return encrypted_decrypted


def update_decryption_by_key_index(decryption, changed_index, shift, key_length, alphabet):
    power = 1
    for index in range(changed_index, len(decryption), key_length):
        decryption[index] = encrypt_decrypt_single(decryption[index], shift*power, alphabet)
        power *= (-1)


def get_zero_mono_key():
    return 0


def get_all_mono_keys(alphabet):
    return list(range(alphabet.length))

