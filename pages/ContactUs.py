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
    """Renders a more visually appealing Community page using tabs and icons."""

    st.markdown("""
    <style>
    /* General container style */
    .main-container {
        padding: 1rem;
    }
   
    .contact-container {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%);
        border-radius: 18px;
        margin-bottom: 2rem;
    }
    .contact-container h1 {
        color: rgb(214, 51, 108);
        font-family: 'Baloo 2', cursive;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .contact-container p {
        color: #333;
        font-size: 1.2rem;
        font-style: italic;
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
        # --- Header Section --- 
        st.markdown("""
        <div class="contact-container">
            <h1>📞Contact Us</h1>
            <p>We'd love to hear from you! Please fill out the form below or reach out to us via email.</p>
        </div>
        """, unsafe_allow_html=True)


    # --- Interactive Contact Form ---
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name", placeholder="Enter your name")
        email = st.text_input("Your Email", placeholder="Enter your valid email address")
        subject = st.selectbox(
            "Subject",
            ["General Inquiry", "Technical Support", "Feedback & Suggestions", "Careers"]
        )
        message = st.text_area("Message", height=150, placeholder="How can we help?")
        
        submitted = st.form_submit_button("Send Message")
        
        if submitted:
            # In a real app, you would add logic here to email the form data.
            st.success("Thank you for your message! We'll get back to you soon.")

    st.divider()

    # --- Other Contact Info ---
    st.markdown("""
        <p>
            <b>Or contact us directly:</b><br>
            <b>Email:</b> <a href='mailto:support@talkheal.com'>support@talkheal.com</a><br>
            <b>Careers:</b> <a href='mailto:careers@talkheal.com'>careers@talkheal.com</a><br>
            <b>Community:</b> <a href='mailto:community@talkheal.com'>community@talkheal.com</a><br><br>
            <b>Follow us on Social Media:</b><br>
            <a href='https://instagram.com/talkheal' target='_blank'>Instagram</a> | 
            <a href='https://twitter.com/talkheal' target='_blank'>Twitter</a> | 
            <a href='https://facebook.com/talkheal' target='_blank'>Facebook</a>
        </p>
    """, unsafe_allow_html=True)

    # Close the div
    st.markdown("</div>", unsafe_allow_html=True)

show()