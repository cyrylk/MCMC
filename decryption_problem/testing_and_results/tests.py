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
upper_trigrams_distribution = data_generator.get_log_distribution_from_json\
    ("../data/trigram_log_distributions_uppercase.json")
full_bigrams_distribution = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions.json")
full_monograms_distribution = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions.json")
full_trigrams_distribution = data_generator.get_log_distribution_from_json("../data/trigram_log_distributions.json")

vigenere_alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alpha_qwerty_alphabet = alphabetic.Alphabet('''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$''' +
                                            '''%^&*()_-=+{}[]|;:"<>,.?/''')

code = data_generator.generate_random_vigenere_key_fixed(alpha_qwerty_alphabet, 245)
coded = autokey.encrypt_text(alphabetic.StrippedText
                                      (data_generator.get_string_cleared(
    data_generator.generate_random_excerpt("../data/1984.txt", 1000)),
                                       alpha_qwerty_alphabet),
                                      code,
                                      alpha_qwerty_alphabet)


print("ORIGINAL")
print(coded.get_non_stripped_text())
x = autokey_decoder.get_max_monogram_state(coded, full_monograms_distribution, 245, alpha_qwerty_alphabet)
print("MAX MONOGRAM")
print(autokey.decrypt_text(coded, x[0], alpha_qwerty_alphabet).get_non_stripped_text(), x[1])
print("MONOGRAM CONSISTENCY")
print(consistency(x[0], autokey.reverse_key(code, alpha_qwerty_alphabet), alpha_qwerty_alphabet))


result = autokey_decoder.break_bounded_length_code_with_mcmc_monogram_criteria(coded, alpha_qwerty_alphabet,
                                                   [2], [1.0], [full_bigrams_distribution], 100000, 250,
                                                                               full_monograms_distribution)

print(len(result[0]))
print("MAX BIGRAM")
print(autokey.decrypt_text(coded, result[0], alpha_qwerty_alphabet).get_non_stripped_text())
print("BIGRAM CONSISTENCY")
print(consistency(result[0], autokey.reverse_key(code, alpha_qwerty_alphabet), alpha_qwerty_alphabet))


