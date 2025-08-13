#!/bin/bash

# Atim Assistant - GitHub Integration Setup Script
# This script helps configure GitHub integration for Atim AI Assistant

echo "🤖 Atim Assistant - GitHub Integration Setup"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the atim-assistant directory"
    exit 1
fi

echo "📋 Setting up GitHub integration for Atim Assistant..."
echo ""

# Step 1: Check current environment
echo "🔍 Checking current configuration..."
if [ -f "backend/.env" ]; then
    echo "✅ Backend .env file exists"
else
    echo "❌ Backend .env file missing"
    exit 1
fi

if [ -f ".env" ]; then
    echo "✅ Frontend .env file exists"
else
    echo "❌ Frontend .env file missing"
    exit 1
fi

echo ""

# Step 2: GitHub Token Setup Instructions
echo "🔑 GitHub Token Setup Instructions:"
echo "=================================="
echo ""
echo "1. Create Atim's GitHub Account (if not exists):"
echo "   - Go to: https://github.com/signup"
echo "   - Username: atim-ai-assistant"
echo "   - Email: Use a dedicated email for Atim"
echo "   - Profile: Add Atim's description and avatar"
echo ""
echo "2. Generate Atim's GitHub Token:"
echo "   - Go to: https://github.com/settings/tokens"
echo "   - Click 'Generate new token (classic)'"
echo "   - Note: 'Atim AI Assistant - Repository Access'"
echo "   - Expiration: 90 days (or longer)"
echo "   - Scopes:"
echo "     ✅ repo (Full control of private repositories)"
echo "     ✅ public_repo (Access public repositories)"
echo "     ✅ issues (Create issues)"
echo "     ✅ pull_requests (Create pull requests)"
echo ""
echo "3. Generate Your Personal Access Token:"
echo "   - Go to: https://github.com/settings/tokens"
echo "   - Click 'Generate new token (classic)'"
echo "   - Note: 'Atim Assistant - User Access'"
echo "   - Expiration: 90 days (or longer)"
echo "   - Scopes:"
echo "     ✅ repo (Full control of private repositories)"
echo "     ✅ public_repo (Access public repositories)"
echo "     ✅ issues (Create issues)"
echo "     ✅ pull_requests (Create pull requests)"
echo ""

# Step 3: Update environment files
echo "📝 Updating environment files..."
echo ""

# Update backend .env
cat > backend/.env << 'EOF'
SECRET_KEY=dev-secret-key-change-in-production
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
# MAIL_DEFAULT_SENDER=noreply@atim-assistant.com

# Mailhog local testing
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@atim-assistant.com

# GitHub Integration
# For GitHub App (Atim Bot) - Set this for autonomous operations
# Create a GitHub Personal Access Token for Atim at: https://github.com/settings/tokens
ATIM_GITHUB_TOKEN=your_atim_github_app_token_here
ATIM_GITHUB_USERNAME=atim-ai-assistant

# For User Token - Set this for user-based operations
# Create a GitHub Personal Access Token for your account at: https://github.com/settings/tokens
GITHUB_TOKEN=your_github_personal_access_token_here

# GitHub Repository
GITHUB_REPO=NiloticNetwork/NiloticNetworkBlockchain
EOF

# Update frontend .env
cat > .env << 'EOF'
VITE_API_URL=http://localhost:5070/api

# Atim's GitHub Bot Configuration
ATIM_GITHUB_TOKEN=your_atim_github_app_token_here
ATIM_GITHUB_USERNAME=atim-ai-assistant
ATIM_TARGET_REPO=NiloticNetwork/NiloticNetworkBlockchain
EOF

echo "✅ Environment files updated"
echo ""

# Step 4: Test current setup
echo "🧪 Testing current setup..."
cd backend
python atim_github_bot.py
cd ..

echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Replace the placeholder tokens in the .env files:"
echo "   - backend/.env: Update ATIM_GITHUB_TOKEN and GITHUB_TOKEN"
echo "   - .env: Update ATIM_GITHUB_TOKEN"
echo ""
echo "2. Test the integration:"
echo "   cd backend && python atim_github_bot.py"
echo ""
echo "3. Restart the application:"
echo "   ./stop-atim.sh && ./start-atim.sh"
echo ""
echo "4. Access the application:"
echo "   Open http://localhost:5173 in your browser"
echo ""
echo "🎉 Setup complete! Follow the instructions above to configure your tokens." 