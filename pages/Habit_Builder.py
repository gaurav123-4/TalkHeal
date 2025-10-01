import streamlit as st
import datetime
import random
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

@dataclass
class Habit:
    name: str
    category: str
    difficulty: str
    streak: int = 0
    total_completions: int = 0
    last_completed: Optional[str] = None
    created_date: str = None
    notes: str = ""
    reminder_time: Optional[str] = None

@dataclass
class Challenge:
    title: str
    description: str
    category: str
    difficulty: str
    points: int
    duration_days: int = 1

def initialize_session_state():
    """Initialize all session state variables"""
    if 'habits' not in st.session_state:
        st.session_state.habits = []
    
    if 'completed_challenges' not in st.session_state:
        st.session_state.completed_challenges = []
    
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 0
    
    if 'weekly_goals' not in st.session_state:
        st.session_state.weekly_goals = {}
    
    if 'habit_history' not in st.session_state:
        st.session_state.habit_history = {}

def get_predefined_challenges():
    """Return a comprehensive list of mental health challenges"""
    return [
        Challenge("Gratitude Practice", "Write down 3 things you are grateful for today", "Mindfulness", "Easy", 5),
        Challenge("Digital Detox", "Spend 1 hour without any screens or social media", "Wellness", "Medium", 10),
        Challenge("Nature Connection", "Spend 30 minutes outdoors in nature", "Physical", "Easy", 8),
        Challenge("Deep Breathing", "Practice deep breathing exercises for 10 minutes", "Mindfulness", "Easy", 5),
        Challenge("Mindful Reading", "Read for 20 minutes without distractions", "Mental", "Easy", 6),
        Challenge("Acts of Kindness", "Perform one random act of kindness", "Social", "Medium", 10),
        Challenge("Creative Expression", "Spend 15 minutes on a creative activity", "Mental", "Medium", 8),
        Challenge("Hydration Focus", "Drink 8 glasses of water throughout the day", "Physical", "Easy", 4),
        Challenge("Meditation Practice", "Complete a 15-minute meditation session", "Mindfulness", "Medium", 12),
        Challenge("Journal Reflection", "Write about your emotions for 10 minutes", "Mental", "Easy", 7),
        Challenge("Physical Activity", "Do 30 minutes of any physical exercise", "Physical", "Medium", 10),
        Challenge("Sleep Hygiene", "Go to bed 30 minutes earlier than usual", "Wellness", "Medium", 8),
        Challenge("Social Connection", "Have a meaningful conversation with someone", "Social", "Easy", 6),
        Challenge("Mindful Eating", "Eat one meal without distractions", "Wellness", "Easy", 5),
        Challenge("Declutter Space", "Organize and clean your living space for 20 minutes", "Wellness", "Easy", 6)
    ]

def get_habit_categories():
    """Return habit categories with suggested habits"""
    return {
        "Mindfulness": ["Daily meditation", "Gratitude journaling", "Mindful breathing", "Body scan practice"],
        "Physical": ["Morning walk", "Stretching routine", "Drink water", "Exercise", "Yoga practice"],
        "Mental": ["Read for 20 minutes", "Learn something new", "Creative writing", "Puzzle solving"],
        "Social": ["Call a friend", "Practice active listening", "Express appreciation", "Join a group activity"],
        "Wellness": ["Sleep 8 hours", "Healthy meal prep", "Digital detox", "Self-care routine", "Clean living space"]
    }

def calculate_habit_score(habit: Habit) -> int:
    """Calculate a score for habit based on streak and difficulty"""
    difficulty_multiplier = {"Easy": 1, "Medium": 2, "Hard": 3}
    base_score = habit.streak * difficulty_multiplier.get(habit.difficulty, 1)
    return base_score + habit.total_completions

