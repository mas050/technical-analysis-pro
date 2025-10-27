# 📚 Git & GitHub Workflow Guide

Complete guide for managing your Technical Analysis Pro repository on GitHub.

---

## 🚀 Part 1: Initial Setup & First Push to GitHub

### Step 1: Navigate to Your Project

```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
```

### Step 2: Initialize Git Repository

```bash
git init
```

### Step 3: Verify .gitignore Exists

Check that `.gitignore` is present and contains:

```bash
cat .gitignore
```

Should include:
- `venv/`
- `node_modules/`
- `__pycache__/`
- `.env`
- `charts/`
- `reports/`

### Step 4: Add All Files

```bash
git add .
```

### Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: Technical Analysis Pro web application

- Flask backend with REST API and WebSocket support
- React frontend with real-time progress tracking
- 50+ technical indicators (RSI, MACD, Bollinger Bands, etc.)
- AI-powered insights with Google Gemini
- Comprehensive visualization charts
- Raspberry Pi deployment guide with Tailscale
- Systemd service for auto-start on boot"
```

### Step 6: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon (top right)
3. Select **New repository**
4. Repository name: `technical-analysis-pro`
5. Description: `AI-Powered Technical Analysis Web Application`
6. Choose **Public** or **Private**
7. **DO NOT** check "Initialize with README" (you already have one)
8. Click **Create repository**

### Step 7: Authenticate with GitHub

**Option A: Using GitHub CLI (Recommended - Easiest)**

```bash
# Install GitHub CLI if not already installed
brew install gh

# Authenticate
gh auth login
```

Follow the prompts:
- Choose: **GitHub.com**
- Choose: **HTTPS**
- Authenticate with: **Login with a web browser**
- Copy the code shown and paste in browser

**Option B: Using SSH (Most Secure)**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept defaults
# Copy your public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# 1. Go to GitHub.com → Settings → SSH and GPG keys
# 2. Click "New SSH key"
# 3. Paste your key
# 4. Click "Add SSH key"
```

**Option C: Using Personal Access Token**

```bash
# 1. Go to GitHub.com → Settings → Developer settings
# 2. Personal access tokens → Tokens (classic)
# 3. Generate new token (classic)
# 4. Select scope: repo (full control)
# 5. Generate and COPY the token immediately
```

### Step 8: Add Remote Repository

**If using GitHub CLI or Personal Access Token (HTTPS):**

```bash
git remote add origin https://github.com/mas050/technical-analysis-pro.git
```

**If using SSH:**

```bash
git remote add origin git@github.com:mas050/technical-analysis-pro.git
```

### Step 9: Rename Branch to Main

```bash
git branch -M main
```

### Step 10: Push to GitHub

```bash
git push -u origin main
```

### Step 11: Verify on GitHub

Go to https://github.com/mas050/technical-analysis-pro and verify all files are there!

✅ **Initial setup complete!**

---

## 🔄 Part 2: Daily Workflow - Updating Your Repository

### Quick 3-Step Process

Every time you make changes and want to update GitHub:

```bash
# 1. Add changes
git add .

# 2. Commit with message
git commit -m "Description of what you changed"

# 3. Push to GitHub
git push
```

### Detailed Workflow

#### Step 1: Check What Changed

```bash
# See which files were modified
git status

# See the actual changes
git diff

# See changes in a specific file
git diff app.py
```

#### Step 2: Add Your Changes

**Option A: Add everything**

```bash
git add .
```

**Option B: Add specific files**

```bash
git add app.py technical_analysis.py
```

**Option C: Add by pattern**

```bash
# Add all Python files
git add *.py

# Add all files in a directory
git add frontend/src/
```

#### Step 3: Commit Your Changes

**Good commit message format:**

```bash
git commit -m "Type: Brief description

Optional detailed explanation of what changed and why"
```

**Commit message types:**
- `Fix:` - Bug fixes
- `Add:` - New features
- `Update:` - Improvements to existing features
- `Remove:` - Removed features or files
- `Refactor:` - Code restructuring
- `Docs:` - Documentation changes
- `Style:` - Formatting, styling changes

**Examples:**

