"""
OAuth Callback Page for TalkHeal
Handles OAuth authentication callbacks from providers
"""

import streamlit as st
import sys
import os

# Add the parent directory to the path to import auth modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Handle OAuth callback"""
    st.title("Authenticating...")
    
    # Get query parameters (support older/newer Streamlit)
    try:
        query_params = st.query_params  # Streamlit >= 1.30
    except Exception:
        try:
            query_params = st.experimental_get_query_params()
        except Exception:
            query_params = {}
    
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
    
    # Try to handle OAuth callback
    try:
        from auth.oauth_utils import handle_oauth_callback
        
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
    
    except Exception as e:
        st.error(f"OAuth error: {str(e)}")
        st.info("Please try logging in again.")
        
        if st.button("Back to Login"):
            st.switch_page("TalkHeal.py")

if __name__ == "__main__":
    main()

