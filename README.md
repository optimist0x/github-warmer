# 🔥 GitHub Warmer

**Universal GitHub Activity Generator**

A comprehensive Python tool to generate realistic GitHub activity including historical commits, Pull Requests, Issues, and daily changes. Perfect for maintaining an active GitHub profile or demonstrating consistent development activity.

## ✨ Features

- 🕰️ **Historical Commits** - Create backdated commits for 2023-2025
- 🚀 **Pull Requests** - Generate realistic PRs with code and descriptions
- 📝 **Issues** - Create bug reports and feature requests
- 📅 **Daily Changes** - Make random daily commits
- 🎯 **Mass Activity** - Create maximum GitHub activity
- 🔧 **Easy Setup** - Simple configuration and usage

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/github-warmer.git
cd github-warmer

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example configuration
cp config.example.json config.json

# Edit config.json with your GitHub credentials
nano config.json
```

**Required GitHub Token Permissions:**
- `repo` (Full control of private repositories)
- `public_repo` (Access public repositories)

### 3. Usage

```bash
python3 github_warmer.py
```

## 📋 Configuration

Create a `config.json` file with your GitHub credentials:

```json
{
  "github_username": "your-github-username",
  "github_email": "your-email@example.com",
  "github_token": "your-github-personal-access-token",
  "repos_dir": "repos"
}
```

### Getting GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `public_repo`
4. Copy the generated token

## 🎯 Usage Modes

### 1. Historical Commits
Creates backdated commits for 2023-2025 to show long-term activity.

```bash
python3 github_warmer.py
# Select option 1
```

### 2. PR & Issues
Generates Pull Requests and Issues with realistic content.

```bash
python3 github_warmer.py
# Select option 2
```

### 3. Daily Change
Makes random daily commits to keep your profile active.

```bash
python3 github_warmer.py
# Select option 3
```

### 4. Mass Activity
Creates maximum activity with lots of PRs and Issues.

```bash
python3 github_warmer.py
# Select option 4
```

### 5. All Modes
Runs all modes sequentially for complete activity generation.

```bash
python3 github_warmer.py
# Select option 5
```

## 📊 What Gets Created

### Historical Commits
- Backdated commits from 2023-2025
- Realistic commit messages
- Code changes and documentation updates
- 2 commits per month per repository

### Pull Requests
- Feature implementations
- Bug fixes
- Performance improvements
- Security enhancements
- All PRs are automatically merged

### Issues
- Bug reports
- Feature requests
- Improvement suggestions
- All Issues are automatically closed

### Daily Changes
- Random code modifications
- Documentation updates
- Small feature additions
- Bug fixes

## 🛠️ Technical Details

### Supported File Types
- Python (`.py`)
- JavaScript (`.js`, `.ts`)
- JSON (`.json`)
- Markdown (`.md`)

### Repository Requirements
- Must be owned by your GitHub account
- Must have at least one file
- Supports both `main` and `master` branches

### API Usage
- Uses GitHub REST API v3
- Respects GitHub rate limits
- Includes proper error handling

## 🔒 Security & Privacy

- **No Data Collection** - All activity is local to your repositories
- **Secure Configuration** - Credentials stored locally in config.json
- **Rate Limiting** - Respects GitHub API limits
- **Error Handling** - Graceful failure with detailed error messages

## 📈 Results

After running GitHub Warmer, your profile will show:

- 🟢 **Consistent Activity** - Regular commits over multiple years
- 🚀 **Professional PRs** - Well-documented pull requests
- 📝 **Realistic Issues** - Bug reports and feature requests
- 📊 **Active Contribution Graph** - Fully green GitHub calendar

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Fork the repository
git clone https://github.com/your-username/github-warmer.git
cd github-warmer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make your changes and test
python3 github_warmer.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use. Please use responsibly and in accordance with GitHub's Terms of Service. The generated activity should represent realistic development work and not be used to misrepresent your actual coding abilities.

## 🆘 Support

If you encounter any issues:

1. Check that your GitHub token has the correct permissions
2. Ensure your repositories exist and are accessible
3. Verify your internet connection
4. Check the error messages for specific issues

## 🌟 Features in Detail

### Smart Branch Detection
Automatically detects whether your repository uses `main` or `master` as the default branch.

### Realistic Content Generation
- Professional commit messages
- Detailed PR descriptions
- Comprehensive issue reports
- Contextual code changes

### Error Recovery
- Graceful handling of API errors
- Automatic retry mechanisms
- Detailed error reporting
- Safe failure modes

### Customizable Activity
- Adjustable commit frequency
- Configurable repository selection
- Multiple activity modes
- Flexible scheduling

## 📊 Example Output

```
🔥 GitHub Warmer - Universal GitHub Activity Generator
============================================================

Available modes:
1. Historical Commits - Create backdated commits for 2023-2025
2. PR & Issues - Create Pull Requests and Issues
3. Daily Change - Create daily random changes
4. Mass Activity - Create maximum activity
5. All Modes - Run all modes sequentially

Select mode (1-5): 2

🔥 PR & Issues Mode
Creating Pull Requests and Issues...

🔥 Creating Pull Request for Schedule
----------------------------------------
✅ Branch pr-20250102120000 created
✅ File src/feature_20250102.py created
✅ Pull Request created: Add new feature: user authentication
   🔗 URL: https://github.com/username/Schedule/pull/1
✅ Pull Request #1 merged

🔥 Creating Issue for Schedule
----------------------------------------
✅ Issue created: Bug: UI not responsive on mobile
   🔗 URL: https://github.com/username/Schedule/issues/1
✅ Issue #1 closed

🎉 GitHub Warmer completed successfully!
📊 Check your GitHub profile for the new activity!
```

---

**Made with ❤️ for the GitHub community**
