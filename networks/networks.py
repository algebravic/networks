"""
Some sorting networks.
"""
from typing import Iterable, List, Tuple

def bitonic(num: int) -> Iterable[Tuple[int, int]]:
    """
    Bitonic network, per Wikipedia
    """
    kind = 2
    while kind <= num:
        jind = kind // 2
        while jind > 0:
            for ind in range(num):
                lval = ind ^ jind
                if lval > ind:
                    if (ind & kind) == 0:
                        yield ind, lval
                    else:
                        yield lval, ind
            jind //= 2
        kind *= 2
