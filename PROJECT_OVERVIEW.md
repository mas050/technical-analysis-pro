# 📊 Technical Analysis Pro - Project Overview

## 🎯 What This System Does

A professional web application that performs comprehensive technical analysis on stocks, cryptocurrencies, and commodities with AI-powered insights.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
│                  (React Frontend)                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Landing Page → Progress View → Report Viewer    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────┐
│                   FLASK BACKEND                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  REST API + WebSocket Server                     │  │
│  │  • /api/analyze - Start analysis                 │  │
│  │  • /api/report - Get results                     │  │
│  │  • WebSocket - Real-time progress               │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│              ANALYSIS ENGINE                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Technical Analysis System                       │  │
│  │  • Fetch market data (yfinance)                  │  │
│  │  • Calculate 50+ indicators                      │  │
│  │  • Generate predictions                          │  │
│  │  • Create visualizations                         │  │
│  │  • AI insights (Google Gemini)                   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                          │
│  • Yahoo Finance (Market Data)                          │
│  • Google Gemini AI (Insights)                          │
└─────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
Technical_Analysis_Website/
│
├── 🐍 Backend (Python/Flask)
│   ├── app.py                    # Main Flask application
│   ├── technical_analysis.py    # Core analysis engine
│   ├── html_report.py           # Report generator
│   ├── visualization.py         # Chart creation
│   └── requirements.txt         # Python dependencies
│
├── ⚛️ Frontend (React)
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── LandingPage.js   # Home page with form
│   │   │   ├── AnalysisProgress.js  # Progress tracker
│   │   │   └── ReportViewer.js  # Report display
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Global styles
│   │   └── index.js             # React entry point
│   └── package.json             # Node dependencies
│
├── 📄 Documentation
│   ├── README.md                # Main documentation
│   ├── SETUP_GUIDE.md          # Detailed setup
│   ├── QUICKSTART.md           # Quick start guide
│   └── PROJECT_OVERVIEW.md     # This file
│
├── 🚀 Scripts
│   ├── start.sh                # Development startup
│   └── start_production.sh     # Production startup
│
└── 📊 Generated (auto-created)
    ├── charts/                 # PNG charts
    └── reports/                # HTML reports
```

## 🔄 User Flow

```
1. LANDING PAGE
   ↓
   User enters:
   • Symbol (AAPL, BTC-USD, etc.)
   • Date range (default: 12 months)
   • API key (optional)
   ↓
   Click "Generate Analysis"

2. PROGRESS VIEW
   ↓
   Real-time updates:
   • Fetching data... (15%)
   • Calculating indicators... (40%)
   • Analyzing patterns... (70%)
   • Generating signals... (90%)
   • AI insights... (95%)
   • Complete! (100%)

3. REPORT VIEWER
   ↓
   Interactive HTML report:
   • Trading signals
   • Technical indicators
   • Charts & visualizations
   • AI insights
   • Risk metrics
   ↓
   Options:
   • Download report
   • Share results
   • Start new analysis
```

## 🎨 Key Features

### 1. Landing Page
- **Symbol Search**: Dropdown with popular symbols
- **Date Picker**: Custom date range selection
- **API Key Input**: Optional for AI insights
- **Responsive Design**: Works on all devices

### 2. Progress Tracking
- **Real-time Updates**: WebSocket connection
- **Visual Progress Bar**: Animated progress
- **Step-by-Step Status**: Current operation display
- **Milestone Indicators**: Key stages highlighted

### 3. Report Viewer
- **Embedded Report**: Full HTML report in iframe
- **Download Option**: Save report locally
- **Share Feature**: Share via native share API
- **Navigation**: Easy return to home

## 🔧 Technical Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Flask | Web framework |
| Flask-SocketIO | Real-time communication |
| yfinance | Market data API |
| pandas/numpy | Data processing |
| matplotlib/seaborn | Chart generation |
| ta | Technical indicators |
| scikit-learn | ML predictions |
| Google Gemini | AI insights |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| Socket.io-client | WebSocket client |
| Axios | HTTP requests |
| Lucide React | Icon library |
| CSS3 | Styling & animations |

## 📊 Analysis Pipeline

```
1. DATA ACQUISITION
   └─ Fetch historical + live data from Yahoo Finance

2. INDICATOR CALCULATION
   ├─ Trend: SMA, EMA, MACD, ADX, Ichimoku, PSAR
   ├─ Momentum: RSI, Stochastic, Williams %R, ROC
   ├─ Volatility: Bollinger Bands, ATR, Keltner
   └─ Volume: OBV, CMF, MFI, VWAP

3. ADVANCED ANALYSIS
   ├─ Fibonacci retracement levels
   ├─ Support & resistance (pivot points)
   ├─ Price predictions (linear regression)
   └─ Risk metrics (Sharpe, drawdown, volatility)

4. SIGNAL GENERATION
   └─ Buy/Sell/Hold with confidence score

5. VISUALIZATION
   ├─ Main technical chart
   ├─ Advanced indicators dashboard
   ├─ Fibonacci & S/R levels
   └─ Correlation heatmap

6. AI INSIGHTS
   └─ Google Gemini analysis & recommendations

7. REPORT GENERATION
   └─ Professional HTML report with all results
```

## 🎯 API Endpoints

### REST API
```
GET  /api/health              # Health check
POST /api/analyze             # Start analysis
GET  /api/session/<id>        # Session status
GET  /api/report/<id>         # Get report
GET  /api/symbols/search      # Search symbols
```

### WebSocket Events
```
→ connect                     # Client connects
← progress_update             # Progress updates
← analysis_complete           # Analysis done
← analysis_error              # Error occurred
→ disconnect                  # Client disconnects
```

## 🔐 Security Features

- ✅ API keys never stored on server
- ✅ Session-based isolation
- ✅ CORS protection
- ✅ Input validation
- ✅ No user data collection
- ✅ Secure WebSocket connections

## 📈 Performance

- **Analysis Time**: 30-60 seconds typical
- **Concurrent Users**: Supports multiple sessions
- **Data Range**: Handles years of historical data
- **Chart Generation**: High-quality 300 DPI images
- **Report Size**: ~2-5 MB typical

## 🌟 Unique Features

1. **Real-time Progress**: Live updates during analysis
2. **AI Integration**: Google Gemini insights
3. **Professional Reports**: Publication-ready HTML
4. **Modern UI**: Beautiful, responsive design
5. **Comprehensive**: 50+ technical indicators
6. **Easy to Use**: No coding required
7. **Free to Run**: Open source, self-hosted

## 🚀 Deployment Options

### Development
```bash
./start.sh
# Frontend: localhost:3000
# Backend: localhost:5000
```

### Production
```bash
./start_production.sh
# Serves from: localhost:5000
```

### Docker (Future)
```bash
docker-compose up
```

## 📝 Customization Points

- **Add Symbols**: Edit `app.py` symbols database
- **Change Indicators**: Modify `technical_analysis.py`
- **Customize UI**: Edit React components & CSS
- **Add Features**: Extend Flask API endpoints
- **Modify Reports**: Update `html_report.py`

## 🎓 Learning Resources

This project demonstrates:
- ✅ Full-stack web development
- ✅ Real-time communication (WebSockets)
- ✅ Data analysis with Python
- ✅ React component architecture
- ✅ API design & implementation
- ✅ AI integration
- ✅ Professional UI/UX design

## 🤝 Contributing

Areas for contribution:
- Additional technical indicators
- More chart types
- Enhanced AI prompts
- Mobile app version
- Additional data sources
- Backtesting features
- Portfolio tracking

---

**Built with ❤️ by Sebastien Martineau**
