
import itertools
import pytest

import baseball.baseball as bb

@pytest.mark.parametrize("a, b, expected_runs", [
    (bb.possible_states[-1], bb.possible_states[-1], 3),
    (bb.possible_states[0], bb.possible_states[0], 1),
    (bb.possible_states[0], bb.possible_states[1], 0),
])
def test_num_runs(a, b, expected_runs):
    assert bb.runs_scored(a, b) == expected_runs


def test_num_outs(a, expected_outs):
    assert bb.num_outs(a) == expected_outs
