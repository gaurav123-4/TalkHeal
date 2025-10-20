import streamlit as st
from core.water_tracker import log_water_intake, get_today_total, get_last_n_days_totals, get_today_entries, load_water_log, edit_water_intake_entry, delete_water_intake_entry
import pandas as pd
import datetime

st.set_page_config(page_title="Water Intake Tracker", page_icon="💧", layout="centered")
# Custom CSS for enhanced visuals
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Card-like containers */
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    /* Title styling */
    h1 {
        color: black !important;  /* Plain black text */
        background: none !important;  /* Remove gradient background */
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #0d47a1;
        font-weight: 700;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #42a5f5, #1976d2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2, #0d47a1);
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
        transform: translateY(-2px);
    }
    
    /* Number input styling */
    .stNumberInput > div > input {
        border-radius: 15px;
        border: 2px solid #42a5f5;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        background: white;
    }
    
    /* Number input label */
    .stNumberInput label {
        color: #1976d2 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Dark mode text fixes */
    @media (prefers-color-scheme: dark) {
        .stNumberInput label {
            color: #64b5f6 !important;
        }
        
        .stSuccess {
            background: linear-gradient(135deg, #66bb6a, #43a047) !important;
            color: white !important;
            border-radius: 15px;
            padding: 1rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        .stSuccess * {
            color: white !important;  /* Ensure all child elements have white text */
        }
        
        .stCaption, .stCaption p {
            color: #e0e0e0 !important;
        }
    }

    /* Additional styles for Streamlit's dark mode UI */
    body.streamlit-dark .stNumberInput label {
        color: #64b5f6 !important;
    }

    body.streamlit-dark .stSuccess {
        background: linear-gradient(135deg, #66bb6a, #43a047) !important;
        color: white !important;
        border-radius: 15px;
        padding: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }

    body.streamlit-dark .stSuccess * {
        color: white !important;  /* Ensure all child elements have white text */
    }

    body.streamlit-dark .stCaption,
    body.streamlit-dark .stCaption p {
        color: #e0e0e0 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1976d2;
        text-align: center;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0d47a1;
        text-align: center;
    }
    
    /* Success message styling (common styles) */
    .stSuccess {
        background: linear-gradient(135deg, #66bb6a, #43a047) !important;
        color: white !important;
        border-radius: 15px;
        padding: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .stSuccess * {
        color: white !important;
    }
    
    /* Bar chart container */
    [data-testid="stArrowVegaLiteChart"] {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Column containers (fixed data-testid selector) */
    [data-testid="stColumn"] {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }

    /* --- Dark Mode Enhancements --- */
    body.streamlit-dark .stApp {
        background: linear-gradient(135deg, #1e2a38 0%, #273443 100%);
    }

    body.streamlit-dark h1 {
        color: #e1eef9 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }

    body.streamlit-dark h2, body.streamlit-dark h3, body.streamlit-dark h4 {
        color: #8ab4f8; /* A lighter, more vibrant blue for dark mode */
    }

    body.streamlit-dark [data-testid="stMetricValue"] {
        color: #8ab4f8;
    }

    body.streamlit-dark [data-testid="stMetricLabel"] {
        color: #b0c4de;
    }

    body.streamlit-dark [data-testid="stColumn"] {
        background: #2c3e50; /* Darker, muted blue-gray */
        border: 1px solid #3a4b5c;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    body.streamlit-dark [data-testid="stArrowVegaLiteChart"] {
        background: #2c3e50;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #3a4b5c;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    /* Making chart text readable in dark mode */
    body.streamlit-dark .vega-embed .mark-text text {
        fill: #e1eef9;
    }
    body.streamlit-dark .vega-embed .axis-title {
        fill: #b0c4de;
    }
    body.streamlit-dark .vega-embed .axis-label {
        fill: #b0c4de;
    }
</style>
""", unsafe_allow_html=True)
# Header with animated water drop
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <div style="font-size: 4rem; animation: float 3s ease-in-out infinite;">💧</div>
</div>
<style>
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
</style>
""", unsafe_allow_html=True)
st.title("Water Intake Tracker")
st.markdown("""
<div style='text-align: center; font-size: 1.2rem; color: #424242; margin-bottom: 2rem; 
            background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 15px;'>
    <b>Easily log your water intake and track your daily progress.</b><br>
    <span style='color: #1976d2;'>Staying hydrated is key to wellness!</span>
</div>
""", unsafe_allow_html=True)

# 1. Customizable Daily Goal
if "daily_water_goal" not in st.session_state:
    st.session_state.daily_water_goal = 2000  # Default goal

goal = st.number_input(
    "🎯 Set Your Daily Goal (ml)",
    min_value=100,
    max_value=10000,
    value=st.session_state.daily_water_goal,
    step=100,
    help="Set your personal daily water intake goal."
)
st.session_state.daily_water_goal = goal  # Update session state

col1, col2 = st.columns([2, 1], gap="large")
with col1:
    st.markdown("<div style='margin-bottom: 1rem;'>", unsafe_allow_html=True)
    amount = st.number_input("💦 Enter amount (ml)", min_value=50, max_value=2000, value=250, step=50)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🌊 Log Water Intake", use_container_width=True):
        current_total = get_today_total()
        log_water_intake(amount)
        st.success(f"✨ Logged {amount} ml of water!")
        
        if current_total < goal and (current_total + amount) >= goal:
            st.balloons()
            st.markdown("""
            <div style='background: linear-gradient(135deg, #ffd700, #ffed4e); 
                        padding: 1rem; border-radius: 15px; text-align: center; 
                        font-weight: 700; font-size: 1.3rem; color: #d84315;
                        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); margin-top: 1rem;'>
                🎉 Congratulations! You've reached your daily goal! 🎉
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center; margin-top: 1rem; color: #0d47a1;'>Or use a quick-add button:</h4>", unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    if q1.button("Glass (250ml)", use_container_width=True):
        log_water_intake(250)
        st.success("✨ Logged 250 ml of water!")

    if q2.button("Bottle (500ml)", use_container_width=True):
        log_water_intake(500)
        st.success("✨ Logged 500 ml of water!")

    if q3.button("Bottle (1L)", use_container_width=True):
        log_water_intake(1000)
        st.success("✨ Logged 1000 ml of water!")

with col2:
    st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>Today's Total</h3>", unsafe_allow_html=True)
    total = get_today_total()
    st.metric(label="Total (ml)", value=total)
    
    progress = min(total / goal, 1.0)
    
    # Enhanced progress bar with gradient and animation
    if progress >= 1.0:
        color = "linear-gradient(135deg, #2ecc71, #27ae60)"
        glow = "0 0 20px rgba(46, 204, 113, 0.6)"
    elif progress > 0.6:
        color = "linear-gradient(135deg, #f39c12, #e67e22)"
        glow = "0 0 15px rgba(243, 156, 18, 0.4)"
    else:
        color = "linear-gradient(135deg, #e74c3c, #c0392b)"
        glow = "0 0 15px rgba(231, 76, 60, 0.4)"
    
    st.markdown(f"""
    <div style="background: #e3f2fd; border-radius: 15px; height: 30px; width: 100%; 
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.1); position: relative; overflow: hidden;">
        <div style="background: {color}; border-radius: 15px; height: 100%; width: {progress*100}%; 
                    box-shadow: {glow}; transition: width 0.5s ease, box-shadow 0.5s ease;
                    position: relative;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                        animation: shimmer 2s infinite;"></div>
        </div>
    </div>
    <style>
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
    </style>
    <div style='text-align:center; margin-top: 0.5rem; font-weight: 600; font-size: 1.1rem; color: #0d47a1;'>
        {total} / {goal} ml ({int(progress*100)}%)
    </div>
    """, unsafe_allow_html=True)
def get_personalized_tip(daily_goal, last_7_days_data):
    # Default tip
    tip = "💡 Tip: Aim for at least 2 liters (2000 ml) per day!"

    if not last_7_days_data:
        return "💡 Tip: Start logging your water intake to get personalized tips!"

    # Calculate average intake and consistency
    total_intake = sum(day[1] for day in last_7_days_data)
    days_logged = len(last_7_days_data)
    average_intake = total_intake / days_logged if days_logged > 0 else 0
    
    days_met_goal = sum(1 for day in last_7_days_data if day[1] >= daily_goal)

    # Provide tips based on user's recent performance
    if days_logged < 3:
        tip = "💡 Tip: Keep logging for a few more days to unlock more insightful tips!"
    elif days_met_goal >= 5:
        tip = "🏆 You're doing great! Keep up the consistent hydration to maintain your energy levels."
    elif average_intake < daily_goal / 2:
        tip = "💧 Tip: Try starting your day with a large glass of water to kickstart your hydration."
    elif average_intake < daily_goal:
        tip = "📈 You're getting close! Try carrying a reusable water bottle as a visual reminder to drink more."
    elif days_met_goal == 7:
        tip = "🥇 Perfect week! You've mastered the art of staying hydrated. Keep it up!"

    return tip

# ... (rest of the app)

st.markdown(f"""
...
<div style='text-align:center; margin-top: 0.5rem; font-weight: 600; font-size: 1.1rem; color: #0d47a1;'>
    {total} / {goal} ml ({int(progress*100)}%)
</div>
""", unsafe_allow_html=True)

# Personalized Hydration Tip
last_7_days_data = get_last_n_days_totals(7)
personalized_tip = get_personalized_tip(goal, last_7_days_data)
st.caption(personalized_tip)


# 2. Detailed Log View with Edit/Delete
with st.expander("📜 Today's Log", expanded=False):
    todays_entries = get_today_entries()
    if not todays_entries:
        st.info("No water logged yet today. Start tracking!")
    else:
        # Sort entries by timestamp descending
        todays_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        
        for entry in todays_entries:
            ts = entry['timestamp']
            amount = entry['amount_ml']
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{pd.to_datetime(ts).strftime('%I:%M %p')}**: {amount} ml")

            with col2:
                if st.button("Delete", key=f"delete_{ts}"):
                    delete_water_intake_entry(ts)
                    st.rerun()

            with col3:
                edit_key = f"edit_{ts}"
                if edit_key not in st.session_state:
                    st.session_state[edit_key] = False

                if st.button("Edit", key=f"edit_btn_{ts}"):
                    st.session_state[edit_key] = not st.session_state[edit_key]

            if st.session_state[edit_key]:
                new_amount = st.number_input("New Amount (ml)", value=amount, key=f"num_{ts}")
                if st.button("Save", key=f"save_{ts}"):
                    edit_water_intake_entry(ts, new_amount)
                    st.session_state[edit_key] = False
                    st.rerun()

# Analytics and Trends
with st.expander("📈 Analytics and Trends", expanded=False):
    st.markdown("""
    <div style='margin: 1rem 0; text-align: center;'>
        <div style='font-size: 1.5rem; font-weight: 700; color: #0d47a1;'>
            Last 7 Days Progress (Bar Chart)
        </div>
    </div>
    """, unsafe_allow_html=True)
    days_data_7 = get_last_n_days_totals(7)
    df_7 = pd.DataFrame(days_data_7, columns=["Date", "Water (ml)"])
    st.bar_chart(df_7.set_index("Date"), height=250, use_container_width=True)

    st.markdown("""
    <div style='margin: 2rem 0 1rem 0; text-align: center;'>
        <div style='font-size: 1.5rem; font-weight: 700; color: #0d47a1;'>
            Last 30 Days Trend (Line Chart)
        </div>
    </div>
    """, unsafe_allow_html=True)
    days_data_30 = get_last_n_days_totals(30)
    df_30 = pd.DataFrame(days_data_30, columns=["Date", "Water (ml)"])
    st.line_chart(df_30.set_index("Date"), height=250, use_container_width=True)

# Data Export Functionality
with st.expander("📥 Export Your Data", expanded=False):
    st.markdown("""
    <p style='font-size: 1.1rem; color: #424242;'>
        Download your entire water intake history as a CSV file. This can be useful for personal records or for sharing with a healthcare provider.
    </p>
    """, unsafe_allow_html=True)

    if st.button("Generate CSV for Download", key="export_data"):
        water_data = load_water_log()
        if not water_data:
            st.warning("No water intake data found to export.")
        else:
            all_entries = []
            for date, entries in water_data.items():
                for entry in entries:
                    all_entries.append({
                        "Date": date,
                        "Time": pd.to_datetime(entry['timestamp']).strftime('%I:%M:%S %p'),
                        "Amount (ml)": entry['amount_ml']
                    })
            
            if all_entries:
                export_df = pd.DataFrame(all_entries)
                # Sort by date and time
                export_df = export_df.sort_values(by=["Date", "Time"], ascending=[False, False])
                
                csv = export_df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"water_intake_history_{datetime.date.today().isoformat()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No entries found to export.")
# Footer with encouraging message
st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding: 1.5rem; 
            background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(13, 71, 161, 0.1)); 
            border-radius: 20px; border: 2px solid rgba(33, 150, 243, 0.3);'>
    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>💪</div>
    <div style='font-size: 1.2rem; font-weight: 600; color: #0d47a1;'>
        Keep up the great work!
    </div>
    <div style='color: #424242; margin-top: 0.5rem;'>
        Every drop counts towards a healthier you
    </div>
</div>
""", unsafe_allow_html=True)