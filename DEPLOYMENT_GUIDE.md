# TalkHeal Streamlit Cloud Deployment Guide

## Quick Fixes for Common Deployment Issues

### 1. Clean Requirements.txt
The requirements.txt has been cleaned up. Make sure it matches the current version.

### 2. Streamlit Cloud Configuration

#### Step 1: Create `.streamlit/secrets.toml` for local testing
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_gemini_api_key_here"

# OAuth Configuration (Optional)
OAUTH_REDIRECT_URI = "https://your-app-name.streamlit.app/oauth_callback"

# Google OAuth (Optional)
GOOGLE_CLIENT_ID = "your_google_client_id"
GOOGLE_CLIENT_SECRET = "your_google_client_secret"

# GitHub OAuth (Optional)
GITHUB_CLIENT_ID = "your_github_client_id"
GITHUB_CLIENT_SECRET = "your_github_client_secret"

# Microsoft OAuth (Optional)
MICROSOFT_CLIENT_ID = "your_microsoft_client_id"
MICROSOFT_CLIENT_SECRET = "your_microsoft_client_secret"
```

#### Step 2: Deploy to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix OAuth deployment issues"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `TalkHeal.py`
   - Add secrets in the "Advanced settings"

3. **Set Environment Variables in Streamlit Cloud**:
   - Go to your app's settings
   - Add these secrets:
     ```
     GEMINI_API_KEY = your_actual_api_key
     OAUTH_REDIRECT_URI = https://your-app-name.streamlit.app/oauth_callback
     GOOGLE_CLIENT_ID = your_google_client_id (if using Google OAuth)
     GOOGLE_CLIENT_SECRET = your_google_client_secret (if using Google OAuth)
     ```

### 3. OAuth Provider Setup

#### Google OAuth Setup:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `https://your-app-name.streamlit.app/oauth_callback?provider=google`

#### GitHub OAuth Setup:
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create new OAuth App
3. Set Authorization callback URL: `https://your-app-name.streamlit.app/oauth_callback?provider=github`

### 4. Test Deployment

1. **Test without OAuth first**:
   - Deploy with just GEMINI_API_KEY
   - Test guest login and regular features

2. **Add OAuth gradually**:
   - Add one OAuth provider at a time
   - Test each provider before adding the next

### 5. Common Issues & Solutions

#### Issue: "Module not found" errors
**Solution**: Make sure all imports use relative paths and check requirements.txt

#### Issue: "Page config already set" error
**Solution**: Only call `st.set_page_config()` once in the main file

#### Issue: OAuth redirect not working
**Solution**: 
- Check redirect URI matches exactly
- Ensure HTTPS is used in production
- Verify OAuth provider settings

#### Issue: Database errors
**Solution**: SQLite files are created automatically, no manual setup needed

### 6. Minimal Working Version

If OAuth is causing issues, you can deploy without it:

1. Comment out OAuth imports in `TalkHeal.py`
2. Comment out OAuth section in `login_page.py`
3. Deploy with just basic authentication
4. Add OAuth back once basic deployment works

### 7. Debugging Tips

1. **Check Streamlit Cloud logs**:
   - Go to your app's settings
   - Click "View logs"
   - Look for specific error messages

2. **Test locally first**:
   ```bash
   streamlit run TalkHeal.py
   ```

3. **Use simple test**:
   ```bash
   python test_oauth.py
   ```

### 8. Alternative Deployment Options

If Streamlit Cloud continues to have issues:

1. **Heroku**: Use `Procfile` and `runtime.txt`
2. **Railway**: Simple deployment with environment variables
3. **Render**: Free tier available with automatic deployments
4. **DigitalOcean App Platform**: More control over environment

## Quick Start Commands

```bash
# 1. Clean up and commit
git add .
git commit -m "Fix deployment issues"
git push origin main

# 2. Test locally
streamlit run TalkHeal.py

# 3. Test OAuth setup
python test_oauth.py
```

## Support

If you're still having issues:
1. Check the Streamlit Cloud logs for specific errors
2. Try deploying without OAuth first
3. Ensure all environment variables are set correctly
4. Verify OAuth provider configurations match your redirect URIs
