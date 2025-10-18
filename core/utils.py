import sqlite3
import streamlit as st
import hashlib
from datetime import datetime, timedelta, timezone
import requests
import re
import json
import os
import google.generativeai


def get_current_time():
    """
    Returns the user's local time formatted as HH:MM AM/PM.
    Uses Streamlit's timezone offset if available.
    """
    tz_offset = st.context.timezone_offset

    if tz_offset is None:
        now = datetime.now()
    else:
        now_utc = datetime.now(timezone.utc)
        now = now_utc + timedelta(minutes=-tz_offset)

    return now.strftime("%I:%M %p").lstrip("0")


def hash_email(email):
    """
    Hash email to a short hex digest for privacy and consistent user identification.
    Args:
        email (str): The user's email address.
    Returns:
        str: Shortened SHA-256 hex digest or None if email is empty.
    """
    if not email:
        return None
    return hashlib.sha256(email.encode()).hexdigest()[:10]  # shorten for readability


def create_new_conversation(initial_message=None):
    """
    Create a new conversation for the current user or IP.
    Optionally adds an initial user message.
    Args:
        initial_message (str, optional): The first message in the conversation.
    Returns:
        int: The new conversation ID.
    """
    user_email = st.session_state.get("user_profile", {}).get("email", None)
    ip = cached_user_ip()

    user_key = user_email if user_email else ip

    user_convos = [c for c in st.session_state.conversations if c.get("user_key") == user_key]

    new_id = len(user_convos) + 1  # sequential per-user

    new_convo = {
        "id": new_id,
        "user_key": user_key,
        "title": initial_message[:30] + "..." if initial_message and len(initial_message) > 30 else "New Conversation",
        "date": datetime.now().strftime("%B %d, %Y"),
        "messages": []
    }

    if initial_message:
        new_convo["messages"].append({
            "sender": "user",
            "message": initial_message,
            "time": get_current_time()
        })

    st.session_state.conversations.insert(0, new_convo)
    st.session_state.active_conversation = new_id
    return new_id


def clean_ai_response(response_text):
    """
    Clean AI response by removing HTML tags and extra whitespace.
    Args:
        response_text (str): The raw AI response.
    Returns:
        str: Cleaned response text.
    """
    if not response_text:
        return response_text
    response_text = re.sub(r'<[^>]+>', '', response_text)
    response_text = re.sub(r'\s+', ' ', response_text).strip()
    response_text = response_text.replace('&nbsp;', ' ')
    response_text = response_text.replace('&lt;', '<')
    response_text = response_text.replace('&gt;', '>')
    response_text = response_text.replace('&amp;', '&')
    return response_text


def get_ai_response(user_message, model):
    """
    Generate an AI response to the user's message using the provided model.
    Handles errors and ensures a supportive, plain-text reply.
    Args:
        user_message (str): The user's message.
        model: The AI model instance.
    Returns:
        str: The AI's response.
    """
    if model is None:
        return "I'm sorry, I can't connect right now. Please check the API configuration."

    mental_health_prompt = f"""
    You are a compassionate mental health support chatbot named TalkHeal. Your role is to:
    1. Provide empathetic, supportive responses
    2. Encourage professional help when needed
    3. Never diagnose or provide medical advice
    4. Be warm, understanding, and non-judgmental
    5. Ask follow-up questions to better understand the user's situation
    6. Provide coping strategies and resources when appropriate
    7. Not assume that the user is always in overwhelming states. Sometimes he/she might also be in joyful or curious moods and ask questions not related to mental health
    
    IMPORTANT: Respond with PLAIN TEXT ONLY. Do not include any HTML tags, markdown formatting, or special characters. Just provide a natural, conversational response.
    
    User message: {user_message}
    
    Respond in a caring, supportive manner (keep response under 150 words):
    """
    try:
        response = model.generate_content(mental_health_prompt)
        cleaned_response = clean_ai_response(response.text)
        return cleaned_response
    except ValueError:
        return "I'm having trouble understanding your message. Could you please rephrase it?"
    except google.generativeai.types.BlockedPromptException:
        return "I understand you're going through something difficult. Let's focus on how you're feeling and what might help you feel better."
    except google.generativeai.types.GenerationException:
        return "I'm having trouble generating a response right now. Please try again in a moment."
    except requests.RequestException:
        return "I'm having trouble connecting to my services. Please check your internet connection and try again."
    except Exception:
        return "I'm here to listen and support you. Sometimes I have trouble connecting, but I want you to know that your feelings are valid and you're not alone. Would you like to share more about what you're experiencing?"


