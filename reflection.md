# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The system is built around four classes that mirror the real-world entities in a pet care workflow:

- **Task** — a Python dataclass representing a single care action. It holds `description`, `task_type` (walk, feeding, medication, etc.), `time` ("HH:MM"), `duration_minutes`, `priority` ("low"/"medium"/"high"), `frequency` ("once"/"daily"/"weekly"), `due_date`, `completed` status, and the `pet_name` it belongs to. Its two methods are `mark_complete()` (which sets `completed = True` and schedules the next occurrence for recurring tasks) and `is_recurring()` (returns True if frequency is not "once").

- **Pet** — a dataclass holding a pet's `name`, `species`, `breed`, and a list of `Task` objects. It exposes `add_task()` to attach tasks, `list_tasks()` to retrieve all tasks, and `get_pending_tasks()` to return only incomplete ones.

- **Owner** — holds the owner's `name` and a list of `Pet` objects. It provides `add_pet()` to register a new pet, `list_pets()` to view them, and `get_all_tasks()` which aggregates every task across all pets into a single flat list.

- **Scheduler** — the intelligence layer. It holds a reference to the `Owner` and operates on all tasks across all pets. Its methods are: `sort_by_time()` (sorts by HH:MM string), `sort_by_priority()` (sorts high → medium → low, then by time), `filter_tasks(pet_name, completed)` (returns a filtered subset), `detect_conflicts()` (returns warning strings for tasks scheduled at the same time for the same pet), and `get_todays_schedule()` (returns all tasks due today, sorted by priority then time).

The three core actions I designed around are: **add a pet and its tasks**, **generate a sorted daily schedule**, and **detect task conflicts**.

**b. Design changes**

One meaningful change occurred during the conflict detection implementation. The initial UML design scoped `detect_conflicts()` to flag conflicts *for the same pet only* (using `(pet_name, time)` as the lookup key). During implementation it became clear that an owner physically cannot be in two places at once, so a conflict between Biscuit's medication at 08:00 and Mochi's vet check-up at 08:00 is equally problematic. The key was changed to just `time`, making the detector cross-pet by default. This was a small but important correctness fix that the initial design had overlooked.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: **time** (the `HH:MM` slot a task is assigned to) and **priority** (high / medium / low). A secondary constraint is **frequency** — whether a task is once, daily, or weekly — which drives recurring task creation. I decided priority matters most because a pet owner should always see critical care (medication, feeding) before optional enrichment activities, even if an enrichment task is earlier in the day. Time is the tiebreaker within the same priority tier.

**b. Tradeoffs**

The conflict detector flags any two tasks that share the exact same `HH:MM` string, across any pets. This is intentionally lightweight — it does **not** check for overlapping durations (e.g., a 60-minute appointment at 08:00 overlapping a 30-minute walk at 08:30). That tradeoff is reasonable here because the app targets a single owner managing a small number of pets at home; exact-time collisions are the most actionable signal, and duration-overlap detection would require significantly more complex interval arithmetic without meaningfully improving the user experience at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

GitHub Copilot (Claude Sonnet) was used throughout every phase via VS Code chat. The most effective uses were: (1) **design brainstorming** — asking "design 4 OOP classes for a pet care app with these responsibilities" to generate the initial UML and class skeletons rapidly; (2) **scaffolding** — generating `pawpal_system.py` stubs from the UML description, saving significant boilerplate time; (3) **test generation** — asking "write pytest tests for sorting, recurrence, and conflict detection" produced a solid starting suite; and (4) **wiring the UI** — asking how `st.session_state` works to persist objects across Streamlit reruns. The most helpful prompt pattern was attaching a specific file and asking a targeted question (e.g., "given this Task dataclass, how should mark_complete handle recurring tasks using timedelta?") rather than open-ended questions.

**b. Judgment and verification**

The AI's initial `detect_conflicts()` implementation scoped conflicts to the same pet only, using `(pet_name, time)` as the dictionary key. I rejected this because a single owner managing multiple pets cannot attend to two pets at the same time slot — the bug would have silently missed real scheduling conflicts in the demo data (Biscuit's medication and Mochi's vet check-up both at 08:00). I verified the fix by manually running `main.py` and confirming the conflict warning appeared, then adding a dedicated pytest test (`test_detect_conflicts_flags_same_time`) to lock in the correct behavior permanently.

---

## 4. Testing and Verification

**a. What you tested**

Six behaviors were tested: (1) `mark_complete()` sets `completed = True`, (2) `add_task()` increases the pet's task count, (3) `sort_by_time()` returns tasks in chronological order, (4) marking a daily task complete auto-creates a next-day occurrence via `timedelta`, (5) `detect_conflicts()` flags two tasks at the same time slot, and (6) `filter_tasks(pet_name=...)` returns only the specified pet's tasks. These tests are important because they cover the two required behaviors plus all four algorithmic features — if any of these break, the scheduler's core value to the user is compromised.

**b. Confidence**

Confidence level: 5/5 for the implemented behaviors. All 6 tests pass consistently. The main untested edge case is duration-based overlap detection (e.g., a 60-min task at 08:00 overlapping a 30-min task at 08:30) — the current detector only flags exact time matches. If I had more time, I would add tests for: an owner with zero pets, a pet with no tasks, a weekly recurring task advancing 7 days, and priority-sort stability when two tasks share the same priority and time.

---

## 5. Reflection

**a. What went well**

The "CLI-first" workflow worked extremely well. Building and verifying all logic in `pawpal_system.py` and `main.py` before touching `app.py` meant the Streamlit integration was straightforward — there were no surprises because the backend was already proven. The tabulate-formatted CLI output also made it easy to visually confirm that sorting, filtering, and conflict detection were all behaving correctly before writing a single test.

**b. What you would improve**

In the next iteration I would add duration-aware conflict detection — instead of only flagging exact time matches, check whether any two tasks' time windows overlap (start_time + duration_minutes). I would also add a data persistence layer so the Owner and Pet state survives between Streamlit sessions, removing the need to re-enter everything on each page reload.

**c. Key takeaway**

The most important lesson was that **AI accelerates scaffolding but cannot replace design judgment**. The AI generated correct-looking code for conflict detection that had a subtle logical flaw (same-pet only). Without understanding the system's intent — that one owner manages all pets — I would have shipped a broken feature that passed a naive test. Being the "lead architect" means staying responsible for the *why* behind every design decision, using AI to handle the *how* faster.
