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
        "content": '''
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
        '''
    },
    {
        "id": 2,
        "title": "Your Mood is a Map: How Tracking Your Emotions Can Guide You",
        "author": "Team Talkheal",
        "date": datetime(2025, 9, 22),
        "excerpt": "Our feelings can seem chaotic, but they hold valuable clues to our well-being. Discover how the simple act of tracking your mood can serve as a personal map, guiding you toward greater self-awareness and emotional balance...",
        "content": '''
            <p>Our emotions can often feel like unpredictable weather—stormy one moment, sunny the next. But what if you had a way to navigate this internal landscape? Mood tracking is that compass. It's the simple practice of noting how you feel each day, and it's a powerful tool for self-discovery.</p>

            <h4>1. Why Track Your Mood?</h4>
            <p>Awareness is the first step to change. By consistently checking in with yourself, you move from being reactive to your emotions to being proactive. Tracking helps you see beyond the immediate feeling and understand the bigger picture of your emotional health. It provides a baseline, allowing you to notice when things are off and celebrate when you're feeling good.</p>

            <h4>2. How to Start: The Art of the Daily Check-in</h4>
            <p>Getting started is easy. Use the <b>Mood Dashboard</b> feature in TalkHeal to log how you're feeling. Was it a 'Happy' day or a 'Stressed' one? You don't need to write a novel. A simple, honest label is enough. The goal is to create a consistent habit of pausing and acknowledging your internal state without judgment.</p>

            <h4>3. Connect the Dots: Identify Your Patterns</h4>
            <p>After a week or two of tracking, you'll have a valuable set of data. Now you can become a detective in your own life. Look for patterns:
            <ul>
                <li>Do you feel more anxious after drinking coffee?</li>
                <li>Does a good night's sleep consistently lead to a better mood?</li>
                <li>Is there a particular day of the week that you often feel down?</li>
            </ul>
            These connections, which might seem obvious in hindsight, are often hidden in the noise of daily life. Seeing them written down makes them tangible and actionable.</p>

            <h4>4. From Insight to Action</h4>
            <p>Your mood map isn't just for observation; it's for navigation. Once you identify a pattern, you can make small, intentional changes. If you notice that a morning walk boosts your mood, you can prioritize it. If you find that scrolling social media before bed correlates with anxiety, you can create a new wind-down routine. Your data empowers you to make informed decisions that genuinely support your well-being.</p>
            <hr>
            <p>Your feelings are valid, and they are valuable sources of information. Start tracking your mood today and discover the power of your own emotional map.</p>
        '''
    },
    {
        "id": 3,
        "title": "The Science of Small Wins: Building Healthy Habits That Stick",
        "author": "Team Talkheal",
        "date": datetime(2025, 9, 22),
        "excerpt": "Big life changes often start with the smallest steps. We explore the science behind how habits are formed and offer practical, gentle strategies to help you build positive routines that last, one small win at a time...",
        "content": '''
            <p>Have you ever set a huge goal—like meditating for 30 minutes every day—only to give up after a few attempts? You're not alone. The secret to lasting change isn't about massive bursts of effort; it's about the quiet, consistent power of small, positive habits.</p>

            <h4>1. The Habit Loop: Cue, Routine, Reward</h4>
            <p>Scientists who study behavior have identified a simple neurological loop at the core of every habit. It consists of three parts:
            <ul>
                <li><b>The Cue:</b> A trigger that tells your brain to go into automatic mode (e.g., putting on your running shoes).</li>
                <li><b>The Routine:</b> The physical or emotional action you take (e.g., going for a run).</li>
                <li><b>The Reward:</b> A positive stimulus that tells your brain this loop is worth remembering for the future (e.g., the feeling of accomplishment afterward).</li>
            </ul>
            To build a new habit, you need to make this loop work for you, not against you.</p>

            <h4>2. Start 'Too Small to Fail'</h4>
            <p>The biggest mistake we make is starting too big. Instead, make your new habit so easy that you can't say no. Want to start journaling? Don't commit to writing three pages; commit to writing <b>one sentence</b>. Want to meditate? Start with <b>one minute</b>. These 'small wins' release dopamine in your brain, creating a positive feedback loop that builds momentum.</p>

            <h4>3. Habit Stacking: Anchor the New to the Old</h4>
            <p>A powerful technique is to 'stack' your new habit on top of an existing one. The existing habit acts as the cue. For example:
            <ul>
                <li>"After I brush my teeth (existing habit), I will do two minutes of stretching (new habit)."</li>
                <li>"After I pour my morning coffee (existing habit), I will open my journal (new habit)."</li>
            </ul>
            This anchors the new behavior to a solid foundation, making it much more likely to stick.</p>

            <h4>4. Track the Process, Not Just the Goal</h4>
            <p>Focus on showing up, not on the results. Use the <b>Habit Builder</b> in TalkHeal to track your consistency. Seeing a chain of checkmarks is a powerful reward in itself. It shifts your focus from a distant, intimidating goal to the simple, achievable act of not breaking the chain today. If you miss a day, don't panic. The rule is simple: never miss twice.</p>
            <hr>
            <p>Be patient and celebrate your small wins. Lasting change is a marathon, not a sprint, and it's built one tiny, consistent step at a time.</p>
        '''
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