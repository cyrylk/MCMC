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
from math import log


upper_bigrams_distribution = data_generator.get_log_distribution_from_json\
    ("../data/bigram_log_distributions_uppercase.json")
upper_monograms_distribution = data_generator.get_log_distribution_from_json\
    ("../data/monogram_log_distributions_uppercase.json")
upper_trigrams_distribution = data_generator.get_log_distribution_from_json\
    ("../data/trigram_log_distributions_uppercase.json")
full_bigrams_distribution = data_generator.get_log_distribution_from_json("../data/bigram_log_distributions.json")
full_monograms_distribution = data_generator.get_log_distribution_from_json("../data/monogram_log_distributions.json")
full_trigrams_distribution = data_generator.get_log_distribution_from_json("../data/trigram_log_distributions.json")


scrabble = set([word[:-1] for word in open("../data/scrabble_words.txt", "r").readlines()])

vigenere_alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alpha_qwerty_alphabet = alphabetic.Alphabet('''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$''' +
                                            '''%^&*()_-=+{}[]|;:"<>,.?/''')
alpha_qwerty_space = alphabetic.Alphabet('''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$''' +
                                            '''%^&*()_-=+{}[]|;:"<>,.?/ ''')

# test case 1 (from subsection 4.5. of the thesis),
# we are testing what are the boundaries when the n-gram frequency approach has a chance to work at all by
# running deterministic mono- and bigram algorithms on some instances of the problem with different text and
# key lengths on vigenere alphabet - for vigenere cipher only, because other ciphers base
# on actually the same concept
# loop used for testing has been removed and  its examples might be found in some older revisions on
# branch dev/finalization, results are stored in monograms_and_bigrams_efficiency*.txt

# test case 2 (first from subsection 4.9. of the thesis),
# brief test of mono- and bigram methods when text is stripped of non-vigenere symbols
# testing loop removed from here, but it was the same concept as in test case 1, just non-vigenere
# symbols were removed from text before encoding and decoding it
# results in efficiency_non_vigenere_stripped814.txt

# test case 3 (second from subsection 4.9. of the thesis)
# results in unknown_length.txt

# random.seed(time())
# plain_text = data_generator.get_string_cleared(data_generator.generate_random_excerpt("../data/1984.txt", 1000)).upper()
# plain_text = alphabetic.StrippedText(plain_text, vigenere_alphabet)


# efficiency = open("unknown_length.txt", "w")
# key_lengths = [10, 50, 100, 150, 200, 240]
# efficiency.write("\\begin{center}\\begin{tabular}{" +
# "|c|c|c|} \n" +
# "\\hline RZECZYWISTA DŁUGOŚĆ & ODGADNIĘTA DŁUGOŚĆ & SKUTECZNOŚĆ\\\\ \\hline \n")
#
# for key_length in key_lengths:
#     print(key_length)
#     encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, key_length)
#     decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
#     encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)
#     breaker = vigenere_decoder.break_bounded_length_code_with_mcmc_monogram_criteria\
#         (encryption, vigenere_alphabet, [2], [1.0], [upper_bigrams_distribution], 0.25, 1, 250,
#          upper_monograms_distribution, scrabble)
#     efficiency.write(str(key_length) + " & " + str(len(breaker[0])) + " & " +
#                      str(consistency(breaker[0], decoding_key, vigenere_alphabet))[:4]
#                      + "\\\\ \\hline \n")
#
# efficiency.write("\\end{tabular}\\end{center} \n")
#
# efficiency.close()

# test case 4 (third from subsection 4.9. of the thesis)
# studying chain convergence
# results in 1984_vigenere*.txt

