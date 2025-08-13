#!/usr/bin/env python3

import os
import time
import jwt
import requests
from dotenv import load_dotenv

def test_github_app_setup():
    """Test GitHub App setup step by step"""
    print("🤖 Testing GitHub App Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    app_id = os.environ.get('GITHUB_APP_ID')
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    client_id = os.environ.get('GITHUB_APP_CLIENT_ID')
    client_secret = os.environ.get('GITHUB_APP_CLIENT_SECRET')
    repo_name = os.environ.get('GITHUB_REPO')
    
    print(f"📋 Configuration:")
    print(f"   App ID: {app_id}")
    print(f"   Private Key Path: {private_key_path}")
    print(f"   Client ID: {client_id}")
    print(f"   Repository: {repo_name}")
    
    # Check if private key file exists
    if not os.path.exists(private_key_path):
        print(f"❌ Private key file not found: {private_key_path}")
        return False
    
    print(f"✅ Private key file exists: {private_key_path}")
    
    # Read private key
    try:
        with open(private_key_path, 'r') as f:
            private_key = f.read()
        print(f"✅ Private key loaded successfully")
    except Exception as e:
        print(f"❌ Failed to read private key: {e}")
        return False
    
    # Generate JWT
    try:
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,  # 10 minutes
            'iss': int(app_id)
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
        print(f"✅ JWT token generated successfully")
        print(f"   Token length: {len(jwt_token)} characters")
        
    except Exception as e:
        print(f"❌ Failed to generate JWT: {e}")
        return False
    
    # Test GitHub API
    try:
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Test app endpoint
        response = requests.get(
            f'https://api.github.com/app',
            headers=headers
        )
        
        if response.status_code == 200:
            app_data = response.json()
            print(f"✅ GitHub App API test successful")
            print(f"   App name: {app_data.get('name', 'Unknown')}")
            print(f"   App description: {app_data.get('description', 'No description')}")
        else:
            print(f"❌ GitHub App API test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test GitHub API: {e}")
        return False
    
    print(f"\n🎉 GitHub App setup test completed successfully!")
    return True

if __name__ == "__main__":
    test_github_app_setup()

