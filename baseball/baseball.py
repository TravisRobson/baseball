
from enum import Enum
import itertools

class OutStates(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2

class RunnerStates(Enum):
    """All possible ways runners can be on bases."""
    # The length of these arrays are used to calculate number of runs given a transition.
    NONE = [0]# 0
    B1 = [1] #1
    B2 = [2] #2
    B3 = [3] #3
    B12 = [1, 2] #4
    B13 = [1, 3] #5
    B23 = [2, 3]# 6
    B123 = [1, 2, 3] #7

class ThirdOutStates(Enum):
    """Values (rhs) is equal to number of runs scored. Relied on elsewhere."""
    RUNS_0 = 0
    RUNS_1 = 1
    RUNS_2 = 2
    RUNS_3 = 3

# The order here is important to match Blake's matrix.
possible_states = list(itertools.product(list(OutStates), list(RunnerStates))) + list(ThirdOutStates)

def get_index(state):
    """Which index into possible_states does 'state' correspond to?"""
    for i, s in enumerate(possible_states):
        if state == s:
            return i
    raise LookupError(f'State {state} isn\'t a possible baseball state.')

def runs_scored(a, b):
    """Given transition from state a to b how many runs were scored?"""
    for i in list(ThirdOutStates):
        if i == b:
            return b.value

    delta_runners = len(b[1].value) - len(a[1].value)
    delta_outs = b[0].value - b[0].value
    return delta_runners - delta_outs + 1


def num_outs(state):
    """Calculate the number of outs for a given state."""
    for i in list(ThirdOutStates):
        if state == i:
            return 3
    for i in list(OutStates):
        if state[0] == i:
            return state[0].value
