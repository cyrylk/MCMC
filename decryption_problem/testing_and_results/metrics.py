

def consistency(guessed_key, real_key, alphabet_length):
    guessed_copy = guessed_key[:]
    real_copy = real_key[:]
    while len(guessed_copy) != len(real_copy):
        if len(guessed_copy) > len(real_copy):
            real_copy += real_key
        else:
            guessed_copy += guessed_key
    dist = 0
    for i in range(len(guessed_copy)):
        if not (guessed_copy[i] - real_copy[i]) % alphabet_length:
            dist += 1

    return dist/len(guessed_copy)


print(consistency([1, 2, 3], [1, 3], 6))

