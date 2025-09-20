import streamlit as st
import random
import time

def mood_color_matching_game():
    """Complete Mood Color Matching Game for emotional awareness and color psychology"""
    
    st.markdown("### 🎨 Mood Color Matching Game")
    st.markdown("**Express and understand emotions through color psychology!**")
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Games", key="back_mood"):
            st.rerun()
    
    # Initialize game state
    if "mood_score" not in st.session_state:
        st.session_state.mood_score = 0
    if "mood_question" not in st.session_state:
        st.session_state.mood_question = 0
    if "mood_total_questions" not in st.session_state:
        st.session_state.mood_total_questions = 8
    if "mood_game_completed" not in st.session_state:
        st.session_state.mood_game_completed = False
    
    # Color psychology data with educational facts
    mood_colors = {
        "Happy/Joyful": {
            "correct": "Yellow", 
            "colors": ["Yellow", "Black", "Gray", "Brown"], 
            "fact": "Yellow stimulates optimism and energy, often associated with happiness and sunshine. It can boost mental clarity and creativity!",
            "psychology": "Studies show yellow activates the left side of the brain, promoting logical thinking and positivity."
        },
        "Calm/Peaceful": {
            "correct": "Blue", 
            "colors": ["Red", "Blue", "Orange", "Purple"],
            "fact": "Blue promotes calmness and serenity, often used in meditation spaces. It can lower heart rate and reduce anxiety!",
            "psychology": "Blue light therapy is used to treat seasonal depression and improve mood regulation."
        },
        "Energetic/Active": {
            "correct": "Red", 
            "colors": ["Blue", "Green", "Red", "White"],
            "fact": "Red increases energy and excitement, stimulating both mind and body. It can boost confidence and motivation!",
            "psychology": "Red is known to increase adrenaline production and can improve physical performance."
        },
        "Natural/Grounded": {
            "correct": "Green", 
            "colors": ["Pink", "Yellow", "Green", "Purple"],
            "fact": "Green represents nature and growth, promoting balance and harmony. It's the most restful color for the human eye!",
            "psychology": "Green environments have been shown to reduce mental fatigue and improve focus."
        },
        "Creative/Imaginative": {
            "correct": "Purple", 
            "colors": ["Brown", "Gray", "Purple", "Black"],
            "fact": "Purple enhances creativity and imagination, often linked to artistic expression and spirituality!",
            "psychology": "Purple combines the stability of blue and energy of red, promoting both calm focus and creative thinking."
        },
        "Warm/Comforting": {
            "correct": "Orange", 
            "colors": ["Blue", "Orange", "Gray", "White"],
            "fact": "Orange creates feelings of warmth and comfort, promoting social connection and enthusiasm!",
            "psychology": "Orange is associated with increased appetite and social interaction, often used in therapeutic settings."
        },
        "Pure/Clean": {
            "correct": "White", 
            "colors": ["Black", "Red", "White", "Brown"],
            "fact": "White represents purity, clarity, and new beginnings. It promotes mental clarity and fresh perspectives!",
            "psychology": "White spaces can reduce mental clutter and improve concentration and decision-making."
        },
        "Mysterious/Deep": {
            "correct": "Black", 
            "colors": ["Yellow", "Pink", "Black", "White"],
            "fact": "Black represents depth, mystery, and elegance. It can promote introspection and sophisticated thinking!",
            "psychology": "Black is associated with power and authority, and can help people feel more confident in decision-making."
        }
    }
    
    moods = list(mood_colors.keys())
    
    # Display game stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h3>Score: {st.session_state.mood_score}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_q = min(st.session_state.mood_question + 1, st.session_state.mood_total_questions)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: #333;">
            <h3>Question: {current_q}/{st.session_state.mood_total_questions}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        percentage = round((st.session_state.mood_score / (st.session_state.mood_question * 10)) * 100) if st.session_state.mood_question > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: #333;">
            <h3>Accuracy: {percentage}%</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Game instructions
    if st.session_state.mood_question == 0 and not st.session_state.mood_game_completed:
        st.markdown("""
        ### 📖 How to Play:
        1. **Read the emotion/mood** presented to you
        2. **Choose the color** that best represents that feeling
        3. **Learn color psychology facts** with each answer
        4. **Build emotional intelligence** through color awareness
        
        ### 🎯 Mental Health Benefits:
        - **Emotional Awareness:** Better understanding of your feelings
        - **Color Psychology:** Learn how colors affect mood and behavior
        - **Mood Regulation:** Use colors therapeutically in daily life
        - **Self-Expression:** Develop emotional vocabulary through colors
        """)
        
        if st.button("🎨 Start Color Psychology Journey", key="start_mood_game", type="primary"):
            st.session_state.mood_question = 0
            st.session_state.mood_score = 0
            st.session_state.mood_game_completed = False
            st.rerun()
    
    # Game play
    elif st.session_state.mood_question < st.session_state.mood_total_questions and not st.session_state.mood_game_completed:
        current_mood = moods[st.session_state.mood_question]
        mood_data = mood_colors[current_mood]
        
        st.markdown(f"### 🎭 Which color best represents: **{current_mood}**?")
        
        # Show a beautiful mood representation
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;">
            <h2 style="margin: 0; font-size: 2.5rem;">{current_mood}</h2>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">Think about this feeling and choose the color that matches it</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Color options with beautiful styling
        options = mood_data["colors"].copy()
        random.shuffle(options)
        
        # Color codes for styling
        color_codes = {
            "Red": "#FF6B6B", "Blue": "#4ECDC4", "Green": "#45B7D1", "Yellow": "#FFA07A",
            "Purple": "#A8E6CF", "Orange": "#FFB347", "Pink": "#FFB6C1", "Black": "#696969",
            "White": "#F0F0F0", "Brown": "#D2B48C", "Gray": "#C0C0C0"
        }
        
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (col, color) in enumerate(zip(cols, options)):
            with col:
                color_code = color_codes.get(color, "#CCCCCC")
                
                # Custom button styling
                st.markdown(f"""
                <style>
                .color-button-{i} {{
                    background-color: {color_code};
                    color: {'black' if color in ['White', 'Yellow', 'Pink'] else 'white'};
                    border: 3px solid #fff;
                    border-radius: 20px;
                    padding: 2rem 1rem;
                    font-size: 1.2rem;
                    font-weight: bold;
                    width: 100%;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }}
                .color-button-{i}:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                }}
                </style>
                """, unsafe_allow_html=True)
                
                if st.button(f"🎨 {color}", key=f"mood_color_{i}", help=f"Choose {color}"):
                    if color == mood_data["correct"]:
                        st.session_state.mood_score += 10
                        st.success(f"✅ **Perfect match!** {mood_data['fact']}")
                        
                        # Show additional psychology insight
                        st.info(f"🧠 **Psychology Insight:** {mood_data['psychology']}")
                        
                        # Celebration for correct answers
                        if st.session_state.mood_question % 3 == 0:
                            st.balloons()
                        
                    else:
                        st.error(f"❌ **Not quite right.** The correct answer was **{mood_data['correct']}**.")
                        st.info(f"💡 **Learn:** {mood_data['fact']}")
                    
                    st.session_state.mood_question += 1
                    time.sleep(2)
                    st.rerun()
        
        # Progress bar
        progress = st.session_state.mood_question / st.session_state.mood_total_questions
        st.progress(progress, f"Progress: {st.session_state.mood_question}/{st.session_state.mood_total_questions} questions")
    
    # Game completion
    elif st.session_state.mood_question >= st.session_state.mood_total_questions or st.session_state.mood_game_completed:
        st.session_state.mood_game_completed = True
        
        # Final results
        st.balloons()
        st.markdown("### 🎉 **Color Psychology Master!**")
        
        final_percentage = round((st.session_state.mood_score / (st.session_state.mood_total_questions * 10)) * 100)
        
        # Performance feedback
        if final_percentage == 100:
            st.success("🌟 **PERFECT SCORE!** You have incredible color-emotion awareness! You're a true color psychology expert!")
            achievement = "Color Psychology Genius! 🎨✨"
        elif final_percentage >= 75:
            st.success("🎯 **Outstanding!** You have excellent understanding of color psychology! Your emotional intelligence is impressive!")
            achievement = "Color Emotion Expert! 🎨🧠"
        elif final_percentage >= 50:
            st.success("👍 **Great job!** You're developing good color-emotion connections! Keep exploring color psychology!")
            achievement = "Color Psychology Student! 🎨📚"
        else:
            st.info("💪 **Good start!** Color psychology takes practice. Every connection you make strengthens your emotional awareness!")
            achievement = "Color Explorer! 🎨🔍"
        
        # Detailed results
        st.markdown(f"""
        ### 📊 **Your Color Psychology Results:**
        - **Final Score:** {st.session_state.mood_score}/{st.session_state.mood_total_questions * 10} points
        - **Accuracy:** {final_percentage}%
        - **Achievement:** {achievement}
        - **Questions Completed:** {st.session_state.mood_total_questions}
        
        ### 🎨 **How to Use Color Psychology in Daily Life:**
        - **Wear blue** when you need to feel calm and focused
        - **Add yellow** to your space for energy and creativity  
        - **Use green** in your environment to reduce stress
        - **Choose red** when you need confidence and motivation
        - **Incorporate purple** for creative and spiritual activities
        - **Use orange** to feel more social and enthusiastic
        
        ### 🧠 **Emotional Benefits You've Gained:**
        - **Enhanced emotional vocabulary** through color associations
        - **Better mood awareness** and self-understanding
        - **Practical tools** for mood regulation using colors
        - **Deeper connection** between visual stimuli and emotions
        """)
        
        # Reset option
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Play Again", key="restart_mood_game", type="primary"):
                st.session_state.mood_score = 0
                st.session_state.mood_question = 0
                st.session_state.mood_game_completed = False
                st.success("Starting new color psychology journey!")
                st.rerun()
    
    # Control buttons
    if st.session_state.mood_question > 0 and not st.session_state.mood_game_completed:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔄 Restart Game", key="restart_mood"):
                st.session_state.mood_score = 0
                st.session_state.mood_question = 0
                st.session_state.mood_game_completed = False
                st.rerun()
        
        with col3:
            if st.button("⏭️ Skip Question", key="skip_mood"):
                st.session_state.mood_question += 1
                st.warning("Question skipped. Try to answer all questions for best learning!")
                st.rerun()

# Simple wrapper to show just the game
def show_games_page():
    """Show Mood Color Matching Game only"""
    
    # Header
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #ff69b4; font-family: 'Baloo 2', cursive;">🎨 Mood Color Matching</h1>
        <p style="color: #ffb6d5; font-size: 1.2rem;">Express emotions through color psychology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the mood color game directly
    mood_color_matching_game()

if __name__ == "__main__":
    show_games_page()