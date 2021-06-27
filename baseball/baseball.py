
import copy
from dataclasses import dataclass
from enum import Enum
import itertools
import numpy as np
import scipy.stats as ss


class OutStates(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2

class RunnerStates(Enum):
    """All possible ways runners can be on bases."""
    # The length of these arrays are used to calculate number of runs given a transition.
    NONE = []# 0
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

    delta_runners = len(a[1].value) - len(b[1].value) 
    delta_outs = num_outs(b) - num_outs(a)
    return delta_runners - delta_outs + 1


def num_outs(state):
    """Calculate the number of outs for a given state."""
    for i in list(ThirdOutStates):
        if state == i:
            return 3
    for i in list(OutStates):
        if state[0] == i:
            return state[0].value

@dataclass
class Score:
    """Simply to give names to the score."""
    home: int = 0
    away: int = 0

def bottom_of(inning):
    if inning - np.floor(inning) == 0.0:
        return False
    return True

def game_over(score, inning):
    # This value used for easy debugging (i.e. to create short games)
    max_innings = 9.0 
    #max_innings = 1.0

    if inning >= max_innings:
        if score.home > score.away:
            return True
        if bottom_of(inning):
            if score.home != score.away:
                return True

    return False


class StateSampler:
    """Provide a random baseball state given current state."""
    def __init__(self, filename):
        self.__matrix = np.load('data/transitionMatrixBatByBat.npy')
        assert(self.__matrix.shape[0] == len(possible_states))
        assert(self.__matrix.shape[0] == self.__matrix.shape[1])
        # Fix the seed so we can get repeatable results if we want.
        # https://stackoverflow.com/a/63980788
        seed = 123456789
        self.__scipy_randomGen = ss.multinomial
        self.__scipy_randomGen.random_state = np.random.Generator(np.random.PCG64(seed))

    def sample(self, state):
        index = get_index(state)
        trans_probs = self.__matrix[index, :]
        # @todo TJR: Put this check in the constructor
        assert np.isclose(np.sum(trans_probs), 1.0, 1.0e-7) # @todo TJR: 1.0e-7 close enough for floating points?
        sample = self.__scipy_randomGen.rvs(n=1, p=trans_probs) #ss.multinomial.rvs(n=1, p=trans_probs)
        new_index = np.where(sample == 1)[0][0]
        return possible_states[new_index]

def play_ball():
    score = Score()
    outs = 0
    batting_team = 'away'
    inning = 1.0

    sampler = StateSampler('data/transitionMatrixBatByBat.npy')

    # Execute every inning
    while True:
        #print(f'Inning {inning}, batting {batting_team}, score: home ({score.home}), away({score.away})')
        state = (OutStates.ZERO, RunnerStates.NONE)

        at_bats = 0
        while num_outs(state) < 3:
            new_state = sampler.sample(state)

            # Update the score.
            runs = runs_scored(state, new_state)
            if batting_team == 'away':
                score.away += runs
            else:
                score.home += runs
            
            state = copy.deepcopy(new_state) # @todo TJR: Deep copy is needed right?
            
            # Prevent infinite loops from (likely) invalid transition matrices.
            at_bats += 1
            if at_bats > 100:
                raise Exception('Potential infinite loop for batters.')

        # Check if the game is over
        if game_over(score, inning):
            break
        elif inning > 20:
            raise Exception('Potential infinite loop for innings.')            

        inning += 0.5

        # change team up to bat
        if batting_team == "away":
            batting_team = 'home'
        else:
            batting_team = 'away'

    return score

