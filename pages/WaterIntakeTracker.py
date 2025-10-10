import streamlit as st
from core.water_tracker import log_water_intake, get_today_total, get_last_n_days_totals
import pandas as pd
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
st.caption("💡 Tip: Aim for at least 2 liters (2000 ml) per day!")
# 7-day water intake graph with enhanced styling
st.markdown("""
<div style='margin: 2rem 0 1rem 0; text-align: center;'>
    <div style='font-size: 2rem; font-weight: 700; color: #0d47a1; 
                background: white; padding: 1rem; border-radius: 15px; 
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);'>
        📊 Last 7 Days Progress
    </div>
</div>
""", unsafe_allow_html=True)
days_data = get_last_n_days_totals(7)
df = pd.DataFrame(days_data, columns=["Date", "Water (ml)"])
st.bar_chart(df.set_index("Date"), height=250, use_container_width=True)
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