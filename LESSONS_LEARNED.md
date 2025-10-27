# 🎓 Lessons Learned: Python to Professional Web App

**Critical lessons for converting Python scripts into production-ready web applications.**

---

## 🚨 Critical Issues & Solutions

### 1. Port Conflicts on macOS

**Problem:** Port 5000 is reserved by Apple's AirPlay Receiver on macOS Monterey and later.

**Solution:**
- Always use port 5001 or higher for Flask apps on macOS
- Test with `curl -v http://localhost:5000` to detect AirPlay conflicts
- Look for `Server: AirTunes/860.7.1` in response headers

**Code Fix:**
```python
socketio.run(app, host='0.0.0.0', port=5001)  # Not 5000!
```

---

### 2. Matplotlib Thread Safety

**Problem:** Matplotlib crashes with `NSException` when creating plots in background threads on macOS.

**Error:**
```
libc++abi: terminating due to uncaught exception of type NSException
```

**Solution:** Always set non-interactive backend BEFORE importing pyplot:

```python
import matplotlib
matplotlib.use('Agg')  # MUST be before pyplot import
import matplotlib.pyplot as plt
```

**Where to add:**
- `visualization.py` (top of file)
- `technical_analysis.py` (top of file)
- Any file that creates plots

---

### 3. Flask-SocketIO Production Warning

**Problem:** Newer Flask-SocketIO versions (6.0+) block Werkzeug in production.

**Error:**
```
RuntimeError: The Werkzeug web server is not designed to run in production.
Pass allow_unsafe_werkzeug=True to the run() method to disable this error.
```

**Solution:**
```python
socketio.run(app, 
             host='0.0.0.0', 
             port=5001, 
             allow_unsafe_werkzeug=True)  # Required for production
```

---

### 4. CORS Configuration

**Problem:** React frontend can't communicate with Flask backend due to CORS.

**Solution:** Proper CORS setup for development:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

socketio = SocketIO(app, cors_allowed_origins="*")
```

---

### 5. React Frontend API URLs

**Problem:** Frontend hardcoded to `localhost` doesn't work on remote devices.

**Critical Mistake:**
```javascript
// ❌ This only works on the same machine
axios.post('http://localhost:5001/api/analyze', data)
```

**Solutions:**

**Option A: Environment Variables (Best for production)**
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
axios.post(`${API_URL}/api/analyze`, data)
```

Then build with:
```bash
REACT_APP_API_URL=http://100.76.210.77:5001 npm run build
```

**Option B: Relative URLs with Proxy (Best for development)**
```javascript
// In package.json
"proxy": "http://localhost:5001"

// In code
axios.post('/api/analyze', data)  // Proxied automatically
```

**Option C: Hardcode for specific deployment**
```javascript
// Only if deploying to specific server
axios.post('http://100.76.210.77:5001/api/analyze', data)
```

---

### 6. Missing Frontend Public Directory

**Problem:** React build fails with "Could not find a required file: index.html"

**Solution:** Always include `public/` directory with:

**public/index.html:**
```html
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
```

**public/manifest.json:**
```json
{
  "short_name": "App",
  "name": "Your App Name",
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

---

### 7. Raspberry Pi Package Names

**Problem:** Package names differ between Ubuntu/Debian versions.

**Common Issues:**
```bash
# ❌ Fails on newer Raspberry Pi OS
sudo apt install libtiff5

