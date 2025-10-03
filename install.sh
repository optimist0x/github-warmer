#!/bin/bash

# GitHub Warmer Installation Script
echo "🔥 GitHub Warmer - Installation Script"
echo "======================================"
echo ""

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ Python3 and pip3 are installed"
echo ""

# Install requirements
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Create config file if it doesn't exist
if [ ! -f "config.json" ]; then
    echo "🔧 Creating configuration file..."
    cp config.example.json config.json
    echo "✅ Configuration file created: config.json"
    echo ""
    echo "📝 Please edit config.json with your GitHub credentials:"
    echo "   - GitHub username"
    echo "   - GitHub email"
    echo "   - GitHub Personal Access Token"
    echo ""
    echo "🔗 To create a GitHub token:"
    echo "   https://github.com/settings/tokens"
    echo "   Required scopes: repo, public_repo"
else
    echo "✅ Configuration file already exists"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 To run GitHub Warmer:"
echo "   python3 github_warmer.py"
echo ""
echo "📚 For more information, see README.md"