def get_daily_challenge():
    """Get or generate today's challenge"""
    today = datetime.date.today().isoformat()
    challenges = get_predefined_challenges()
    
    if 'daily_challenge_date' not in st.session_state or st.session_state.daily_challenge_date != today:
        # Generate new challenge for today
        available_challenges = [c for c in challenges if c.title not in st.session_state.completed_challenges]
        if not available_challenges:
            available_challenges = challenges  # Reset if all completed
            st.session_state.completed_challenges = []
        
        st.session_state.daily_challenge = random.choice(available_challenges)
        st.session_state.daily_challenge_date = today
        st.session_state.daily_challenge_completed = False
    
    return st.session_state.daily_challenge

def display_progress_analytics():
    """Display habit progress analytics"""
    if not st.session_state.habits:
        st.info("Add some habits to see your progress analytics!")
        return
    
    # Prepare data for visualization
    habit_data = []
    for h in st.session_state.habits:
        # Handle both dict and Habit object formats
        if isinstance(h, dict):
            habit = Habit(**h)
        else:
            habit = h
            
        habit_data.append({
            'Habit': habit.name,
            'Streak': habit.streak,
            'Total Completions': habit.total_completions,
            'Category': habit.category,
            'Difficulty': habit.difficulty,
            'Score': calculate_habit_score(habit)
        })
    
    if not habit_data:
        st.info("No habit data available yet!")
        return
        
    df = pd.DataFrame(habit_data)
    
    # Create subplots
    col1, col2 = st.columns(2)
    
    with col1:
        # Streak comparison
        fig_streak = px.bar(df, x='Habit', y='Streak', color='Category',
                           title='Current Streaks by Habit')
        fig_streak.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_streak, use_container_width=True)
    
    with col2:
        # Category distribution
        category_counts = df.groupby('Category').size().reset_index(name='Count')
        fig_pie = px.pie(category_counts, values='Count', names='Category',
                        title='Habits by Category')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Weekly progress heatmap (simplified version)
    st.subheader("📊 Weekly Progress Overview")
    
    # Show basic stats instead of complex heatmap for now
    total_habits = len(habit_data)
    active_streaks = len([h for h in habit_data if h['Streak'] > 0])
    avg_streak = sum(h['Streak'] for h in habit_data) / total_habits if total_habits > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Habits", total_habits)
    with col2:
        st.metric("Active Streaks", active_streaks)
    with col3:
        st.metric("Average Streak", f"{avg_streak:.1f} days")

