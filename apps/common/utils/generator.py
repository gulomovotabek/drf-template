import string
import random


def get_random_string(length=4):
    # Generates a random string of letters and digits
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))
