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
from decryption_problem.common.common import consistency
import re


upper_bigrams_distribution = data_generator.get_log_distribution_from_json\
    ("../data/bigram_log_distributions_uppercase.json")
upper_monograms_distribution = data_generator.get_log_distribution_from_json\
    ("../data/monogram_log_distributions_uppercase.json")
# upper_trigrams_distribution = data_generator.get_log_distribution_from_json\
#     ("../data/trigram_log_distributions_uppercase.json")
full_bigrams_distribution = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions.json")
full_monograms_distribution = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions.json")
# full_trigrams_distribution = data_generator.get_log_distribution_from_json("../data/trigram_log_distributions.json")
scrabble = set([word[:-1] for word in open("../data/scrabble_words.txt", "r").readlines()])

vigenere_alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alpha_qwerty_alphabet = alphabetic.Alphabet('''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$''' +
                                            '''%^&*()_-=+{}[]|;:"<>,.?/''')
alpha_qwerty_space = alphabetic.Alphabet('''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$''' +
                                            '''%^&*()_-=+{}[]|;:"<>,.?/ ''')

# print(qwerty_alpha_alphabet[(alpha_qwerty_alphabet.letters_to_position["t"] +
#                              alpha_qwerty_alphabet.letters_to_position["H"])
#       % qwerty_alpha_alphabet.length])
# exp = alpha_qwerty_alphabet[(qwerty_alpha_alphabet.letters_to_position["`"])]
# exp = alpha_qwerty_alphabet[(alpha_qwerty_alphabet.letters_to_position[exp]
#                             - alpha_qwerty_alphabet.letters_to_position["H"]) % alpha_qwerty_alphabet.length]
# print(exp, alpha_qwerty_alphabet.length)

# first, we are testing what are the boundaries when the frequency approach has a chance to work at all
# (1) with vigenere alphabet - for vigenere cipher only, because other ciphers base on actually the same concept
#

plain_text = alphabetic.StrippedText(
    data_generator.get_string_cleared(data_generator.generate_random_excerpt("../data/1984.txt", 2000)).upper(),
    vigenere_alphabet)
# encoding_key = data_generator.generate_random_vigenere_key_fixed(alpha_qwerty_space, 400)
# decoding_key = vigenere.reverse_key(encoding_key, alpha_qwerty_space)
# encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, alpha_qwerty_space)
# decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, alpha_qwerty_space, [0 for i in range(400)],
#                                                             [2], [1.0], [full_bigrams_distribution], 100000, decoding_key,
#                                                             [0.9, 1.0])
#
# print(decode[2])
# print(vigenere.encrypt_decrypt_text(encryption, decode[0], alpha_qwerty_space).get_non_stripped_text())

efficiency = open("MCMC_efficiency_vigenere_classic.txt", "w")

random.seed(time())

encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, 10)
decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)

opt1 = vigenere_decoder.break_bounded_length_code_with_mcmc_monogram_criteria(encryption, vigenere_alphabet,
                                                                       [2], [1.0], [upper_bigrams_distribution],
                                                                       20000, 1, 100, upper_monograms_distribution)

opt2 = vigenere_decoder.break_bounded_length_code_with_mcmc_monogram_criteria(encryption, vigenere_alphabet,
                                                                       [2], [1.0], [upper_bigrams_distribution],
                                                                       20000, 100, 500,
                                                                              upper_monograms_distribution)

split1 = re.split('[^a-zA-Z]', vigenere.encrypt_decrypt_text(encryption, opt1[0],
                                                             vigenere_alphabet).get_non_stripped_text())
split2 = re.split('[^a-zA-Z]', vigenere.encrypt_decrypt_text(encryption, opt2[0],
                                                             vigenere_alphabet).get_non_stripped_text())
i1 = 0
i2 = 0
for i in range(len(split1)):
    if split1[i] in scrabble:
        i1+=1
    if split2[i] in scrabble:
        i2+=1

if i1 >= i2:
    print(len(opt1[0]))

else:
    print(len(opt2[0]))

print(consistency(opt1[0], decoding_key, vigenere_alphabet))
print(consistency(opt2[0], decoding_key, vigenere_alphabet))

time1 = time()
monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
                                                             150, vigenere_alphabet)
decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, monogram_maximizer[0],
                                                            [2], [1.0], [upper_bigrams_distribution], 30000)
print(common.consistency(decode[0], decoding_key, vigenere_alphabet))
time2 = time()
print(time2 - time1)

time1 = time()
print(consistency(vigenere_decoder.get_max_bigram_state(encryption, upper_bigrams_distribution, 150, vigenere_alphabet)[0], decoding_key,
                  vigenere_alphabet))
time2 = time()
print(time2 - time1)

for key_length in range(50, 1050, 50):
    encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, key_length)
    decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
    encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)

    efficiency.write(str(key_length)+"\\\\\n")

    monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
                                                                 key_length, vigenere_alphabet)

    efficiency.write("MONOGRAM ACCURACY: " + str(consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet))
                     + "\\\\\n")

    thres = [thr for thr in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] if thr > consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet)]
    decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, monogram_maximizer[0],
                                                                [2], [1.0], [upper_bigrams_distribution], 400*key_length, decoding_key, thres
                                                              )

    efficiency.write("BIGRAM ACCURACY: " + str(consistency(decode[0], decoding_key, vigenere_alphabet))
                     + "\\\\\n")
    efficiency.write("BIGRAM THRESHOLDS " + str(thres) + " IN STEPS : " + str(decode[2])
                     + "\\\\\\\\\n")
    print(key_length)

efficiency.close()
