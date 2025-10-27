# 🚀 Quick Raspberry Pi Setup Guide

Minimal setup guide to deploy Technical Analysis Pro on your Raspberry Pi with auto-start.

---

## Prerequisites

✅ Raspberry Pi with Tailscale already running  
✅ SSH access to your Pi  
✅ Location: `/home/sebastien/Python`

---

## Step 1: SSH into Your Raspberry Pi

```bash
ssh sebastien@<your-pi-tailscale-ip>
```

Or if you set a hostname:
```bash
ssh sebastien@raspberry-pi
```

---

## Step 2: Navigate to Python Directory

```bash
cd /home/sebastien/Python
```

---

## Step 3: Clone the Repository

```bash
git clone https://github.com/mas050/technical-analysis-pro.git
cd technical-analysis-pro
```

---

## Step 4: Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip \
    libjpeg-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libopenjp2-7 libtiff-dev libwebp-dev
```

**Note:** Changed `libtiff5` to `libtiff-dev` for newer Raspberry Pi OS versions.

---

## Step 5: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** This may take 10-15 minutes on Raspberry Pi.

---

## Step 6: Create Environment File (Optional)

```bash
nano .env
```

Add your API key if you have one:

```bash
GEMINI_API_KEY=your_api_key_here
```

Save: `Ctrl+X`, then `Y`, then `Enter`

---

## Step 7: Update app.py for Network Access

```bash
nano app.py
```

Find the last line (around line 357):
```python
socketio.run(app, debug=False, host='127.0.0.1', port=5001)
```

Change to:
```python
socketio.run(app, debug=False, host='0.0.0.0', port=5001)
```

Save: `Ctrl+X`, then `Y`, then `Enter`

---

## Step 8: Test the Application

```bash
python app.py
```

You should see:
```
🚀 Technical Analysis Web Application Starting...
📊 Server running at: http://localhost:5001
```

Press `Ctrl+C` to stop.

If it works, proceed to auto-start setup.

---

## Step 9: Create Systemd Service

```bash
sudo nano /etc/systemd/system/technical-analysis.service
```

Paste this configuration:

```ini
[Unit]
Description=Technical Analysis Pro Web Application
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=sebastien
Group=sebastien
WorkingDirectory=/home/sebastien/Python/technical-analysis-pro
Environment="PATH=/home/sebastien/Python/technical-analysis-pro/venv/bin"
EnvironmentFile=-/home/sebastien/Python/technical-analysis-pro/.env
ExecStart=/home/sebastien/Python/technical-analysis-pro/venv/bin/python /home/sebastien/Python/technical-analysis-pro/app.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/technical-analysis/app.log
StandardError=append:/var/log/technical-analysis/error.log

[Install]
WantedBy=multi-user.target
```

Save: `Ctrl+X`, then `Y`, then `Enter`

---

## Step 10: Create Log Directory

```bash
sudo mkdir -p /var/log/technical-analysis
sudo chown sebastien:sebastien /var/log/technical-analysis
```

---

## Step 11: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable technical-analysis.service

# Start the service now
sudo systemctl start technical-analysis.service

# Check status
sudo systemctl status technical-analysis.service
```

You should see: **active (running)** in green ✅

---

## Step 12: Access Your Application

From any device on your Tailscale network:

```
http://<your-pi-tailscale-ip>:5001
```

Or if you have a hostname:
```
http://raspberry-pi:5001
```

---

## ✅ Done!

Your Technical Analysis Pro is now:
- ✅ Running on your Raspberry Pi
- ✅ Auto-starts on boot/reboot
- ✅ Accessible via Tailscale from any device

---

## 🔧 Management Commands

### View Logs

```bash
# Real-time logs
tail -f /var/log/technical-analysis/app.log

# Error logs
tail -f /var/log/technical-analysis/error.log

# Or use journalctl
sudo journalctl -u technical-analysis.service -f
```

### Control Service

```bash
# Stop
sudo systemctl stop technical-analysis.service

# Start
sudo systemctl start technical-analysis.service

# Restart
sudo systemctl restart technical-analysis.service

# Check status
sudo systemctl status technical-analysis.service
```

### Update Application

```bash
# Stop service
sudo systemctl stop technical-analysis.service

# Navigate to directory
cd /home/sebastien/Python/technical-analysis-pro

# Pull latest changes
git pull

# Update dependencies if needed
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start technical-analysis.service
```

---

## 🚨 Troubleshooting

### Service won't start

```bash
# Check logs
sudo journalctl -u technical-analysis.service -n 50

# Test manually
cd /home/sebastien/Python/technical-analysis-pro
source venv/bin/activate
python app.py
```

### Can't access from other devices

```bash
# Check if service is running
sudo systemctl status technical-analysis.service

# Check if port is listening
sudo netstat -tulpn | grep 5001

# Check Tailscale
tailscale status
```

### Port already in use

```bash
# Find what's using port 5001
sudo lsof -i :5001

# Change port in app.py if needed
nano app.py
# Change port=5001 to port=5002 (or any available port)
```

---

## 📊 Quick Reference

| Task | Command |
|------|---------|
| Start service | `sudo systemctl start technical-analysis.service` |
| Stop service | `sudo systemctl stop technical-analysis.service` |
| Restart service | `sudo systemctl restart technical-analysis.service` |
| View logs | `tail -f /var/log/technical-analysis/app.log` |
| Check status | `sudo systemctl status technical-analysis.service` |
| Update app | `git pull` then restart service |

---

## 🎯 Total Setup Time

- **Steps 1-6:** ~15-20 minutes (mostly waiting for pip install)
- **Steps 7-11:** ~5 minutes
- **Total:** ~25 minutes

That's it! Your app is now running 24/7 on your Raspberry Pi! 🎉
