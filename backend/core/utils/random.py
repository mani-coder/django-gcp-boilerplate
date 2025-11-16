# Standard Library Imports
import random

# Third Party Library Imports
from hashids import Hashids


def generate_random_key(length=32):
    hashids = Hashids(min_length=length, salt="App AI")
    return hashids.encode(random.randint(131, 19870567))
