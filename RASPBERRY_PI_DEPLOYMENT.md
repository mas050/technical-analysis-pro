# 🥧 Raspberry Pi Deployment Guide with Tailscale

This guide will help you deploy the Technical Analysis Pro web application on your Raspberry Pi, making it accessible from any device on your Tailscale network.

## 📋 Prerequisites

- Raspberry Pi (3, 4, or 5 recommended)
- Raspberry Pi OS (64-bit recommended)
- Internet connection
- Tailscale account (free tier works great)
- At least 2GB RAM (4GB+ recommended)
- 8GB+ SD card space available

## 🎯 Overview

By the end of this guide, you'll have:
- ✅ Technical Analysis Pro running on your Raspberry Pi
- ✅ Auto-start on boot using systemd
- ✅ Access from any device via Tailscale
- ✅ Production-ready setup with proper logging

---

## Part 1: Initial Raspberry Pi Setup

### Step 1: Update Your Raspberry Pi

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Required System Packages

```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7 \
    libtiff5 \
    libwebp-dev
```

These packages are needed for:
- Python development
- Image processing (matplotlib charts)
- PDF generation (weasyprint)

---

## Part 2: Install and Configure Tailscale

### Step 1: Install Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### Step 2: Authenticate Tailscale

```bash
sudo tailscale up
```

This will give you a URL to visit in your browser. Log in with your Tailscale account to authenticate the device.

### Step 3: Get Your Tailscale IP

```bash
tailscale ip -4
```

**Save this IP address!** This is how you'll access your app from other devices.

Example output: `100.64.0.5`

### Step 4: Set a Tailscale Machine Name (Optional but Recommended)

