# 📊 Technical Analysis Pro - AI-Powered Market Insights

A professional-grade web application for comprehensive technical analysis of stocks, cryptocurrencies, and commodities. Powered by advanced technical indicators and Google Gemini AI for intelligent market insights.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 📈 Comprehensive Technical Analysis
- **Trend Indicators**: SMA, EMA, MACD, ADX, Ichimoku Cloud, Parabolic SAR
- **Momentum Indicators**: RSI, Stochastic Oscillator, Williams %R, ROC
- **Volatility Indicators**: Bollinger Bands, ATR, Keltner Channels
- **Volume Indicators**: OBV, CMF, MFI, VWAP

### 🎯 Advanced Features
- Fibonacci retracement levels
- Support and resistance calculations
- Price predictions using linear regression
- Risk metrics (Sharpe ratio, max drawdown, volatility)
- Automated trading signals (Buy/Sell/Hold)

### 🤖 AI-Powered Insights
- Integration with Google Gemini 2.5 Flash
- Intelligent market analysis and recommendations
- Natural language insights and explanations

### 🎨 Professional Visualizations
- Interactive price charts with indicators
- Advanced technical indicator dashboards
- Fibonacci and support/resistance levels
- Correlation heatmaps

### 🌐 Modern Web Interface
- Beautiful, responsive React frontend
- Real-time progress updates via WebSocket
- Professional HTML reports
- Mobile-friendly design

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Installation

1. **Clone the repository**
```bash
cd /Users/sebastien.martineau/Python/Technical_Analysis_Website
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
```

4. **Set up environment variables**
```bash
# Optional: For AI insights
export GEMINI_API_KEY="your_google_gemini_api_key"
```

Get your free API key at [Google AI Studio](https://makersuite.google.com/app/apikey)

### Running the Application

#### Development Mode

1. **Start the Flask backend** (in the root directory):
```bash
python app.py
```

2. **Start the React frontend** (in a new terminal, in the `frontend` directory):
```bash
cd frontend
npm start
```

3. **Open your browser** and navigate to:
```
http://localhost:3000
```

#### Production Mode

1. **Build the React frontend**:
```bash
cd frontend
npm run build
```

2. **Run the Flask server**:
```bash
python app.py
```

3. **Access the application**:
```
http://localhost:5000
```

## 📖 Usage

### Web Interface

1. **Select a Symbol**: Choose from stocks (AAPL, GOOGL), crypto (BTC-USD, ETH-USD), or commodities (GC=F, CL=F)
2. **Set Date Range**: Default is 12 months, ending today
3. **Add API Key** (Optional): For AI-powered insights
4. **Generate Analysis**: Click the button and watch real-time progress
5. **View Report**: Interactive HTML report with all analysis results

### Command Line Interface

You can still use the original CLI:

```bash
# Basic analysis
python technical_analysis.py AAPL

# Custom date range
python technical_analysis.py AAPL --start 2024-01-01 --end 2024-12-31

# With Gemini API key
python technical_analysis.py AAPL --api-key YOUR_KEY

# Without live data
python technical_analysis.py AAPL --no-live
```

## 🏗️ Project Structure

```
Technical_Analysis_Website/
├── app.py                      # Flask web application
├── technical_analysis.py       # Core analysis engine
├── html_report.py             # HTML report generator
├── visualization.py           # Chart generation
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── frontend/                  # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── LandingPage.js
│   │   │   ├── AnalysisProgress.js
│   │   │   └── ReportViewer.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
├── charts/                    # Generated charts (auto-created)
└── reports/                   # Generated reports (auto-created)
```

## 🔌 API Endpoints

### REST API

- `GET /api/health` - Health check
- `POST /api/analyze` - Start new analysis
- `GET /api/session/<session_id>` - Get session status
- `GET /api/report/<session_id>` - Get HTML report
- `GET /api/symbols/search?q=<query>` - Search symbols

### WebSocket Events

- `progress_update` - Real-time progress updates
- `analysis_complete` - Analysis completion notification
- `analysis_error` - Error notifications

## 🎨 Supported Assets

### Stocks
- AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM, V, WMT, and more

### Cryptocurrencies
- BTC-USD, ETH-USD, BNB-USD, XRP-USD, ADA-USD, DOGE-USD, SOL-USD

### Commodities
- GC=F (Gold), SI=F (Silver), CL=F (Crude Oil), NG=F (Natural Gas)

### Indices
- ^GSPC (S&P 500), ^DJI (Dow Jones), ^IXIC (NASDAQ)

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket support
- **yfinance**: Market data
- **pandas/numpy**: Data processing
- **matplotlib/seaborn**: Visualizations
- **ta**: Technical indicators
- **scikit-learn**: ML predictions
- **Google Gemini**: AI insights

### Frontend
- **React**: UI framework
- **Socket.io-client**: Real-time updates
- **Axios**: HTTP client
- **Lucide React**: Icons
- **CSS3**: Styling with gradients and animations

## ⚙️ Configuration

### Environment Variables

```bash
# Required for AI insights
GEMINI_API_KEY=your_api_key_here

# Optional: Custom port
PORT=5000
```

### Frontend Configuration

Edit `frontend/package.json` to change the proxy:
```json
"proxy": "http://localhost:5000"
```

## 📊 Example Analysis Output

The system generates:
- **Interactive HTML Report**: Professional, printable report with all metrics
- **Technical Charts**: 4 comprehensive chart sets
- **AI Insights**: Natural language market analysis
- **Trading Signals**: Clear Buy/Sell/Hold recommendations
- **Risk Metrics**: Sharpe ratio, volatility, drawdown

## 🔒 Security Notes

- API keys are never stored on the server
- All analysis runs in isolated sessions
- Reports are session-specific
- No user data is collected or stored

## ⚠️ Disclaimer

This tool provides technical analysis for **educational purposes only**. It does not constitute financial advice, investment recommendations, or an offer to buy or sell any securities. Past performance is not indicative of future results. Always conduct your own research and consult with a qualified financial advisor before making any investment decisions. Trading and investing carry risk of loss.

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Sebastien Martineau**
- Proprietary Technical Analysis System
- AI-Powered Market Insights

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For support, please open an issue in the repository.

---

**Made with ❤️ and ☕ by Sebastien Martineau**
