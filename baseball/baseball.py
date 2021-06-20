
import itertools

first_outcomes = ['first', 'second', 'third', 'home', 'out']
batter_outcomes = first_outcomes + ['strike', 'foul', 'ball']
second_outcomes = first_outcomes[1:]
third_outcomes = first_outcomes[2:]


def invalid(a, b):
    """Make sure b, runner leading a, is not on same base as a, or a base before a."""
    if a == 'first':
        if b in ['first']:
            return True

    if a == 'second':
        if b in ['first', 'second']:
            return True

    # TODO: Is it somehow weirdly possible for a player to go backwards?
    if a == 'third':
        if b in ['first', 'second', 'third']:
            return True

def list_outcomes(on_first, on_second, on_third):
    """List all possible outcomes for a single pitch."""
    # No players on base
    if not on_first and not on_second and not on_third:
        return batter_outcomes

    # One player on base
    if on_first and not on_second and not on_third:
        outcomes = list(itertools.product(batter_outcomes, first_outcomes))
        for bat, first in list(outcomes): # list() creates a copy so we can modify original
            if invalid(bat, first):
                outcomes.remove((bat, first))

    if not on_first and on_second and not on_third:
        outcomes = list(itertools.product(batter_outcomes, second_outcomes))
        for bat, second in list(outcomes):
            if invalid(bat, second):
                outcomes.remove((bat, second))

    if not on_first and not on_second and on_third:
        outcomes = list(itertools.product(batter_outcomes, third_outcomes))
        for bat, third in list(outcomes):
            if invalid(bat, third):
                outcomes.remove((bat, third))

    # Two players on base
    if on_first and on_second and not on_third:
        outcomes = list(itertools.product(batter_outcomes, first_outcomes, second_outcomes))
        for bat, first, second in list(outcomes):
            if invalid(bat, first) or invalid(bat, second) or invalid(first, second):
                outcomes.remove((bat, first, second))

    if on_first and not on_second and on_third:
        outcomes = list(itertools.product(batter_outcomes, first_outcomes, third_outcomes))
        for bat, first, third in list(outcomes):
            if invalid(bat, first) or invalid(bat, third) or invalid(first, third):
                outcomes.remove((bat, first, third))

    if not on_first and on_second and on_third:
        outcomes = list(itertools.product(batter_outcomes, second_outcomes, third_outcomes))
        for bat, second, third in list(outcomes):
            if invalid(bat, second) or invalid(bat, third) or invalid(second, third):
                outcomes.remove((bat, second, third))

    # Three players on base
    if on_first and on_second and on_third:
        outcomes = list(itertools.product(batter_outcomes, first_outcomes, second_outcomes, third_outcomes))
        for bat, first, second, third in list(outcomes):
            invalid_bat = invalid(bat, first) or invalid(bat, second) or invalid(bat, third)
            if invalid_bat or invalid(first, second) or invalid(first, third) or invalid(second, third):
                outcomes.remove((bat, first, second, third))

    return outcomes

