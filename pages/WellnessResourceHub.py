import streamlit as st
import random
import pandas as pd
from datetime import datetime
import uuid

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
wellness_tasks_categorized = {
    "Mindfulness & Reflection": [
        "Take 10 deep, slow breaths",
        "Write down one thing you're grateful for",
        "Listen to one favorite calming song",
        "Jot down 3 things you accomplished today, big or small."
    ],
    "Physical Well-being": [
        "Drink a full glass of water",
        "Stretch for 5 minutes",
        "Go for a 10-minute walk outside",
        "Put on a favorite upbeat song and have a mini dance party."
    ],
    "Environment & Breaks": [
        "Tidy up your workspace for 5 minutes",
        "Step away from screens for 5 minutes",
        "Step outside for 2 minutes and take a breath of fresh air.",
        "Look out a window and name 5 different things you can see."
    ],
    "Social Connection": [
        "Send a thank you message to a friend or family member."
    ]
}

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

    # --- Wellness Tip Collections ---
    stress_tips = [
        "Try a 5-minute guided meditation to calm your mind.",
        "Step away from your screen for 10 minutes and stretch.",
        "Listen to some calming music or nature sounds."
    ]

    sleep_tips = [
        "Avoid caffeine or large meals close to bedtime.",
        "Create a relaxing bedtime routine, like reading a book.",
        "Ensure your bedroom is dark, quiet, and cool."
    ]

    mood_tips = [
        "Journal your thoughts to understand your feelings better.",
        "Reach out to a friend or loved one to talk.",
        "Engage in a hobby that you enjoy."
    ]
    
    energy_tips = [
        "Ensure you're getting enough rest and nutrients.",
        "A short walk can sometimes boost energy more than a nap.",
        "Stay hydrated to maintain your energy levels."
    ]

    activity_tips = [
        "Even a short 10-minute walk can boost your energy and mood.",
        "Try a quick 7-minute workout routine.",
        "Dancing to your favorite song is a fun way to get moving."
    ]

    social_tips = [
        "Consider calling or messaging a friend or family member.",
        "Even a brief, positive social interaction can improve your day.",
        "Plan a social activity for the coming week."
    ]

    # Initialize session state for self-check history
    if "self_check_history" not in st.session_state:
        st.session_state.self_check_history = []

    with st.container(border=True):
        st.subheader("How are you feeling today?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            stress = st.slider("🧠 Stress", 0, 10, 5, help="0 = Not Stressed, 10 = Extremely Stressed")
            sleep = st.slider("😴 Sleep (hours)", 0, 12, 7, help="How many hours of sleep did you get last night?")
            energy_level = st.slider("⚡️ Energy Level", 0, 10, 6, help="0 = No Energy, 10 = Full of Energy")

        with col2:
            physical_activity = st.number_input("🏃‍♂️ Physical Activity (minutes)", min_value=0, help="How many minutes did you exercise today?")
            social_connection = st.radio("🤝 Social Connection", ["Yes", "No"], horizontal=True, help="Did you connect with a friend or loved one today?")
            
            mood_options = {"😞": 2, "😐": 5, "😊": 8}
            selected_emoji = st.radio("😊 Mood", options=list(mood_options.keys()), horizontal=True, help="How is your overall mood today?")
            mood_score = mood_options[selected_emoji]

        note = st.text_area("Add a note about your day (optional):", placeholder="What's on your mind? Any details about why you feel this way?")

        if st.button("Log and Get My Wellness Tip"):
            # --- Tip Logic ---
            tips_to_show = []
            if stress > 7:
                tips_to_show.append(("stress", f"It looks like your stress is high. To find some calm, you could try this: *{random.choice(stress_tips)}*"))
            if sleep < 6:
                tips_to_show.append(("sleep", f"It seems you had a short night's sleep. To improve your rest, consider this tip: *{random.choice(sleep_tips)}*"))
            if mood_score < 5:
                tips_to_show.append(("mood", f"It's okay to have tough days. For a little mood boost, you could try this: *{random.choice(mood_tips)}*"))
            if energy_level < 4:
                tips_to_show.append(("energy", f"It looks like your energy is low. To recharge, you might find this helpful: *{random.choice(energy_tips)}*"))
            if physical_activity < 20:
                tips_to_show.append(("activity", f"Getting some movement in can really help. Here's a small idea: *{random.choice(activity_tips)}*"))
            if social_connection == "No":
                tips_to_show.append(("social", f"Connecting with others can make a big difference. Here's a gentle nudge: *{random.choice(social_tips)}*"))

            st.markdown("---")
            if not tips_to_show:
                st.success("🌟 You're doing well! Keep maintaining your healthy habits.")
            else:
                st.subheader("💡 Your Personalized Suggestions")
                for category, tip in tips_to_show:
                    with st.container(border=True):
                        st.info(tip)
                        if category == "stress":
                            if st.button("🧘 Start a Breathing Exercise"):
                                st.switch_page("pages/Breathing_Exercise.py")
            
            # --- Store Data ---
            st.session_state.self_check_history.append({
                "Date": datetime.now(),
                "Stress": stress,
                "Sleep (hours)": sleep,
                "Mood": mood_score,
                "Energy": energy_level,
                "Activity (min)": physical_activity,
                "Social": 1 if social_connection == "Yes" else 0,
                "Note": note
            })
            st.rerun()

    # --- History and Visualization ---
    if st.session_state.self_check_history:
        st.markdown("---")
        st.subheader("📈 Your Self-Check History")
        
        history_df = pd.DataFrame(st.session_state.self_check_history)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        history_df = history_df.set_index("Date")

        # --- Summary Statistics ---
        st.subheader("📊 Summary Statistics")
        time_window = st.selectbox("Select time window:", ["Last 7 days", "Last 30 days", "All time"])

        if time_window == "Last 7 days":
            summary_df = history_df[history_df.index > datetime.now() - pd.Timedelta(days=7)]
        elif time_window == "Last 30 days":
            summary_df = history_df[history_df.index > datetime.now() - pd.Timedelta(days=30)]
        else:
            summary_df = history_df

        if not summary_df.empty:
            avg_metrics = summary_df.drop(columns=['Note'], errors='ignore').mean()
            cols = st.columns(len(avg_metrics))
            for i, (metric, value) in enumerate(avg_metrics.items()):
                with cols[i]:
                    st.metric(label=f"Avg. {metric}", value=f"{value:.1f}")
        else:
            st.info("Not enough data for this time window.")

        # --- Interactive Chart ---
        st.subheader("📈 Interactive Chart")
        
        available_metrics = [col for col in history_df.columns if col != 'Note']
        
        selected_metrics = st.multiselect(
            "Select metrics to display:",
            options=available_metrics,
            default=available_metrics[:3]
        )

        if selected_metrics:
            st.line_chart(history_df[selected_metrics])
        else:
            st.info("Select one or more metrics to display the chart.")

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
    
    # --- Data Migration ---
    migrated_tasks = []
    for task in st.session_state.tasks:
        if isinstance(task, str): # Very old format
            migrated_tasks.append({"task": task, "completed": False, "key": str(uuid.uuid4()), "priority": "Medium", "due_date": None})
        else:
            if "key" not in task:
                task["key"] = str(uuid.uuid4())
            if "priority" not in task:
                task["priority"] = "Medium"
            if "due_date" not in task:
                task["due_date"] = None # Add default due_date
            migrated_tasks.append(task)
    st.session_state.tasks = migrated_tasks


    # --- Task Input Form ---
    with st.form("new_task_form", clear_on_submit=True):
        st.write("Add a new task")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_task = st.text_input("Task description", label_visibility="collapsed", placeholder="What do you need to do?")
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1, label_visibility="collapsed")
        with col3:
            due_date = st.date_input("Due Date", value=None, label_visibility="collapsed")

        submitted = st.form_submit_button("➕ Add Task")
        if submitted and new_task:
            st.session_state.tasks.append({
                "task": new_task, 
                "completed": False, 
                "key": str(uuid.uuid4()),
                "priority": priority,
                "due_date": due_date
            })
            st.rerun()

    # --- Wellness Task Suggestion Button ---
    st.markdown("--- ")
    st.subheader("💡 Get a Wellness Task Suggestion")
    selected_category = st.selectbox(
        "Choose a category for a task suggestion:",
        list(wellness_tasks_categorized.keys()),
        key="wellness_task_category_selector"
    )
    if st.button(f"Suggest a {selected_category} Task"):
        suggested_task = random.choice(wellness_tasks_categorized[selected_category])
        st.session_state.tasks.append({
            "task": suggested_task, 
            "completed": False, 
            "key": str(uuid.uuid4()),
            "priority": "Medium",
            "due_date": None
        })
        st.rerun()

    st.subheader("✅ Your Tasks")

    # --- Sorting and Filtering ---
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.radio(
            "Sort by:",
            ["Order Added", "Due Date", "Priority"],
            horizontal=True,
            key="task_sort"
        )
    with col2:
        filter_status = st.selectbox(
            "Filter by:",
            ["All", "Incomplete", "Completed"],
            key="task_filter"
        )

    tasks_to_display = st.session_state.tasks.copy()

    # --- Filtering Logic ---
    if filter_status == "Incomplete":
        tasks_to_display = [t for t in tasks_to_display if not t["completed"]]
    elif filter_status == "Completed":
        tasks_to_display = [t for t in tasks_to_display if t["completed"]]
    
    # --- Sorting Logic ---
    if sort_by == "Due Date":
        # Sorts tasks with due dates first, then tasks without
        tasks_to_display.sort(key=lambda x: (x.get('due_date') is None, x.get('due_date')))
    elif sort_by == "Priority":
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        tasks_to_display.sort(key=lambda x: priority_map.get(x.get('priority', 'Medium')))


    # --- Display Progress Bar ---
    if tasks_to_display:
        completed_count = sum(1 for t in tasks_to_display if t["completed"])
        total_count = len(tasks_to_display)
        progress_ratio = completed_count / total_count if total_count > 0 else 0
        st.progress(progress_ratio, text=f"{completed_count}/{total_count} Tasks Completed")

        # --- Celebrate Completion ---
        if completed_count > 0 and completed_count == total_count:
            st.balloons()
            st.success("🎉 All tasks completed! Great job!")

    # --- Task Display, Edit, and Deletion Logic ---
    indices_to_delete = []
    for i, task in enumerate(tasks_to_display):
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
                    # Find the original task in the main list and update it
                    for original_task in st.session_state.tasks:
                        if original_task["key"] == task["key"]:
                            original_task["task"] = st.session_state.edited_task_text
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
                priority_icon = {"Low": "🔹", "Medium": "🔸", "High": "🔥"}.get(task.get("priority", "Medium"), "🔸")
                
                due_date_str = ""
                if task.get("due_date"):
                    due_date_str = f" (Due: {task['due_date'].strftime('%b %d')})"

                base_label = f"{priority_icon} {task['task']}{due_date_str}"
                label = f"~~{base_label}~~" if task["completed"] else base_label
                
                # Find the original task index to modify its 'completed' status
                original_task_index = next((idx for idx, t in enumerate(st.session_state.tasks) if t["key"] == task["key"]), None)
                if original_task_index is not None:
                    if st.checkbox(label, value=task["completed"], key=f"task_{task['key']}") != task["completed"]:
                         st.session_state.tasks[original_task_index]["completed"] = not task["completed"]
                         st.rerun()

            with col_edit_btn:
                if st.button("✏️ Edit", key=f"edit_btn_{task['key']}"):
                    st.session_state.editing_task_id = task["key"]
                    st.session_state.edited_task_text = task["task"]
                    st.rerun()
            with col_delete_btn:
                if st.button("🗑️", key=f"delete_btn_{task['key']}", help=f"Delete task: {task['task']}"):
                    # Find the original task to delete it
                    original_task_index = next((idx for idx, t in enumerate(st.session_state.tasks) if t["key"] == task["key"]), None)
                    if original_task_index is not None:
                        indices_to_delete.append(original_task_index)

    # Perform deletions after iterating through the list
    if indices_to_delete:
        # Sort indices in reverse to avoid index shifting issues
        for index in sorted(indices_to_delete, reverse=True):
            del st.session_state.tasks[index]
        st.rerun()

    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above!")

