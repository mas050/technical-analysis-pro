# 🔄 Quick Update Workflow

**Fast guide for updating your app from Mac to Raspberry Pi.**

---

## 📤 Part 1: Push Changes from Mac

### Step 1: Check What Changed

```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
git status
```

### Step 2: Add and Commit Changes

```bash
# Add all changes
git add .

# Or add specific files
git add app.py frontend/src/App.js

# Commit with clear message
git commit -m "Description of your changes"
```

### Step 3: Push to GitHub

```bash
git push
```

---

## 📥 Part 2: Update Raspberry Pi

### Quick Commands (Copy & Paste)

```bash
sudo systemctl stop technical-analysis.service
cd /home/sebastien/Python/technical-analysis-pro
git stash
git pull
cd frontend
npm run build
cd ..
sudo systemctl start technical-analysis.service
sudo systemctl status technical-analysis.service
```

### Step-by-Step Explanation

```bash
# 1. Stop the service
sudo systemctl stop technical-analysis.service

# 2. Navigate to project
cd /home/sebastien/Python/technical-analysis-pro

# 3. Stash any local changes (if needed)
git stash

# 4. Pull latest changes from GitHub
git pull

# 5. Rebuild frontend (if you changed frontend files)
cd frontend
npm run build
cd ..

# 6. Restart the service
sudo systemctl start technical-analysis.service

# 7. Verify it's running
sudo systemctl status technical-analysis.service
```

---

## 🎯 When to Rebuild Frontend

**Rebuild frontend if you changed:**
- ✅ Any file in `frontend/src/`
- ✅ `frontend/package.json`
- ✅ React components, styles, or logic

**Skip frontend rebuild if you only changed:**
- ❌ Backend Python files (`app.py`, `technical_analysis.py`, etc.)
- ❌ `requirements.txt`
- ❌ Documentation files (`.md`)

### Backend-Only Update (Faster)

```bash
sudo systemctl stop technical-analysis.service
cd /home/sebastien/Python/technical-analysis-pro
git stash
git pull
sudo systemctl start technical-analysis.service
```

⏱️ **Time saved:** ~15 minutes (no npm build)

---

## 🔍 Verify Changes

### Check Service Status

```bash
sudo systemctl status technical-analysis.service
```

Should show: **● active (running)** in green

### View Logs

```bash
# Real-time logs
sudo journalctl -u technical-analysis.service -f

# Last 50 lines
sudo journalctl -u technical-analysis.service -n 50

# Application logs
tail -f /var/log/technical-analysis/app.log
```

### Test the App

Open in browser:
```
http://100.76.210.77:5001
```

Clear browser cache if needed:
- **Hard refresh:** `Ctrl+Shift+R` or `Cmd+Shift+R`
- **Clear cache:** `Ctrl+Shift+Delete` or `Cmd+Shift+Delete`

---

## 🚨 Troubleshooting

### Git Pull Fails: "Your local changes would be overwritten"

```bash
# Stash local changes
git stash

# Pull updates
git pull

# If you want to keep local changes
git stash pop
```

### Service Won't Start After Update

```bash
# Check error logs
cat /var/log/technical-analysis/error.log

# Run manually to see errors
cd /home/sebastien/Python/technical-analysis-pro
source venv/bin/activate
python app.py
```

### Frontend Build Fails

```bash
# Clean and reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Python Dependencies Changed

```bash
# Update Python packages
cd /home/sebastien/Python/technical-analysis-pro
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Find what's using the port
sudo lsof -i :5001

# Kill the process (if needed)
sudo kill -9 <PID>

# Or restart the Pi
sudo reboot
```

---

## 📊 Complete Update Workflow

### Scenario 1: Backend Changes Only

**On Mac:**
```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
git add app.py technical_analysis.py
git commit -m "Fix: Improved error handling"
git push
```

**On Pi:**
```bash
sudo systemctl stop technical-analysis.service
cd /home/sebastien/Python/technical-analysis-pro
git stash && git pull
sudo systemctl start technical-analysis.service
```

⏱️ **Total time:** ~2 minutes

---

### Scenario 2: Frontend Changes Only

**On Mac:**
```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
git add frontend/src/
git commit -m "Update: Improved UI styling"
git push
```

**On Pi:**
```bash
sudo systemctl stop technical-analysis.service
cd /home/sebastien/Python/technical-analysis-pro
git stash && git pull
cd frontend && npm run build && cd ..
sudo systemctl start technical-analysis.service
```

⏱️ **Total time:** ~15 minutes (npm build)

---

### Scenario 3: Both Backend and Frontend Changes

**On Mac:**
```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
git add .
git commit -m "Update: Multiple improvements"
git push
```

**On Pi:**
```bash
sudo systemctl stop technical-analysis.service
cd /home/sebastien/Python/technical-analysis-pro
git stash && git pull
cd frontend && npm run build && cd ..
sudo systemctl start technical-analysis.service
```

⏱️ **Total time:** ~15 minutes

---

### Scenario 4: New Python Dependencies

**On Mac:**
```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
# Add new package to requirements.txt
git add requirements.txt
git commit -m "Add: New dependency for feature X"
git push
```

**On Pi:**
```bash
sudo systemctl stop technical-analysis.service
cd /home/sebastien/Python/technical-analysis-pro
git stash && git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl start technical-analysis.service
```

⏱️ **Total time:** ~5-10 minutes (depending on package)

---

## 💡 Pro Tips

### 1. Create an Update Script

Save this as `update.sh` on your Raspberry Pi:

```bash
#!/bin/bash
echo "🛑 Stopping service..."
sudo systemctl stop technical-analysis.service

