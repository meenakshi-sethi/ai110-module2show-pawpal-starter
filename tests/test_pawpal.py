"""
Initial automated tests for PawPal+ core classes.
Tests: Task completion, Pet task addition.
"""

from datetime import date
import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(description="Morning walk", time="08:00", priority="high",
              frequency="once", pet_name="Biscuit") -> Task:
    return Task(
        description=description,
        task_type="walk",
        time=time,
        duration_minutes=30,
        priority=priority,
        frequency=frequency,
        due_date=date.today(),
        pet_name=pet_name,
    )


def make_owner_with_two_pets() -> Owner:
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    mochi = Pet(name="Mochi", species="Cat", breed="Siamese")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner


# ---------------------------------------------------------------------------
# Test 1: Task Completion — mark_complete() changes status to True
# ---------------------------------------------------------------------------

def test_mark_complete_sets_completed_true():
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# ---------------------------------------------------------------------------
# Test 2: Task Addition — adding a task increases pet task count
# ---------------------------------------------------------------------------

def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1
    pet.add_task(make_task(description="Evening walk", time="17:30"))
    assert len(pet.tasks) == 2


# ---------------------------------------------------------------------------
# Test 3: Sorting — sort_by_time() returns chronological order
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    owner = make_owner_with_two_pets()
    owner.pets[0].add_task(make_task(time="17:30", pet_name="Biscuit"))
    owner.pets[0].add_task(make_task(time="07:00", description="Feeding", pet_name="Biscuit"))
    owner.pets[1].add_task(make_task(time="11:00", description="Playtime", pet_name="Mochi"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times), f"Expected sorted times, got {times}"


# ---------------------------------------------------------------------------
# Test 4: Recurring tasks — daily task creates next-day task after mark_complete
# ---------------------------------------------------------------------------

def test_daily_task_creates_next_occurrence():
    today = date.today()
    task = make_task(frequency="daily")
    task.due_date = today
    next_task = task.mark_complete()
    assert next_task is not None, "Expected a new task for the next day"
    assert next_task.due_date == today + __import__("datetime").timedelta(days=1)
    assert next_task.completed is False


# ---------------------------------------------------------------------------
# Test 5: Conflict detection — flags two tasks at the same time
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_same_time():
    owner = make_owner_with_two_pets()
    owner.pets[0].add_task(make_task(time="08:00", description="Medication", pet_name="Biscuit"))
    owner.pets[1].add_task(make_task(time="08:00", description="Vet check-up", pet_name="Mochi"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


# ---------------------------------------------------------------------------
# Test 6: filter_tasks — returns only tasks for the specified pet
# ---------------------------------------------------------------------------

def test_filter_tasks_by_pet_name():
    owner = make_owner_with_two_pets()
    owner.pets[0].add_task(make_task(description="Walk", pet_name="Biscuit"))
    owner.pets[1].add_task(make_task(description="Playtime", pet_name="Mochi"))

    scheduler = Scheduler(owner)
    biscuit_tasks = scheduler.filter_tasks(pet_name="Biscuit")
    assert all(t.pet_name == "Biscuit" for t in biscuit_tasks)
    assert len(biscuit_tasks) == 1
