
import streamlit as st
import sqlite3

st.set_page_config(
    page_title="My Wellness | The Caregiver Circle",
    page_icon="🌿"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "discussion_board.db")

    
def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wellness_checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mood TEXT,
        stress_level INTEGER,
        physical_wellness TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diary_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        entry TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS physical_health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sleep_hours REAL,
        activity_minutes INTEGER,
        energy_level INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()

# PRIVATE DIARY FUNCTIONS

def save_diary_entry(user_id, title, entry):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO diary_entries (user_id, title, entry)
        VALUES (?, ?, ?)
    """, (user_id, title, entry))
    conn.commit()
    conn.close()

def get_diary_entries(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, entry, created_at
        FROM diary_entries
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    entries = cursor.fetchall()
    conn.close()
    return entries

def update_diary_entry(entry_id, user_id, title, entry):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE diary_entries
        SET title = ?, entry = ?
        WHERE id = ? AND user_id = ?
    """, (title, entry, entry_id, user_id))
    conn.commit()
    conn.close()

def delete_diary_entry(entry_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM diary_entries
        WHERE id = ? AND user_id = ?
    """, (entry_id, user_id))
    conn.commit()
    conn.close()

# WELLNESS CHECK-IN FUNCTIONS

def save_checkin(user_id, mood, stress, physical_wellness, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO wellness_checkins
        (user_id, mood, stress_level, physical_wellness, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, mood, stress, physical_wellness, notes))
    conn.commit()
    conn.close()

def get_checkins(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mood, stress_level, physical_wellness, notes, created_at
        FROM wellness_checkins
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    checkins = cursor.fetchall()
    conn.close()
    return checkins

# PHYSICAL HEALTH FUNCTIONS

def save_physical_health(user_id, sleep, activity, energy, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO physical_health
        (user_id, sleep_hours, activity_minutes, energy_level, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, sleep, activity, energy, notes))
    conn.commit()
    conn.close()

def get_physical_health(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sleep_hours, activity_minutes, energy_level, notes, created_at
        FROM physical_health
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

# PAGE DISPLAY

st.title("🌿 My Wellness")

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to access your private wellness space.")
    st.page_link("pages/1_Account.py", label="Go to Account")

else:
    user_id = st.session_state.user_id

    st.write(f"Welcome, {st.session_state.username}!")
    st.caption("Your personal wellness space is private.")

    # WELLNESS CHECK-IN

    st.divider()
    st.header("💚 Wellness Check-In")
    st.write("Take a moment to check in with yourself.")

    with st.form("wellness_checkin_form"):
        mood = st.selectbox(
            "How are you feeling today?",
            ["Very good", "Good", "Okay", "Not great", "Struggling"]
        )

        stress = st.slider(
            "How would you rate your stress level?",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Very low stress | 10 = Extremely high stress"
        )

        physical_wellness = st.selectbox(
            "How are you feeling physically?",
            ["Great", "Good", "Okay", "Tired", "Not feeling well"]
        )

        notes = st.text_area(
            "Anything else you'd like to share? (Optional)",
            height=100
        )

        submitted = st.form_submit_button("Save Check-In")

        if submitted:
            save_checkin(
                user_id, mood, stress, physical_wellness, notes.strip()
            )
            st.success("Your wellness check-in has been saved!")
            st.rerun()

    st.subheader("Previous Check-Ins")
    checkins = get_checkins(user_id)

    if not checkins:
        st.info("Your check-in history will appear here.")

    for checkin in checkins:
        mood, stress, physical, notes, created_at = checkin

        with st.expander(f"Check-In — {created_at}"):
            st.write(f"**Mood:** {mood}")
            st.write(f"**Stress level:** {stress}/10")
            st.write(f"**Physical wellness:** {physical}")
            if notes:
                st.write(f"**Notes:** {notes}")

    # PHYSICAL HEALTH TRACKER

    st.divider()
    st.header("🏃 Physical Health Tracker")
    st.write("Keep track of your physical wellness over time.")

    with st.form("physical_health_form"):
        sleep = st.number_input(
            "How many hours did you sleep?",
            min_value=0.0,
            max_value=24.0,
            value=7.0,
            step=0.5
        )

        activity = st.number_input(
            "Physical activity (minutes)",
            min_value=0,
            max_value=1440,
            value=0,
            step=5
        )

        energy = st.slider(
            "How would you rate your energy level?",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Very low energy | 10 = Very high energy"
        )

        health_notes = st.text_area(
            "Additional physical health notes (Optional)",
            height=100
        )

        health_submitted = st.form_submit_button("Save Physical Health Record")

        if health_submitted:
            save_physical_health(
                user_id,
                sleep,
                activity,
                energy,
                health_notes.strip()
            )
            st.success("Your physical health record has been saved!")
            st.rerun()

    st.subheader("Physical Health History")
    health_records = get_physical_health(user_id)

    if not health_records:
        st.info("Your physical health history will appear here.")

    for record in health_records:
        sleep, activity, energy, notes, created_at = record

        with st.expander(f"Physical Health — {created_at}"):
            st.write(f"**Sleep:** {sleep} hours")
            st.write(f"**Activity:** {activity} minutes")
            st.write(f"**Energy:** {energy}/10")
            if notes:
                st.write(f"**Notes:** {notes}")

    # PRIVATE DIARY

    st.divider()
    st.header("📖 My Private Diary")
    st.write("A private space to reflect, write, and revisit your experiences.")

    with st.form("new_diary_entry"):
        title = st.text_input("Entry title")
        entry = st.text_area("What's on your mind?", height=200)

        submitted = st.form_submit_button("Save Diary Entry")

        if submitted:
            if entry.strip():
                save_diary_entry(user_id, title.strip(), entry.strip())
                st.success("Your diary entry has been saved.")
                st.rerun()
            else:
                st.warning("Please write something before saving.")

    st.subheader("Previous Diary Entries")
    entries = get_diary_entries(user_id)

    if not entries:
        st.info("Your diary is empty. Your first entry can start here.")

    for diary in entries:
        entry_id, entry_title, entry_text, created_at = diary

        with st.expander(
            f"{entry_title or 'Untitled Entry'} — {created_at}"
        ):
            st.write(entry_text)
            st.divider()
            st.write("**Edit this entry**")

            with st.form(f"edit_form_{entry_id}"):
                edited_title = st.text_input(
                    "Title",
                    value=entry_title or "",
                    key=f"title_{entry_id}"
                )

                edited_text = st.text_area(
                    "Entry",
                    value=entry_text,
                    height=150,
                    key=f"text_{entry_id}"
                )

                update_button = st.form_submit_button("Save Changes")

                if update_button:
                    if edited_text.strip():
                        update_diary_entry(
                            entry_id, user_id,
                            edited_title.strip(), edited_text.strip()
                        )
                        st.success("Entry updated.")
                        st.rerun()
                    else:
                        st.warning("An entry cannot be empty.")

            if st.button("Delete Entry", key=f"delete_{entry_id}"):
                delete_diary_entry(entry_id, user_id)
                st.success("Entry deleted.")
                st.rerun()
