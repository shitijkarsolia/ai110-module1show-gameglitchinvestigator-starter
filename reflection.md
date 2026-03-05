# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first examined the game code, I identified several critical bugs:

**Bug 1: Backwards hints** - The hint messages were completely reversed. When my guess was too high (greater than the secret), the game told me "📈 Go HIGHER!" instead of telling me to go lower. Similarly, when my guess was too low, it said "📉 Go LOWER!" when I actually needed to go higher. This made the game impossible to win by following the hints.

**Bug 2: Type confusion on even attempts** - On every even-numbered attempt (2nd, 4th, 6th guess), the code converted the secret number from an integer to a string (lines 158-161 in app.py). This caused unpredictable comparison behavior because comparing an integer guess to a string secret uses alphabetical ordering instead of numerical ordering.

**Bug 3: Hardcoded range messages** - The game always displayed "Guess a number between 1 and 100" regardless of the selected difficulty level. Easy mode should be 1-20, Normal 1-100, and Hard 1-50, but the message never updated to reflect the actual range.

---

## 2. How did you use AI as a teammate?

I primarily used VS Code Copilot inside Cursor to help me reason about the bugs and refactor the game logic. Instead of asking it to magically “fix everything,” I treated it like a pair-programmer: I asked targeted questions about specific functions, edge cases, and how to structure my tests. The AI was especially helpful at quickly pointing out suspicious code paths and suggesting where to add assertions.

One correct suggestion from the AI was to move the core guessing logic into a pure helper function in `logic_utils.py` and write unit tests around it. The agent proposed implementing `check_guess` there and then adding a pytest case that simulated the old bug where the secret number was stored as a string. I verified that this was a good idea by running `pytest` and confirming that all four tests (including the new one) passed, and by playing the game to see that “Too High/Too Low” hints behaved correctly even after multiple guesses.

An example of a more incomplete/misleading suggestion was when the AI initially focused only on flipping the “Go HIGHER/Go LOWER” messages in `app.py` without immediately addressing the deeper state/type issue. That change made the hints look correct on the surface, but the game could still behave strangely because the secret was sometimes treated as a string. I realized this fix was not enough when I compared the debug panel values with my guesses and saw inconsistent behavior, which pushed me to ask the AI follow-up questions about Streamlit state and types and then simplify the logic to always compare against the numeric `st.session_state.secret`.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
