# Deployment Guide - Mac Development & Raspberry Pi Production

## 🎯 Overview

This guide explains how to develop on your Mac and deploy to your Raspberry Pi without manually changing URLs each time.

---

## 🔧 How It Works

The app now automatically detects the environment and uses the correct API URL:

### **Development (Mac)**
- Uses `npm start` (development mode)
- Reads `.env.development`
- API URL: `http://localhost:5001`

### **Production (Raspberry Pi)**
- Uses `npm run build` (production mode)
- Reads `.env.production`
- API URL: `http://100.76.210.77:5001` (your Tailscale IP)

### **Fallback Logic**
If no environment variable is set, the app automatically detects:
- **localhost/127.0.0.1** → Uses `http://localhost:5001`
- **Any other hostname** → Uses `http://{hostname}:5001`

---

## 📁 Environment Files

### `.env.development` (Mac Development)
```env
REACT_APP_API_URL=http://localhost:5001
```

### `.env.production` (Raspberry Pi)
```env
REACT_APP_API_URL=http://100.76.210.77:5001
```

**Both files are committed to Git** - No manual changes needed!

---

## 🖥️ Development Workflow (Mac)

### 1. **Start Development Server**
```bash
cd frontend
npm start
```
- Opens at `http://localhost:3000`
- Uses `.env.development`
- API calls go to `http://localhost:5001`
- Hot reload enabled

### 2. **Start Backend**
```bash
python app.py
```
- Runs on `http://localhost:5001`

### 3. **Make Changes**
- Edit React components
- Changes auto-reload
- Test locally

### 4. **Commit & Push**
```bash
git add .
git commit -m "Your changes"
git push origin main
```

---

## 🥧 Production Deployment (Raspberry Pi)

### 1. **Pull Latest Changes**
```bash
cd ~/Technical_Analysis_Website_Enhancements
git pull origin main
```

### 2. **Build Frontend**
```bash
cd frontend
npm run build
```
- Uses `.env.production`
- Creates optimized build
- API URL: `http://100.76.210.77:5001`

### 3. **Start Backend**
```bash
cd ..
python app.py
```
- Serves React build from `frontend/build`
- Runs on port 5001

### 4. **Access from Any Device**
- Via Tailscale: `http://100.76.210.77:5001`
- Via local network: `http://192.168.1.x:5001`

---

## 🔄 Complete Workflow Example

### On Mac (Development):
```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm start

# Make changes, test, commit
git add .
git commit -m "Added new feature"
git push
```

### On Raspberry Pi (Production):
```bash
# Pull changes
git pull

# Rebuild frontend
cd frontend
npm run build

# Restart backend
cd ..
pkill -f "python app.py"  # Stop old process
python app.py &           # Start new process
```

---

## 🚀 Quick Commands

### Mac Development:
```bash
# Start everything
python app.py &
cd frontend && npm start
```

### Raspberry Pi Production:
```bash
# Update and deploy
git pull && cd frontend && npm run build && cd .. && python app.py
```

---

## 🎨 Environment Variables Reference

| Variable | Development | Production |
|----------|-------------|------------|
| `REACT_APP_API_URL` | `http://localhost:5001` | `http://100.76.210.77:5001` |
| `NODE_ENV` | `development` | `production` |
| Build command | `npm start` | `npm run build` |
| Hot reload | ✅ Yes | ❌ No |
| Optimized | ❌ No | ✅ Yes |
| File size | Large | Small (minified) |

---

## 🔍 Troubleshooting

### Issue: "Can't connect to API"

**On Mac:**
```bash
# Check if backend is running
curl http://localhost:5001/api/health

# Should return: {"status":"healthy","timestamp":"..."}
```

**On Raspberry Pi:**
```bash
# Check if backend is running
curl http://100.76.210.77:5001/api/health

# Check from another device
curl http://100.76.210.77:5001/api/health
```

### Issue: "Wrong API URL in browser"

**Check console:**
1. Open DevTools (F12)
2. Look for: `API_URL: http://...`
3. Verify it matches your environment

