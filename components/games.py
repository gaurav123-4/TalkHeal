import streamlit as st
import random
import time
from datetime import datetime
import json

def show_games_page():
    """Main games page with various mental health focused mini-games"""
    
    st.markdown("""
    <style>
    .game-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .game-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .game-button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a6f);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .game-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    .score-display {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="game-header">
        <h1>🎮 Mental Wellness Games</h1>
        <p>Interactive games designed to boost your mental health and well-being</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Game selection
    games = {
        "🧠 Memory Challenge": "memory_game",
        "🎨 Mood Color Match": "color_mood_game", 
        "😌 Stress Relief Clicker": "stress_clicker_game",
        "💭 Positive Word Association": "word_association_game",
        "🫁 Breathing Pattern Game": "breathing_game"
    }
    
    st.subheader("Choose Your Wellness Game:")
    
    # Add responsive game selection CSS
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .game-selection-container {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .game-selection-container .stButton {
            width: 100%;
        }
        .game-selection-container .stButton > button {
            width: 100% !important;
            min-height: 50px !important;
            font-size: 0.9rem !important;
            text-align: center !important;
        }
    }
    @media (min-width: 769px) {
        .game-selection-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
        }
        .game-selection-row .stButton {
            flex: 1 1 200px;
            max-width: 250px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Responsive layout for game buttons - max 2 per row on desktop, stack on mobile
    games_list = list(games.items())
    
    st.markdown('<div class="game-selection-container">', unsafe_allow_html=True)
    
    # Group games into rows of 2 for better mobile compatibility
    for i in range(0, len(games_list), 2):
        row_games = games_list[i:i+2]
        cols = st.columns(len(row_games))
        
        for j, (game_name, game_key) in enumerate(row_games):
            with cols[j]:
                if st.button(game_name, key=f"select_{game_key}", use_container_width=True):
                    st.session_state.current_game = game_key
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display selected game
    if 'current_game' in st.session_state:
        st.markdown("---")
        
        if st.session_state.current_game == "memory_game":
            memory_challenge_game()
        elif st.session_state.current_game == "color_mood_game":
            mood_color_matching_game()
        elif st.session_state.current_game == "stress_clicker_game":
            stress_relief_clicker()
        elif st.session_state.current_game == "word_association_game":
            positive_word_association()
        elif st.session_state.current_game == "breathing_game":
            breathing_pattern_game()

def memory_challenge_game():
    """Simon Says style memory game for cognitive improvement"""
    st.markdown("""
    <div class="game-card">
        <h3>🧠 Memory Challenge Game</h3>
        <p>Improve your memory and concentration by following the pattern!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize game state
    if 'memory_sequence' not in st.session_state:
        st.session_state.memory_sequence = []
        st.session_state.user_sequence = []
        st.session_state.memory_level = 1
        st.session_state.memory_score = 0
        st.session_state.show_sequence = False
        st.session_state.game_over = False
    
    colors = ["🔴", "🟡", "🟢", "🔵"]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="score-display">
            Level: {st.session_state.memory_level}<br>
            Score: {st.session_state.memory_score}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚀 Start New Game", key="start_memory"):
            st.session_state.memory_sequence = [random.choice(colors)]
            st.session_state.user_sequence = []
            st.session_state.memory_level = 1
            st.session_state.memory_score = 0
            st.session_state.show_sequence = True
            st.session_state.game_over = False
            st.rerun()
    
    if st.session_state.show_sequence and not st.session_state.game_over:
        st.write("🔍 **Watch the sequence carefully!**")
        sequence_container = st.empty()
        
        # Show sequence with delay
        for i, color in enumerate(st.session_state.memory_sequence):
            sequence_container.markdown(f"### Sequence: {' '.join(st.session_state.memory_sequence[:i+1])}")
            time.sleep(0.8)
        
        st.session_state.show_sequence = False
        st.write("🎯 **Now repeat the sequence:**")
    
    if not st.session_state.show_sequence and not st.session_state.game_over:
        st.write("Click the colors in the correct order:")
        
        # Add responsive CSS for memory game colors
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            .memory-colors-container {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                justify-content: center;
                margin: 1rem 0;
            }
            .memory-colors-container .stButton {
                flex: 1 1 45%;
                min-width: 80px;
                max-width: 120px;
            }
            .memory-colors-container .stButton > button {
                font-size: 2rem !important;
                min-height: 60px !important;
                width: 100% !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="memory-colors-container">', unsafe_allow_html=True)
        
        # Use 2x2 grid for mobile compatibility
        for row in range(2):
            cols = st.columns(2)
            for col in range(2):
                color_index = row * 2 + col
                if color_index < len(colors):
                    color = colors[color_index]
                    with cols[col]:
                        if st.button(color, key=f"memory_{color}_{len(st.session_state.user_sequence)}", use_container_width=True):
                            st.session_state.user_sequence.append(color)
        
        st.markdown('</div>', unsafe_allow_html=True)
                    
        # Check if sequence matches
        if len(st.session_state.user_sequence) == len(st.session_state.memory_sequence):
            if st.session_state.user_sequence == st.session_state.memory_sequence:
                st.session_state.memory_score += 10 * st.session_state.memory_level
                st.session_state.memory_level += 1
                st.session_state.memory_sequence.append(random.choice(colors))
                st.session_state.user_sequence = []
                st.session_state.show_sequence = True
                st.success(f"🎉 Correct! Level {st.session_state.memory_level}")
                st.rerun()
            else:
                st.session_state.game_over = True
                st.error("❌ Wrong sequence! Game Over!")
        
        elif st.session_state.user_sequence[len(st.session_state.user_sequence)-1] != st.session_state.memory_sequence[len(st.session_state.user_sequence)-1]:
            st.session_state.game_over = True
            st.error("❌ Wrong color! Game Over!")
        
        if st.session_state.user_sequence:
            st.write(f"Your sequence: {' '.join(st.session_state.user_sequence)}")

def mood_color_matching_game():
    """Color matching game for mood expression"""
    st.markdown("""
    <div class="game-card">
        <h3>🎨 Mood Color Matching Game</h3>
        <p>Express your emotions through colors and learn about color psychology!</p>
    </div>
    """, unsafe_allow_html=True)
    
    mood_colors = {
        "😊 Happy": "🟡",
        "😢 Sad": "🔵", 
        "😠 Angry": "🔴",
        "😌 Calm": "🟢",
        "💜 Loving": "🟣",
        "🧡 Energetic": "🟠"
    }
    
    if 'color_score' not in st.session_state:
        st.session_state.color_score = 0
    
    st.write("**Match the emotion with the color that represents it:**")
    
    # Randomize the mood for the question
    current_mood = random.choice(list(mood_colors.keys()))
    correct_color = mood_colors[current_mood]
    
    st.write(f"### Current Emotion: {current_mood}")
    
    # Create color options (correct + 3 random wrong ones)
    all_colors = list(set(mood_colors.values()))
    wrong_colors = [c for c in all_colors if c != correct_color]
    options = [correct_color] + random.sample(wrong_colors, min(3, len(wrong_colors)))
    random.shuffle(options)
    
    # Add responsive CSS for mood color selection  
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .mood-color-selection {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            margin: 1rem 0;
        }
        .mood-color-selection .stButton {
            flex: 1 1 45%;
            min-width: 70px;
            max-width: 100px;
        }
        .mood-color-selection .stButton > button {
            font-size: 2rem !important;
            min-height: 60px !important;
            width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="mood-color-selection">', unsafe_allow_html=True)
    
    # Use 2 columns per row for better mobile layout
    for row in range(0, len(options), 2):
        row_options = options[row:row+2]
        cols = st.columns(len(row_options))
        
        for j, color in enumerate(row_options):
            with cols[j]:
                button_index = row + j
                if st.button(color, key=f"color_choice_{button_index}", use_container_width=True):
                    if color == correct_color:
                        st.session_state.color_score += 10
                        st.success("🎉 Perfect match! Colors can really reflect our emotions!")
                        
                        # Show color psychology fact
                        facts = {
                            "🟡": "Yellow is associated with happiness, optimism, and mental clarity!",
                            "🔵": "Blue represents calmness and can help reduce anxiety and stress.",
                            "🔴": "Red is linked to strong emotions like passion, energy, and sometimes anger.",
                            "🟢": "Green promotes balance, harmony, and has a calming effect on the mind.",
                            "🟣": "Purple is often associated with creativity, spirituality, and compassion.",
                            "🟠": "Orange represents enthusiasm, creativity, and positive energy!"
                        }
                        st.info(f"💡 **Did you know?** {facts.get(correct_color, 'Colors have powerful psychological effects!')}")
                    else:
                        st.error("Try again! Think about what this emotion feels like.")
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="score-display">
        Color Wisdom Score: {st.session_state.color_score} 🎨
    </div>
    """, unsafe_allow_html=True)

def stress_relief_clicker():
    """Simple clicking game for stress relief"""
    st.markdown("""
    <div class="game-card">
        <h3>😌 Stress Relief Clicker</h3>
        <p>Click to release stress and tension. Each click helps you feel calmer!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'stress_clicks' not in st.session_state:
        st.session_state.stress_clicks = 0
        st.session_state.stress_level = 100
    
    # Visual stress ball
    stress_ball_size = max(50, 150 - (st.session_state.stress_clicks // 10))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🔴", key="stress_ball", help="Click me to release stress!"):
            st.session_state.stress_clicks += 1
            st.session_state.stress_level = max(0, st.session_state.stress_level - 2)
            
            # Encouraging messages
            messages = [
                "Deep breath... you're doing great! 🌟",
                "Feel the tension melting away... 😌", 
                "Each click brings more peace... ✨",
                "You're stronger than your stress! 💪",
                "Breathe in calm, breathe out tension... 🫁"
            ]
            
            if st.session_state.stress_clicks % 5 == 0:
                st.success(random.choice(messages))
    
    # Progress bars
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Clicks for Calm", st.session_state.stress_clicks)
    with col2:
        st.metric("Stress Level", f"{st.session_state.stress_level}%")
    
    # Stress level progress bar
    st.progress((100 - st.session_state.stress_level) / 100)
    
    if st.session_state.stress_level == 0:
        st.balloons()
        st.success("🎉 Congratulations! You've achieved complete calm! Your mind is now at peace. 🧘‍♀️")

def positive_word_association():
    """Word association game to promote positive thinking"""
    st.markdown("""
    <div class="game-card">
        <h3>💭 Positive Word Association</h3>
        <p>Build positive thinking patterns by connecting uplifting words!</p>
    </div>
    """, unsafe_allow_html=True)
    
    positive_words = [
        "Joy", "Peace", "Love", "Hope", "Courage", "Strength", "Gratitude",
        "Kindness", "Compassion", "Success", "Growth", "Healing", "Bright",
        "Beautiful", "Wonderful", "Amazing", "Brilliant", "Fantastic", "Excellent"
    ]
    
    if 'word_chain' not in st.session_state:
        st.session_state.word_chain = []
        st.session_state.word_score = 0
    
    if not st.session_state.word_chain:
        starter_word = random.choice(positive_words)
        st.session_state.word_chain.append(starter_word)
    
    st.write("**Build a chain of positive words! Each word should relate to the previous one:**")
    st.write(f"### Current chain: {' → '.join(st.session_state.word_chain)}")
    
    # Input for next word
    next_word = st.text_input("Add the next positive word:", key="word_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Add Word", key="add_word") and next_word:
            st.session_state.word_chain.append(next_word.title())
            st.session_state.word_score += 5
            
            encouragements = [
                f"Beautiful connection! '{next_word}' adds wonderful energy! ✨",
                f"Perfect! '{next_word}' brings such positive vibes! 🌟", 
                f"Excellent! Your mind is creating beautiful associations! 💫",
                f"Amazing! '{next_word}' flows perfectly with positive energy! 🌈"
            ]
            st.success(random.choice(encouragements))
            st.rerun()
    
    with col2:
        if st.button("🔄 New Chain", key="new_chain"):
            st.session_state.word_chain = [random.choice(positive_words)]
            st.rerun()
    
    st.markdown(f"""
    <div class="score-display">
        Positivity Score: {st.session_state.word_score} ✨<br>
        Chain Length: {len(st.session_state.word_chain)} words
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.word_chain) >= 10:
        st.success("🎉 Amazing! You've created a beautiful chain of positivity! Your mind is becoming more attuned to positive thoughts! 🌟")

def breathing_pattern_game():
    """Interactive breathing exercise game"""
    st.markdown("""
    <div class="game-card">
        <h3>🫁 Breathing Pattern Game</h3>
        <p>Follow the breathing patterns for relaxation and mindfulness!</p>
    </div>
    """, unsafe_allow_html=True)
    
    breathing_patterns = {
        "4-7-8 Relaxation": {"inhale": 4, "hold": 7, "exhale": 8, "description": "Perfect for reducing anxiety and promoting sleep"},
        "Box Breathing": {"inhale": 4, "hold": 4, "exhale": 4, "description": "Used by Navy SEALs for focus and stress management"},
        "Energizing Breath": {"inhale": 6, "hold": 2, "exhale": 4, "description": "Boosts energy and mental clarity"}
    }
    
    selected_pattern = st.selectbox("Choose a breathing pattern:", list(breathing_patterns.keys()))
    pattern = breathing_patterns[selected_pattern]
    
    st.info(f"**{selected_pattern}:** {pattern['description']}")
    
    if 'breathing_active' not in st.session_state:
        st.session_state.breathing_active = False
        st.session_state.breathing_cycles = 0
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌬️ Start Breathing Exercise", key="start_breathing"):
            st.session_state.breathing_active = True
            st.session_state.breathing_cycles = 0
    
    with col2:
        if st.button("⏹️ Stop", key="stop_breathing"):
            st.session_state.breathing_active = False
    
    if st.session_state.breathing_active:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Breathing cycle simulation
        cycle_phases = [
            ("Inhale slowly...", pattern["inhale"], "🌬️➡️"),
            ("Hold your breath...", pattern["hold"], "⏸️"),
            ("Exhale gently...", pattern["exhale"], "🌬️⬅️")
        ]
        
        for phase_name, duration, emoji in cycle_phases:
            for i in range(duration):
                progress = (i + 1) / duration
                progress_bar.progress(progress)
                status_text.markdown(f"### {emoji} {phase_name} ({i+1}/{duration})")
                time.sleep(1)
        
        st.session_state.breathing_cycles += 1
        
        if st.session_state.breathing_cycles >= 3:
            st.session_state.breathing_active = False
            st.success(f"🎉 Excellent! You completed 3 breathing cycles. Feel the calm energy flowing through you! 🧘‍♀️")
            st.balloons()
    
    if st.session_state.breathing_cycles > 0:
        st.markdown(f"""
        <div class="score-display">
            Breathing Cycles Completed: {st.session_state.breathing_cycles} 🫁<br>
            Mindfulness Level: {"🧘‍♀️" * min(5, st.session_state.breathing_cycles)}
        </div>
        """, unsafe_allow_html=True)

# Additional utility functions for games
def reset_all_games():
    """Reset all game states"""
    game_keys = [
        'memory_sequence', 'user_sequence', 'memory_level', 'memory_score', 'show_sequence', 'game_over',
        'color_score', 'stress_clicks', 'stress_level', 'word_chain', 'word_score',
        'breathing_active', 'breathing_cycles', 'current_game'
    ]
    
    for key in game_keys:
        if key in st.session_state:
            del st.session_state[key]

def get_games_statistics():
    """Get user's gaming statistics"""
    stats = {
        'memory_high_score': st.session_state.get('memory_score', 0),
        'color_wisdom_score': st.session_state.get('color_score', 0),
        'stress_relief_clicks': st.session_state.get('stress_clicks', 0),
        'positive_word_score': st.session_state.get('word_score', 0),
        'breathing_cycles': st.session_state.get('breathing_cycles', 0)
    }
    return stats

if __name__ == "__main__":
    show_games_page()