import streamlit as st
import base64
from pathlib import Path

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
    """Renders a more visually appealing Community page using tabs and icons."""

    st.markdown("""
    <style>
    /* General container style */
    .main-container {
        padding: 1rem;
    }
    /* Header style */
    .community-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%);
        border-radius: 18px;
        margin-bottom: 2rem;
    }
    .community-header h1 {
        color: rgb(214, 51, 108);
        font-family: 'Baloo 2', cursive;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .community-header p {
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
        <div class="community-header">
            <h1>👋Welcome to the TalkHeal Community</h1>
            <p>Connect. Share. Grow.</p>
        </div>
        """, unsafe_allow_html=True)

        # --- Tabs Section --- 
        tab1, tab2, tab3 = st.tabs(["✨ Features", "💖 Our Promise", "📜 Guidelines"])

        with tab1:
            st.subheader("What You'll Find Inside")
            features = {
                "💬": "Share your journey: A space to inspire and be inspired.",
                "🤝": "Find encouragement: Get support from members who understand.",
                "🎉": "Join community events: Participate in challenges and discussions.",
                "📚": "Access exclusive resources: Unlock group activities and wellness tools."
            }
            for icon, text in features.items():
                st.markdown(f'<div class="icon-list-item"><span>{icon}</span> {text}</div>', unsafe_allow_html=True)

        with tab2:
            st.subheader("A Community You Can Trust")
            promises = {
                "🛡️": "A safe and inclusive space: We prioritize your emotional safety.",
                "⚖️": "Professionally moderated: Cared for by professionals and trained volunteers.",
                "😊": "Build lasting connections: Make friends and find your support system.",
                "🤫": "Non-judgmental atmosphere: Come as you are. You are welcome here."
            }
            for icon, text in promises.items():
                st.markdown(f'<div class="icon-list-item"><span>{icon}</span> {text}</div>', unsafe_allow_html=True)

        with tab3:
            st.subheader("Our Shared Values")
            guidelines = {
                "Respect": "Treat everyone with kindness. Healthy debates are natural, but personal attacks are not.",
                "Confidentiality": "What is shared in the community should stay in the community. Do not share personal stories outside this space.",
                "Support": "Offer genuine and constructive support. Avoid giving unsolicited advice.",
                "Safety": "Do not post content that is graphic, violent, or promotes self-harm. If you are in crisis, please use our emergency resources."
            }
            for title, desc in guidelines.items():
                with st.expander(f"**{title}**"):
                    st.write(desc)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Call to Action --- 
        st.info("Ready to be part of something beautiful? Join the conversation today!")
        st.page_link("pages/CommunityForum.py", label="Go to the Community Forum", icon="➡️", use_container_width=True)

# To run the page
if __name__ == "__main__":
    show()