#!/usr/bin/env python3

"""
Atim Assistant - GitHub App Test Script
======================================

This script tests the GitHub App integration for Atim Assistant.
Run this after configuring your GitHub App to verify everything is working.
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

def test_environment_variables():
    """Test if GitHub App environment variables are properly configured"""
    print("🔍 Testing GitHub App Environment Variables...")
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
    
    # Check GitHub App variables
    app_vars = [
        'GITHUB_APP_ID',
        'GITHUB_APP_PRIVATE_KEY_PATH',
        'GITHUB_APP_INSTALLATION_ID',
        'GITHUB_REPO'
    ]
    
    for var in app_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} is set: {value}")
        else:
            print(f"❌ {var} is not set")
    
    # Check private key file
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    if private_key_path and os.path.exists(private_key_path):
        print(f"✅ Private key file exists: {private_key_path}")
    else:
        print(f"❌ Private key file missing: {private_key_path}")
    
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

def test_github_app_integration():
    """Test GitHub App integration using the app script"""
    print("🤖 Testing GitHub App Integration...")
    print("=" * 50)
    
    try:
        # Import and run the app test
        sys.path.append('backend')
        from atim_github_app import test_atim_app
        test_atim_app()
        return True
    except ImportError as e:
        print(f"❌ Could not import atim_github_app: {e}")
        print("   Make sure the file exists and PyJWT is installed: pip install PyJWT")
        return False
    except Exception as e:
        print(f"❌ Error testing GitHub App integration: {e}")
        return False

def test_repository_access():
    """Test if we can access the target repository via GitHub App"""
    print("📁 Testing Repository Access via GitHub App...")
    print("=" * 50)
    
    try:
        from github import Github
        from github.Auth import AppAuth
        import jwt
        import time
        import requests
        load_dotenv()
        
        app_id = os.environ.get('GITHUB_APP_ID')
        private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
        installation_id = os.environ.get('GITHUB_APP_INSTALLATION_ID')
        repo_name = os.environ.get('GITHUB_REPO', 'NiloticNetwork/NiloticNetworkBlockchain')
        
        if not all([app_id, private_key_path, installation_id]):
            print("❌ GitHub App credentials not fully configured")
            return False
        
        # Generate JWT
        with open(private_key_path, 'r') as f:
            private_key = f.read()
        
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,  # 10 minutes
            'iss': int(app_id)
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
        
        # Get installation token
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.post(
            f'https://api.github.com/app/installations/{installation_id}/access_tokens',
            headers=headers
        )
        
        if response.status_code != 201:
            print(f"❌ Failed to get installation token: {response.text}")
            return False
        
        access_token = response.json()['token']
        
        # Initialize GitHub client
        g = Github(auth=AppAuth(app_id, access_token))
        repo = g.get_repo(repo_name)
        
        print(f"✅ Successfully accessed repository: {repo.full_name}")
        print(f"   Description: {repo.description or 'No description'}")
        print(f"   Language: {repo.language or 'Not specified'}")
        print(f"   Stars: {repo.stargazers_count}")
        print(f"   Forks: {repo.forks_count}")
        print(f"   Open Issues: {repo.open_issues_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing repository via GitHub App: {e}")
        return False

def test_required_packages():
    """Test if required packages are installed"""
    print("📦 Testing Required Packages...")
    print("=" * 50)
    
    required_packages = [
        ('PyJWT', 'jwt'),
        ('PyGithub', 'github'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is not installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print()
    return True

def main():
    """Run all tests"""
    print("🤖 Atim Assistant - GitHub App Test")
    print("=" * 60)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Required Packages", test_required_packages),
        ("Environment Variables", test_environment_variables),
        ("Backend API", test_backend_api),
        ("Frontend", test_frontend),
        ("GitHub App Integration", test_github_app_integration),
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
        print("\n🎉 All tests passed! Atim GitHub App is ready to use.")
        print("   Access the application at: http://localhost:5173")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the configuration.")
        print("   Refer to GITHUB_APP_SETUP.md for setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 