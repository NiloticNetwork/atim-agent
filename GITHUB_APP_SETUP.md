# 🤖 Atim Assistant - GitHub App Setup Guide

## Overview

This guide will help you set up Atim Assistant as a proper GitHub App, which is the modern, secure, and recommended approach for bots. GitHub Apps provide better security, granular permissions, and a distinct identity for your AI assistant.

## Why GitHub Apps Over Personal Access Tokens?

### ✅ Advantages of GitHub Apps
- **Distinct Identity**: Appears as "[Atim Agent]" in GitHub
- **Granular Permissions**: Only request the permissions you need
- **Installation-based**: Can be installed on specific repositories
- **Webhook Support**: Real-time notifications and events
- **Better Security**: No user account credentials required
- **Scalable**: Can be installed on multiple repositories
- **Modern API**: Uses the latest GitHub API features

### ❌ Limitations of Personal Access Tokens
- **User Account**: Requires a GitHub user account
- **Broad Permissions**: Often grants more access than needed
- **Security Risk**: User credentials in environment variables
- **No Webhooks**: Limited to polling for updates
- **Account Management**: Need to manage user account separately

## Step-by-Step GitHub App Setup

### 1. Create a GitHub App

1. **Go to GitHub App Settings**:
   - Visit: https://github.com/settings/apps
   - Click "New GitHub App"

2. **Configure Basic Information**:
   ```
   App name: Atim AI Assistant
   Homepage URL: http://localhost:5173 (or your domain)
   App description: AI-powered blockchain development assistant for the Nilotic Network
   ```

3. **Set Webhook URL** (Optional for local development):
   ```
   Webhook URL: http://localhost:5070/webhook
   Webhook secret: atim-webhook-secret (generate a random string)
   ```

4. **Configure Permissions**:
   ```
   Repository permissions:
   - Contents: Read & write
   - Issues: Read & write
   - Pull requests: Read & write
   - Metadata: Read-only
   
   User permissions:
   - Email addresses: Read-only
   ```

5. **Subscribe to Events**:
   ```
   - Issues
   - Pull requests
   - Push
   - Repository
   ```

6. **Set Installation Options**:
   ```
   - Allow users to install the app on their repositories
   - Allow users to install the app on their organizations
   ```

### 2. Generate App Credentials

After creating the app, you'll get:

1. **App ID**: A numeric identifier
2. **Client ID**: For OAuth flows
3. **Client Secret**: For OAuth flows
4. **Private Key**: Download the .pem file

### 3. Install the App

1. **Install on Your Repository**:
   - Go to your app's installation page
   - Click "Install App"
   - Select your repository: `NiloticNetwork/NiloticNetworkBlockchain`
   - Grant the requested permissions

2. **Get Installation ID**:
   - After installation, note the installation ID
   - This will be used in API calls

### 4. Update Environment Configuration

Update your `.env` files with the GitHub App credentials:

#### Backend Configuration (`backend/.env`)
```bash
# GitHub App Configuration
GITHUB_APP_ID=your_app_id_here
GITHUB_APP_PRIVATE_KEY_PATH=backend/atim-app.private-key.pem
GITHUB_APP_INSTALLATION_ID=your_installation_id_here
GITHUB_APP_CLIENT_ID=your_client_id_here
GITHUB_APP_CLIENT_SECRET=your_client_secret_here

# Webhook Configuration (if using webhooks)
GITHUB_WEBHOOK_SECRET=atim-webhook-secret

# Repository Configuration
GITHUB_REPO=NiloticNetwork/NiloticNetworkBlockchain
```

#### Frontend Configuration (`.env`)
```bash
VITE_API_URL=http://localhost:5070/api

# GitHub App Configuration
GITHUB_APP_ID=your_app_id_here
GITHUB_APP_INSTALLATION_ID=your_installation_id_here
GITHUB_REPO=NiloticNetwork/NiloticNetworkBlockchain
```

### 5. Update the GitHub Integration Code

The GitHub integration needs to be updated to use the App authentication instead of PATs. Here's what needs to be changed:

