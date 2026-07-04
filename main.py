"""
PawPal+ CLI demo script.
Creates an Owner, two Pets, and several Tasks, then prints Today's Schedule
using the Scheduler, including sorting, filtering, conflict detection,
and tabulate-formatted output.
"""

from datetime import date
from tabulate import tabulate

from pawpal_system import Owner, Pet, Task, Scheduler

# ---------------------------------------------------------------------------
# Task type emoji map for readable output (Stretch: Professional Formatting)
# ---------------------------------------------------------------------------
TASK_EMOJI = {
    "walk":        "🦮",
    "feeding":     "🍖",
    "medication":  "💊",
    "grooming":    "✂️ ",
    "enrichment":  "🧸",
    "appointment": "🏥",
}

today = date.today()


def build_demo_data() -> Owner:
    """Create a sample Owner with two Pets and several Tasks."""
    owner = Owner(name="Jordan")

    # --- Pet 1: Biscuit the Golden Retriever ---
    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    biscuit.add_task(Task(
        description="Evening walk",
        task_type="walk",
        time="17:30",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        due_date=today,
        pet_name="Biscuit",
    ))
    biscuit.add_task(Task(
        description="Morning feeding",
        task_type="feeding",
        time="07:00",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        due_date=today,
        pet_name="Biscuit",
    ))
    biscuit.add_task(Task(
        description="Heartworm medication",
        task_type="medication",
        time="08:00",
        duration_minutes=5,
        priority="high",
        frequency="weekly",
        due_date=today,
        pet_name="Biscuit",
    ))
    biscuit.add_task(Task(
        description="Grooming session",
        task_type="grooming",
        time="14:00",
        duration_minutes=45,
        priority="low",
        frequency="once",
        due_date=today,
        pet_name="Biscuit",
    ))

    # --- Pet 2: Mochi the Siamese Cat ---
    mochi = Pet(name="Mochi", species="Cat", breed="Siamese")
    mochi.add_task(Task(
        description="Morning feeding",
        task_type="feeding",
        time="07:30",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        due_date=today,
        pet_name="Mochi",
    ))
    mochi.add_task(Task(
        description="Playtime / enrichment",
        task_type="enrichment",
        time="11:00",
        duration_minutes=20,
        priority="medium",
        frequency="daily",
        due_date=today,
        pet_name="Mochi",
    ))
    # Intentional conflict: same time as Biscuit's medication — for conflict demo
    mochi.add_task(Task(
        description="Vet check-up",
        task_type="appointment",
        time="08:00",
        duration_minutes=60,
        priority="high",
        frequency="once",
        due_date=today,
        pet_name="Mochi",
    ))

    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner


def format_tasks(tasks: list[Task]) -> str:
    """Render a list of tasks as a tabulate table."""
    rows = []
    for t in tasks:
        emoji = TASK_EMOJI.get(t.task_type, "📋")
        status = "✅" if t.completed else "⬜"
        rows.append([
            t.time,
            f"{emoji} {t.description}",
            t.pet_name,
            t.priority.upper(),
            f"{t.duration_minutes} min",
            t.frequency,
            status,
        ])
    return tabulate(
        rows,
        headers=["Time", "Task", "Pet", "Priority", "Duration", "Frequency", "Done"],
        tablefmt="rounded_outline",
    )


def main() -> None:
    owner = build_demo_data()
    scheduler = Scheduler(owner)

    print(f"\n{'='*60}")
    print(f"  🐾  PawPal+ Daily Planner  —  {today.strftime('%A, %B %d %Y')}")
    print(f"  Owner: {owner.name}")
    print(f"{'='*60}\n")

    # ── Today's Schedule (sorted by priority → time) ──
    print("📅  TODAY'S SCHEDULE  (sorted by priority → time)\n")
    todays = scheduler.get_todays_schedule()
    print(format_tasks(todays))

    # ── All tasks sorted by time only ──
    print("\n⏰  ALL TASKS  (sorted by time)\n")
    by_time = scheduler.sort_by_time()
    print(format_tasks(by_time))

    # ── Filter: pending tasks for Biscuit ──
    print("\n🔍  FILTER: Pending tasks for Biscuit\n")
    biscuit_pending = scheduler.filter_tasks(pet_name="Biscuit", completed=False)
    print(format_tasks(biscuit_pending))

    # ── Conflict detection ──
    print("\n🚨  CONFLICT DETECTION\n")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found.")

    # ── Recurring task demo ──
    print("\n🔄  RECURRING TASK DEMO\n")
    feeding = owner.pets[0].tasks[1]   # Biscuit's Morning feeding (daily)
    print(f"  Completing: '{feeding.description}' for {feeding.pet_name} (due {feeding.due_date})")
    next_task = feeding.mark_complete()
    if next_task:
        print(f"  ✅ Marked complete. Next occurrence auto-created: due {next_task.due_date}")
        owner.pets[0].add_task(next_task)

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
