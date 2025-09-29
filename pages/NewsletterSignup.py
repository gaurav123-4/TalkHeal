import streamlit as st
import base64
import re

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
        
        h1 {{
            color: rgb(214, 51, 108) !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
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

def newsletter_signup_form():
    """Displays the newsletter signup form and handles submission."""
    
    # Regex for basic email validation
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: "Baloo 2", cursive;'>Subscribe to Our Weekly Newsletter</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                Get the latest wellness tips, mental health news, and exclusive content delivered straight to your inbox!
                <br><br>
                <b>Sign up below to join our community:</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key="newsletter_form"):
        email = st.text_input("Email Address", placeholder="Enter your email", key="newsletter_email")
        submit = st.form_submit_button("Subscribe", help="Sign up for our newsletter")
        
        if submit:
            if email and re.match(EMAIL_REGEX, email):
                # In a real app, you would save the email to a database here.
                st.success("Thank you for subscribing! You'll receive our next newsletter soon.")
                st.balloons()
            else:
                st.error("Please enter a valid email address.")
    
    st.markdown("<p style='text-align: center; color: #ff0a54; font-size: 0.9rem;'>We respect your privacy and will never share your email.</p>", unsafe_allow_html=True)

def show():
    """Renders the Newsletter Signup page."""
    st.title("Newsletter Signup")
    
    # Check if the user has already subscribed in this session
    if 'subscribed' not in st.session_state:
        st.session_state.subscribed = False

    if st.session_state.subscribed:
        st.success("You are already subscribed! Thank you for being a part of our community.")
        st.markdown("---")
        st.page_link("app.py", label="Back to Home", icon="🏠")
    else:
        newsletter_signup_form()

# To run the page
if __name__ == "__main__":
    show()