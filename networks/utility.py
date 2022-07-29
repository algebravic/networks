"""
Utility functions for sorting networks
"""

from typing import List, Tuple
from functools import partial
from collections import Counter
from itertools import chain

def flip(fst: int, snd: int, trg: int) -> int:
    """
    Apply a transposition.
    """
    return fst if trg == snd else (snd if trg == fst else trg)

def diff(tup1: Tuple[int], tup2: Tuple[int]) -> int:
    """
    Number of differences between corresponding elements
    """
    return sum((int(_[0] != _[1]) for _ in zip(tup1, tup2)))

def standardize(net: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Knuth section 5.3.4 exercise 16, page 239
    """
    num = len(net)
    changes = 0

    while True:

        # Find bad pair
        place = None
        for ind, (left, right) in enumerate(net):
            if left > right:
                place = ind
                lft, rgt = left, right
                break

        if place is None:
            break
        tfn = partial(flip, lft, rgt)

        for jind in range(place, num):
            val = tuple(map(tfn, net[jind]))
            changes += diff(val, net[jind])
            net[jind] = val

    print(f"There were {changes} changes")
        
def network_histogram(net: List[Tuple[int, int]]) -> Counter:
    """
    Return a histogram of the number of times an element is touched.
    """
    return Counter(chain(*net))
