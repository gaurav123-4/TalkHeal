#!/usr/bin/env python3
"""
TalkHeal Application Launcher
This script provides an easy way to start TalkHeal with proper setup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Creating sample .env file...")
        
        sample_env = """# OAuth Configuration (Optional)
OAUTH_REDIRECT_URI=http://localhost:8501/oauth_callback

# Google OAuth (Get from Google Cloud Console)
# GOOGLE_CLIENT_ID=your_google_client_id_here
# GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# GitHub OAuth (Get from GitHub Developer Settings)
# GITHUB_CLIENT_ID=your_github_client_id_here
# GITHUB_CLIENT_SECRET=your_github_client_secret_here

# Microsoft OAuth (Get from Azure App Registration)
# MICROSOFT_CLIENT_ID=your_microsoft_client_id_here
# MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret_here
"""
        
        with open(".env", "w") as f:
            f.write(sample_env)
        
        print("✅ Sample .env file created")
        print("Please edit .env file with your OAuth credentials if needed")
        return True

def check_streamlit_config():
    """Check if Streamlit config exists"""
    config_file = Path(".streamlit/config.toml")
    if config_file.exists():
        print("✅ Streamlit config found")
        return True
    else:
        print("⚠️  Streamlit config not found")
        print("Creating basic Streamlit config...")
        
        # Create .streamlit directory if it doesn't exist
        os.makedirs(".streamlit", exist_ok=True)
        
        config_content = """[server]
port = 8501
headless = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#ff69b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
        
        with open(config_file, "w") as f:
            f.write(config_content)
        
        print("✅ Streamlit config created")
        return True

def main():
    """Main launcher function"""
    print("🚀 TalkHeal Application Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("TalkHeal.py").exists():
        print("❌ TalkHeal.py not found in current directory")
        print("Please run this script from the TalkHeal directory")
        sys.exit(1)
    
    # Run checks
    checks = [
        check_requirements,
        check_env_file,
        check_streamlit_config
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    if not all_passed:
        print("\n❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("🚀 Starting TalkHeal...")
    print("=" * 40)
    
    # Start the application
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "TalkHeal.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 TalkHeal stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting TalkHeal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

