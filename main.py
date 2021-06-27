#!/usr/bin/env python3


import copy
from dataclasses import dataclass
import numpy as np
import random
import scipy.stats as ss

import baseball.baseball as bb


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

def play_ball():
    score = Score()
    outs = 0
    batting_team = 'away'
    inning = 1.0

    matrix = np.load('data/transitionMatrixBatByBat.npy')
    assert(matrix.shape[0] == len(bb.possible_states))
    assert(matrix.shape[0] == matrix.shape[1])
    #print(matrix[0,:])

    # Execute every inning
    while True:
        #print(f'Inning {inning}, batting {batting_team}, score: home ({score.home}), away({score.away})')
        state = (bb.OutStates.ZERO, bb.RunnerStates.NONE)

        at_bats = 0
        while bb.num_outs(state) < 3: # half-inning
            # Sample a state transition 
            index = bb.get_index(state)
            trans_probs = matrix[index, :]
            assert np.isclose(np.sum(trans_probs), 1.0, 1.0e-7) # @todo TJR: 1.0e-7 close enough for floating points?
            sample = ss.multinomial.rvs(n=1, p=trans_probs)
            new_index = np.where(sample == 1)[0][0]
            new_state = bb.possible_states[new_index]

            # Calculate the number of runs scored
            runs = bb.runs_scored(state, new_state)
            #print(f'runs {runs}, outs {bb.num_outs(new_state)}')
            if batting_team == 'away':
                score.away += runs
            else:
                score.home += runs

            
            state = copy.deepcopy(new_state) # @todo TJR: Deep copy is needed right?
            
            # Prevent infinite loops from (likely) invalid transition matrices.
            at_bats += 1
            if at_bats > 100:
                raise Exception('Infinite loop for batters.')

        # Check if the game is over
        if game_over(score, inning):
            break
        elif inning > 20:
            raise Exception('Infinite loop for innings.')            

        inning += 0.5

        # change team up to bat
        if batting_team == "away":
            batting_team = 'home'
        else:
            batting_team = 'away'

    return score


if __name__ == '__main__':
    """Run many games and calculate some stats."""
    games = 1000
    scores = np.zeros([games, 2])
    for i in range(games):
        score = play_ball()
        scores[i] = score.home, score.away

    team_one_wins = len(np.where(scores[:,0] > scores[:,1])[0])
    print(f'Team one probability: {team_one_wins/games}')
    print(f'Mean scores: {np.mean(scores)}')
    print(f'std  scores: {np.std(scores)}')


    

