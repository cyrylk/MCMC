import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.common.common as common
import decryption_problem.ciphers.vigenere as vigenere
import decryption_problem.algorithm.vigenere_neighbours as neighbours
import decryption_problem.algorithm.vigenere_calculator as calculator
import random
from math import log


def fixed_procedure(text, distributions, starting_state, n_list, steps, alphabet, coefs):
    current_state = starting_state
    current_decryption = vigenere.encrypt_decrypt_text(text, current_state, alphabet)
    current_frequencies = []
    current_state_function = 0
    index = 0
    for n in n_list:
        freqs = common.calculate_n_gram_frequencies(current_decryption, n, alphabet)
        current_frequencies.append(freqs)
        current_state_function += common.calculate_log_n_gram_function(freqs, distributions[index])*coefs[index]
        index += 1

    max_function = current_state_function
    max_state = current_state

    for i in range(steps):
        candidate = neighbours.get_candidate_fixed(current_state, alphabet)
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
    print (current_state_function)
    return max_state, max_function


def bounded_procedure(text, distribution, starting_state, n, steps, alphabet, boundary):
    current_state = starting_state
    current_decryption = vigenere.encrypt_decrypt_text(text, current_state, alphabet)
    current_frequencies = common.calculate_n_gram_frequencies(current_decryption, n, alphabet)
    current_state_function = common.calculate_log_n_gram_function(current_frequencies, distribution)

    max_function = current_state_function
    max_state = current_state
    for i in range(steps):
        candidate = neighbours.get_candidate_bounded2(current_state, boundary, alphabet)
        if len(candidate) == len(current_state):
            frequency_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                                current_decryption, alphabet)
            dist_change = common.calculate_log_function_change(frequency_change, distribution)
            changed_index = calculator.find_change_in_key(current_state, candidate)
            shift = candidate[changed_index] - current_state[changed_index]
            u = random.random()
            if log(u) < dist_change:
                vigenere.update_decryption_by_key_index(current_decryption, changed_index, shift, len(current_state),
                                                        alphabet)
                current_state = candidate
                common.update_frequency(current_frequencies, frequency_change)
                current_state_function *= dist_change
                if current_state_function > max_function:
                    max_state = candidate
                    max_function = current_state_function
            continue

        new_decryption = vigenere.encrypt_decrypt_text(text, candidate, alphabet)
        new_frequencies = common.calculate_n_gram_frequencies(new_decryption, n, alphabet)
        new_function = common.calculate_log_n_gram_function(new_frequencies, distribution)
        u = random.random()
        diff = new_function - current_state_function
        if log(u) < diff:
            current_state = candidate
            current_state_function = new_function
            current_decryption = new_decryption
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function

    text.set_non_stripped_part(vigenere.encrypt_decrypt_text(encrypted, max_state, alphabeto).non_stripped_part)
    print(text.get_non_stripped_text())
    print(max_state)


from decryption_problem.algorithm.distribution_generator import generate_from_file_log, generate_from_file


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

code = [10, 11, 3, 11, 15, 20, 18, 12, 25, 8, 22, 21, 4, 23, 5, 22, 15, 22, 16, 24, 3, 25, 19, 24, 16, 23, 23, 7, 4, 23, 25, 1, 17, 15, 1, 0, 8, 7, 25, 8, 19, 17, 1, 1, 4, 23, 6, 16, 18, 18, 8, 1, 13, 5, 2, 1, 5, 8, 10, 10, 8, 24, 20, 23, 15, 22, 6, 16, 12, 4, 22, 13, 12, 15, 11, 24, 12, 12, 0, 5, 1, 5, 10, 19, 25, 1, 8, 0, 25, 9, 1, 19, 3, 18, 11, 22, 5, 1, 18, 23]

encrypted = vigenere.encrypt_decrypt_text(plain, code, alphabeto)
res = fixed_procedure(encrypted, [standard2], neighbours.get_starting_state_fixed(alphabeto, len(code)),
                             [2], 250000, alphabeto, [1.0])
maxx_state = res[0]
maxx_function = res[1]
# bounded_procedure(encrypted, standard2, neighbours.get_starting_state_bounded(alphabeto, 20), 2, 10000, alphabeto, 20)

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
print(maxx_function)
decrypted1 = vigenere.encrypt_decrypt_text(encrypted, maxx_state, alphabeto)

decrypted2 = vigenere.encrypt_decrypt_text(encrypted, [-i for i in code], alphabeto)
frequencies = common.calculate_n_gram_frequencies(decrypted2, 2, alphabeto)
state_function = common.calculate_log_n_gram_function(frequencies, standard2)
print(state_function)

print(decrypted1.get_non_stripped_text())
print()
print(decrypted2.get_non_stripped_text())


