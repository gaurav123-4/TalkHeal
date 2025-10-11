import streamlit as st
import sqlite3
import base64
from uuid import uuid4
from datetime import date
from core.utils import require_authentication

# Centralized Authentication Check
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
    
require_authentication()

def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(main_bg_path, sidebar_bg_path=None):
    main_bg = get_base64_of_bin_file(main_bg_path)
    sidebar_bg = get_base64_of_bin_file(sidebar_bg_path) if sidebar_bg_path else main_bg
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{main_bg}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 2px solid rgba(245, 167, 208, 0.6);
            box-shadow: 4px 0 24px rgba(0,0,0,0.15);
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{sidebar_bg}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def analyze_sentiment(entry: str) -> str:
    if any(word in entry.lower() for word in ['sad', 'tired', 'upset', 'angry']):
        return "Negative"
    elif any(word in entry.lower() for word in ['happy', 'grateful', 'joy']):
        return "Positive"
    return "Neutral"

DB_PATH = "journals.db"

def init_journal_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id TEXT PRIMARY KEY,
        email TEXT,
        entry TEXT,
        sentiment TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_entry(email, entry, sentiment):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO journal_entries (id, email, entry, sentiment, date)
    VALUES (?, ?, ?, ?, ?)
    """, (str(uuid4()), email, entry, sentiment, str(date.today()))) # Use date.today()
    conn.commit()
    conn.close()

def fetch_entries(email, sentiment_filter=None, start_date=None, end_date=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT id, entry, sentiment, date FROM journal_entries
        WHERE email = ?
    """
    params = [email]
    if sentiment_filter and sentiment_filter != "All":
        query += " AND sentiment = ?"
        params.append(sentiment_filter)
    if start_date and end_date:
        query += " AND date BETWEEN ? AND ?"
        params.extend([start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")])
    query += " ORDER BY date DESC"
    rows = cursor.execute(query, params).fetchall()
    conn.close()
    return rows

def update_entry(entry_id, new_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    new_sentiment = analyze_sentiment(new_text)
    cursor.execute("UPDATE journal_entries SET entry = ?, sentiment = ? WHERE id = ?", (new_text, new_sentiment, entry_id))
    conn.commit()
    conn.close()

def journaling_app():
    set_background("static_files/mint.png")
    st.markdown(
        """
        <style>
        /* CSS styles for the app */
        textarea.stTextArea > div > textarea { color: white !important; background-color: #222222 !important; }
        button[aria-expanded] { color: white !important; }
        .streamlit-expanderContent p, .streamlit-expanderContent div { color: white !important; }
        .stTextArea, .css-1d391kg, .stMarkdown, .css-1v0mbdj { color: white !important; }
        textarea::placeholder { color: #ccc !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📝 My Journal")
    st.markdown("Write about your day, thoughts, or anything you'd like to reflect on.")
    email = st.session_state.user_profile.get("email")

    with st.form("journal_form"):
        journal_text = st.text_area("How are you feeling today?", height=200)
        submitted = st.form_submit_button("Submit Entry")

    if submitted and journal_text.strip():
        sentiment = analyze_sentiment(journal_text)
        save_entry(email, journal_text, sentiment)
        st.success(f"Entry saved! Sentiment: **{sentiment}**")
        st.rerun() 

    st.markdown("---")
    st.subheader("📖 Your Journal Entries")

    filter_sentiment = st.selectbox("Filter by Sentiment", ["All", "Positive", "Neutral", "Negative"])
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    entries = fetch_entries(email, sentiment_filter=filter_sentiment, start_date=start_date, end_date=end_date)
        
    if not entries:
        st.info("No entries found for selected filters.")
    else:
        for entry_id, entry, sentiment, entry_date in entries:
            with st.expander(f"{entry_date} - Mood: {sentiment}"):
                st.write(entry)
                
                if st.button("Edit", key=f"edit_{entry_id}"):
                    st.session_state.edit_id = entry_id

                if st.session_state.get("edit_id") == entry_id:
                    with st.form(key=f"edit_form_{entry_id}"):
                        new_text = st.text_area("Edit your entry", value=entry, height=200)
                        if st.form_submit_button("Save"):
                            update_entry(entry_id, new_text)
                            st.session_state.edit_id = None
                            st.rerun()

init_journal_db()
journaling_app()