"""
OAuth Demo for TalkHeal
This script demonstrates how to use OAuth authentication
"""

import streamlit as st
from auth.oauth_config import oauth_config
from auth.oauth_utils import get_oauth_login_url

st.set_page_config(page_title="OAuth Demo", page_icon="🔐", layout="centered")

def main():
    st.title("TalkHeal OAuth Demo")
    st.markdown("This demo shows how OAuth authentication works in TalkHeal.")
    
    # Check available providers
    providers = oauth_config.get_available_providers()
    
    if not providers:
        st.error("No OAuth providers configured")
        st.info("Please set up your OAuth credentials in .env file")
        st.code("""
# Example .env file
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
        """)
        return
    
    st.success(f" {len(providers)} OAuth provider(s) configured")
    
    # Show provider details
    for provider in providers:
        with st.expander(f"🔧 {provider.title()} Configuration"):
            config = oauth_config.get_provider(provider)
            st.json({
                "Client ID": config.client_id[:10] + "...",
                "Redirect URI": config.redirect_uri,
                "Scope": config.scope,
                "Auth URL": config.auth_url
            })
    
    # Demo OAuth flow
    st.markdown("---")
    st.markdown("### 🚀 Try OAuth Login")
    
    for provider in providers:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button(f"Login with {provider.title()}", key=f"demo_{provider}"):
                try:
                    oauth_url = get_oauth_login_url(provider)
                    st.success(f" Generated OAuth URL for {provider}")
                    st.code(oauth_url, language="text")
                    
                    # In a real app, this would redirect the user
                    st.info("In the real app, this would redirect you to the OAuth provider")
                    
                except Exception as e:
                    st.error(f" Error generating OAuth URL: {e}")
        
        with col2:
            st.info(f"Click the button to generate a {provider.title()} OAuth URL")
    
    # Show OAuth flow diagram
    st.markdown("---")
    st.markdown("###  OAuth Flow Diagram")
    
    st.markdown("""
    ```mermaid
    sequenceDiagram
        participant U as User
        participant A as TalkHeal App
        participant P as OAuth Provider
        participant C as Callback Handler
        
        U->>A: Click "Login with Google"
        A->>A: Generate state parameter
        A->>U: Redirect to Google OAuth
        U->>P: Authorize application
        P->>C: Redirect with code & state
        C->>P: Exchange code for token
        P->>C: Return access token
        C->>P: Get user info with token
        P->>C: Return user data
        C->>A: Create/update user session
        A->>U: User logged in successfully
    ```
    """)
    
    # Security features
    st.markdown("---")
    st.markdown("### Security Features")
    
    security_features = [
        "✅ CSRF protection with state parameter",
        "✅ Secure token exchange",
        "✅ User data normalization",
        "✅ Session management",
        "✅ Provider verification",
        "✅ Error handling"
    ]
    
    for feature in security_features:
        st.markdown(feature)
    
    # Next steps
    st.markdown("---")
    st.markdown("### Next Steps")
    
    st.markdown("""
    1. **Set up OAuth providers** - Follow the setup guide in `OAUTH_SETUP.md`
    2. **Configure environment variables** - Add your OAuth credentials to `.env`
    3. **Test the integration** - Run `python test_oauth.py`
    4. **Start the app** - Run `streamlit run TalkHeal.py`
    5. **Try OAuth login** - Click the OAuth buttons on the login page
    """)

if __name__ == "__main__":
    main()

