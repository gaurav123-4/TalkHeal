import streamlit as st

def render_page():
    """
    Loads CSS and displays the copyright notice page.
    """
    st.set_page_config(page_title="Copyright Notice", page_icon="©️")

    # 1. Separate CSS for better maintainability and import the Google Font.
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700&display=swap');

            .copyright-container {
                background: linear-gradient(135deg, #fef5f9 0%, #ffffff 100%);
                border-radius: 20px;
                box-shadow: 0 4px 25px rgba(210, 75, 125, 0.15);
                padding: 2.5rem;
                margin: 2rem auto;
                max-width: 900px;
                border: 1px solid #ffeaf2;
            }

            .copyright-container h2 {
                /* 3. Improved color contrast and added icon */
                color: #c53c6e;
                font-family: 'Baloo 2', cursive;
                font-weight: 700;
                text-align: center;
                margin-bottom: 2rem;
                font-size: 2.5rem;
            }

            .copyright-container p {
                color: #333;
                font-size: 1.1rem;
                /* 4. Enhanced readability with better line spacing */
                line-height: 1.7;
                margin-bottom: 1.25rem;
            }
            
            .copyright-container .notice {
                font-weight: bold;
                color: #333;
            }

            .copyright-container .last-updated {
                font-style: italic;
                text-align: right;
                font-size: 1rem;
                color: #555;
                margin-top: 2rem;
                margin-bottom: 0;
            }
            
            .copyright-container a {
                color: #c53c6e;
                text-decoration: none;
                font-weight: bold;
            }
            
            .copyright-container a:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. Use more semantic HTML and add a mailto link.
    st.markdown("""
        <div class="copyright-container">
            <h2>©️ Copyright Notice</h2>
            <p class="notice">Copyright &copy; 2025 TalkHeal. All rights reserved.</p>
            <p>
                All content, design, graphics, and code on this app are the property of TalkHeal and its creators unless otherwise stated.
            </p>
            <p>
                Unauthorized use, reproduction, or distribution of any material from this app is strictly prohibited.
            </p>
            <p>
                For permissions or inquiries, please contact us at <a href="mailto:support@talkheal.com">support@talkheal.com</a>.
            </p>
            <p class="last-updated">
                Last updated: September 2025
            </p>
        </div>
    """, unsafe_allow_html=True)

# Run the function to display the page
render_page()