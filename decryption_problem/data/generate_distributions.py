import json
import decryption_problem.data.data_generator as data_generator
import string
from decryption_problem.alphabetic.alphabetic import Alphabet


all_printable = data_generator.get_string_cleared(string.printable + " ")
upper_printable = all_printable[:10] + all_printable[36:]
complete_alphabet = Alphabet(data_generator.get_string_cleared(string.printable + " "))
upper_alphabet = Alphabet(upper_printable)


bigram_log_distributions_all = \
    data_generator.generate_log_distribution_from_learning_set([
    data_generator.get_string_cleared("war_and_peace.txt"),
    data_generator.get_string_cleared("oliver_twist.txt"),
    data_generator.get_string_cleared("pride_and_prejudice.txt")], complete_alphabet, 2)

bigram_log_distributions_upper = \
    data_generator.generate_log_distribution_from_learning_set([
    data_generator.get_string_cleared("war_and_peace.txt").upper(),
    data_generator.get_string_cleared("oliver_twist.txt").upper(),
    data_generator.get_string_cleared("pride_and_prejudice.txt").upper()], upper_alphabet, 2)

monogram_log_distributions_all = \
    data_generator.generate_log_distribution_from_learning_set([
    data_generator.get_string_cleared("war_and_peace.txt"),
    data_generator.get_string_cleared("oliver_twist.txt"),
    data_generator.get_string_cleared("pride_and_prejudice.txt")], complete_alphabet, 1)

monogram_log_distributions_upper = \
    data_generator.generate_log_distribution_from_learning_set([
    data_generator.get_string_cleared("war_and_peace.txt").upper(),
    data_generator.get_string_cleared("oliver_twist.txt").upper(),
    data_generator.get_string_cleared("pride_and_prejudice.txt").upper()], upper_alphabet, 1)

trigram_log_distributions_all = \
    data_generator.generate_log_distribution_from_learning_set([
    data_generator.get_string_cleared("war_and_peace.txt"),
    data_generator.get_string_cleared("oliver_twist.txt"),
    data_generator.get_string_cleared("pride_and_prejudice.txt")], complete_alphabet, 3)

trigram_log_distributions_upper = \
    data_generator.generate_log_distribution_from_learning_set([
    data_generator.get_string_cleared("war_and_peace.txt").upper(),
    data_generator.get_string_cleared("oliver_twist.txt").upper(),
    data_generator.get_string_cleared("pride_and_prejudice.txt").upper()], upper_alphabet, 3)


file1 = open("bigram_log_distributions.json", "w")
file2 = open("bigram_log_distributions_uppercase.json", "w")
file3 = open("monogram_log_distributions.json", "w")
file4 = open("monogram_log_distributions_uppercase.json", "w")
file5 = open("trigram_log_distributions.json", "w")
file6 = open("trigram_log_distributions_uppercase.json", "w")
json.dump(bigram_log_distributions_all, file1)
json.dump(bigram_log_distributions_upper, file2)
json.dump(monogram_log_distributions_all, file3)
json.dump(monogram_log_distributions_upper, file4)
json.dump(trigram_log_distributions_all, file5)
json.dump(trigram_log_distributions_upper, file6)
file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
file6.close()

