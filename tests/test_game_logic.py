import json
import os
import sys
import tempfile

# Ensure the project root (where logic_utils.py lives) is on the import path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from logic_utils import check_guess, get_range_for_difficulty, load_high_scores, save_high_score

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


def test_get_range_for_difficulty_hard_mode_bug_fixed():
    """
    The game previously behaved inconsistently with difficulty ranges.
    This test verifies that the logic helper returns the correct range for each mode,
    especially that Hard mode uses 1–50 instead of the generic 1–100 range.
    """
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    # Unknown difficulty should fall back to the Normal range
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- High Score feature tests (added via Agent Mode) ---

def test_load_high_scores_missing_file():
    """load_high_scores returns empty dict when the file doesn't exist."""
    assert load_high_scores("/tmp/nonexistent_hs.json") == {}


def test_save_and_load_high_score():
    """Round-trip: save a score then load it back."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    try:
        # First save should always be a new high score
        assert save_high_score("Normal", 80, 3, path) is True
        scores = load_high_scores(path)
        assert scores["Normal"]["score"] == 80
        assert scores["Normal"]["attempts"] == 3

        # A lower score should NOT overwrite
        assert save_high_score("Normal", 50, 5, path) is False
        scores = load_high_scores(path)
        assert scores["Normal"]["score"] == 80  # unchanged

        # A higher score SHOULD overwrite
        assert save_high_score("Normal", 90, 1, path) is True
        scores = load_high_scores(path)
        assert scores["Normal"]["score"] == 90
    finally:
        os.unlink(path)


def test_high_scores_separate_by_difficulty():
    """Each difficulty level tracks its own high score independently."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    try:
        save_high_score("Easy", 70, 2, path)
        save_high_score("Hard", 40, 4, path)
        scores = load_high_scores(path)
        assert scores["Easy"]["score"] == 70
        assert scores["Hard"]["score"] == 40
        assert "Normal" not in scores
    finally:
        os.unlink(path)
