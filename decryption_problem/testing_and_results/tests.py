import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.data.data_generator as data_generator
import decryption_problem.ciphers.vigenere as vigenere
import decryption_problem.ciphers.autokey as autokey
import decryption_problem.ciphers.vigenere_extended as extended
import decryption_problem.algorithm.vigenere_decoder as vigenere_decoder
import decryption_problem.algorithm.autokey_decoder as autokey_decoder
import decryption_problem.algorithm.extended_decoder as extended_decoder
import decryption_problem.common.common as common
from timeit import default_timer as time
import random
from decryption_problem.testing_and_results.metrics import consistency_vigenere, consistency_vigenere_extended

random.seed(time)

alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
standard2 = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions_uppercase.json")
standard1 = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions_uppercase.json")
standard3 = data_generator.get_log_distribution_from_json("../data/trigram_log_distributions_uppercase.json")
# standard4 = data_generator.get_log_distribution_from_json("../data/quadrigram_log_distributions_uppercase.json")

print(standard1)

plain = alphabetic.StrippedText('''   IF YOUTH, THROUGHOUT ALL HISTORY, HAD HAD A CHAMPION TO STAND UP FOR IT; 
TO SHOW A DOUBTING WORLD THAT A CHILD CAN THINK; AND, POSSIBLY, DO IT PRACTICALLY; YOU WOULDN’T CONSTANTLY 
RUN ACROSS FOLKS TODAY WHO CLAIM THAT “A CHILD DON’T KNOW ANYTHING.” A CHILD’S BRAIN STARTS FUNCTIONING AT BIRTH; 
AND HAS, AMONGST ITS MANY INFANT CONVOLUTIONS, THOUSANDS OF DORMANT ATOMS, INTO WHICH GOD HAS PUT A MYSTIC 
POSSIBILITY FOR NOTICING AN ADULT’S ACT, AND FIGURING OUT ITS PURPORT.
UP TO ABOUT ITS PRIMARY SCHOOL DAYS A CHILD THINKS, NATURALLY, ONLY OF PLAY. BUT MANY A 
FORM OF PLAY CONTAINS DISCIPLINARY FACTORS. “YOU CAN’T DO THIS,” OR “THAT PUTS YOU OUT,” 
SHOWS A CHILD THAT IT MUST THINK, PRACTICALLY, OR FAIL. NOW, IF, THROUGHOUT CHILDHOOD, 
A BRAIN HAS NO OPPOSITION, IT IS PLAIN THAT IT WILL ATTAIN A POSITION OF “STATUS QUO,” AS WITH OUR ORDINARY ANIMALS. 
MAN KNOWS NOT WHY A COW, DOG OR LION WAS NOT BORN WITH A BRAIN ON A PAR WITH OURS; WHY SUCH ANIMALS CANNOT ADD, SUBTRACT, 
OR OBTAIN FROM BOOKS AND SCHOOLING, THAT PARAMOUNT POSITION WHICH MAN HOLDS TODAY.''', alphabet)

print(common.get_bigrams_in_coords(plain, 0))

code = data_generator.generate_random_extended_key_fixed(alphabet, 80)

print(len(code))
print(len(plain))
coprimes = extended.get_coprimes(alphabet.length)
coprimes_mapping = extended.get_coprimes_mapping(coprimes)
encryption = extended.encrypt_decrypt_text(plain, code, alphabet, coprimes)
x = extended_decoder.get_max_monogram_state(encryption, standard1, len(code), alphabet)
print(extended.encrypt_decrypt_text(encryption, x, alphabet, coprimes).get_non_stripped_text())
# print([- i % alphabet.length for i in code])
print(consistency_vigenere_extended(x, [extended.reverse_key(i, alphabet, coprimes, coprimes_mapping)
                                        for i in code], alphabet.length))
res = extended_decoder.break_fixed_length_code_with_mcmc(encryption, alphabet,
                                                         x,
                                                         [3], [1.0],
                                                         [standard3],
                                                         100000)


maxx_state = res[0]
maxx_weight = res[1]

print(maxx_weight)
print(consistency_vigenere_extended(maxx_state, [extended.reverse_key(i, alphabet, coprimes, coprimes_mapping)
                                        for i in code], alphabet.length))
decrypted1 = extended.encrypt_decrypt_text(encryption, maxx_state, alphabet, coprimes)

decrypted2 = plain
state_function = 0
frequencies = common.calculate_n_gram_frequencies(decrypted2, 2)
state_function += common.calculate_n_gram_log_weight(frequencies, standard2)
print(state_function)

print(decrypted1.get_non_stripped_text())
print()
print(decrypted2.get_non_stripped_text())

maximizer = extended_decoder.get_max_bigram_state(encryption, standard2, len(code), alphabet)[0]
decrypted3 = extended.encrypt_decrypt_text(encryption, maximizer,
                                           alphabet, coprimes)
frequencies = common.calculate_n_gram_frequencies(decrypted3, 2)
state_function = common.calculate_n_gram_log_weight(frequencies, standard2)
print(decrypted3.get_non_stripped_text())
print(state_function)
print(maximizer)
print(consistency_vigenere(maximizer, [extended.reverse_key(i, alphabet, coprimes, coprimes_mapping)
                                        for i in code], alphabet.length))