```bash
# Simple fix
git commit -m "Fix: Resolved port 5000 conflict with AirPlay"

# New feature
git commit -m "Add: Support for cryptocurrency analysis"

# Multiple changes
git commit -m "Update: Improved analysis performance

- Optimized data fetching from Yahoo Finance
- Reduced chart generation time by 40%
- Added caching for frequently accessed symbols"

# Documentation update
git commit -m "Docs: Updated Raspberry Pi deployment guide"
```

#### Step 4: Push to GitHub

```bash
git push
```

That's it! Your changes are now on GitHub.

---

## 📋 Common Scenarios

### Scenario 1: Fixed a Bug

```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website

# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Fix: Matplotlib crash on background threads

Added matplotlib.use('Agg') to prevent NSException on macOS"

# Push
git push
```

### Scenario 2: Added New Feature

```bash
# Add changes
git add .

# Commit
git commit -m "Add: Export analysis to PDF

Users can now download analysis reports as PDF files"

# Push
git push
```

### Scenario 3: Updated Documentation

```bash
# Add changes
git add RASPBERRY_PI_DEPLOYMENT.md

# Commit
git commit -m "Docs: Added troubleshooting section to Pi guide"

# Push
git push
```

### Scenario 4: Multiple Small Changes Throughout the Day

```bash
# After first change
git add app.py
git commit -m "Fix: CORS configuration for port 5001"
git push

# After second change
git add visualization.py
git commit -m "Update: Improved chart colors"
git push

# After third change
git add README.md
git commit -m "Docs: Updated installation instructions"
git push
```

### Scenario 5: Working on a Big Feature

```bash
# Create a new branch for the feature
git checkout -b feature-advanced-alerts

# Make your changes
# ...

# Commit changes
git add .
git commit -m "Add: Advanced price alert system"

# Push to new branch
git push -u origin feature-advanced-alerts

# When ready, merge to main on GitHub via Pull Request
# Or merge locally:
git checkout main
git merge feature-advanced-alerts
git push
```

---

## 🔍 Useful Git Commands

### Checking Status

```bash
# See what files changed
git status

# See actual code changes
git diff

# See changes for specific file
git diff app.py

# See commit history
git log

# See compact commit history
git log --oneline

# See last 5 commits
git log -5 --oneline
```

### Undoing Changes

```bash
# Undo changes to a specific file (before commit)
git checkout -- app.py

# Undo all uncommitted changes
git reset --hard

# Undo last commit but keep changes
git reset --soft HEAD~1

# Undo last commit and discard changes
git reset --hard HEAD~1

# Undo a pushed commit (creates new commit)
git revert HEAD
git push
```

### Branch Management

```bash
# See all branches
git branch

# Create new branch
git checkout -b new-feature

# Switch to existing branch
git checkout main

# Delete local branch
git branch -d feature-name

# Delete remote branch
git push origin --delete feature-name
```

### Syncing with GitHub

```bash
# Pull latest changes from GitHub
git pull

# Pull and rebase
git pull --rebase

# Fetch changes without merging
git fetch

# See remote repository info
git remote -v
```

---

## 🚨 Troubleshooting

### Problem: "Authentication failed"

**Solution:**

```bash
# Re-authenticate with GitHub CLI
gh auth login

# Or update remote URL with token
git remote set-url origin https://YOUR_TOKEN@github.com/mas050/technical-analysis-pro.git
```

### Problem: "Your branch is behind 'origin/main'"

**Solution:**

```bash
# Pull latest changes first
git pull

# Then push your changes
git push
```

### Problem: "Merge conflict"

**Solution:**

```bash
# Pull changes
git pull

# Open conflicted files and resolve conflicts
# Look for <<<<<<< HEAD markers

# After resolving, add files
git add .

# Commit the merge
git commit -m "Merge: Resolved conflicts"

# Push
git push
```

### Problem: Accidentally committed sensitive data (.env file)

**Solution:**

```bash
# Remove from git but keep locally
git rm --cached .env

# Commit the removal
git commit -m "Remove: Sensitive .env file from repository"

# Push
git push

# Make sure .env is in .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Update: Add .env to gitignore"
git push
```

### Problem: Want to undo a pushed commit

**Solution:**

```bash
# Revert the commit (safest - creates new commit)
git revert HEAD
git push

# Or reset (dangerous - rewrites history)
git reset --hard HEAD~1
git push --force
```

### Problem: Pushed to wrong branch

**Solution:**

