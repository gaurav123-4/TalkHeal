import streamlit as st


# --- Custom CSS for Toggle Button ---
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
        <button class="community-btn" onclick="window.scrollTo({top: document.body.scrollHeight * 0.25, behavior: 'smooth'});">
            💬 Join the Community Forum
        </button>
    </div>
'''

st.set_page_config(page_title="TalkHeal Community", page_icon="💬", layout="wide")

st.title("💬 TalkHeal Community Forum")
st.markdown("""
Welcome to the anonymous support group and community forum! Here, you can connect with others who have similar experiences, share your thoughts, and find support in a safe, AI-moderated environment.

**Why join?**
- Share your story anonymously
- Get support from peers
- Help others by sharing your experience
- AI moderation ensures a safe and supportive space
""")




# --- Chat Sessions Section (placeholder for where your chat session UI ends) ---
# ...existing code for chat sessions...

# --- Community Forum Box (styled like Chat Sessions/Profile) ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #ffe4f0 0%, #fff 100%); border-radius: 16px; box-shadow: 0 2px 12px 0 rgba(209,74,122,0.10); padding: 1.2rem 1.2rem 1rem 1.2rem; margin: 1.2rem 0;">
        <div style="font-weight: 600; font-size: 1.1rem; color: #d14a7a; margin-bottom: 0.5rem; display: flex; align-items: center;">
            <span style='font-size:1.3rem; margin-right:0.5rem;'>💬</span> Community Forum
        </div>
        <div style="color: #222; font-size: 0.98rem; margin-bottom: 0.7rem;">
            Connect, share, and support each other in a safe space.
        </div>
        <form action="#community-forum-section">
            <button style="background: linear-gradient(90deg, #ffb6d5 0%, #d14a7a 100%); color: white; font-weight: 600; border: none; border-radius: 1.2rem; padding: 0.6rem 1.5rem; font-size: 1rem; cursor: pointer; box-shadow: 0 2px 8px 0 rgba(209,74,122,0.13); transition: background 0.2s;" type="submit">
                Go to Forum
            </button>
        </form>
    </div>
""", unsafe_allow_html=True)


# --- Community Forum Toggle Button (Best UX) ---
st.markdown("""
    <style>
    .community-forum-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, #fcb1e0 0%, #d14a7a 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 1.2rem;
        padding: 0.7rem 1.7rem;
        margin: 1.2rem 0 0.7rem 0;
        box-shadow: 0 2px 10px 0 rgba(209,74,122,0.13);
        cursor: pointer;
        transition: background 0.2s, transform 0.1s;
        outline: none;
        width: 100%;
        max-width: 250px;
    }
    .community-forum-btn:hover {
        background: linear-gradient(90deg, #d14a7a 0%, #fcb1e0 100%);
        transform: translateY(-2px) scale(1.03);
    }
    </style>
    <script>
    function scrollToForum() {
        const forum = document.getElementById('community-forum-section');
        if (forum) {
            forum.scrollIntoView({behavior: 'smooth'});
        }
    }
    </script>
    <div style="display: flex; justify-content: center;">
        <button class="community-forum-btn" onclick="scrollToForum()">💬 Community Forum</button>
    </div>
""", unsafe_allow_html=True)


# --- Forum Section ---
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
