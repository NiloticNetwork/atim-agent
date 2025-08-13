# 🤖 Atim Assistant - GitHub Integration Setup Guide

## Overview

Atim Assistant needs proper GitHub integration to function as an AI Technical Project Manager Agent. This guide will help you set up the GitHub integration step by step.

## Current Status

- ✅ **Application Running**: Frontend (http://localhost:5173) and Backend (http://localhost:5070)
- ✅ **API Working**: Sample data and endpoints functional
- ❌ **GitHub Integration**: Not configured (tokens missing)

## Step-by-Step Setup

### 1. Create Atim's GitHub Account

**Option A: Create a new account for Atim**
1. Go to: https://github.com/signup
2. Username: `atim-ai-assistant` (or your preferred name)
3. Email: Use a dedicated email for Atim
4. Profile: Add Atim's description and avatar

**Option B: Use your existing account**
- Skip this step if you want to use your personal GitHub account

### 2. Generate GitHub Tokens

#### For Atim Bot (Recommended)
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Configure the token:
   - **Note**: "Atim AI Assistant - Repository Access"
   - **Expiration**: 90 days (or longer)
   - **Scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `public_repo` (Access public repositories)
     - ✅ `issues` (Create issues)
     - ✅ `pull_requests` (Create pull requests)
4. Copy the token (starts with `ghp_`)

#### For Your Personal Account (Fallback)
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Configure the token:
   - **Note**: "Atim Assistant - User Access"
   - **Expiration**: 90 days (or longer)
   - **Scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `public_repo` (Access public repositories)
     - ✅ `issues` (Create issues)
     - ✅ `pull_requests` (Create pull requests)
4. Copy the token (starts with `ghp_`)

### 3. Configure Environment Variables

#### Update Backend Configuration (`backend/.env`)

Replace the placeholder values with your actual tokens:

```bash
# GitHub Integration
ATIM_GITHUB_TOKEN=ghp_your_atim_bot_token_here
ATIM_GITHUB_USERNAME=atim-ai-assistant
GITHUB_TOKEN=ghp_your_personal_token_here
GITHUB_REPO=NiloticNetwork/NiloticNetworkBlockchain
```

#### Update Frontend Configuration (`.env`)

```bash
VITE_API_URL=http://localhost:5070/api
ATIM_GITHUB_TOKEN=ghp_your_atim_bot_token_here
ATIM_GITHUB_USERNAME=atim-ai-assistant
ATIM_TARGET_REPO=NiloticNetwork/NiloticNetworkBlockchain
```

### 4. Test the Integration

Run the test script to verify everything is working:

```bash
cd backend
python atim_github_bot.py
```

Expected output:
```
🤖 Testing Atim GitHub Bot...
==================================================
🤖 Atim authenticated as: atim-ai-assistant
✅ Atim can access repository: NiloticNetwork/NiloticNetworkBlockchain
Repository: NiloticNetwork/NiloticNetworkBlockchain
Bot Status: online
✅ Atim bot is online and ready!
==================================================
```

### 5. Restart the Application

After configuring the tokens, restart the application:

```bash
./stop-atim.sh
./start-atim.sh
```

## Repository Access

### For Public Repositories
- No additional setup needed
- Atim can access public repositories with the configured tokens

### For Private Repositories
1. **Add Atim as a collaborator**:
   - Go to your repository settings
   - Navigate to "Collaborators and teams"
   - Add `atim-ai-assistant` as a collaborator
2. **Or ensure tokens have the `repo` scope**:
   - The `repo` scope grants access to private repositories

## Atim's Capabilities

Once configured, Atim can:

### 🤖 Autonomous Operations
- **Create Issues**: Automatically create issues with AI analysis
- **Generate Pull Requests**: Create PRs with suggested fixes
- **Comment on Issues**: Provide AI-powered insights
- **Repository Analysis**: Analyze code and suggest improvements

### 📊 Project Management
- **Kanban Board**: Track issues and PRs
- **Issue Tracking**: Monitor and manage issues
- **PR Management**: Review and manage pull requests
- **Chat Interface**: Discuss issues and PRs

### 🔍 Code Analysis
- **Security Analysis**: Detect security vulnerabilities
- **Performance Analysis**: Identify performance issues
- **Code Quality**: Suggest improvements
- **Documentation**: Generate documentation

## Troubleshooting

### Common Issues

#### 1. "Bad credentials" Error
```
❌ Atim GitHub authentication failed: 401 {"message": "Bad credentials"}
```
**Solution**: Check that your GitHub tokens are correct and have the right permissions.

#### 2. "Repository not found" Error
```
❌ Error accessing repository: 404 {"message": "Not Found"}
```
**Solution**: 
- Verify the repository name is correct
- Ensure Atim has access to the repository
- Check if the repository is private and Atim has access

#### 3. "Permission denied" Error
```
❌ Atim failed to create issue: 403 {"message": "Resource not accessible by integration"}
```
**Solution**: 
- Ensure the token has the `issues` scope
- Check if issues are enabled in the repository
- Verify Atim has write access to the repository

### Debug Commands

```bash
# Test Atim's bot
cd backend && python atim_github_bot.py

# Test GitHub integration
cd backend && python test_github.py

# Check environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('ATIM_TOKEN:', 'Set' if os.environ.get('ATIM_GITHUB_TOKEN') else 'Not set')"

# Check application status
curl http://localhost:5070/api/kanban
```

## Security Considerations

1. **Token Security**: 
   - Keep tokens secure and don't commit them to version control
   - Rotate tokens regularly
   - Use environment variables, not hardcoded values

2. **Repository Access**: 
   - Only grant necessary permissions
   - Review Atim's actions regularly
   - Monitor repository activity

3. **Audit Trail**: 
   - All Atim actions are logged
   - Actions are clearly marked as AI-generated
   - Maintain transparency about AI involvement

## Next Steps

After successful setup:

1. **Test Basic Functionality**:
   - Create a test issue
   - Generate a test PR
   - Verify repository analysis

2. **Configure Advanced Features**:
   - Set up automated issue creation
   - Configure PR templates
   - Set up notification systems

3. **Production Deployment**:
   - Use production-grade tokens
   - Set up proper environment variables
   - Configure monitoring and logging

## Success Indicators

You'll know Atim is working correctly when:

- ✅ `python atim_github_bot.py` shows "Atim bot is online and ready!"
- ✅ You can access http://localhost:5173 and see the Kanban board
- ✅ Atim can create issues and PRs in your repository
- ✅ The chat interface responds to queries about your repository

---

**🤖 Atim AI Assistant** - Your autonomous blockchain development partner!

For support, check the logs in `backend/server.log` or run the debug commands above. 