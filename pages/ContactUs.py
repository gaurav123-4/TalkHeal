import streamlit as st

def show():
    # Inject CSS to style the container
    st.markdown("""
        <style>
            .contact-container {
                background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%);
                border-radius: 18px;
                box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12);
                padding: 2.5rem;
                margin: 2rem auto;
                max-width: 900px;
            }
            .contact-container h2 {
                color: #d14a7a;
                font-family: 'Baloo 2', cursive;
            }
        </style>
    """, unsafe_allow_html=True)

    # Use a markdown div to apply the custom class
    st.markdown("<div class='contact-container'>", unsafe_allow_html=True)

    st.markdown("<h2>Contact Us</h2>", unsafe_allow_html=True)
    st.write("We'd love to hear from you! Please fill out the form below or reach out to us via email.")
    st.write("") # Add a little space

    # --- Interactive Contact Form ---
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name", placeholder="Enter your name")
        email = st.text_input("Your Email", placeholder="Enter your valid email address")
        subject = st.selectbox(
            "Subject",
            ["General Inquiry", "Technical Support", "Feedback & Suggestions", "Careers"]
        )
        message = st.text_area("Message", height=150, placeholder="How can we help?")
        
        submitted = st.form_submit_button("Send Message")
        
        if submitted:
            # In a real app, you would add logic here to email the form data.
            st.success("Thank you for your message! We'll get back to you soon.")

    st.divider()

    # --- Other Contact Info ---
    st.markdown("""
        <p>
            <b>Or contact us directly:</b><br>
            <b>Email:</b> <a href='mailto:support@talkheal.com'>support@talkheal.com</a><br>
            <b>Careers:</b> <a href='mailto:careers@talkheal.com'>careers@talkheal.com</a><br>
            <b>Community:</b> <a href='mailto:community@talkheal.com'>community@talkheal.com</a><br><br>
            <b>Follow us on Social Media:</b><br>
            <a href='https://instagram.com/talkheal' target='_blank'>Instagram</a> | 
            <a href='https://twitter.com/talkheal' target='_blank'>Twitter</a> | 
            <a href='https://facebook.com/talkheal' target='_blank'>Facebook</a>
        </p>
    """, unsafe_allow_html=True)

    # Close the div
    st.markdown("</div>", unsafe_allow_html=True)

show()