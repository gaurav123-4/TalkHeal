import streamlit as st
import random

st.set_page_config(page_title="Wellness Resource Hub", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🌿 Wellness Hub Menu")
page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Wellness Hub",
        "🌞 Daily Affirmation",
        "✅ Quick Self-Check",
        "📅 Daily Planner",
        "📊 Mood Tracker",
        "📚 Wellness Resources"
    ]
)

# --- Wellness categories ---
categories = {
    "🧘 Mind": [
        "Practice meditation for 5 minutes daily",
        "Try journaling your thoughts",
        "Use apps like Headspace or Calm"
    ],
    "💪 Body": [
        "Do at least 20 minutes of exercise",
        "Simple stretches help reduce stiffness",
        "Stay hydrated while being active"
    ],
    "🥗 Nutrition": [
        "Eat balanced meals with protein, carbs, and veggies",
        "Drink at least 7–8 glasses of water daily",
        "Avoid too much junk food"
    ],
    "😴 Sleep": [
        "Aim for 7–8 hours of sleep daily",
        "Avoid screen time 30 mins before bed",
        "Keep a consistent sleep schedule"
    ],
    "🌸 Stress Relief": [
        "Try deep breathing (inhale 4s, hold 4s, exhale 4s)",
        "Listen to calming music",
        "Take short breaks while working"
    ]
}

# --- Motivational Affirmations ---
affirmations = [
    "✨ You are stronger than you think.",
    "🌞 Small steps every day lead to big changes.",
    "🌸 Prioritize your well-being — you deserve it.",
    "💡 Every day is a new beginning — take a deep breath and start fresh."
]

# --- Page 1: Wellness Hub ---
if page == "🏠 Wellness Hub":
    st.title("🌿 Wellness Resource Hub")
    st.write("Click on a category to explore simple wellness tips and resources.")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🧘 Mind"):
            for tip in categories["🧘 Mind"]:
                st.write("- " + tip)

        with st.expander("🥗 Nutrition"):
            for tip in categories["🥗 Nutrition"]:
                st.write("- " + tip)

        with st.expander("🌸 Stress Relief"):
            for tip in categories["🌸 Stress Relief"]:
                st.write("- " + tip)

    with col2:
        with st.expander("💪 Body"):
            for tip in categories["💪 Body"]:
                st.write("- " + tip)

        with st.expander("😴 Sleep"):
            for tip in categories["😴 Sleep"]:
                st.write("- " + tip)

    st.markdown("---")
    st.success(random.choice(affirmations))

# --- Page 2: Daily Affirmation ---
elif page == "🌞 Daily Affirmation":
    st.title("🌞 Daily Positive Affirmation")
    st.write("Here’s a little boost for your day:")
    st.info(random.choice(affirmations))

# --- Page 3: Quick Self-Check ---
elif page == "✅ Quick Self-Check":
    st.title("✅ Quick Wellness Self-Check")
    st.write("Answer a few quick questions to get simple wellness advice.")

    stress = st.slider("How stressed are you feeling today?", 0, 10, 5)
    sleep = st.slider("How many hours did you sleep last night?", 0, 12, 7)
    mood = st.slider("How is your overall mood today?", 0, 10, 6)

    if st.button("Get My Wellness Tip"):
        if stress > 7:
            st.warning("😟 You seem stressed. Try deep breathing or take a short walk.")
        elif sleep < 6:
            st.warning("😴 You need more rest. Try to get at least 7–8 hours of sleep.")
        elif mood < 5:
            st.info("💙 It’s okay to have tough days. Try journaling or talking to a friend.")
        else:
            st.success("🌟 You're doing well! Keep maintaining your healthy habits.")

# --- Page 4: Daily Planner ---
elif page == "📅 Daily Planner":
    st.title("📅 Daily Planner")
    st.write("Plan your day with simple goals. Mark tasks as complete or remove them.")

    # Initialize or migrate session state for tasks
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    # Simple migration from old format (list of strings) to new format (list of dicts)
    elif st.session_state.tasks and isinstance(st.session_state.tasks[0], str):
        st.session_state.tasks = [{"task": t, "completed": False} for t in st.session_state.tasks]

    # --- Task Input Form ---
    with st.form("new_task_form", clear_on_submit=True):
        new_task = st.text_input("Add a new task:")
        submitted = st.form_submit_button("➕ Add Task")
        if submitted and new_task:
            st.session_state.tasks.append({"task": new_task, "completed": False})
            st.rerun()

    st.subheader("✅ Your Tasks")

    # --- Task Deletion and Completion Logic ---
    indices_to_delete = []
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            # The checkbox state directly modifies the session state dictionary value
            st.session_state.tasks[i]["completed"] = st.checkbox(
                task["task"],
                value=task["completed"],
                key=f"task_{i}"
            )
        with col2:
            if st.button("🗑️", key=f"delete_{i}", help=f"Delete task: {task['task']}"):
                indices_to_delete.append(i)

    # Perform deletions after iterating through the list
    if indices_to_delete:
        for i in sorted(indices_to_delete, reverse=True):
            del st.session_state.tasks[i]
        st.rerun()

    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above!")

