import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, date, time, timedelta

# --- Configuration ---
DATA_FILE = "water_tracker_data.json"
ML_TO_OZ = 0.033814

# --- Achievements Definition ---
ACHIEVEMENTS = {
    "first_log": {"name": "First Drop!", "description": "Log your first drink."},
    "streak_3": {"name": "On a Roll!", "description": "Hit your goal 3 days in a row."},
    "streak_7": {"name": "Hydration Hero!", "description": "Hit your goal for a full week!"},
    "total_10l": {"name": "Getting Started", "description": "Log a total of 10 liters."},
    "total_50l": {"name": "Serious Sipper", "description": "Log a total of 50 liters."},
}

# --- UI Styling ---
st.set_page_config(
    page_title="Daily Water Tracker",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for a beautiful, interactive, and mobile-friendly look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* --- General Body & Background --- */
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f8ff; /* Fallback */
    }

    .main {
        background-image: linear-gradient(to right top, #84fab0, #8fd3f4);
        background-attachment: fixed;
        color: #0a2540;
    }

    /* --- Main App Container (the "card") --- */
    .st-emotion-cache-1y4p8pa {
        padding-top: 1rem; /* Reduce top padding */
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* --- Typography --- */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        color: #004080;
        text-align: center;
        padding-bottom: 0.5rem;
    }
    .st-subheader {
        font-family: 'Poppins', sans-serif;
        color: #005f9e;
        text-align: center;
        font-weight: 600;
    }

    /* --- Progress Circle --- */
    .progress-circle {
        position: relative;
        width: 210px;
        height: 210px;
        border-radius: 50%;
        background: conic-gradient(var(--fill-color) calc(var(--progress) * 1%), #eaf6ff 0);
        display: grid;
        place-items: center;
        margin: 1rem auto 2rem auto;
        transition: background 0.6s ease-out;
        box-shadow: 0 0 30px rgba(143, 211, 244, 0.5);
    }
    .progress-circle::before {
        content: '';
        position: absolute;
        width: 84%;
        height: 84%;
        background: #ffffff;
        border-radius: 50%;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.07);
    }
    .progress-text {
        position: relative;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        color: #004a7c;
    }
    .progress-subtext {
        position: relative;
        font-size: 1rem;
        color: #555;
        font-weight: 400;
        margin-top: -5px;
    }

    /* --- Quick Add Buttons --- */
    .stButton>button {
        border-radius: 18px;
        background-image: linear-gradient(to right, #63a4ff, #8ed6ff);
        color: white;
        border: none;
        padding: 14px 20px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 164, 255, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 20px rgba(99, 164, 255, 0.4);
        filter: brightness(1.05);
    }
    .stButton>button:active {
        transform: translateY(0px);
        box-shadow: 0 4px 10px rgba(99, 164, 255, 0.3);
    }

    /* --- Custom Amount Form --- */
    .st-form {
        border: none;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1rem;
        background-color: rgba(234, 246, 255, 0.6);
    }
    /* Style for the "Add Custom Amount" button specifically */
    .st-form .stButton>button {
        background-image: linear-gradient(to right, #56ab2f, #a8e063);
    }

    /* --- Log Expander & Entries --- */
    .st-expander {
        border-radius: 18px;
        border: none;
        background-color: rgba(255, 255, 255, 0.4);
        margin-top: 2rem;
    }
    .st-expander header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #005f9e;
    }
    /* This targets the container created by st.container() inside the expander */
    .st-expander div[data-testid="stVerticalBlock"] {
        border-bottom: 1px solid #e0e7ff;
        padding: 0.8rem 0;
    }
     .st-expander > div:last-of-type > div[data-testid="stVerticalBlock"] {
        border-bottom: none;
    }
    .log-text {
        font-size: 1rem;
        color: #223;
        font-weight: 600;
    }
    .log-time {
        font-size: 0.85rem;
        color: #556;
    }
    /* Edit/Delete buttons in the log */
    .st-expander .stButton>button {
        background: transparent;
        color: #99a;
        border: none;
        padding: 5px;
        font-size: 16px;
        box-shadow: none;
        width: auto;
        transition: color 0.2s ease;
    }
    .st-expander .stButton>button:hover {
        color: #ff4b4b; /* Red for delete/cancel */
        transform: none;
        box-shadow: none;
        filter: none;
    }
    .st-expander .stButton>button[help="Save changes"]:hover {
        color: #28a745; /* Green for save */
    }
    .st-expander .stButton>button[help="Edit this entry"]:hover {
        color: #007bff; /* Blue for edit */
    }
</style>
""", unsafe_allow_html=True)


# --- Data Handling Functions ---
def load_data():
    """Loads user data from the JSON file, with defaults for new reminder settings."""
    defaults = {
        "goal": 2500, 
        "units": "ml", 
        "log": {},
        "reminders_enabled": False,
        "reminder_interval": 60,
        "reminder_start_time": "09:00",
        "reminder_end_time": "21:00",
        "quick_add_amounts": [250, 500, 750],
        "reminder_sound_enabled": True,
        "achievements": {},
        "goal_met_dates": [],
        "total_volume_logged_ml": 0
    }
    if not os.path.exists(DATA_FILE):
        return defaults
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Set defaults for any missing keys for backward compatibility
            for key, value in defaults.items():
                data.setdefault(key, value)
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return defaults

def save_data(data):
    """Saves user data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_export_data():
    """Prepares user log data for CSV export."""
    log_data = st.session_state.app_data.get("log", {})
    if not log_data:
        return ""

    export_rows = []
    current_unit = st.session_state.app_data.get("units", "ml")

    for date_str, entries in log_data.items():
        for entry in entries:
            amount_ml = entry['amount']
            display_amount = get_display_amount(amount_ml)
            row = {
                "date": date_str,
                "timestamp": entry['timestamp'],
                "amount_ml": int(amount_ml),
                "amount_display": f"{display_amount:.1f}" if current_unit == "oz" else int(display_amount),
                "unit_display": current_unit
            }
            export_rows.append(row)
    
    if not export_rows:
        return ""

    df = pd.DataFrame(export_rows)
    df = df.sort_values(by="timestamp", ascending=False)
    return df.to_csv(index=False).encode('utf-8')

def log_water_intake(amount_ml):
    """Logs a new water intake entry (always in ml) and saves it."""
    total_before = get_daily_total()
    
    today_str = str(date.today())
    if today_str not in st.session_state.app_data["log"]:
        st.session_state.app_data["log"][today_str] = []
    
    st.session_state.app_data["log"][today_str].append({
        "amount": amount_ml,
        "timestamp": datetime.now().isoformat()
    })
    
    if 'last_toast_time' in st.session_state:
        del st.session_state['last_toast_time']
    
    # --- Achievement Checks ---
    check_achievements(total_before, amount_ml)
    
    save_data(st.session_state.app_data)

def get_daily_total():
    """Calculates the total water intake for today in ml."""
    today_str = str(date.today())
    today_log = st.session_state.app_data["log"].get(today_str, [])
    return sum(entry['amount'] for entry in today_log)

def delete_log_entry(timestamp_to_delete):
    """Deletes a specific water intake entry based on its timestamp."""
    today_str = str(date.today())
    today_log = st.session_state.app_data["log"].get(today_str, [])
    updated_log = [entry for entry in today_log if entry["timestamp"] != timestamp_to_delete]
    if len(updated_log) < len(today_log):
        st.session_state.app_data["log"][today_str] = updated_log
        save_data(st.session_state.app_data)

def update_log_entry(timestamp_to_update, new_amount_ml):
    """Updates the amount for a specific water intake entry (always in ml)."""
    today_str = str(date.today())
    today_log = st.session_state.app_data["log"].get(today_str, [])
    for entry in today_log:
        if entry["timestamp"] == timestamp_to_update:
            entry["amount"] = new_amount_ml
            break
    st.session_state.app_data["log"][today_str] = today_log
    save_data(st.session_state.app_data)

# --- Achievement Functions ---
def unlock_achievement(ach_id):
    """Unlocks an achievement, saves it, and shows a notification."""
    if not st.session_state.app_data["achievements"].get(ach_id, {}).get("unlocked", False):
        st.session_state.app_data["achievements"][ach_id] = {
            "unlocked": True,
            "date": str(date.today())
        }
        st.toast(f"🏆 Achievement Unlocked: {ACHIEVEMENTS[ach_id]['name']}", icon="🏆")

def update_streak():
    """Calculates the current goal streak and unlocks achievements."""
    goal_met_dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in st.session_state.app_data.get("goal_met_dates", [])])
    if not goal_met_dates:
        return

    streak = 0
    # Check from today backwards
    expected_date = date.today()
    if expected_date not in goal_met_dates:
         expected_date = date.today() - timedelta(days=1)

    for d in reversed(goal_met_dates):
        if d == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break
    
    if streak >= 3:
        unlock_achievement("streak_3")
    if streak >= 7:
        unlock_achievement("streak_7")

