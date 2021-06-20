#!/usr/bin/env python3

from enum import Enum
import numpy as np
import random

import baseball.baseball as bb

#verbose=False
verbose=True

num_innings=1
#num_innings=9


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
            while outs < 3:
                on_first = False
                on_second = False
                on_third = False
                strikes = 0
                balls = 0
                batting = True
                if verbose:
                    print(f'Batter up, outs {outs}')
                while batting:
                    possible_outcomes = bb.list_outcomes(on_first, on_second, on_third)
                    outcome = random.choices(possible_outcomes, weight=None, k=1)[0]
                    if verbose:
                        print(f'pitch outcome {outcome}')
    
                    # Process batter's outcomes
                    if outcome[0] == 'strike':
                        strikes += 1 

#                    elif outcome == Outcomes.FOUL:
#                        # TODO: There is a chance of stealing
#                        if (strikes < 2):
#                            strikes += 1
#
#                    elif outcome == Outcomes.BALL:
#                        # TODO: There is a chance of stealing
#                        balls += 1

                    #elif outcome == Outcomes.OUT:
                    elif outcome[0] == 'out':
                        batting = False
                        outs += 1

                    elif outcome == Outcomes.FIRST:
                        batting = False
                        on_first = True
#                        if not True in bases: # No players on base, put batter on first.
#                            bases[0] = True
#
#                        # Runners are on what bases?
#                        runner_bases = []
#                        for i, base in enumerate(bases):
#                            if base:
#                                runner_bases.append(i + 1)
#
#                        # Consider leading running
#                        possible_bases = range(runner_bases[-1], 4)
#                        out = [-1] + list(possible_bases) # -1 here will imply an out.
#                        choice = random.choices(out, weights=None, k=1)
#                        if choice == -1:
#                            outs += 1
#                            if outs == 3:
#                                break

                    elif outcome == Outcomes.SECOND:
                        if not True in bases: # No players on base, put batter on second
                            bases[1] = True

                        # TODO: Need state of players on bases
                        batting = False

                    elif outcome == Outcomes.THIRD:
                        if not True in bases: # No players on base, put batter on third
                            bases[1] = True
                        # TODO: Need state of players on bases
                        batting = False

                    elif outcome == Outcomes.HOMER:
                        batting = False
                        score[team] += 1

                        # Any players on base score
                        # TODO: there is a possibility of a home run where people get out
                        # and there are pickles etc.
                        for base in bases:
                            if base:
                                score[team] += 1

                    else:
                        raise f'Invalid outcome: {outcome}.'
    
                    if strikes == 3:
                        batting = False
                        outs += 1
                        if outs == 3:
                            break
    
                    if balls == 4:
                        # TODO: Put player on first
                        batting = False
                        pass
    
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
    games = 1 
    scores = np.zeros([games,2])

    for i in range(games):
        score = simulate_game()
        scores[i] = score[0], score[1]

    team_one_wins = len(np.where(scores[:,0] > scores[:,1])[0])
    print(f'Team one probability: {team_one_wins/games}')


    

