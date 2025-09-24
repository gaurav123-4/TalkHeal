import streamlit as st
import time
import datetime

def initialize_state():
    """Initializes all necessary session state variables."""
    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'SETUP'
    if 'session_log' not in st.session_state:
        st.session_state.session_log = [] # List of {'timestamp': dt, 'duration': mins}
    if 'mood_before' not in st.session_state:
        st.session_state.mood_before = 5
    if 'mood_after' not in st.session_state:
        st.session_state.mood_after = None
    if 'session_minutes' not in st.session_state:
        st.session_state.session_minutes = 2

def calculate_streak(log):
    """Calculates the current practice streak in days."""
    if not log:
        return 0
    
    log_dates = sorted([entry['timestamp'].date() for entry in log], reverse=True)
    unique_dates = sorted(list(set(log_dates)), reverse=True)
    
    today = datetime.date.today()
    streak = 0

    # Check if the most recent session was today or yesterday
    if not (unique_dates[0] == today or unique_dates[0] == today - datetime.timedelta(days=1)):
        return 0

    if unique_dates[0] == today:
        streak += 1
        
    for i in range(len(unique_dates) - 1):
        if unique_dates[i] - datetime.timedelta(days=1) == unique_dates[i+1]:
            streak += 1
        else:
            break
            
    # If the last session was yesterday, the streak starts from there
    if unique_dates[0] == today - datetime.timedelta(days=1) and streak == 0:
        streak = 1

    return streak

def calculate_weekly_minutes(log):
    """Calculates total practice minutes in the last 7 days."""
    one_week_ago = datetime.datetime.now().date() - datetime.timedelta(days=7)
    weekly_minutes = 0
    for entry in log:
        if entry['timestamp'].date() > one_week_ago:
            weekly_minutes += entry['duration']
    return weekly_minutes

def show_setup_view():
    """Displays the main page for setting up the exercise."""
    st.markdown("<h2 style='text-align: center; color: teal;'>🧘 Breathing Exercise</h2>", unsafe_allow_html=True)
    st.markdown("Use this simple breathing exercise to relax. Follow the circle expanding and contracting.")

    st.markdown("### 📊 Your Progress")
    col1, col2 = st.columns(2)
    with col1:
        streak = calculate_streak(st.session_state.session_log)
        st.metric("Current Streak", f"{streak} Days 🔥")
    with col2:
        weekly_minutes = calculate_weekly_minutes(st.session_state.session_log)
        st.metric("This Week's Total", f"{weekly_minutes} Mins")

    st.markdown("--- ")

    st.markdown("### ⚙️ Session Setup")
    st.session_state.mood_before = st.slider("First, rate your current stress level (1=Low, 10=High):", 1, 10, 5)
    st.session_state.session_minutes = st.slider("How many minutes do you want to practice?", 1, 15, 2)
    
    if st.button("Start Session"):
        st.session_state.page_state = 'RUNNING'
        st.rerun()

def run_session_view():
    """Displays the animation and timer for the session."""
    st.markdown("<h2 style='text-align: center; color: teal;'>🧘 Breathing Exercise</h2>", unsafe_allow_html=True)
    st.markdown("### 👇 Follow the animation to breathe in and out")

    circle_animation = """
    <style>
    @keyframes breathe { 0% { transform: scale(0.8); } 40% { transform: scale(1.2); } 60% { transform: scale(1.2); } 100% { transform: scale(0.8); } }
    .breathing-circle { margin: auto; margin-top: 50px; height: 150px; width: 150px; border-radius: 50%; background-color: #90e0ef; animation: breathe 10s ease-in-out infinite; }
    </style>
    <div class="breathing-circle"></div>
    """
    st.markdown(circle_animation, unsafe_allow_html=True)
    st.write("") # Spacer

    timer_placeholder = st.empty()
    breath_text_placeholder = st.empty()
    
    total_seconds = st.session_state.session_minutes * 60
    cycle_length = 10 # 4s in, 2s hold, 4s out

    for i in range(total_seconds, 0, -1):
        mins, secs = divmod(i, 60)
        timer_placeholder.markdown(f"<h2 style='text-align: center;'>⏳ {mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)

        phase_time = (total_seconds - i) % cycle_length
        if 0 <= phase_time < 4:
            breath_text_placeholder.markdown("<h3 style='text-align: center;'>🌬️ Breathe In...</h3>", unsafe_allow_html=True)
        elif 4 <= phase_time < 6:
            breath_text_placeholder.markdown("<h3 style='text-align: center;'>✋ Hold...</h3>", unsafe_allow_html=True)
        else:
            breath_text_placeholder.markdown("<h3 style='text-align: center;'>😮‍💨 Breathe Out...</h3>", unsafe_allow_html=True)
        time.sleep(1)

    # Log the session
    st.session_state.session_log.append({
        'timestamp': datetime.datetime.now(),
        'duration': st.session_state.session_minutes
    })
    st.session_state.page_state = 'SUMMARY'
    st.rerun()

def show_summary_view():
    """Displays the post-session summary and mood check-in."""
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>✅ Session Complete!</h2>", unsafe_allow_html=True)
    st.markdown("--- ")

    st.markdown("### 📈 Your Results")
    st.session_state.mood_after = st.slider("Finally, rate your new stress level (1=Low, 10=High):", 1, 10, st.session_state.mood_before)

    mood_change = st.session_state.mood_after - st.session_state.mood_before
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Starting Stress", f"{st.session_state.mood_before}/10")
    col2.metric("Ending Stress", f"{st.session_state.mood_after}/10")
    col3.metric("Change", f"{mood_change}")

    if mood_change < 0:
        st.success(f"Great job! Your stress level decreased. You practiced for {st.session_state.session_minutes} minutes.")
    elif mood_change == 0:
        st.info(f"You maintained your stress level. Consistent practice helps! You completed a {st.session_state.session_minutes}-minute session.")
    else:
        st.warning(f"Stress levels can fluctuate. Thank you for taking the time to practice for {st.session_state.session_minutes} minutes today.")

    st.markdown("--- ")
    if st.button("✨ Start Another Session"):
        st.session_state.page_state = 'SETUP'
        st.session_state.mood_after = None
        st.rerun()

# --- Main App Logic ---
initialize_state()

if st.session_state.page_state == 'SETUP':
    show_setup_view()
elif st.session_state.page_state == 'RUNNING':
    run_session_view()
elif st.session_state.page_state == 'SUMMARY':
    show_summary_view()