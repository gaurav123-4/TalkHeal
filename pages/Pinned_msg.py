# This file handles rendering and managing the "Pinned Messages" page.
import streamlit as st
from datetime import datetime
import base64
from components.chat_interface import toggle_pin_message, inject_custom_css


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

        /* Sidebar: brighter translucent background */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.6);
            color: {'black' if is_dark else 'rgba(49, 51, 63, 0.8)'} ;  /* Adjusted for light background */
        }}

        .block-container {{
            background-color: rgba(255, 255, 255, 0);
            max-width: 100% !important;
            padding-left: 1rem;
            padding-right: 1rem;
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

# Set your background image
selected_palette = st.session_state.get("palette_name", "Pink")
set_background_for_theme(selected_palette)

def show():
    """Renders a more visually appealing Community page using tabs and icons."""

    st.markdown("""
    <style>
    /* General container style */
    .main-container {
        padding: 1rem;
    }
    
    .pinned-msg {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%);
        border-radius: 18px;
        margin-bottom: 2rem;
    }
    .pinned-msg h1 {
        color: rgb(214, 51, 108);
        font-family: 'Baloo 2', cursive;
        font-size: 2.5rem;
        font-weight: 700;
    }
    /* Custom list style with icons */
    .icon-list-item {
        display: flex;
        align-items: center;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background-color: #f8f9fa;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #31333F; /* Set text color for dark mode visibility */
    }
    .icon-list-item span {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
          
    </style>
    """, unsafe_allow_html=True)

    

    with st.container():
    
        st.markdown("""
        <div class="pinned-msg">
            <h1>📌 Pinned Messages</h1>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()

def render_pinned_messages_page():
    
    # Initialize pinned messages if not exists
    if "pinned_messages" not in st.session_state:
        st.session_state.pinned_messages = []

    if not st.session_state.pinned_messages:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: rgba(255,255,255,0.1); border-radius: 15px; margin: 20px 0;">
            <h3>🔖 No Pinned Messages Yet</h3>
            <p>Pin important messages from your conversations to save them here for quick access.</p>
            <p><strong>How to pin:</strong> Look for the 📌 button next to any message in your chat conversations.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Stats section
    total_pinned = len(st.session_state.pinned_messages)
    user_pins = len([msg for msg in st.session_state.pinned_messages if msg.get("sender") == "user"])
    bot_pins = len([msg for msg in st.session_state.pinned_messages if msg.get("sender") == "bot"])

    st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <strong>📊 Your Pinned Messages:</strong> {total_pinned} total | {user_pins} from you | {bot_pins} from TalkHeal
    </div>
    """, unsafe_allow_html=True)

    # Filter options
    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        filter_sender = st.selectbox(
            "Filter by:",
            ["All Messages", "My Messages", "TalkHeal Messages"],
            key="pin_filter_sender"
        )

    with col2:
        sort_order = st.selectbox(
            "Sort by:",
            ["Recently Pinned", "Oldest First"],
            key="pin_sort_order"
        )

    # Apply filters
    filtered_messages = st.session_state.pinned_messages.copy()

    if filter_sender == "My Messages":
        filtered_messages = [msg for msg in filtered_messages if msg.get("sender") == "user"]
    elif filter_sender == "TalkHeal Messages":
        filtered_messages = [msg for msg in filtered_messages if msg.get("sender") == "bot"]

    # Apply sorting
    if sort_order == "Recently Pinned":
        filtered_messages.sort(key=lambda x: x.get("pinned_date", ""), reverse=True)
    else:
        filtered_messages.sort(key=lambda x: x.get("pinned_date", ""))

    if not filtered_messages:
        st.info("No messages match your current filter.")
        return

    # Clear all button
    if st.button("🗑️ Clear All Pinned Messages", type="secondary"):
        if st.session_state.get("confirm_clear_pins", False):
            st.session_state.pinned_messages = []
            st.session_state.confirm_clear_pins = False
            st.success("All pinned messages cleared!")
            st.rerun()
        else:
            st.session_state.confirm_clear_pins = True
            st.warning("Click again to confirm clearing all pinned messages.")
            st.rerun()

    st.markdown("---")

    # Render pinned messages using same chat bubble style
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for i, msg in enumerate(filtered_messages):
        sender = msg.get("sender", "bot")
        text = msg.get("message", "")

        if sender == "user":
            st.markdown(f"""
            <div class="user-message">
                {text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                {text}
            </div>
            """, unsafe_allow_html=True)

        # Unpin button
        if st.button("❌ Unpin", key=f"unpin_{i}"):
            st.session_state.pinned_messages.remove(msg)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# Main execution
if __name__ == "__main__":
    render_pinned_messages_page()
