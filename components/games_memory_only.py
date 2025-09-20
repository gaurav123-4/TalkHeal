import streamlit as st
import random
import time

def memory_challenge_game():
    """Complete Memory Challenge Game - Simon Says style for cognitive improvement"""
    
    st.markdown("### 🧠 Memory Challenge Game")
    st.markdown("**Improve your memory and concentration with this Simon Says style game!**")
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Games", key="back_memory"):
            st.rerun()
    
    # Initialize game state
    if "memory_sequence" not in st.session_state:
        st.session_state.memory_sequence = []
    if "memory_user_sequence" not in st.session_state:
        st.session_state.memory_user_sequence = []
    if "memory_score" not in st.session_state:
        st.session_state.memory_score = 0
    if "memory_game_active" not in st.session_state:
        st.session_state.memory_game_active = False
    if "memory_show_sequence" not in st.session_state:
        st.session_state.memory_show_sequence = False
    if "memory_level" not in st.session_state:
        st.session_state.memory_level = 1
    
    # Game colors and styling
    colors = ["🔴", "🔵", "🟢", "🟡"]
    color_names = ["Red", "Blue", "Green", "Yellow"]
    color_codes = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
    
    # Display game stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h3>Score: {st.session_state.memory_score}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h3>Level: {st.session_state.memory_level}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sequence_length = len(st.session_state.memory_sequence)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h3>Sequence: {sequence_length}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Game instructions
    if not st.session_state.memory_game_active:
        st.markdown("""
        ### 📖 How to Play:
        1. **Click "Start New Game"** to begin
        2. **Watch the sequence** of colors carefully
        3. **Click "I'm Ready!"** when you've memorized it
        4. **Repeat the sequence** by clicking the colors in order
        5. **Each correct sequence** increases your score and level!
        
        ### 🎯 Mental Health Benefits:
        - **Improves working memory** and concentration
        - **Enhances cognitive flexibility** and processing speed
        - **Builds confidence** through progressive difficulty
        - **Reduces stress** through focused attention training
        """)
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎮 Start New Game", key="start_memory", type="primary"):
            st.session_state.memory_sequence = [random.randint(0, 3)]
            st.session_state.memory_user_sequence = []
            st.session_state.memory_score = 0
            st.session_state.memory_level = 1
            st.session_state.memory_game_active = True
            st.session_state.memory_show_sequence = True
            st.success("New game started! Watch the sequence...")
            st.rerun()
    
    with col2:
        if st.button("👀 Show Sequence", key="show_sequence", disabled=not st.session_state.memory_game_active):
            st.session_state.memory_show_sequence = True
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset Game", key="reset_memory"):
            for key in ["memory_sequence", "memory_user_sequence", "memory_score", 
                       "memory_game_active", "memory_show_sequence", "memory_level"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("Game reset!")
            st.rerun()
    
    # Display sequence (when showing)
    if st.session_state.memory_show_sequence and st.session_state.memory_sequence:
        st.markdown("### 👁️ **Memorize this sequence:**")
        
        # Create animated sequence display
        sequence_cols = st.columns(len(st.session_state.memory_sequence))
        for i, color_idx in enumerate(st.session_state.memory_sequence):
            with sequence_cols[i]:
                st.markdown(f"""
                <div style="
                    background-color: {color_codes[color_idx]};
                    color: white;
                    padding: 2rem;
                    border-radius: 50%;
                    text-align: center;
                    font-size: 2rem;
                    margin: 0.5rem;
                    animation: pulse 1.5s ease-in-out infinite;
                ">
                    {colors[color_idx]}
                </div>
                <style>
                @keyframes pulse {{
                    0% {{ transform: scale(1); opacity: 1; }}
                    50% {{ transform: scale(1.1); opacity: 0.8; }}
                    100% {{ transform: scale(1); opacity: 1; }}
                }}
                </style>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("✅ I'm Ready to Play!", key="ready_memory", type="primary"):
            st.session_state.memory_show_sequence = False
            st.success("Great! Now click the sequence in the correct order!")
            st.rerun()
    
    # Game playing interface
    elif st.session_state.memory_game_active and not st.session_state.memory_show_sequence:
        st.markdown("### 🎯 **Click the sequence in order:**")
        
        # Color buttons for playing
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (col, color, name, color_code) in enumerate(zip(cols, colors, color_names, color_codes)):
            with col:
                button_style = f"""
                <style>
                div.stButton > button:first-child {{
                    background-color: {color_code};
                    color: white;
                    border: 3px solid #fff;
                    border-radius: 20px;
                    font-size: 1.5rem;
                    font-weight: bold;
                    padding: 1rem;
                    width: 100%;
                    height: 120px;
                    transition: all 0.3s ease;
                }}
                div.stButton > button:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                }}
                </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                
                if st.button(f"{color}\n{name}", key=f"color_{i}"):
                    st.session_state.memory_user_sequence.append(i)
                    
                    # Check if sequence is correct so far
                    user_len = len(st.session_state.memory_user_sequence)
                    sequence_len = len(st.session_state.memory_sequence)
                    
                    if user_len <= sequence_len:
                        if st.session_state.memory_user_sequence[-1] != st.session_state.memory_sequence[user_len-1]:
                            # Wrong sequence - Game Over
                            st.error("❌ **Wrong sequence! Game Over!**")
                            st.markdown(f"**Final Score: {st.session_state.memory_score}**")
                            st.balloons()
                            
                            # Show correct sequence
                            correct_sequence = " → ".join([f"{colors[j]} {color_names[j]}" for j in st.session_state.memory_sequence])
                            st.info(f"**Correct sequence was:** {correct_sequence}")
                            
                            st.session_state.memory_game_active = False
                            
                        elif user_len == sequence_len:
                            # Completed sequence correctly!
                            st.success("✅ **Perfect! Sequence completed correctly!**")
                            st.session_state.memory_score += 10
                            st.session_state.memory_level += 1
                            
                            # Add new color to sequence
                            st.session_state.memory_sequence.append(random.randint(0, 3))
                            st.session_state.memory_user_sequence = []
                            st.session_state.memory_show_sequence = True
                            
                            # Celebration
                            if st.session_state.memory_level % 5 == 0:
                                st.balloons()
                                st.success(f"🎉 **Amazing! You reached Level {st.session_state.memory_level}!**")
                            
                            time.sleep(1)
                        else:
                            # Continue sequence
                            st.info(f"Good! {user_len}/{sequence_len} colors correct. Keep going!")
                    
                    st.rerun()
        
        # Show current user input
        if st.session_state.memory_user_sequence:
            st.markdown("### 📝 **Your current input:**")
            user_display = " → ".join([f"{colors[i]} {color_names[i]}" for i in st.session_state.memory_user_sequence])
            st.markdown(f"**{user_display}**")
        
        # Progress indicator
        if st.session_state.memory_user_sequence:
            progress = len(st.session_state.memory_user_sequence) / len(st.session_state.memory_sequence)
            st.progress(progress, f"Progress: {len(st.session_state.memory_user_sequence)}/{len(st.session_state.memory_sequence)}")
    
    # Game completed message
    elif not st.session_state.memory_game_active and st.session_state.memory_score > 0:
        st.markdown("### 🎉 **Game Over!**")
        
        # Performance feedback
        if st.session_state.memory_score >= 50:
            st.success("🌟 **Excellent memory skills! Your cognitive training is paying off!**")
        elif st.session_state.memory_score >= 30:
            st.success("🎯 **Great job! Your memory and focus are improving!**")
        elif st.session_state.memory_score >= 10:
            st.info("👍 **Good effort! Keep practicing to strengthen your memory!**")
        else:
            st.info("💪 **Every attempt helps! Memory games get easier with practice!**")
        
        st.markdown(f"""
        ### 📊 **Your Performance:**
        - **Final Score:** {st.session_state.memory_score} points
        - **Highest Level Reached:** {st.session_state.memory_level}
        - **Sequences Completed:** {st.session_state.memory_score // 10}
        
        ### 🧠 **Memory Training Benefits:**
        - You exercised your **working memory** - the mental workspace for processing information
        - You practiced **sustained attention** - crucial for daily tasks and learning
        - You built **cognitive resilience** - the ability to bounce back from mistakes
        - You enhanced **pattern recognition** - helpful for problem-solving
        """)

# Simple wrapper to show just the game
def show_games_page():
    """Show Memory Challenge Game only"""
    
    # Header
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #ff69b4; font-family: 'Baloo 2', cursive;">🧠 Memory Challenge</h1>
        <p style="color: #ffb6d5; font-size: 1.2rem;">Simon Says style game for cognitive improvement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the memory game directly
    memory_challenge_game()

if __name__ == "__main__":
    show_games_page()
