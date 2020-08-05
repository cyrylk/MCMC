import random


def get_random_swap(size):
    smaller = random.randint(0, size-2)
    return smaller, random.randint(smaller+1, size-1)

