import streamlit as st
from datetime import datetime
import json

# --- Blog Data ---
# In a real app, this might come from a database or a CMS.
# For now, we'll store it as a list of dictionaries.

def load_blog_posts():
    with open('data/blog_posts.json', 'r') as f:
        posts = json.load(f)
    for post in posts:
        post['date'] = datetime.strptime(post['date'], '%Y-%m-%d')
    return posts

BLOG_POSTS = load_blog_posts()


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
            st.image(post["featured_image"])
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

    # --- Post Content ---
    st.title(post["title"])
    st.caption(f"By {post['author']} on {post['date'].strftime('%B %d, %Y')}")
    st.image(post["featured_image"])
    st.markdown("---")
    st.markdown(post["content"], unsafe_allow_html=True)
    st.markdown("---")
    if st.button("← Back to Blog"):
        del st.session_state.selected_blog_post
        st.rerun()

    # --- Comments Section ---
    st.subheader("💬 Comments")

    post_comments = st.session_state.comments.get(post_id, [])

    if not post_comments:
        st.info("No comments yet. Be the first to comment!")
    else:
        for comment in post_comments:
            with st.container(border=True):
                st.caption(f"{comment['author']} on {comment['timestamp'].strftime('%B %d, %Y at %I:%M %p')}")
                st.write(comment["comment"])

    st.markdown("---")

    # --- Comment Form ---
    st.subheader("Leave a Comment")
    with st.form("comment_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        comment_text = st.text_area("Your Comment")
        submitted = st.form_submit_button("Submit Comment")

        if submitted and name and comment_text:
            if post_id not in st.session_state.comments:
                st.session_state.comments[post_id] = []
            
            st.session_state.comments[post_id].append({
                "author": name,
                "comment": comment_text,
                "timestamp": datetime.now()
            })
            st.rerun()

def show():
    """Main function to render the blog page."""
    # Initialize session state for comments if it doesn't exist
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    if "selected_blog_post" in st.session_state:
        show_full_post(st.session_state.selected_blog_post)
    else:
        show_blog_list()

show()