import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.algorithm.common as common
import decryption_problem.ciphers.vigenere as vigenere
import decryption_problem.algorithm.neighbours_vigenere as neighbours
import decryption_problem.algorithm.vigenere_calculator as calculator
import random


def fixed_procedure(text, distribution, starting_state, n, steps, alphabet):
    current_state = starting_state
    current_decryption = vigenere.encrypt_decrypt_text(text, current_state, alphabet)
    current_frequencies = common.calculate_n_gram_frequencies(current_decryption, n, alphabet)
    current_state_function = common.calculate_n_gram_function(current_frequencies, distribution)
    max_function = current_state_function
    max_state = current_state

    for i in range(steps):
        candidate = neighbours.get_candidate_fixed(current_state, alphabet)
        frequency_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                            current_decryption, alphabet)
        dist_change = common.calculate_function_change(frequency_change, distribution)
        changed_index = calculator.find_change_in_key(current_state, candidate)
        shift = candidate[changed_index] - current_state[changed_index]
        u = random.random()
        if u < dist_change:
            vigenere.update_decryption_by_key_index(current_decryption, changed_index, shift, len(current_state),
                                                    alphabet)
            current_state = candidate
            common.update_frequency(current_frequencies, frequency_change)
            current_state_function *= dist_change
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function

    print("".join(vigenere.encrypt_decrypt_text(text, max_state, alphabet)))


def bounded_procedure(text, distribution, starting_state, n, steps, alphabet, boundary):
    current_state = starting_state
    current_decryption = vigenere.encrypt_decrypt_text(text, current_state, alphabet)
    current_frequencies = common.calculate_n_gram_frequencies(current_decryption, n, alphabet)
    current_state_function = common.calculate_n_gram_function(current_frequencies, distribution)
    max_function = current_state_function
    max_state = current_state

    max_function = current_state_function
    max_state = current_state
    for i in range(steps):
        candidate = neighbours.get_candidate_bounded2(current_state, boundary, alphabet)
        if len(candidate) == len(current_state):
            frequency_change = calculator.get_frequency_change_fixed_key_length(current_state, candidate, n,
                                                                                current_decryption, alphabet)
            dist_change = common.calculate_function_change(frequency_change, distribution)
            changed_index = calculator.find_change_in_key(current_state, candidate)
            shift = candidate[changed_index] - current_state[changed_index]
            u = random.random()
            if u < dist_change:
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
        new_function = common.calculate_n_gram_function(new_frequencies, distribution)
        u = random.random()
        if u < new_function / current_state_function:
            current_state = candidate
            current_state_function = new_function
            current_decryption = new_decryption
            if current_state_function > max_function:
                max_state = candidate
                max_function = current_state_function

    print("".join(vigenere.encrypt_decrypt_text(text, max_state, alphabet)))
    print(max_state)


from decryption_problem.algorithm.distribution_generator import generate_from_file


from timeit import default_timer as time
random.seed(time())

standard = generate_from_file("../data/english_bigrams.txt")
alphabeto = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plain = list('''DOYOUKNOWIWANTTOFINISHTHISTHESISANDIHOPEIWILLACCOMPLISHITBECAUSEITWOULDBEVERYNICELETITBESOPLEASEREBELWITHOUTACAUSE'''+
             "ITHASTOWORKTOMAKEMEHAPPYIAMDOINGMYBEST")

encrypted = vigenere.encrypt_decrypt_text(plain, [4, 2, 5, 6, 7, 8, 9], alphabeto)
# fixed_procedure(encrypted, standard, [1, 1, 1, 1, 1], 2, 5000, alphabeto)
bounded_procedure(encrypted, standard, [17, 24, 11], 2, 5000, alphabeto, 7)
