import streamlit as st
import base64

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
            background-color: {'rgba(0, 0, 0, 0.5)' if is_dark else 'rgba(255, 255, 255, 0.3)'} !important;
            transition: background-color 0.4s ease;
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


def show_app_overview():

    # --- Community Toggle Button CSS and HTML ---
    community_toggle_css = '''
        <style>
        .community-toggle {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 2rem auto 1.5rem auto;
        }
        .community-btn {
            background: linear-gradient(90deg, #ffb6d5 0%, #d14a7a 100%);
            color: white;
            font-size: 1.3rem;
            font-weight: 600;
            border: none;
            border-radius: 2rem;
            padding: 0.9rem 2.2rem;
            box-shadow: 0 4px 18px 0 rgba(209,74,122,0.13);
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            outline: none;
        }
        .community-btn:hover {
            background: linear-gradient(90deg, #d14a7a 0%, #ffb6d5 100%);
            transform: translateY(-2px) scale(1.04);
        }
        </style>
    '''
    community_toggle_html = '''
        <div class="community-toggle">
            <a href="/app" target="_self" style="text-decoration: none;">
                <button class="community-btn">
                    💬 Join the Community Forum
                </button>
            </a>
        </div>
    '''
    st.markdown(community_toggle_css, unsafe_allow_html=True)
    st.markdown(community_toggle_html, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #ffe4ef; border-radius: 15px; padding: 2rem; margin-bottom: 2rem;'>
            <h2 style='color: #d6336c; text-align: center;'>App Overview</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #fff; border-radius: 10px; box-shadow: 0 2px 8px #d6336c22; padding: 2rem; margin-bottom: 2rem;'>
            <h3 style='color: #d6336c;'>Welcome to TalkHeal!</h3>
            <div style='color: #000;'>
                TalkHeal is your trusted companion for mental wellness, designed to empower you on your journey to emotional health.<br><br>
                <b>Key Features:</b>
                <ul>
                    <li><b>Mood Tracking:</b> Visualize your emotional patterns.</li>
                    <li><b>Coping Tools:</b> Breathing exercises & journaling.</li>
                    <li><b>Resource Hub:</b> Articles, guides, expert advice.</li>
                    <li><b>Community Support:</b> Safe, inclusive space.</li>
                    <li><b>Dashboard:</b> Track progress and achievements.</li>
                </ul>
                <br>
                <b>Why TalkHeal?</b><br>
                <ul>
                    <li>Soothing, user-friendly design.</li>
                    <li>Privacy-first, secure data.</li>
                    <li>Works on all devices.</li>
                    <li>Free to start, premium for more.</li>
                </ul>
                <br>
                <b>Start your journey with TalkHeal and discover a happier, healthier you!</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 🔹 Call function so Streamlit actually runs it
show_app_overview()