# random.seed(time())
# plain_text = data_generator.get_string_cleared(data_generator.generate_random_excerpt("../data/1984.txt", 1000)).upper()
# plain_text = alphabetic.StrippedText(plain_text, vigenere_alphabet)
#
#
# efficiency_MCMC = open("1984_vigenere_classic_MCMC.txt", "w")
# efficiency_deterministic = open("1984_vigenere_classic_deterministic.txt", "w")
#
# efficiency_deterministic.write("\\begin{center}\\begin{tabular}{")
# efficiency_deterministic.write("|c|c|c|} \n")
# efficiency_deterministic.write("\\hline DŁUGOŚĆ KLUCZA & CZAS & SKUTECZNOŚĆ "
#                      "\\\\ \hline \n")
# efficiency_MCMC.write("\\begin{center}\\begin{tabular}{")
# efficiency_MCMC.write("|c|c|c|c|c|c|c|c|} \\\\ \n")
# efficiency_MCMC.write("\\hline DŁUGOŚĆ KLUCZA &  MONOGRAM CZAS & MONOGRAM SKUTECZNOŚĆ & BIGRAM CZAS & BIGRAM ZBIEŻNOŚĆ "
#                      "& BIGRAM SKUTECZNOŚĆ & "
#                      "TRIGRAM CZAS & "
#                      "TRIGRAM SKUTECZNOŚĆ "
#                      "\\\\ \hline \n")
#
# for key_length in range(40, 440, 40):
#     encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, key_length)
#     decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
#     encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)
#
#     efficiency_deterministic.write(str(key_length)+" & ")
#     efficiency_MCMC.write(str(key_length) + " & ")
#
#     start = time()
#     monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
#                                                                  key_length, vigenere_alphabet)
#     interval = time() - start
#     efficiency_MCMC.write(str(interval)[:4] + "s" + " & " +
#                           str(consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet))
#                           + " & ")
#     start = time()
#     bigram_maximizer = vigenere_decoder.get_max_bigram_state(encryption, upper_bigrams_distribution,
#                                                              key_length,
#                                                              vigenere_alphabet)
#     interval = time() - start
#
#     efficiency_deterministic.write(str(interval)[:4] + "s" + " & " +
#                           str(consistency(bigram_maximizer[0], decoding_key, vigenere_alphabet))[:4]
#                           + " \\\\ \\hline \n")
#
#     steps = int(5*len(vigenere.get_all_mono_keys(vigenere_alphabet)) * key_length * (log(key_length) + 5))
#     all_thresholds = [0.3, 0.35,  0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
#     effective = [thr for thr in all_thresholds if thr >
#                  consistency(monogram_maximizer[0], bigram_maximizer[0], vigenere_alphabet)]
#
#     start = time()
#     decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, monogram_maximizer[0],
#                                                                 [2], [1.0], [upper_bigrams_distribution], steps,
#                                                                 bigram_maximizer[0], effective)
#     interval = time() - start
#
#     steps_when_achieved = decode[2] + ["-" for i in range(len(effective) - len(decode[2]))]
#     print(effective, steps_when_achieved)
#     convergence_pairs = {str(effective[i]): str(steps_when_achieved[i])
#                          for i in range(len(effective))}
#     efficiency_MCMC.write(str(interval)[:4] + "s" + " & \\makecell{" +
#                           "\\\\".join([thr + ": " + convergence_pairs[thr] for thr in convergence_pairs]) +
#                           "\\\\ max kroków: " + str(steps) +
#                           "} & " + str(consistency(decode[0], decoding_key, vigenere_alphabet))[:4] + " & ")
#     start = time()
#     decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, decode[0],
#                                                                 [3], [1.0], [upper_trigrams_distribution], steps//4)
#     interval = time() - start
#     efficiency_MCMC.write(str(interval)[:4] + "s" + " & " + str(consistency(decode[0], decoding_key,
#                                                                             vigenere_alphabet))[:4] +
#                           " \\\\ \\hline \n")
#     print(key_length)
#
#
# efficiency_MCMC.write("\\end{tabular}\\end{center} \n")
# efficiency_deterministic.write("\\end{tabular}\\end{center} \n")
# efficiency_MCMC.close()
# efficiency_deterministic.close()

random.seed(time())
plain_text = data_generator.get_string_cleared(data_generator.generate_random_excerpt("../data/madame_bovary.txt", 1000)).upper()
plain_text = alphabetic.StrippedText(plain_text, vigenere_alphabet)


efficiency_MCMC = open("bovary_vigenere_classic_MCMC.txt", "w")

efficiency_MCMC.write("\\begin{center}\\begin{tabular}{")
efficiency_MCMC.write("|c|c|c|c|c|c|c|} \n")
efficiency_MCMC.write("\\hline \\makecell{DŁUGOŚĆ\\\\KLUCZA} &  \\makecell{MONOGRAM\\\\CZAS} & "
                      "\\makecell{MONOGRAM\\\\SKUTECZNOŚĆ} & \\makecell{BIGRAM\\\\CZAS} &  "
                      "\\makecell{BIGRAM\\\\SKUTECZNOŚĆ} & \\makecell{TRIGRAM\\\\CZAS} & "
                      "\\makecell{TRIGRAM\\\\SKUTECZNOŚĆ}"
                     "\\\\ \hline \n")

for key_length in range(40, 440, 40):
    encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, key_length)
    decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
    encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)

    efficiency_MCMC.write(str(key_length) + " & ")

    start = time()
    monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
                                                                 key_length, vigenere_alphabet)
    interval = time() - start
    efficiency_MCMC.write(str(interval)[:4] + "s" + " & " +
                          str(consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet))
                          + " & ")
    steps = int(10*len(vigenere.get_all_mono_keys(vigenere_alphabet)) * key_length)
    start = time()
    decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, monogram_maximizer[0],
                                                                [2], [1.0], [upper_bigrams_distribution], steps)
    interval = time() - start

    efficiency_MCMC.write(str(interval)[:4] + "s" + " & " + str(consistency(decode[0], decoding_key, vigenere_alphabet))[:4] +
                          " & ")
    start = time()
    decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, decode[0],
                                                                [3], [1.0], [upper_trigrams_distribution], steps)
    interval = time() - start
    efficiency_MCMC.write(str(interval)[:4] + "s" + " & " + str(consistency(decode[0], decoding_key,
                                                                            vigenere_alphabet))[:4] +
                          " \\\\ \\hline \n")
    print(key_length)


