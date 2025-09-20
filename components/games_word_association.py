import streamlit as st
import random
import time
from datetime import datetime

def positive_word_association_game():
    """Complete Positive Word Association Game for cognitive restructuring and positive thinking"""
    
    st.markdown("### 💭 Positive Word Association Game")
    st.markdown("**Transform negative thoughts into positive ones - Build optimistic thinking patterns!**")
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Games", key="back_word"):
            st.rerun()
    
    # Initialize game state
    if "word_score" not in st.session_state:
        st.session_state.word_score = 0
    if "word_round" not in st.session_state:
        st.session_state.word_round = 0
    if "word_total_rounds" not in st.session_state:
        st.session_state.word_total_rounds = 10
    if "word_streak" not in st.session_state:
        st.session_state.word_streak = 0
    if "word_game_completed" not in st.session_state:
        st.session_state.word_game_completed = False
    if "word_start_time" not in st.session_state:
        st.session_state.word_start_time = None
    if "positive_mindset_level" not in st.session_state:
        st.session_state.positive_mindset_level = 0
    
    # Comprehensive word transformation pairs for cognitive restructuring
    word_pairs = [
        {
            "negative": "Failure", 
            "positive": ["Learning", "Growth", "Experience", "Opportunity"],
            "distractors": ["Disaster", "Shame", "Worthless", "Defeat"],
            "explanation": "Reframing failure as learning helps build resilience and growth mindset.",
            "therapy_note": "This cognitive restructuring technique is used in CBT to combat perfectionism and fear of failure."
        },
        {
            "negative": "Stress", 
            "positive": ["Challenge", "Motivation", "Energy", "Focus"],
            "distractors": ["Overwhelming", "Impossible", "Crushing", "Hopeless"],
            "explanation": "Viewing stress as a challenge activates problem-solving rather than avoidance.",
            "therapy_note": "Research shows that people who view stress as enhancing perform better under pressure."
        },
        {
            "negative": "Problem", 
            "positive": ["Solution", "Puzzle", "Adventure", "Discovery"],
            "distractors": ["Crisis", "Nightmare", "Burden", "Trap"],
            "explanation": "Problems become opportunities for creative thinking and personal development.",
            "therapy_note": "Solution-focused therapy emphasizes reframing problems as puzzles to solve."
        },
        {
            "negative": "Mistake", 
            "positive": ["Lesson", "Progress", "Insight", "Improvement"],
            "distractors": ["Disaster", "Stupidity", "Failure", "Embarrassment"],
            "explanation": "Mistakes are valuable learning experiences that lead to wisdom and growth.",
            "therapy_note": "Self-compassion therapy teaches treating mistakes as part of the human experience."
        },
        {
            "negative": "Difficult", 
            "positive": ["Rewarding", "Strengthening", "Character-building", "Empowering"],
            "distractors": ["Impossible", "Crushing", "Defeating", "Overwhelming"],
            "explanation": "Difficult experiences build resilience, skills, and inner strength.",
            "therapy_note": "Post-traumatic growth theory shows how challenges can lead to positive transformation."
        },
        {
            "negative": "Rejection", 
            "positive": ["Redirection", "Protection", "New-path", "Better-fit"],
            "distractors": ["Worthless", "Unloved", "Inadequate", "Hopeless"],
            "explanation": "Rejection often redirects us toward better opportunities and relationships.",
            "therapy_note": "Cognitive reframing helps process rejection as guidance rather than judgment."
        },
        {
            "negative": "Change", 
            "positive": ["Growth", "Adventure", "Opportunity", "Evolution"],
            "distractors": ["Loss", "Chaos", "Threat", "Destruction"],
            "explanation": "Change brings new possibilities, experiences, and personal development.",
            "therapy_note": "Acceptance and Commitment Therapy helps embrace change as natural and beneficial."
        },
        {
            "negative": "Criticism", 
            "positive": ["Feedback", "Insight", "Guidance", "Improvement"],
            "distractors": ["Attack", "Hatred", "Judgment", "Rejection"],
            "explanation": "Constructive criticism provides valuable information for personal growth.",
            "therapy_note": "Learning to separate criticism of actions from criticism of self is key to emotional health."
        },
        {
            "negative": "Anxiety", 
            "positive": ["Preparation", "Awareness", "Motivation", "Sensitivity"],
            "distractors": ["Terror", "Weakness", "Madness", "Failure"],
            "explanation": "Anxiety can be reframed as your mind's way of preparing and staying alert.",
            "therapy_note": "Mindfulness-based approaches teach viewing anxiety as information rather than threat."
        },
        {
            "negative": "Loneliness", 
            "positive": ["Self-discovery", "Independence", "Reflection", "Freedom"],
            "distractors": ["Abandonment", "Worthlessness", "Isolation", "Despair"],
            "explanation": "Solitude provides opportunities for self-reflection and personal growth.",
            "therapy_note": "Distinguishing between chosen solitude and unwanted loneliness is therapeutic."
        }
    ]
    
    # Display game statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h4>Score</h4>
            <h2>{st.session_state.word_score}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_round = min(st.session_state.word_round + 1, st.session_state.word_total_rounds)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h4>Round</h4>
            <h2>{current_round}/{st.session_state.word_total_rounds}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: #333;">
            <h4>Streak</h4>
            <h2>{st.session_state.word_streak}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        mindset_color = "#4CAF50" if st.session_state.positive_mindset_level > 70 else "#FFC107" if st.session_state.positive_mindset_level > 40 else "#FF9800"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {mindset_color} 0%, {mindset_color}99 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h4>Positivity</h4>
            <h2>{st.session_state.positive_mindset_level}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Game instructions
    if st.session_state.word_round == 0 and not st.session_state.word_game_completed:
        st.markdown("""
        ### 📖 How Cognitive Reframing Works:
        
        **What is Cognitive Reframing?**
        Cognitive reframing is a therapeutic technique used to identify and change negative thought patterns. 
        It's a core component of Cognitive Behavioral Therapy (CBT) and helps build mental resilience.
        
        **How to Play:**
        1. **Read the negative word** presented to you
        2. **Choose the positive reframe** from the options given
        3. **Learn the psychology** behind each transformation
        4. **Build new neural pathways** for optimistic thinking
        5. **Apply these techniques** in your daily life
        
        ### 🧠 Mental Health Benefits:
        - **Reduces Depression:** Breaks negative thought cycles
        - **Decreases Anxiety:** Transforms worry into constructive thinking
        - **Builds Resilience:** Develops coping strategies for challenges
        - **Improves Self-Esteem:** Replaces self-criticism with self-compassion
        - **Enhances Problem-Solving:** Shifts from problem-focus to solution-focus
        """)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🧠 Start Cognitive Training", key="start_word_game", type="primary"):
                st.session_state.word_start_time = datetime.now()
                st.rerun()
    
    # Game play
    elif st.session_state.word_round < st.session_state.word_total_rounds and not st.session_state.word_game_completed:
        current_pair = word_pairs[st.session_state.word_round]
        
        # Display the negative thought prominently
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;">
            <h3 style="margin: 0;">Negative Thought:</h3>
            <h1 style="margin: 0.5rem 0; font-size: 3rem;">"{current_pair['negative']}"</h1>
            <p style="margin: 0; font-size: 1.2rem;">How can we reframe this into something positive?</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔄 **Choose the best positive reframe:**")
        
        # Create options (positive + distractors)
        all_options = current_pair['positive'] + current_pair['distractors']
        random.shuffle(all_options)
        
        # Create buttons in a 2x4 grid
        cols1 = st.columns(4)
        cols2 = st.columns(4)
        all_cols = cols1 + cols2
        
        for i, (col, option) in enumerate(zip(all_cols, all_options)):
            with col:
                # Style buttons based on whether they're positive or negative
                if option in current_pair['positive']:
                    button_style = "primary"
                    help_text = f"This is a positive reframe of '{current_pair['negative']}'"
                else:
                    button_style = "secondary"  
                    help_text = f"This maintains negative thinking about '{current_pair['negative']}'"
                
                if st.button(f"💭 {option}", key=f"word_option_{i}", 
                           help=help_text, use_container_width=True):
                    
                    if option in current_pair['positive']:
                        # Correct positive reframe
                        st.session_state.word_score += 10
                        st.session_state.word_streak += 1
                        st.session_state.positive_mindset_level = min(100, st.session_state.positive_mindset_level + 8)
                        
                        success_messages = [
                            f"✅ **Excellent reframe!** '{option}' transforms '{current_pair['negative']}' into an opportunity for growth!",
                            f"🌟 **Perfect choice!** Viewing '{current_pair['negative']}' as '{option}' builds resilience and optimism!",
                            f"🎯 **Outstanding!** This cognitive restructuring helps break negative thought patterns!",
                            f"💪 **Brilliant thinking!** You've successfully reframed limiting beliefs into empowering ones!"
                        ]
                        
                        st.success(random.choice(success_messages))
                        
                        # Show educational content
                        st.info(f"🧠 **Why this works:** {current_pair['explanation']}")
                        st.markdown(f"🔬 **Therapy insight:** {current_pair['therapy_note']}")
                        
                        # Streak bonuses
                        if st.session_state.word_streak == 3:
                            st.balloons()
                            st.success("🔥 Amazing! 3 correct reframes in a row! You're building powerful positive thinking habits!")
                        elif st.session_state.word_streak == 5:
                            st.balloons()
                            st.success("🚀 Incredible! 5-streak! Your cognitive flexibility is improving dramatically!")
                        elif st.session_state.word_streak >= 7:
                            st.balloons()
                            st.success("👑 Cognitive Reframing Master! You've developed expert-level positive thinking skills!")
                        
                    else:
                        # Incorrect - chose negative option
                        st.session_state.word_streak = 0
                        st.session_state.positive_mindset_level = max(0, st.session_state.positive_mindset_level - 3)
                        
                        st.error(f"❌ **This maintains negative thinking.** '{option}' keeps you stuck in a limiting mindset.")
                        
                        # Show what positive reframes were available
                        positive_options = ", ".join(current_pair['positive'])
                        st.info(f"💡 **Better reframes:** {positive_options}")
                        st.markdown(f"🔄 **Remember:** {current_pair['explanation']}")
                    
                    st.session_state.word_round += 1
                    time.sleep(3)
                    st.rerun()
        
        # Progress indicator
        progress = st.session_state.word_round / st.session_state.word_total_rounds
        st.progress(progress, f"Progress: {st.session_state.word_round}/{st.session_state.word_total_rounds} reframes completed")
        
        # Show current streak if > 0
        if st.session_state.word_streak > 0:
            st.markdown(f"🔥 **Current streak: {st.session_state.word_streak} correct reframes!**")
    
    # Game completion
    elif st.session_state.word_round >= st.session_state.word_total_rounds or st.session_state.word_game_completed:
        st.session_state.word_game_completed = True
        
        # Final results
        st.balloons()
        st.markdown("### 🎉 **Cognitive Reframing Complete!**")
        
        final_percentage = round((st.session_state.word_score / (st.session_state.word_total_rounds * 10)) * 100)
        
        # Performance evaluation
        if final_percentage >= 90:
            st.success("🌟 **COGNITIVE RESTRUCTURING MASTER!** You have exceptional ability to transform negative thoughts into positive ones!")
            achievement = "Cognitive Behavioral Therapy Expert! 🧠✨"
            mindset_level = "Optimistic Thinker"
        elif final_percentage >= 70:
            st.success("🎯 **EXCELLENT REFRAMING SKILLS!** You're developing powerful positive thinking patterns!")
            achievement = "Positive Psychology Practitioner! 🧠💪"
            mindset_level = "Positive Thinker"
        elif final_percentage >= 50:
            st.success("👍 **GOOD PROGRESS!** You're learning to challenge negative thought patterns effectively!")
            achievement = "Cognitive Flexibility Builder! 🧠📈"
            mindset_level = "Growing Mindset"
        else:
            st.info("💪 **GREAT START!** Cognitive reframing is a skill that improves with practice. Every attempt strengthens your mental resilience!")
            achievement = "Mindset Explorer! 🧠🔍"
            mindset_level = "Learning Phase"
        
        # Detailed performance analysis
        if st.session_state.word_start_time:
            completion_time = (datetime.now() - st.session_state.word_start_time).seconds
            thinking_speed = completion_time / st.session_state.word_total_rounds
        else:
            completion_time = 0
            thinking_speed = 0
        
        st.markdown(f"""
        ### 📊 **Your Cognitive Reframing Results:**
        - **Final Score:** {st.session_state.word_score}/{st.session_state.word_total_rounds * 10} points ({final_percentage}%)
        - **Achievement Level:** {achievement}
        - **Thinking Style:** {mindset_level}
        - **Longest Streak:** {st.session_state.word_streak} consecutive correct reframes
        - **Positivity Level:** {st.session_state.positive_mindset_level}%
        - **Completion Time:** {completion_time} seconds
        - **Average Processing:** {thinking_speed:.1f} seconds per reframe
        
        ### 🧠 **How to Apply Cognitive Reframing in Daily Life:**
        
        **When you catch negative thoughts:**
        1. **PAUSE** - Notice the negative thought without judgment
        2. **IDENTIFY** - What specific words trigger negativity?
        3. **CHALLENGE** - Is this thought helpful or harmful?
        4. **REFRAME** - What's a more balanced, positive perspective?
        5. **PRACTICE** - Repeat the positive reframe until it feels natural
        
        **Real-world examples:**
        - **"I'm terrible at this"** → **"I'm learning and improving"**
        - **"This is impossible"** → **"This is challenging but doable"**
        - **"I always mess up"** → **"I'm human and I learn from mistakes"**
        - **"Nobody likes me"** → **"Some people connect with me, and that's enough"**
        
        ### 🎯 **Next Steps for Mental Health:**
        - Practice this technique for 5 minutes daily
        - Keep a thought record to track negative patterns
        - Use positive self-talk during stressful situations
        - Consider working with a therapist for deeper cognitive restructuring
        - Share these techniques with friends and family
        """)
        
        # Reset option
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Practice Again", key="restart_word_game", type="primary"):
                # Reset all game state
                st.session_state.word_score = 0
                st.session_state.word_round = 0
                st.session_state.word_streak = 0
                st.session_state.word_game_completed = False
                st.session_state.word_start_time = None
                # Keep positive_mindset_level to show cumulative progress
                st.success("Starting new cognitive reframing session!")
                st.rerun()
    
    # Control buttons during game
    if st.session_state.word_round > 0 and not st.session_state.word_game_completed:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Restart Training", key="restart_word"):
                st.session_state.word_score = 0
                st.session_state.word_round = 0
                st.session_state.word_streak = 0
                st.session_state.word_game_completed = False
                st.session_state.word_start_time = datetime.now()
                st.rerun()
        
        with col2:
            if st.button("💡 Reframing Tip", key="word_tip"):
                tips = [
                    "🧠 Ask yourself: 'Is this thought helping or hurting me?'",
                    "🔄 Try replacing 'I have to' with 'I choose to' for empowerment",
                    "🌱 Change 'I can't' to 'I'm learning how to' for growth mindset",
                    "⚖️ Look for evidence both for and against your negative thought",
                    "🎯 Focus on what you can control rather than what you can't",
                    "💪 Remember: Thoughts are not facts - they're mental events",
                    "🌈 Ask: 'What would I tell a friend in this situation?'",
                    "📈 Replace absolutes like 'always/never' with 'sometimes/often'"
                ]
                
                random_tip = random.choice(tips)
                st.info(f"**Cognitive Reframing Tip:**\n\n{random_tip}")
        
        with col3:
            if st.button("⏭️ Skip This Word", key="skip_word"):
                st.session_state.word_round += 1
                st.session_state.word_streak = 0
                st.warning("Word skipped. Try to complete all reframes for maximum benefit!")
                st.rerun()

# Simple wrapper to show just the game
def show_games_page():
    """Show Positive Word Association Game only"""
    
    # Header
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #ff69b4; font-family: 'Baloo 2', cursive;">💭 Positive Word Association</h1>
        <p style="color: #ffb6d5; font-size: 1.2rem;">Transform negative thoughts into positive ones</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the word association game directly
    positive_word_association_game()

if __name__ == "__main__":
    show_games_page()