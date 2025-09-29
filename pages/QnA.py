import streamlit as st
import base64

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


def show():
    # Page Header
    st.markdown("""
        <div style='background: var(--secondary-background-color); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(0,0,0,0.1); padding: 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='text-align: center; font-family: "Helvetica Neue", sans-serif;'>Expert-Led Q&A Sessions</h2>
            <p style='font-size: 1.1rem; text-align: center;'>
                Connect with licensed mental health professionals, gain valuable insights, and get your questions answered in our expert-led sessions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Meet our Experts Section
    st.markdown("<h3 style='text-align: center;'>Meet Our Experts</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("static_files/blue.png", width=150)
        st.markdown("<p style='text-align: center;'><b>Dr. Rahul Kumar</b><br>Clinical Psychologist</p>", unsafe_allow_html=True)
    with col2:
        st.image("static_files/mint.png", width=150)
        st.markdown("<p style='text-align: center;'><b>Dr. Manish Kumar</b><br>Licensed Therapist</p>", unsafe_allow_html=True)
    with col3:
        st.image("static_files/lavender.png", width=150)
        st.markdown("<p style='text-align: center;'><b>Dr. Rajiv Kumar</b><br>Counseling Psychologist</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Upcoming Sessions Section
    st.markdown("""
        <div style='background-color: var(--secondary-background-color); border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 2rem; margin-bottom: 2rem;'>
            <h3>Upcoming Sessions</h3>
            <h4>Navigating Stress in the Digital Age</h4>
            <p>
                Join Dr. Rahul Kumar for a live Q&A on managing stress and digital fatigue.
            </p>
            <p><b>Date:</b> October 15, 2025</p>
            <p><b>Time:</b> 6:00 PM GMT</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Register Now"):
        st.success("Registration is not yet open. Please check back later!")


    st.markdown("---")

    # Past Sessions Section
    st.markdown("<h3>Past Sessions</h3>", unsafe_allow_html=True)

    st.markdown("<h4>Understanding Anxiety</h4>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=G0zJGDokyA")
    st.markdown("A short animated video explaining the basics of mental health and anxiety.")

    st.markdown("<h4>Mindfulness and Meditation Techniques</h4>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=O-6f5wQXSu8") # Placeholder video
    st.markdown("Learn simple mindfulness and meditation techniques to calm your mind.")


    st.markdown("---")

    # Submit a Question Section
    st.markdown("<h3>Submit a Question</h3>", unsafe_allow_html=True)
    question = st.text_area("Have a question for our experts? Submit it here and we might answer it in our next session.", height=150)
    if st.button("Submit Question"):
        if question:
            st.success("Thank you for your submission!")
        else:
            st.warning("Please enter a question before submitting.")

show()