# --- Page 5: Mood Tracker ---
elif page == "📊 Mood Tracker":
    st.title("📊 Mood Tracker")
    st.write("Log your daily mood and add a note to track progress and identify patterns.")

    # Initialize session state for moods
    if "moods" not in st.session_state:
        st.session_state.moods = []

    # --- Data Migration for backward compatibility ---
    migrated_moods = []
    if st.session_state.moods and ("mood" in st.session_state.moods[0]):
        for m in st.session_state.moods:
            primary_mood_map = {
                "😊 Happy": "😊 Positive",
                "😐 Okay": "😐 Neutral",
                "😟 Stressed": "😟 Negative",
                "😢 Sad": "😟 Negative"
            }
            migrated_moods.append({
                "date": m.get("date", datetime.now()),
                "primary_mood": primary_mood_map.get(m["mood"], "😐 Neutral"),
                "intensity": 3,
                "tags": [m["mood"]] if m["mood"] in ["😟 Stressed", "😢 Sad"] else [],
                "note": m.get("note", "")
            })
        st.session_state.moods = migrated_moods
    
    # --- Mood Logging UI ---
    with st.container(border=True):
        st.subheader("How are you feeling right now?")
        primary_mood = st.radio(
            "What's your primary mood today?",
            ["😊 Positive", "😐 Neutral", "😟 Negative"],
            horizontal=True
        )
        mood_intensity = st.slider(
            "How strong is this feeling?",
            1, 5, 3,
            help="1 = Mild, 5 = Very Strong"
        )
        mood_tags = st.multiselect(
            "You can also select other feelings or activities from today:",
            ["Grateful", "Tired", "Anxious", "Productive", "Creative", "Relaxed", "Stressed"]
        )
        note = st.text_area("Add a note to remember the context (optional):")

        if st.button("Log Mood"):
            st.session_state.moods.append({
                "date": datetime.now(),
                "primary_mood": primary_mood,
                "intensity": mood_intensity,
                "tags": mood_tags,
                "note": note
            })
            st.success(f"Logged mood: {primary_mood}")
            st.rerun()

    st.markdown("---")

    # --- Mood History Display ---
    if st.session_state.moods:
        st.subheader("📅 Your Mood Log")
        for entry in reversed(st.session_state.moods):
            mood_icon = entry.get('primary_mood', '😐')[0]
            date_str = entry.get('date', datetime.now()).strftime("%B %d, %Y")
            intensity = entry.get('intensity', 'N/A')

            with st.expander(f"{mood_icon} {date_str} - Intensity: {intensity}"):
                if entry.get('note'):
                    st.write(f"**Note:** *{entry['note']}*")
                
                if entry.get('tags'):
                    st.write("**Tags:**")
                    st.multiselect(
                        f"tags_display_{entry['date']}",
                        options=entry['tags'],
                        default=entry['tags'],
                        disabled=True,
                        label_visibility="collapsed"
                    )


        st.subheader("📊 Mood Analysis")
        st.write("Here are some patterns from your recent mood logs:")
        df = pd.DataFrame(st.session_state.moods)
        df['date'] = pd.to_datetime(df['date'])

        # Ensure 'primary_mood' column exists before trying to access it
        if 'primary_mood' in df.columns and not df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Primary Mood Distribution**")
                mood_counts = df['primary_mood'].value_counts()
                st.bar_chart(mood_counts)

                st.write("**Mood Intensity Over Time**")
                intensity_df = df.set_index('date')
                st.line_chart(intensity_df['intensity'])

            with col2:
                st.write("**Most Common Feelings & Activities**")
                all_tags = [tag for tags_list in df['tags'] for tag in tags_list]
                if all_tags:
                    tag_counts = pd.Series(all_tags).value_counts()
                    st.bar_chart(tag_counts)
                else:
                    st.info("Add tags to your entries to see which feelings are most common.")

        else:
            st.info("Log your mood to see an analysis here.")
        
        st.markdown("---")
        st.subheader("🔍 A Look Back")
        st.write("Curious about your past self? See your mood from a week or a month ago.")

        def find_closest_entry(target_date):
            if not st.session_state.moods:
                return None
            
            df = pd.DataFrame(st.session_state.moods)
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # Find the entry with the minimum difference from the target date
            time_diffs = abs(df['date'] - target_date)
            closest_index = time_diffs.idxmin()
            
            # Only return if the closest entry is within a reasonable threshold (e.g., 1 day)
            if time_diffs[closest_index] <= pd.Timedelta(days=1):
                return df.loc[closest_index].to_dict()
            return None

        col1, col2 = st.columns(2)

        with col1:
            if st.button("What was my mood a week ago?"):
                target = datetime.now().date() - pd.Timedelta(days=7)
                past_entry = find_closest_entry(target)
                if past_entry:
                    mood = past_entry.get('primary_mood', 'N/A')
                    note = past_entry.get('note', '*No note was left.*')
                    st.info(f"A week ago, you felt: **{mood}**. You wrote: *'{note}'*")
                else:
                    st.warning("No entry found from around a week ago.")

        with col2:
            if st.button("What was my mood a month ago?"):
                target = datetime.now().date() - pd.Timedelta(days=30)
                past_entry = find_closest_entry(target)
                if past_entry:
                    mood = past_entry.get('primary_mood', 'N/A')
                    note = past_entry.get('note', '*No note was left.*')
                    st.info(f"A month ago, you felt: **{mood}**. You wrote: *'{note}'*")
                else:
                    st.warning("No entry found from around a month ago.")

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

    st.subheader("😥 For Managing Difficult Emotions")
    st.markdown('''
        - What is a feeling you are currently struggling with? Describe it without judgment.
        - Write a letter to your anxiety or stress. What do you want to say to it?
        - What does support look like for you right now? Who or what can provide it?
        - Describe a time you felt resilient. What did that feel like in your body?
    ''')

    st.subheader("🧘‍♀️ For Mind-Body Connection")
    st.markdown('''
        - How does your body feel today? Scan from head to toe and notice any sensations.
        - What is one thing your body does for you that you're grateful for?
        - Describe an activity that makes you feel strong and capable in your body.
        - What is one way you can be kinder to your body this week?
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
        from PIL import Image
    except ImportError:
        st.error("The Creative Corner requires the `streamlit-drawable-canvas` and `Pillow` libraries. Please install them by running `pip install streamlit-drawable-canvas Pillow`")
        st.stop()

    drawing_prompts = [
        "Draw your happy place.",
        "Doodle your favorite animal.",
        "Illustrate a feeling without using words.",
        "Draw a pattern that represents your current mood.",
        "Create a character from your imagination.",
        "Draw something that makes you feel calm.",
        "Doodle a collection of your favorite things.",
        "Illustrate a dream you remember.",
        "Draw a plant or a flower from memory.",
        "Create an abstract design using only lines and shapes."
    ]

    if 'drawing_prompt' not in st.session_state:
        st.session_state.drawing_prompt = random.choice(drawing_prompts)

    if st.button("Get a New Prompt"):
        st.session_state.drawing_prompt = random.choice(drawing_prompts)

    st.info(f"**Drawing Prompt:** {st.session_state.drawing_prompt}")
    st.markdown("---")


    # --- Canvas Controls ---
    if 'drawing_mode' not in st.session_state:
        st.session_state.drawing_mode = "freedraw"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Freedraw"):
            st.session_state.drawing_mode = "freedraw"
    with col2:
        if st.button("Line"):
            st.session_state.drawing_mode = "line"
    with col3:
        if st.button("Rectangle"):
            st.session_state.drawing_mode = "rect"
    with col4:
        if st.button("Circle"):
            st.session_state.drawing_mode = "circle"
            
    col1, col2 = st.columns(2)
    with col1:
        stroke_width = st.slider("Stroke width: ", 1, 25, 3)
    with col2:
        stroke_color = st.color_picker("Stroke color: ", "#000000")

    bg_color = st.color_picker("Background color: ", "#EEEEEE")
    bg_image = st.file_uploader("Upload a background image:", type=["png", "jpg"])

    # --- Create the Canvas ---
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        height=400,
        width=600,
        drawing_mode=st.session_state.drawing_mode,
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