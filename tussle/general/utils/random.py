import random


def generate_random_string(lowercase_letters=True, uppercase_letters=True, numbers=True, length=20):
    # Compute the complete list of characters we have to work with
    characters = []
    if lowercase_letters:
        characters += list("abcdefghijklmnopqrstuvwxyz")
    if uppercase_letters:
        characters += list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if numbers:
        characters += list("0123456789")

    # Generate a random string of the desired length
    result = ""
    for i in range(length):
        result += random.choice(characters)

    return result

