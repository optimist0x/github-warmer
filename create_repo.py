#!/usr/bin/env python3
"""
Script to create GitHub repository for GitHub Warmer
"""

import requests
import json
import os

def create_github_repo():
    # Load config from the main directory
    config_path = "../config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        github_token = config['github_token']
        github_username = config['github_username']
    else:
        print("❌ Config file not found")
        return False
    
    # Repository details
    repo_data = {
        "name": "github-warmer",
        "description": "🔥 Universal GitHub Activity Generator - Create realistic commits, PRs, and issues for your GitHub profile",
        "homepage": "https://github.com/optimist0x/github-warmer",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_downloads": True,
        "auto_init": False
    }
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = "https://api.github.com/user/repos"
    
    try:
        response = requests.post(url, headers=headers, json=repo_data)
        
        if response.status_code == 201:
            repo_info = response.json()
            print("✅ Repository created successfully!")
            print(f"🔗 URL: {repo_info['html_url']}")
            print(f"📝 Clone URL: {repo_info['clone_url']}")
            return repo_info['clone_url']
        else:
            print(f"❌ Error creating repository: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    create_github_repo()