#### Update `backend/atim_github_bot.py`
```python
import jwt
import time
from github import Github
from github.Auth import AppAuth

class AtimGitHubApp:
    def __init__(self):
        self.app_id = os.environ.get('GITHUB_APP_ID')
        self.private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
        self.installation_id = os.environ.get('GITHUB_APP_INSTALLATION_ID')
        
        # Generate JWT for app authentication
        self.jwt = self._generate_jwt()
        
        # Get installation access token
        self.access_token = self._get_installation_token()
        
        # Initialize GitHub client
        self.github = Github(auth=AppAuth(self.app_id, self.access_token))
    
    def _generate_jwt(self):
        """Generate JWT for GitHub App authentication"""
        with open(self.private_key_path, 'r') as f:
            private_key = f.read()
        
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,  # 10 minutes
            'iss': self.app_id
        }
        
        return jwt.encode(payload, private_key, algorithm='RS256')
    
    def _get_installation_token(self):
        """Get installation access token"""
        headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.post(
            f'https://api.github.com/app/installations/{self.installation_id}/access_tokens',
            headers=headers
        )
        
        if response.status_code == 201:
            return response.json()['token']
        else:
            raise Exception(f"Failed to get installation token: {response.text}")
```

## Webhook Setup (Optional)

For real-time updates, set up webhooks:

### 1. Configure Webhook Endpoint

Add to `backend/app.py`:
```python
@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    
    # Verify webhook signature
    if not verify_webhook_signature(payload, signature):
        return 'Unauthorized', 401
    
    event_type = request.headers.get('X-GitHub-Event')
    
    if event_type == 'issues':
        handle_issue_event(request.json)
    elif event_type == 'pull_request':
        handle_pr_event(request.json)
    
    return 'OK', 200
```

### 2. Webhook Events to Handle

- **Issues**: When issues are created, updated, or commented on
- **Pull Requests**: When PRs are created, updated, or merged
- **Push**: When code is pushed to the repository
- **Repository**: When repository settings change

## Testing the GitHub App

### 1. Test App Authentication
```bash
cd backend
python test_github_app.py
```

Expected output:
```
🤖 Testing Atim GitHub App...
==================================================
✅ GitHub App authenticated successfully
✅ Installation access token generated
✅ Repository access verified: NiloticNetwork/NiloticNetworkBlockchain
✅ Atim GitHub App is ready!
==================================================
```

### 2. Test App Capabilities
```python
# Test creating an issue as the app
app = AtimGitHubApp()
issue = app.create_issue(
    title="Test Issue from Atim App",
    body="This is a test issue created by Atim AI Assistant GitHub App."
)
print(f"Created issue: #{issue.number}")
```

## Security Best Practices

### 1. Private Key Security
- Store the private key file securely
- Use environment variables for paths
- Don't commit private keys to version control
- Rotate keys regularly

### 2. Installation Permissions
- Only request necessary permissions
- Review and audit app installations
- Monitor app usage and logs

### 3. Webhook Security
- Verify webhook signatures
- Use HTTPS for webhook endpoints
- Validate webhook payloads
- Rate limit webhook processing

## Migration from PAT to GitHub App

If you're migrating from Personal Access Tokens:

1. **Backup current configuration**
2. **Create the GitHub App** (steps above)
3. **Update environment variables**
4. **Test the new authentication**
5. **Remove old PAT configuration**
6. **Update any hardcoded PAT references**

## Troubleshooting

### Common Issues

#### 1. "App authentication failed"
- Check App ID and private key path
- Verify private key format (PEM)
- Ensure JWT generation is working

#### 2. "Installation not found"
- Verify installation ID
- Check if app is installed on repository
- Ensure installation has correct permissions

#### 3. "Permission denied"
- Review app permissions
- Check installation permissions
- Verify repository access

### Debug Commands
```bash
# Test app authentication
python test_github_app.py

# Check environment variables
python -c "import os; print('APP_ID:', os.environ.get('GITHUB_APP_ID'))"

# Verify private key
openssl rsa -in atim-app.private-key.pem -check
```

## Next Steps

After setting up the GitHub App:

1. **Test the integration**: Run the test scripts
2. **Configure webhooks**: For real-time updates
3. **Update the frontend**: To use app authentication
4. **Deploy to production**: With proper security measures
5. **Monitor usage**: Track app performance and errors

---

**🤖 Atim AI Assistant** - Now with proper GitHub App identity!

This setup gives Atim a professional, secure, and scalable presence in your GitHub workflow. 