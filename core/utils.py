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
    """Returns the user's local time formatted as HH:MM AM/PM."""
    tz_offset = st.context.timezone_offset

    if tz_offset is None:
        now = datetime.now()
    else:
        now_utc = datetime.now(timezone.utc)
        now = now_utc + timedelta(minutes=-tz_offset)

    return now.strftime("%I:%M %p").lstrip("0")


def hash_email(email):
    """Hash email to a short hex digest for privacy and consistent user identification."""
    if not email:
        return None
    return hashlib.sha256(email.encode()).hexdigest()[:10]  # shorten for readability


def create_new_conversation(initial_message=None):
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
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "unknown_ip"


def get_memory_file():
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
    memory_file = get_memory_file()
    with open(memory_file, 'w', encoding="utf-8") as f:
        json.dump(conversations, f, indent=4)


def load_conversations():
    memory_file = get_memory_file()
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r', encoding="utf-8") as f:
        return json.load(f)


def save_feedback(convo_id, message, feedback, comment=None):
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
