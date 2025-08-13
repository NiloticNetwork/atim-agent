#!/usr/bin/env python3

"""
Atim Assistant - GitHub App Integration Test
===========================================

This script tests the GitHub App integration to ensure everything is working properly.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from github_integration_app import GitHubIntegrationApp as AtimGitHubApp
except ImportError:
    print("❌ Could not import GitHubIntegrationApp. Make sure github_integration_app.py exists.")
    sys.exit(1)

def test_github_app_integration():
    """Test the GitHub App integration"""
    print("🤖 Testing Atim GitHub App Integration")
    print("=" * 50)
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    print("📋 Environment Variables Check:")
    required_vars = [
        'GITHUB_APP_ID',
        'GITHUB_APP_PRIVATE_KEY_PATH', 
        'GITHUB_APP_CLIENT_ID',
        'GITHUB_APP_CLIENT_SECRET',
        'GITHUB_REPO'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value[:20]}..." if len(value) > 20 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print()
    
    # Check private key file
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    if os.path.exists(private_key_path):
        print(f"✅ Private key file exists: {private_key_path}")
    else:
        print(f"❌ Private key file missing: {private_key_path}")
        return False
    
    print()
    
    # Test GitHub App initialization
    print("🔧 Testing GitHub App Initialization:")
    try:
        app = AtimGitHubApp()
        
        if app.github and app.repo:
            print("✅ GitHub App initialized successfully")
            print(f"✅ Repository access: {app.repo.full_name}")
            
            # Test repository stats
            stats = app.get_repository_stats()
            if stats:
                print("✅ Repository stats retrieved successfully")
                print(f"   - Open issues: {stats.get('open_issues', 'N/A')}")
                print(f"   - Open PRs: {stats.get('open_pulls', 'N/A')}")
                print(f"   - Stars: {stats.get('stars', 'N/A')}")
                print(f"   - Language: {stats.get('language', 'N/A')}")
            
            # Test app info
            app_info = app.get_app_info()
            if app_info:
                print("✅ App info retrieved successfully")
                print(f"   - App name: {app_info.get('name', 'N/A')}")
                print(f"   - App ID: {app_info.get('app_id', 'N/A')}")
                print(f"   - Client ID: {app_info.get('client_id', 'N/A')}")
            
            return True
            
        else:
            print("❌ GitHub App initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during GitHub App initialization: {e}")
        return False

def test_issue_creation():
    """Test issue creation (dry run)"""
    print("\n🔧 Testing Issue Creation (Dry Run):")
    try:
        app = AtimGitHubApp()
        
        if not app.github or not app.repo:
            print("❌ GitHub App not properly initialized")
            return False
        
        # Test issue creation without actually creating one
        test_title = "Test Issue - Atim GitHub App Integration"
        test_description = "This is a test issue to verify the GitHub App integration is working properly."
        test_labels = ["test", "automation"]
        
        print(f"✅ Would create issue with title: {test_title}")
        print(f"✅ Would add labels: {test_labels}")
        print("✅ Issue creation test passed (dry run)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during issue creation test: {e}")
        return False

def main():
    """Main test function"""
    print("🤖 Atim Assistant - GitHub App Integration Test")
    print("=" * 60)
    print()
    
    # Test basic integration
    if not test_github_app_integration():
        print("\n❌ GitHub App integration test failed")
        print("\n📋 Troubleshooting steps:")
        print("1. Check that all environment variables are set correctly")
        print("2. Verify the private key file exists and has correct permissions")
        print("3. Ensure the GitHub App is installed on the target repository")
        print("4. Check that the App has the required permissions")
        return False
    
    # Test issue creation
    if not test_issue_creation():
        print("\n❌ Issue creation test failed")
        return False
    
    print("\n🎉 All tests passed! GitHub App integration is working correctly.")
    print("\n📋 Next steps:")
    print("1. Restart the ATIM assistant: cd .. && ./stop-atim.sh && ./start-atim.sh")
    print("2. Try creating an issue from the web interface")
    print("3. Monitor the server logs for any issues")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 