def display_habit_management():
    """Display habit management interface"""
    st.markdown("### 🎯 My Habits")
    
    if not st.session_state.habits:
        st.info("🌱 Start your journey by adding your first habit below!")
        return
    
    # Filter and sort options
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Filter by Category", 
                                     ["All"] + list(get_habit_categories().keys()))
    with col2:
        sort_by = st.selectbox("Sort by", ["Name", "Streak", "Category", "Difficulty"])
    with col3:
        sort_order = st.selectbox("Order", ["Ascending", "Descending"])
    
    # Convert dicts back to Habit objects for easier handling
    habits_objects = []
    for h in st.session_state.habits:
        if isinstance(h, dict):
            habits_objects.append(Habit(**h))
        else:
            habits_objects.append(h)
    
    # Filter habits
    filtered_habits = habits_objects
    if category_filter != "All":
        filtered_habits = [h for h in filtered_habits if h.category == category_filter]
    
    # Sort habits
    reverse = sort_order == "Descending"
    if sort_by == "Name":
        filtered_habits.sort(key=lambda x: x.name, reverse=reverse)
    elif sort_by == "Streak":
        filtered_habits.sort(key=lambda x: x.streak, reverse=reverse)
    elif sort_by == "Category":
        filtered_habits.sort(key=lambda x: x.category, reverse=reverse)
    elif sort_by == "Difficulty":
        filtered_habits.sort(key=lambda x: x.difficulty, reverse=reverse)
    
    # Display habits
    for i, habit in enumerate(filtered_habits):
        original_index = next(idx for idx, h in enumerate(st.session_state.habits) 
                            if (h.get('name') if isinstance(h, dict) else h.name) == habit.name)
        
        with st.expander(f"🎯 {habit.name}", expanded=False):
            # Check if this habit is currently being edited
            if st.session_state.get(f"editing_{original_index}", False):
                st.markdown("#### Edit Habit Details")
                with st.form(key=f"edit_habit_form_{original_index}"):
                    col1_edit, col2_edit = st.columns(2)
                    with col1_edit:
                        edited_name = st.text_input("Habit Name", value=habit.name, key=f"edit_name_{original_index}")
                        edited_category = st.selectbox("Category", list(get_habit_categories().keys()), index=list(get_habit_categories().keys()).index(habit.category), key=f"edit_category_{original_index}")
                    with col2_edit:
                        edited_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(habit.difficulty), key=f"edit_difficulty_{original_index}")
                        
                        # Handle reminder_time conversion
                        current_reminder_time = None
                        if habit.reminder_time:
                            try:
                                current_reminder_time = datetime.datetime.strptime(habit.reminder_time, '%H:%M:%S').time()
                            except ValueError:
                                # Handle cases where reminder_time might be in a different format or invalid
                                pass
                        edited_reminder_time = st.time_input("Reminder Time (Optional)", value=current_reminder_time, key=f"edit_reminder_{original_index}")
                    
                    edited_notes = st.text_area("Notes (Optional)", value=habit.notes, key=f"edit_notes_{original_index}")
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save_changes = st.form_submit_button("💾 Save Changes")
                    with col_cancel:
                        cancel_edit = st.form_submit_button("❌ Cancel")
                    
                    if save_changes:
                        # Update habit in session state
                        habit_data = st.session_state.habits[original_index]
                        if isinstance(habit_data, dict):
                            habit_data['name'] = edited_name
                            habit_data['category'] = edited_category
                            habit_data['difficulty'] = edited_difficulty
                            habit_data['notes'] = edited_notes
                            habit_data['reminder_time'] = edited_reminder_time.isoformat() if edited_reminder_time else None
                        
                        st.session_state[f"editing_{original_index}"] = False
                        st.success(f"Habit '{edited_name}' updated!")
                        st.rerun()
                    
                    if cancel_edit:
                        st.session_state[f"editing_{original_index}"] = False
                        st.rerun()
            else:
                # Normal display mode
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Streak", f"{habit.streak} days", f"+{habit.total_completions} total")
                with col2:
                    difficulty_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
                    st.metric("Difficulty", f"{difficulty_emoji.get(habit.difficulty, '')} {habit.difficulty}")
                with col3:
                    st.metric("Category", habit.category)
                
                # Check completion status
                today = datetime.date.today()
                last_completed = None
                if habit.last_completed:
                    if isinstance(habit.last_completed, str):
                        last_completed = datetime.datetime.strptime(habit.last_completed, '%Y-%m-%d').date()
                    else:
                        last_completed = habit.last_completed
                
                # Action buttons
                col_complete, col_edit, col_archive, col_confirm = st.columns(4)
                
                with col_complete:
                    if last_completed == today:
                        st.success("✅ Completed Today!")
                    else:
                        if st.button("Mark Complete", key=f"complete_{original_index}"):
                            # Update habit in session state
                            habit_data = st.session_state.habits[original_index]
                            if isinstance(habit_data, dict):
                                if last_completed == today - datetime.timedelta(days=1):
                                    habit_data['streak'] += 1
                                else:
                                    habit_data['streak'] = 1
                                habit_data['total_completions'] += 1
                                habit_data['last_completed'] = today.isoformat()
                            
                            # Award points
                            points = {"Easy": 5, "Medium": 10, "Hard": 15}
                            st.session_state.user_points += points.get(habit.difficulty, 5)
                            
                            st.rerun()
                
                with col_edit:
                    if st.button("✏️ Edit", key=f"edit_btn_{original_index}"):
                        st.session_state[f"editing_{original_index}"] = True
                        st.rerun()
                
                with col_archive:
                    if st.button("Archive", key=f"archive_{original_index}"):
                        if st.session_state.get(f"confirm_archive_{original_index}", False):
                            st.session_state.habits.pop(original_index)
                            st.rerun()
                        else:
                            st.session_state[f"confirm_archive_{original_index}"] = True
                            st.rerun()
                
                with col_confirm:
                    if st.session_state.get(f"confirm_archive_{original_index}", False):
                        st.warning("Click Archive again to confirm")
                
                # Show notes if any
                if habit.notes:
                    st.write(f"📝 **Notes:** {habit.notes}")

