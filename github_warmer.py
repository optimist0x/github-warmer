#!/usr/bin/env python3
"""
GitHub Warmer - Universal GitHub Activity Generator
==================================================

A comprehensive tool to generate realistic GitHub activity including:
- Historical commits (2023-2025)
- Pull Requests with code
- Issues and bug reports
- Daily random changes

Usage:
    python3 github_warmer.py

Author: GitHub Warmer Community
License: MIT
"""

import os
import json
import random
import time
import requests
import subprocess
import shutil
import base64
from datetime import datetime, timedelta
from pathlib import Path

class GitHubWarmer:
    def __init__(self):
        self.config = self.load_or_create_config()
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.config['github_token']}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": f"{self.config['github_username']}-github-warmer"
        }
        self.repos_dir = Path("repos")
        
    def load_or_create_config(self):
        """Load or create configuration file"""
        config_file = "config.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Create default config
        print("🔧 Configuration file not found. Creating config.json...")
        print("Please fill in your GitHub credentials:")
        
        config = {
            "github_username": input("GitHub Username: ").strip(),
            "github_email": input("GitHub Email: ").strip(),
            "github_token": input("GitHub Personal Access Token: ").strip(),
            "repos_dir": "repos"
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration saved to config.json")
        return config
    
    def run_command(self, command, cwd=None):
        """Execute shell command"""
        try:
            result = subprocess.run(command, shell=True, cwd=cwd, 
                                  capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Command error: {e}")
            return None
    
    def generate_historical_dates(self, start_year=2023, end_year=2025, commits_per_month=2):
        """Generate historical commit dates"""
        dates = []
        current_date = datetime.now()
        
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year > current_date.year or (year == current_date.year and month > current_date.month):
                    continue
                
                for _ in range(commits_per_month):
                    day = random.randint(1, 28)
                    hour = random.randint(9, 22)
                    minute = random.randint(0, 59)
                    date = datetime(year, month, day, hour, minute)
                    dates.append(date)
        
        return sorted(dates)
    
    def clone_repository(self, repo_name):
        """Clone repository from GitHub"""
        repo_path = self.repos_dir / repo_name
        
        if repo_path.exists():
            shutil.rmtree(repo_path)
        
        clone_url = f"https://github.com/{self.config['github_username']}/{repo_name}.git"
        result = self.run_command(f"git clone {clone_url}", cwd=self.repos_dir)
        
        if result is not None:
            print(f"✅ Repository {repo_name} cloned")
            return repo_path
        else:
            print(f"❌ Failed to clone {repo_name}")
            return None
    
    def make_historical_change(self, file_path, date):
        """Make historical change to file"""
        if not os.path.exists(file_path):
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')
            
            if file_path.endswith('.py'):
                change = f"""
# Historical update {date_str}
def historical_feature():
    \"\"\"Feature added on {date_str}\"\"\"
    print('Historical feature working')
    return True"""
                content += change
            elif file_path.endswith('.md'):
                change = f"""

## Update {date_str}
- Historical feature added
- Code improvements
- Documentation updated"""
                content += change
            else:
                change = f"""
// Historical update {date_str}
// Code improvements and bug fixes"""
                content = change + "\n" + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"❌ Error modifying file {file_path}: {e}")
            return False
    
    def create_historical_commits(self, repo_name, start_year=2023, end_year=2025, commits_per_month=2):
        """Create historical commits for repository"""
        print(f"\n🔥 Creating historical commits for {repo_name}")
        print("=" * 50)
        
        repo_path = self.clone_repository(repo_name)
        if repo_path is None:
            return False
        
        # Configure git
        self.run_command(f"git config user.name '{self.config['github_username']}'", cwd=repo_path)
        self.run_command(f"git config user.email '{self.config['github_email']}'", cwd=repo_path)
        
        # Generate dates
        dates = self.generate_historical_dates(start_year, end_year, commits_per_month)
        
        print(f"📅 Creating {len(dates)} historical commits...")
        
        commit_messages = [
            "Add new feature", "Fix bug", "Improve code", "Update documentation",
            "Optimize performance", "Refactor code", "Add tests", "Update dependencies",
            "Fix security issue", "Improve UI", "Add error handling", "Update README"
        ]
        
        for i, date in enumerate(dates, 1):
            print(f"   🔨 Commit {i}/{len(dates)}: {date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Find files to modify
            files_to_change = []
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.json', '.md')) and not file.startswith('.'):
                        files_to_change.append(os.path.join(root, file))
            
            if files_to_change:
                file_to_change = random.choice(files_to_change)
                if self.make_historical_change(file_to_change, date):
                    commit_message = random.choice(commit_messages)
                    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
                    commit_cmd = f'git add . && GIT_COMMITTER_DATE="{date_str}" git commit --date="{date_str}" -m "{commit_message}"'
                    
                    result = self.run_command(commit_cmd, cwd=repo_path)
                    if result is not None:
                        print(f"      ✅ {commit_message}")
        
        # Push to GitHub
        print(f"\n🚀 Pushing historical commits to GitHub...")
        result = self.run_command("git push --force-with-lease", cwd=repo_path)
        
        if result is not None:
            print(f"✅ Historical commits for {repo_name} pushed successfully!")
            return True
        else:
            print(f"❌ Failed to push commits for {repo_name}")
            return False
    
    def create_branch(self, repo_name, branch_name):
        """Create new branch"""
        try:
            for default_branch in ["main", "master"]:
                ref_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/git/ref/heads/{default_branch}"
                response = requests.get(ref_url, headers=self.headers)
                if response.status_code == 200:
                    base_branch = default_branch
                    break
            else:
                print(f"❌ Cannot find main branch in {repo_name}")
                return None
            
            ref_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/git/ref/heads/{base_branch}"
            response = requests.get(ref_url, headers=self.headers)
            ref_data = response.json()
            sha = ref_data['object']['sha']
            
            create_ref_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/git/refs"
            create_data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": sha
            }
            
            response = requests.post(create_ref_url, headers=self.headers, json=create_data)
            
            if response.status_code == 201:
                print(f"✅ Branch {branch_name} created")
                return branch_name
            else:
                print(f"❌ Error creating branch: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating branch: {e}")
            return None
    
    def create_file_in_branch(self, repo_name, branch_name, file_path, content, commit_message):
        """Create file in branch"""
        try:
            content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            file_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/contents/{file_path}"
            file_data = {
                "message": commit_message,
                "content": content_b64,
                "branch": branch_name
            }
            
            response = requests.get(file_url, headers=self.headers, params={"ref": branch_name})
            if response.status_code == 200:
                existing_file = response.json()
                file_data["sha"] = existing_file["sha"]
            
            response = requests.put(file_url, headers=self.headers, json=file_data)
            
            if response.status_code in [200, 201]:
                print(f"✅ File {file_path} created")
                return True
            else:
                print(f"❌ Error creating file: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return False
    
    def create_pull_request(self, repo_name, title, body, head_branch):
        """Create pull request"""
        try:
            for default_branch in ["main", "master"]:
                ref_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/git/ref/heads/{default_branch}"
                response = requests.get(ref_url, headers=self.headers)
                if response.status_code == 200:
                    base_branch = default_branch
                    break
            else:
                base_branch = "main"
            
            pr_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/pulls"
            pr_data = {
                "title": title,
                "body": body,
                "head": head_branch,
                "base": base_branch
            }
            
            response = requests.post(pr_url, headers=self.headers, json=pr_data)
            
            if response.status_code == 201:
                pr_data = response.json()
                print(f"✅ Pull Request created: {title}")
                print(f"   🔗 URL: {pr_data['html_url']}")
                return pr_data['number']
            else:
                print(f"❌ Error creating PR: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating PR: {e}")
            return None
    
    def create_issue(self, repo_name, title, body, labels=None):
        """Create issue"""
        try:
            if labels is None:
                labels = []
                
            issue_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/issues"
            issue_data = {
                "title": title,
                "body": body,
                "labels": labels
            }
            
            response = requests.post(issue_url, headers=self.headers, json=issue_data)
            
            if response.status_code == 201:
                issue_data = response.json()
                print(f"✅ Issue created: {title}")
                print(f"   🔗 URL: {issue_data['html_url']}")
                return issue_data['number']
            else:
                print(f"❌ Error creating Issue: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating Issue: {e}")
            return None
    
    def merge_pull_request(self, repo_name, pr_number):
        """Merge pull request"""
        try:
            merge_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/pulls/{pr_number}/merge"
            merge_data = {
                "commit_title": f"Merge PR #{pr_number}",
                "merge_method": "merge"
            }
            
            response = requests.put(merge_url, headers=self.headers, json=merge_data)
            
            if response.status_code == 200:
                print(f"✅ Pull Request #{pr_number} merged")
                return True
            else:
                print(f"❌ Error merging PR: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error merging PR: {e}")
            return False
    
    def close_issue(self, repo_name, issue_number):
        """Close issue"""
        try:
            issue_url = f"{self.base_url}/repos/{self.config['github_username']}/{repo_name}/issues/{issue_number}"
            issue_data = {"state": "closed"}
            
            response = requests.patch(issue_url, headers=self.headers, json=issue_data)
            
            if response.status_code == 200:
                print(f"✅ Issue #{issue_number} closed")
                return True
            else:
                print(f"❌ Error closing Issue: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error closing Issue: {e}")
            return False
    
    def generate_file_content(self, file_type):
        """Generate file content for PR"""
        if file_type == "feature":
            return '''"""
New feature implementation
"""

def new_feature():
    """New feature function"""
    print("Feature is working!")
    return True

def feature_helper():
    """Helper function"""
    return "Helper data"

if __name__ == "__main__":
    new_feature()
'''
        elif file_type == "bugfix":
            return '''"""
Bug fix implementation
"""

def fixed_function():
    """Fixed function"""
    try:
        result = 42
        return result
    except Exception as e:
        print(f"Error handled: {e}")
        return None

def validate_input(data):
    """Input validation"""
    if not data:
        raise ValueError("Data cannot be empty")
    return data

if __name__ == "__main__":
    fixed_function()
'''
        else:  # improvement
            return '''"""
Code improvement implementation
"""

class ImprovedClass:
    """Improved class"""
    
    def __init__(self):
        self.data = []
    
    def improved_method(self):
        """Improved method"""
        return sorted(self.data)
    
    def optimized_operation(self):
        """Optimized operation"""
        return sum(self.data)

if __name__ == "__main__":
    obj = ImprovedClass()
    obj.improved_method()
'''
    
    def create_pull_request_activity(self, repo_name):
        """Create pull request with realistic content"""
        print(f"\n🔥 Creating Pull Request for {repo_name}")
        print("-" * 40)
        
        pr_templates = [
            ("Add new feature: user authentication", "## Description\nThis PR adds user authentication functionality.\n\n## Changes\n- Added authentication module\n- Updated database schema\n- Added tests\n\n## Testing\n- [x] Unit tests pass\n- [x] Integration tests pass"),
            ("Implement data validation", "## Summary\nImplements comprehensive data validation.\n\n## Features\n- Input validation\n- Error handling\n- Performance optimization\n\n## Breaking Changes\nNone"),
            ("Fix memory leak in main function", "## Bug Fix\nFixes memory leak issue.\n\n## Problem\nMemory leak was causing performance issues.\n\n## Solution\n- Proper resource management\n- Added cleanup procedures\n- Enhanced error handling"),
            ("Improve performance", "## Performance Improvement\nOptimizes application performance.\n\n## Changes\n- Algorithm optimization\n- Memory usage reduction\n- Caching implementation\n\n## Results\n- 40% faster execution\n- 30% less memory usage"),
            ("Add API integration", "## Feature\nAdds API integration capabilities.\n\n## Implementation\n- RESTful API endpoints\n- Authentication handling\n- Error management\n\n## Testing\nAll tests pass successfully"),
            ("Enhance security", "## Security Enhancement\nImproves application security.\n\n## Changes\n- Input sanitization\n- Authentication improvements\n- Vulnerability fixes\n\n## Impact\nEnhanced security posture")
        ]
        
        title, body = random.choice(pr_templates)
        
        # Create branch
        branch_name = f"pr-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if not self.create_branch(repo_name, branch_name):
            return False
        
        # Create file
        file_types = ["feature", "bugfix", "improvement"]
        file_type = random.choice(file_types)
        file_content = self.generate_file_content(file_type)
        commit_message = f"Add {file_type}: {title[:30]}..."
        
        if not self.create_file_in_branch(repo_name, branch_name, f"src/{file_type}_{datetime.now().strftime('%Y%m%d')}.py", file_content, commit_message):
            return False
        
        # Create PR
        pr_number = self.create_pull_request(repo_name, title, body, branch_name)
        
        if pr_number:
            time.sleep(2)
            self.merge_pull_request(repo_name, pr_number)
            return True
        
        return False
    
    def create_issue_activity(self, repo_name):
        """Create issue with realistic content"""
        print(f"\n🔥 Creating Issue for {repo_name}")
        print("-" * 40)
        
        issue_templates = [
            ("Bug: UI not responsive on mobile", "## Bug Description\nUI becomes unresponsive on mobile devices.\n\n## Steps to Reproduce\n1. Open on mobile\n2. Navigate to feature\n3. UI freezes\n\n## Expected Behavior\nSmooth UI interaction\n\n## Environment\n- Mobile browser\n- iOS/Android"),
            ("Feature Request: dark mode", "## Feature Request\nAdd dark mode support.\n\n## Problem\nUsers want dark theme option.\n\n## Proposed Solution\n- Theme toggle\n- System preference detection\n- Persistent settings\n\n## Benefits\nBetter user experience"),
            ("Improvement: better error messages", "## Improvement Suggestion\nImprove error message clarity.\n\n## Current State\nError messages are unclear.\n\n## Proposed Improvement\n- Clearer language\n- Actionable guidance\n- Better formatting\n\n## Impact\nImproved user experience"),
            ("Bug: file upload fails", "## Bug Report\nFile upload functionality fails.\n\n## Issue\nLarge files cannot be uploaded.\n\n## Environment\n- Chrome browser\n- Files > 10MB\n\n## Workaround\nSplit files into smaller chunks"),
            ("Feature Request: search functionality", "## Feature Request\nAdd search capabilities.\n\n## Use Case\nUsers need to find content quickly.\n\n## Implementation Ideas\n- Full-text search\n- Filter options\n- Search suggestions\n\n## Priority\nHigh - requested by many users")
        ]
        
        title, body = random.choice(issue_templates)
        labels = random.choice([["bug"], ["enhancement"], ["improvement"], ["feature"]])
        
        # Create issue
        issue_number = self.create_issue(repo_name, title, body, labels)
        
        if issue_number:
            time.sleep(2)
            self.close_issue(repo_name, issue_number)
            return True
        
        return False
    
    def create_daily_change(self, repo_name):
        """Create daily random change"""
        print(f"\n🔥 Creating daily change for {repo_name}")
        print("-" * 40)
        
        repo_path = self.repos_dir / repo_name
        
        if not repo_path.exists():
            if not self.clone_repository(repo_name):
                return False
        
        # Configure git
        self.run_command(f"git config user.name '{self.config['github_username']}'", cwd=repo_path)
        self.run_command(f"git config user.email '{self.config['github_email']}'", cwd=repo_path)
        
        # Find files to modify
        files_to_change = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.json', '.md')) and not file.startswith('.'):
                    files_to_change.append(os.path.join(root, file))
        
        if files_to_change:
            file_to_change = random.choice(files_to_change)
            if self.make_historical_change(file_to_change, datetime.now()):
                commit_messages = [
                    "Daily update", "Code improvement", "Bug fix", "Feature enhancement",
                    "Performance optimization", "Documentation update", "Code cleanup"
                ]
                commit_message = random.choice(commit_messages)
                
                result = self.run_command("git add . && git commit -m \"" + commit_message + "\"", cwd=repo_path)
                if result is not None:
                    print(f"✅ {commit_message}")
                    
                    # Push to GitHub
                    result = self.run_command("git push", cwd=repo_path)
                    if result is not None:
                        print(f"✅ Daily change pushed to {repo_name}")
                        return True
        
        print(f"❌ Failed to create daily change for {repo_name}")
        return False
    
    def run_activity_mode(self, mode, repo_names=None):
        """Run different activity modes"""
        if repo_names is None:
            repo_names = ["Schedule", "warm"]  # Default repositories
        
        self.repos_dir.mkdir(exist_ok=True)
        
        if mode == "historical":
            print("🔥 Historical Commits Mode")
            print("Creating historical commits for 2023-2025...")
            
            for repo_name in repo_names:
                self.create_historical_commits(repo_name, 2023, 2025, 2)
        
        elif mode == "pr_issues":
            print("🔥 PR & Issues Mode")
            print("Creating Pull Requests and Issues...")
            
            pr_count = 3
            issue_count = 5
            
            for repo_name in repo_names:
                print(f"\n📝 Creating {pr_count} PRs and {issue_count} Issues for {repo_name}")
                
                # Create PRs
                for i in range(pr_count):
                    print(f"\n📝 Creating PR {i+1}/{pr_count}")
                    self.create_pull_request_activity(repo_name)
                    time.sleep(1)
                
                # Create Issues
                for i in range(issue_count):
                    print(f"\n📝 Creating Issue {i+1}/{issue_count}")
                    self.create_issue_activity(repo_name)
                    time.sleep(1)
        
        elif mode == "daily":
            print("🔥 Daily Change Mode")
            print("Creating daily random changes...")
            
            for repo_name in repo_names:
                self.create_daily_change(repo_name)
        
        elif mode == "mass":
            print("🔥 Mass Activity Mode")
            print("Creating maximum activity...")
            
            pr_count = 8
            issue_count = 12
            
            for repo_name in repo_names:
                print(f"\n📝 Creating {pr_count} PRs and {issue_count} Issues for {repo_name}")
                
                # Create PRs
                for i in range(pr_count):
                    print(f"\n📝 Creating PR {i+1}/{pr_count}")
                    self.create_pull_request_activity(repo_name)
                    time.sleep(1)
                
                # Create Issues
                for i in range(issue_count):
                    print(f"\n📝 Creating Issue {i+1}/{issue_count}")
                    self.create_issue_activity(repo_name)
                    time.sleep(1)

def main():
    print("🔥 GitHub Warmer - Universal GitHub Activity Generator")
    print("=" * 60)
    print("Generate realistic GitHub activity including:")
    print("- Historical commits (2023-2025)")
    print("- Pull Requests with code")
    print("- Issues and bug reports")
    print("- Daily random changes")
    print()
    
    warmer = GitHubWarmer()
    
    print("Available modes:")
    print("1. Historical Commits - Create backdated commits for 2023-2025")
    print("2. PR & Issues - Create Pull Requests and Issues")
    print("3. Daily Change - Create daily random changes")
    print("4. Mass Activity - Create maximum activity (lots of PRs and Issues)")
    print("5. All Modes - Run all modes sequentially")
    print()
    
    try:
        choice = input("Select mode (1-5): ").strip()
        
        if choice == "1":
            warmer.run_activity_mode("historical")
        elif choice == "2":
            warmer.run_activity_mode("pr_issues")
        elif choice == "3":
            warmer.run_activity_mode("daily")
        elif choice == "4":
            warmer.run_activity_mode("mass")
        elif choice == "5":
            print("🔥 Running all modes...")
            warmer.run_activity_mode("historical")
            time.sleep(5)
            warmer.run_activity_mode("pr_issues")
            time.sleep(5)
            warmer.run_activity_mode("daily")
            time.sleep(5)
            warmer.run_activity_mode("mass")
        else:
            print("❌ Invalid choice")
            return
        
        print("\n🎉 GitHub Warmer completed successfully!")
        print("📊 Check your GitHub profile for the new activity!")
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
