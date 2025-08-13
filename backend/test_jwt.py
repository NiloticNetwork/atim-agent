#!/usr/bin/env python3

"""
Test JWT generation for GitHub App
"""

import os
import time
import jwt
from dotenv import load_dotenv

def test_jwt_generation():
    """Test JWT generation"""
    load_dotenv()
    
    app_id = os.environ.get('GITHUB_APP_ID')
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    
    print(f"App ID: {app_id}")
    print(f"Private key path: {private_key_path}")
    
    if not os.path.exists(private_key_path):
        print("❌ Private key file not found")
        return False
    
    try:
        with open(private_key_path, 'r') as f:
            private_key = f.read()
        
        print(f"Private key length: {len(private_key)} characters")
        print(f"Private key starts with: {private_key[:50]}...")
        
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,  # 10 minutes
            'iss': int(app_id)
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
        print(f"✅ JWT token generated successfully")
        print(f"JWT token length: {len(jwt_token)} characters")
        print(f"JWT token starts with: {jwt_token[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ JWT generation failed: {e}")
        return False

if __name__ == "__main__":
    test_jwt_generation() 