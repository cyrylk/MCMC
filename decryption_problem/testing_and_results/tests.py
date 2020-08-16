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


upper_bigrams_distribution = data_generator.get_log_distribution_from_json\
    ("../data/bigram_log_distributions_uppercase.json")
upper_monograms_distribution = data_generator.get_log_distribution_from_json\
    ("../data/monogram_log_distributions_uppercase.json")
# upper_trigrams_distribution = data_generator.get_log_distribution_from_json\
#     ("../data/trigram_log_distributions_uppercase.json")
full_bigrams_distribution = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions.json")
full_monograms_distribution = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions.json")
# full_trigrams_distribution = data_generator.get_log_distribution_from_json("../data/trigram_log_distributions.json")
# scrabble = set([word[:-1] for word in open("../data/scrabble_words.txt", "r").readlines()])

vigenere_alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alpha_qwerty_alphabet = alphabetic.Alphabet('''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$''' +
                                            '''%^&*()_-=+{}[]|;:"<>,.?/''')
qwerty_alpha_alphabet = alphabetic.Alphabet('''qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM''' +
                                            '''`~!@#$%^&*()_-=+{}[]|;:"<>,.?/,0123456789''')

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
    data_generator.get_string_cleared(data_generator.generate_random_excerpt("../data/1984.txt", 1000).upper()),
    vigenere_alphabet)
efficiency = open("monograms_and_bigrams_efficiency1000.txt", "w")


random.seed(time())

for key_length in range(20, 600, 20):
    encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, key_length)
    decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
    encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)

    efficiency.write(str(key_length)+"\n")

    monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
                                                                 key_length, vigenere_alphabet)

    efficiency.write("MONOGRAM ACCURACY: " + str(consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet))
                     + "\n")

    bigram_maximizer = vigenere_decoder.get_max_bigram_state(encryption, upper_bigrams_distribution, key_length,
                                                             vigenere_alphabet)

    efficiency.write("BIGRAM ACCURACY: " + str(consistency(bigram_maximizer[0], decoding_key, vigenere_alphabet))
                     + "\n")
    print(key_length)

efficiency.close()
