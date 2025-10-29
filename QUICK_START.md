# Quick Start Guide

## 🚀 Development on Mac

### Start Development Server (Hot Reload):
```bash
# Terminal 1 - Backend
# Kill any existing process on port 5001
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website_Enhancements
python app.py

# Terminal 2 - Frontend (Development Mode)
# Kill any existing process on port 3000
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website_Enhancements/frontend
npm start
```

**Access:** http://localhost:3000 (auto-opens)
- ✅ Hot reload enabled
- ✅ Uses `http://localhost:5001` API
- ✅ Fast development

### Quick One-Liner (Kill & Start):
```bash
# Backend
lsof -ti:5001 | xargs kill -9 2>/dev/null || true && python app.py

# Frontend
lsof -ti:3000 | xargs kill -9 2>/dev/null || true && cd frontend && npm start
```

---

## 🥧 Deploy to Raspberry Pi

### On Raspberry Pi:
```bash
# Pull latest code
git pull

# Build production frontend
cd frontend
npm run build

# Start backend
cd ..
python app.py
```

**Access:** http://100.76.210.77:5001 (via Tailscale)
- ✅ Optimized build
- ✅ Uses `http://100.76.210.77:5001` API
- ✅ Accessible from any device on Tailscale

---

## 🔄 Workflow

### Mac:
1. Make changes
2. Test with `npm start`
3. Commit & push

### Raspberry Pi:
1. `git pull`
2. `cd frontend && npm run build`
3. `python app.py`

**No manual URL changes needed!** 🎉

---

## 📝 Environment Files

- `.env.development` → Mac (localhost)
- `.env.production` → Raspberry Pi (Tailscale IP)

Both are committed to Git - automatic switching!
