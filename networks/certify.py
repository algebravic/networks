"""
Make up a CNF encoding a counterexample to a network being a sorting network.
"""

from typing import Tuple, List
from itertools import chain
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

def check_network(network: List[Tuple[int, int]]):
    """
    Check that this is a list of pairs of non-negative integers,
    each pair being distinct.  Output the largest element of the
    collection of all pairs + 1 (i.e. the number of channels).
    """

    if not (isinstance(network, list)
            and all((isinstance(_, tuple)
                     and len(_) == 2
                     and _[0] >= 0
                     and _[1] >= 0
                     and _[0] != _[1]) for _ in network)):
        raise ValueError("Improper input -- must be a list of distinct nonnegative integer pairs")

    support = set(chain(*network))

    channels = 1 + max(support)
    if len(support) != channels:
        print("There are gaps!")
    return channels

def is_unsorted(values: List[int], pool:IDPool, stem='x', sense: bool = True):

    unsorted = []

    for ind, (lft, rgt) in enumerate(zip(values[:-1], values[1:])):

        var = pool.id((stem, ind))
        unsorted.append(var)

        yield from [[-var, rgt], [-var, -lft], [var, -rgt, lft]]

    if sense: # unsorted
        yield unsorted
    else:
        yield from ([-_] for _ in unsorted)

def certify(network: List[Tuple[int, int]], merger: int = 0):
    """
    Test a putative sorting network using the 0/1 principle.
    Construct a SAT model to find a counterexample 0/1 sequence
    that is not sorted.

    If this is UNSAT, then we have a valid sorting network.
    We then output a proof of UNSAT in DRUP format.

    If SAT we output a counterexample.

    If merger != 0, this will certify a merging network
    for (merger, num - merger) split.
    """

    channels = check_network(network)

    # Form the input variables

    pool = IDPool()
    cnf = CNF()

    # These are are the original values
    xvars = [pool.id(('x', _)) for _ in range(channels)]

    if merger:
        cnf.extend(list(is_unsorted(xvars[: merger], pool, stem = 'bottom', sense = False)))
        cnf.extend(list(is_unsorted(xvars[merger: ], pool, stem = 'top', sense = False)))

    # These will be the current values after apply an initial segment of the network
    values = xvars.copy()

    for ind , (left, right) in enumerate(network):

        # max is OR and min is AND

        # Two new variables for min/max of the two considered locations
        min_val = pool.id(('min', ind))
        max_val = pool.id(('max', ind))

        cnf.extend([[-min_val, values[left]],
                    [-min_val, values[right]],
                    [-values[left], -values[right], min_val]])

        cnf.extend([[-max_val, values[left], values[right]],
                    [-values[left], max_val],
                    [-values[right], max_val]])

        values[left] = min_val
        values[right] = max_val

    # Now Make up the unsorted CNF

    cnf.extend(list(is_unsorted(values, pool, stem = 'unsort')))

    return cnf, pool

def get_example(model: List[int], pool: IDPool) -> List[int]:
    """
    Get the counterexample.
    """

    values = [(pool.obj(abs(_)), int(_ > 0)) for _ in model]
    x_values = [(_[0][1], _[1]) for _ in values if _[0][0] == 'x']
    support = {_[0] for _ in x_values}
    if len(support) != 1 + max(support):
        print("There were gaps")
    return [_[1] for _ in sorted(x_values)]

def certify_network(network: List[Tuple[int, int]],
                    solver_name: str = 'glucose3',
                    with_proof = False):
    """
    Use cadical to certify the sorting network, or provide a 0/1
    counterexample.
    """

    cnf, pool = certify(network)

    solver = Solver(name= solver_name, bootstrap_with = cnf,
                    use_timer = True,
                    with_proof = with_proof)

    status = solver.solve()

    print(f"Took {solver.time()} seconds")
    print(f"stats: {solver.accum_stats()}")

    return (('no good', get_example(solver.get_model(), pool)) if status
            else ('good', solver.get_proof() if with_proof else []))
