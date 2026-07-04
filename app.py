"""
PawPal+ Streamlit UI — wired to pawpal_system.py backend.
Uses st.session_state to persist Owner across reruns.
"""

from datetime import date
import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care planner — powered by your Python scheduling engine.")

TASK_EMOJI = {
    "walk": "🦮", "feeding": "🍖", "medication": "💊",
    "grooming": "✂️", "enrichment": "🧸", "appointment": "🏥",
}

# ---------------------------------------------------------------------------
# Session state — persist Owner so it survives every Streamlit rerun
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None

# ---------------------------------------------------------------------------
# Sidebar — Owner setup
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("👤 Owner Setup")
    owner_name_input = st.text_input("Your name", value="Jordan")
    if st.button("Set / Update Owner"):
        if st.session_state.owner is None:
            st.session_state.owner = Owner(name=owner_name_input)
        else:
            st.session_state.owner.name = owner_name_input
        st.success(f"Owner set to **{owner_name_input}**")

    st.divider()

    # Add a pet
    st.header("🐾 Add a Pet")
    with st.form("add_pet_form"):
        pet_name_input   = st.text_input("Pet name", value="Biscuit")
        species_input    = st.selectbox("Species", ["Dog", "Cat", "Other"])
        breed_input      = st.text_input("Breed", value="Golden Retriever")
        add_pet_btn      = st.form_submit_button("Add Pet")

    if add_pet_btn:
        if st.session_state.owner is None:
            st.warning("Set an owner name first.")
        else:
            existing_names = [p.name.lower() for p in st.session_state.owner.pets]
            if pet_name_input.lower() in existing_names:
                st.warning(f"**{pet_name_input}** is already added.")
            else:
                st.session_state.owner.add_pet(
                    Pet(name=pet_name_input, species=species_input, breed=breed_input)
                )
                st.success(f"Added **{pet_name_input}** the {species_input}!")

# ---------------------------------------------------------------------------
# Guard — require owner before showing the rest of the UI
# ---------------------------------------------------------------------------
if st.session_state.owner is None:
    st.info("👈 Enter your name in the sidebar and click **Set / Update Owner** to get started.")
    st.stop()

owner: Owner = st.session_state.owner
st.subheader(f"Welcome, {owner.name}!")

# ---------------------------------------------------------------------------
# Add a Task
# ---------------------------------------------------------------------------
st.header("➕ Schedule a Task")

pets = owner.list_pets()
if not pets:
    st.warning("Add at least one pet in the sidebar before scheduling tasks.")
else:
    pet_names = [p.name for p in pets]
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_pet  = st.selectbox("Pet", pet_names)
            task_desc     = st.text_input("Description", value="Morning walk")
            task_type     = st.selectbox("Type", list(TASK_EMOJI.keys()))
            task_time     = st.text_input("Time (HH:MM)", value="08:00")
        with col2:
            duration_min  = st.number_input("Duration (min)", min_value=1, max_value=480, value=30)
            priority      = st.selectbox("Priority", ["high", "medium", "low"])
            frequency     = st.selectbox("Frequency", ["once", "daily", "weekly"])
            due_date      = st.date_input("Due date", value=date.today())

        add_task_btn = st.form_submit_button("Add Task")

    if add_task_btn:
        target_pet = next(p for p in pets if p.name == selected_pet)
        new_task = Task(
            description=task_desc,
            task_type=task_type,
            time=task_time,
            duration_minutes=int(duration_min),
            priority=priority,
            frequency=frequency,
            due_date=due_date,
            pet_name=selected_pet,
        )
        target_pet.add_task(new_task)
        st.success(f"Task **{task_desc}** added for **{selected_pet}**!")

st.divider()

# ---------------------------------------------------------------------------
# Generate Schedule
# ---------------------------------------------------------------------------
st.header("📅 Generate Schedule")

if st.button("Generate schedule", type="primary"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.info("No tasks yet. Add some tasks above.")
    else:
        scheduler = Scheduler(owner)

        # Conflict warnings
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("✅ No scheduling conflicts detected.")

        # Today's schedule sorted by priority → time
        st.subheader(f"🗓️ Today's Schedule — {date.today().strftime('%A, %B %d %Y')}")
        todays = scheduler.get_todays_schedule()
        if todays:
            rows = []
            for t in todays:
                emoji = TASK_EMOJI.get(t.task_type, "📋")
                rows.append({
                    "Time": t.time,
                    "Task": f"{emoji} {t.description}",
                    "Pet": t.pet_name,
                    "Priority": t.priority.upper(),
                    "Duration": f"{t.duration_minutes} min",
                    "Frequency": t.frequency,
                    "Done": "✅" if t.completed else "⬜",
                })
            st.table(rows)
        else:
            st.info("No tasks due today.")

        # Full schedule sorted by time
        st.subheader("⏰ All Tasks — sorted by time")
        by_time = scheduler.sort_by_time()
        rows_all = []
        for t in by_time:
            emoji = TASK_EMOJI.get(t.task_type, "📋")
            rows_all.append({
                "Time": t.time,
                "Task": f"{emoji} {t.description}",
                "Pet": t.pet_name,
                "Priority": t.priority.upper(),
                "Due": str(t.due_date),
                "Done": "✅" if t.completed else "⬜",
            })
        st.table(rows_all)

st.divider()

# ---------------------------------------------------------------------------
# Current Pets summary
# ---------------------------------------------------------------------------
st.header("🐾 Your Pets")
if not pets:
    st.info("No pets added yet.")
else:
    for pet in pets:
        pending = pet.get_pending_tasks()
        with st.expander(f"{pet.name} — {pet.breed} ({pet.species})  |  {len(pending)} pending task(s)"):
            if pet.tasks:
                rows = [{"Time": t.time, "Task": t.description, "Priority": t.priority,
                         "Done": "✅" if t.completed else "⬜"} for t in pet.tasks]
                st.table(rows)
            else:
                st.caption("No tasks yet.")
