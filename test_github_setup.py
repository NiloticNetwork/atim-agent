#!/usr/bin/env python3

"""
Atim Assistant - GitHub Integration Test Script
==============================================

This script tests the GitHub integration setup for Atim Assistant.
Run this after configuring your GitHub tokens to verify everything is working.
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

def test_environment_variables():
    """Test if environment variables are properly configured"""
    print("🔍 Testing Environment Variables...")
    print("=" * 50)
    
    load_dotenv()
    
    # Check backend environment
    backend_env_path = "backend/.env"
    if os.path.exists(backend_env_path):
        print(f"✅ Backend .env file exists: {backend_env_path}")
    else:
        print(f"❌ Backend .env file missing: {backend_env_path}")
        return False
    
    # Check frontend environment
    frontend_env_path = ".env"
    if os.path.exists(frontend_env_path):
        print(f"✅ Frontend .env file exists: {frontend_env_path}")
    else:
        print(f"❌ Frontend .env file missing: {frontend_env_path}")
        return False
    
    # Check GitHub tokens
    atim_token = os.environ.get('ATIM_GITHUB_TOKEN')
    user_token = os.environ.get('GITHUB_TOKEN')
    
    if atim_token and atim_token != 'your_atim_github_app_token_here':
        print("✅ ATIM_GITHUB_TOKEN is configured")
    else:
        print("❌ ATIM_GITHUB_TOKEN not configured or using placeholder")
    
    if user_token and user_token != 'your_github_personal_access_token_here':
        print("✅ GITHUB_TOKEN is configured")
    else:
        print("❌ GITHUB_TOKEN not configured or using placeholder")
    
    # Check other required variables
    required_vars = ['ATIM_GITHUB_USERNAME', 'GITHUB_REPO']
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} is set: {value}")
        else:
            print(f"❌ {var} is not set")
    
    print()
    return True

def test_backend_api():
    """Test if the backend API is running and accessible"""
    print("🌐 Testing Backend API...")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5070/api/kanban", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running and accessible")
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                print(f"✅ API returned {len(data['data'])} kanban items")
            else:
                print("⚠️  API returned empty data")
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend API is not running or not accessible")
        print("   Start the backend with: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Error testing backend API: {e}")
        return False
    
    print()
    return True

def test_frontend():
    """Test if the frontend is running and accessible"""
    print("🎨 Testing Frontend...")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            if "Atim Assistant" in response.text:
                print("✅ Frontend contains Atim Assistant content")
            else:
                print("⚠️  Frontend content not as expected")
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running or not accessible")
        print("   Start the frontend with: npm run dev")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False
    
    print()
    return True

def test_github_integration():
    """Test GitHub integration using the bot script"""
    print("🤖 Testing GitHub Integration...")
    print("=" * 50)
    
    try:
        # Import and run the bot test
        sys.path.append('backend')
        from atim_github_bot import test_atim_bot
        test_atim_bot()
        return True
    except ImportError as e:
        print(f"❌ Could not import atim_github_bot: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing GitHub integration: {e}")
        return False

def test_repository_access():
    """Test if we can access the target repository"""
    print("📁 Testing Repository Access...")
    print("=" * 50)
    
    try:
        from github import Github
        load_dotenv()
        
        token = os.environ.get('ATIM_GITHUB_TOKEN') or os.environ.get('GITHUB_TOKEN')
        repo_name = os.environ.get('GITHUB_REPO', 'NiloticNetwork/NiloticNetworkBlockchain')
        
        if not token or token in ['your_atim_github_app_token_here', 'your_github_personal_access_token_here']:
            print("❌ GitHub token not configured")
            return False
        
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        print(f"✅ Successfully accessed repository: {repo.full_name}")
        print(f"   Description: {repo.description or 'No description'}")
        print(f"   Language: {repo.language or 'Not specified'}")
        print(f"   Stars: {repo.stargazers_count}")
        print(f"   Forks: {repo.forks_count}")
        print(f"   Open Issues: {repo.open_issues_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing repository: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Atim Assistant - GitHub Integration Test")
    print("=" * 60)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Backend API", test_backend_api),
        ("Frontend", test_frontend),
        ("GitHub Integration", test_github_integration),
        ("Repository Access", test_repository_access)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Atim Assistant is ready to use.")
        print("   Access the application at: http://localhost:5173")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the configuration.")
        print("   Refer to GITHUB_SETUP_GUIDE.md for setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 