#!/usr/bin/env python3

import os
import time
import jwt
import requests
from dotenv import load_dotenv

def check_app_permissions():
    """Check GitHub App permissions and installation"""
    print("🤖 Checking GitHub App Permissions")
    print("=" * 45)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    app_id = os.environ.get('GITHUB_APP_ID')
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    installation_id = os.environ.get('GITHUB_APP_INSTALLATION_ID')
    repo_name = os.environ.get('GITHUB_REPO')
    
    print(f"📋 App ID: {app_id}")
    print(f"📋 Installation ID: {installation_id}")
    print(f"📋 Repository: {repo_name}")
    
    # Generate JWT
    try:
        with open(private_key_path, 'r') as f:
            private_key = f.read()
        
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,
            'iss': int(app_id)
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Check app information
        print(f"\n🔍 Checking App Information:")
        response = requests.get('https://api.github.com/app', headers=headers)
        
        if response.status_code == 200:
            app_data = response.json()
            print(f"✅ App found: {app_data.get('name')}")
            print(f"   Description: {app_data.get('description', 'No description')}")
            print(f"   Permissions: {app_data.get('permissions', {})}")
        else:
            print(f"❌ Failed to get app info: {response.status_code}")
            return
        
        # Check installation
        if installation_id:
            print(f"\n🔍 Checking Installation:")
            response = requests.get(
                f'https://api.github.com/app/installations/{installation_id}',
                headers=headers
            )
            
            if response.status_code == 200:
                install_data = response.json()
                print(f"✅ Installation found")
                print(f"   Account: {install_data.get('account', {}).get('login', 'Unknown')}")
                print(f"   Permissions: {install_data.get('permissions', {})}")
                print(f"   Repository Selection: {install_data.get('repository_selection', 'Unknown')}")
                
                # Get installation access token
                print(f"\n🔑 Getting Installation Access Token:")
                token_response = requests.post(
                    f'https://api.github.com/app/installations/{installation_id}/access_tokens',
                    headers=headers
                )
                
                if token_response.status_code == 201:
                    token_data = token_response.json()
                    print(f"✅ Installation token generated")
                    print(f"   Token expires: {token_data.get('expires_at')}")
                    
                    # Test repository access with installation token
                    install_headers = {
                        'Authorization': f'Bearer {token_data["token"]}',
                        'Accept': 'application/vnd.github.v3+json'
                    }
                    
                    print(f"\n🔍 Testing Repository Access with Installation Token:")
                    
                    # Test repository access
                    repo_response = requests.get(
                        f'https://api.github.com/repos/{repo_name}',
                        headers=install_headers
                    )
                    
                    if repo_response.status_code == 200:
                        print(f"✅ Repository accessible with installation token")
                        
                        # Test issue creation
                        test_data = {
                            "title": "Test Issue from Atim AI Assistant (Installation Token)",
                            "body": "This is a test issue using installation token.",
                            "labels": ["test", "automation"]
                        }
                        
                        issue_response = requests.post(
                            f'https://api.github.com/repos/{repo_name}/issues',
                            headers=install_headers,
                            json=test_data
                        )
                        
                        print(f"📝 Issue Creation Test: {issue_response.status_code}")
                        
                        if issue_response.status_code == 201:
                            issue_data = issue_response.json()
                            print(f"✅ Issue created successfully: #{issue_data['number']}")
                            
                            # Clean up
                            close_response = requests.patch(
                                f'https://api.github.com/repos/{repo_name}/issues/{issue_data["number"]}',
                                headers=install_headers,
                                json={"state": "closed"}
                            )
                            
                            if close_response.status_code == 200:
                                print(f"✅ Test issue closed successfully")
                            else:
                                print(f"⚠️  Could not close test issue: {close_response.status_code}")
                                
                        else:
                            print(f"❌ Failed to create issue: {issue_response.status_code}")
                            print(f"   Response: {issue_response.text}")
                    else:
                        print(f"❌ Repository not accessible: {repo_response.status_code}")
                        
                else:
                    print(f"❌ Failed to get installation token: {token_response.status_code}")
                    print(f"   Response: {token_response.text}")
            else:
                print(f"❌ Installation not found: {response.status_code}")
                print(f"   Response: {response.text}")
        else:
            print(f"⚠️  No installation ID configured")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_app_permissions()