# ✅ Works on Raspberry Pi OS Bookworm
sudo apt install libtiff-dev
```

**Always use `-dev` packages:**
- `libtiff-dev` (not `libtiff5`)
- `libjpeg-dev`
- `libfreetype6-dev`

---

## 📋 Pre-Flight Checklist

Before deploying ANY Python web app:

### Backend Checklist

- [ ] Port is NOT 5000 on macOS (use 5001+)
- [ ] Matplotlib uses `Agg` backend if creating plots
- [ ] Flask-SocketIO has `allow_unsafe_werkzeug=True`
- [ ] CORS is properly configured
- [ ] Host is `0.0.0.0` (not `127.0.0.1`) for network access
- [ ] All imports are at the top of files
- [ ] `.gitignore` excludes `venv/`, `__pycache__/`, `.env`
- [ ] `requirements.txt` is up to date

### Frontend Checklist

- [ ] `public/` directory exists with `index.html`
- [ ] API URLs use environment variables or proxy
- [ ] WebSocket URLs match API URLs
- [ ] `package.json` has correct dependencies
- [ ] `.gitignore` excludes `node_modules/`, `build/`

### Deployment Checklist

- [ ] System dependencies installed
- [ ] Python virtual environment created
- [ ] All Python packages installed
- [ ] Frontend built (`npm run build`)
- [ ] Systemd service file created
- [ ] Log directories created with correct permissions
- [ ] Service enabled for auto-start
- [ ] Firewall configured if needed

---

## 🏗️ Recommended Project Structure

```
project/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
├── technical_analysis.py           # Core business logic
├── visualization.py                # Chart generation
├── html_report.py                  # Report generation
├── frontend/                       # React frontend
│   ├── public/                     # Static files
│   │   ├── index.html             # Required!
│   │   ├── manifest.json          # PWA manifest
│   │   └── robots.txt             # SEO
│   ├── src/                       # React source
│   │   ├── index.js               # Entry point
│   │   ├── App.js                 # Main component
│   │   ├── App.css                # Styles
│   │   └── components/            # React components
│   ├── package.json               # Node dependencies
│   └── .env                       # Frontend env vars
├── charts/                        # Generated charts (gitignored)
├── reports/                       # Generated reports (gitignored)
└── venv/                          # Virtual environment (gitignored)
```

---

## 🔧 Essential Code Templates

### 1. Flask App Template

```python
"""
Flask Web Application Template
"""

import matplotlib
matplotlib.use('Agg')  # CRITICAL: Before any matplotlib imports

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# CORS Configuration
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# SocketIO Configuration
socketio = SocketIO(app, 
                    cors_allowed_origins="*",
                    async_mode='threading')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    os.makedirs('charts', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    socketio.run(app, 
                 debug=False, 
                 host='0.0.0.0', 
                 port=5001,
                 allow_unsafe_werkzeug=True)
```

### 2. React API Service Template

```javascript
// src/services/api.js
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

export const api = {
  async post(endpoint, data) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  },
  
  async get(endpoint) {
    const response = await fetch(`${API_URL}${endpoint}`);
    return response.json();
  }
};
```

### 3. Systemd Service Template

```ini
[Unit]
Description=Your App Name
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/app/venv/bin"
EnvironmentFile=-/path/to/app/.env
ExecStart=/path/to/app/venv/bin/python /path/to/app/app.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/your-app/app.log
StandardError=append:/var/log/your-app/error.log

[Install]
WantedBy=multi-user.target
```

---

## 🐛 Debugging Workflow

### 1. Backend Not Starting

```bash
# Check if port is in use
sudo lsof -i :5001

# Check for Python errors
python app.py

# Check system logs
sudo journalctl -u your-service.service -n 50
```

### 2. Frontend Not Connecting

```bash
# Test backend directly
curl http://localhost:5001/api/health

# Check browser console (F12)
# Look for CORS errors or network errors

# Verify API URL in frontend
grep -r "localhost:5001" frontend/src/
```

### 3. Service Crashes on Start

```bash
# View error logs
cat /var/log/your-app/error.log

# Run manually to see errors
cd /path/to/app
source venv/bin/activate
python app.py
```

---

## 📦 Dependency Management

### Python Requirements Template

```txt
# requirements.txt
Flask==3.0.0
flask-cors==4.0.0
flask-socketio==5.3.5
python-socketio==5.10.0

# Data & Analysis
yfinance==0.2.32
pandas==2.1.3
numpy==1.26.2
ta==0.11.0
scipy==1.11.4
scikit-learn==1.3.2

