import streamlit as st

st.set_page_config(page_title="Community Forum", page_icon="🌐", layout="wide")
st.title("🌐 Community Forum")
st.markdown("""
Welcome to the TalkHeal Community Forum! Here you can connect, share experiences, ask questions, and support each other in a safe, AI-moderated environment.

**Why join?**
- Share your story anonymously
- Get support from peers
- Help others by sharing your experience
- AI moderation ensures a safe and supportive space
""")

with st.expander("📘 Forum Guidelines"):
    st.markdown("""
    - **Be Kind & Respectful:** Treat everyone with respect. No personal attacks.
    - **Stay Anonymous:** Do not share personal identifying information.
    - **Offer Support:** Provide constructive and supportive feedback.
    - **Safety First:** Do not post content that is graphic or promotes self-harm. Our AI moderator is here to help.
    """)

st.markdown('<div id="community-forum-section"></div>', unsafe_allow_html=True)
with st.expander("Join the Anonymous Support Group"):
	st.write("Post your message or support request below. All posts are anonymous and moderated by AI for safety.")
	user_message = st.text_area("Share your thoughts or ask for support:", max_chars=500)
	if st.button("Post Anonymously"):
		if user_message.strip():
			st.success("Your message has been posted anonymously! (Demo: Not stored)")
		else:
			st.warning("Please enter a message before posting.")

st.markdown("---")
st.info("This is a demo. In a full implementation, messages would be stored securely and AI moderation would be active.")