In the Tailscale admin console (https://login.tailscale.com/admin/machines):
1. Find your Raspberry Pi
2. Click the three dots menu
3. Select "Edit machine name"
4. Set a friendly name like `raspberry-pi-analysis`

Now you can access it via: `http://raspberry-pi-analysis:5001`

---

## Part 3: Deploy the Application

### Step 1: Create Application Directory

```bash
# Create a dedicated directory for the app
sudo mkdir -p /opt/technical-analysis
sudo chown $USER:$USER /opt/technical-analysis
cd /opt/technical-analysis
```

### Step 2: Transfer Your Application Files

**Option A: Using Git (if you have a repository)**

```bash
cd /opt/technical-analysis
git clone <your-repo-url> .
```

**Option B: Using SCP from your Mac**

On your Mac, run:

```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
scp -r * pi@<raspberry-pi-ip>:/opt/technical-analysis/
```

Replace `<raspberry-pi-ip>` with your Raspberry Pi's local IP or Tailscale IP.

**Option C: Using rsync (recommended for updates)**

```bash
rsync -avz --exclude 'venv' --exclude 'node_modules' --exclude '__pycache__' \
  /Users/sebastien.martineau/Python/Technical_Analysis_Website/ \
  pi@<raspberry-pi-ip>:/opt/technical-analysis/
```

### Step 3: Set Up Python Virtual Environment

```bash
cd /opt/technical-analysis
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** This may take 10-20 minutes on a Raspberry Pi due to compiling some packages.

### Step 5: Create Necessary Directories

```bash
mkdir -p charts reports
chmod 755 charts reports
```

### Step 6: Test the Application

```bash
python app.py
```

You should see:
```
================================================================================
🚀 Technical Analysis Web Application Starting...
================================================================================

📊 Server running at: http://localhost:5001
```

Press `Ctrl+C` to stop it. If it works, proceed to the next section.

---

## Part 4: Configure for Production

### Step 1: Create Production Configuration

Create a production config file:

```bash
nano /opt/technical-analysis/.env
```

Add the following:

```bash
# Optional: Google Gemini API Key for AI insights
GEMINI_API_KEY=your_api_key_here

# Flask configuration
FLASK_ENV=production
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 2: Update app.py for Production

The app is already configured to bind to `127.0.0.1`. For Tailscale access, we need to bind to all interfaces:

```bash
nano /opt/technical-analysis/app.py
```

Find the last line:
```python
socketio.run(app, debug=False, host='127.0.0.1', port=5001)
```

Change it to:
```python
socketio.run(app, debug=False, host='0.0.0.0', port=5001)
```

This allows access from any network interface (including Tailscale).

Save and exit.

---

## Part 5: Create Systemd Service for Auto-Start

### Step 1: Create Service File

```bash
sudo nano /etc/systemd/system/technical-analysis.service
```

### Step 2: Add Service Configuration

Paste the following:

```ini
[Unit]
Description=Technical Analysis Pro Web Application
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/opt/technical-analysis
Environment="PATH=/opt/technical-analysis/venv/bin"
EnvironmentFile=-/opt/technical-analysis/.env
ExecStart=/opt/technical-analysis/venv/bin/python /opt/technical-analysis/app.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/technical-analysis/app.log
StandardError=append:/var/log/technical-analysis/error.log

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Important:** If your username is not `pi`, replace `User=pi` and `Group=pi` with your actual username.

Save and exit (`Ctrl+X`, `Y`, `Enter`).

### Step 3: Create Log Directory

```bash
sudo mkdir -p /var/log/technical-analysis
sudo chown $USER:$USER /var/log/technical-analysis
```

### Step 4: Reload Systemd and Enable Service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable technical-analysis.service

# Start the service now
sudo systemctl start technical-analysis.service
```

### Step 5: Check Service Status

```bash
sudo systemctl status technical-analysis.service
```

You should see:
```
● technical-analysis.service - Technical Analysis Pro Web Application
   Loaded: loaded (/etc/systemd/system/technical-analysis.service; enabled)
   Active: active (running) since ...
```

If it shows "active (running)" in green, you're good! ✅

### Step 6: View Logs

```bash
# View application logs
tail -f /var/log/technical-analysis/app.log

# View error logs
tail -f /var/log/technical-analysis/error.log

# Or use journalctl
sudo journalctl -u technical-analysis.service -f
```

---

## Part 6: Configure Firewall (Optional but Recommended)

### Step 1: Install UFW (if not already installed)

```bash
sudo apt install ufw -y
```

### Step 2: Configure Firewall Rules

```bash
# Allow SSH (important - don't lock yourself out!)
sudo ufw allow 22/tcp

# Allow the application port (only from Tailscale network)
sudo ufw allow from 100.64.0.0/10 to any port 5001

# Enable firewall
sudo ufw enable
```

### Step 3: Check Firewall Status

```bash
sudo ufw status
```

---

## Part 7: Access Your Application

### From Any Device on Your Tailscale Network:

**Option 1: Using Tailscale IP**

```
http://100.64.0.5:5001
```
(Replace with your actual Tailscale IP)

**Option 2: Using Machine Name**

```
http://raspberry-pi-analysis:5001
```
(Replace with your actual machine name)

### Test It:

1. Open the URL in your browser
2. You should see the Technical Analysis Pro landing page
3. Try running an analysis on AAPL
4. Verify everything works!

---

## Part 8: Useful Management Commands

### Service Management

```bash
# Start the service
sudo systemctl start technical-analysis.service

# Stop the service
sudo systemctl stop technical-analysis.service

# Restart the service
sudo systemctl restart technical-analysis.service

# Check status
sudo systemctl status technical-analysis.service

# View logs
sudo journalctl -u technical-analysis.service -f

# Disable auto-start
sudo systemctl disable technical-analysis.service

# Re-enable auto-start
sudo systemctl enable technical-analysis.service
```

### Application Logs

```bash
# View real-time logs
tail -f /var/log/technical-analysis/app.log

# View last 100 lines
tail -n 100 /var/log/technical-analysis/app.log

# View error logs
tail -f /var/log/technical-analysis/error.log

# Clear old logs (if they get too large)
sudo truncate -s 0 /var/log/technical-analysis/app.log
sudo truncate -s 0 /var/log/technical-analysis/error.log
```

### Update Application

```bash
# Stop the service
sudo systemctl stop technical-analysis.service

# Navigate to app directory
cd /opt/technical-analysis

# Pull latest changes (if using git)
git pull

# Or use rsync from your Mac
# rsync -avz --exclude 'venv' ... (see Part 3, Step 2)

# Update dependencies if needed
source venv/bin/activate
pip install -r requirements.txt

# Restart the service
sudo systemctl start technical-analysis.service
```

---

## Part 9: Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status technical-analysis.service

# View detailed logs
sudo journalctl -u technical-analysis.service -n 50

# Check if port is already in use
sudo lsof -i :5001

# Test running manually
cd /opt/technical-analysis
source venv/bin/activate
python app.py
```

### Can't Access from Other Devices

```bash
# Check if Tailscale is running
tailscale status

# Check if service is listening
sudo netstat -tulpn | grep 5001

# Check firewall
sudo ufw status

# Test from Raspberry Pi itself
curl http://localhost:5001/api/health
```

### Application Crashes

```bash
# View error logs
tail -n 100 /var/log/technical-analysis/error.log

# Check system resources
free -h
df -h

# Restart service
sudo systemctl restart technical-analysis.service
```

### Memory Issues

If your Raspberry Pi has limited RAM:

```bash
# Add swap space
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Port 5001 Already in Use

```bash
# Find what's using the port
sudo lsof -i :5001

# Kill the process (replace PID)
sudo kill -9 <PID>

# Or use a different port in app.py
```

---

## Part 10: Performance Optimization

### Step 1: Reduce Chart Quality for Faster Generation

Edit `visualization.py`:

```python
# Change DPI from 300 to 150 for faster generation
plt.savefig(filename, dpi=150, bbox_inches='tight')
```

### Step 2: Limit Historical Data Range

For faster analysis on Raspberry Pi, consider limiting to 1-2 years of data instead of 5 years.

### Step 3: Enable Log Rotation

```bash
sudo nano /etc/logrotate.d/technical-analysis
```

Add:

```
/var/log/technical-analysis/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## Part 11: Security Best Practices

### 1. Keep System Updated

```bash
# Run weekly
sudo apt update && sudo apt upgrade -y
```

### 2. Use Strong Tailscale ACLs

In Tailscale admin console, configure ACLs to restrict access to specific users/devices.

### 3. Regular Backups

```bash
# Backup application data
tar -czf ~/technical-analysis-backup-$(date +%Y%m%d).tar.gz \
  /opt/technical-analysis \
  --exclude='venv' \
  --exclude='__pycache__'
```

### 4. Monitor Logs

```bash
# Set up a cron job to check for errors
crontab -e

# Add:
0 * * * * grep -i error /var/log/technical-analysis/error.log | tail -n 10
```

---

## Part 12: Advanced Configuration

### Enable HTTPS (Optional)

If you want HTTPS access:

1. Install nginx as reverse proxy
2. Use Let's Encrypt with Tailscale certificates
3. Configure nginx to proxy to port 5001

### Multiple Instances

To run multiple instances on different ports:

1. Copy the service file: `technical-analysis-5002.service`
2. Change the port in app.py
3. Enable both services

### Resource Monitoring

Install monitoring tools:

```bash
sudo apt install htop iotop -y
```

Monitor while analysis is running:
```bash
htop
```

---

## 📊 Quick Reference Card

| Task | Command |
|------|---------|
| Start service | `sudo systemctl start technical-analysis.service` |
| Stop service | `sudo systemctl stop technical-analysis.service` |
| Restart service | `sudo systemctl restart technical-analysis.service` |
| View logs | `tail -f /var/log/technical-analysis/app.log` |
| Check status | `sudo systemctl status technical-analysis.service` |
| Access URL | `http://<tailscale-ip>:5001` |
| Tailscale IP | `tailscale ip -4` |
| Update app | Stop service → Update files → Start service |

---

## 🎉 Success Checklist

- [ ] Raspberry Pi updated and packages installed
- [ ] Tailscale installed and authenticated
- [ ] Application files transferred to `/opt/technical-analysis`
- [ ] Python dependencies installed in virtual environment
- [ ] Service file created and enabled
- [ ] Service starts successfully
- [ ] Can access from another device via Tailscale
- [ ] Analysis completes successfully
- [ ] Service auto-starts after reboot

---

## 🆘 Getting Help

If you encounter issues:

1. Check the logs: `sudo journalctl -u technical-analysis.service -n 100`
2. Verify Tailscale: `tailscale status`
3. Test manually: `cd /opt/technical-analysis && source venv/bin/activate && python app.py`
4. Check resources: `free -h` and `df -h`

---

## 🔄 Updating the Application

When you make changes on your Mac:

```bash
# On your Mac
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
rsync -avz --exclude 'venv' --exclude 'node_modules' --exclude '__pycache__' \
  ./ pi@<tailscale-ip>:/opt/technical-analysis/

# On Raspberry Pi
sudo systemctl restart technical-analysis.service
```

---

## 🎯 Final Notes

- **Performance**: First analysis may be slow (30-90 seconds) on Raspberry Pi
- **Memory**: 4GB RAM recommended for smooth operation
- **Storage**: Charts and reports will accumulate - clean periodically
- **Updates**: Keep both Raspberry Pi OS and Python packages updated
- **Backup**: Regular backups recommended before major updates

**Your Technical Analysis Pro is now running 24/7 on your Raspberry Pi!** 🚀

Access it from anywhere on your Tailscale network at:
```
http://<your-tailscale-ip>:5001
```

Enjoy your always-available technical analysis platform! 📊📈
