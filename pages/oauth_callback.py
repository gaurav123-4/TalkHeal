"""
OAuth Callback Page for TalkHeal
Handles OAuth authentication callbacks from providers
"""

import streamlit as st
from urllib.parse import parse_qs, urlparse
from auth.oauth_utils import handle_oauth_callback

st.set_page_config(page_title="OAuth Callback", page_icon="🔐", layout="centered")

def main():
    """Handle OAuth callback"""
    st.title("Authenticating...")
    
    # Get query parameters
    query_params = st.query_params
    
    # Check for required parameters
    code = query_params.get("code")
    state = query_params.get("state")
    provider = query_params.get("provider")
    error = query_params.get("error")
    
    if error:
        st.error(f"OAuth Error: {error}")
        st.info("Please try logging in again.")
        if st.button("Back to Login"):
            st.switch_page("TalkHeal.py")
        return
    
    if not all([code, state, provider]):
        st.error("Missing required OAuth parameters")
        st.info("Please try logging in again.")
        if st.button("Back to Login"):
            st.switch_page("TalkHeal.py")
        return
    
    # Show loading spinner
    with st.spinner("Authenticating with OAuth provider..."):
        success, message = handle_oauth_callback(provider, code, state)
    
    if success:
        st.success("Authentication successful!")
        st.balloons()
        
        st.info("Redirecting to TalkHeal...")
        st.rerun()
    else:
        st.error(f"Authentication failed: {message}")
        st.info("Please try logging in again.")
        
        if st.button("Back to Login"):
            st.switch_page("TalkHeal.py")

if __name__ == "__main__":
    main()
