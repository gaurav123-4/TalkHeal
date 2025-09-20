import streamlit as st
from datetime import datetime

# --- Blog Data ---
# In a real app, this might come from a database or a CMS.
# For now, we'll store it as a list of dictionaries.

BLOG_POSTS = [
    {
        "id": 1,
        "title": "How to Start Your Healing Journey: A Beginner's Guide",
        "author": "Team Talkheal",
        "date": datetime(2025, 9, 19),
        "excerpt": "Healing is not a destination, but a gentle, ongoing process of returning to yourself. This guide offers five simple yet powerful first steps you can take today...",
        "content": """
            <p>Healing is a personal and often non-linear journey. It's about progress, not perfection. If you're feeling lost and don't know where to begin, remember that the smallest step in the right direction can make the biggest difference. Here are five simple yet powerful first steps you can take today.</p>

            <h4>1. Acknowledge Your Feelings Without Judgment</h4>
            <p>The first step is always awareness. Allow yourself to feel whatever you are feeling—sadness, anger, confusion, or numbness. Don't try to suppress these emotions or judge yourself for having them. Find a quiet space, take a deep breath, and simply say to yourself, "I am feeling [your emotion], and that is okay." This simple act of validation is a powerful form of self-compassion.</p>

            <h4>2. Practice Mindful Breathing</h4>
            <p>When we are overwhelmed, our breathing often becomes shallow and rapid. Ground yourself in the present moment with a simple breathing exercise.
            <ul>
                <li>Find a comfortable position, either sitting or lying down.</li>
                <li>Close your eyes and place one hand on your belly.</li>
                <li>Inhale slowly through your nose for a count of four, feeling your belly rise.</li>
                <li>Hold your breath for a count of four.</li>
                <li>Exhale slowly through your mouth for a count of six, feeling your belly fall.</li>
            </ul>
            Repeat this for 2-3 minutes. This technique, known as diaphragmatic breathing, activates the body's relaxation response and can instantly reduce feelings of anxiety.</p>

            <h4>3. Write It Down: The Power of Journaling</h4>
            <p>You don't have to be a writer to benefit from journaling. Get a notebook or use the journaling feature in TalkHeal and just start writing. Don't worry about grammar or making sense. This is for your eyes only.
            <br><br>
            Try one of these prompts:
            <ul>
                <li>"Today, I am feeling..."</li>
                <li>"One thing I can do to be kind to myself right now is..."</li>
                <li>"What is one small thing that brought me a moment of peace today?"</li>
            </ul>
            Externalizing your thoughts can bring clarity and provide a sense of release.</p>

            <h4>4. Connect with Nature</h4>
            <p>Nature has a profound ability to soothe and heal. If you can, spend 10-15 minutes outdoors. It doesn't have to be a strenuous hike; a simple walk in a local park, sitting on a bench, or even just paying attention to the sky from your window can help. Focus on the sensory details—the feeling of the sun on your skin, the sound of birds, the smell of rain. This helps pull you out of your internal world and into the calming presence of the natural world.</p>

            <h4>5. Reach Out for Support</h4>
            <p>Healing doesn't have to be a solitary journey. Reaching out is a sign of strength, not weakness. This could mean talking to a trusted friend or family member, or simply starting a conversation with your AI companion here at TalkHeal. Sharing your experience can lessen the burden and remind you that you are not alone.</p>
            <hr>
            <p>Remember, your healing journey is uniquely yours. Be patient and compassionate with yourself. Every step, no matter how small, is a victory.</p>
        """
    }
]

def show_blog_list():
    """Displays the list of blog post summaries."""
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem; margin: 2rem auto; max-width: 900px; text-align: center;'>
            <h1 style='color: #d14a7a; font-family: "Baloo 2", cursive;'>The TalkHeal Blog</h1>
            <p style='font-size: 1.1rem;'>Articles, tips, and stories to support your mental wellness journey.</p>
        </div>
    """, unsafe_allow_html=True)

    for post in sorted(BLOG_POSTS, key=lambda x: x["date"], reverse=True):
        st.markdown("---")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader(post["title"])
            st.caption(f"By {post['author']} on {post['date'].strftime('%B %d, %Y')}")
            st.write(post["excerpt"])
        with col2:
            if st.button("Read More", key=f"read_{post['id']}", use_container_width=True):
                st.session_state.selected_blog_post = post['id']
                st.rerun()

def show_full_post(post_id):
    """Displays the full content of a selected blog post."""
    post = next((p for p in BLOG_POSTS if p["id"] == post_id), None)
    if not post:
        st.error("Blog post not found.")
        if st.button("← Back to Blog"):
            del st.session_state.selected_blog_post
            st.rerun()
        return

    st.title(post["title"])
    st.caption(f"By {post['author']} on {post['date'].strftime('%B %d, %Y')}")
    st.markdown("---")
    st.markdown(post["content"], unsafe_allow_html=True)
    st.markdown("---")
    if st.button("← Back to Blog"):
        del st.session_state.selected_blog_post
        st.rerun()

def show():
    """Main function to render the blog page."""
    if "selected_blog_post" in st.session_state:
        show_full_post(st.session_state.selected_blog_post)
    else:
        show_blog_list()

show()