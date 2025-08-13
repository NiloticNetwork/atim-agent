#!/usr/bin/env python3

"""
Atim Assistant - GitHub App Credentials Setup
============================================

This script helps configure the GitHub App credentials for Atim Assistant.
Run this after creating your GitHub App to set up the integration properly.
"""

import os
import re
import secrets
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

def create_private_key_file(private_key_content, file_path):
    """Create the private key file"""
    try:
        with open(file_path, 'w') as f:
            f.write(private_key_content)
        
        # Set proper permissions (read-only for owner)
        os.chmod(file_path, 0o600)
        print(f"✅ Created private key file: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create private key file: {e}")
        return False

def main():
    print("🤖 Atim Assistant - GitHub App Credentials Setup")
    print("=" * 60)
    print()
    
    print("📋 Current GitHub App Configuration:")
    print("App ID: 1741466")
    print("Installation ID: Iv23liISYyXEKNDrU0aR")
    print("Client ID: Iv23liISYyXEKNDrU0aR")
    print("Target Repository: NiloticNetwork/NiloticNetworkBlockchain")
    print()
    
    print("🔧 To complete the setup, you need:")
    print("1. The GitHub App private key (.pem file content)")
    print("2. Update the environment variables")
    print()
    
    # Get private key content
    print("📝 Enter your GitHub App private key content:")
    print("(Paste the entire .pem file content, including BEGIN and END lines)")
    print("Press Enter twice when done:")
    
    private_key_lines = []
    while True:
        line = input()
        if line == "" and private_key_lines and private_key_lines[-1] == "":
            break
        private_key_lines.append(line)
    
    private_key_content = '\n'.join(private_key_lines[:-1])  # Remove the last empty line
    
    if not private_key_content.strip():
        print("❌ No private key content provided")
        return
    
    # Create private key file
    private_key_path = "atim-app.private-key.pem"
    if not create_private_key_file(private_key_content, private_key_path):
        return
    
    # Update backend .env file
    backend_env_updates = {
        'GITHUB_APP_ID': '1741466',
        'GITHUB_APP_PRIVATE_KEY_PATH': private_key_path,
        'GITHUB_APP_INSTALLATION_ID': 'Iv23liISYyXEKNDrU0aR',
        'GITHUB_APP_CLIENT_ID': 'Iv23liISYyXEKNDrU0aR',
        'GITHUB_APP_CLIENT_SECRET': '0ad55f0276c49696924c6b0ead36737d5b864206',
        'GITHUB_REPO': 'NiloticNetwork/NiloticNetworkBlockchain',
        # Clear the old token-based configuration
        'ATIM_GITHUB_TOKEN': '',
        'GITHUB_TOKEN': ''
    }
    
    if update_env_file('.env', backend_env_updates):
        print("✅ Backend configuration updated")
    
    # Update frontend .env file
    frontend_env_path = '../.env'
    frontend_env_updates = {
        'GITHUB_APP_ID': '1741466',
        'GITHUB_APP_INSTALLATION_ID': 'Iv23liISYyXEKNDrU0aR',
        'GITHUB_REPO': 'NiloticNetwork/NiloticNetworkBlockchain'
    }
    
    if update_env_file(frontend_env_path, frontend_env_updates):
        print("✅ Frontend configuration updated")
    
    print()
    print("🎉 GitHub App credentials configured successfully!")
    print()
    print("📋 Next steps:")
    print("1. Test the GitHub App integration:")
    print("   python test_github_app_integration.py")
    print("2. Restart the ATIM assistant:")
    print("   cd .. && ./stop-atim.sh && ./start-atim.sh")
    print("3. Try creating an issue from the web interface")
    print()

if __name__ == "__main__":
    main() 