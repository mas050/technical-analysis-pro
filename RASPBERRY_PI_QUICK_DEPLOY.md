# 🥧 Raspberry Pi Quick Deploy Guide

**Deploy any Python web app to Raspberry Pi with Tailscale in under 30 minutes.**

---

## 📋 Prerequisites

✅ Raspberry Pi with Tailscale already running  
✅ SSH access to your Pi  
✅ GitHub repository with your code  
✅ Base location: `/home/sebastien/Python`

---

## 🚀 Part 1: One-Time Raspberry Pi Setup (Do Once)

### Install Node.js (if not already installed)

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Install System Dependencies for Python Projects

```bash
sudo apt update
sudo apt install -y \
    python3-venv python3-pip \
    libjpeg-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libopenjp2-7 libtiff-dev libwebp-dev \
    build-essential
```

### Get Your Tailscale IP

```bash
tailscale ip -4
```

**Save this IP!** Example: `100.76.210.77`

---

## 🎯 Part 2: Deploy New App (Repeat for Each App)

### Step 1: SSH into Raspberry Pi

```bash
ssh sebastien@<tailscale-ip>
```

### Step 2: Clone Repository

```bash
cd /home/sebastien/Python
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### Step 3: Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

⏱️ **Wait 10-15 minutes** for packages to install on Raspberry Pi.

### Step 4: Configure for Network Access

Edit `app.py`:

```bash
nano app.py
```

Find the last line and ensure it has:
```python
socketio.run(app, 
             debug=False, 
             host='0.0.0.0',              # Not 127.0.0.1!
             port=5001,                    # Or your chosen port
             allow_unsafe_werkzeug=True)   # Required!
```

### Step 5: Create Environment File (if needed)

```bash
nano .env
```

Add your API keys:
```bash
GEMINI_API_KEY=your_key_here
SECRET_KEY=your_secret_key
```

### Step 6: Build Frontend (if React app)

#### Create Missing Public Directory

```bash
mkdir -p frontend/public

cat > frontend/public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <title>Your App Name</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

