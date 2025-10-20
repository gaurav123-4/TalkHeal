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

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Connect with TalkHeal on Social Media</h2>
            <div style='color: #222; font-size: 1.1rem;'>
                Stay updated, inspired, and engaged!<br><br>
                <b>Follow us for:</b>
                <ul>
                    <li>Daily wellness tips and motivational posts</li>
                    <li>Community stories and success journeys</li>
                    <li>Live events, Q&A sessions, and more</li>
                </ul>
                <br>
                <b>Our Social Media Channels:</b>
                <ul>
                    <li><a href='https://www.instagram.com/talkheal' target='_blank' style='color:#d14a7a;'>Instagram</a></li>
                    <li><a href='https://www.facebook.com/talkheal' target='_blank' style='color:#d14a7a;'>Facebook</a></li>
                    <li><a href='https://twitter.com/talkheal' target='_blank' style='color:#d14a7a;'>Twitter (X)</a></li>
                    <li><a href='https://www.linkedin.com/company/talkheal' target='_blank' style='color:#d14a7a;'>LinkedIn</a></li>
                    <li><a href='https://www.youtube.com/@talkheal' target='_blank' style='color:#d14a7a;'>YouTube</a></li>
                </ul>
                <br>
                <i>Join our online family and be part of the movement for better mental wellness!</i>
            </div>
        </div>
    """, unsafe_allow_html=True)

show()