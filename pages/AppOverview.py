import streamlit as st

def show_app_overview():

    # --- Community Toggle Button CSS and HTML ---
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
            <a href="/app" target="_self" style="text-decoration: none;">
                <button class="community-btn">
                    💬 Join the Community Forum
                </button>
            </a>
        </div>
    '''
    st.markdown(community_toggle_css, unsafe_allow_html=True)
    st.markdown(community_toggle_html, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #ffe4ef; border-radius: 15px; padding: 2rem; margin-bottom: 2rem;'>
            <h2 style='color: #d6336c; text-align: center;'>App Overview</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #fff; border-radius: 10px; box-shadow: 0 2px 8px #d6336c22; padding: 2rem; margin-bottom: 2rem;'>
            <h3 style='color: #d6336c;'>Welcome to TalkHeal!</h3>
            <div style='color: #000;'>
                TalkHeal is your trusted companion for mental wellness, designed to empower you on your journey to emotional health.<br><br>
                <b>Key Features:</b>
                <ul>
                    <li><b>Mood Tracking:</b> Visualize your emotional patterns.</li>
                    <li><b>Coping Tools:</b> Breathing exercises & journaling.</li>
                    <li><b>Resource Hub:</b> Articles, guides, expert advice.</li>
                    <li><b>Community Support:</b> Safe, inclusive space.</li>
                    <li><b>Dashboard:</b> Track progress and achievements.</li>
                </ul>
                <br>
                <b>Why TalkHeal?</b><br>
                <ul>
                    <li>Soothing, user-friendly design.</li>
                    <li>Privacy-first, secure data.</li>
                    <li>Works on all devices.</li>
                    <li>Free to start, premium for more.</li>
                </ul>
                <br>
                <b>Start your journey with TalkHeal and discover a happier, healthier you!</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 🔹 Call function so Streamlit actually runs it
show_app_overview()