efficiency_MCMC.write("\\end{tabular}\\end{center} \n")
efficiency_MCMC.close()

# plain_text = alphabetic.StrippedText(
#     data_generator.get_string_cleared(data_generator.generate_random_excerpt("../data/1984.txt", 2000)).upper(),
#     vigenere_alphabet)
# # encoding_key = data_generator.generate_random_vigenere_key_fixed(alpha_qwerty_space, 400)
# # decoding_key = vigenere.reverse_key(encoding_key, alpha_qwerty_space)
# # encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, alpha_qwerty_space)
# # decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, alpha_qwerty_space, [0 for i in range(400)],
# #                                                             [2], [1.0], [full_bigrams_distribution], 100000, decoding_key,
# #                                                             [0.9, 1.0])
# #
# # print(decode[2])
# # print(vigenere.encrypt_decrypt_text(encryption, decode[0], alpha_qwerty_space).get_non_stripped_text())
#
# efficiency = open("MCMC_efficiency_vigenere_classic.txt", "w")
#
# random.seed(time())
#
# encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, 10)
# decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
# encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)
#
# # opt1 = vigenere_decoder.break_bounded_length_code_with_mcmc_monogram_criteria(encryption, vigenere_alphabet,
# #                                                                        [2], [1.0], [upper_bigrams_distribution],
# #                                                                        20000, 1, 100, upper_monograms_distribution)
# #
# # opt2 = vigenere_decoder.break_bounded_length_code_with_mcmc_monogram_criteria(encryption, vigenere_alphabet,
# #                                                                        [2], [1.0], [upper_bigrams_distribution],
# #                                                                        20000, 100, 500,
# #                                                                               upper_monograms_distribution)
# #
# # split1 = re.split('[^a-zA-Z]', vigenere.encrypt_decrypt_text(encryption, opt1[0],
# #                                                              vigenere_alphabet).get_non_stripped_text())
# # split2 = re.split('[^a-zA-Z]', vigenere.encrypt_decrypt_text(encryption, opt2[0],
# #                                                              vigenere_alphabet).get_non_stripped_text())
# # i1 = 0
# # i2 = 0
# # for i in range(len(split1)):
# #     if split1[i] in scrabble:
# #         i1+=1
# #     if split2[i] in scrabble:
# #         i2+=1
# #
# # if i1 >= i2:
# #     print(len(opt1[0]))
# #
# # else:
# #     print(len(opt2[0]))
# #
# # print(consistency(opt1[0], decoding_key, vigenere_alphabet))
# # print(consistency(opt2[0], decoding_key, vigenere_alphabet))
#
# time1 = time()
# monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
#                                                              150, vigenere_alphabet)
# decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, monogram_maximizer[0],
#                                                             [2], [1.0], [upper_bigrams_distribution], 5000)
# print(common.consistency(decode[0], decoding_key, vigenere_alphabet))
# time2 = time()
# print(time2 - time1)
#
# time1 = time()
# print(consistency(vigenere_decoder.get_max_bigram_state(encryption, upper_bigrams_distribution, 150, vigenere_alphabet)[0], decoding_key,
#                   vigenere_alphabet))
# time2 = time()
# print(time2 - time1)
#
# for key_length in range(50, 1050, 50):
#     encoding_key = data_generator.generate_random_vigenere_key_fixed(vigenere_alphabet, key_length)
#     decoding_key = vigenere.reverse_key(encoding_key, vigenere_alphabet)
#     encryption = vigenere.encrypt_decrypt_text(plain_text, encoding_key, vigenere_alphabet)
#
#     efficiency.write(str(key_length)+"\\\\\n")
#
#     monogram_maximizer = vigenere_decoder.get_max_monogram_state(encryption, upper_monograms_distribution,
#                                                                  key_length, vigenere_alphabet)
#
#     efficiency.write("MONOGRAM ACCURACY: " + str(consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet))
#                      + "\\\\\n")
#
#     thres = [thr for thr in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] if thr > consistency(monogram_maximizer[0], decoding_key, vigenere_alphabet)]
#     decode = vigenere_decoder.break_fixed_length_code_with_mcmc(encryption, vigenere_alphabet, monogram_maximizer[0],
#                                                                 [2], [1.0], [upper_bigrams_distribution], 400*key_length, decoding_key, thres
#                                                               )
#
#     efficiency.write("BIGRAM ACCURACY: " + str(consistency(decode[0], decoding_key, vigenere_alphabet))
#                      + "\\\\\n")
#     efficiency.write("BIGRAM THRESHOLDS " + str(thres) + " IN STEPS : " + str(decode[2])
#                      + "\\\\\\\\\n")
#     print(key_length)
#
# efficiency.close()
