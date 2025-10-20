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


def render_page():
    """
    Loads CSS and displays the copyright notice page.
    """
    st.set_page_config(page_title="Copyright Notice", page_icon="©️")

    # 1. Separate CSS for better maintainability and import the Google Font.
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700&display=swap');

            .copyright-container {
                background: linear-gradient(135deg, #fef5f9 0%, #ffffff 100%);
                border-radius: 20px;
                box-shadow: 0 4px 25px rgba(210, 75, 125, 0.15);
                padding: 2.5rem;
                margin: 2rem auto;
                max-width: 900px;
                border: 1px solid #ffeaf2;
            }

            .copyright-container h2 {
                /* 3. Improved color contrast and added icon */
                color: #c53c6e;
                font-family: 'Baloo 2', cursive;
                font-weight: 700;
                text-align: center;
                margin-bottom: 2rem;
                font-size: 2.5rem;
            }

            .copyright-container p {
                color: #333;
                font-size: 1.1rem;
                /* 4. Enhanced readability with better line spacing */
                line-height: 1.7;
                margin-bottom: 1.25rem;
            }
            
            .copyright-container .notice {
                font-weight: bold;
                color: #333;
            }

            .copyright-container .last-updated {
                font-style: italic;
                text-align: right;
                font-size: 1rem;
                color: #555;
                margin-top: 2rem;
                margin-bottom: 0;
            }
            
            .copyright-container a {
                color: #c53c6e;
                text-decoration: none;
                font-weight: bold;
            }
            
            .copyright-container a:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. Use more semantic HTML and add a mailto link.
    st.markdown("""
        <div class="copyright-container">
            <h2>©️ Copyright Notice</h2>
            <p class="notice">Copyright &copy; 2025 TalkHeal. All rights reserved.</p>
            <p>
                All content, design, graphics, and code on this app are the property of TalkHeal and its creators unless otherwise stated.
            </p>
            <p>
                Unauthorized use, reproduction, or distribution of any material from this app is strictly prohibited.
            </p>
            <p>
                For permissions or inquiries, please contact us at <a href="mailto:support@talkheal.com">support@talkheal.com</a>.
            </p>
            <p class="last-updated">
                Last updated: September 2025
            </p>
        </div>
    """, unsafe_allow_html=True)

# Run the function to display the page
render_page()