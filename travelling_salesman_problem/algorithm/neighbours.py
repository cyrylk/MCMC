import random


def get_random_swap(size):
    smaller = random.randint(0, size-2)
    return smaller, random.randint(smaller+1, size-1)

def get_random_swap2(size):
    smaller = random.randint(0, size-1)
    return smaller, random.randint(smaller+1, smaller + size - 1) % size

