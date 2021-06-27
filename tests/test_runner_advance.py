
import itertools
import pytest

import baseball.baseball as bb

def test_num_runs():
    state = bb.possible_states[0]
    assert bb.runs_scored(state, state) == 0



## I don't like how the test is depending on these being spelled right, etc.
#@pytest.mark.parametrize("outcome, present", [
#    (('out', 'out'), True),
#    (('out', 'first'), True),
#    (('out', 'second'), True),
#    (('out', 'third'), True),
#    (('out', 'home'), True),
#    (('first', 'out'), True),
#    (('first', 'second'), True),
#    (('first', 'third'), True),
#    (('first', 'home'), True),
#    (('second', 'out'), True),
#    (('second', 'third'), True),
#    (('second', 'home'), True),
#    (('third', 'out'), True),
#    (('third', 'home'), True),
#    (('home', 'out'), True),
#    (('home', 'home'), True),
#    (('first', 'first'), False),
#    (('second', 'first'), False),
#    (('second', 'second'), False),
#    (('third', 'first'), False),
#    (('third', 'second'), False),
#    (('third', 'third'), False),
#    (('strike', 'first'), True)
#])
#def test_batter_first(outcome, present):
#    """Outcomes for batter and a player on first"""
#    outcomes = bb.list_outcomes(True, False, False) 
#    assert (outcome in outcomes) == present
#
#@pytest.mark.parametrize("outcome, present", [
#    (('out', 'out', 'out'), True),
#    (('first', 'second', 'third'), True),
#    (('first', 'first', 'second'), False),
#    (('first', 'third', 'second'), False),
#])
#def test_batter_first_second(outcome, present):
#    """Outcomes for batter, player on first, player on second"""
#    outcomes = bb.list_outcomes(True, True, False)
#    assert (outcome in outcomes) == present
#
#@pytest.mark.parametrize("outcome, present", [
#    (('out', 'out', 'out', 'out'), True),
#    (('first', 'second', 'third', 'home'), True),
#    (('first', 'first', 'second', 'out'), False),
#    (('first', 'third', 'second', 'out'), False),
#    (('foul', 'second', 'third', 'out'), True),
#])
#def test_bases_full(outcome, present):
#    outcomes = bb.list_outcomes(True, True, True)
#    assert (outcome in outcomes) == present

