import streamlit as st
import sqlite3
import base64
from uuid import uuid4
from datetime import date
from core.utils import require_authentication
import pandas as pd
import altair as alt
import csv
from io import StringIO
from fpdf import FPDF

def get_base64_of_bin_file(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background_for_theme(selected_palette="pink"):
    from core.theme import get_current_theme

    # --- Get current theme info ---
    current_theme = st.session_state.get("current_theme", None)
    if not current_theme:
        current_theme = get_current_theme()
    
    is_dark = current_theme["name"] == "Dark"

    # --- Map light themes to background images ---
    palette_color = {
        "light": "static_files/pink.png",
        "calm blue": "static_files/blue.png",
        "mint": "static_files/mint.png",
        "lavender": "static_files/lavender.png",
        "pink": "static_files/pink.png"
    }

    # --- Select background based on theme ---
    if is_dark:
        background_image_path = "static_files/dark.png"
    else:
        background_image_path = palette_color.get(selected_palette.lower(), "static_files/pink.png")

    encoded_string = get_base64_of_bin_file(background_image_path)
    st.markdown(
        f"""
        <style>
        /* Entire app background */
        html, body, [data-testid="stApp"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Main content transparency */
        .block-container {{
            background-color: rgba(255, 255, 255, 0);
        }}

        /* Sidebar: brighter translucent background */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.6);  /* Brighter and translucent */
            color: {'black' if is_dark else 'rgba(49, 51, 63, 0.8)'} ;  /* Adjusted for light background */
        }}

        span {{
            color: {'#f0f0f0' if is_dark else 'rgba(49, 51, 63, 0.8)'} !important;
            transition: color 0.3s ease;
        }}

        /* Header bar: fully transparent */
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0);
        }}

        /* Hide left/right arrow at sidebar bottom */
        button[title="Close sidebar"],
        button[title="Open sidebar"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)

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
    query += " ORDER BY date ASC"
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

def delete_entry(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def create_mood_trend_chart(entries):
    if not entries:
        return None

    df = pd.DataFrame(entries, columns=['id', 'entry', 'sentiment', 'date'])
    df['date'] = pd.to_datetime(df['date'])
    
    sentiment_mapping = {"Positive": 1, "Neutral": 0, "Negative": -1}
    df['sentiment_score'] = df['sentiment'].map(sentiment_mapping)

    chart = alt.Chart(df).mark_line(
        point=alt.OverlayMarkDef(color="red")
    ).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('sentiment_score:Q', title='Mood Score'),
        tooltip=['date', 'sentiment']
    ).properties(
        title="Mood Trend Over Time"
    ).interactive()

    return chart

def get_csv_export(entries):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Sentiment', 'Entry'])
    for _, entry, sentiment, entry_date in entries:
        writer.writerow([entry_date, sentiment, entry])
    return output.getvalue()

def get_pdf_export(entries):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for _, entry, sentiment, entry_date in entries:
        pdf.cell(200, 10, txt=f"Date: {entry_date}", ln=True)
        pdf.cell(200, 10, txt=f"Sentiment: {sentiment}", ln=True)
        pdf.multi_cell(0, 10, txt=entry)
        pdf.ln(10)
    return pdf.output(dest='S').encode('latin-1')

def journaling_app():
    set_background_for_theme(selected_palette)
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
    st.subheader("Mood Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", value=date.today())

    entries = fetch_entries(email, start_date=start_date, end_date=end_date)
    
    chart = create_mood_trend_chart(entries)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Not enough data to display mood trend. Write some journal entries first!")


    st.markdown("---")
    st.subheader("📖 Your Journal Entries")

    filter_sentiment = st.selectbox("Filter by Sentiment", ["All", "Positive", "Neutral", "Negative"])
    
    filtered_entries = entries
    if filter_sentiment != "All":
        filtered_entries = [entry for entry in entries if entry[2] == filter_sentiment]

    if not filtered_entries:
        st.info("No entries found for selected filters.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            csv_data = get_csv_export(filtered_entries)
            st.download_button(
                label="Export as CSV",
                data=csv_data,
                file_name="journal_entries.csv",
                mime="text/csv",
            )
        with col2:
            pdf_data = get_pdf_export(filtered_entries)
            st.download_button(
                label="Export as PDF",
                data=pdf_data,
                file_name="journal_entries.pdf",
                mime="application/pdf",
            )

        for entry_id, entry, sentiment, entry_date in reversed(filtered_entries):
            with st.expander(f"{entry_date} - Mood: {sentiment}"):
                st.write(entry)
                
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("Edit", key=f"edit_{entry_id}"):
                        st.session_state.edit_id = entry_id
                with col2:
                    if st.button("Delete", key=f"delete_{entry_id}"):
                        delete_entry(entry_id)
                        st.rerun()

                if st.session_state.get("edit_id") == entry_id:
                    with st.form(key=f"edit_form_{entry_id}"):
                        new_text = st.text_area("Edit your entry", value=entry, height=200)
                        if st.form_submit_button("Save"):
                            update_entry(entry_id, new_text)
                            st.session_state.edit_id = None
                            st.rerun()

init_journal_db()
journaling_app()