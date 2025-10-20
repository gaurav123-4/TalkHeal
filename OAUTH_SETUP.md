# OAuth Setup Guide for TalkHeal

This guide will help you set up OAuth authentication for TalkHeal using Google, GitHub, and Microsoft providers.

## Prerequisites

1. Python 3.8+
2. Streamlit
3. OAuth provider accounts (Google, GitHub, Microsoft)

## Environment Variables

Create a `.env` file in the TalkHeal directory with the following variables:

```env
# OAuth Configuration
OAUTH_REDIRECT_URI=http://localhost:8501/oauth_callback

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here

# Microsoft OAuth
MICROSOFT_CLIENT_ID=your_microsoft_client_id_here
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret_here
```

## OAuth Provider Setup

### 1. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:8501/oauth_callback?provider=google` (for development)
   - `https://yourdomain.com/oauth_callback?provider=google` (for production)
7. Copy the Client ID and Client Secret to your `.env` file

### 2. GitHub OAuth Setup

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the application details:
   - Application name: TalkHeal
   - Homepage URL: `http://localhost:8501` (or your domain)
   - Authorization callback URL: `http://localhost:8501/oauth_callback?provider=github`
4. Click "Register application"
5. Copy the Client ID and Client Secret to your `.env` file

### 3. Microsoft OAuth Setup

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" → "App registrations"
3. Click "New registration"
4. Fill in the details:
   - Name: TalkHeal
   - Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
   - Redirect URI: Web - `http://localhost:8501/oauth_callback?provider=microsoft`
5. Click "Register"
6. Go to "Certificates & secrets" → "New client secret"
7. Copy the Application (client) ID and Client Secret to your `.env` file

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables in `.env` file

3. Run the application:
```bash
streamlit run TalkHeal.py
```

## Features

- **Google OAuth**: Sign in with Google account
- **GitHub OAuth**: Sign in with GitHub account  
- **Microsoft OAuth**: Sign in with Microsoft account
- **Guest Login**: Continue without authentication
- **Traditional Login**: Email/password authentication

## Security Features

- Secure state parameter validation
- CSRF protection
- Token expiration handling
- User data normalization across providers
- Secure session management

## Troubleshooting

### Common Issues

1. **"OAuth provider not configured"**: Check your `.env` file and ensure all required variables are set
2. **"Invalid redirect URI"**: Ensure your redirect URI matches exactly what you configured with the OAuth provider
3. **"Access denied"**: Check if the OAuth app is properly configured and the user has granted permissions

### Development vs Production

- **Development**: Use `http://localhost:8501` as your base URL
- **Production**: Update all redirect URIs to use your production domain
- **HTTPS**: OAuth providers require HTTPS in production

## Customization

You can customize the OAuth providers by modifying `auth/oauth_config.py`:

- Add new providers
- Modify scopes
- Change redirect URIs
- Update user data mapping

## Support

For issues related to OAuth setup, please check:
1. OAuth provider documentation
2. Streamlit OAuth documentation
3. Application logs for detailed error messages

