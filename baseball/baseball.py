
from enum import Enum
import itertools

class OutStates(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2

class RunnerStates(Enum):
    NONE = 0
    B1 = 1
    B2 = 2
    B3 = 3
    B12 = 4
    B13 = 5
    B23 = 6
    B123 = 7

class ThirdOutStates(Enum):
    RUNS_0 = 0
    RUNS_1 = 1
    RUNS_2 = 2
    RUNS_3 = 3

# The order here is important to match Blake's matrix.
possible_states = list(itertools.product(list(OutStates), list(RunnerStates))) + list(ThirdOutStates)

def get_index(state):
    for i, s in enumerate(possible_states):
        if state == s:
            return i
        else:
            raise LookupError(f'State {state} isn\'t a possible baseball state.')


