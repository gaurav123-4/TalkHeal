import streamlit as st
import base64
from components.reset_page import show_reset_password_page

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

# --- Grab token from URL ---
reset_token = st.query_params.get("token")

# --- Initialize session state ---
if "reset_token" not in st.session_state:
    st.session_state.reset_token = None
if "show_reset_page" not in st.session_state:
    st.session_state.show_reset_page = False

# --- If token exists in URL, save it and show reset page ---
if reset_token:
    st.session_state.reset_token = reset_token
    st.session_state.show_reset_page = True

def run():
    if st.session_state.show_reset_page and st.session_state.reset_token:
        show_reset_password_page()
    else:
        st.info("No reset token provided. Please check your email link.")

if __name__ == "__main__":
    run()