**Force rebuild:**
```bash
cd frontend
rm -rf build node_modules/.cache
npm run build
```

### Issue: "Changes not showing on Raspberry Pi"

**Clear cache and rebuild:**
```bash
cd frontend
rm -rf build
npm run build
cd ..
# Restart Flask
pkill -f "python app.py"
python app.py
```

**Hard refresh browser:**
- Chrome/Firefox: `Ctrl+Shift+R` or `Cmd+Shift+R`
- Safari: `Cmd+Option+R`

---

## 📝 Git Workflow

### Files to Commit:
✅ `.env.development` - Mac localhost config
✅ `.env.production` - Raspberry Pi Tailscale config
✅ `src/` - All source code
✅ `public/` - Static assets
✅ `package.json` - Dependencies

### Files to Ignore (.gitignore):
❌ `build/` - Generated files
❌ `node_modules/` - Dependencies
❌ `.env.local` - Local overrides

---

## 🌐 Accessing the App

### From Mac (Development):
- **Frontend dev server**: `http://localhost:3000`
- **Backend API**: `http://localhost:5001`
- **API health**: `http://localhost:5001/api/health`

### From Raspberry Pi (Production):
- **Via Tailscale**: `http://100.76.210.77:5001`
- **Via local network**: `http://192.168.1.x:5001`
- **API health**: `http://100.76.210.77:5001/api/health`

### From Other Devices (via Tailscale):
- **Any device**: `http://100.76.210.77:5001`
- Works on phone, tablet, laptop
- Must be connected to Tailscale

---

## 🔐 Environment-Specific Settings

### Development (.env.development):
```env
REACT_APP_API_URL=http://localhost:5001
# Add more dev-specific vars here
```

### Production (.env.production):
```env
REACT_APP_API_URL=http://100.76.210.77:5001
# Add more prod-specific vars here
```

### Local Override (.env.local) - Optional:
```env
# This file is gitignored
# Use for personal overrides
REACT_APP_API_URL=http://custom-url:5001
```

**Priority:** `.env.local` > `.env.production` > `.env.development`

---

## 🎯 Best Practices

### 1. **Always Test Locally First**
```bash
# On Mac
npm start  # Test in development mode
npm run build  # Test production build
```

### 2. **Commit Both Environment Files**
- `.env.development` - For team members
- `.env.production` - For deployment

### 3. **Use Meaningful Commit Messages**
```bash
git commit -m "feat: Add glassmorphism to dropdown"
git commit -m "fix: Correct API URL for production"
git commit -m "docs: Update deployment guide"
```

### 4. **Keep Raspberry Pi Updated**
```bash
# Regular updates
git pull
cd frontend && npm run build
```

---

## 🚀 Automation Scripts

### Mac - Start Development:
Create `start-dev.sh`:
```bash
#!/bin/bash
python app.py &
cd frontend && npm start
```

### Raspberry Pi - Deploy:
Create `deploy.sh`:
```bash
#!/bin/bash
echo "Pulling latest changes..."
git pull

echo "Building frontend..."
cd frontend
npm run build

echo "Restarting backend..."
cd ..
pkill -f "python app.py"
nohup python app.py > app.log 2>&1 &

echo "Deployment complete!"
echo "Access at: http://100.76.210.77:5001"
```

Make executable:
```bash
chmod +x start-dev.sh deploy.sh
```

---

## ✅ Summary

### Development (Mac):
1. ✅ Uses `npm start`
2. ✅ Reads `.env.development`
3. ✅ API: `http://localhost:5001`
4. ✅ Hot reload enabled
5. ✅ No build needed

### Production (Raspberry Pi):
1. ✅ Uses `npm run build`
2. ✅ Reads `.env.production`
3. ✅ API: `http://100.76.210.77:5001`
4. ✅ Optimized & minified
5. ✅ Accessible via Tailscale

### No Manual Changes Needed! 🎉
- Commit both `.env` files to Git
- Mac automatically uses localhost
- Raspberry Pi automatically uses Tailscale IP
- One codebase, multiple environments

**Your workflow is now seamless!** 🚀
