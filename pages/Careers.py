import streamlit as st
import os
from datetime import datetime

def show():
    st.markdown("""        <style>
            .career-container {
                background-color: var(--secondary-background-color);
                color: var(--text-color);
                padding: 2rem;
                border-radius: 10px;
                margin: 2rem auto;
                max-width: 900px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .opening-item {
                padding: 0.5rem 0;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .opening-item:hover {
                background-color: rgba(0,0,0,0.05);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='career-container'>", unsafe_allow_html=True)
    
    st.header("🚀 Careers at TalkHeal")
    st.write("Join our mission to support mental wellness and make a real impact!")
    
    st.markdown("---")
    
    st.subheader("Current Openings")
    
    openings = {
        "Community Manager": "🤝",
        "Content Writer (Mental Health)": "✍️",
        "Full Stack Developer": "💻",
        "UI/UX Designer": "🎨"
    }
    
    for opening, icon in openings.items():
        st.markdown(f"<div class='opening-item'>{icon} {opening}</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("Apply Now")
    
    with st.form("application_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        position = st.selectbox("Position", options=list(openings.keys()))
        resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])
        cover_letter = st.text_area("Cover Letter (Optional)")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if name and email and position and resume:
                # Create a directory for applications if it doesn't exist
                if not os.path.exists("data/applications"):
                    os.makedirs("data/applications")
                
                # Create a directory for the specific application
                now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                application_dir = f"data/applications/{name.replace(' ', '_')}_{now}"
                os.makedirs(application_dir)
                
                # Save the resume
                with open(os.path.join(application_dir, resume.name), "wb") as f:
                    f.write(resume.getbuffer())
                    
                # Save the application info
                with open(os.path.join(application_dir, "application.txt"), "w") as f:
                    f.write(f"Name: {name}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"Position: {position}\n")
                    f.write(f"Cover Letter:\n{cover_letter}")
                    
                st.success("Your application has been submitted successfully! We will get back to you soon.")
            else:
                st.error("Please fill out all the required fields.")

    st.info("More roles and details coming soon!")
    
    st.markdown("</div>", unsafe_allow_html=True)

show()