#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from github import Github, GithubException

def test_github_token():
    """Test GitHub token permissions and repository access"""
    
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment")
        return False
    
    print(f"✅ GITHUB_TOKEN found: {github_token[:10]}...")
    
    try:
        # Initialize GitHub client
        g = Github(github_token)
        
        # Test basic authentication
        user = g.get_user()
        print(f"✅ Authenticated as: {user.login}")
        
        # Test repository access
        repo_name = "NiloticNetwork/NiloticNetworkBlockchain"
        try:
            repo = g.get_repo(repo_name)
            print(f"✅ Repository access: {repo.full_name}")
            print(f"   - Private: {repo.private}")
            print(f"   - Issues enabled: {repo.has_issues}")
            print(f"   - Open issues: {repo.open_issues_count}")
            
            # Test issue creation permissions
            try:
                # Try to create a test issue
                test_issue = repo.create_issue(
                    title="Test Issue from Atim",
                    body="This is a test issue to verify permissions.",
                    labels=["test"]
                )
                print(f"✅ Issue creation successful: #{test_issue.number}")
                
                # Clean up - close the test issue
                test_issue.edit(state="closed")
                print("✅ Test issue closed")
                
                return True
                
            except GithubException as e:
                print(f"❌ Issue creation failed: {e}")
                print(f"   Status: {e.status}")
                print(f"   Message: {e.data.get('message', 'Unknown error')}")
                
                if e.status == 403:
                    print("\n🔧 To fix this, you need to:")
                    print("1. Go to https://github.com/settings/tokens")
                    print("2. Edit your token or create a new one")
                    print("3. Ensure these scopes are selected:")
                    print("   - repo (Full control of private repositories)")
                    print("   - public_repo (Access public repositories)")
                    print("   - issues (Create issues)")
                    print("4. Update your .env file with the new token")
                
                return False
                
        except GithubException as e:
            print(f"❌ Repository access failed: {e}")
            return False
            
    except GithubException as e:
        print(f"❌ GitHub authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing GitHub Token Permissions...")
    print("=" * 50)
    
    success = test_github_token()
    
    print("=" * 50)
    if success:
        print("✅ GitHub token is working correctly!")
    else:
        print("❌ GitHub token needs to be fixed.") 