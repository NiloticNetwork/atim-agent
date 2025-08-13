#!/usr/bin/env python3

"""
Atim Assistant - GitHub App Configuration Script
==============================================

This script helps configure Atim Assistant as a GitHub App.
Run this after creating your GitHub App to set up the integration.
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

def generate_webhook_secret():
    """Generate a secure webhook secret"""
    return secrets.token_urlsafe(32)

def main():
    print("🤖 Atim Assistant - GitHub App Configuration")
    print("=" * 60)
    print()
    
    print("📋 GitHub App Setup Instructions:")
    print("1. Go to: https://github.com/settings/apps")
    print("2. Click 'New GitHub App'")
    print("3. Configure the app with the details below")
    print("4. Install the app on your repository")
    print("5. Get the credentials and enter them here")
    print()
    
    print("🔧 App Configuration Details:")
    print("App name: Atim AI Assistant")
    print("Homepage URL: http://localhost:5173")
    print("App description: AI-powered blockchain development assistant for the Nilotic Network")
    print()
    
    print("📋 Required Permissions:")
    print("Repository permissions:")
    print("  - Contents: Read & write")
    print("  - Issues: Read & write")
    print("  - Pull requests: Read & write")
    print("  - Metadata: Read-only")
    print()
    print("User permissions:")
    print("  - Email addresses: Read-only")
    print()
    
    print("📋 Events to subscribe to:")
    print("  - Issues")
    print("  - Pull requests")
    print("  - Push")
    print("  - Repository")
    print()
    
    # Get user input
    print("Enter your GitHub App credentials:")
    print()
    
    app_id = input("GitHub App ID (numeric): ").strip()
    installation_id = input("Installation ID (numeric): ").strip()
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    repo = input("Target Repository (default: NiloticNetwork/NiloticNetworkBlockchain): ").strip() or "NiloticNetwork/NiloticNetworkBlockchain"
    
    # Generate webhook secret
    webhook_secret = generate_webhook_secret()
    
    if not app_id or not installation_id:
        print("❌ Please provide App ID and Installation ID")
        return False
    
    print()
    print("📝 Setting up private key file...")
    
    # Create private key file path
    private_key_path = "backend/atim-app.private-key.pem"
    
    print(f"📁 Private key should be saved as: {private_key_path}")
    print("   Download the private key from your GitHub App settings")
    print("   and save it to the path above.")
    print()
    
    # Check if private key exists
    if os.path.exists(private_key_path):
        print("✅ Private key file exists")
    else:
        print("⚠️  Private key file not found")
        print(f"   Please download and save to: {private_key_path}")
        print()
    
    print("📝 Updating configuration files...")
    
    # Update backend .env
    backend_updates = {
        'GITHUB_APP_ID': app_id,
        'GITHUB_APP_PRIVATE_KEY_PATH': private_key_path,
        'GITHUB_APP_INSTALLATION_ID': installation_id,
        'GITHUB_APP_CLIENT_ID': client_id,
        'GITHUB_APP_CLIENT_SECRET': client_secret,
        'GITHUB_WEBHOOK_SECRET': webhook_secret,
        'GITHUB_REPO': repo
    }
    
    if update_env_file('backend/.env', backend_updates):
        print("✅ Backend configuration updated")
    else:
        print("❌ Failed to update backend configuration")
        return False
    
    # Update frontend .env
    frontend_updates = {
        'GITHUB_APP_ID': app_id,
        'GITHUB_APP_INSTALLATION_ID': installation_id,
        'GITHUB_REPO': repo
    }
    
    if update_env_file('.env', frontend_updates):
        print("✅ Frontend configuration updated")
    else:
        print("❌ Failed to update frontend configuration")
        return False
    
    print()
    print("🎉 GitHub App configuration updated successfully!")
    print()
    print("📋 Next steps:")
    print("1. Ensure private key file exists: backend/atim-app.private-key.pem")
    print("2. Install required Python packages: pip install PyJWT")
    print("3. Test the configuration: python test_github_app.py")
    print("4. Restart the application: ./stop-atim.sh && ./start-atim.sh")
    print("5. Access the application: http://localhost:5173")
    print()
    print("🔧 Webhook Configuration (Optional):")
    print(f"Webhook URL: http://localhost:5070/webhook")
    print(f"Webhook Secret: {webhook_secret}")
    print("   Add this to your GitHub App webhook settings")
    print()
    print("🤖 Atim GitHub App should now be ready!")
    
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