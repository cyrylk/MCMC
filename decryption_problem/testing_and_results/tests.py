import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.data.data_generator as data_generator
import decryption_problem.ciphers.vigenere as vigenere
import decryption_problem.ciphers.autokey as autokey
import decryption_problem.ciphers.vigenere_extended as extended
import decryption_problem.algorithm.vigenere_decoder as vigenere_decoder
import decryption_problem.common.common as common


alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
standard2 = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions_uppercase.json")
standard1 = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions_uppercase.json")

print(standard1)

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
OR OBTAIN FROM BOOKS AND SCHOOLING, THAT PARAMOUNT POSITION WHICH MAN HOLDS TODAY.''', alphabet)


code = [10, 11, 3, 11, 15, 20, 18, 12, 25, 8, 22, 21, 4, 23, 5, 22, 15, 22, 16, 24, 3, 25, 19, 24, 16, 23, 23, 7, 4, 23,
        25, 1, 17, 15, 1, 0, 8, 7, 25, 8, 19, 17, 1, 1, 4, 23, 6, 16, 18, 18, 8, 1, 13, 5, 2, 1, 5, 8, 10, 10, 8, 24,
        20]

encryption = vigenere.encrypt_decrypt_text(plain, code, alphabet)
res = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, alphabet,
                                                         vigenere_decoder.get_max_monogram_state(encryption,
                                                                                                 standard1, len(code),
                                                                                                 alphabet), [2], [1.0],
                                                         [standard2],
                                                         15000)
maxx_state = res[0]
maxx_weight = res[1]

print(maxx_weight)
decrypted1 = vigenere.encrypt_decrypt_text(encryption, maxx_state, alphabet)

decrypted2 = vigenere.encrypt_decrypt_text(encryption, [-i for i in code], alphabet)
state_function = 0
frequencies = common.calculate_n_gram_frequencies(decrypted2, 2)
state_function += common.calculate_n_gram_log_weight(frequencies, standard2)
print(state_function)

print(decrypted1.get_non_stripped_text())
print()
print(decrypted2.get_non_stripped_text())

maximizer = vigenere_decoder.get_max_bigram_state(encryption, standard2, len(code), alphabet)[0]
decrypted3 = vigenere.encrypt_decrypt_text(encryption, maximizer,
                                           alphabet)
frequencies = common.calculate_n_gram_frequencies(decrypted3, 2)
state_function = common.calculate_n_gram_log_weight(frequencies, standard2)
print(decrypted3.get_non_stripped_text())
print(state_function)
print([(-i) % 26 for i in code])
print(maximizer)

