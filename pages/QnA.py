import streamlit as st
import os
from datetime import datetime

def show():
    # Initialize session state for registered sessions
    if 'registered_sessions' not in st.session_state:
        st.session_state.registered_sessions = []

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
        st.image("static_files/pink.png", width=150)
        st.markdown("<p style='text-align: center;'><b>Dr. Rahul Kumar</b><br>Clinical Psychologist</p>", unsafe_allow_html=True)
    with col2:
        st.image("static_files/mint.png", width=150)
        st.markdown("<p style='text-align: center;'><b>Dr. Manish Kumar</b><br>Licensed Therapist</p>", unsafe_allow_html=True)
    with col3:
        st.image("static_files/lavender.png", width=150)
        st.markdown("<p style='text-align: center;'><b>Dr. Rajiv Kumar</b><br>Counseling Psychologist</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Upcoming Sessions Section
    upcoming_session = "Navigating Stress in the Digital Age"
    st.markdown("""
        <div style='background-color: var(--secondary-background-color); border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 2rem; margin-bottom: 2rem;'>
            <h3>Upcoming Sessions</h3>
            <h4>{upcoming_session}</h4>
            <p>
                Join Dr. Rahul Kumar for a live Q&A on managing stress and digital fatigue.
            </p>
            <p><b>Date:</b> October 15, 2025</p>
            <p><b>Time:</b> 6:00 PM GMT</p>
        </div>
    """, unsafe_allow_html=True)
    
    if upcoming_session in st.session_state.registered_sessions:
        st.success("You are already registered for this session!")
    else:
        if st.button("Register Now"):
            st.session_state.registered_sessions.append(upcoming_session)
            st.success("You have successfully registered for this session!")
            st.rerun()


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
            # Create a directory for questions if it doesn't exist
            if not os.path.exists("data/questions"):
                os.makedirs("data/questions")
            
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"data/questions/question_{now}.txt", "w") as f:
                f.write(question)
            st.success("Thank you for your submission!")
        else:
            st.warning("Please enter a question before submitting.")

show()