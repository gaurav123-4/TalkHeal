import streamlit as st
from core.water_tracker import log_water_intake, get_today_total, get_last_n_days_totals
import pandas as pd

st.set_page_config(page_title="Water Intake Tracker", page_icon="💧", layout="centered")
st.title("💧 Water Intake Tracker")

st.markdown("""
Easily log your water intake and track your daily progress. Staying hydrated is key to wellness!
""")

goal = 2000  # Define goal for reuse

col1, col2 = st.columns([2, 1])

with col1:
    amount = st.number_input("Enter amount (ml)", min_value=50, max_value=2000, value=250, step=50)
    if st.button("Log Water Intake", use_container_width=True):
        current_total = get_today_total()
        log_water_intake(amount)
        st.success(f"Logged {amount} ml of water!")
        # --- UI/UX Enhancement: Celebrate reaching the goal ---
        if current_total < goal and (current_total + amount) >= goal:
            st.balloons()

with col2:
    st.subheader("Today's Total")
    total = get_today_total()
    st.metric(label="Total (ml)", value=total)

    # --- UI/UX Enhancement: Colored Progress Bar ---
    progress = min(total / goal, 1.0)

    # Determine color based on progress
    if progress >= 1.0:
        color = "#2a9d8f"  # Green
    elif progress > 0.6:
        color = "#e9c46a"  # Yellow
    else:
        color = "#f4a261"  # Orange

    # Custom HTML for the progress bar
    st.markdown(f"""
    <div style="background: #F0F2F6; border-radius: 10px; height: 25px; width: 100%;">
        <div style="background: {color}; border-radius: 10px; height: 100%; width: {progress*100}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-top:4px;'>{total} / {goal} ml (Goal)</div>", unsafe_allow_html=True)

st.caption("Tip: Aim for at least 2 liters (2000 ml) per day!")

# --- 7-day water intake graph ---
st.markdown("<div style='margin:1.2em 0 0.2em 0; font-size:1.08em; color:#0096c7; text-align:center;'><b>Last 7 Days</b></div>", unsafe_allow_html=True)
days_data = get_last_n_days_totals(7)
df = pd.DataFrame(days_data, columns=["Date", "Water (ml)"])
st.bar_chart(df.set_index("Date"), height=220, use_container_width=True)