def display_add_habit_form():
    """Display form to add new habits"""
    st.markdown("### ➕ Add New Habit")
    
    with st.form("add_habit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            habit_name = st.text_input("Habit Name", placeholder="e.g., Meditate for 10 minutes")
            category = st.selectbox("Category", list(get_habit_categories().keys()))
        
        with col2:
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            reminder_time = st.time_input("Reminder Time (Optional)", value=None)
        
        # Quick suggestions based on category
        if category:
            st.write(f"💡 **Suggestions for {category}:**")
            suggestions = get_habit_categories()[category]
            
            # Create a selectbox for suggestions instead
            selected_suggestion = st.selectbox("Choose a suggestion (optional)", 
                                             [""] + suggestions, 
                                             index=0)
            if selected_suggestion:
                habit_name = selected_suggestion
        
        notes = st.text_area("Notes (Optional)", placeholder="Any additional details or motivation...")
        
        submitted = st.form_submit_button("🎯 Add Habit")
        
        if submitted and habit_name:
            new_habit = Habit(
                name=habit_name,
                category=category,
                difficulty=difficulty,
                created_date=datetime.date.today().isoformat(),
                notes=notes,
                reminder_time=reminder_time.isoformat() if reminder_time else None
            )
            
            # Convert to dict for session state storage
            st.session_state.habits.append(asdict(new_habit))
            st.success(f"🎉 Added habit: {habit_name}")
            st.rerun()
        elif submitted:
            st.warning("Please enter a habit name.")

def display_daily_challenge():
    """Display daily challenge section"""
    st.markdown("### 🏆 Daily Challenge")
    
    challenge = get_daily_challenge()
    
    # Display challenge card
    difficulty_colors = {"Easy": "#28a745", "Medium": "#ffc107", "Hard": "#dc3545"}
    color = difficulty_colors.get(challenge.difficulty, "#6c757d")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {color}20, {color}10); 
                border-left: 5px solid {color}; 
                border-radius: 10px; 
                padding: 1.5rem; 
                margin: 1rem 0;'>
        <h4 style='color: {color}; margin-bottom: 0.5rem;'>🎯 {challenge.title}</h4>
        <p style='font-size: 1.1rem; margin-bottom: 1rem;'>{challenge.description}</p>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span><strong>Category:</strong> {challenge.category}</span>
            <span><strong>Difficulty:</strong> {challenge.difficulty}</span>
            <span><strong>Points:</strong> {challenge.points} 🌟</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Challenge completion
    if st.session_state.get('daily_challenge_completed', False):
        st.success("🎉 Challenge completed today! Great job!")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            notes = st.text_input("How did it go? (Optional)", placeholder="Reflection on the challenge...")
        with col2:
            if st.button("✅ Complete Challenge"):
                st.session_state.daily_challenge_completed = True
                st.session_state.completed_challenges.append(challenge.title)
                st.session_state.user_points += challenge.points
                st.success(f"🌟 Earned {challenge.points} points!")
                st.rerun()

