#!/usr/bin/env python3

import argparse
import numpy as np
import sys
from tqdm import tqdm # for progress bar
import time # for progress bar

import baseball.baseball as bb

if __name__ == '__main__':
    """Run many games and calculate some stats."""
    # default values
    num_games = 10

    # Parse command line options
    parser = argparse.ArgumentParser(description='Baseball simulator')
    parser.add_argument('-n', action='store', dest='num_games', type=int, help='Number of games to simulate.', default=num_games)
    out = parser.parse_args(sys.argv[1:])
    num_games = out.num_games

    scores = np.zeros([num_games, 2])
    for i in tqdm(range(num_games), desc="Playing ball…", ascii=False, ncols=75):
        score = bb.play_ball()
        scores[i] = score.home, score.away

    team_one_wins = len(np.where(scores[:,0] > scores[:,1])[0])
    print(f'Team one probability: {team_one_wins/games}')
    print(f'Mean scores: {np.mean(scores)}')
    print(f'median scores: {np.median(scores)}')
    print(f'std  scores: {np.std(scores)}')
    
    np.save('output/scores.npy', scores)

    