def cached_user_ip():
    """
    Get the user's IP address, caching it in session state for 1 hour.
    Returns:
        str: The user's IP address or a fallback session ID.
    """
    if hasattr(st.session_state, 'cached_ip') and hasattr(st.session_state, 'ip_cache_time'):
        cache_age = datetime.now() - st.session_state.ip_cache_time
        if cache_age < timedelta(hours=1):
            return st.session_state.cached_ip
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        ip = response.text.strip()
        st.session_state.cached_ip = ip
        st.session_state.ip_cache_time = datetime.now()
        return ip
    except (requests.RequestException, requests.Timeout, Exception):
        fallback_id = f"session_{hash(str(st.session_state)) % 100000}"
        if not hasattr(st.session_state, 'cached_ip'):
            st.session_state.cached_ip = fallback_id
            st.session_state.ip_cache_time = datetime.now()
        return st.session_state.cached_ip


def get_user_ip():
    """
    Get the user's public IP address (no caching).
    Returns:
        str: The user's IP address or 'unknown_ip'.
    """
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "unknown_ip"


def get_memory_file():
    """
    Get the filename for storing conversation history, based on user email or IP.
    Returns:
        str: The path to the memory file.
    """
    user_email = st.session_state.get("user_profile", {}).get("email")
    if user_email:
        safe_email = user_email.replace("@", "_at_").replace(".", "_dot_")
        filename = f"data/conversations_{safe_email}.json"
    else:
        ip = cached_user_ip()
        filename = f"data/conversations_{ip}.json"
    os.makedirs("data", exist_ok=True)
    return filename


def save_conversations(conversations):
    """
    Save the list of conversations to the user's memory file.
    Args:
        conversations (list): List of conversation dicts.
    """
    memory_file = get_memory_file()
    with open(memory_file, 'w', encoding="utf-8") as f:
        json.dump(conversations, f, indent=4)


def load_conversations():
    """
    Load the user's conversation history from file.
    Returns:
        list: List of conversation dicts, or empty list if none exist.
    """
    memory_file = get_memory_file()
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r', encoding="utf-8") as f:
        return json.load(f)


