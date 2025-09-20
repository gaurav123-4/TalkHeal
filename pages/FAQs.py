import streamlit as st

# Page title
st.markdown("""
    <div style='background-color: #ffe4ef; border-radius: 15px; padding: 2rem; margin-bottom: 2rem;'>
        <h2 style='color: #d6336c; text-align: center;'>Frequently Asked Questions (FAQs)</h2>
    </div>
""", unsafe_allow_html=True)

# FAQ container
st.markdown("""
    <div style='background-color: #fff; border-radius: 10px; box-shadow: 0 2px 8px #d6336c22; padding: 2rem; margin-bottom: 2rem;'>
""", unsafe_allow_html=True)

# Question 1
with st.expander("What is TalkHeal?"):
    st.markdown("""
        <div style='padding: 1rem;'>
            TalkHeal is your trusted companion for mental wellness, designed to empower you on your journey to emotional health. Our platform combines science-backed tools, expert resources, and a supportive community to help you thrive every day.
        </div>
    """, unsafe_allow_html=True)

# Question 2
with st.expander("What are the key features of TalkHeal?"):
    st.markdown("""
        <div style='padding: 1rem;'>
            <b>Key Features include:</b>
            <ul>
                <li><b>Mood Tracking:</b> Visualize your emotional patterns and gain insights to improve your well-being.</li>
                <li><b>Coping Tools:</b> Access quick coping cards, breathing exercises, and journaling to manage stress and anxiety.</li>
                <li><b>Wellness Resource Hub:</b> Explore articles, self-help guides, and connect with specialists for expert advice.</li>
                <li><b>Community Support:</b> Join a safe, inclusive space to share experiences and find encouragement.</li>
                <li><b>Personalized Dashboard:</b> Track your progress and celebrate your achievements.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Question 3
with st.expander("Why should I use TalkHeal?"):
    st.markdown("""
        <div style='padding: 1rem;'>
            TalkHeal is designed with you in mind:
            <ul>
                <li>It has a beautiful, user-friendly design with soothing colors and intuitive navigation.</li>
                <li>It is accessible on all devices—desktop, tablet, and mobile.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Question 4
with st.expander("Is TalkHeal free to use?"):
    st.markdown("""
        <div style='padding: 1rem;'>
            Yes, TalkHeal is free to get started. We also offer premium resources for deeper support.
        </div>
    """, unsafe_allow_html=True)

# Question 5
with st.expander("Is my data secure and private?"):
    st.markdown("""
        <div style='padding: 1rem;'>
            Absolutely. We have a privacy-first approach. Your data is always secure and confidential.
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)