# --- Page 5: Mood Tracker ---
elif page == "📊 Mood Tracker":
    st.title("📊 Mood Tracker")
    st.write("Log your daily mood and add a note to track progress and identify patterns.")

    # Initialize or migrate session state for moods
    if "moods" not in st.session_state:
        st.session_state.moods = []
    # Simple migration from old format (list of strings) to new format (list of dicts)
    elif st.session_state.moods and isinstance(st.session_state.moods[0], str):
        st.session_state.moods = [{"mood": m, "note": ""} for m in st.session_state.moods]

    mood = st.radio("How do you feel today?", ["😊 Happy", "😐 Okay", "😟 Stressed", "😢 Sad"])
    note = st.text_input("Add a note to remember the context (optional):")

    if st.button("Log Mood"):
        st.session_state.moods.append({"mood": mood, "note": note})
        st.success(f"Logged mood: {mood}")
        st.rerun()

    st.subheader("📅 Mood History")
    if st.session_state.moods:
        # Display moods in reverse chronological order
        for entry in reversed(st.session_state.moods):
            if entry["note"]:
                st.markdown(f"- **{entry['mood']}**: *{entry['note']}*")
            else:
                st.markdown(f"- **{entry['mood']}**")
    else:
        st.info("No moods logged yet.")

# --- Page 6: Wellness Resources ---
elif page == "📚 Wellness Resources":
    st.title("📚 Wellness Resources")
    st.write("A curated list of trusted resources to support your well-being journey.")

    st.subheader("🧘 Meditation & Mindfulness")
    st.markdown("""
        - **[Headspace](https://www.headspace.com/)**: Guided meditations, animations, articles, and videos.
        - **[Calm](https://www.calm.com/)**: A popular app for sleep, meditation, and relaxation.
        - **[Tara Brach](https://www.tarabrach.com/guided-meditations/)**: Free guided meditations and talks on mindfulness.
        - **[Mindful.org](https://www.mindful.org/)**: Articles, guides, and resources on practicing mindfulness.
    """)

    st.subheader("💪 Fitness & Movement")
    st.markdown("""
        - **[Nike Training Club](https://www.nike.com/ntc-app)**: A wide range of free workouts and personalized training plans.
        - **[Yoga with Adriene](https://www.youtube.com/user/yogawithadriene)**: High-quality free yoga and mindfulness videos for all levels.
        - **[Fitness Blender](https://www.fitnessblender.com/)**: A huge variety of free, full-length workout videos.
    """)

    st.subheader("🥗 Nutrition")
    st.markdown("""
        - **[Nutrition.gov](https://www.nutrition.gov/)**: Trustworthy information to make healthy eating choices.
        - **[MyFitnessPal](https://www.myfitnesspal.com/)**: A popular tool for tracking food intake and calories.
    """)

    st.subheader("😴 Sleep Health")
    st.markdown("""
        - **[Sleep Foundation](https://www.sleepfoundation.org/)**: Evidence-based information and resources on sleep health.
        - **[The Sleep Council](https://sleepcouncil.org.uk/)**: Practical advice on how to get a better night's sleep.
    """)

    st.subheader("🎙️ Wellness Podcasts")
    st.markdown("""
        - **[The Happiness Lab](https://www.pushkin.fm/podcasts/the-happiness-lab-with-dr-laurie-santros)**: Dr. Laurie Santos explores the science of happiness.
        - **[Feel Better, Live More](https://drchatterjee.com/blog/)**: Hosted by Dr. Rangan Chatterjee, offering practical health advice.
        - **[Ten Percent Happier](https://www.tenpercent.com/podcast)**: Interviews with meditation experts and scientists.
    """)

    st.subheader("📖 Recommended Books")
    st.markdown("""
        - **[Atomic Habits by James Clear](https://jamesclear.com/atomic-habits)**: A guide to building good habits and breaking bad ones.
        - **[The Power of Now by Eckhart Tolle](https://eckharttolle.com/power-of-now-a-guide-to-spiritual-enlightenment/)**: A book on mindfulness and living in the present moment.
        - **[10% Happier by Dan Harris](https.www.goodreads.com/book/show/18505796-10-happier)**: A true story about a news anchor who discovers meditation.
    """)

    st.subheader("❤️ Crisis Support")
    st.warning("If you are in immediate distress, please reach out. You are not alone.")
    st.markdown("""
        - **[Crisis Text Line](https://www.crisistextline.org/)**: Text HOME to 741741 from anywhere in the US, anytime, about any type of crisis.
        - **[The National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/)**: Call 988 for free and confidential support.
    """)