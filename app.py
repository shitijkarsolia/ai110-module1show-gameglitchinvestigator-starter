import random
import streamlit as st

# FIX: Refactored core game logic into shared helpers with guidance from an AI coding agent.
from logic_utils import get_range_for_difficulty, parse_guess, update_score, load_high_scores, save_high_score


def check_guess(guess, secret):
    # FIX: Debugged and corrected the hint logic together with an AI assistant.
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


# FEATURE (Challenge 4): Enhanced Game UI — color-coded Hot/Cold hints with emojis,
# progress bar, and session summary table, built with an AI coding agent.

def get_hot_cold_hint(guess, secret, low, high):
    """Return a Hot/Cold emoji label and CSS color based on distance from the secret."""
    distance = abs(guess - secret)
    total_range = high - low
    ratio = distance / total_range if total_range > 0 else 1

    if ratio <= 0.05:
        return "🔥🔥🔥 BOILING!", "#ff1744"
    elif ratio <= 0.15:
        return "🔥 Hot!", "#ff5722"
    elif ratio <= 0.30:
        return "🌡️ Warm", "#ff9800"
    elif ratio <= 0.50:
        return "🌤️ Cool", "#42a5f5"
    else:
        return "❄️ Freezing!", "#1565c0"


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="centered")

# FEATURE (Challenge 4): Custom CSS for enhanced visuals
st.markdown("""
<style>
    .hot-cold-badge {
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        display: inline-block;
        margin: 4px 0;
    }
    .session-summary {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .progress-label {
        font-size: 0.85rem;
        color: #aaa;
        margin-bottom: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FEATURE: High Score display — planned and built with an AI coding agent (Agent Mode).
# The agent suggested loading scores from a JSON file keyed by difficulty and showing
# them prominently in the sidebar so players always know the score to beat.
st.sidebar.divider()
st.sidebar.subheader("🏆 High Scores")
high_scores = load_high_scores()
for diff in ["Easy", "Normal", "Hard"]:
    entry = high_scores.get(diff)
    if entry:
        st.sidebar.metric(f"{diff}", f"{entry['score']} pts", f"in {entry['attempts']} guesses")
    else:
        st.sidebar.caption(f"{diff}: No score yet")

if "secret" not in st.session_state:
    # FIX: Stabilized the secret number range per difficulty after debugging with an AI pair-programmer.
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIX: Reset attempts correctly to avoid off-by-one errors spotted during AI-assisted testing.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIX: Synced the player-facing range message with the actual difficulty bounds using AI feedback.
attempts_left = attempt_limit - st.session_state.attempts
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

# FEATURE (Challenge 4): Attempts progress bar — visual indicator of remaining guesses
# Use a placeholder so the bar updates after the guess is processed (avoids off-by-one display).
st.markdown('<p class="progress-label">Attempts used</p>', unsafe_allow_html=True)
progress_placeholder = st.empty()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Reset all game state consistently for new sessions after walking through edge cases with an AI assistant.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

    # FEATURE (Challenge 4): Game Session Summary Table — shown after win or loss
    import pandas as pd
    numeric_hist = [g for g in st.session_state.history if isinstance(g, (int, float))]
    if numeric_hist:
        secret = st.session_state.secret
        summary_data = []
        for i, g in enumerate(numeric_hist, 1):
            dist = abs(g - secret)
            hint_label, _ = get_hot_cold_hint(g, secret, low, high)
            if g == secret:
                direction = "🎯 Correct"
            elif g > secret:
                direction = "📉 Too High"
            else:
                direction = "📈 Too Low"
            summary_data.append({
                "Guess #": i,
                "Value": g,
                "Direction": direction,
                "Proximity": hint_label,
                "Distance": dist,
            })
        st.subheader("📋 Game Session Summary")
        result_emoji = "🏆 WIN" if st.session_state.status == "won" else "💀 LOSS"
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Result", result_emoji)
        col_b.metric("Score", st.session_state.score)
        col_c.metric("Attempts", f"{st.session_state.attempts} / {attempt_limit}")
        st.dataframe(
            pd.DataFrame(summary_data),
            use_container_width=True,
            hide_index=True,
        )
    # Fill progress bar before st.stop() so it shows the final attempt count
    progress_placeholder.progress(
        st.session_state.attempts / attempt_limit,
        text=f"{st.session_state.attempts} / {attempt_limit}",
    )
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        # FIX: Removed the string-conversion bug for the secret number after discussing Streamlit state with an AI assistant.
        # Always compare against the numeric secret stored in session state.
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)
            # FEATURE (Challenge 4): Color-coded Hot/Cold proximity hint
            if outcome != "Win":
                hint_label, hint_color = get_hot_cold_hint(guess_int, secret, low, high)
                st.markdown(
                    f'<span class="hot-cold-badge" style="background:{hint_color}; color:#fff;">'
                    f'{hint_label}</span>',
                    unsafe_allow_html=True,
                )

        # FIX: Adjusted attempt indexing for scoring after pairing with an AI to analyze test runs.
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts - 1,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # FEATURE: Persist high score on win — agent-suggested to call save_high_score here
            # so the leaderboard in the sidebar updates automatically on the next rerun.
            is_new = save_high_score(difficulty, st.session_state.score, st.session_state.attempts)
            extra = " 🏆 New high score!" if is_new else ""
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}{extra}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# FEATURE: Guess History sidebar — the AI agent recommended visualizing how close each
# guess was to the secret using a bar chart so players can see their convergence pattern.
numeric_history = [g for g in st.session_state.history if isinstance(g, (int, float))]
if numeric_history:
    st.sidebar.divider()
    st.sidebar.subheader("📊 Guess History")
    secret = st.session_state.secret
    # Show a table: guess number, value, and distance from secret
    import pandas as pd
    df = pd.DataFrame({
        "Guess #": list(range(1, len(numeric_history) + 1)),
        "Value": numeric_history,
        "Distance": [abs(g - secret) for g in numeric_history],
    })
    st.sidebar.dataframe(df, use_container_width=True, hide_index=True)
    # Bar chart of distance — should trend toward 0 if the player is converging
    st.sidebar.bar_chart(df.set_index("Guess #")["Distance"])

# Fill the progress bar placeholder now that attempts have been updated
progress_ratio = st.session_state.attempts / attempt_limit
progress_placeholder.progress(progress_ratio, text=f"{st.session_state.attempts} / {attempt_limit}")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

# FIX: Moved debug panel to sidebar to prevent expander toggle from stealing button clicks.
with st.sidebar.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