def display_achievements_and_stats():
    """Display user achievements and statistics"""
    st.markdown("### 🏆 Your Achievements")
    
    # User stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_habits = len(st.session_state.habits)
    
    # Handle both dict and Habit object formats
    total_completions = 0
    max_streak = 0
    active_streaks = 0
    
    for h in st.session_state.habits:
        if isinstance(h, dict):
            total_completions += h.get('total_completions', 0)
            streak = h.get('streak', 0)
            max_streak = max(max_streak, streak)
            if streak > 0:
                active_streaks += 1
        else:
            total_completions += h.total_completions
            max_streak = max(max_streak, h.streak)
            if h.streak > 0:
                active_streaks += 1
    
    with col1:
        st.metric("🎯 Total Habits", total_habits)
    with col2:
        st.metric("✅ Completions", total_completions)
    with col3:
        st.metric("🔥 Best Streak", f"{max_streak} days")
    with col4:
        st.metric("🌟 Points", st.session_state.user_points)
    
    # Achievement badges
    st.markdown("#### 🏅 Achievement Badges")
    badges = []
    
    if total_habits >= 1:
        badges.append("🌱 Habit Starter")
    if total_habits >= 5:
        badges.append("🎯 Goal Setter")
    if max_streak >= 7:
        badges.append("🔥 Week Warrior")
    if max_streak >= 30:
        badges.append("💪 Month Master")
    if total_completions >= 50:
        badges.append("⭐ Consistency Champion")
    if st.session_state.user_points >= 100:
        badges.append("🏆 Point Collector")
    
    if badges:
        badge_cols = st.columns(min(len(badges), 4))
        for i, badge in enumerate(badges):
            with badge_cols[i % 4]:
                st.info(badge)
    else:
        st.info("Start completing habits and challenges to earn badges!")

def show():
    """Main application function"""
    st.set_page_config(page_title="Habit Builder Pro", page_icon="🎯", layout="wide")
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 2rem; color: white;'>
        <h1 style='margin: 0; font-size: 2.5rem;'>🎯 Habit Builder Pro</h1>
        <p style='margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;'>
            Build lasting habits, track your progress, and transform your mental well-being
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "🎯 My Habits", 
        "🏆 Daily Challenge", 
        "➕ Add Habit", 
        "📈 Analytics"
    ])
    
    with tab1:
        # Dashboard
        display_achievements_and_stats()
        st.markdown("---")
        
        if st.session_state.habits:
            st.markdown("### 📋 Today's Quick View")
            today = datetime.date.today()
            
            # Show up to 3 habits
            display_habits = st.session_state.habits[:3]
            for h in display_habits:
                # Handle both dict and Habit object formats
                if isinstance(h, dict):
                    habit_name = h.get('name', 'Unknown Habit')
                    streak = h.get('streak', 0)
                    last_completed = h.get('last_completed')
                else:
                    habit_name = h.name
                    streak = h.streak
                    last_completed = h.last_completed
                
                last_completed_date = None
                if last_completed:
                    if isinstance(last_completed, str):
                        last_completed_date = datetime.datetime.strptime(last_completed, '%Y-%m-%d').date()
                    else:
                        last_completed_date = last_completed
                
                if last_completed_date == today:
                    st.success(f"✅ {habit_name} - Completed!")
                else:
                    st.info(f"⏳ {habit_name} - Pending (Streak: {streak})")
    
    with tab2:
        display_habit_management()
    
    with tab3:
        display_daily_challenge()
    
    with tab4:
        display_add_habit_form()
    
    with tab5:
        st.markdown("### 📈 Progress Analytics")
        display_progress_analytics()
    
    # Sidebar with quick stats and tips
    with st.sidebar:
        st.markdown("### 🚀 Quick Stats")
        st.metric("Active Habits", len(st.session_state.habits))
        st.metric("Total Points", st.session_state.user_points)
        
        st.markdown("---")
        st.markdown("### 💡 Daily Tip")
        tips = [
            "Start small - even 1% improvement daily compounds over time!",
            "Consistency beats perfection. Focus on showing up daily.",
            "Stack new habits onto existing routines for better success.",
            "Celebrate small wins - they fuel motivation for bigger goals.",
            "Track your progress - what gets measured gets managed!"
        ]
        st.info(random.choice(tips))
        
        st.markdown("---")
        st.markdown("### 🔧 Settings")
        if st.button("🗑️ Reset All Data"):
            if st.session_state.get('confirm_reset', False):
                st.session_state.habits = []
                st.session_state.completed_challenges = []
                st.session_state.user_points = 0
                st.success("Data reset successfully!")
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("Click again to confirm reset")

if __name__ == "__main__":
    show()