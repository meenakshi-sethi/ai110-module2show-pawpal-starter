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

Run the full test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

| Test | What it verifies |
|------|-----------------|
| `test_mark_complete_sets_completed_true` | `Task.mark_complete()` sets `completed = True` |
| `test_add_task_increases_pet_task_count` | `Pet.add_task()` increases the pet's task list length |
| `test_sort_by_time_returns_chronological_order` | `Scheduler.sort_by_time()` returns tasks in HH:MM order |
| `test_daily_task_creates_next_occurrence` | Marking a daily task complete auto-creates a next-day task via `timedelta` |
| `test_detect_conflicts_flags_same_time` | `Scheduler.detect_conflicts()` flags two tasks at the same time slot |
| `test_filter_tasks_by_pet_name` | `Scheduler.filter_tasks(pet_name=...)` returns only that pet's tasks |

### Passing Test Output

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 6 items

tests/test_pawpal.py::test_mark_complete_sets_completed_true PASSED      [ 16%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 33%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 50%]
tests/test_pawpal.py::test_daily_task_creates_next_occurrence PASSED     [ 66%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time PASSED       [ 83%]
tests/test_pawpal.py::test_filter_tasks_by_pet_name PASSED               [100%]

============================== 6 passed in 0.01s ===============================
```

**Confidence Level: ⭐⭐⭐⭐⭐ (5/5)** — All 6 tests pass, covering the two required behaviors (task completion, task addition) plus sorting correctness, recurring task recurrence, conflict detection, and filtering. The only untested edge case is duration-overlap conflict detection, which is a documented tradeoff.

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

### Running the CLI demo

```bash
python main.py
```

This creates owner **Jordan** with two pets — **Biscuit** (Golden Retriever) and **Mochi** (Siamese) — and 7 tasks across both pets. The output shows:
- Today's schedule sorted by **priority → time** (HIGH tasks first, then MEDIUM, then LOW)
- All tasks sorted by **time only**
- A filtered view of **pending tasks for Biscuit**
- A **conflict warning** for 08:00 (Biscuit's medication overlaps Mochi's vet check-up)
- A **recurring task demo**: Biscuit's daily morning feeding is marked complete and a new task is auto-created for the next day

See the full CLI output in the [Sample Output](#%EF%B8%8F-sample-output) section above.

### Running the Streamlit app

```bash
streamlit run app.py
```

1. **Set your name** — Enter your name in the sidebar and click "Set / Update Owner". This creates an `Owner` object stored in `st.session_state` that persists for the entire session.
2. **Add a pet** — Fill in the pet name, species, and breed in the sidebar form and click "Add Pet". Each submission calls `Owner.add_pet()` and stores a real `Pet` object in memory.
3. **Schedule a task** — Select a pet, fill in the task details (description, type, time, priority, frequency, due date), and click "Add Task". This calls `Pet.add_task()` with a fully typed `Task` dataclass instance.
4. **Generate schedule** — Click the "Generate schedule" button. The app calls `Scheduler.detect_conflicts()` and displays any time-slot conflicts as `st.warning()` banners. It then shows today's tasks sorted by priority → time, and all tasks sorted by time.
5. **Review your pets** — The "Your Pets" section at the bottom shows each pet in an expandable card with their pending task count and a full task table.

### Key Scheduler behaviors visible in the UI
- **Priority-first sorting**: HIGH tasks always appear before MEDIUM and LOW in Today's Schedule
- **Conflict warnings**: Overlapping time slots trigger orange `st.warning()` banners before the schedule is displayed
- **Cross-pet scheduling**: The schedule aggregates tasks from all pets into one unified view
- **Recurring task logic**: Tasks marked with `daily` or `weekly` frequency automatically generate their next occurrence when `mark_complete()` is called

---

## ⚡ Advanced Scheduling Logic

Beyond simple time sorting, PawPal+ implements **priority-based scheduling** via `Scheduler.sort_by_priority()`. Tasks are ordered by priority tier first (high → medium → low), then by time as a tiebreaker within each tier. This ensures a pet owner always sees the most critical care actions at the top of their schedule, regardless of when they are scheduled.

### How it works

`sort_by_priority()` uses a composite sort key `(PRIORITY_ORDER[priority], time)` where `PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}`. This is distinct from `sort_by_time()` which sorts purely chronologically.

### CLI output example — priority sort across two pets

```
╭────────┬─────────────────────────┬─────────┬────────────┬────────────╮
│ Time   │ Task                    │ Pet     │ Priority   │ Duration   │
├────────┼─────────────────────────┼─────────┼────────────┼────────────┤
│ 07:00  │ 🍖 Morning feeding       │ Biscuit │ HIGH       │ 10 min     │
│ 08:00  │ 🏥 Vet check-up          │ Mochi   │ HIGH       │ 60 min     │
│ 17:30  │ 🦮 Evening walk          │ Biscuit │ HIGH       │ 30 min     │
│ 11:00  │ 🧸 Playtime / enrichment │ Mochi   │ MEDIUM     │ 20 min     │
│ 14:00  │ ✂️  Grooming session     │ Biscuit │ LOW        │ 45 min     │
╰────────┴─────────────────────────┴─────────┴────────────┴────────────╯
```

All three HIGH tasks appear first (sorted by time within that tier), MEDIUM next, LOW last — regardless of their scheduled times. Compare this to `sort_by_time()` which would place Grooming (14:00) before Evening walk (17:30) regardless of their LOW vs HIGH priority.

---

## 🎨 Professional UI and Output Formatting

The CLI demo (`main.py`) uses structured formatting to produce readable, scannable output instead of raw Python object strings.

### Libraries and functions used

| Feature | Library / Function | Details |
|---------|--------------------|---------|
| Table rendering | `tabulate` (v0.9+) | `tablefmt="rounded_outline"` for clean bordered tables |
| Task type icons | Custom `TASK_EMOJI` dict | Maps task types to emojis: 🦮 walk, 🍖 feeding, 💊 medication, ✂️ grooming, 🧸 enrichment, 🏥 appointment |
| Completion indicator | Unicode symbols | `✅` for completed, `⬜` for pending |
| Conflict indicator | Unicode prefix | `⚠️` prefixes every conflict warning string |
| Section headers | Unicode + separators | `📅`, `⏰`, `🔍`, `🚨`, `🔄` prefix each output section |

### Installation

```bash
pip install tabulate
```

`tabulate` is included in `requirements.txt`.
