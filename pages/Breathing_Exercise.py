import streamlit as st
import time
import datetime
import json
from streamlit_lottie import st_lottie

# --- CONFIG & CONSTANTS ---
TECHNIQUES = {
    "Default Relaxation (4-2-4)": {"inhale": 4, "hold1": 2, "exhale": 4, "hold2": 0},
    "Box Breathing (4-4-4-4)": {"inhale": 4, "hold1": 4, "exhale": 4, "hold2": 4},
    "4-7-8 Breathing": {"inhale": 4, "hold1": 7, "exhale": 8, "hold2": 0},
}
LOTTIE_ANIMATION_PATH = "assets/yoga_animation.json"

# --- STATE MANAGEMENT ---
def initialize_state():
    """Initializes all necessary session state variables."""
    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'SETUP'
    if 'session_log' not in st.session_state:
        st.session_state.session_log = []
    if 'mood_before' not in st.session_state:
        st.session_state.mood_before = 5
    if 'mood_after' not in st.session_state:
        st.session_state.mood_after = None
    if 'session_minutes' not in st.session_state:
        st.session_state.session_minutes = 2
    if 'breathing_technique' not in st.session_state:
        st.session_state.breathing_technique = list(TECHNIQUES.keys())[0]

# --- HELPER FUNCTIONS ---
def load_lottie_animation(filepath):
    """Loads a Lottie animation from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def calculate_streak(log):
    if not log: return 0
    unique_dates = sorted(list(set([entry['timestamp'].date() for entry in log])), reverse=True)
    today, streak = datetime.date.today(), 0
    if not (unique_dates[0] == today or unique_dates[0] == today - datetime.timedelta(days=1)): return 0
    if unique_dates[0] == today: streak += 1
    for i in range(len(unique_dates) - 1):
        if unique_dates[i] - datetime.timedelta(days=1) == unique_dates[i+1]: streak += 1
        else: break
    if unique_dates[0] == today - datetime.timedelta(days=1) and streak == 0: streak = 1
    return streak

def calculate_weekly_minutes(log):
    one_week_ago = datetime.datetime.now().date() - datetime.timedelta(days=7)
    return sum(entry['duration'] for entry in log if entry['timestamp'].date() > one_week_ago)

# --- UI VIEWS ---
def show_setup_view():
    st.markdown("<h2 style='text-align: center; color: teal;'>🧘 Breathing Exercise</h2>", unsafe_allow_html=True)
    st.markdown("Use this guided exercise to relax. Select a technique, then start your session.")

    st.markdown("### 📊 Your Progress")
    col1, col2 = st.columns(2)
    col1.metric("Current Streak", f"{calculate_streak(st.session_state.session_log)} Days 🔥")
    col2.metric("This Week's Total", f"{calculate_weekly_minutes(st.session_state.session_log)} Mins")
    st.markdown("--- ")

    st.markdown("### ⚙️ Session Setup")
    st.session_state.breathing_technique = st.selectbox("Choose a Breathing Technique:", options=list(TECHNIQUES.keys()))
    
    st.session_state.mood_before = st.slider("First, rate your current stress level (1=Low, 10=High):", 1, 10, 5)
    st.session_state.session_minutes = st.slider("How many minutes do you want to practice?", 1, 15, 2)
    
    if st.button("Start Session"):
        st.session_state.page_state = 'RUNNING'
        st.rerun()

def run_session_view():
    params = TECHNIQUES[st.session_state.breathing_technique]
    inhale, hold1, exhale, hold2 = params['inhale'], params['hold1'], params['exhale'], params['hold2']
    cycle_length = sum(params.values())

    st.markdown(f"<h2 style='text-align: center; color: teal;'>🧘 {st.session_state.breathing_technique}</h2>", unsafe_allow_html=True)
    
    lottie_animation = load_lottie_animation(LOTTIE_ANIMATION_PATH)
    if lottie_animation:
        st_lottie(lottie_animation, height=200, speed=1, quality="high")
    else:
        st.warning("Animation file not found. Displaying a placeholder.")

    timer_placeholder = st.empty()
    breath_text_placeholder = st.empty()
    total_seconds = st.session_state.session_minutes * 60

    for i in range(total_seconds, 0, -1):
        mins, secs = divmod(i, 60)
        timer_placeholder.markdown(f"<h2 style='text-align: center;'>⏳ {mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)

        phase_time = (total_seconds - i) % cycle_length
        if 0 <= phase_time < inhale: breath_text_placeholder.markdown("<h3 style='text-align: center;'>🌬️ Breathe In...</h3>", unsafe_allow_html=True)
        elif inhale <= phase_time < inhale + hold1: breath_text_placeholder.markdown("<h3 style='text-align: center;'>✋ Hold...</h3>", unsafe_allow_html=True)
        elif inhale + hold1 <= phase_time < inhale + hold1 + exhale: breath_text_placeholder.markdown("<h3 style='text-align: center;'>😮‍💨 Breathe Out...</h3>", unsafe_allow_html=True)
        else: breath_text_placeholder.markdown("<h3 style='text-align: center;'>✋ Hold...</h3>", unsafe_allow_html=True)
        time.sleep(1)

    st.session_state.session_log.append({'timestamp': datetime.datetime.now(), 'duration': st.session_state.session_minutes, 'technique': st.session_state.breathing_technique})
    st.session_state.page_state = 'SUMMARY'
    st.rerun()

def show_summary_view():
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

    technique_practiced = st.session_state.session_log[-1]['technique']
    duration_practiced = st.session_state.session_log[-1]['duration']
    st.success(f"Great job! You completed a {duration_practiced}-minute session of {technique_practiced}.")
    st.markdown("--- ")
    if st.button("✨ Start Another Session"):
        st.session_state.page_state = 'SETUP'
        st.session_state.mood_after = None
        st.rerun()

# --- Main App Logic ---
initialize_state()

if st.session_state.page_state == 'SETUP': show_setup_view()
elif st.session_state.page_state == 'RUNNING': run_session_view()
elif st.session_state.page_state == 'SUMMARY': show_summary_view()