def check_achievements(total_before_log, amount_logged):
    """Checks all achievement conditions after a log entry."""
    # 1. First Log
    unlock_achievement("first_log")

    # 2. Total Volume
    total_volume = st.session_state.app_data.get("total_volume_logged_ml", 0) + amount_logged
    st.session_state.app_data["total_volume_logged_ml"] = total_volume
    if total_volume >= 10000:
        unlock_achievement("total_10l")
    if total_volume >= 50000:
        unlock_achievement("total_50l")

    # 3. Goal-based streaks
    goal = st.session_state.app_data.get("goal", 2500)
    total_after_log = total_before_log + amount_logged
    if total_before_log < goal and total_after_log >= goal:
        today_str = str(date.today())
        if today_str not in st.session_state.app_data["goal_met_dates"]:
            st.session_state.app_data["goal_met_dates"].append(today_str)
        update_streak()

# --- Unit Conversion and Display Functions ---
def get_display_amount(ml_value):
    """Converts ml to the preferred unit for display."""
    unit = st.session_state.app_data.get("units", "ml")
    if unit == "oz":
        return ml_value * ML_TO_OZ
    return ml_value

def get_display_string(ml_value):
    """Returns a formatted string for the given ml value in the user's preferred unit."""
    unit = st.session_state.app_data.get("units", "ml")
    display_val = get_display_amount(ml_value)
    return f"{display_val:.1f} {unit}" if unit == "oz" else f"{int(display_val)} {unit}"

