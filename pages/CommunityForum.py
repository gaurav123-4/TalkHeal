import streamlit as st
import base64
import random
import datetime

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

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
            color: black;  /* Adjusted for light background */
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
set_background("static_files/pink.png")

# --- Page Configuration ---
st.set_page_config(page_title="Community Forum", page_icon="🌐", layout="wide")

# --- Helper Functions ---

# List of fun anonymous names
ANONYMOUS_NAMES = [
    "Creative Cat", "Brave Bear", "Wise Wolf", "Gentle Giraffe", "Happy Hippo",
    "Curious Crow", "Daring Dolphin", "Kind Koala", "Lucky Llama", "Patient Panda"
]

# Simple profanity filter (for demonstration)
BANNED_WORDS = ["badword1", "badword2", "example_profanity"]

def initialize_state():
    """Initializes session state variables."""
    if 'posts' not in st.session_state:
        st.session_state.posts = []
    if 'user_name' not in st.session_state:
        st.session_state.user_name = random.choice(ANONYMOUS_NAMES)

def format_time_ago(dt):
    """Formats a datetime object into a 'time ago' string."""
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - dt
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} minute(s) ago"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hour(s) ago"
    days = hours / 24
    return f"{int(days)} day(s) ago"

def contains_profanity(message):
    """Checks if a message contains any banned words."""
    return any(word in message.lower() for word in BANNED_WORDS)

# --- UI Rendering ---

def show_post_form():
    """Displays the form for creating a new post."""
    with st.form("new_post_form", clear_on_submit=True):
        st.subheader(f"Post as: {st.session_state.user_name}")
        message = st.text_area("Share your thoughts or ask for support:", height=150, max_chars=1000)
        submitted = st.form_submit_button("Post Anonymously")
        
        if submitted:
            if not message.strip():
                st.warning("Please enter a message before posting.")
            elif contains_profanity(message):
                st.error("Your message contains inappropriate language and was blocked by our AI moderator.")
            else:
                new_post = {
                    "id": len(st.session_state.posts) + 1,
                    "author": st.session_state.user_name,
                    "message": message,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc),
                    "replies": []
                }
                st.session_state.posts.insert(0, new_post) # Add to the beginning of the list
                st.success("Your message has been posted anonymously!")
                st.rerun()

def show_posts():
    """Displays all the posts and their replies."""
    if not st.session_state.posts:
        st.info("No posts yet. Be the first to share your story!")
        return

    for post in st.session_state.posts:
        with st.container(border=True):
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**{post['author']}** · *{format_time_ago(post['timestamp'])}*")
                st.markdown(post['message'])
            
            # Display replies
            for reply in post['replies']:
                with st.chat_message("user", avatar="💬"):
                     st.markdown(f"**{reply['author']}** · *{format_time_ago(reply['timestamp'])}*")
                     st.markdown(reply['message'])

            # Reply form
            with st.expander("Add a reply..."):
                reply_message = st.text_area("Your reply", key=f"reply_{post['id']}")
                if st.button("Submit Reply", key=f"submit_reply_{post['id']}"):
                    if reply_message.strip():
                        new_reply = {
                            "author": st.session_state.user_name,
                            "message": reply_message,
                            "timestamp": datetime.datetime.now(datetime.timezone.utc)
                        }
                        post['replies'].append(new_reply)
                        st.rerun()

# --- Main Page --- 

initialize_state()

st.title("🌐 Community Forum")
st.markdown("Welcome! Connect, share, and support each other in a safe, AI-moderated environment.")

with st.expander("📘 Forum Guidelines"):
    st.markdown("""
    - **Be Kind & Respectful:** Treat everyone with respect. No personal attacks.
    - **Stay Anonymous:** Do not share personal identifying information.
    - **Offer Support:** Provide constructive and supportive feedback.
    - **Safety First:** Do not post content that is graphic or promotes self-harm. Our AI moderator is here to help.
    """)

st.markdown("--- ")

# --- Layout: Two Columns ---
col1, col2 = st.columns([2, 1]) # 2/3 for posts, 1/3 for form

with col1:
    st.header("Recent Posts")
    show_posts()

with col2:
    st.header("Create a Post")
    show_post_form()

st.markdown("---")
st.info("This is a prototype. Posts are cleared when you close the browser tab.")
