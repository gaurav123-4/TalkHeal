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
        <div class="game-header-inner">
            <div class="game-title">🎮 TalkHeal Games</div>
            <div class="game-sub">Interactive, bite-sized activities to boost focus, reduce stress, and build positive habits.</div>
            <div class="game-badges">
                <span class="badge">✨ Quick</span>
                <span class="badge">🌈 Fun</span>
                <span class="badge">💚 Therapeutic</span>
            </div>
        </div>
    </div>

    <style>
    /* header visuals */
    .game-header { background: linear-gradient(120deg, #ffd1e6 0%, #ffb6c1 60%, #ffc0cb 100%); padding: 1.8rem; border-radius: 16px; color: #4a2b3a; margin-bottom: 1rem; box-shadow: 0 10px 30px rgba(14,21,47,0.06); position:relative; overflow:hidden; }
    .game-header:before { content:""; position:absolute; inset:0; background: radial-gradient(circle at 10% 20%, rgba(255,255,255,0.03), transparent 8%), radial-gradient(circle at 90% 80%, rgba(255,255,255,0.02), transparent 8%); pointer-events:none; }
    .game-header-inner { max-width: 980px; margin: 0 auto; text-align: center; position:relative; z-index:1; }
    .game-title { font-size: 3.6rem; font-weight: 900; margin-bottom: 6px; background: linear-gradient(90deg,#7a2b6b,#ff6b9a); -webkit-background-clip:text; color:transparent; letter-spacing: -0.03em; text-shadow: 0 6px 18px rgba(122,43,107,0.12); font-family: 'Inter', 'Segoe UI', Roboto, -apple-system, 'Helvetica Neue', Arial, sans-serif; }
    .game-sub { color: rgba(74,43,58,0.85); margin-bottom: 12px; font-size: 1rem; }
    .game-badges { display:flex; gap:10px; justify-content:center; margin-bottom:12px; }
    .badge { background: rgba(255, 255, 255, 0.12); padding:8px 14px; border-radius:999px; font-weight:700; box-shadow: 0 6px 18px rgba(11,22,55,0.08); transition: transform 160ms ease, box-shadow 160ms ease; }
    .badge:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(11,22,55,0.12); }
    @media (max-width: 600px) { .game-title { font-size:2rem; } .game-sub { font-size:0.95rem; } .badge{padding:6px 10px;} }
    </style>
    """, unsafe_allow_html=True)
    
    # Game selection
    games = [
        ("🎯 Reaction Time", "reaction_game", "Test and improve your reflexes with a quick reaction timer."),
        ("🎨 Mood Color Match", "color_mood_game", "Express and explore emotions using color choices."),
        ("😌 Stress Relief Clicker", "stress_clicker_game", "Release tension with a simple, calming clicker."),
        ("💭 Positive Word Association", "word_association_game", "Build a chain of uplifting words to boost positivity."),
        ("🫁 Breathing Pattern Game", "breathing_game", "Guided breathing exercises to relax and center yourself.")
    ]

    st.markdown(
        """
    <div style='text-align:center; margin-top: 12px; margin-bottom: 8px;'>
        <h2 style='margin:0; font-weight:800; letter-spacing: -0.01em; color: #4a2b3a;'>Choose Your Wellness Game</h2>
        <p style='margin:4px 0 0; color: rgba(74,43,58,0.7);'>Pick a short activity to feel better right now</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Beautified selection CSS
    st.markdown("""
    <style>
    .game-selection-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; align-items: stretch; }
    .game-card-select { background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)); border-radius: 12px; padding: 14px; text-align:center; box-shadow: 0 8px 24px rgba(11,22,55,0.06); transition: transform .18s ease, box-shadow .18s ease; }
    .game-card-select:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(11,22,55,0.10); }
    .game-card-title { font-size:1.15rem; font-weight:800; margin-bottom:6px; }
    .game-card-desc { font-size:0.9rem; color: rgba(11,22,55,0.65); margin-bottom: 10px; min-height: 44px; }
    .play-btn { background: linear-gradient(90deg, #ff7aa2, #ffb3c7); color: white; border: none; padding: 10px 14px; border-radius: 999px; font-weight:700; cursor:pointer; }
    .play-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 26px rgba(122,43,107,0.12); }
    @media (max-width: 640px) { .game-card-desc { min-height: auto; } .game-card-title { font-size:1rem; } }
    </style>
    """, unsafe_allow_html=True)

    # Render cards using Streamlit columns so we can center the Play button inside each card
    ncols = min(3, len(games))  # up to 3 columns on wide screens
    for i in range(0, len(games), ncols):
        row = games[i:i+ncols]
        cols = st.columns(len(row), gap="large")
        for col, (name, key, desc) in zip(cols, row):
            with col:
                card_html = f"""
                <div class='game-card-select'>
                    <div class='game-card-title'>{name}</div>
                    <div class='game-card-desc'>{desc}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                # Create inner columns to center the Play button visually
                inner = st.columns([1, 2, 1])
                with inner[1]:
                    if st.button("Play", key=f"select_{key}"):
                        st.session_state.current_game = key
    
    # Display selected game
    if 'current_game' in st.session_state:
        st.markdown("---")
        
        if st.session_state.current_game == "reaction_game":
            reaction_time_game()
        elif st.session_state.current_game == "color_mood_game":
            mood_color_matching_game()
        elif st.session_state.current_game == "stress_clicker_game":
            stress_relief_clicker()
        elif st.session_state.current_game == "word_association_game":
            positive_word_association()
        elif st.session_state.current_game == "breathing_game":
            breathing_pattern_game()

def memory_challenge_game():
    """Simplified Simon-style memory game optimized for reliability and clarity.

    Rules:
    - Press Start to begin (or the sequence will auto-start on first visit).
    - Watch the shown colors one-by-one.
    - After the sequence shows, click the colors in the same order.
    - A wrong click ends the game; correct full sequence advances the level.
    """
    st.markdown("""
    <div class="game-card">
        <h3>🧠 Memory Challenge (Simple)</h3>
        <p>Watch the sequence, then repeat it. The sequence grows by one color each level.</p>
    </div>
    """, unsafe_allow_html=True)

    # Define colors as (key, emoji) pairs for stable keys and display
    color_options = [
        ("red", "🔴"),
        ("yellow", "🟡"),
        ("green", "🟢"),
        ("blue", "🔵"),
    ]

    # Difficulty setting controls how quickly the sequence shows and starting length
    difficulty = st.selectbox("Difficulty:", ["Easy", "Normal", "Hard"], key="memory_difficulty")
    speed_map = {"Easy": 0.8, "Normal": 0.55, "Hard": 0.35}
    start_length = {"Easy": 1, "Normal": 1, "Hard": 2}

    # Initialize session state
    if 'memory_sequence' not in st.session_state:
        st.session_state.memory_sequence = []
        st.session_state.user_sequence = []
        st.session_state.memory_level = 0
        st.session_state.memory_score = 0
        st.session_state.show_sequence = False
        st.session_state.game_over = False

    # Auto-start with a color if sequence empty
    if not st.session_state.memory_sequence:
        st.session_state.memory_sequence = [random.choice([c for k, c in color_options]) for _ in range(start_length.get(difficulty, 1))]
        st.session_state.user_sequence = []
        st.session_state.memory_level = len(st.session_state.memory_sequence)
        st.session_state.show_sequence = True

    # Header / controls
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div class="score-display">
            Level: {st.session_state.memory_level}<br>
            Score: {st.session_state.memory_score}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🚀 Start New Game", key="start_memory_simple"):
            st.session_state.memory_sequence = [random.choice([c for k, c in color_options])]
            st.session_state.user_sequence = []
            st.session_state.memory_level = 1
            st.session_state.memory_score = 0
            st.session_state.show_sequence = True
            st.session_state.game_over = False
            st.rerun()

    # Display sequence visually (centered big emoji) without forcing unnecessary reruns
    display = st.empty()
    if st.session_state.show_sequence and not st.session_state.game_over:
        display.markdown("### 🔍 Watch the sequence...")
        big = st.empty()
        show_speed = speed_map.get(difficulty, 0.55)
        for idx, color in enumerate(st.session_state.memory_sequence):
            big.markdown(f"<div style='font-size:72px; text-align:center'>{color}</div>", unsafe_allow_html=True)
            time.sleep(show_speed)
            big.markdown("<div style='font-size:28px; text-align:center'>...</div>", unsafe_allow_html=True)
            time.sleep(0.15)
        # Clear big display and allow player to interact
        big.empty()
        display.empty()
        st.session_state.show_sequence = False
        st.session_state.user_sequence = []

    # If game over, show result and offer restart
    if st.session_state.game_over:
        st.error("❌ Wrong sequence! Game Over!")
        st.markdown(f"**Final score:** {st.session_state.memory_score} — **Level reached:** {st.session_state.memory_level}")
        if st.button("🔁 Restart", key="restart_memory_simple"):
            st.session_state.memory_sequence = []
            st.session_state.user_sequence = []
            st.session_state.memory_level = 0
            st.session_state.memory_score = 0
            st.session_state.show_sequence = True
            st.session_state.game_over = False
            st.experimental_rerun()
        return

    st.write("Click the colors in the same order you saw them:")

    # Render buttons in a 2x2 grid (interactive)
    for r in range(2):
        cols = st.columns(2)
        for c in range(2):
            idx = r * 2 + c
            key_name, emoji = color_options[idx]
            with cols[c]:
                # Disable buttons while sequence is showing
                disabled = st.session_state.show_sequence or st.session_state.game_over
                if st.button(emoji, key=f"mem_btn_{key_name}", use_container_width=True, disabled=disabled):
                    # Append and check
                    st.session_state.user_sequence.append(emoji)
                    pos = len(st.session_state.user_sequence) - 1
                    # Safe comparison
                    if pos < len(st.session_state.memory_sequence):
                        if st.session_state.user_sequence[pos] != st.session_state.memory_sequence[pos]:
                            st.session_state.game_over = True
                        else:
                            # If user completed the sequence correctly
                            if len(st.session_state.user_sequence) == len(st.session_state.memory_sequence):
                                st.session_state.memory_score += 10 * st.session_state.memory_level
                                st.session_state.memory_level += 1
                                # Add a new random color
                                st.session_state.memory_sequence.append(random.choice([c for k, c in color_options]))
                                st.session_state.show_sequence = True
                                st.session_state.user_sequence = []
                                st.success(f"✅ Correct! Advancing to level {st.session_state.memory_level}")
                    else:
                        # Defensive fallback
                        st.session_state.game_over = True
                    # update view
                    st.experimental_rerun()

    # Show current typed sequence (for feedback)
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

    # Initialize score and history
    if 'color_score' not in st.session_state:
        st.session_state.color_score = 0
    if 'color_history' not in st.session_state:
        st.session_state.color_history = []  # list of (mood, chosen, correct)
    if 'mood_locked' not in st.session_state:
        st.session_state.mood_locked = False
    if 'mood_hint_shown' not in st.session_state:
        st.session_state.mood_hint_shown = False

    st.markdown("**Match the emotion with the color that represents it:**")

    # Pick or keep current mood in session state so hints and 'next' work predictably
    if 'mood_current' not in st.session_state or st.button("Next Mood", key="mood_next"):
        st.session_state.mood_current = random.choice(list(mood_colors.keys()))
        # build options once per mood
        correct_color = mood_colors[st.session_state.mood_current]
        all_colors = list(set(mood_colors.values()))
        wrong_colors = [c for c in all_colors if c != correct_color]
        options = [correct_color] + random.sample(wrong_colors, min(3, len(wrong_colors)))
        random.shuffle(options)
        st.session_state.mood_options = options
        st.session_state.mood_locked = False
        st.session_state.mood_hint_shown = False

    current_mood = st.session_state.mood_current
    options = st.session_state.get('mood_options')
    correct_color = mood_colors[current_mood]

    # Header row with hint and quick stats
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.write(f"### Current Emotion: {current_mood}")
    with c2:
        if st.button("Hint", key="mood_hint"):
            st.session_state.mood_hint_shown = True
    with c3:
        st.write(f"Streak: {sum(1 for h in st.session_state.color_history if h[2])}")

    # Show hint if requested
    if st.session_state.mood_hint_shown:
        fact_map = {
            "🟡": "Yellow is associated with happiness, optimism, and mental clarity!",
            "🔵": "Blue represents calmness and can help reduce anxiety and stress.",
            "🔴": "Red is linked to strong emotions like passion, energy, and sometimes anger.",
            "🟢": "Green promotes balance, harmony, and has a calming effect on the mind.",
            "🟣": "Purple is often associated with creativity, spirituality, and compassion.",
            "🟠": "Orange represents enthusiasm, creativity, and positive energy!"
        }
        st.info("💡 Hint: " + fact_map.get(correct_color, "Colors have powerful psychological effects!"))

    # Add improved CSS for larger circular buttons
    st.markdown("""
    <style>
    .mood-color-selection { display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin: 12px 0; }
    .mood-color-selection .stButton > button { font-size: 2.4rem !important; min-height: 84px !important; width: 84px !important; border-radius: 999px !important; }
    .mood-color-selection .stButton > button:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(11,22,55,0.08); }
    @media (max-width: 640px) { .mood-color-selection .stButton > button { font-size: 2rem !important; min-height: 64px !important; width: 64px !important; } }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="mood-color-selection">', unsafe_allow_html=True)

    # Render options (disable after a choice until Next Mood)
    for i, color in enumerate(options):
        disabled = st.session_state.mood_locked
        if st.button(color, key=f"color_choice_{i}", use_container_width=False, disabled=disabled):
            # process choice
            chosen = color
            correct = chosen == correct_color
            st.session_state.color_history.insert(0, (current_mood, chosen, correct))
            if correct:
                st.session_state.color_score += 10
                st.success("🎉 Perfect match! Colors can really reflect our emotions!")
                # show fact after correct
                facts = {
                    "🟡": "Yellow is associated with happiness, optimism, and mental clarity!",
                    "🔵": "Blue represents calmness and can help reduce anxiety and stress.",
                    "🔴": "Red is linked to strong emotions like passion, energy, and sometimes anger.",
                    "🟢": "Green promotes balance, harmony, and has a calming effect on the mind.",
                    "🟣": "Purple is often associated with creativity, spirituality, and compassion.",
                    "🟠": "Orange represents enthusiasm, creativity, and positive energy!"
                }
                st.info(f"💡 {facts.get(correct_color)}")
            else:
                st.error("😕 That's not the typical match — try the next one or read the hint.")
            st.session_state.mood_locked = True

    st.markdown('</div>', unsafe_allow_html=True)

    # Right column: score and recent history
    hist_col1, hist_col2 = st.columns([1, 2])
    with hist_col1:
        st.markdown(f"""
        <div class="score-display">
            Color Wisdom Score: {st.session_state.color_score} 🎨
        </div>
        """, unsafe_allow_html=True)
    with hist_col2:
        st.markdown("**Recent choices**")
        if st.session_state.color_history:
            for mood, chosen, correct in st.session_state.color_history[:6]:
                icon = "✅" if correct else "❌"
                st.write(f"{icon} {mood} → {chosen}")
        else:
            st.write("No rounds played yet. Try one!")

    # Next Mood control (also reset lock/hint)
    if st.button("Next Mood", key="mood_next_bottom"):
        st.session_state.mood_current = random.choice(list(mood_colors.keys()))
        correct_color = mood_colors[st.session_state.mood_current]
        all_colors = list(set(mood_colors.values()))
        wrong_colors = [c for c in all_colors if c != correct_color]
        options = [correct_color] + random.sample(wrong_colors, min(3, len(wrong_colors)))
        random.shuffle(options)
        st.session_state.mood_options = options
        st.session_state.mood_locked = False
        st.session_state.mood_hint_shown = False

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
    if 'calm_streak' not in st.session_state:
        st.session_state.calm_streak = 0
    
    # Visual stress ball (rendered as a circle whose size shrinks as you calm down)
    stress_ball_size = max(48, 150 - (st.session_state.stress_clicks * 3))

    st.markdown(f"""
    <div style='text-align:center; margin: 8px 0 16px;'>
      <div style='display:inline-block; width:{stress_ball_size}px; height:{stress_ball_size}px; border-radius:50%; background: radial-gradient(circle at 30% 30%, #ff6b6b, #e04343); box-shadow: 0 8px 24px rgba(224,67,67,0.18);'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Release Stress", key="stress_ball", help="Click me to release stress!"):
            st.session_state.stress_clicks += 1
            prev_level = st.session_state.stress_level
            st.session_state.stress_level = max(0, st.session_state.stress_level - 2)

            # Encouraging messages
            messages = [
                "Deep breath... you're doing great! 🌟",
                "Feel the tension melting away... 😌", 
                "Each click brings more peace... ✨",
                "You're stronger than your stress! 💪",
                "Breathe in calm, breathe out tension... 🫁"
            ]

            # increase calm streak when progress is made, reset if no progress
            if st.session_state.stress_level < prev_level:
                st.session_state.calm_streak += 1
            else:
                st.session_state.calm_streak = 0

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
    
    # Small controls and tips
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("Reset", key="stress_reset"):
            st.session_state.stress_clicks = 0
            st.session_state.stress_level = 100
            st.session_state.calm_streak = 0
            st.experimental_rerun()
    with c2:
        if st.button("Tip", key="stress_tip"):
            tips = [
                "Try inhaling for 4 seconds, hold 2, exhale for 6.",
                "Close your eyes and imagine a peaceful place for 20 seconds.",
                "Place both feet flat on the floor and feel the support beneath you.",
            ]
            st.info(random.choice(tips))
        with c3:
                st.markdown(f"""
                <div style='text-align:right'>
                    <strong>Calm streak:</strong> {st.session_state.calm_streak}  <br>
                    <strong>Clicks:</strong> {st.session_state.stress_clicks}
                </div>
                """, unsafe_allow_html=True)

def reaction_time_game():
    """Simple reaction time tester to replace the unstable memory game."""
    st.markdown("""
    <div class="game-card">
        <h3>🎯 Reaction Time Test</h3>
        <p>Wait for the green circle, then click as fast as you can. Measure your reaction time!</p>
    </div>
    """, unsafe_allow_html=True)

    if 'reaction_state' not in st.session_state:
        st.session_state.reaction_state = 'idle'  # idle | waiting | ready | result
        st.session_state.reaction_start = None
        st.session_state.reaction_time = None
        st.session_state.reaction_attempts = []
        st.session_state.reaction_best = None

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🔄 Start Test", key="start_reaction"):
            st.session_state.reaction_state = 'waiting'
            st.session_state.reaction_start = None
            st.session_state.reaction_time = None
            st.rerun()

    with col2:
        if st.button("📊 Show Results", key="show_reaction_results"):
            if st.session_state.reaction_attempts:
                avg = sum(st.session_state.reaction_attempts) / len(st.session_state.reaction_attempts)
                best = min(st.session_state.reaction_attempts)
                last = st.session_state.reaction_attempts[-1]
                st.metric("Last", f"{last*1000:.0f} ms")
                st.metric("Best", f"{best*1000:.0f} ms")
                st.metric("Average", f"{avg*1000:.0f} ms")
            else:
                st.info("No attempts recorded yet.")
        if st.button("Clear Results", key="clear_reaction_results"):
            st.session_state.reaction_attempts = []
            st.session_state.reaction_best = None
            st.session_state.reaction_time = None
            st.experimental_rerun()

    # Waiting state: after pressing Start, wait a random interval then prompt user
    if st.session_state.reaction_state == 'waiting':
        wait_sec = random.uniform(1.0, 3.0)
        st.write("Get ready... Wait for green...")
        # Use a blocking sleep to simulate wait then set ready state
        time.sleep(wait_sec)
        st.session_state.reaction_state = 'ready'
        st.session_state.reaction_start = time.time()
        st.rerun()

    if st.session_state.reaction_state == 'ready':
        # Show green target to click
        if st.button("🟢 CLICK!", key="reaction_click", use_container_width=True):
            end = time.time()
            rt = end - (st.session_state.reaction_start or end)
            st.session_state.reaction_time = rt
            st.session_state.reaction_attempts.append(rt)
            st.session_state.reaction_state = 'result'
            st.rerun()
        else:
            st.write("Click the green button as fast as you can!")

    if st.session_state.reaction_state == 'result':
        # Display last result and update best
        rt = st.session_state.reaction_time or 0.0
        st.success(f"Your reaction time: {rt*1000:.0f} ms")
        # update best/attempts safely
        if rt > 0:
            if 'reaction_attempts' not in st.session_state:
                st.session_state.reaction_attempts = [rt]
            else:
                st.session_state.reaction_attempts.append(rt)
            if st.session_state.reaction_best is None or rt < st.session_state.reaction_best:
                st.session_state.reaction_best = rt

        if st.button("Try again", key="reaction_try_again"):
            st.session_state.reaction_state = 'idle'
            st.session_state.reaction_start = None
            st.session_state.reaction_time = None
            st.rerun()

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
    if 'saved_chains' not in st.session_state:
        st.session_state.saved_chains = []  # list of lists
    
    if not st.session_state.word_chain:
        starter_word = random.choice(positive_words)
        st.session_state.word_chain.append(starter_word)
    
    st.write("**Build a chain of positive words! Each word should relate to the previous one:**")
    st.write(f"### Current chain: {' → '.join(st.session_state.word_chain)}")
    
    # Suggestion chips to inspire the next word
    st.markdown("**Suggestions:**")
    sugg_cols = st.columns(6)
    suggestions = random.sample(positive_words, min(6, len(positive_words)))
    for i, word in enumerate(suggestions):
        with sugg_cols[i % 6]:
            if st.button(word, key=f"suggest_{i}"):
                # push suggestion into input by appending directly
                st.session_state.word_chain.append(word)
                st.session_state.word_score += 5
                st.success(f"Nice! '{word}' fits beautifully.")

    # Input for next word with add/undo/save controls
    next_word = st.text_input("Add the next positive word:", key="word_input")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("✅ Add Word", key="add_word") and next_word:
            candidate = next_word.strip().title()
            if candidate and candidate not in st.session_state.word_chain:
                st.session_state.word_chain.append(candidate)
                st.session_state.word_score += 5
                encouragements = [
                    f"Beautiful connection! '{candidate}' adds wonderful energy! ✨",
                    f"Perfect! '{candidate}' brings such positive vibes! 🌟", 
                    f"Excellent! Your mind is creating beautiful associations! 💫",
                    f"Amazing! '{candidate}' flows perfectly with positive energy! 🌈"
                ]
                st.success(random.choice(encouragements))
            else:
                st.warning("That word is already in the chain or empty. Try a new one or pick a suggestion.")
            # clear input by resetting the widget key
            st.session_state['word_input'] = ''
            st.rerun()

    with col2:
        if st.button("↩️ Undo Last", key="undo_word"):
            if len(st.session_state.word_chain) > 1:
                removed = st.session_state.word_chain.pop()
                st.info(f"Removed '{removed}' from the chain.")
                st.session_state.word_score = max(0, st.session_state.word_score - 5)
            else:
                st.warning("Can't remove the starter word.")
            st.rerun()

    with col3:
        if st.button("💾 Save Chain", key="save_chain"):
            # save a copy, avoid duplicates
            snapshot = st.session_state.word_chain.copy()
            if snapshot not in st.session_state.saved_chains:
                st.session_state.saved_chains.insert(0, snapshot)
                st.success("Chain saved! You can view saved chains below.")
            else:
                st.info("This chain is already saved.")
            st.rerun()
    
    st.markdown(f"""
    <div class="score-display">
        Positivity Score: {st.session_state.word_score} ✨<br>
        Chain Length: {len(st.session_state.word_chain)} words
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.word_chain) >= 10:
        st.success("🎉 Amazing! You've created a beautiful chain of positivity! Your mind is becoming more attuned to positive thoughts! 🌟")

    # Display saved chains (recent first)
    if st.session_state.saved_chains:
        st.markdown("### Saved chains")
        for i, chain in enumerate(st.session_state.saved_chains[:6]):
            st.write(f"{i+1}. {' → '.join(chain)}")
        if st.button("Clear saved chains", key="clear_saved_chains"):
            st.session_state.saved_chains = []
            st.experimental_rerun()

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
    
    # breathing state
    if 'breathing_active' not in st.session_state:
        st.session_state.breathing_active = False
        st.session_state.breathing_cycles = 0
        st.session_state.breathing_mode = 'Guided'  # Guided | Auto
        st.session_state.breathing_phase = None
        st.session_state.breathing_phase_step = 0

    # Mode selector: Guided avoids long blocking sleeps by advancing step-by-step
    col_mode, _ = st.columns([3, 1])
    with col_mode:
        st.session_state.breathing_mode = st.selectbox("Mode:", ["Guided", "Auto"], index=0, key="breath_mode_select")

    # Controls
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶️ Start", key="start_breathing"):
            st.session_state.breathing_active = True
            st.session_state.breathing_phase = 0
            st.session_state.breathing_phase_step = 0
            # reset cycles when starting fresh
            if st.session_state.breathing_cycles == 0:
                st.session_state.breathing_cycles = 0
            st.experimental_rerun()
    with c2:
        if st.button("⏸️ Pause", key="pause_breathing"):
            st.session_state.breathing_active = False
            st.experimental_rerun()
    with c3:
        if st.button("⏹️ Stop", key="stop_breathing"):
            st.session_state.breathing_active = False
            st.session_state.breathing_phase = None
            st.session_state.breathing_phase_step = 0
            st.experimental_rerun()

    # A small display area
    progress_bar = st.progress(0)
    status_text = st.empty()

    cycle_phases = [
        ("Inhale slowly...", pattern["inhale"], "🌬️➡️"),
        ("Hold your breath...", pattern["hold"], "⏸️"),
        ("Exhale gently...", pattern["exhale"], "🌬️⬅️")
    ]

    # Auto mode: keep the existing blocking behavior (short waits) for a fully automated session
    if st.session_state.breathing_mode == 'Auto' and st.session_state.breathing_active:
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
        st.experimental_rerun()

    # Guided mode: advance one second/step per user-visible rerun (no long blocking)
    if st.session_state.breathing_mode == 'Guided' and st.session_state.breathing_active:
        # ensure phase index is valid
        phase_idx = st.session_state.breathing_phase or 0
        phase_name, duration, emoji = cycle_phases[phase_idx]
        step = st.session_state.breathing_phase_step
        # advance current phase by one step
        progress = (step + 1) / duration
        progress_bar.progress(progress)
        status_text.markdown(f"### {emoji} {phase_name} ({step+1}/{duration})")

        # schedule next step: use a small sleep to let UI update, then increment step and rerun
        time.sleep(1)
        step += 1
        if step >= duration:
            # move to next phase
            phase_idx = (phase_idx + 1) % len(cycle_phases)
            step = 0
            if phase_idx == 0:
                st.session_state.breathing_cycles += 1
                # completed one full cycle
                if st.session_state.breathing_cycles >= 3:
                    st.session_state.breathing_active = False
                    st.success(f"🎉 Excellent! You completed 3 breathing cycles. Feel the calm energy flowing through you! 🧘‍♀️")
                    st.balloons()
        st.session_state.breathing_phase = phase_idx
        st.session_state.breathing_phase_step = step
        st.experimental_rerun()
    
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