"""
Test script for OAuth functionality
Run this to test OAuth configuration without starting the full app
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_oauth_config():
    """Test OAuth configuration"""
    print("🔐 Testing OAuth Configuration...")
    
    try:
        from auth.oauth_config import oauth_config
        
        print(f"Available providers: {oauth_config.get_available_providers()}")
        
        for provider in oauth_config.get_available_providers():
            print(f"\n✅ {provider.upper()} OAuth configured")
            provider_config = oauth_config.get_provider(provider)
            print(f"   Client ID: {provider_config.client_id[:10]}...")
            print(f"   Redirect URI: {provider_config.redirect_uri}")
        
        if not oauth_config.get_available_providers():
            print("❌ No OAuth providers configured")
            print("Please set up your OAuth credentials in .env file")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OAuth config: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\n🗄️ Testing Database...")
    
    try:
        from auth.auth_utils import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def test_oauth_utils():
    """Test OAuth utility functions"""
    print("\n🔧 Testing OAuth Utils...")
    
    try:
        from auth.oauth_utils import generate_state, store_oauth_state, verify_oauth_state
        
        # Test state generation
        state = generate_state()
        print(f"✅ State generated: {state[:10]}...")
        
        # Test state storage and verification
        store_oauth_state(state, "google")
        verified_provider = verify_oauth_state(state)
        
        if verified_provider == "google":
            print("✅ State storage and verification working")
        else:
            print("❌ State verification failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OAuth utils: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 TalkHeal OAuth Test Suite")
    print("=" * 40)
    
    tests = [
        test_oauth_config,
        test_database,
        test_oauth_utils
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! OAuth is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

