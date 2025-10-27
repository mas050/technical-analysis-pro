"""
Flask Web Application for Technical Analysis System
Professional-grade web interface with real-time progress updates
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import threading
from datetime import datetime, timedelta
from technical_analysis import TechnicalAnalyzer
from html_report import generate_html_report
import uuid

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Configure CORS - allow all origins in development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

socketio = SocketIO(app, 
                    cors_allowed_origins="*",
                    async_mode='threading',
                    logger=False,
                    engineio_logger=False)

# Store active analysis sessions
active_sessions = {}

class ProgressTracker:
    """Track and emit progress updates during analysis"""
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.progress = 0
        self.status = "Initializing..."
        self.current_step = ""
        
    def update(self, progress, status, step=""):
        self.progress = progress
        self.status = status
        self.current_step = step
        socketio.emit('progress_update', {
            'session_id': self.session_id,
            'progress': progress,
            'status': status,
            'step': step
        }, namespace='/analysis')
        
    def complete(self, html_file):
        socketio.emit('analysis_complete', {
            'session_id': self.session_id,
            'html_file': html_file,
            'status': 'completed'
        }, namespace='/analysis')


def run_analysis_async(session_id, symbol, start_date, end_date, api_key):
    """Run analysis in background thread with progress updates"""
    tracker = ProgressTracker(session_id)
    
    try:
        # Initialize
        tracker.update(5, "Initializing analyzer...", "Setting up technical analyzer")
        analyzer = TechnicalAnalyzer(symbol, start_date, end_date, api_key)
        
        # Fetch data
        tracker.update(15, "Fetching market data...", f"Downloading data for {symbol}")
        analyzer.fetch_data(include_today=True)
        
        # Calculate indicators
        tracker.update(30, "Calculating trend indicators...", "SMA, EMA, MACD, ADX")
        analyzer.calculate_trend_indicators()
        
        tracker.update(40, "Calculating momentum indicators...", "RSI, Stochastic, Williams %R")
        analyzer.calculate_momentum_indicators()
        
        tracker.update(50, "Calculating volatility indicators...", "Bollinger Bands, ATR, Keltner")
        analyzer.calculate_volatility_indicators()
        
        tracker.update(60, "Calculating volume indicators...", "OBV, CMF, MFI, VWAP")
        analyzer.calculate_volume_indicators()
        
        tracker.update(70, "Calculating Fibonacci levels...", "Retracement levels")
        analyzer.calculate_fibonacci_levels()
        
        tracker.update(75, "Calculating support/resistance...", "Pivot points")
        analyzer.calculate_support_resistance()
        
        tracker.update(80, "Generating predictions...", "Price forecasting")
        analyzer.predict_price_movement()
        
        tracker.update(85, "Calculating risk metrics...", "Sharpe ratio, drawdown")
        analyzer.calculate_risk_metrics()
        
        tracker.update(90, "Generating trading signals...", "Buy/Sell/Hold signals")
        analyzer.generate_trading_signals()
        
        # Create visualizations
        tracker.update(92, "Creating charts...", "Generating visualizations")
        charts_dir = f'charts/{session_id}'
        os.makedirs(charts_dir, exist_ok=True)
        analyzer.create_visualizations(output_dir=charts_dir)
        
        # Get AI insights
        tracker.update(95, "Generating AI insights...", "Consulting Google Gemini")
        ai_insights = analyzer.get_gemini_insights()
        
        # Generate HTML report
        tracker.update(98, "Generating report...", "Creating HTML report")
        html_content = generate_html_report(
            symbol=symbol,
            analysis_results=analyzer.analysis_results,
            charts_dir=charts_dir,
            ai_insights=ai_insights,
            start_date=start_date,
            end_date=end_date
        )
        
        # Save HTML report
        reports_dir = 'reports'
        os.makedirs(reports_dir, exist_ok=True)
        html_file = f'{reports_dir}/{session_id}.html'
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Store results
        active_sessions[session_id] = {
            'status': 'completed',
            'html_file': html_file,
            'symbol': symbol,
            'results': analyzer.analysis_results,
            'completed_at': datetime.now().isoformat()
        }
        
        tracker.update(100, "Analysis complete!", "Ready to view")
        tracker.complete(html_file)
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in analysis: {error_msg}")
        socketio.emit('analysis_error', {
            'session_id': session_id,
            'error': error_msg
        }, namespace='/analysis')
        
        active_sessions[session_id] = {
            'status': 'error',
            'error': error_msg
        }


@app.route('/')
def index():
    """Serve React frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def start_analysis():
    """Start a new technical analysis"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Log the request for debugging
        print(f"Received analysis request from {request.remote_addr}")
        print(f"Content-Type: {request.content_type}")
        print(f"Request data: {request.get_data(as_text=True)}")
        
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        symbol = data.get('symbol', '').upper()
        start_date = data.get('start_date')
        end_date = data.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        api_key = data.get('api_key') or os.getenv('GEMINI_API_KEY')
        
        # Validate inputs
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        # Set default start date if not provided (12 months ago)
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        print(f"Starting analysis for {symbol} (Session: {session_id})")
        
        # Initialize session
        active_sessions[session_id] = {
            'status': 'running',
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'started_at': datetime.now().isoformat()
        }
        
        # Start analysis in background thread
        thread = threading.Thread(
            target=run_analysis_async,
            args=(session_id, symbol, start_date, end_date, api_key)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'status': 'started',
            'message': 'Analysis started successfully'
        }), 202
        
    except Exception as e:
        print(f"Error in start_analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get status of an analysis session"""
    session = active_sessions.get(session_id)
    
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify(session)


