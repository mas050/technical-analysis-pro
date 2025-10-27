# 🚀 Setup Guide - Technical Analysis Pro

This guide will help you get the application up and running quickly.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.9 or higher**
   ```bash
   python3 --version
   ```

2. **Node.js 16 or higher**
   ```bash
   node --version
   ```

3. **npm (comes with Node.js)**
   ```bash
   npm --version
   ```

## 🔧 Installation Steps

### Step 1: Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 3: Set Up Environment Variables (Optional but Recommended)

For AI-powered insights, you'll need a Google Gemini API key:

1. Get your free API key at [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set the environment variable:

   **macOS/Linux:**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

   **Windows:**
   ```cmd
   set GEMINI_API_KEY=your_api_key_here
   ```

   **Or create a `.env` file in the root directory:**
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## 🎯 Running the Application

### Option 1: Quick Start (Development Mode)

Use the provided startup script:

```bash
./start.sh
```

This will:
- Activate the virtual environment
- Install/update dependencies
- Start the Flask backend on port 5000
- Start the React frontend on port 3000
- Open your browser automatically

### Option 2: Manual Start (Development Mode)

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Then open your browser to `http://localhost:3000`

### Option 3: Production Mode

Build and run the production version:

```bash
./start_production.sh
```

Or manually:

```bash
# Build frontend
cd frontend
npm run build
cd ..

# Run production server
source venv/bin/activate
python app.py
```

Then open your browser to `http://localhost:5000`

## 🌐 Accessing the Application

- **Development Frontend**: http://localhost:3000
- **Production/Backend**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📱 Using the Application

### 1. Landing Page
- Select a symbol (stock, crypto, or commodity)
- Choose date range (default: 12 months)
- Optionally add your Gemini API key
- Click "Generate Analysis"

### 2. Progress Screen
- Watch real-time progress updates
- See which analysis steps are being performed
- Typical analysis takes 30-60 seconds

### 3. Report Viewer
- View comprehensive HTML report
- Download report for offline viewing
- Share results
- Start new analysis

## 🔍 Example Symbols to Try

### Stocks
- `AAPL` - Apple Inc.
- `GOOGL` - Alphabet Inc.
- `MSFT` - Microsoft
- `TSLA` - Tesla
- `NVDA` - NVIDIA

### Cryptocurrencies
- `BTC-USD` - Bitcoin
- `ETH-USD` - Ethereum
- `BNB-USD` - Binance Coin
- `SOL-USD` - Solana

### Commodities
- `GC=F` - Gold Futures
- `SI=F` - Silver Futures
- `CL=F` - Crude Oil Futures

### Indices
- `^GSPC` - S&P 500
- `^DJI` - Dow Jones
- `^IXIC` - NASDAQ

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 or 3000 is already in use:

**Backend (port 5000):**
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9
```

**Frontend (port 3000):**
```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9
```

### Module Not Found Errors

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Build Errors

Clear cache and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### WebSocket Connection Issues

Make sure both backend and frontend are running. The frontend needs to connect to the backend's WebSocket endpoint.

### Charts Not Displaying

Ensure the `charts` directory exists and has write permissions:
```bash
mkdir -p charts reports
chmod 755 charts reports
```

## 📊 API Testing

You can test the API directly:

```bash
# Health check
curl http://localhost:5000/api/health

# Search symbols
curl http://localhost:5000/api/symbols/search?q=AAPL

# Start analysis (requires POST with JSON)
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","start_date":"2024-01-01","end_date":"2024-12-31"}'
```

## 🔒 Security Notes

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is already configured to exclude sensitive files
- API keys are never stored on the server
- All analysis sessions are isolated

## 📚 Additional Resources

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Google Gemini API](https://ai.google.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)

## 💡 Tips for Best Results

1. **Use Valid Symbols**: Make sure the symbol exists on Yahoo Finance
2. **Reasonable Date Ranges**: 1-5 years of data works best
3. **API Key**: Add your Gemini API key for AI insights
4. **Network Connection**: Ensure stable internet for data fetching
5. **Browser**: Use modern browsers (Chrome, Firefox, Safari, Edge)

## 🆘 Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure ports 5000 and 3000 are available
4. Check your internet connection
5. Review the troubleshooting section above

## 🎉 You're Ready!

Your Technical Analysis Pro application is now set up and ready to use. Start analyzing markets with professional-grade tools and AI-powered insights!

---

**Happy Trading! 📈**

*Remember: This tool is for educational purposes only. Always do your own research and consult with financial advisors before making investment decisions.*
