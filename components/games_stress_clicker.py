import streamlit as st
import random
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

def stress_relief_clicker_game():
    """Complete Stress Relief Clicker Game for anxiety management and instant stress relief"""
    
    st.markdown("### 😌 Stress Relief Clicker Game")
    st.markdown("**Click to release stress and tension - Each click brings more peace!**")
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Games", key="back_stress"):
            st.rerun()
    
    # Initialize game state
    if "clicker_count" not in st.session_state:
        st.session_state.clicker_count = 0
    if "clicker_start_time" not in st.session_state:
        st.session_state.clicker_start_time = None
    if "stress_level" not in st.session_state:
        st.session_state.stress_level = 100
    if "relaxation_level" not in st.session_state:
        st.session_state.relaxation_level = 0
    if "daily_clicks" not in st.session_state:
        st.session_state.daily_clicks = 0
    if "affirmation_shown" not in st.session_state:
        st.session_state.affirmation_shown = False
    if "breathing_prompt" not in st.session_state:
        st.session_state.breathing_prompt = False
    
    # Stress level categories with colors and descriptions
    stress_levels = [
        (0, 20, "😌 Completely Relaxed", "#4CAF50", "You're in a state of deep calm and tranquility"),
        (21, 40, "😊 Very Calm", "#8BC34A", "Feeling peaceful and centered"),
        (41, 60, "🙂 Moderately Relaxed", "#CDDC39", "Stress is melting away nicely"),
        (61, 80, "😐 Getting Better", "#FFEB3B", "You're making good progress"),
        (81, 90, "😅 Still Tense", "#FF9800", "Keep clicking - relief is coming!"),
        (91, 100, "😰 Very Stressed", "#FF5722", "Take deep breaths and keep clicking")
    ]
    
    # Find current stress state
    current_state = next((state for min_s, max_s, state, color, desc in stress_levels 
                         if min_s <= st.session_state.stress_level <= max_s), 
                        ("😌 Completely Relaxed", "#4CAF50", "Perfect state of calm"))
    
    current_color = next((color for min_s, max_s, state, color, desc in stress_levels 
                         if min_s <= st.session_state.stress_level <= max_s), "#4CAF50")
    
    current_desc = next((desc for min_s, max_s, state, color, desc in stress_levels 
                        if min_s <= st.session_state.stress_level <= max_s), "Perfect calm")
    
    # Display current stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h4>Total Clicks</h4>
            <h2>{st.session_state.clicker_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {current_color} 0%, {current_color}99 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h4>Stress Level</h4>
            <h2>{st.session_state.stress_level}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        relaxation_color = "#4CAF50" if st.session_state.relaxation_level > 70 else "#8BC34A" if st.session_state.relaxation_level > 40 else "#FFC107"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {relaxation_color} 0%, {relaxation_color}99 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h4>Relaxation</h4>
            <h2>{st.session_state.relaxation_level}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.session_state.clicker_start_time:
            session_time = (datetime.now() - st.session_state.clicker_start_time).seconds
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                <h4>Session Time</h4>
                <h2>{session_time}s</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                <h4>Session Time</h4>
                <h2>0s</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Current state display
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {current_color} 0%, {current_color}aa 100%); 
                padding: 1.5rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;">
        <h2>{current_state}</h2>
        <p style="font-size: 1.1rem; margin: 0;">{current_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Game instructions (show only at start)
    if st.session_state.clicker_count == 0:
        st.markdown("""
        ### 📖 How to Use Stress Relief Clicker:
        1. **Click the stress ball** below to release tension
        2. **Focus on your breathing** while clicking
        3. **Let each click represent** letting go of worry
        4. **Watch your stress level decrease** and relaxation increase
        5. **Read the affirmations** that appear to boost positivity
        
        ### 🧘‍♀️ Mental Health Benefits:
        - **Immediate Stress Relief:** Physical action helps release tension
        - **Mindful Focus:** Concentrated clicking promotes present-moment awareness  
        - **Anxiety Reduction:** Repetitive action can calm racing thoughts
        - **Positive Reinforcement:** Affirmations boost self-esteem and confidence
        - **Breathing Regulation:** Prompts help establish healthy breathing patterns
        """)
    
    # Main stress relief button
    st.markdown("### 🎈 Click the Stress Ball to Release Tension:")
    
    # Stress ball visual that changes size based on stress level
    ball_size = max(80, 180 - (st.session_state.clicker_count // 5))
    ball_emoji = "🔴" if st.session_state.stress_level > 70 else "🟠" if st.session_state.stress_level > 40 else "🟡" if st.session_state.stress_level > 20 else "🟢"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"{ball_emoji}", key="stress_ball", 
                    help="Click me to release stress and tension!",
                    use_container_width=True):
            
            # Start timing if first click
            if st.session_state.clicker_start_time is None:
                st.session_state.clicker_start_time = datetime.now()
            
            # Update counters
            st.session_state.clicker_count += 1
            st.session_state.daily_clicks += 1
            
            # Decrease stress and increase relaxation
            stress_reduction = random.randint(2, 5)
            st.session_state.stress_level = max(0, st.session_state.stress_level - stress_reduction)
            st.session_state.relaxation_level = min(100, st.session_state.relaxation_level + stress_reduction)
            
            # Show positive affirmations periodically
            if st.session_state.clicker_count % 8 == 0:
                affirmations = [
                    "🌟 You are releasing tension with each click!",
                    "❄️ Feel the stress melting away like ice in sunshine!",
                    "🧘‍♀️ You are in control of your inner peace!", 
                    "🌊 Each click brings waves of calm to your mind!",
                    "💪 You are stronger than your stress and anxiety!",
                    "🌸 Breathe deeply and let go of all worries!",
                    "✨ You deserve peace, calm, and happiness!",
                    "🦋 Watch your worries transform into lightness!",
                    "🌈 You are creating space for joy and serenity!",
                    "💎 Your inner strength shines brighter than any stress!"
                ]
                
                chosen_affirmation = random.choice(affirmations)
                st.success(chosen_affirmation)
                st.session_state.affirmation_shown = True
            
            # Breathing prompts every 15 clicks
            if st.session_state.clicker_count % 15 == 0:
                breathing_prompts = [
                    "🫁 Take a deep breath in... hold for 3 seconds... and slowly exhale...",
                    "🌬️ Breathe in calm energy... breathe out all tension and worry...", 
                    "💨 Inhale peace and serenity... exhale stress and anxiety...",
                    "🍃 Let your breath flow naturally... feel your body relaxing...",
                    "🌊 Breathe like gentle ocean waves... in and out... calm and steady..."
                ]
                
                chosen_prompt = random.choice(breathing_prompts)
                st.info(chosen_prompt)
                st.session_state.breathing_prompt = True
            
            # Special achievements
            if st.session_state.clicker_count == 25:
                st.balloons()
                st.success("🎉 Amazing! You've reached 25 clicks of calm! Your dedication to wellness is inspiring!")
            
            elif st.session_state.clicker_count == 50:
                st.balloons()
                st.success("🌟 Incredible! 50 clicks of stress relief! You're building wonderful self-care habits!")
            
            elif st.session_state.clicker_count == 100:
                st.balloons()
                st.success("👑 Stress Relief Champion! 100 clicks of pure relaxation! You've mastered this technique!")
            
            elif st.session_state.stress_level == 0:
                st.balloons()
                st.success("🧘‍♀️ Perfect! You've achieved complete calm! Your mind is now at peace!")
            
            st.rerun()
    
    # Progress visualization
    if st.session_state.clicker_count > 0:
        
        # Stress level gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = st.session_state.stress_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Current Stress Level"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': current_color},
                'steps': [
                    {'range': [0, 25], 'color': "lightgreen"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"}, 
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "darkgreen", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            }
        ))
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress bars
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Stress Reduction Progress:**")
            stress_progress = (100 - st.session_state.stress_level) / 100
            st.progress(stress_progress, f"Stress Relief: {100 - st.session_state.stress_level}%")
        
        with col2:
            st.markdown("**Relaxation Achievement:**")
            st.progress(st.session_state.relaxation_level / 100, f"Relaxation: {st.session_state.relaxation_level}%")
    
    # Session statistics
    if st.session_state.clicker_start_time and st.session_state.clicker_count > 0:
        session_duration = (datetime.now() - st.session_state.clicker_start_time).seconds
        if session_duration > 0:
            clicks_per_minute = (st.session_state.clicker_count / session_duration) * 60
            
            st.markdown("### 📊 Session Statistics:")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Clicks Per Minute", f"{clicks_per_minute:.1f}")
            
            with col2:
                stress_reduced = 100 - st.session_state.stress_level
                st.metric("Stress Reduced", f"{stress_reduced}%")
            
            with col3:
                efficiency = (stress_reduced / st.session_state.clicker_count) * 100 if st.session_state.clicker_count > 0 else 0
                st.metric("Relief Efficiency", f"{efficiency:.1f}%")
    
    # Control buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reset Session", key="reset_clicker"):
            st.session_state.clicker_count = 0
            st.session_state.clicker_start_time = None
            st.session_state.stress_level = 100
            st.session_state.relaxation_level = 0
            st.session_state.affirmation_shown = False
            st.session_state.breathing_prompt = False
            st.success("Session reset! Ready for a fresh start!")
            st.rerun()
    
    with col2:
        if st.button("🧘‍♀️ Quick Meditation", key="meditation_prompt"):
            st.info("""
            🧘‍♀️ **1-Minute Meditation Break:**
            
            Close your eyes... Take a deep breath in through your nose for 4 counts... 
            Hold for 4 counts... Exhale through your mouth for 6 counts...
            
            Feel your body relaxing... Your shoulders dropping... Your jaw unclenching...
            You are safe... You are calm... You are at peace...
            
            When you're ready, open your eyes and continue clicking for more relief! 🌟
            """)
    
    with col3:
        if st.button("💡 Stress Management Tips", key="stress_tips"):
            tips = [
                "🌿 Practice deep breathing exercises throughout the day",
                "🚶‍♀️ Take regular walking breaks to clear your mind", 
                "💧 Stay hydrated - dehydration increases stress hormones",
                "😴 Prioritize 7-8 hours of quality sleep each night",
                "📱 Take breaks from screens and social media",
                "🎵 Listen to calming music or nature sounds",
                "📝 Write down your worries to externalize them",
                "🤗 Connect with supportive friends and family"
            ]
            
            random_tip = random.choice(tips)
            st.info(f"**Daily Stress Management Tip:**\n\n{random_tip}")
    
    # Achievement badges
    if st.session_state.clicker_count > 0:
        st.markdown("### 🏆 Achievement Progress:")
        
        badges = [
            (10, "🌱 Stress Buster Beginner", "Taking the first steps toward calm"),
            (25, "🌸 Relaxation Explorer", "Building healthy stress relief habits"),
            (50, "🌟 Calm Achiever", "Showing dedication to mental wellness"),
            (75, "🧘‍♀️ Mindfulness Master", "Developing excellent self-care skills"),
            (100, "👑 Zen Champion", "Achieved expert level stress management!")
        ]
        
        earned_badges = [badge for threshold, badge, desc in badges if st.session_state.clicker_count >= threshold]
        upcoming_badge = next((badge for threshold, badge, desc in badges if st.session_state.clicker_count < threshold), None)
        
        if earned_badges:
            st.markdown("**🎖️ Badges Earned:**")
            for badge in earned_badges:
                st.success(f"{badge}")
        
        if upcoming_badge:
            threshold, badge, desc = upcoming_badge
            progress_to_next = (st.session_state.clicker_count / threshold) * 100
            st.markdown(f"**🎯 Next Badge:** {badge}")
            st.progress(progress_to_next / 100, f"{st.session_state.clicker_count}/{threshold} clicks to {badge}")

# Simple wrapper to show just the game
def show_games_page():
    """Show Stress Relief Clicker Game only"""
    
    # Header
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #ff69b4; font-family: 'Baloo 2', cursive;">😌 Stress Relief Clicker</h1>
        <p style="color: #ffb6d5; font-size: 1.2rem;">Click away your stress and anxiety</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the stress clicker game directly
    stress_relief_clicker_game()

if __name__ == "__main__":
    show_games_page()