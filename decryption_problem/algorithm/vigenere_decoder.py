import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.common.common as common
import decryption_problem.ciphers.vigenere as vigenere
import decryption_problem.algorithm.vigenere_neighbours as neighbours
import decryption_problem.algorithm.vigenere_calculator as calculator
import random
from math import log


def get_max_monogram_state_coord(text, coordinate, monogram_dist, key_length, alphabet):
    max_state = 0
    max_func = 0
    for j in range(len(monogram_dist)):
        func = 0
        for i in range(coordinate, len(text), key_length):
            func += monogram_dist[vigenere.encrypt_decrypt_single(text[i], j, alphabet)]
        if func > max_func:
            max_state = j
            max_func = func
    return max_state


def get_max_monogram_state(text, monogram_dist, key_length, alphabet):
    return [get_max_monogram_state_coord(text, coordinate, monogram_dist, key_length, alphabet) for coordinate in
            range(key_length)]


def get_bigram_weight(text, bigram, coord, key_length, bigram_dist, alphabet):
    weight = 0
    for i in range(coord, len(text) - 1, key_length):
        text[i] = vigenere.encrypt_decrypt_single(text[i], bigram[0], alphabet)
        text[i+1] = vigenere.encrypt_decrypt_single(text[i+1], bigram[1], alphabet)
        gram = common.get_n_gram_at_i(text, 2, i)
        try:
            weight += bigram_dist[gram]
        except KeyError:
            pass
        text[i] = vigenere.encrypt_decrypt_single(text[i], -bigram[0], alphabet)
        text[i + 1] = vigenere.encrypt_decrypt_single(text[i + 1], -bigram[1], alphabet)
    return weight


def get_max_bigram_state(text, bigram_dist, key_length, alphabet):
    codes = [[[0 for i in range(key_length-1)] for a in range(alphabet.length)] for b in range(alphabet.length)]
    values = [[get_bigram_weight(text, (a, b), 0, key_length, bigram_dist, alphabet) for b in range(alphabet.length)]
              for a in range(alphabet.length)]
    new_values = [[0 for b in range(alphabet.length)] for a in range(alphabet.length)]
    for r in range(1, key_length):
        for i in range(len(codes)):
            for j in range(len(codes[i])):
                max_func = values[i][0] + get_bigram_weight(text, (0, j), r, key_length, bigram_dist, alphabet)
                max_val = 0
                for k in range(len(codes[i])):
                    func = values[i][k] + get_bigram_weight(text, (k, j), r, key_length, bigram_dist, alphabet)
                    if func > max_func:
                        max_func = func
                        max_val = k
                new_values[i][j] = max_func
                codes[i][j][r-1] = max_val

        aux = values
        values = new_values
        new_values = aux

    maxi = values[0][0]
    max_state = 0
    for i in range(len(values)):
        if values[i][i] > maxi:
            maxi = values[i][i]
            max_state = i

    print("MAXIMIZADO", maxi)
    res = []
    t = len(codes[max_state][max_state]) - 1
    current = max_state
    for i in range(len(codes[max_state][max_state])):
        current = codes[max_state][current][t]
        res.append(current)
        t -= 1
    res.append(max_state)
    res.reverse()
    return res


def fixed_procedure(text, distributions, starting_state, n_list, steps, alphabet, coefs):
    current_state = starting_state
    current_decryption = vigenere.encrypt_decrypt_text(text, current_state, alphabet)
    current_frequencies = []
    current_state_function = 0
    index = 0
    for n in n_list:
        freqs = common.calculate_n_gram_frequencies(current_decryption, n)
        current_frequencies.append(freqs)
        current_state_function += common.calculate_log_n_gram_function(freqs, distributions[index])*coefs[index]
        index += 1

    max_function = current_state_function
    max_state = current_state

    for i in range(steps):
        candidate = neighbours.get_candidate(current_state, alphabet)
        frequencies_change = []
        dist_change = 0
        index = 0
        for n in n_list:
            freq_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                   current_decryption, alphabet)
            frequencies_change.append(freq_change)

            dist_change += common.calculate_log_function_change(freq_change, distributions[index])*coefs[index]
            index += 1
        changed_index = calculator.find_change_in_key(current_state, candidate)
        shift = candidate[changed_index] - current_state[changed_index]
        u = random.random()
        if log(u) < dist_change:
            vigenere.update_decryption_by_key_index(current_decryption, changed_index, shift, len(current_state),
                                                    alphabet)
            current_state = candidate
            for f in range(len(frequencies_change)):
                common.update_frequency(current_frequencies[f], frequencies_change[f])
            current_state_function += dist_change
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function
    return max_state, max_function


