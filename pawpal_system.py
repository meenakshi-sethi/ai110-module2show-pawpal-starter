"""
PawPal+ backend logic layer.
Contains all core classes: Task, Pet, Owner, and Scheduler.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """Represents a single pet care action."""

    description: str
    task_type: str          # "walk" | "feeding" | "medication" | "grooming" | "enrichment" | "appointment"
    time: str               # "HH:MM" format, e.g. "08:30"
    duration_minutes: int
    priority: str           # "low" | "medium" | "high"
    frequency: str          # "once" | "daily" | "weekly"
    due_date: date
    pet_name: str
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and return a new Task for the next occurrence if recurring."""
        self.completed = True
        if self.is_recurring():
            delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
            return Task(
                description=self.description,
                task_type=self.task_type,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + delta,
                pet_name=self.pet_name,
                completed=False,
            )
        return None

    def is_recurring(self) -> bool:
        """Return True if this task repeats (daily or weekly)."""
        return self.frequency in ("daily", "weekly")


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """Represents a pet owned by an Owner."""

    name: str
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a Task to this pet."""
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> list[Task]:
        """Return only incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.completed]


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

@dataclass
class Owner:
    """Represents the pet owner who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new Pet under this owner."""
        self.pets.append(pet)

    def list_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Scheduler:
    """Intelligence layer — sorts, filters, and analyzes tasks across all pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialise the Scheduler with an Owner instance."""
        self.owner = owner

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted chronologically by HH:MM time string."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def sort_by_priority(self) -> list[Task]:
        """Return all tasks sorted by priority (high first), then by time."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda t: (PRIORITY_ORDER.get(t.priority, 9), t.time),
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for any two tasks scheduled at the same time (same or different pets)."""
        warnings: list[str] = []
        seen: dict[str, Task] = {}   # time -> first task seen at that time
        for task in self.owner.get_all_tasks():
            key = task.time
            if key in seen:
                first = seen[key]
                warnings.append(
                    f"⚠️  Conflict at {task.time}: "
                    f'"{first.description}" ({first.pet_name}) '
                    f'and "{task.description}" ({task.pet_name})'
                )
            else:
                seen[key] = task
        return warnings

    def get_todays_schedule(self) -> list[Task]:
        """Return all tasks due today, sorted by priority then time."""
        today = date.today()
        todays = [t for t in self.owner.get_all_tasks() if t.due_date == today]
        return sorted(
            todays,
            key=lambda t: (PRIORITY_ORDER.get(t.priority, 9), t.time),
        )
