#!/usr/bin/env python3
"""
Simple script to create GitHub repository
"""

import requests
import json

# You need to replace this with your actual GitHub token
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # Replace with your token
GITHUB_USERNAME = "optimist0x"

def create_repo():
    repo_data = {
        "name": "github-warmer",
        "description": "🔥 Universal GitHub Activity Generator - Create realistic commits, PRs, and issues for your GitHub profile",
        "homepage": "https://github.com/optimist0x/github-warmer",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_downloads": True
    }
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/github-warmer"
    
    try:
        # First check if repo exists
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Repository already exists!")
            return True
        
        # Create repository
        url = "https://api.github.com/user/repos"
        response = requests.post(url, headers=headers, json=repo_data)
        
        if response.status_code == 201:
            repo_info = response.json()
            print("✅ Repository created successfully!")
            print(f"🔗 URL: {repo_info['html_url']}")
            print(f"📝 Clone URL: {repo_info['clone_url']}")
            return True
        else:
            print(f"❌ Error creating repository: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("Please update GITHUB_TOKEN in this script with your actual token")
    print("Then run: python3 create_repo_simple.py")
    # create_repo()
