# Standard Library Imports
import math


def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


def round_to_nearest_multiple(number, multiple):
    return multiple * normal_round(number / float(multiple))


def round_to_nearest_5(number):
    return round_to_nearest_multiple(number, multiple=5)


def sumof(*args):
    """
    Sum all the elements exclude None entries.
    """
    sum = 0
    for arg in args:
        if arg is not None:
            sum += arg
    return sum
