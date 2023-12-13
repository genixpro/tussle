from dependency_injector.wiring import inject, Provide
import base64
import hashlib


def compute_random_completion_index_from_randomized_value(randomized_value, temperature, config=Provide['config']):
    """
    This function calculates an exact index from a randomized value and a temperature.
    Basically the index is supposed to indicate which one of the multiple
    cached completions we are going to pull. This allows us to have multiple
    completions for the same prompt, and then we can pick one of them randomly
    based on the randomized value. This is a nice compromise between the desire
    to cache completions, and the desire to get a variety of fresh completions

    :param randomized_value:
    :param temperature:
    :return:
    """

    # This code ensures that we keep more completions for higher temperatures,
    # since those involve more creativity and randomness, thus we don't want
    # to generate the exact same completion over and over again.
    return max(0, round(randomized_value * temperature * config['completion']['completion_cache_number_of_variants_per_temperature_unit']))


def compute_hash_for_prompt(prompt):
    return str(base64.b64encode(hashlib.sha256(prompt.encode('utf-8')).digest()), 'utf8')
