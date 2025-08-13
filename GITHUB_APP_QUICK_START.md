# 🚀 Atim Assistant - GitHub App Quick Start

## Overview

This guide will help you quickly set up Atim Assistant as a proper GitHub App, giving it a distinct identity and secure access to your repositories.

## ✅ Why GitHub Apps?

- **Distinct Identity**: Appears as "[Atim Agent]" in GitHub
- **Granular Permissions**: Only request what you need
- **Better Security**: No user account credentials
- **Modern API**: Latest GitHub features
- **Webhook Support**: Real-time notifications

## 🚀 Quick Setup (5 Steps)

### Step 1: Create GitHub App

1. Go to: https://github.com/settings/apps
2. Click "New GitHub App"
3. Configure with these details:

```
App name: Atim AI Assistant
Homepage URL: http://localhost:5173
App description: AI-powered blockchain development assistant for the Nilotic Network
```

4. Set permissions:
   - **Repository permissions**: Contents (Read & write), Issues (Read & write), Pull requests (Read & write), Metadata (Read-only)
   - **User permissions**: Email addresses (Read-only)

5. Subscribe to events: Issues, Pull requests, Push, Repository

6. Set installation options: Allow users to install on repositories

### Step 2: Install the App

1. After creating the app, click "Install App"
2. Select your repository: `NiloticNetwork/NiloticNetworkBlockchain`
3. Grant the requested permissions
4. Note the **Installation ID** from the URL

### Step 3: Get App Credentials

From your GitHub App settings, note:
- **App ID** (numeric)
- **Installation ID** (from step 2)
- **Client ID**
- **Client Secret**
- **Private Key** (download the .pem file)

### Step 4: Configure Atim Assistant

Run the configuration script:
```bash
cd web/atim-assistant
python setup_github_app.py
```

Enter your credentials when prompted.

### Step 5: Test the Setup

```bash
python test_github_app.py
```

Expected output:
```
🎉 All tests passed! Atim GitHub App is ready to use.
   Access the application at: http://localhost:5173
```

## 📁 Files Created

- `backend/atim_github_app.py` - GitHub App implementation
- `setup_github_app.py` - Configuration script
- `test_github_app.py` - Test script
- `GITHUB_APP_SETUP.md` - Detailed setup guide

## 🔧 Environment Variables

Your `.env` files will be updated with:

```bash
# Backend (.env)
GITHUB_APP_ID=your_app_id
GITHUB_APP_PRIVATE_KEY_PATH=backend/atim-app.private-key.pem
GITHUB_APP_INSTALLATION_ID=your_installation_id
GITHUB_APP_CLIENT_ID=your_client_id
GITHUB_APP_CLIENT_SECRET=your_client_secret
GITHUB_WEBHOOK_SECRET=generated_secret
GITHUB_REPO=NiloticNetwork/NiloticNetworkBlockchain

# Frontend (.env)
GITHUB_APP_ID=your_app_id
GITHUB_APP_INSTALLATION_ID=your_installation_id
GITHUB_REPO=NiloticNetwork/NiloticNetworkBlockchain
```

## 🎯 What Atim Can Do

Once configured, Atim will:

- ✅ **Create Issues**: Automatically create issues with AI analysis
- ✅ **Generate PRs**: Create pull requests with suggested fixes
- ✅ **Comment**: Provide AI-powered insights on issues
- ✅ **Analyze Code**: Detect security and performance issues
- ✅ **Manage Projects**: Track issues and PRs in Kanban board

## 🔍 Troubleshooting

### Common Issues

#### "App authentication failed"
- Check App ID and private key path
- Verify private key format (PEM)
- Ensure JWT generation is working

#### "Installation not found"
- Verify installation ID
- Check if app is installed on repository
- Ensure installation has correct permissions

#### "Permission denied"
- Review app permissions
- Check installation permissions
- Verify repository access

### Debug Commands

```bash
# Test GitHub App
python test_github_app.py

# Test specific component
cd backend && python atim_github_app.py

# Check environment
python -c "import os; print('APP_ID:', os.environ.get('GITHUB_APP_ID'))"
```

## 🎉 Success Indicators

You'll know it's working when:

- ✅ `python test_github_app.py` shows all tests passed
- ✅ Atim appears as "[Atim Agent]" in GitHub
- ✅ Can create issues and PRs automatically
- ✅ Kanban board shows real repository data
- ✅ Chat interface responds to repository queries

## 📞 Next Steps

After successful setup:

1. **Test Basic Features**: Create a test issue
2. **Configure Webhooks**: For real-time updates
3. **Customize Permissions**: Adjust as needed
4. **Deploy to Production**: With proper security
5. **Monitor Usage**: Track app performance

---

**🤖 Atim AI Assistant** - Now with proper GitHub App identity!

This setup gives Atim a professional, secure, and scalable presence in your GitHub workflow. 