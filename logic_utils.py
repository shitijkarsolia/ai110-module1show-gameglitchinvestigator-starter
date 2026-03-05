import json
import os

HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "high_scores.json")


# FEATURE: High Score tracker — planned and implemented with an AI coding agent (Agent Mode).
# The agent suggested persisting scores to a JSON file keyed by difficulty so that
# high scores survive across Streamlit reruns and browser refreshes.

def load_high_scores(path: str = HIGH_SCORE_FILE) -> dict:
    """Load high scores from a JSON file. Returns a dict keyed by difficulty."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_high_score(difficulty: str, score: int, attempts: int, path: str = HIGH_SCORE_FILE) -> bool:
    """Save score if it beats the current high score for the given difficulty.

    Returns True if a new high score was set, False otherwise.
    """
    scores = load_high_scores(path)
    entry = scores.get(difficulty)

    if entry is None or score > entry["score"]:
        scores[difficulty] = {"score": score, "attempts": attempts}
        with open(path, "w") as f:
            json.dump(scores, f, indent=2)
        return True
    return False


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Clarified difficulty ranges by extracting this helper with an AI pair-programmer.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    # Default to the Normal range for any unexpected difficulty value
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Hardened input parsing and error messages together with an AI assistant.
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return an outcome string.

    Outcome examples: "Win", "Too High", "Too Low".

    This function is also robust to the secret being stored as a string
    (which used to happen on some attempts in the Streamlit app), so it
    guards against that bug coming back.
    """
    # FIX: Refactored comparison logic into a testable helper with guidance from an AI coding agent.
    try:
        if guess == secret:
            return "Win"
        if guess > secret:
            return "Too High"
        return "Too Low"
    except TypeError:
        # Fallback: coerce both values to ints if they were different types
        g = int(guess)
        s = int(secret)
        if g == s:
            return "Win"
        if g > s:
            return "Too High"
        return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Tuned scoring curve and attempt-based bonuses using Copilot Agent mode feedback.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
