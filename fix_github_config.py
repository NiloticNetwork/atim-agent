#!/usr/bin/env python3

"""
Atim Assistant - GitHub Configuration Fix Script
==============================================

This script helps fix the GitHub configuration by updating environment variables.
Run this after you have your GitHub tokens ready.
"""

import os
import re
from datetime import datetime

def update_env_file(file_path, updates):
    """Update environment file with new values"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read current content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Apply updates
    for key, value in updates.items():
        # Pattern to match the variable assignment
        pattern = rf'^{key}=.*$'
        replacement = f'{key}={value}'
        
        if re.search(pattern, content, re.MULTILINE):
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        else:
            # Add the variable if it doesn't exist
            content += f'\n{replacement}'
    
    # Write updated content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated {file_path}")
    return True

def main():
    print("🔧 Atim Assistant - GitHub Configuration Fix")
    print("=" * 50)
    print()
    
    print("📋 Current Issues Found:")
    print("❌ ATIM_GITHUB_TOKEN not configured")
    print("❌ ATIM_GITHUB_USERNAME not set")
    print("❌ GITHUB_REPO not set")
    print()
    
    print("🔑 To fix these issues, you need to:")
    print("1. Generate GitHub tokens (see GITHUB_SETUP_GUIDE.md)")
    print("2. Update the environment files with your tokens")
    print()
    
    # Get user input
    print("Enter your GitHub configuration:")
    print()
    
    atim_token = input("Atim's GitHub Token (starts with ghp_): ").strip()
    user_token = input("Your Personal GitHub Token (starts with ghp_): ").strip()
    username = input("Atim's GitHub Username (default: atim-ai-assistant): ").strip() or "atim-ai-assistant"
    repo = input("Target Repository (default: NiloticNetwork/NiloticNetworkBlockchain): ").strip() or "NiloticNetwork/NiloticNetworkBlockchain"
    
    if not atim_token or atim_token == "your_atim_github_app_token_here":
        print("❌ Please provide a valid Atim GitHub token")
        return False
    
    if not user_token or user_token == "your_github_personal_access_token_here":
        print("❌ Please provide a valid personal GitHub token")
        return False
    
    print()
    print("📝 Updating configuration files...")
    
    # Update backend .env
    backend_updates = {
        'ATIM_GITHUB_TOKEN': atim_token,
        'ATIM_GITHUB_USERNAME': username,
        'GITHUB_TOKEN': user_token,
        'GITHUB_REPO': repo
    }
    
    if update_env_file('backend/.env', backend_updates):
        print("✅ Backend configuration updated")
    else:
        print("❌ Failed to update backend configuration")
        return False
    
    # Update frontend .env
    frontend_updates = {
        'ATIM_GITHUB_TOKEN': atim_token,
        'ATIM_GITHUB_USERNAME': username,
        'ATIM_TARGET_REPO': repo
    }
    
    if update_env_file('.env', frontend_updates):
        print("✅ Frontend configuration updated")
    else:
        print("❌ Failed to update frontend configuration")
        return False
    
    print()
    print("🎉 Configuration updated successfully!")
    print()
    print("📋 Next steps:")
    print("1. Test the configuration: python test_github_setup.py")
    print("2. Restart the application: ./stop-atim.sh && ./start-atim.sh")
    print("3. Access the application: http://localhost:5173")
    print()
    print("🤖 Atim Assistant should now be ready to work with GitHub!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1) 