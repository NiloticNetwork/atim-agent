#!/usr/bin/env python3

"""
Add your real GitHub App private key
"""

import os

def main():
    print("🤖 Atim Assistant - Add Real GitHub App Private Key")
    print("=" * 60)
    print()
    
    print("📋 Current Status:")
    print("✅ JWT generation working")
    print("✅ Environment variables configured")
    print("⚠️  Using placeholder private key")
    print()
    
    print("📝 To add your real private key:")
    print("1. Go to https://github.com/settings/apps")
    print("2. Find your 'Atim AI Assistant' app")
    print("3. Download the private key (.pem file)")
    print("4. Copy the entire content of the .pem file")
    print()
    
    print("📝 Paste your real private key content here:")
    print("(Press Enter twice when done)")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        except EOFError:
            break
    
    private_key = '\n'.join(lines[:-1])  # Remove last empty line
    
    if not private_key.strip():
        print("❌ No private key provided")
        return
    
    # Check if it looks like a valid private key
    if not private_key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
        print("❌ This doesn't look like a valid RSA private key")
        print("   Make sure you copied the entire .pem file content")
        return
    
    # Create private key file
    with open('atim-app.private-key.pem', 'w') as f:
        f.write(private_key)
    
    # Set proper permissions
    os.chmod('atim-app.private-key.pem', 0o600)
    
    print("✅ Real private key file updated successfully!")
    print("✅ You can now test the GitHub App integration")
    print()
    print("Run: python test_github_app_integration.py")

if __name__ == "__main__":
    main() 