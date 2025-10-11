import streamlit as st
import base64
import random
import pandas as pd
from datetime import datetime
import uuid

def get_base64_of_bin_file(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background_for_theme(selected_palette="pink"):
    from core.theme import get_current_theme

    # --- Get current theme info ---
    current_theme = st.session_state.get("current_theme", None)
    if not current_theme:
        current_theme = get_current_theme()
    
    is_dark = current_theme["name"] == "Dark"

    # --- Map light themes to background images ---
    palette_color = {
        "light": "static_files/pink.png",
        "calm blue": "static_files/blue.png",
        "mint": "static_files/mint.png",
        "lavender": "static_files/lavender.png",
        "pink": "static_files/pink.png"
    }

    # --- Select background based on theme ---
    if is_dark:
        background_image_path = "static_files/dark.png"
    else:
        background_image_path = palette_color.get(selected_palette.lower(), "static_files/pink.png")

    encoded_string = get_base64_of_bin_file(background_image_path)

    st.markdown(
        f"""
        <style>
        /* Entire app background */
        html, body, [data-testid="stApp"] {{
            background-color: {'rgba(0, 0, 0, 0.5)' if is_dark else 'rgba(255, 255, 255, 0.3)'} !important;
            transition: background-color 0.4s ease;
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Main content transparency */
        .block-container {{
            background-color: rgba(255, 255, 255, 0);
        }}

        /* Sidebar: brighter translucent background */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.6);  /* Brighter and translucent */
            color: {'black' if is_dark else 'rgba(49, 51, 63, 0.8)'} ;  /* Adjusted for light background */
        }}

        /* Header bar: fully transparent */
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0);
        }}

        h1 {{
            color: rgb(214, 51, 108) !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}

        h2, h3, h4, h5, h6,
        p, span, strong, div, label {{
            color: {'#f0f0f0' if is_dark else 'rgba(49, 51, 63, 0.8)'} !important;
            transition: color 0.3s ease;
        }}

        /* Hide left/right arrow at sidebar bottom */
        button[title="Close sidebar"],
        button[title="Open sidebar"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)


st.set_page_config(page_title="Wellness Resource Hub", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🌿 Wellness Hub Menu")
page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Wellness Hub",
        "✅ Quick Self-Check",
        "📅 Daily Planner",
        "🎯 Wellness Goals",
        "📊 Mood Tracker",
        "📓 Journaling Prompts",
        "📚 Wellness Resources",
        "🤝 Community Tips",
        "🎨 Creative Corner"
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
    "💡 Every day is a new beginning — take a deep breath and start fresh.",
    "🌱 Your growth is a journey, not a race.",
    "💖 Be kind to your mind. You're doing your best.",
    "🌟 You are capable of amazing things.",
    "🧘‍♀️ Inhale peace, exhale stress.",
    "🌈 Healing is not linear — and that’s okay.",
    "🔥 Challenges help you grow stronger and wiser.",
    "🌻 You radiate positivity and resilience.",
    "☀️ Even the darkest night ends with sunrise.",
    "💎 You are enough, just as you are.",
    "🌊 Let go of what you can’t control — flow forward.",
    "🌿 Rest is productive — recharge without guilt.",
    "🎯 Focus on progress, not perfection.",
    "❤️ Your feelings are valid, and so are you.",
    "🦋 Transformation takes time — trust the process.",
    "✨ You bring light to the spaces you enter.",
    "🌼 Celebrate small victories — they matter."
]

# --- Wellness Task Suggestions ---
wellness_tasks = [
    "Drink a full glass of water",
    "Stretch for 5 minutes",
    "Take 10 deep, slow breaths",
    "Write down one thing you're grateful for",
    "Go for a 10-minute walk outside",
    "Tidy up your workspace for 5 minutes",
    "Listen to one favorite calming song",
    "Step away from screens for 5 minutes",
    "Jot down 3 things you accomplished today, big or small.",
    "Send a thank you message to a friend or family member.",
    "Step outside for 2 minutes and take a breath of fresh air.",
    "Put on a favorite upbeat song and have a mini dance party.",
    "Look out a window and name 5 different things you can see."
]

# --- Community Stories Data ---
community_stories = [
    {
        "author": "A grateful user",
        "category": "Gratitude",
        "story": "I started writing down three things I'm grateful for every night before bed. It felt silly at first, but after a week, I noticed I was feeling more positive throughout the day. It's the small things that make a big difference."
    },
    {
        "author": "Someone who found calm",
        "category": "Stress Relief",
        "story": "The 4-7-8 breathing technique has been a lifesaver for my anxiety. Whenever I feel overwhelmed, I take a few minutes to do it, and it's like hitting a reset button. Inhale for 4, hold for 7, exhale for 8. Try it!"
    },
    {
        "author": "A student",
        "category": "Productivity",
        "story": "I used to struggle with procrastination. Now, I use the Pomodoro Technique (25 minutes of focused work, 5-minute break). Knowing I have a break coming up makes it so much easier to start. The 'Focus Session' feature here is great for that."
    },
    {
        "author": "A recent graduate",
        "category": "Self-Kindness",
        "story": "My therapist told me to treat myself like I would treat a good friend. It changed my perspective. I'm much less critical of myself now and celebrate small wins instead of only focusing on my flaws. Be kind to yourself!"
    }
]

# --- Page 1: Wellness Hub ---
if page == "🏠 Wellness Hub":
    st.title("🌿 Wellness Hub Dashboard")

    # Integrated Daily Affirmation
    st.info(f"✨ **Today's Affirmation:** {random.choice(affirmations)}")

    st.markdown("---    ")
    st.write("Explore these wellness categories to find tips and resources for your well-being.")

    # Card-based layout for categories
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🧘 Mind")
            for tip in categories["🧘 Mind"]:
                st.write(f"- {tip}")
            st.write(" ") # Add some padding

        with st.container(border=True):
            st.subheader("🥗 Nutrition")
            for tip in categories["🥗 Nutrition"]:
                st.write(f"- {tip}")
            st.write(" ")

        with st.container(border=True):
            st.subheader("🌸 Stress Relief")
            for tip in categories["🌸 Stress Relief"]:
                st.write(f"- {tip}")
            st.write(" ")

    with col2:
        with st.container(border=True):
            st.subheader("💪 Body")
            for tip in categories["💪 Body"]:
                st.write(f"- {tip}")
            st.write(" ")

        with st.container(border=True):
            st.subheader("😴 Sleep")
            for tip in categories["😴 Sleep"]:
                st.write(f"- {tip}")
            st.write(" ")

# --- Page 3: Quick Self-Check ---
elif page == "✅ Quick Self-Check":
    st.title("✅ Quick Wellness Self-Check")
    st.write("Track your well-being over time. Answer a few quick questions to get simple wellness advice and see your progress.")

    # Initialize session state for self-check history
    if "self_check_history" not in st.session_state:
        st.session_state.self_check_history = []

    stress = st.slider("How stressed are you feeling today?", 0, 10, 5)
    sleep = st.slider("How many hours did you sleep last night?", 0, 12, 7)
    mood = st.slider("How is your overall mood today?", 0, 10, 6)

    if st.button("Log and Get My Wellness Tip"):
        # --- Tip Logic ---
        if stress > 7:
            st.warning("😟 You seem stressed. Try deep breathing or take a short walk.")
        elif sleep < 6:
            st.warning("😴 You need more rest. Try to get at least 7–8 hours of sleep.")
        elif mood < 5:
            st.info("💙 It’s okay to have tough days. Try journaling or talking to a friend.")
        else:
            st.success("🌟 You're doing well! Keep maintaining your healthy habits.")
        
        # --- Store Data ---
        st.session_state.self_check_history.append({
            "Date": datetime.now(),
            "Stress": stress,
            "Sleep (hours)": sleep,
            "Mood": mood
        })
        st.rerun()

    # --- History and Visualization ---
    if st.session_state.self_check_history:
        st.markdown("---")
        st.subheader("📈 Your Self-Check History")
        
        history_df = pd.DataFrame(st.session_state.self_check_history)
        history_df = history_df.set_index("Date")
        
        st.line_chart(history_df)
        
        with st.expander("View Raw Data"):
            st.dataframe(history_df)

# --- Page 4: Daily Planner ---
elif page == "📅 Daily Planner":
    st.title("📅 Daily Planner")
    st.write("Plan your day with simple goals. Mark tasks as complete or remove them.")

    # Initialize or migrate session state for tasks
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
        st.session_state.editing_task_id = None
        st.session_state.edited_task_text = ""
    # Simple migration from old format (list of strings) to new format (list of dicts)
    elif st.session_state.tasks and isinstance(st.session_state.tasks[0], str):
        st.session_state.tasks = [{"task": t, "completed": False, "key": str(uuid.uuid4())} for t in st.session_state.tasks]
        st.session_state.editing_task_id = None
        st.session_state.edited_task_text = ""

    # Ensure all existing tasks have a 'key' if they somehow don't (e.g., after a hot reload)
    for task in st.session_state.tasks:
        if "key" not in task:
            task["key"] = str(uuid.uuid4())

    # --- Task Input Form ---
    with st.form("new_task_form", clear_on_submit=True):
        new_task = st.text_input("Add a new task:")
        submitted = st.form_submit_button("➕ Add Task")
        if submitted and new_task:
            st.session_state.tasks.append({"task": new_task, "completed": False, "key": str(uuid.uuid4())})
            st.rerun()

    # --- Wellness Task Suggestion Button ---
    if st.button("💡 Suggest a Wellness Task"):
        suggested_task = random.choice(wellness_tasks)
        st.session_state.tasks.append({"task": suggested_task, "completed": False})
        st.rerun()

    st.subheader("✅ Your Tasks")

    # --- Display Progress Bar ---
    if st.session_state.tasks:
        completed_count = sum(1 for t in st.session_state.tasks if t["completed"])
        total_count = len(st.session_state.tasks)
        progress_ratio = completed_count / total_count if total_count > 0 else 0
        st.progress(progress_ratio, text=f"{completed_count}/{total_count} Tasks Completed")

        # --- Celebrate Completion ---
        if completed_count > 0 and completed_count == total_count:
            st.balloons()
            st.success("🎉 All tasks completed! Great job!")

    # --- Task Display, Edit, and Deletion Logic ---
    indices_to_delete = []
    for i, task in enumerate(st.session_state.tasks):
        if st.session_state.editing_task_id == task["key"]:
            # Editing mode
            col_edit_input, col_edit_save, col_edit_cancel = st.columns([0.7, 0.15, 0.15])
            with col_edit_input:
                st.session_state.edited_task_text = st.text_input(
                    "Edit Task:",
                    value=st.session_state.edited_task_text,
                    key=f"edit_input_{task['key']}",
                    label_visibility="collapsed"
                )
            with col_edit_save:
                if st.button("💾 Save", key=f"save_edit_{task['key']}"):
                    # Find the task by key and update its text
                    for t in st.session_state.tasks:
                        if t["key"] == task["key"]:
                            t["task"] = st.session_state.edited_task_text
                            break
                    st.session_state.editing_task_id = None
                    st.session_state.edited_task_text = ""
                    st.rerun()
            with col_edit_cancel:
                if st.button("❌ Cancel", key=f"cancel_edit_{task['key']}"):
                    st.session_state.editing_task_id = None
                    st.session_state.edited_task_text = ""
                    st.rerun()
        else:
            # Normal display mode
            col_checkbox, col_edit_btn, col_delete_btn = st.columns([0.7, 0.15, 0.15])
            with col_checkbox:
                label = f"~~{task['task']}~~" if task["completed"] else task["task"]
                st.session_state.tasks[i]["completed"] = st.checkbox(
                    label,
                    value=task["completed"],
                    key=f"task_{task['key']}" # Use task key for unique widget key
                )
            with col_edit_btn:
                if st.button("✏️ Edit", key=f"edit_btn_{task['key']}"):
                    st.session_state.editing_task_id = task["key"]
                    st.session_state.edited_task_text = task["task"]
                    st.rerun()
            with col_delete_btn:
                if st.button("🗑️", key=f"delete_btn_{task['key']}", help=f"Delete task: {task['task']}"):
                    indices_to_delete.append(i)

    # Perform deletions after iterating through the list
    if indices_to_delete:
        # Delete tasks by key to avoid issues with re-indexing
        st.session_state.tasks = [t for i, t in enumerate(st.session_state.tasks) if i not in indices_to_delete]
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

        st.subheader("📊 Mood Analysis")
        st.write("Here is a summary of your logged moods:")
        df = pd.DataFrame(st.session_state.moods)
        mood_counts = df['mood'].value_counts()
        st.bar_chart(mood_counts)

    else:
        st.info("No moods logged yet.")

# --- Page 6: Journaling Prompts ---
elif page == "📓 Journaling Prompts":
    st.title("📓 Journaling Prompts")
    st.write("Use these prompts to inspire your self-reflection. You don't have to answer them all; just pick one that resonates with you today.")

    st.subheader("🌟 For Gratitude and Positivity")
    st.markdown('''
        - What is one small thing that brought you joy today?
        - Who is someone you're grateful for, and why?
        - Write about a compliment you received that made you feel good.
        - What is a personal strength you are proud of?
    ''')

    st.subheader("🤔 For Self-Reflection and Growth")
    st.markdown('''
        - What is a challenge you recently overcame, and what did you learn?
        - If you could give your past self one piece of advice, what would it be?
        - Describe a time you felt truly at peace. What were you doing?
        - What is one habit you'd like to develop, and what is the first step?
    ''')

    st.subheader("🔮 For Future Goals and Aspirations")
    st.markdown('''
        - Describe your ideal day, from morning to night.
        - What is a skill you want to learn in the next year?
        - If there were no obstacles, what is one dream you would pursue?
        - Write a letter to your future self, five years from now.
    ''')

# --- Page 7: Wellness Resources ---
elif page == "📚 Wellness Resources":
    st.title("📚 Wellness Resources")
    st.write("A curated list of trusted resources to support your well-being journey.")

    # --- Initialize Session State for Ratings ---
    if 'user_ratings' not in st.session_state:
        st.session_state.user_ratings = {}

    # --- Data for Wellness Resources ---
    wellness_resources_data = {
        "🧘 Meditation & Mindfulness": [
            {"title": "Headspace", "url": "https://www.headspace.com/", "description": "Guided meditations, animations, articles, and videos."},
            {"title": "Calm", "url": "https://www.calm.com/", "description": "A popular app for sleep, meditation, and relaxation."},
            {"title": "Tara Brach", "url": "https://www.tarabrach.com/guided-meditations/", "description": "Free guided meditations and talks on mindfulness."},
            {"title": "Mindful.org", "url": "https://www.mindful.org/", "description": "Articles, guides, and resources on practicing mindfulness."}
        ],
        "💪 Fitness & Movement": [
            {"title": "Nike Training Club", "url": "https://www.nike.com/ntc-app", "description": "A wide range of free workouts and personalized training plans."},
            {"title": "Yoga with Adriene", "url": "https://www.youtube.com/user/yogawithadriene", "description": "High-quality free yoga and mindfulness videos for all levels."},
            {"title": "Fitness Blender", "url": "https://www.fitnessblender.com/", "description": "A huge variety of free, full-length workout videos."}
        ],
        "🥗 Nutrition": [
            {"title": "Nutrition.gov", "url": "https://www.nutrition.gov/", "description": "Trustworthy information to make healthy eating choices."},
            {"title": "MyFitnessPal", "url": "https://www.myfitnesspal.com/", "description": "A popular tool for tracking food intake and calories."}
        ],
        "😴 Sleep Health": [
            {"title": "Sleep Foundation", "url": "https://www.sleepfoundation.org/", "description": "Evidence-based information and resources on sleep health."},
            {"title": "The Sleep Council", "url": "https://sleepcouncil.org.uk/", "description": "Practical advice on how to get a better night's sleep."}
        ],
        "🎙️ Wellness Podcasts": [
            {"title": "The Happiness Lab", "url": "https://www.pushkin.fm/podcasts/the-happiness-lab-with-dr-laurie-santros", "description": "Dr. Laurie Santos explores the science of happiness."},
            {"title": "Feel Better, Live More", "url": "https://drchatterjee.com/blog/", "description": "Hosted by Dr. Rangan Chatterjee, offering practical health advice."},
            {"title": "Ten Percent Happier", "url": "https://www.tenpercent.com/podcast", "description": "Interviews with meditation experts and scientists."}
        ],
        "📖 Recommended Books": [
            {"title": "Atomic Habits by James Clear", "url": "https://jamesclear.com/atomic-habits", "description": "A guide to building good habits and breaking bad ones."},
            {"title": "The Power of Now by Eckhart Tolle", "url": "https://eckharttolle.com/power-of-now-a-guide-to-spiritual-enlightenment/", "description": "A book on mindfulness and living in the present moment."},
            {"title": "10% Happier by Dan Harris", "url": "https://www.goodreads.com/book/show/18505796-10-happier", "description": "A true story about a news anchor who discovers meditation."}
        ],
        "❤️ Crisis Support": [
            {"title": "Crisis Text Line", "url": "https://www.crisistextline.org/", "description": "Text HOME to 741741 from anywhere in the US, anytime, about any type of crisis."},
            {"title": "The National Suicide Prevention Lifeline", "url": "https://suicidepreventionlifeline.org/", "description": "Call 988 for free and confidential support."}
        ]
    }

    # --- Filtering Logic ---
    all_categories = list(wellness_resources_data.keys())
    selected_categories = st.multiselect(
        "Filter resources by category:",
        options=all_categories,
        default=[]
    )

    # If no categories are selected, show all. Otherwise, show only selected.
    categories_to_show = selected_categories if selected_categories else all_categories

    st.markdown("---")

    # --- Display Resources in Cards ---
    for category in categories_to_show:
        resources = wellness_resources_data[category]

        if category == "❤️ Crisis Support":
            st.subheader(category)
            st.warning("If you are in immediate distress, please reach out. You are not alone.")
        else:
            st.subheader(category)

        col1, col2 = st.columns(2)
        
        for i, resource in enumerate(resources):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                with st.container(border=True):
                    st.markdown(f"##### {resource['title']}")
                    st.write(resource['description'])
                    st.page_link(resource['url'], label="Visit Resource 🔗", icon="➡️")

                    # --- Rating Logic ---
                    if category != "❤️ Crisis Support":
                        st.markdown("---")
                        current_rating = st.session_state.user_ratings.get(resource['url'], 0)
                        
                        key = f"rating_{resource['url']}"

                        new_rating = st.selectbox(
                            "Your Rating:",
                            options=[0, 1, 2, 3, 4, 5],
                            format_func=lambda x: f"{'⭐'*x}" if x > 0 else "Not Rated",
                            index=current_rating,
                            key=key
                        )

                        if new_rating != current_rating:
                            if new_rating > 0:
                                st.session_state.user_ratings[resource['url']] = new_rating
                            elif resource['url'] in st.session_state.user_ratings:
                                del st.session_state.user_ratings[resource['url']]
                            st.rerun()
        
        st.write("") # Add space between categories

# --- Page 8: Community Tips ---
elif page == "🤝 Community Tips":
    st.title("🤝 Community Tips & Stories")
    st.markdown("A collection of anonymous stories and practical tips from our community. We hope you find encouragement and new ideas here.")
    st.markdown("---")

    for item in community_stories:
        with st.container(border=True):
            st.markdown(f"**A tip about: {item['category']}**")
            st.write(f"*{item['story']}*")
            st.caption(f"— {item['author']}")
        st.write("") # Add some space

# --- Page 9: Creative Corner ---
elif page == "🎨 Creative Corner":
    st.title("🎨 Creative Corner")
    st.markdown("Unleash your creativity! Use this space to draw, doodle, and relax. Don't worry about making it perfect—just have fun.")
    st.markdown("---")

    # Import inside the page to avoid dependency issues if not installed
    try:
        from streamlit_drawable_canvas import st_canvas
    except ImportError:
        st.error("The Creative Corner requires the `streamlit-drawable-canvas` library. Please install it by running `pip install streamlit-drawable-canvas`")
        st.stop()

    # --- Canvas Controls ---
    col1, col2 = st.columns(2)
    with col1:
        stroke_width = st.slider("Stroke width: ", 1, 25, 3)
    with col2:
        stroke_color = st.color_picker("Stroke color: ", "#000000")

    bg_color = st.color_picker("Background color: ", "#EEEEEE")

    # --- Create the Canvas ---
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas",
    )

# --- Page 10: Wellness Goals ---
elif page == "🎯 Wellness Goals":
    st.title("🎯 Wellness Goal Setting")
    st.markdown("Set long-term ambitions and break them down into smaller, manageable sub-tasks.")
    st.markdown("---")

    # Initialize session state for goals
    if "wellness_goals" not in st.session_state:
        st.session_state.wellness_goals = []

    # --- Goal Input Form ---
    with st.form("new_goal_form", clear_on_submit=True):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            new_goal = st.text_input("Enter a new wellness goal:", label_visibility="collapsed", placeholder="Enter a new wellness goal...")
        with col2:
            target_date = st.date_input("Target Date", min_value=datetime.today(), label_visibility="collapsed")
        
        submitted = st.form_submit_button("➕ Add New Goal")
        if submitted and new_goal:
            st.session_state.wellness_goals.append({
                "goal": new_goal,
                "status": "Not Started",
                "key": str(uuid.uuid4()),
                "target_date": target_date,
                "sub_tasks": []
            })
            st.rerun()

    st.subheader("📈 Your Goals")

    # --- Display Progress Bar ---
    if st.session_state.wellness_goals:
        # Auto-migrate old goals to new data structure
        for i, goal in enumerate(st.session_state.wellness_goals):
            if "sub_tasks" not in goal:
                st.session_state.wellness_goals[i]["sub_tasks"] = []

        completed_count = sum(1 for g in st.session_state.wellness_goals if g.get("status") == "Completed")
        total_count = len(st.session_state.wellness_goals)
        progress_ratio = completed_count / total_count if total_count > 0 else 0
        st.progress(progress_ratio, text=f"{completed_count}/{total_count} Goals Completed")

        if completed_count > 0 and completed_count == total_count:
            st.balloons()
            st.success("🎉 You've completed all your goals! Amazing work!")

    # --- Display and Manage Goals ---
    if not st.session_state.wellness_goals:
        st.info("You haven't set any goals yet. Add one above to get started!")
    else:
        goal_indices_to_delete = []
        for i, goal in enumerate(st.session_state.wellness_goals):
            goal_key = goal['key']

            # --- Automatic Status Update Logic ---
            if goal.get("sub_tasks"):
                all_subs_completed = all(st["completed"] for st in goal["sub_tasks"])
                if all_subs_completed:
                    st.session_state.wellness_goals[i]["status"] = "Completed"
                elif any(st["completed"] for st in goal["sub_tasks"]):
                    st.session_state.wellness_goals[i]["status"] = "In Progress"
                else:
                    st.session_state.wellness_goals[i]["status"] = "Not Started"
            
            st.markdown("--- ")
            
            # --- Main Goal Display ---
            col_title, col_delete_goal = st.columns([0.9, 0.1])
            with col_title:
                st.subheader(goal["goal"])
            with col_delete_goal:
                if st.button("🗑️", key=f"delete_goal_{goal_key}", help="Delete this entire goal"):
                    goal_indices_to_delete.append(i)
                    st.rerun()

            # --- Goal Details (Status, Date, Sub-task progress) ---
            status = goal.get("status", "Not Started")
            color = "green" if status == "Completed" else "orange" if status == "In Progress" else "blue"
            
            sub_task_count = len(goal.get("sub_tasks", []))
            completed_sub_tasks = sum(1 for st in goal.get("sub_tasks", []) if st["completed"])

            meta_col1, meta_col2, meta_col3 = st.columns(3)
            with meta_col1:
                st.markdown(f":{color}[●] **Status:** {status}")
            with meta_col2:
                if "target_date" in goal and goal["target_date"]:
                    days_remaining = (goal["target_date"] - datetime.now().date()).days
                    if status != "Completed" and days_remaining < 0:
                        st.markdown(f"🗓️ **Target:** {goal['target_date'].strftime('%b %d')} (Overdue)")
                    else:
                        st.markdown(f"🗓️ **Target:** {goal['target_date'].strftime('%b %d, %Y')}")
            with meta_col3:
                st.markdown(f"✅ **Sub-tasks:** {completed_sub_tasks}/{sub_task_count}")

            # --- Sub-task Management --- 
            with st.expander("Manage Sub-tasks"):
                # --- Add new sub-task ---
                with st.form(f"sub_task_form_{goal_key}", clear_on_submit=True):
                    new_sub_task_text = st.text_input("Add a new sub-task", placeholder="Break it down...", label_visibility="collapsed")
                    if st.form_submit_button("➕ Add Sub-task"):
                        if new_sub_task_text:
                            st.session_state.wellness_goals[i]["sub_tasks"].append({
                                "task": new_sub_task_text,
                                "completed": False,
                                "key": str(uuid.uuid4())
                            })
                            st.rerun()

                # --- Display and manage sub-tasks ---
                sub_indices_to_delete = []
                for sub_i, sub_task in enumerate(goal["sub_tasks"]):
                    sub_task_key = sub_task['key']
                    sub_col1, sub_col2 = st.columns([0.9, 0.1])
                    with sub_col1:
                        is_completed = st.checkbox(
                            sub_task["task"],
                            value=sub_task["completed"],
                            key=f"subtask_{sub_task_key}"
                        )
                        if is_completed != sub_task["completed"]:
                            st.session_state.wellness_goals[i]["sub_tasks"][sub_i]["completed"] = is_completed
                            st.rerun()
                    with sub_col2:
                        if st.button("🗑️", key=f"delete_subtask_{sub_task_key}", help="Delete sub-task"):
                            sub_indices_to_delete.append(sub_i)
                
                if sub_indices_to_delete:
                    for index in sorted(sub_indices_to_delete, reverse=True):
                        del st.session_state.wellness_goals[i]["sub_tasks"][index]
                    st.rerun()

        if goal_indices_to_delete:
            for index in sorted(goal_indices_to_delete, reverse=True):
                del st.session_state.wellness_goals[index]
            st.rerun()