@app.route('/api/report/<session_id>', methods=['GET'])
def get_report(session_id):
    """Get the HTML report for a completed analysis"""
    session = active_sessions.get(session_id)
    
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    if session['status'] != 'completed':
        return jsonify({'error': 'Analysis not completed yet'}), 400
    
    html_file = session.get('html_file')
    if not html_file or not os.path.exists(html_file):
        return jsonify({'error': 'Report file not found'}), 404
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/api/symbols/search', methods=['GET'])
def search_symbols():
    """Search for stock/crypto/commodity symbols"""
    query = request.args.get('q', '').upper()
    
    # Common symbols database (can be expanded)
    symbols = {
        # Stocks
        'AAPL': 'Apple Inc.',
        'GOOGL': 'Alphabet Inc.',
        'MSFT': 'Microsoft Corporation',
        'AMZN': 'Amazon.com Inc.',
        'TSLA': 'Tesla Inc.',
        'META': 'Meta Platforms Inc.',
        'NVDA': 'NVIDIA Corporation',
        'JPM': 'JPMorgan Chase & Co.',
        'V': 'Visa Inc.',
        'WMT': 'Walmart Inc.',
        'DIS': 'The Walt Disney Company',
        'NFLX': 'Netflix Inc.',
        'BA': 'Boeing Company',
        'GE': 'General Electric',
        'F': 'Ford Motor Company',
        
        # Crypto
        'BTC-USD': 'Bitcoin',
        'ETH-USD': 'Ethereum',
        'BNB-USD': 'Binance Coin',
        'XRP-USD': 'Ripple',
        'ADA-USD': 'Cardano',
        'DOGE-USD': 'Dogecoin',
        'SOL-USD': 'Solana',
        'MATIC-USD': 'Polygon',
        
        # Commodities
        'GC=F': 'Gold Futures',
        'SI=F': 'Silver Futures',
        'CL=F': 'Crude Oil Futures',
        'NG=F': 'Natural Gas Futures',
        'HG=F': 'Copper Futures',
        
        # Indices
        '^GSPC': 'S&P 500',
        '^DJI': 'Dow Jones Industrial Average',
        '^IXIC': 'NASDAQ Composite',
        '^RUT': 'Russell 2000'
    }
    
    if query:
        results = [
            {'symbol': symbol, 'name': name}
            for symbol, name in symbols.items()
            if query in symbol or query in name.upper()
        ]
    else:
        results = [{'symbol': symbol, 'name': name} for symbol, name in symbols.items()]
    
    return jsonify(results[:20])  # Limit to 20 results


@socketio.on('connect', namespace='/analysis')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected to analysis namespace')
    emit('connected', {'status': 'connected'})


@socketio.on('disconnect', namespace='/analysis')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected from analysis namespace')


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('charts', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Run the application
    print("\n" + "="*80)
    print("🚀 Technical Analysis Web Application Starting...")
    print("="*80)
    print("\n📊 Server running at: http://localhost:5001")
    print("💡 API Documentation: http://localhost:5001/api/health")
    print("\n⚠️  Make sure to set GEMINI_API_KEY environment variable for AI insights")
    print("="*80 + "\n")
    
    socketio.run(app, debug=False, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
