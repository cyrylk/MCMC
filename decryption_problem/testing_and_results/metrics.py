

def consistency_vigenere(guessed_key, real_key, alphabet_length):
    guessed_copy = guessed_key[:]
    real_copy = real_key[:]
    while len(guessed_copy) != len(real_copy):
        if len(guessed_copy) > len(real_copy):
            real_copy += real_key
        else:
            guessed_copy += guessed_key
    consistency = 0
    for i in range(len(guessed_copy)):
        if not (guessed_copy[i] - real_copy[i]) % alphabet_length:
            consistency += 1

    return consistency/len(guessed_copy)

def consistency_vigenere_extended(guessed_key, real_key, alphabet_length):
    guessed_copy = guessed_key[:]
    real_copy = real_key[:]
    while len(guessed_copy) != len(real_copy):
        if len(guessed_copy) > len(real_copy):
            real_copy += real_key
        else:
            guessed_copy += guessed_key
    consistency = 0
    for i in range(len(guessed_copy)):
        if not (guessed_copy[i][0] - real_copy[i][0]) % alphabet_length or \
                not (guessed_copy[i][1] - real_copy[i][1]) % alphabet_length:
            consistency += 1

    return consistency/len(guessed_copy)


