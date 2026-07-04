# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the CLI demo with:

```bash
python main.py
```

```
============================================================
  🐾  PawPal+ Daily Planner  —  Saturday, July 04 2026
  Owner: Jordan
============================================================

📅  TODAY'S SCHEDULE  (sorted by priority → time)

╭────────┬─────────────────────────┬─────────┬────────────┬────────────┬─────────────┬────────╮
│ Time   │ Task                    │ Pet     │ Priority   │ Duration   │ Frequency   │ Done   │
├────────┼─────────────────────────┼─────────┼────────────┼────────────┼─────────────┼────────┤
│ 07:00  │ 🍖 Morning feeding       │ Biscuit │ HIGH       │ 10 min     │ daily       │ ⬜      │
│ 07:30  │ 🍖 Morning feeding       │ Mochi   │ HIGH       │ 10 min     │ daily       │ ⬜      │
│ 08:00  │ 💊 Heartworm medication  │ Biscuit │ HIGH       │ 5 min      │ weekly      │ ⬜      │
│ 08:00  │ 🏥 Vet check-up          │ Mochi   │ HIGH       │ 60 min     │ once        │ ⬜      │
│ 17:30  │ 🦮 Evening walk          │ Biscuit │ HIGH       │ 30 min     │ daily       │ ⬜      │
│ 11:00  │ 🧸 Playtime / enrichment │ Mochi   │ MEDIUM     │ 20 min     │ daily       │ ⬜      │
│ 14:00  │ ✂️  Grooming session     │ Biscuit │ LOW        │ 45 min     │ once        │ ⬜      │
╰────────┴─────────────────────────┴─────────┴────────────┴────────────┴─────────────┴────────╯

🚨  CONFLICT DETECTION

  ⚠️  Conflict at 08:00: "Heartworm medication" (Biscuit) and "Vet check-up" (Mochi)

🔄  RECURRING TASK DEMO

  Completing: 'Morning feeding' for Biscuit (due 2026-07-04)
  ✅ Marked complete. Next occurrence auto-created: due 2026-07-05

============================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by time | `Scheduler.sort_by_time()` | Sorts all tasks across all pets chronologically by `HH:MM` string using a lambda key |
| Sort by priority | `Scheduler.sort_by_priority()` | Sorts high → medium → low, then by time as a tiebreaker — used in `get_todays_schedule()` |
| Filter by pet / status | `Scheduler.filter_tasks(pet_name, completed)` | Returns a filtered subset; both params are optional |
| Conflict detection | `Scheduler.detect_conflicts()` | Flags any two tasks sharing the same time slot (across all pets); returns warning strings without crashing |
| Recurring tasks | `Task.mark_complete()` | When a daily/weekly task is marked complete, auto-creates the next occurrence using `timedelta(days=1)` or `timedelta(weeks=1)` |
| Today's schedule | `Scheduler.get_todays_schedule()` | Filters tasks due today, then sorts by priority → time |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
