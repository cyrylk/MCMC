import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.common.common as common
import decryption_problem.ciphers.vigenere_extended as extended
import decryption_problem.algorithm.extended_neighbours as neighbours
import decryption_problem.algorithm.extended_calculator as calculator
import random
from math import log

from timeit import default_timer as time
random.seed(time())

def fixed_procedure(text, distributions, starting_state, n_list, steps, alphabet, coefs, coprimes):
    current_state = starting_state
    current_decryption = extended.encrypt_decrypt_text(text, current_state, alphabet, coprimes)

    current_frequencies = []
    current_state_function = 0
    index = 0
    #one function it should be from list of freqs
    for n in n_list:
        freqs = common.calculate_n_gram_frequencies(current_decryption, n, alphabet)
        current_frequencies.append(freqs)
        current_state_function += common.calculate_log_n_gram_function(freqs, distributions[index])*coefs[index]
        index += 1

    max_function = current_state_function
    max_state = current_state
    for i in range(steps):
        candidate = neighbours.get_candidate_fixed(current_state, alphabet, coprimes)
        frequencies_change = []
        dist_change = 0
        index = 0
        for n in n_list:
            freq_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                   current_decryption, text, alphabet, coprimes)
            frequencies_change.append(freq_change)

            dist_change += common.calculate_log_function_change(freq_change, distributions[index])*coefs[index]
            index += 1
        changed_index = calculator.find_change_in_key(current_state, candidate)
        u = random.random()
        if log(u) < dist_change:
            extended.update_decryption_by_key_index(current_decryption, text, changed_index, candidate[changed_index],
                                                    len(current_state),
                                                    alphabet, coprimes)
            current_state = candidate
            for f in range(len(frequencies_change)):
                common.update_frequency(current_frequencies[f], frequencies_change[f])
            current_state_function += dist_change
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function
    print(max_state, max_function)
    return max_state, max_function


from decryption_problem.algorithm.distribution_generator import generate_from_file_log





alphabeto = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
standard3 = generate_from_file_log("../data/english_trigrams.txt", alphabeto, 3)
standard2 = generate_from_file_log("../data/english_bigrams.txt", alphabeto, 2)
standard1 = generate_from_file_log("../data/english_monograms.txt", alphabeto, 1)

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

coprimess = extended.get_coprimes(alphabeto.length)
code = neighbours.get_starting_state_fixed(alphabeto, 60, coprimess)

encrypted = extended.encrypt_decrypt_text(plain, code, alphabeto, coprimess)
res = fixed_procedure(encrypted, [standard2], neighbours.get_starting_state_fixed(alphabeto, len(code), coprimess),
                             [2], 200000, alphabeto, [1.0], coprimess)
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
decrypted1 = extended.encrypt_decrypt_text(encrypted, maxx_state, alphabeto, coprimess)

# decrypted2 = extended.decrypt_text(encrypted, [-i for i, j in code], alphabeto)
# state_function = 0
# frequencies = common.calculate_n_gram_frequencies(decrypted2, 1, alphabeto)
# state_function += common.calculate_log_n_gram_function(frequencies, standard1)*0.2
# frequencies = common.calculate_n_gram_frequencies(decrypted2, 2, alphabeto)
# state_function += common.calculate_log_n_gram_function(frequencies, standard2)*0.6
# frequencies = common.calculate_n_gram_frequencies(decrypted2, 3, alphabeto)
# state_function += common.calculate_log_n_gram_function(frequencies, standard3)*0.2
# print(state_function)

print(decrypted1.get_non_stripped_text())
# print()
# print(decrypted2.get_non_stripped_text())