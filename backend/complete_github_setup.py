#!/usr/bin/env python3

"""
Simple script to complete GitHub App setup
"""

import os
import sys

def main():
    print("🤖 Atim Assistant - GitHub App Setup")
    print("=" * 40)
    print()
    
    print("📋 To complete the setup, you need:")
    print("1. Go to https://github.com/settings/apps")
    print("2. Find your 'Atim AI Assistant' app")
    print("3. Download the private key (.pem file)")
    print("4. Copy the entire content of the .pem file")
    print()
    
    print("📝 Paste your private key content here:")
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
    
    # Create private key file
    with open('atim-app.private-key.pem', 'w') as f:
        f.write(private_key)
    
    # Set proper permissions
    os.chmod('atim-app.private-key.pem', 0o600)
    
    print("✅ Private key file created successfully!")
    print("✅ You can now test the GitHub App integration")
    print()
    print("Run: python test_github_app_integration.py")

if __name__ == "__main__":
    main() 