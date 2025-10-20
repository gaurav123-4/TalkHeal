"""
OAuth Configuration for TalkHeal
Supports Google, GitHub, and Microsoft OAuth providers
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class OAuthProvider:
    """OAuth provider configuration"""
    client_id: str
    client_secret: str
    auth_url: str
    token_url: str
    user_info_url: str
    scope: str
    redirect_uri: str

class OAuthConfig:
    """OAuth configuration manager"""
    
    def __init__(self):
        self.base_redirect_uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8501/oauth_callback")
        self.providers = self._load_providers()
    
    def _load_providers(self) -> Dict[str, OAuthProvider]:
        """Load OAuth provider configurations from environment variables"""
        providers = {}
        
        # Google OAuth
        if os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"):
            providers["google"] = OAuthProvider(
                client_id=os.getenv("GOOGLE_CLIENT_ID"),
                client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
                auth_url="https://accounts.google.com/o/oauth2/v2/auth",
                token_url="https://oauth2.googleapis.com/token",
                user_info_url="https://www.googleapis.com/oauth2/v2/userinfo",
                scope="openid email profile",
                redirect_uri=f"{self.base_redirect_uri}?provider=google"
            )
        
        # GitHub OAuth
        if os.getenv("GITHUB_CLIENT_ID") and os.getenv("GITHUB_CLIENT_SECRET"):
            providers["github"] = OAuthProvider(
                client_id=os.getenv("GITHUB_CLIENT_ID"),
                client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
                auth_url="https://github.com/login/oauth/authorize",
                token_url="https://github.com/login/oauth/access_token",
                user_info_url="https://api.github.com/user",
                scope="user:email",
                redirect_uri=f"{self.base_redirect_uri}?provider=github"
            )
        
        # Microsoft OAuth
        if os.getenv("MICROSOFT_CLIENT_ID") and os.getenv("MICROSOFT_CLIENT_SECRET"):
            providers["microsoft"] = OAuthProvider(
                client_id=os.getenv("MICROSOFT_CLIENT_ID"),
                client_secret=os.getenv("MICROSOFT_CLIENT_SECRET"),
                auth_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
                user_info_url="https://graph.microsoft.com/v1.0/me",
                scope="openid email profile",
                redirect_uri=f"{self.base_redirect_uri}?provider=microsoft"
            )
        
        return providers
    
    def get_provider(self, provider_name: str) -> OAuthProvider:
        """Get OAuth provider configuration"""
        if provider_name not in self.providers:
            raise ValueError(f"OAuth provider '{provider_name}' not configured")
        return self.providers[provider_name]
    
    def get_auth_url(self, provider_name: str, state: str = None) -> str:
        """Generate OAuth authorization URL"""
        provider = self.get_provider(provider_name)
        
        params = {
            "client_id": provider.client_id,
            "redirect_uri": provider.redirect_uri,
            "scope": provider.scope,
            "response_type": "code",
            "access_type": "offline" if provider_name == "google" else None,
            "prompt": "consent" if provider_name == "google" else None
        }
        
        if state:
            params["state"] = state
        
        # Build query string
        query_params = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        return f"{provider.auth_url}?{query_params}"
    
    def is_provider_available(self, provider_name: str) -> bool:
        """Check if OAuth provider is configured"""
        return provider_name in self.providers
    
    def get_available_providers(self) -> list:
        """Get list of available OAuth providers"""
        return list(self.providers.keys())

# Global OAuth configuration instance
oauth_config = OAuthConfig()

