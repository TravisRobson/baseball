#!/usr/bin/env python3

from enum import Enum
import numpy as np
import random

import baseball.baseball as bb

verbose=False
#verbose=True

#num_innings=2
num_innings=9


def simulate_game():
    score = [0, 0]
    team = 0 # 0 or 1, depending on which team is up to bat.
    inning = 1
    while True:
            outs = 0
            if team == 0:
                if verbose:
                    print(f'Top of inning {inning}')
            else:
                if verbose:
                    print(f'Bottom of inning {inning}')

            # We need to distinguish where runners are before (init) and after the pitch
            init_on_first = False
            init_on_second = False
            init_on_third = False

            while outs < 3:
                strikes = 0
                balls = 0
                batting = True
                if verbose:
                    print(f'Batter up, outs {outs}')
                while batting:

                    on_first = init_on_first
                    on_second = init_on_second
                    on_third = init_on_third

                    possible_outcomes = bb.list_outcomes(init_on_first, init_on_second, init_on_third)
                    outcome = random.choices(possible_outcomes, weights=None, k=1)[0]
                    if isinstance(outcome, tuple):
                        batter_outcome = outcome[0]
                    else:
                        batter_outcome = outcome

                    if verbose:
                        print(f'pitch outcome {outcome}')

                    # TODO: 4 balls might goof my Cartesian product scheme a little.
                    # Not obvious where to process the result of 4 balls.

                    # Process third base runner
                    if init_on_third:
                        # TODO: Unclear how to index, it's either 1, 2, or 3. Must exist a cleaner way.
                        if init_on_first and init_on_second:
                            third_outcome = outcome[3]
                        elif (init_on_first and not init_on_second) or (not init_on_first and init_on_second):
                            third_outcome = outcome[2]
                        else:
                            third_outcome = outcome[1]

                        if third_outcome == 'out':
                            outs += 1
                            on_third = False
                        elif third_outcome == 'home':
                            score[team] += 1
                            on_third = False

                    # Process second base runner
                    if init_on_second:
                        # TODO TJR: Need better way to figure out if it's index 1 or 2
                        if init_on_first:
                            second_outcome = outcome[2]
                        else:
                            second_outcome = outcome[1]

                        if second_outcome == 'out':
                            outs += 1
                            on_second = False
                        elif second_outcome == 'third':
                            on_second = False
                            on_third = True
                        elif second_outcome == 'home':
                            on_second = False
                            score[team] += 1

                    # Process first base runner
                    if init_on_first:
                        first_outcome = outcome[1]
                        if first_outcome == 'out':
                            outs += 1
                            on_first = False
                        elif first_outcome == 'second':
                            on_first = False
                            on_second = True
                        elif first_outcome == 'third':
                            on_first = False
                            on_third = True
    
                    # Process batter's outcomes
                    if batter_outcome == 'strike':
                        strikes += 1 

                    elif batter_outcome == 'foul':
                        if (strikes < 2):
                            strikes += 1

                    elif batter_outcome == 'ball':
                        balls += 1
                        # TODO: Any other work that should go here?
                    
                    elif batter_outcome == 'out':
                        batting = False
                        outs += 1

                    elif batter_outcome == 'first':
                        batting = False
                        on_first = True

                    elif batter_outcome == 'second':
                        batting = False
                        on_second = True

                    elif batter_outcome == 'third':
                        batting = False
                        on_third = True

                    elif batter_outcome == 'home':
                        batting = False
                        score[team] += 1

                    else:
                        raise f'Invalid outcome: {batter_outcome}.'
    
                    if strikes == 3:
                        batting = False
                        outs += 1

                    init_on_first = on_first
                    init_on_second = on_second
                    init_on_third = on_third

                    # Process 4 balls
                    # TODO: Make sure this is where the 4 balls logic should go.
#                    if balls == 4:
#                        pass
#                        # TODO: I need to double check this logic
#                        if on_first and on_second and on_third:
#                            score[team] += 1
#                        elif on_first and on_second:
#                            on_third = True
#                        elif on_first and not on_second:
#                            on_second = True
#                        on_first = True
#                        batting = False


            # If was bottom of inning (team 1) then increment inning
            if team == 1:
                inning += 1
    
            # Take care of which team is up next
            if team == 0:
                team = 1
            else:
                team = 0
    
            if verbose:
                print(f'Score: {score[0]} to {score[1]}')
                print('----------------------------------\n')
            
            # Game over at 9th inning (potentially the top of 9th if home winning) or
            # when there isn't a tie past the 9th.
            # TODO: Fix logic for when the home team is winning (i.e. don't play second half of inning).
            if inning >= num_innings and team == 1 and score[0] != score[1]:
                if verbose:
                    print('Game over!')
                break

    return score


if __name__ == '__main__':
    games = 100
    scores = np.zeros([games,2])

    for i in range(games):
        score = simulate_game()
        scores[i] = score[0], score[1]

    team_one_wins = len(np.where(scores[:,0] > scores[:,1])[0])
    print(f'Team one probability: {team_one_wins/games}')
    print(f'Mean scores: {np.mean(scores)}')


    

