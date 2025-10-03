#!/bin/bash

# GitHub Warmer - Quick Run Script
echo "🔥 GitHub Warmer - Quick Run"
echo "============================"
echo ""

# Check if config exists
if [ ! -f "config.json" ]; then
    echo "❌ Configuration file not found!"
    echo "   Please run: ./install.sh"
    exit 1
fi

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3."
    exit 1
fi

echo "✅ All checks passed"
echo ""

# Run the main script
python3 github_warmer.py
