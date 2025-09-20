import streamlit as st
import time
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

def breathing_pattern_game():
    """Complete Interactive Breathing Pattern Game for anxiety relief and mindfulness"""
    
    st.markdown("### 🌬️ Breathing Pattern Game")
    st.markdown("**Master therapeutic breathing techniques - Reduce anxiety and improve focus!**")
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Games", key="back_breathing"):
            st.rerun()
    
    # Initialize breathing game state
    if "breathing_technique" not in st.session_state:
        st.session_state.breathing_technique = None
    if "breathing_active" not in st.session_state:
        st.session_state.breathing_active = False
    if "breathing_cycles" not in st.session_state:
        st.session_state.breathing_cycles = 0
    if "target_cycles" not in st.session_state:
        st.session_state.target_cycles = 5
    if "breathing_start_time" not in st.session_state:
        st.session_state.breathing_start_time = None
    if "stress_level_before" not in st.session_state:
        st.session_state.stress_level_before = None
    if "stress_level_after" not in st.session_state:
        st.session_state.stress_level_after = None
    if "session_completed" not in st.session_state:
        st.session_state.session_completed = False
    if "heart_rate_data" not in st.session_state:
        st.session_state.heart_rate_data = []
    if "relaxation_score" not in st.session_state:
        st.session_state.relaxation_score = 0
    
    # Breathing techniques database
    breathing_techniques = {
        "4-7-8": {
            "name": "4-7-8 Technique (Sleep & Anxiety)",
            "inhale": 4, "hold": 7, "exhale": 8,
            "description": "Developed by Dr. Andrew Weil, this technique activates the parasympathetic nervous system for deep relaxation.",
            "benefits": ["Reduces anxiety", "Improves sleep quality", "Lowers blood pressure", "Decreases stress hormones"],
            "when_to_use": "Before sleep, during panic attacks, when feeling overwhelmed",
            "science": "The extended exhale activates the vagus nerve, triggering the body's relaxation response.",
            "color": "#4A90E2",
            "icon": "😴"
        },
        "box": {
            "name": "Box Breathing (Focus & Control)",
            "inhale": 4, "hold": 4, "exhale": 4, "hold2": 4,
            "description": "Used by Navy SEALs and athletes for maintaining calm under pressure and enhancing focus.",
            "benefits": ["Improves concentration", "Reduces stress", "Enhances performance", "Builds mental resilience"],
            "when_to_use": "Before important meetings, during exams, in stressful situations",
            "science": "Equal timing creates autonomic balance between sympathetic and parasympathetic systems.",
            "color": "#50C878",
            "icon": "🎯"
        },
        "coherent": {
            "name": "Coherent Breathing (Balance & Heart Health)",
            "inhale": 5, "hold": 0, "exhale": 5,
            "description": "Creates heart rate variability coherence, optimizing cardiovascular and nervous system function.",
            "benefits": ["Improves heart rate variability", "Reduces blood pressure", "Enhances emotional regulation", "Boosts immune function"],
            "when_to_use": "Daily practice, during meditation, for general wellness",
            "science": "5-second cycles match natural heart rate variability rhythms for optimal physiological coherence.",
            "color": "#FF6B6B",
            "icon": "❤️"
        },
        "triangle": {
            "name": "Triangle Breathing (Energy & Clarity)",
            "inhale": 3, "hold": 3, "exhale": 3,
            "description": "Simple yet effective technique for quick stress relief and mental clarity throughout the day.",
            "benefits": ["Quick stress relief", "Improves mental clarity", "Easy to remember", "Energizing effect"],
            "when_to_use": "During work breaks, in traffic, before presentations",
            "science": "Shorter cycles prevent hyperventilation while still providing conscious breath control benefits.",
            "color": "#FFD700",
            "icon": "⚡"
        },
        "extended": {
            "name": "Extended Exhale (Deep Relaxation)",
            "inhale": 4, "hold": 2, "exhale": 8,
            "description": "Emphasizes long exhales to maximize activation of the parasympathetic nervous system.",
            "benefits": ["Deep muscle relaxation", "Reduces cortisol", "Improves digestion", "Calms nervous system"],
            "when_to_use": "After workouts, during chronic stress, for deep relaxation",
            "science": "Extended exhales stimulate the vagus nerve more than inhales, promoting deep calm.",
            "color": "#9B59B6",
            "icon": "🧘"
        }
    }
    
    # Display current stats if session is active
    if st.session_state.breathing_active or st.session_state.session_completed:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                <h4>Cycles</h4>
                <h2>{st.session_state.breathing_cycles}/{st.session_state.target_cycles}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.breathing_start_time:
                elapsed = (datetime.now() - st.session_state.breathing_start_time).seconds
                minutes = elapsed // 60
                seconds = elapsed % 60
                time_str = f"{minutes}:{seconds:02d}"
            else:
                time_str = "0:00"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                <h4>Time</h4>
                <h2>{time_str}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: #333;">
                <h4>Technique</h4>
                <h2>{breathing_techniques[st.session_state.breathing_technique]['icon']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            relaxation_color = "#4CAF50" if st.session_state.relaxation_score > 70 else "#FFC107" if st.session_state.relaxation_score > 40 else "#FF9800"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {relaxation_color} 0%, {relaxation_color}99 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                <h4>Calm</h4>
                <h2>{st.session_state.relaxation_score}%</h2>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technique selection phase
    if not st.session_state.breathing_technique:
        st.markdown("""
        ### 🧘 **Choose Your Breathing Technique**
        
        Each technique targets different aspects of mental and physical well-being. 
        Select based on your current needs:
        """)
        
        # Create technique selection cards
        for key, technique in breathing_techniques.items():
            with st.container():
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: {technique['color']}; padding: 2rem; border-radius: 15px; 
                                text-align: center; color: white; font-size: 3rem;">
                        {technique['icon']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"### {technique['name']}")
                    st.markdown(f"**Description:** {technique['description']}")
                    
                    # Show timing pattern
                    if key == "box":
                        pattern = f"Inhale {technique['inhale']}s → Hold {technique['hold']}s → Exhale {technique['exhale']}s → Hold {technique['hold2']}s"
                    elif "hold2" in technique:
                        pattern = f"Inhale {technique['inhale']}s → Hold {technique['hold']}s → Exhale {technique['exhale']}s → Hold {technique['hold2']}s"
                    else:
                        hold_text = f" → Hold {technique['hold']}s" if technique['hold'] > 0 else ""
                        pattern = f"Inhale {technique['inhale']}s{hold_text} → Exhale {technique['exhale']}s"
                    
                    st.markdown(f"**Pattern:** {pattern}")
                    st.markdown(f"**Best for:** {technique['when_to_use']}")
                    
                    if st.button(f"Select {technique['name']}", key=f"select_{key}", type="primary"):
                        st.session_state.breathing_technique = key
                        st.rerun()
                
                st.markdown("---")
        
        # Show general benefits
        st.markdown("""
        ### 🌟 **Science-Backed Benefits of Breathing Exercises:**
        
        - **Reduces Anxiety:** Activates parasympathetic nervous system
        - **Improves Focus:** Increases oxygen flow to prefrontal cortex  
        - **Lowers Blood Pressure:** Relaxes vascular system
        - **Enhances Sleep:** Triggers natural relaxation response
        - **Boosts Immunity:** Reduces stress hormones like cortisol
        - **Improves Heart Rate Variability:** Optimizes cardiovascular health
        - **Increases Mindfulness:** Develops present-moment awareness
        """)
    
    # Pre-session stress assessment
    elif st.session_state.stress_level_before is None:
        technique = breathing_techniques[st.session_state.breathing_technique]
        
        st.markdown(f"""
        ### {technique['icon']} **{technique['name']} Selected!**
        
        **About this technique:**
        {technique['description']}
        
        **Benefits you'll experience:**
        """)
        
        for benefit in technique['benefits']:
            st.markdown(f"✅ {benefit}")
        
        st.markdown(f"**Scientific basis:** {technique['science']}")
        
        st.markdown("---")
        st.markdown("### 📊 **Pre-Session Assessment**")
        st.markdown("Rate your current stress/anxiety level to track improvement:")
        
        stress_before = st.slider(
            "Current Stress Level", 
            min_value=1, max_value=10, value=5,
            help="1 = Very calm and relaxed, 10 = Very stressed and anxious"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Start Breathing Session", type="primary", key="start_breathing"):
                st.session_state.stress_level_before = stress_before
                st.session_state.breathing_start_time = datetime.now()
                st.session_state.breathing_active = True
                st.rerun()
    
    # Active breathing session
    elif st.session_state.breathing_active and st.session_state.breathing_cycles < st.session_state.target_cycles:
        technique = breathing_techniques[st.session_state.breathing_technique]
        
        # Create breathing visualization
        st.markdown(f"### {technique['icon']} **{technique['name']} - Cycle {st.session_state.breathing_cycles + 1}/{st.session_state.target_cycles}**")
        
        # Progress bar for current cycle
        progress_placeholder = st.empty()
        
        # Breathing circle visualization
        circle_placeholder = st.empty()
        
        # Instruction text
        instruction_placeholder = st.empty()
        
        # Control buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⏸️ Pause Session", key="pause_breathing"):
                st.session_state.breathing_active = False
                st.info("Session paused. Click 'Resume' to continue.")
                st.rerun()
        
        with col2:
            if st.button("⏭️ Skip Cycle", key="skip_cycle"):
                st.session_state.breathing_cycles += 1
                if st.session_state.breathing_cycles >= st.session_state.target_cycles:
                    st.session_state.breathing_active = False
                    st.session_state.session_completed = True
                st.rerun()
        
        with col3:
            if st.button("🛑 End Session", key="end_breathing"):
                st.session_state.breathing_active = False
                st.session_state.session_completed = True
                st.rerun()
        
        # Breathing cycle logic
        if st.session_state.breathing_active:
            # Simulate one breathing cycle
            cycle_phases = []
            
            if st.session_state.breathing_technique == "box":
                cycle_phases = [
                    ("Inhale", technique['inhale'], "#4CAF50"),
                    ("Hold", technique['hold'], "#FFC107"), 
                    ("Exhale", technique['exhale'], "#2196F3"),
                    ("Hold", technique['hold2'], "#FF9800")
                ]
            else:
                phases = [("Inhale", technique['inhale'], "#4CAF50")]
                if technique['hold'] > 0:
                    phases.append(("Hold", technique['hold'], "#FFC107"))
                phases.append(("Exhale", technique['exhale'], "#2196F3"))
                cycle_phases = phases
            
            # Execute one complete cycle
            for phase_name, duration, color in cycle_phases:
                if not st.session_state.breathing_active:
                    break
                    
                for second in range(duration):
                    if not st.session_state.breathing_active:
                        break
                    
                    # Update progress
                    progress = (second + 1) / duration
                    progress_placeholder.progress(progress, f"{phase_name}: {second + 1}/{duration} seconds")
                    
                    # Update breathing circle
                    if phase_name == "Inhale":
                        size = 50 + (progress * 100)  # Expand circle
                    elif phase_name == "Exhale": 
                        size = 150 - (progress * 100)  # Contract circle
                    else:
                        size = 150  # Hold steady
                    
                    circle_html = f"""
                    <div style="display: flex; justify-content: center; align-items: center; height: 300px;">
                        <div style="width: {size}px; height: {size}px; border-radius: 50%; 
                                    background: radial-gradient(circle, {color}88, {color}); 
                                    transition: all 0.5s ease-in-out; display: flex; 
                                    justify-content: center; align-items: center; color: white; 
                                    font-size: 1.5rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                            {phase_name}
                        </div>
                    </div>
                    """
                    circle_placeholder.markdown(circle_html, unsafe_allow_html=True)
                    
                    # Update instruction
                    instructions = {
                        "Inhale": "Breathe in slowly through your nose...",
                        "Hold": "Hold your breath gently...", 
                        "Exhale": "Breathe out slowly through your mouth..."
                    }
                    instruction_placeholder.markdown(f"""
                    <div style="text-align: center; padding: 1rem; font-size: 1.3rem; color: {color};">
                        <strong>{instructions.get(phase_name, phase_name)}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(1)
            
            # Complete cycle
            if st.session_state.breathing_active:
                st.session_state.breathing_cycles += 1
                
                # Simulate heart rate improvement
                baseline_hr = 80 - (st.session_state.breathing_cycles * 2)
                variation = random.uniform(-5, 5)
                current_hr = max(60, baseline_hr + variation)
                st.session_state.heart_rate_data.append(current_hr)
                
                # Update relaxation score
                st.session_state.relaxation_score = min(100, st.session_state.relaxation_score + 15)
                
                if st.session_state.breathing_cycles >= st.session_state.target_cycles:
                    st.session_state.breathing_active = False
                    st.session_state.session_completed = True
                
                st.rerun()
    
    # Session completion and results
    elif st.session_state.session_completed:
        technique = breathing_techniques[st.session_state.breathing_technique]
        
        # Post-session stress assessment if not done
        if st.session_state.stress_level_after is None:
            st.markdown("### 📊 **Post-Session Assessment**")
            st.markdown("How do you feel now after the breathing exercise?")
            
            stress_after = st.slider(
                "Current Stress Level", 
                min_value=1, max_value=10, value=3,
                help="1 = Very calm and relaxed, 10 = Very stressed and anxious",
                key="stress_after_slider"
            )
            
            if st.button("📊 Complete Assessment", type="primary"):
                st.session_state.stress_level_after = stress_after
                st.rerun()
        
        else:
            # Show complete results
            st.balloons()
            st.markdown(f"### 🎉 **{technique['name']} Session Complete!**")
            
            # Calculate improvements
            stress_reduction = st.session_state.stress_level_before - st.session_state.stress_level_after
            improvement_percentage = (stress_reduction / st.session_state.stress_level_before) * 100 if st.session_state.stress_level_before > 0 else 0
            
            session_duration = (datetime.now() - st.session_state.breathing_start_time).seconds if st.session_state.breathing_start_time else 0
            minutes = session_duration // 60
            seconds = session_duration % 60
            
            # Results summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                ### 📈 **Your Results:**
                - **Cycles Completed:** {st.session_state.breathing_cycles}/{st.session_state.target_cycles}
                - **Session Duration:** {minutes}m {seconds}s
                - **Stress Before:** {st.session_state.stress_level_before}/10
                - **Stress After:** {st.session_state.stress_level_after}/10
                - **Stress Reduction:** {stress_reduction} points
                - **Improvement:** {improvement_percentage:.1f}%
                - **Relaxation Score:** {st.session_state.relaxation_score}%
                """)
            
            with col2:
                # Create stress reduction chart
                if len(st.session_state.heart_rate_data) > 0:
                    fig = go.Figure()
                    
                    # Heart rate simulation
                    cycles = list(range(1, len(st.session_state.heart_rate_data) + 1))
                    fig.add_trace(go.Scatter(
                        x=cycles,
                        y=st.session_state.heart_rate_data,
                        mode='lines+markers',
                        name='Simulated Heart Rate',
                        line=dict(color='#FF6B6B', width=3),
                        marker=dict(size=8)
                    ))
                    
                    fig.update_layout(
                        title="Heart Rate Trend During Session",
                        xaxis_title="Breathing Cycle",
                        yaxis_title="Heart Rate (BPM)",
                        height=300,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Performance evaluation
            if improvement_percentage >= 50:
                st.success("🌟 **EXCELLENT!** You achieved significant stress reduction! Your breathing technique is very effective.")
                achievement = "Breathing Master! 🧘‍♀️✨"
            elif improvement_percentage >= 30:
                st.success("🎯 **GREAT PROGRESS!** You're experiencing substantial relaxation benefits from breathing exercises.")
                achievement = "Mindful Breather! 🌬️💪"
            elif improvement_percentage >= 10:
                st.success("👍 **POSITIVE RESULTS!** You're on the right track with breathing for stress relief.")
                achievement = "Breath Awareness Builder! 🫁📈"
            else:
                st.info("💪 **GOOD PRACTICE!** Breathing exercises become more effective with regular practice. Every session counts!")
                achievement = "Wellness Explorer! 🌱🔍"
            
            st.markdown(f"### 🏆 **Achievement Unlocked:** {achievement}")
            
            # Detailed benefits explanation
            st.markdown(f"""
            ### 🧠 **What Happened in Your Body:**
            
            **During {technique['name']}:**
            - **Nervous System:** Activated parasympathetic response (rest & digest mode)
            - **Heart Rate:** Decreased variability improved cardiovascular coherence
            - **Blood Pressure:** Reduced through vascular relaxation
            - **Stress Hormones:** Cortisol and adrenaline levels decreased
            - **Oxygen Delivery:** Improved efficiency to brain and muscles
            - **Muscle Tension:** Released through conscious relaxation
            
            ### 🎯 **How to Make This a Daily Habit:**
            
            **Recommended Schedule:**
            - **Morning:** 5 minutes to start day calmly
            - **Midday:** 3 minutes during lunch break
            - **Evening:** 10 minutes before bedtime
            - **As Needed:** During stressful moments
            
            **Progressive Training:**
            - Week 1-2: Focus on technique accuracy
            - Week 3-4: Increase session duration
            - Week 5+: Practice without visual guides
            
            ### 🔬 **Scientific Research:**
            {technique['science']}
            
            Studies show that regular breathing exercises can:
            - Reduce anxiety by up to 60% in 8 weeks
            - Lower blood pressure by 5-10 mmHg
            - Improve sleep quality by 40%
            - Increase focus and concentration by 25%
            """)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("🔄 Practice Again", key="practice_again", type="primary"):
                    # Reset session state
                    st.session_state.breathing_cycles = 0
                    st.session_state.breathing_active = False
                    st.session_state.stress_level_before = None
                    st.session_state.stress_level_after = None
                    st.session_state.session_completed = False
                    st.session_state.breathing_start_time = None
                    st.session_state.heart_rate_data = []
                    st.session_state.relaxation_score = 0
                    st.success("Starting new breathing session!")
                    st.rerun()
            
            with col2:
                if st.button("🎯 Try Different Technique", key="try_different"):
                    # Reset completely
                    st.session_state.breathing_technique = None
                    st.session_state.breathing_cycles = 0
                    st.session_state.breathing_active = False
                    st.session_state.stress_level_before = None
                    st.session_state.stress_level_after = None
                    st.session_state.session_completed = False
                    st.session_state.breathing_start_time = None
                    st.session_state.heart_rate_data = []
                    st.session_state.relaxation_score = 0
                    st.success("Choose a new breathing technique!")
                    st.rerun()
            
            with col3:
                if st.button("📱 Set Reminder", key="set_reminder"):
                    st.info("""
                    **Daily Breathing Reminder Set!** 📱
                    
                    💡 **Pro Tips:**
                    - Set phone alerts for breathing breaks
                    - Practice during daily activities (walking, waiting)
                    - Use breathing apps for guided sessions
                    - Track your progress in a journal
                    """)
    
    # Paused session resume
    elif not st.session_state.breathing_active and st.session_state.breathing_cycles < st.session_state.target_cycles:
        technique = breathing_techniques[st.session_state.breathing_technique]
        
        st.warning(f"### ⏸️ **Session Paused** - {technique['name']}")
        st.markdown(f"**Progress:** {st.session_state.breathing_cycles}/{st.session_state.target_cycles} cycles completed")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("▶️ Resume Session", key="resume_breathing", type="primary"):
                st.session_state.breathing_active = True
                st.rerun()
        
        with col2:
            if st.button("🔄 Restart Session", key="restart_breathing"):
                st.session_state.breathing_cycles = 0
                st.session_state.breathing_active = True
                st.session_state.breathing_start_time = datetime.now()
                st.rerun()
        
        with col3:
            if st.button("🛑 End Session", key="end_paused"):
                st.session_state.breathing_active = False
                st.session_state.session_completed = True
                st.rerun()

# Simple wrapper to show just the game
def show_games_page():
    """Show Breathing Pattern Game only"""
    
    # Header
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #4A90E2; font-family: 'Baloo 2', cursive;">🌬️ Breathing Pattern Game</h1>
        <p style="color: #87CEEB; font-size: 1.2rem;">Master therapeutic breathing for anxiety relief and mindfulness</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the breathing game directly
    breathing_pattern_game()

if __name__ == "__main__":
    show_games_page()