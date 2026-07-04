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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: **time** (the `HH:MM` slot a task is assigned to) and **priority** (high / medium / low). A secondary constraint is **frequency** — whether a task is once, daily, or weekly — which drives recurring task creation. I decided priority matters most because a pet owner should always see critical care (medication, feeding) before optional enrichment activities, even if an enrichment task is earlier in the day. Time is the tiebreaker within the same priority tier.

**b. Tradeoffs**

The conflict detector flags any two tasks that share the exact same `HH:MM` string, across any pets. This is intentionally lightweight — it does **not** check for overlapping durations (e.g., a 60-minute appointment at 08:00 overlapping a 30-minute walk at 08:30). That tradeoff is reasonable here because the app targets a single owner managing a small number of pets at home; exact-time collisions are the most actionable signal, and duration-overlap detection would require significantly more complex interval arithmetic without meaningfully improving the user experience at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
