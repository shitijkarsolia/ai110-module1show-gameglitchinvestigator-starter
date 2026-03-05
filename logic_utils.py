def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


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
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
