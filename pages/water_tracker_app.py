import streamlit as st
import json
import os
from datetime import datetime, date
import time

# --- Configuration ---
DATA_FILE = "water_tracker_data.json"

# --- UI Styling ---
st.set_page_config(
    page_title="daily water tracker",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for a beautiful, interactive, and mobile-friendly look
st.markdown("""
<style>
    /* Main background with a beautiful gradient */
    .main {
        background-image: linear-gradient(to right top, #6dd5ed, #2193b0);
        background-attachment: fixed;
    }
    /* Main content card with frosted glass effect */
    .st-emotion-cache-1y4p8pa {
        padding-top: 2rem;
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1.5rem;
        background-color: rgba(255, 255, 255, 0.7); /* Semi-transparent card */
        border-radius: 20px;
        backdrop-filter: blur(10px); /* Frosted glass effect */
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    /* Button styling for a modern look */
    .stButton>button {
        border-radius: 50px;
        background-color: #007bff;
        color: white;
        border: none;
        padding: 12px 28px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(0,123,255,0.3);
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,123,255,0.4);
    }
    .stButton>button:active {
        transform: translateY(1px);
    }
    /* Progress circle styling */
    .progress-circle {
        position: relative;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: conic-gradient(var(--fill-color) calc(var(--progress) * 1%), #dfeff7 0);
        display: grid;
        place-items: center;
        margin: 1rem auto 2rem auto;
        transition: background 0.5s;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
    }
    .progress-circle::before {
        content: '';
        position: absolute;
        width: 85%;
        height: 85%;
        background: #fff;
        border-radius: 50%;
    }
    .progress-text {
        position: relative;
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        color: #333;
    }
    .progress-subtext {
        position: relative;
        font-size: 1rem;
        color: #555;
    }
    /* Header styling */
    h1 {
        color: #004080;
    }
</style>
""", unsafe_allow_html=True)


# --- Data Handling Functions ---
def load_data():
    """Loads user data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {"goal": 2500, "units": "ml", "log": {}}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if data.get("units") != "ml": # Convert old data if necessary
                data["units"] = "ml"
                data["goal"] = 2500
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return {"goal": 2500, "units": "ml", "log": {}}

def save_data(data):
    """Saves user data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_water_intake(amount):
    """Logs a new water intake entry and saves it."""
    today_str = str(date.today())
    if today_str not in st.session_state.app_data["log"]:
        st.session_state.app_data["log"][today_str] = []
    
    st.session_state.app_data["log"][today_str].append({
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    })
    save_data(st.session_state.app_data)

def get_daily_total():
    """Calculates the total water intake for today."""
    today_str = str(date.today())
    today_log = st.session_state.app_data["log"].get(today_str, [])
    return sum(entry['amount'] for entry in today_log)

def delete_log_entry(timestamp_to_delete):
    """Deletes a specific water intake entry based on its timestamp."""
    today_str = str(date.today())
    today_log = st.session_state.app_data["log"].get(today_str, [])
    
    # Filter out the entry to be deleted
    updated_log = [entry for entry in today_log if entry["timestamp"] != timestamp_to_delete]
    
    if len(updated_log) < len(today_log):
        st.session_state.app_data["log"][today_str] = updated_log
        save_data(st.session_state.app_data)

def update_log_entry(timestamp_to_update, new_amount):
    """Updates the amount for a specific water intake entry."""
    today_str = str(date.today())
    today_log = st.session_state.app_data["log"].get(today_str, [])
    
    for entry in today_log:
        if entry["timestamp"] == timestamp_to_update:
            entry["amount"] = new_amount
            break
            
    st.session_state.app_data["log"][today_str] = today_log
    save_data(st.session_state.app_data)


# --- UI Components ---
def display_progress_circle(today_total, goal):
    """Renders the interactive progress circle."""
    progress = 0
    if goal > 0:
        progress = min((today_total / goal) * 100, 100)
    
    fill_color = "#2193b0" if progress < 100 else "#28a745"

    st.markdown(f"""
    <div class="progress-circle" style="--progress: {progress}; --fill-color: {fill_color};">
        <div class="progress-text">
            {progress:.0f}%
            <div class="progress-subtext">{today_total:,} / {goal:,} ml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- Main Application Logic ---

# Initialize session state from file
if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()
if 'editing_timestamp' not in st.session_state:
    st.session_state.editing_timestamp = None

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    current_goal = st.session_state.app_data.get("goal", 2500)
    new_goal = st.number_input(
        "Daily Goal (ml)", min_value=1.0, value=float(current_goal), step=50.0
    )
    if new_goal != current_goal:
        st.session_state.app_data['goal'] = new_goal
        save_data(st.session_state.app_data)
        st.rerun()

# --- Main Page Content ---
st.title("💧 daily water tracker")
st.markdown("Your simple and beautiful daily water tracker.")

# Calculate today's total and check against the goal
goal = st.session_state.app_data.get("goal", 2500)
total_consumed = get_daily_total()
goal_reached_before = total_consumed >= goal

# Display the main progress circle
display_progress_circle(total_consumed, goal)

st.subheader("Log Your Intake")

# Quick-add buttons for a highly interactive experience
button_cols = st.columns([1, 1, 1])
common_amounts = [250, 500, 750]

for i, amount in enumerate(common_amounts):
    if button_cols[i].button(f"💧 {amount} ml"):
        log_water_intake(amount)
        # Check if the goal was just reached for the celebration
        if not goal_reached_before and (total_consumed + amount) >= goal:
            st.balloons()
        st.rerun()

# Custom amount input form
with st.form("add_water_form", clear_on_submit=True):
    custom_amount = st.number_input("Enter a custom amount (ml)", min_value=1.0, step=10.0)
    submitted = st.form_submit_button("✅ Add Custom Amount")
    
    if submitted and custom_amount > 0:
        log_water_intake(custom_amount)
        if not goal_reached_before and (total_consumed + custom_amount) >= goal:
            st.balloons()
        st.rerun()

# Display today's entries with an expander
with st.expander("📜 View Today's Log", expanded=True):
    today_log = st.session_state.app_data["log"].get(str(date.today()), [])
    if not today_log:
        st.info("No entries yet for today. Time to hydrate!")
    else:
        for entry in reversed(today_log):
            # If this entry is the one being edited, show the edit UI
            if st.session_state.editing_timestamp == entry['timestamp']:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    new_amount = st.number_input(
                        "New amount",
                        min_value=1.0,
                        value=float(entry['amount']),
                        step=10.0,
                        key=f"input_{entry['timestamp']}"
                    )
                with col2:
                    if st.button("💾", key=f"save_{entry['timestamp']}", help="Save changes"):
                        update_log_entry(entry['timestamp'], new_amount)
                        st.session_state.editing_timestamp = None
                        st.rerun()
                with col3:
                    if st.button("✖️", key=f"cancel_{entry['timestamp']}", help="Cancel edit"):
                        st.session_state.editing_timestamp = None
                        st.rerun()
            else:
                # Otherwise, show the normal log entry
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    time_str = datetime.fromisoformat(entry['timestamp']).strftime('%I:%M %p')
                    st.markdown(f"- **{entry['amount']} ml** at `{time_str}`")
                with col2:
                    if st.button("✏️", key=f"edit_{entry['timestamp']}", help="Edit this entry"):
                        st.session_state.editing_timestamp = entry['timestamp']
                        st.rerun()
                with col3:
                    if st.button("❌", key=f"delete_{entry['timestamp']}", help="Delete this entry"):
                        delete_log_entry(entry['timestamp'])
                        st.rerun()