echo "📥 Pulling updates..."
cd /home/sebastien/Python/technical-analysis-pro
git stash
git pull

echo "🏗️  Building frontend..."
cd frontend
npm run build
cd ..

echo "🚀 Starting service..."
sudo systemctl start technical-analysis.service

echo "✅ Update complete!"
sudo systemctl status technical-analysis.service
```

Make it executable:
```bash
chmod +x update.sh
```

Run it:
```bash
./update.sh
```

### 2. Check Before Pushing

Always test locally on Mac before pushing:

```bash
# Test backend
python app.py

# Test frontend
cd frontend
npm start
```

### 3. Use Descriptive Commit Messages

Good examples:
- ✅ `Fix: Resolved matplotlib crash on background threads`
- ✅ `Add: Support for cryptocurrency analysis`
- ✅ `Update: Improved chart colors and styling`
- ✅ `Remove: Deprecated API endpoint`

Bad examples:
- ❌ `update`
- ❌ `fix stuff`
- ❌ `changes`

### 4. Keep a Changelog

Create `CHANGELOG.md` to track major changes:

```markdown
# Changelog

## [1.1.0] - 2025-10-27
### Changed
- Removed "Ultimate" from report title
- Changed robot icon to sparkle icon
- Updated API URLs to use environment variables

## [1.0.0] - 2025-10-27
### Added
- Initial release
- 50+ technical indicators
- AI-powered insights
```

---

## 🎯 Quick Reference

| Task | Mac Command | Pi Command |
|------|-------------|------------|
| Check changes | `git status` | `git status` |
| Add all files | `git add .` | - |
| Commit | `git commit -m "msg"` | - |
| Push | `git push` | - |
| Pull | - | `git pull` |
| Stop service | - | `sudo systemctl stop technical-analysis.service` |
| Start service | - | `sudo systemctl start technical-analysis.service` |
| Restart service | - | `sudo systemctl restart technical-analysis.service` |
| View logs | - | `sudo journalctl -u technical-analysis.service -f` |
| Build frontend | `npm run build` | `npm run build` |

---

## ⚡ Super Quick Update (One-Liners)

### Mac to GitHub

```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website && git add . && git commit -m "Update" && git push
```

### Pi Update (Backend Only)

```bash
sudo systemctl stop technical-analysis.service && cd /home/sebastien/Python/technical-analysis-pro && git stash && git pull && sudo systemctl start technical-analysis.service
```

### Pi Update (With Frontend)

```bash
sudo systemctl stop technical-analysis.service && cd /home/sebastien/Python/technical-analysis-pro && git stash && git pull && cd frontend && npm run build && cd .. && sudo systemctl start technical-analysis.service
```

---

## 📝 Update Checklist

Before pushing to GitHub:

- [ ] Tested changes locally on Mac
- [ ] All files saved
- [ ] Commit message is descriptive
- [ ] No sensitive data (API keys, passwords) in code

After updating Pi:

- [ ] Service started successfully
- [ ] No errors in logs
- [ ] App accessible from browser
- [ ] Features work as expected
- [ ] Browser cache cleared if needed

---

## 🎉 You're Done!

Your app is now updated and running on the Raspberry Pi! 🚀

**Access it at:** `http://100.76.210.77:5001`

---

## 📞 Need Help?

If something goes wrong:

1. Check service status: `sudo systemctl status technical-analysis.service`
2. View error logs: `cat /var/log/technical-analysis/error.log`
3. Run manually: `cd /home/sebastien/Python/technical-analysis-pro && source venv/bin/activate && python app.py`
4. Check this guide's troubleshooting section

Most issues are solved by:
- Clearing browser cache
- Restarting the service
- Rebuilding the frontend
- Checking error logs
