"""
Yield the comparator sequence for a merging network.
"""

from typing import Iterable, Tuple, List

def batcher(mnum: int, nnum: int) -> Iterable[Tuple[int, int]]:
    """
    Batcher's (m,n) network.
    """

    if not (isinstance(mnum, int) and isinstance(nnum, int)
            and mnum > 0
            and nnum > 0):
        raise ValueError("m and n must be positive integers")


def greatest_power(num: int) -> int:
    """
    Greatest power of 2 less than n
    """

    res = 1
    while res < num:
        res *= 2
    return res // 2

def bitonic_merge(base: int, size: int, par: bool) -> Iterable[Tuple[int, int]]:
    """
    The Network for a bitonic merge with size channels
    starting at base.
    """

    if size > 1:
        mnum = greatest_power(size)
        yield from ((ind, ind + mnum) if par else (ind + mnum, ind)
                    for ind in range(base, base + size - mnum))
        yield from bitonic_merge(base, mnum, par)
        yield from bitonic_merge(base + mnum, size - mnum, par)

def bitonic_sort(size: int, base: int = 0, par: bool = True) -> Iterable[Tuple[int, int]]:
    """
    Recursive construction of bitonic sort
    """
    if size > 1:
        mnum = size // 2
        yield from bitonic_sort(mnum, base = base, par = not par)
        yield from bitonic_sort(size - mnum, base = base + mnum, par = par)
        yield from bitonic_merge(base, size, par)

def group_network(net: List[Tuple[int, int]]) -> Iterable[List[Tuple[int, int]]]:
    """
    Group a sorting network into maximum parallelism
    the length of the output sequence is the depth.
    """

    support = set()
    out = []

    for pair in net:
        if support.intersection(pair):
            yield out
            out = [pair]
            support = set(pair)
        else:
            out.append(pair)
            support.update(pair)
    if support:
        yield out
