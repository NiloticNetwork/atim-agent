#!/usr/bin/env python3

"""
Create a temporary private key for testing
"""

import os

def create_temp_key():
    """Create a temporary private key for testing"""
    
    # This is a sample private key format - you'll need to replace with your real one
    temp_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
[This is a placeholder - you need to replace with your actual GitHub App private key]
-----END RSA PRIVATE KEY-----"""
    
    with open('atim-app.private-key.pem', 'w') as f:
        f.write(temp_key)
    
    os.chmod('atim-app.private-key.pem', 0o600)
    print("✅ Temporary private key file created")
    print("⚠️  This is a placeholder - you need to replace it with your real GitHub App private key")
    print()
    print("To get your real private key:")
    print("1. Go to https://github.com/settings/apps")
    print("2. Find your 'Atim AI Assistant' app")
    print("3. Download the private key (.pem file)")
    print("4. Replace the content in atim-app.private-key.pem")

if __name__ == "__main__":
    create_temp_key() 