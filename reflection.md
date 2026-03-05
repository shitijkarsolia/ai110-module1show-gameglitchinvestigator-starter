# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first examined the game code, I identified several critical bugs:

**Bug 1: Backwards hints** - The hint messages were completely reversed. When my guess was too high (greater than the secret), the game told me "📈 Go HIGHER!" instead of telling me to go lower. Similarly, when my guess was too low, it said "📉 Go LOWER!" when I actually needed to go higher. This made the game impossible to win by following the hints.

**Bug 2: Type confusion on even attempts** - On every even-numbered attempt (2nd, 4th, 6th guess), the code converted the secret number from an integer to a string (lines 158-161 in app.py). This caused unpredictable comparison behavior because comparing an integer guess to a string secret uses alphabetical ordering instead of numerical ordering.

**Bug 3: Hardcoded range messages** - The game always displayed "Guess a number between 1 and 100" regardless of the selected difficulty level. Easy mode should be 1-20, Normal 1-100, and Hard 1-50, but the message never updated to reflect the actual range.

---

## 2. How did you use AI as a teammate?

I primarily used VS Code Copilot to help me reason about the bugs and refactor the game logic. Instead of asking it to magically “fix everything,” I treated it like a pair-programmer: I asked targeted questions about specific functions, edge cases, and how to structure my tests. The AI was especially helpful at quickly pointing out suspicious code paths and suggesting where to add assertions.

One correct suggestion from the AI was to move the core guessing logic into a pure helper function in `logic_utils.py` and write unit tests around it. The agent proposed implementing `check_guess` there and then adding a pytest case that simulated the old bug where the secret number was stored as a string. I verified that this was a good idea by running `pytest` and confirming that all four tests (including the new one) passed, and by playing the game to see that “Too High/Too Low” hints behaved correctly even after multiple guesses.

An example of a more incomplete/misleading suggestion was when the AI initially focused only on flipping the “Go HIGHER/Go LOWER” messages in `app.py` without immediately addressing the deeper state/type issue. That change made the hints look correct on the surface, but the game could still behave strangely because the secret was sometimes treated as a string. I realized this fix was not enough when I compared the debug panel values with my guesses and saw inconsistent behavior, which pushed me to ask the AI follow-up questions about Streamlit state and types and then simplify the logic to always compare against the numeric `st.session_state.secret`.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when both the automated tests and the live game behavior matched the rules I had written down for the game. After each change, I ran `pytest` inside the virtual environment and confirmed that the original tests plus my new `test_get_range_for_difficulty_hard_mode_bug_fixed` all passed. I also manually played several rounds on each difficulty level, watching the debug panel to confirm that the secret stayed within the correct range, the hints matched the comparison, and the attempts/score counters behaved as expected even after hitting "New Game." The AI helped me design these tests by encouraging me to move logic into `logic_utils.py` and then write focused tests for tricky cases like a string secret and the hard-mode range, which gave me much more confidence that the fixes would stick.

---

## 4. What did you learn about Streamlit and state?

I learned that in the original app the secret number kept changing because it was being recomputed on each rerun instead of being stored safely in `st.session_state`. Every time I clicked a button, Streamlit re-executed the script top to bottom, which meant any plain variables were reset unless they were explicitly put into session state. To a friend, I would explain that a Streamlit app is like a function that reruns on every interaction, and `st.session_state` is a special dictionary that remembers values across those reruns. The key change I made was to initialize the secret only when `"secret" not in st.session_state` and always read from that stored value, which finally gave the game a stable secret number throughout a playthrough.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing small, focused tests around any logic that feels even slightly tricky, and running them frequently while I refactor. Another habit is treating AI tools as a brainstorming partner instead of an oracle: I’ll keep asking it for explanations and alternative designs, but I’ll verify everything with tests and by reading the code myself. Next time I work with AI, I’ll be quicker to push back on suggestions that only change surface-level behavior (like just flipping hint strings) and insist on understanding the underlying state or data model first. Overall, this project made me more skeptical of “working” AI-generated code and more confident that I need to stay in control of the debugging process, using AI as support rather than as a replacement for my own reasoning.
