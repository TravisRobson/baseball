
import itertools
import pytest

import baseball.baseball as bb

@pytest.mark.parametrize("a, b, expected_runs", [
    (bb.possible_states[-1], bb.possible_states[-1], 3),
    (bb.possible_states[0], bb.possible_states[0], 1),
])
def test_num_runs(a, b, expected_runs):
    assert bb.runs_scored(a, b) == expected_runs