```bash
# Switch to correct branch
git checkout correct-branch

# Cherry-pick the commit
git cherry-pick commit-hash

# Push to correct branch
git push
```

---

## 📊 Best Practices

### ✅ DO:

- **Commit often** - Small, focused commits are better than large ones
- **Write clear commit messages** - Future you will thank you
- **Pull before you push** - Avoid conflicts
- **Review changes before committing** - Use `git diff`
- **Use branches for big features** - Keep main stable
- **Keep .gitignore updated** - Never commit secrets or generated files

### ❌ DON'T:

- **Don't commit secrets** - API keys, passwords, tokens
- **Don't commit generated files** - `venv/`, `node_modules/`, `__pycache__/`
- **Don't force push to main** - Unless you really know what you're doing
- **Don't commit broken code** - Test before committing
- **Don't use vague commit messages** - "fixed stuff" is not helpful

---

## 🎯 Quick Reference

### Daily Workflow

```bash
# 1. Check status
git status

# 2. See changes
git diff

# 3. Add changes
git add .

# 4. Commit
git commit -m "Type: Description"

# 5. Push
git push
```

### Common Commands

| Task | Command |
|------|---------|
| Check status | `git status` |
| See changes | `git diff` |
| Add all files | `git add .` |
| Add specific file | `git add filename` |
| Commit | `git commit -m "message"` |
| Push | `git push` |
| Pull | `git pull` |
| View history | `git log --oneline` |
| Undo changes | `git reset --hard` |
| Create branch | `git checkout -b branch-name` |

---

## 🔄 Complete Example Workflow

### Making Changes and Updating GitHub

```bash
# 1. Navigate to project
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website

# 2. Make your code changes in your editor
# ... edit files ...

# 3. Check what changed
git status
git diff

# 4. Add changes
git add .

# 5. Commit with clear message
git commit -m "Update: Improved error handling in analysis endpoint

- Added try-catch blocks for API calls
- Better error messages for users
- Logging for debugging"

# 6. Push to GitHub
git push

# 7. Verify on GitHub
# Visit: https://github.com/mas050/technical-analysis-pro
```

---

## 📝 Commit Message Templates

### Bug Fix

```bash
git commit -m "Fix: [Brief description]

[Detailed explanation of the bug and how it was fixed]"
```

### New Feature

```bash
git commit -m "Add: [Feature name]

[Description of what the feature does and why it was added]"
```

### Update/Improvement

```bash
git commit -m "Update: [What was improved]

[Details about the improvements]"
```

### Documentation

```bash
git commit -m "Docs: [What documentation was changed]

[Brief description of changes]"
```

---

## 🎓 Learning Resources

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Interactive Git Tutorial**: https://learngitbranching.js.org/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

---

## 💡 Pro Tips

### Tip 1: Use Git Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --oneline --graph --decorate --all
```

Then use:
```bash
git st          # instead of git status
git co main     # instead of git checkout main
git visual      # see pretty commit graph
```

### Tip 2: Set Up Git Editor

```bash
# Use VS Code as git editor
git config --global core.editor "code --wait"

# Or use nano
git config --global core.editor "nano"
```

### Tip 3: Colorful Git Output

```bash
git config --global color.ui auto
```

### Tip 4: See What Will Be Pushed

```bash
# Before pushing, see what commits will be pushed
git log origin/main..HEAD

# Or see the diff
git diff origin/main..HEAD
```

### Tip 5: Stash Changes Temporarily

```bash
# Save changes without committing
git stash

# Do something else (switch branches, pull, etc.)

# Restore changes
git stash pop
```

---

## ✅ Checklist for Each Update

Before pushing to GitHub:

- [ ] Code works and is tested
- [ ] No sensitive data (API keys, passwords) in code
- [ ] Reviewed changes with `git diff`
- [ ] Clear commit message written
- [ ] `.gitignore` is up to date
- [ ] No unnecessary files being committed

---

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Push your project to GitHub
- ✅ Make updates and push changes
- ✅ Manage your repository effectively
- ✅ Troubleshoot common issues

**Happy coding!** 🚀

---

## 📞 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Use `git status` to see current state
3. Use `git log` to see commit history
4. Search GitHub documentation
5. Check Stack Overflow for specific errors

**Remember:** Git is powerful but forgiving. Most mistakes can be undone! 💪
