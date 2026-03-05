import os
import sys

# Ensure the project root (where logic_utils.py lives) is on the import path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_guess_with_string_secret_prevents_type_bug():
    """
    Simulate the old bug where the secret number was sometimes stored as a string
    (for example on some attempts in the Streamlit app). Even if the secret is a
    string here, the logic should still correctly classify the guess.
    """
    # Exact match should still be a win
    assert check_guess(50, "50") == "Win"
    # Higher and lower comparisons should still behave numerically, not break with TypeError
    assert check_guess(60, "50") == "Too High"
    assert check_guess(40, "50") == "Too Low"
