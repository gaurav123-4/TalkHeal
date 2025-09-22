import streamlit as st
import time

def breathing_exercise():
    st.markdown("<h2 style='text-align: center; color: teal;'>🧘 Breathing Exercise</h2>", unsafe_allow_html=True)

    st.markdown("### 👇 Follow the animation to breathe in and out")
    st.write("Use this simple breathing exercise to relax. Follow the circle expanding and contracting.")

    # The animation is now synced with the breathing pattern (4s in, 2s hold, 4s out)
    circle_animation = """
    <style>
    @keyframes breathe {
      0% { transform: scale(0.8); }
      40% { transform: scale(1.2); }
      60% { transform: scale(1.2); }
      100% { transform: scale(0.8); }
    }

    .breathing-circle {
      margin: auto;
      margin-top: 50px;
      height: 150px;
      width: 150px;
      border-radius: 50%;
      background-color: #90e0ef;
      animation: breathe 10s ease-in-out infinite;
    }
    </style>

    <div class="breathing-circle"></div>
    """
    st.markdown(circle_animation, unsafe_allow_html=True)

    st.write("") # Spacer

    with st.expander("🕒 Set a Timer for Your Session", expanded=True):
        minutes = st.slider("How many minutes do you want to do this?", 1, 15, 2)
        
        if st.button("Start Session"):
            st.success("Session started! Relax and follow the animation and prompts...")
            
            timer_placeholder = st.empty()
            breath_text_placeholder = st.empty()
            
            total_seconds = minutes * 60
            inhale_duration = 4
            hold_duration = 2
            exhale_duration = 4
            cycle_length = inhale_duration + hold_duration + exhale_duration

            for i in range(total_seconds, 0, -1):
                # Timer logic
                mins, secs = divmod(i, 60)
                timer_text = f"{mins:02d}:{secs:02d}"
                timer_placeholder.markdown(f"<h2 style='text-align: center;'>⏳ {timer_text}</h2>", unsafe_allow_html=True)

                # Breathing guidance logic
                elapsed_seconds = total_seconds - i
                phase_time = elapsed_seconds % cycle_length

                if 0 <= phase_time < inhale_duration:
                    breath_text_placeholder.markdown("<h3 style='text-align: center;'>🌬️ Breathe In...</h3>", unsafe_allow_html=True)
                elif inhale_duration <= phase_time < (inhale_duration + hold_duration):
                    breath_text_placeholder.markdown("<h3 style='text-align: center;'>✋ Hold...</h3>", unsafe_allow_html=True)
                else:
                    breath_text_placeholder.markdown("<h3 style='text-align: center;'>😮‍💨 Breathe Out...</h3>", unsafe_allow_html=True)

                time.sleep(1)

            timer_placeholder.empty()
            breath_text_placeholder.markdown("<h3 style='text-align: center;'>✅ Session complete! Well done.</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    breathing_exercise()