def convert_to_ml(amount, from_unit):
    """Converts a given amount from a specific unit back to ml."""
    if from_unit == "oz":
        return amount / ML_TO_OZ
    return amount

# --- Historical Data Function ---
def get_historical_data(log_data, num_days):
    """Processes log data to get total intake for the last num_days."""
    history = {}
    today = date.today()
    for i in range(num_days):
        current_date = today - timedelta(days=i)
        date_str = str(current_date)
        
        daily_total = sum(entry['amount'] for entry in log_data.get(date_str, []))
        history[date_str] = daily_total
        
    if not history:
        return pd.DataFrame({'Date': [], 'Intake': []})
        
    df = pd.DataFrame(list(history.items()), columns=['Date', 'Intake'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date').reset_index(drop=True)
    return df

# --- UI Components ---
def display_progress_circle(today_total_ml, goal_ml):
    """Renders the interactive progress circle with preferred units."""
    progress = 0
    if goal_ml > 0:
        progress = min((today_total_ml / goal_ml) * 100, 100)
    
    fill_color = "#63a4ff" if progress < 100 else "#56ab2f"
    
    total_display = get_display_string(today_total_ml)
    goal_display = get_display_string(goal_ml)

    st.markdown(f"""
    <div class="progress-circle" style="--progress: {progress}; --fill-color: {fill_color};">
        <div class="progress-text">
            {progress:.0f}%
            <div class="progress-subtext">{total_display} / {goal_display}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def play_reminder_sound():
    """Plays a notification sound if enabled by the user."""
    if st.session_state.app_data.get("reminder_sound_enabled", False):
        sound_url = "https://raw.githubusercontent.com/interactivenyc/sounds/master/plink.mp3"
        audio_html = f"""
            <audio autoplay hidden>
                <source src="{sound_url}" type="audio/mpeg">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

def check_and_show_reminder():
    """Checks if a reminder should be shown and displays a toast message."""
    settings = st.session_state.app_data
    if not settings.get("reminders_enabled", False):
        return

    now = datetime.now()
    start_time = datetime.strptime(settings.get("reminder_start_time", "09:00"), "%H:%M").time()
    end_time = datetime.strptime(settings.get("reminder_end_time", "21:00"), "%H:%M").time()

    if not (start_time <= now.time() <= end_time):
        return

    today_log = settings.get("log", {}).get(str(date.today()), [])
    last_drink_time = None
    if today_log:
        last_drink_time = datetime.fromisoformat(today_log[-1]['timestamp'])
    else:
        last_drink_time = now.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)

    interval_minutes = settings.get("reminder_interval", 60)
    minutes_passed = (now - last_drink_time).total_seconds() / 60

    if minutes_passed > interval_minutes:
        last_toast_time = st.session_state.get('last_toast_time')
        if last_toast_time and (now - last_toast_time).total_seconds() / 60 < interval_minutes:
            return

        st.toast(f"💧 Time to hydrate! It's been about {int(minutes_passed)} minutes.", icon="💧")
        play_reminder_sound()
        st.session_state.last_toast_time = now

# --- Main Application Logic ---

# Initialize session state
if 'app_data' not in st.session_state:
    # Check for new user BEFORE loading data to set a flag
    is_new_user = not os.path.exists(DATA_FILE)
    st.session_state.app_data = load_data()
    if is_new_user:
        st.session_state.is_new_user = True

if 'editing_timestamp' not in st.session_state:
    st.session_state.editing_timestamp = None

# --- Onboarding UI for New Users ---
if st.session_state.get('is_new_user', False):
    st.title("👋 Welcome to the Water Tracker!")
    st.markdown("Let's get you set up. Please tell us your daily hydration goal.")

    with st.form("onboarding_form"):
        onboarding_unit = st.radio("First, pick your preferred units:", ["ml", "oz"], horizontal=True)
        
        if onboarding_unit == 'ml':
            step, default_value, format_str = 50.0, 2500.0, "%.0f"
        else:
            step, default_value, format_str = 0.5, 84.5, "%.1f"

        onboarding_goal = st.number_input(
            f"Daily Goal ({onboarding_unit})",
            min_value=1.0,
            value=default_value,
            step=step,
            format=format_str
        )
        
        submitted = st.form_submit_button("Start Tracking!")

        if submitted:
            goal_ml = convert_to_ml(onboarding_goal, onboarding_unit)
            
            st.session_state.app_data['units'] = onboarding_unit
            st.session_state.app_data['goal'] = goal_ml
            
            save_data(st.session_state.app_data)
            
            st.session_state.is_new_user = False
            st.balloons()
            st.success("Setup complete! Happy hydrating.")
            import time
            time.sleep(2)
            st.rerun()

# --- Main App UI for Existing Users ---
else:
    unit = st.session_state.app_data.get("units", "ml")
    goal_ml = st.session_state.app_data.get("goal", 2500)

    # --- Sidebar for Settings ---
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Unit Selector
        new_unit = st.radio("Units", ["ml", "oz"], index=["ml", "oz"].index(unit))
        if new_unit != unit:
            st.session_state.app_data['units'] = new_unit
            save_data(st.session_state.app_data)
            st.rerun()

        # Daily Goal Input
        current_goal_display = get_display_amount(goal_ml)
        
        new_goal_display = st.number_input(
            f"Daily Goal ({unit})",
            min_value=1.0,
            value=float(current_goal_display),
            step=50.0 if unit == 'ml' else 0.5,
            format="%.0f" if unit == 'ml' else "%.1f"
        )
        
        if new_goal_display != current_goal_display:
            new_goal_ml = convert_to_ml(new_goal_display, unit)
            st.session_state.app_data['goal'] = new_goal_ml
            save_data(st.session_state.app_data)
            st.rerun()

        with st.expander("Edit Quick-Add Buttons"):
            quick_add_ml = st.session_state.app_data.get("quick_add_amounts", [250, 500, 750])
            new_quick_add_ml = []
            
            for i in range(3):
                current_val_display = get_display_amount(quick_add_ml[i])
                new_val_display = st.number_input(
                    f"Button {i+1} ({unit})",
                    min_value=1.0,
                    value=float(current_val_display),
                    step=10.0 if unit == 'ml' else 0.1,
                    key=f"quick_add_{i}",
                    format="%.0f" if unit == 'ml' else "%.1f"
                )
                new_quick_add_ml.append(convert_to_ml(new_val_display, unit))

            if new_quick_add_ml != quick_add_ml:
                st.session_state.app_data['quick_add_amounts'] = [int(v) for v in new_quick_add_ml]
                save_data(st.session_state.app_data)
                st.rerun()

        st.divider()
        st.header("⏰ Reminders")
        
        reminders_enabled = st.toggle("Enable Reminders", value=st.session_state.app_data.get('reminders_enabled', False))
        if reminders_enabled != st.session_state.app_data.get('reminders_enabled'):
            st.session_state.app_data['reminders_enabled'] = reminders_enabled
            save_data(st.session_state.app_data)
            st.rerun()

        sound_enabled = st.toggle("Enable Reminder Sound", value=st.session_state.app_data.get('reminder_sound_enabled', True))
        if sound_enabled != st.session_state.app_data.get('reminder_sound_enabled'):
            st.session_state.app_data['reminder_sound_enabled'] = sound_enabled
            save_data(st.session_state.app_data)
            st.rerun()

        reminder_interval = st.number_input("Interval (minutes)", min_value=1, value=st.session_state.app_data.get('reminder_interval', 60))
        if reminder_interval != st.session_state.app_data.get('reminder_interval'):
            st.session_state.app_data['reminder_interval'] = reminder_interval
            save_data(st.session_state.app_data)

        start_time_val = datetime.strptime(st.session_state.app_data.get('reminder_start_time', "09:00"), "%H:%M").time()
        reminder_start_time = st.time_input("Start Time", value=start_time_val)
        if reminder_start_time.strftime("%H:%M") != st.session_state.app_data.get('reminder_start_time'):
            st.session_state.app_data['reminder_start_time'] = reminder_start_time.strftime("%H:%M")
            save_data(st.session_state.app_data)

        end_time_val = datetime.strptime(st.session_state.app_data.get('reminder_end_time', "21:00"), "%H:%M").time()
        reminder_end_time = st.time_input("End Time", value=end_time_val)
        if reminder_end_time.strftime("%H:%M") != st.session_state.app_data.get('reminder_end_time'):
            st.session_state.app_data['reminder_end_time'] = reminder_end_time.strftime("%H:%M")
            save_data(st.session_state.app_data)

        st.divider()
        st.header("💾 Data Management")

        csv_data = generate_export_data()

        st.download_button(
           label="📥 Export Log to CSV",
           data=csv_data,
           file_name="water_tracker_log.csv",
           mime="text/csv",
           disabled=not csv_data,
           help="Download all your logged water intake as a CSV file."
        )


    # --- Main Page Content ---
    st.title("💧 Daily Water Tracker")
    st.markdown("Track your hydration journey, one sip at a time.")

    check_and_show_reminder()

    total_consumed_ml = get_daily_total()
    goal_reached_before = total_consumed_ml >= goal_ml

    display_progress_circle(total_consumed_ml, goal_ml)

    st.subheader("Log Your Intake")

    button_cols = st.columns([1, 1, 1])
    common_amounts_ml = st.session_state.app_data.get("quick_add_amounts", [250, 500, 750])

    for i, amount_ml in enumerate(common_amounts_ml):
        if button_cols[i].button(f"💧 {get_display_string(amount_ml)}"):
            log_water_intake(amount_ml)
            if not goal_reached_before and (total_consumed_ml + amount_ml) >= goal_ml:
                st.balloons()
            st.rerun()

    with st.form("add_water_form", clear_on_submit=True):
        custom_amount = st.number_input(f"Enter a custom amount ({unit})", min_value=0.1, step=0.1)
        submitted = st.form_submit_button("✅ Add Custom Amount")
        
        if submitted and custom_amount > 0:
            custom_amount_ml = convert_to_ml(custom_amount, unit)
            log_water_intake(custom_amount_ml)
            if not goal_reached_before and (total_consumed_ml + custom_amount_ml) >= goal_ml:
                st.balloons()
            st.rerun()

    with st.expander("📜 View Today's Log", expanded=True):
        today_log = st.session_state.app_data["log"].get(str(date.today()), [])
        if not today_log:
            st.info("No entries yet for today. Time to hydrate!")
        else:
            for entry in reversed(today_log):
                with st.container():
                    entry_amount_ml = entry['amount']
                    
                    if st.session_state.editing_timestamp == entry['timestamp']:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            current_edit_amount = get_display_amount(entry_amount_ml)
                            new_amount_display = st.number_input(
                                f"New amount ({unit})",
                                min_value=0.1,
                                value=float(current_edit_amount),
                                step=0.1,
                                key=f"input_{entry['timestamp']}",
                                format="%.1f"
                            )
                        with col2:
                            if st.button("💾", key=f"save_{entry['timestamp']}", help="Save changes"):
                                new_amount_ml = convert_to_ml(new_amount_display, unit)
                                update_log_entry(entry['timestamp'], new_amount_ml)
                                st.session_state.editing_timestamp = None
                                st.rerun()
                        with col3:
                            if st.button("✖️", key=f"cancel_{entry['timestamp']}", help="Cancel edit"):
                                st.session_state.editing_timestamp = None
                                st.rerun()
                    else:
                        col1, col2, col3 = st.columns([4, 1, 1])
                        with col1:
                            time_str = datetime.fromisoformat(entry['timestamp']).strftime('%I:%M %p')
                            st.markdown(f"""
                            <div class="log-text">💧 {get_display_string(entry_amount_ml)}</div>
                            <div class="log-time">at {time_str}</div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if st.button("✏️", key=f"edit_{entry['timestamp']}", help="Edit this entry"):
                                st.session_state.editing_timestamp = entry['timestamp']
                                st.rerun()
                        with col3:
                            if st.button("❌", key=f"delete_{entry['timestamp']}", help="Delete this entry"):
                                delete_log_entry(entry['timestamp'])
                                st.rerun()
    
    st.divider()
    st.subheader("📈 Your Progress (Last 7 Days)")

    log_data = st.session_state.app_data.get("log", {})
    history_df = get_historical_data(log_data, 7)

    if history_df.empty or history_df['Intake'].sum() == 0:
        st.info("Log your intake for a few days to see a chart of your progress here!")
    else:
        goal_display = get_display_amount(goal_ml)

        # Rename column for chart legend and convert values to display unit
        chart_df = history_df.copy()
        chart_df[f'Intake ({unit})'] = chart_df['Intake'].apply(get_display_amount)
        chart_df = chart_df.drop(columns=['Intake'])
        chart_df = chart_df.set_index('Date')

        st.bar_chart(chart_df)
        st.caption(f"Your daily goal is {int(goal_display)} {unit}.")

    st.divider()
    with st.expander("🏆 My Achievements"):
        unlocked_achs = [k for k, v in st.session_state.app_data.get("achievements", {}).items() if v.get("unlocked")]
        if not unlocked_achs:
            st.info("Keep hydrating to unlock achievements!")
        else:
            for ach_id in unlocked_achs:
                ach_details = ACHIEVEMENTS.get(ach_id)
                if ach_details:
                    st.markdown(f"**{ach_details['name']}**: {ach_details['description']}")