cat > frontend/public/manifest.json << 'EOF'
{
  "short_name": "App",
  "name": "Your App Name",
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
EOF
```

#### Update API URLs

Get your Tailscale IP:
```bash
tailscale ip -4
```

Edit frontend files:

```bash
nano frontend/src/App.js
```

Replace ALL instances of `localhost:5001` with your Tailscale IP:
- Change: `http://localhost:5001` 
- To: `http://100.76.210.77:5001` (use your actual IP)

Do the same for:
```bash
nano frontend/src/components/ReportViewer.js
# Replace localhost:5001 with your Tailscale IP
```

#### Build Frontend

```bash
cd frontend
npm install  # Takes 5-10 minutes
npm run build  # Takes 10-15 minutes on Pi
cd ..
```

### Step 7: Test Manually

```bash
python app.py
```

You should see:
```
🚀 Technical Analysis Web Application Starting...
📊 Server running at: http://localhost:5001
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.1.XXX:5001
```

Press `Ctrl+C` to stop.

Test from another device:
```
http://<tailscale-ip>:5001
```

If it works, proceed to auto-start setup!

### Step 8: Create Systemd Service

Choose a service name (e.g., `technical-analysis`, `stock-analyzer`, etc.)

```bash
sudo nano /etc/systemd/system/YOUR-SERVICE-NAME.service
```

Paste this template (update the paths and names):

```ini
[Unit]
Description=Your App Description
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=sebastien
Group=sebastien
WorkingDirectory=/home/sebastien/Python/YOUR_REPO
Environment="PATH=/home/sebastien/Python/YOUR_REPO/venv/bin"
EnvironmentFile=-/home/sebastien/Python/YOUR_REPO/.env
ExecStart=/home/sebastien/Python/YOUR_REPO/venv/bin/python /home/sebastien/Python/YOUR_REPO/app.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/YOUR-SERVICE-NAME/app.log
StandardError=append:/var/log/YOUR-SERVICE-NAME/error.log

[Install]
WantedBy=multi-user.target
```

**Replace:**
- `YOUR-SERVICE-NAME` with your service name
- `YOUR_REPO` with your repository name
- `Your App Description` with a description

Save: `Ctrl+X`, `Y`, `Enter`

### Step 9: Create Log Directory

```bash
sudo mkdir -p /var/log/YOUR-SERVICE-NAME
sudo chown sebastien:sebastien /var/log/YOUR-SERVICE-NAME
```

### Step 10: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start
sudo systemctl enable YOUR-SERVICE-NAME.service

# Start now
sudo systemctl start YOUR-SERVICE-NAME.service

# Check status
sudo systemctl status YOUR-SERVICE-NAME.service
```

Should show: **● active (running)** in green ✅

### Step 11: Access Your App

From any device on Tailscale:
```
http://<tailscale-ip>:5001
```

---

## 🔧 Management Commands

### Control Service

```bash
# Start
sudo systemctl start YOUR-SERVICE-NAME.service

# Stop
sudo systemctl stop YOUR-SERVICE-NAME.service

# Restart
sudo systemctl restart YOUR-SERVICE-NAME.service

# Status
sudo systemctl status YOUR-SERVICE-NAME.service

# View logs
sudo journalctl -u YOUR-SERVICE-NAME.service -f
```

### Update Application

```bash
# Stop service
sudo systemctl stop YOUR-SERVICE-NAME.service

# Pull updates
cd /home/sebastien/Python/YOUR_REPO
git pull

# Update Python dependencies if changed
source venv/bin/activate
pip install -r requirements.txt

# Rebuild frontend if changed
cd frontend
npm run build
cd ..

# Restart service
sudo systemctl start YOUR-SERVICE-NAME.service
```

### View Logs

```bash
# Application logs
tail -f /var/log/YOUR-SERVICE-NAME/app.log

# Error logs
tail -f /var/log/YOUR-SERVICE-NAME/error.log

# System logs
sudo journalctl -u YOUR-SERVICE-NAME.service -n 100
```

---

## 🚨 Troubleshooting

### Service Won't Start

```bash
# Check error logs
cat /var/log/YOUR-SERVICE-NAME/error.log

# Run manually to see errors
cd /home/sebastien/Python/YOUR_REPO
source venv/bin/activate
python app.py
```

### Common Errors & Fixes

#### Error: "RuntimeError: The Werkzeug web server is not designed to run in production"

**Fix:** Add to `app.py`:
```python
socketio.run(app, allow_unsafe_werkzeug=True)
```

#### Error: "NSException" or matplotlib crash

**Fix:** Add to top of any file using matplotlib:
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
```

#### Error: "Port already in use"

**Fix:** Change port in `app.py`:
```python
socketio.run(app, port=5002)  # Use different port
```

Then update systemd service and frontend URLs.

#### Error: "Could not find a required file: index.html"

**Fix:** Create `frontend/public/index.html` (see Step 6)

#### Error: "Network Error" from frontend

**Fix:** Update API URLs in frontend to use Tailscale IP (see Step 6)

### Can't Access from Other Devices

```bash
# Check if service is running
sudo systemctl status YOUR-SERVICE-NAME.service

# Check if port is listening
sudo netstat -tulpn | grep 5001

# Check Tailscale
tailscale status

# Test locally first
curl http://localhost:5001/api/health
```

---

## 📊 Quick Reference

| Task | Command |
|------|---------|
| Get Tailscale IP | `tailscale ip -4` |
| SSH to Pi | `ssh sebastien@<tailscale-ip>` |
| Start service | `sudo systemctl start SERVICE.service` |
| Stop service | `sudo systemctl stop SERVICE.service` |
| Restart service | `sudo systemctl restart SERVICE.service` |
| View logs | `tail -f /var/log/SERVICE/app.log` |
| Check status | `sudo systemctl status SERVICE.service` |
| Update app | Stop → `git pull` → Rebuild → Start |

---

## 🎯 Deployment Checklist

Before deploying:

- [ ] Repository pushed to GitHub
- [ ] `requirements.txt` is complete
- [ ] `app.py` has `host='0.0.0.0'`
- [ ] `app.py` has `allow_unsafe_werkzeug=True`
- [ ] Matplotlib uses `Agg` backend
- [ ] `.gitignore` excludes `venv/`, `node_modules/`, `.env`
- [ ] Frontend `public/` directory exists
- [ ] Frontend API URLs use Tailscale IP (not localhost)
- [ ] Port is not 5000 (use 5001+)

After deploying:

- [ ] Service starts successfully
- [ ] Can access from another device via Tailscale
- [ ] API endpoints work
- [ ] Frontend loads correctly
- [ ] Analysis/features work end-to-end
- [ ] Service survives reboot

---

## 🔄 Multiple Apps on Same Pi

You can run multiple apps on the same Raspberry Pi:

### Use Different Ports

```python
# App 1: port 5001
socketio.run(app, port=5001)

# App 2: port 5002
socketio.run(app, port=5002)

# App 3: port 5003
socketio.run(app, port=5003)
```

### Use Different Service Names

```bash
# App 1
sudo systemctl start technical-analysis.service

# App 2
sudo systemctl start stock-screener.service

# App 3
sudo systemctl start portfolio-tracker.service
```

### Access Different Apps

```
http://<tailscale-ip>:5001  # App 1
http://<tailscale-ip>:5002  # App 2
http://<tailscale-ip>:5003  # App 3
```

---

## ⚡ Performance Tips for Raspberry Pi

### 1. Reduce Chart Quality

```python
# In visualization.py
plt.savefig(filename, dpi=150)  # Not 300
```

### 2. Limit Data Range

```python
# Fetch less historical data
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')  # 1 year
# Instead of 5 years
```

### 3. Add Swap Space (if Pi has limited RAM)

```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### 4. Monitor Resources

```bash
# Install monitoring tools
sudo apt install htop

# Monitor while app runs
htop
```

---

## 🔒 Security Best Practices

### 1. Keep System Updated

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Use Tailscale ACLs

In Tailscale admin console, restrict access to specific users/devices.

### 3. Never Commit Secrets

```bash
# Always use .env files
echo ".env" >> .gitignore

# Use .env.example as template
cp .env .env.example
# Remove actual values from .env.example
git add .env.example
```

### 4. Regular Backups

```bash
# Backup your apps
tar -czf ~/backup-$(date +%Y%m%d).tar.gz \
  /home/sebastien/Python \
  --exclude='venv' \
  --exclude='node_modules' \
  --exclude='__pycache__'
```

---

## 📦 Template Files

### .gitignore Template

```
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Environment
.env
.env.local

# Node
node_modules/
npm-debug.log*

# Build
frontend/build/

# Generated files
charts/
reports/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### .env.example Template

```bash
# API Keys (Get your own keys)
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production

# Optional: Custom port
PORT=5001
```

---

## 🎓 Pro Tips

1. **Always test locally first** before deploying to Pi
2. **Use Tailscale IP in frontend** for remote access
3. **Create log directories** before starting services
4. **Check service status** after every change
5. **Keep GitHub repo updated** for easy redeployment
6. **Document your ports** if running multiple apps
7. **Monitor logs** when testing new features
8. **Backup before major updates**
9. **Test after Pi reboots** to verify auto-start
10. **Use systemd** - it's reliable and standard

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| One-time Pi setup | 5 minutes |
| Clone and setup Python | 15-20 minutes |
| Build frontend | 15-20 minutes |
| Create systemd service | 5 minutes |
| Test and verify | 5 minutes |
| **Total (first app)** | **45-55 minutes** |
| **Subsequent apps** | **30-40 minutes** |

---

## 🎉 Success!

Your app is now:
- ✅ Running 24/7 on Raspberry Pi
- ✅ Auto-starts on boot/reboot
- ✅ Accessible from any device via Tailscale
- ✅ Properly logged for debugging
- ✅ Easy to update via Git

**Access your app from anywhere:**
```
http://<tailscale-ip>:5001
```

Happy deploying! 🚀🥧