# Visualization
matplotlib==3.8.2
seaborn==0.13.0

# AI (Optional)
google-generativeai==0.3.1

# Web Server
gevent==23.9.1
gevent-websocket==0.10.1
```

### Package.json Template

```json
{
  "name": "your-app-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.0",
    "socket.io-client": "^4.7.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "proxy": "http://localhost:5001"
}
```

---

## ⚡ Performance Tips

### 1. Optimize Chart Generation

```python
# Use lower DPI for faster generation
plt.savefig(filename, dpi=150, bbox_inches='tight')  # Not 300

# Close figures to free memory
plt.close('all')
```

### 2. Cache API Responses

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_stock_data(symbol, start_date):
    # Expensive API call
    return yf.download(symbol, start=start_date)
```

### 3. Async Background Tasks

```python
import threading

def run_analysis_async(session_id, symbol):
    thread = threading.Thread(target=analyze, args=(session_id, symbol))
    thread.daemon = True
    thread.start()
```

---

## 🔒 Security Best Practices

### 1. Environment Variables

```python
# Never hardcode secrets
API_KEY = os.getenv('GEMINI_API_KEY')  # ✅
API_KEY = "hardcoded-key-123"          # ❌

# Use .env file
# .env
GEMINI_API_KEY=your_key_here
SECRET_KEY=random_secret_key
```

### 2. Input Validation

```python
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    # Validate inputs
    symbol = data.get('symbol', '').upper()
    if not symbol or len(symbol) > 10:
        return jsonify({'error': 'Invalid symbol'}), 400
    
    # Sanitize inputs
    symbol = ''.join(c for c in symbol if c.isalnum())
```

### 3. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze():
    # Your code here
```

---

## 📊 Monitoring & Logging

### Proper Logging Setup

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.info(f"Starting analysis for {symbol}")
logger.error(f"Failed to fetch data: {str(e)}")
```

---

## 🎯 Quick Wins

### Things That Save Hours

1. **Always test locally first** before deploying
2. **Use environment variables** for all configuration
3. **Set matplotlib backend early** in every file that uses it
4. **Test API endpoints with curl** before building frontend
5. **Check port availability** before starting services
6. **Use systemd for auto-start** instead of cron or screen
7. **Create log directories** before starting services
8. **Test on target platform** (Raspberry Pi) early
9. **Document API endpoints** as you build them
10. **Keep frontend and backend in sync** with version control

---

## 🚀 Deployment Speed Run

**From Python script to production in 30 minutes:**

1. **5 min:** Set up Flask app with CORS and SocketIO
2. **5 min:** Create React frontend with API service
3. **5 min:** Test locally (backend on 5001, frontend on 3000)
4. **5 min:** Build frontend (`npm run build`)
5. **5 min:** Create systemd service
6. **5 min:** Deploy to Raspberry Pi
7. **5 min:** Test and verify

**Total: 35 minutes** (if you follow this guide!)

---

## 💡 Key Takeaways

1. **Port 5000 is cursed on macOS** - always use 5001+
2. **Matplotlib needs `Agg` backend** for threads
3. **Flask-SocketIO needs `allow_unsafe_werkzeug=True`** in production
4. **CORS must be configured** for frontend-backend communication
5. **API URLs must be configurable** for remote access
6. **Public directory is required** for React builds
7. **Package names differ** between OS versions
8. **Test on target platform** early and often
9. **Systemd is the best** way to run services
10. **Documentation saves time** - write it as you go

---

## 📚 Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-SocketIO: https://flask-socketio.readthedocs.io/
- React Documentation: https://react.dev/
- Systemd Service Files: https://www.freedesktop.org/software/systemd/man/systemd.service.html
- Matplotlib Backends: https://matplotlib.org/stable/users/explain/backends.html

---

**Remember:** Every error is a lesson. Document what you learn! 🎓