def save_feedback(convo_id, message, feedback, comment=None):
    """
    Save user feedback for a specific message in a conversation.
    Args:
        convo_id (int): Conversation ID.
        message (str): The message being rated.
        feedback (str): The feedback value.
        comment (str, optional): Optional user comment.
    """
    user_email = st.session_state.get("user_profile", {}).get("email")
    hashed_email = hash_email(user_email) if user_email else "unknown"

    print(f"""
    [save_feedback]
    User: {hashed_email}
    Convo ID: {convo_id}
    Message: {message}
    Feedback: {feedback}
    Comment: {comment if comment else "No comment"}
    """)

    conn = None
    try:
        conn = sqlite3.connect("feedback.db")
        c = conn.cursor()
        # Table creation removed (handled in setup script)

        c.execute('''
            SELECT id FROM feedback WHERE user_email = ? AND convo_id = ? AND message = ?
        ''', (hashed_email, convo_id, message))
        row = c.fetchone()

        if row:
            c.execute('''
                UPDATE feedback
                SET feedback = ?, comment = ?, timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (feedback, comment, row[0]))
            print(f"[save_feedback] Updated existing feedback (id={row[0]})")
        else:
            c.execute('''
                INSERT INTO feedback (user_email, convo_id, message, feedback, comment)
                VALUES (?, ?, ?, ?, ?)
            ''', (hashed_email, convo_id, message, feedback, comment))
            print("[save_feedback] Inserted new feedback")

        conn.commit()

    except Exception as e:
        print(f"[save_feedback] Exception while saving feedback: {e}")

    finally:
        if conn:
            conn.close()


def get_feedback(convo_id, message):
    """
    Retrieve feedback for a specific message in a conversation.
    Args:
        convo_id (int): Conversation ID.
        message (str): The message to look up.
    Returns:
        str or None: The feedback value, or None if not found.
    """
    user_email = st.session_state.get("user_profile", {}).get("email")
    if not user_email:
        print("[get_feedback] No user email found in session. Cannot retrieve feedback.")
        return None

    hashed_email = hash_email(user_email)  # Ensure matching hashed email

    try:
        conn = sqlite3.connect("feedback.db")
        c = conn.cursor()
        c.execute('''
            SELECT feedback FROM feedback WHERE user_email = ? AND convo_id = ? AND message = ?
        ''', (hashed_email, convo_id, message))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print(f"[get_feedback] Exception while fetching feedback: {e}")
        return None
    finally:
        conn.close()


def get_feedback_per_message(convo_id=None):
    """
    Retrieve all feedback entries, optionally filtered by conversation ID.
    Args:
        convo_id (int, optional): Conversation ID to filter by.
    Returns:
        list: List of feedback dicts.
    """
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()

    if convo_id is None:
        c.execute('''
            SELECT user_email, convo_id, message, feedback, comment, timestamp
            FROM feedback
            ORDER BY timestamp DESC
        ''')
    else:
        c.execute('''
            SELECT user_email, convo_id, message, feedback, comment, timestamp
            FROM feedback
            WHERE convo_id = ?
            ORDER BY timestamp DESC
        ''', (convo_id,))

    rows = c.fetchall()
    conn.close()

    return [
        {
            "user_email": r[0],
            "convo_id": r[1],
            "message": r[2],
            "feedback": r[3],
            "comment": r[4],
            "timestamp": r[5],
        }
        for r in rows
    ]
    
#Centralize Authentication
def is_authenticated():
    """
    Check if the user is authenticated in the current session.
    Returns:
        bool: True if authenticated, False otherwise.
    """
    return st.session_state.get("authenticated", False)

def set_authenticated_user(user):
    """
    Set the authenticated user in session state.
    Args:
        user (dict): User profile data.
    """
    st.session_state["authenticated"] = True
    st.session_state["user_profile"] = {
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "join_date": user.get("join_date", datetime.now().strftime("%B %Y"))
    }

def require_authentication():
    """
    Require the user to be authenticated, otherwise stop execution and show a warning.
    """
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("⚠️ Please login from the main page to access this section.")
        st.stop()

def logout_user():
    """
    Log out the user by clearing authentication-related session state keys.
    """
    keys_to_remove = ["authenticated", "user_email", "user_name", "profile_picture", "join_date", "font_size"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]


def create_responsive_columns(num_columns, min_width="120px", mobile_stack_breakpoint=480):
    """
    Create responsive columns that stack vertically on mobile devices.
    Args:
        num_columns (int): Number of columns for desktop layout.
        min_width (str): Minimum width for each column before stacking.
        mobile_stack_breakpoint (int): Screen width (px) below which to stack.
    Returns:
        list: List of Streamlit column objects.
    """
    """
    Create responsive columns that stack vertically on mobile devices.
    
    Args:
        num_columns (int): Number of columns for desktop layout
        min_width (str): Minimum width for each column before stacking
        mobile_stack_breakpoint (int): Screen width (px) below which to stack
        
    Returns:
        list: List of Streamlit column objects
    """
    # For very small screens, use single column
    if mobile_stack_breakpoint > 768:
        # Stack all columns on mobile
        return st.columns([1] * num_columns)
    else:
        # Use equal width columns
        return st.columns(num_columns)


def render_responsive_buttons(buttons_data, columns_per_row=None, mobile_stack=True):
    """
    Render buttons in a responsive layout that stacks on mobile.
    Args:
        buttons_data (list): List of dictionaries with button data.
        columns_per_row (int, optional): Number of buttons per row on desktop.
        mobile_stack (bool): Whether to stack buttons on mobile.
    Returns:
        None (renders buttons directly to Streamlit)
    """
    """
    Render buttons in a responsive layout that stacks on mobile.
    
    Args:
        buttons_data (list): List of dictionaries with button data
                           Each dict should have: {'text': str, 'key': str, 'action': callable, 'type': str}
        columns_per_row (int): Number of buttons per row on desktop (default: len(buttons_data))
        mobile_stack (bool): Whether to stack buttons on mobile
        
    Returns:
        None (renders buttons directly to Streamlit)
    """
    if not buttons_data:
        return
        
    if columns_per_row is None:
        columns_per_row = min(len(buttons_data), 4)  # Max 4 buttons per row
    
    # Add responsive CSS for this specific button group
    st.markdown(f"""
    <style>
    @media (max-width: 768px) {{
        .responsive-button-container {{
            display: flex;
            flex-direction: {'column' if mobile_stack else 'row'};
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        .responsive-button-container .stButton {{
            flex: 1 1 auto;
            min-width: 120px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Group buttons into rows
    for i in range(0, len(buttons_data), columns_per_row):
        row_buttons = buttons_data[i:i + columns_per_row]
        cols = st.columns(len(row_buttons))
        
        for j, button_data in enumerate(row_buttons):
            with cols[j]:
                button_type = button_data.get('type', 'primary')
                help_text = button_data.get('help', '')
                use_container_width = button_data.get('use_container_width', True)
                
                if st.button(
                    button_data['text'],
                    key=button_data['key'],
                    type=button_type,
                    help=help_text,
                    use_container_width=use_container_width
                ):
                    if button_data.get('action'):
                        button_data['action']()
                        
                        
def get_mobile_friendly_columns(desktop_ratios, mobile_threshold=768):
    """
    Convert desktop column ratios to mobile-friendly layout.
    Args:
        desktop_ratios (list): List of column width ratios for desktop.
        mobile_threshold (int): Screen width threshold for mobile layout.
    Returns:
        list: Mobile-optimized column ratios.
    """
    """
    Convert desktop column ratios to mobile-friendly layout.
    
    Args:
        desktop_ratios (list): List of column width ratios for desktop
        mobile_threshold (int): Screen width threshold for mobile layout
        
    Returns:
        list: Mobile-optimized column ratios
    """
    # On mobile, prefer more equal distributions or single column
    if len(desktop_ratios) > 4:
        # Too many columns, use fewer
        return [1] * min(2, len(desktop_ratios))
    elif len(desktop_ratios) > 2:
        # Use more balanced ratios
        return [1] * len(desktop_ratios)
    else:
        # Keep original ratios but ensure minimum widths
        return desktop_ratios
