#!/usr/bin/env python3

import os
import time
import jwt
import requests
from dotenv import load_dotenv

def test_repository_access():
    """Test repository access"""
    print("🤖 Testing Repository Access")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    app_id = os.environ.get('GITHUB_APP_ID')
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    repo_name = os.environ.get('GITHUB_REPO')
    
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
        
        # Test repository access
        response = requests.get(
            f'https://api.github.com/repos/{repo_name}',
            headers=headers
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ Repository found!")
            print(f"   Name: {repo_data.get('full_name')}")
            print(f"   Description: {repo_data.get('description', 'No description')}")
            print(f"   Private: {repo_data.get('private', False)}")
            print(f"   Default Branch: {repo_data.get('default_branch')}")
            
            # Test issue creation permissions
            print(f"\n🔐 Testing Issue Creation Permissions:")
            
            # Check if we can create issues
            response = requests.get(
                f'https://api.github.com/repos/{repo_name}/issues',
                headers=headers,
                params={'per_page': 1}
            )
            
            if response.status_code == 200:
                print(f"✅ Can access issues")
                
                # Try to create a test issue
                test_data = {
                    "title": "Test Issue from Atim AI Assistant",
                    "body": "This is a test issue to verify GitHub App permissions.",
                    "labels": ["test", "automation"]
                }
                
                create_response = requests.post(
                    f'https://api.github.com/repos/{repo_name}/issues',
                    headers=headers,
                    json=test_data
                )
                
                print(f"📝 Issue Creation Test: {create_response.status_code}")
                
                if create_response.status_code == 201:
                    issue_data = create_response.json()
                    print(f"✅ Issue created successfully: #{issue_data['number']}")
                    
                    # Clean up - close the test issue
                    close_response = requests.patch(
                        f'https://api.github.com/repos/{repo_name}/issues/{issue_data["number"]}',
                        headers=headers,
                        json={"state": "closed"}
                    )
                    
                    if close_response.status_code == 200:
                        print(f"✅ Test issue closed successfully")
                    else:
                        print(f"⚠️  Could not close test issue: {close_response.status_code}")
                        
                else:
                    print(f"❌ Failed to create issue: {create_response.status_code}")
                    print(f"   Response: {create_response.text}")
            else:
                print(f"❌ Cannot access issues: {response.status_code}")
                
        elif response.status_code == 404:
            print(f"❌ Repository not found: {repo_name}")
            print(f"   This repository may not exist or the GitHub App may not have access")
        else:
            print(f"❌ Error accessing repository: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_repository_access()