from decryption_problem.algorithm.distribution_generator import generate_from_file_log


from timeit import default_timer as time
random.seed(time())

alphabeto = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

plain = alphabetic.StrippedText('''IF YOUTH, THROUGHOUT ALL HISTORY, HAD HAD A CHAMPION TO STAND UP FOR IT; 
TO SHOW A DOUBTING WORLD THAT A CHILD CAN THINK; AND, POSSIBLY, DO IT PRACTICALLY; YOU WOULDN’T CONSTANTLY 
RUN ACROSS FOLKS TODAY WHO CLAIM THAT “A CHILD DON’T KNOW ANYTHING.” A CHILD’S BRAIN STARTS FUNCTIONING AT BIRTH; 
AND HAS, AMONGST ITS MANY INFANT CONVOLUTIONS, THOUSANDS OF DORMANT ATOMS, INTO WHICH GOD HAS PUT A MYSTIC 
POSSIBILITY FOR NOTICING AN ADULT’S ACT, AND FIGURING OUT ITS PURPORT.

UP TO ABOUT ITS PRIMARY SCHOOL DAYS A CHILD THINKS, NATURALLY, ONLY OF PLAY. BUT MANY A 
FORM OF PLAY CONTAINS DISCIPLINARY FACTORS. “YOU CAN’T DO THIS,” OR “THAT PUTS YOU OUT,” 
SHOWS A CHILD THAT IT MUST THINK, PRACTICALLY, OR FAIL. NOW, IF, THROUGHOUT CHILDHOOD, 
A BRAIN HAS NO OPPOSITION, IT IS PLAIN THAT IT WILL ATTAIN A POSITION OF “STATUS QUO,” AS WITH OUR ORDINARY ANIMALS. 
MAN KNOWS NOT WHY A COW, DOG OR LION WAS NOT BORN WITH A BRAIN ON A PAR WITH OURS; WHY SUCH ANIMALS CANNOT ADD, SUBTRACT, 
OR OBTAIN FROM BOOKS AND SCHOOLING, THAT PARAMOUNT POSITION WHICH MAN HOLDS TODAY.''', alphabeto)


standard3 = generate_from_file_log("../data/english_trigrams.txt", alphabeto, 3)
standard2 = generate_from_file_log("../data/english_bigrams.txt", alphabeto, 2)
standard1 = generate_from_file_log("../data/english_monograms.txt", alphabeto, 1)

code = neighbours.get_random_starting_state(alphabeto, 40)
print(len(code))

encrypted = vigenere.encrypt_decrypt_text(plain, code, alphabeto)
res = fixed_procedure(encrypted, [standard2], get_max_monogram_state(encrypted, standard1, len(code), alphabeto),
                             [2], 15000, alphabeto, [1.0])

# res = bounded_procedure(encrypted, standard2, neighbours.get_starting_state_bounded(alphabeto, 60), 2, 15000, alphabeto,
#                         60)
maxx_state = res[0]
maxx_function = res[1]

# maxx_state = []
# maxx_function = 0
#
# for proc in range(1, 21):
#     curr = fixed_procedure(encrypted, standard, neighbours.get_starting_state_fixed(alphabeto, proc), 2,
#                            900, alphabeto)
#     if curr[1] > maxx_function:
#         maxx_state = curr[0]
#         maxx_function = curr[1]
#
print(maxx_function, maxx_state)
decrypted1 = vigenere.encrypt_decrypt_text(encrypted, maxx_state, alphabeto)

decrypted2 = vigenere.encrypt_decrypt_text(encrypted, [-i for i in code], alphabeto)
frequencies = common.calculate_n_gram_frequencies(decrypted2, 2)
state_function = common.calculate_log_n_gram_function(frequencies, standard2)
print(state_function)

print(decrypted1.get_non_stripped_text())
print()
print(decrypted2.get_non_stripped_text())
print()

print("TESTTTTTTTT")
maximizer = get_max_bigram_state(encrypted, standard2, len(code), alphabeto)
decrypted3 = vigenere.encrypt_decrypt_text(encrypted, maximizer,
                                           alphabeto)
frequencies = common.calculate_n_gram_frequencies(decrypted3, 2)
state_function = common.calculate_log_n_gram_function(frequencies, standard2)
print(decrypted3.get_non_stripped_text())
print(state_function)
print([(-i) % 26 for i in code])
print(maximizer)

# e = 0
# sol = [-i for i in code]
# for i in range(len(sol) - 1):
#     e += get_bigram_weigth(encrypted, (sol[i], sol[i+1]), i, len(sol), standard2, alphabeto)
#
# print(e)


