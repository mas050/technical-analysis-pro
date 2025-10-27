"""
Technical Analysis System
Provides comprehensive technical analysis for stocks, commodities, and cryptocurrencies
with AI-powered insights from Google Gemini.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for thread safety
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import ta
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import google.generativeai as genai
import json
import os
from typing import Dict, List, Tuple, Optional

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class TechnicalAnalyzer:
    """Comprehensive Technical Analysis System"""
    
    def __init__(self, symbol: str, start_date: str, end_date: str, gemini_api_key: Optional[str] = None):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.analysis_results = {}
        
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            print("Warning: No Gemini API key provided. AI insights will be skipped.")
            self.model = None
    
    def fetch_data(self, include_today: bool = True) -> pd.DataFrame:
        """
        Fetch historical data from Yahoo Finance
        
        Args:
            include_today: If True, fetches intraday data for current day
        """
        print(f"Fetching data for {self.symbol} from {self.start_date} to {self.end_date}...")
        ticker = yf.Ticker(self.symbol)
        self.data = ticker.history(start=self.start_date, end=self.end_date)
        
        if self.data.empty:
            raise ValueError(f"No data found for symbol {self.symbol}")
        
        # Remove timezone information to avoid matplotlib issues
        if self.data.index.tz is not None:
            self.data.index = self.data.index.tz_localize(None)
        
        print(f"Successfully fetched {len(self.data)} data points")
        
        # Fetch today's intraday data if requested
        if include_today:
            try:
                today = datetime.now().date()
                last_data_date = self.data.index[-1].date()
                
                # Check if we need today's data
                if last_data_date < today:
                    print(f"Fetching today's intraday data ({today})...")
                    
                    # Fetch 1-day data with 1-minute intervals to get latest price
                    intraday = ticker.history(period='1d', interval='1m')
                    
                    if not intraday.empty:
                        # Get the latest available data point
                        latest = intraday.iloc[-1]
                        latest_time = intraday.index[-1]
                        
                        # Create today's row with current data
                        # Use timezone-naive timestamp to match historical data
                        today_timestamp = pd.Timestamp(today).tz_localize(None)
                        
                        today_data = pd.DataFrame({
                            'Open': [intraday.iloc[0]['Open']],
                            'High': [intraday['High'].max()],
                            'Low': [intraday['Low'].min()],
                            'Close': [latest['Close']],
                            'Volume': [intraday['Volume'].sum()]
                        }, index=[today_timestamp])
                        
                        # Append today's data
                        self.data = pd.concat([self.data, today_data])
                        
                        print(f"✓ Added today's data (last update: {latest_time.strftime('%H:%M:%S')})")
                        print(f"  Current price: ${latest['Close']:.2f}")
                        print(f"  Day's range: ${intraday['Low'].min():.2f} - ${intraday['High'].max():.2f}")
                    else:
                        print("⚠ No intraday data available (market may be closed)")
                else:
                    print(f"✓ Data already includes today ({today})")
                    
            except Exception as e:
                print(f"⚠ Could not fetch today's data: {e}")
                print("  Continuing with historical data only...")
        
        return self.data
    
    def calculate_all_indicators(self):
        """Calculate all technical indicators"""
        self.calculate_trend_indicators()
        self.calculate_momentum_indicators()
        self.calculate_volatility_indicators()
        self.calculate_volume_indicators()
        self.calculate_fibonacci_levels()
        self.calculate_support_resistance()
        self.predict_price_movement()
        self.calculate_risk_metrics()
        self.generate_trading_signals()
    
    def calculate_trend_indicators(self) -> Dict:
        """Calculate trend-following indicators"""
        print("Calculating trend indicators...")
        df = self.data.copy()
        results = {}
        
        # Moving Averages
        df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
        df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
        df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
        df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
        df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
        
        # MACD
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Hist'] = macd.macd_diff()
        
        # ADX
        adx = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'])
        df['ADX'] = adx.adx()
        df['ADX_Pos'] = adx.adx_pos()
        df['ADX_Neg'] = adx.adx_neg()
        
        # Ichimoku Cloud
        ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'])
        df['Ichimoku_A'] = ichimoku.ichimoku_a()
        df['Ichimoku_B'] = ichimoku.ichimoku_b()
        
        # Parabolic SAR
        psar = ta.trend.PSARIndicator(df['High'], df['Low'], df['Close'])
        df['PSAR'] = psar.psar()
        
        self.data = df
        
        results['current_price'] = df['Close'].iloc[-1]
        results['sma_20'] = df['SMA_20'].iloc[-1]
        results['sma_50'] = df['SMA_50'].iloc[-1]
        results['sma_200'] = df['SMA_200'].iloc[-1]
        results['macd'] = df['MACD'].iloc[-1]
        results['macd_signal'] = df['MACD_Signal'].iloc[-1]
        results['adx'] = df['ADX'].iloc[-1]
        results['golden_cross'] = df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]
        results['price_above_sma200'] = df['Close'].iloc[-1] > df['SMA_200'].iloc[-1]
        results['macd_bullish'] = df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1]
        results['trend_strength'] = 'Strong' if df['ADX'].iloc[-1] > 25 else 'Weak'
        
        self.analysis_results['trend'] = results
        return results
    
    def calculate_momentum_indicators(self) -> Dict:
        """Calculate momentum indicators"""
        print("Calculating momentum indicators...")
        df = self.data.copy()
        results = {}
        
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
        df['Stoch_K'] = stoch.stoch()
        df['Stoch_D'] = stoch.stoch_signal()
        df['Williams_R'] = ta.momentum.williams_r(df['High'], df['Low'], df['Close'])
        df['ROC'] = ta.momentum.roc(df['Close'], window=12)
        df['Ultimate_Osc'] = ta.momentum.ultimate_oscillator(df['High'], df['Low'], df['Close'])
        
        self.data = df
        
        results['rsi'] = df['RSI'].iloc[-1]
        results['stoch_k'] = df['Stoch_K'].iloc[-1]
        results['williams_r'] = df['Williams_R'].iloc[-1]
        results['rsi_signal'] = 'Overbought' if df['RSI'].iloc[-1] > 70 else 'Oversold' if df['RSI'].iloc[-1] < 30 else 'Neutral'
        results['stoch_signal'] = 'Overbought' if df['Stoch_K'].iloc[-1] > 80 else 'Oversold' if df['Stoch_K'].iloc[-1] < 20 else 'Neutral'
        
        self.analysis_results['momentum'] = results
        return results
    
    def calculate_volatility_indicators(self) -> Dict:
        """Calculate volatility indicators"""
        print("Calculating volatility indicators...")
        df = self.data.copy()
        results = {}
        
        bollinger = ta.volatility.BollingerBands(df['Close'])
        df['BB_High'] = bollinger.bollinger_hband()
        df['BB_Mid'] = bollinger.bollinger_mavg()
        df['BB_Low'] = bollinger.bollinger_lband()
        df['BB_Width'] = bollinger.bollinger_wband()
        df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
        
        keltner = ta.volatility.KeltnerChannel(df['High'], df['Low'], df['Close'])
        df['Keltner_High'] = keltner.keltner_channel_hband()
        df['Keltner_Low'] = keltner.keltner_channel_lband()
        
        self.data = df
        
        results['bb_high'] = df['BB_High'].iloc[-1]
        results['bb_mid'] = df['BB_Mid'].iloc[-1]
        results['bb_low'] = df['BB_Low'].iloc[-1]
        results['atr'] = df['ATR'].iloc[-1]
        
        current_price = df['Close'].iloc[-1]
        results['bb_position'] = 'Upper' if current_price > df['BB_High'].iloc[-1] else 'Lower' if current_price < df['BB_Low'].iloc[-1] else 'Middle'
        results['volatility_level'] = 'High' if df['BB_Width'].iloc[-1] > df['BB_Width'].mean() else 'Low'
        
        self.analysis_results['volatility'] = results
        return results
    
    def calculate_volume_indicators(self) -> Dict:
        """Calculate volume indicators"""
        print("Calculating volume indicators...")
        df = self.data.copy()
        results = {}
        
        df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
        df['CMF'] = ta.volume.chaikin_money_flow(df['High'], df['Low'], df['Close'], df['Volume'])
        df['MFI'] = ta.volume.money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'])
        df['VWAP'] = ta.volume.volume_weighted_average_price(df['High'], df['Low'], df['Close'], df['Volume'])
        
        self.data = df
        
        results['obv'] = df['OBV'].iloc[-1]
        results['cmf'] = df['CMF'].iloc[-1]
        results['mfi'] = df['MFI'].iloc[-1]
        results['volume_trend'] = 'Accumulation' if df['CMF'].iloc[-1] > 0 else 'Distribution'
        results['mfi_signal'] = 'Overbought' if df['MFI'].iloc[-1] > 80 else 'Oversold' if df['MFI'].iloc[-1] < 20 else 'Neutral'
        
        self.analysis_results['volume'] = results
        return results
    
    def calculate_fibonacci_levels(self) -> Dict:
        """Calculate Fibonacci retracement levels"""
        print("Calculating Fibonacci levels...")
        df = self.data.copy()
        
        high = df['High'].max()
        low = df['Low'].min()
        diff = high - low
        
        levels = {
            '0.0': high,
            '0.236': high - 0.236 * diff,
            '0.382': high - 0.382 * diff,
            '0.500': high - 0.500 * diff,
            '0.618': high - 0.618 * diff,
            '0.786': high - 0.786 * diff,
            '1.0': low
        }
        
        current_price = df['Close'].iloc[-1]
        closest_level = min(levels.items(), key=lambda x: abs(x[1] - current_price))
        
        results = {
            'levels': levels,
            'swing_high': high,
            'swing_low': low,
            'current_price': current_price,
            'closest_level': closest_level[0]
        }
        
        self.analysis_results['fibonacci'] = results
        return results
    
    def calculate_support_resistance(self) -> Dict:
        """Calculate support and resistance levels"""
        print("Calculating support and resistance levels...")
        df = self.data.copy()
        
        high = df['High'].iloc[-1]
        low = df['Low'].iloc[-1]
        close = df['Close'].iloc[-1]
        pivot = (high + low + close) / 3
        
        results = {
            'pivot': pivot,
            'resistance_1': 2 * pivot - low,
            'resistance_2': pivot + (high - low),
            'support_1': 2 * pivot - high,
            'support_2': pivot - (high - low)
        }
        
        self.analysis_results['support_resistance'] = results
        return results
    
    def predict_price_movement(self) -> Dict:
        """Predict future price movement"""
        print("Generating price predictions...")
        df = self.data.copy()
        results = {}
        
        # Linear Regression
        df['Days'] = np.arange(len(df))
        X = df['Days'].values.reshape(-1, 1)
        y = df['Close'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_days = np.arange(len(df), len(df) + 5).reshape(-1, 1)
        predictions = model.predict(future_days)
        
        results['linear_regression'] = {
            'next_5_days': predictions.tolist(),
            'trend': 'Bullish' if model.coef_[0] > 0 else 'Bearish',
            'slope': float(model.coef_[0])
        }
        
        # Volatility-based prediction
        atr = df['ATR'].iloc[-1]
        current_price = df['Close'].iloc[-1]
        results['volatility_range'] = {
            'expected_high': current_price + atr,
            'expected_low': current_price - atr
        }
        
        self.analysis_results['predictions'] = results
        return results
    
    def calculate_risk_metrics(self) -> Dict:
        """Calculate risk and performance metrics"""
        print("Calculating risk metrics...")
        df = self.data.copy()
        returns = df['Close'].pct_change().dropna()
        
        results = {
            'total_return': (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100,
            'volatility': returns.std() * np.sqrt(252) * 100,
            'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0,
            'max_drawdown': ((df['Close'] / df['Close'].cummax()) - 1).min() * 100,
            'avg_daily_return': returns.mean() * 100,
            'positive_days': (returns > 0).sum() / len(returns) * 100
        }
        
        self.analysis_results['risk_metrics'] = results
        return results
    
    def generate_trading_signals(self) -> Dict:
        """Generate comprehensive trading signals"""
        print("Generating trading signals...")
        
        signals = {
            'overall_signal': None,
            'confidence': 0,
            'bullish_signals': [],
            'bearish_signals': []
        }
        
        trend = self.analysis_results.get('trend', {})
        momentum = self.analysis_results.get('momentum', {})
        volume = self.analysis_results.get('volume', {})
        
        if trend.get('golden_cross'):
            signals['bullish_signals'].append('Golden Cross (SMA50 > SMA200)')
        if trend.get('price_above_sma200'):
            signals['bullish_signals'].append('Price above SMA200')
        if trend.get('macd_bullish'):
            signals['bullish_signals'].append('MACD Bullish Crossover')
        
        rsi_signal = momentum.get('rsi_signal')
        if rsi_signal == 'Oversold':
            signals['bullish_signals'].append('RSI Oversold (potential reversal)')
        elif rsi_signal == 'Overbought':
            signals['bearish_signals'].append('RSI Overbought (potential reversal)')
        
        if volume.get('volume_trend') == 'Accumulation':
            signals['bullish_signals'].append('Volume showing accumulation')
        elif volume.get('volume_trend') == 'Distribution':
            signals['bearish_signals'].append('Volume showing distribution')
        
        bullish_count = len(signals['bullish_signals'])
        bearish_count = len(signals['bearish_signals'])
        total_signals = bullish_count + bearish_count
        
        if total_signals > 0:
            if bullish_count > bearish_count:
                signals['overall_signal'] = 'BUY'
                signals['confidence'] = (bullish_count / total_signals) * 100
            elif bearish_count > bullish_count:
                signals['overall_signal'] = 'SELL'
                signals['confidence'] = (bearish_count / total_signals) * 100
            else:
                signals['overall_signal'] = 'HOLD'
                signals['confidence'] = 50
        
        self.analysis_results['trading_signals'] = signals
        return signals
    
    def create_visualizations(self, output_dir: str = 'charts'):
        """Create comprehensive visualization charts"""
        from visualization import create_all_charts
        create_all_charts(self.data, self.symbol, self.analysis_results, output_dir)
    
    def get_gemini_insights(self) -> str:
        """Get AI-powered insights from Google Gemini"""
        if not self.model:
            return "Gemini API key not provided. Skipping AI insights."
        
        print("Generating AI insights with Google Gemini...")
        
        # Prepare comprehensive analysis summary
        summary = self._prepare_analysis_summary()
        
        prompt = f"""Analyze the following technical data and deliver a concise, actionable market briefing:

            {summary}

            Include:

            1. Overall market sentiment and trend analysis
            2. Key support and resistance levels
            3. Risk assessment and potential scenarios
            4. Entry and exit recommendations
            5. Time horizon considerations
            6. Notable divergences or chart patterns
            7. Risk management suggestions

            Conclude with a Key Takeaway summarizing the most critical market insight in no more than 3 sentences.
            Use a direct, confident tone—avoid introductions or self-references.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating AI insights: {str(e)}"
    
    def _prepare_analysis_summary(self) -> str:
        """Prepare a comprehensive summary for AI analysis"""
        summary = f"Symbol: {self.symbol}\n"
        summary += f"Period: {self.start_date} to {self.end_date}\n\n"
        
        for category, data in self.analysis_results.items():
            summary += f"\n{category.upper()}:\n"
            summary += json.dumps(data, indent=2, default=str)
            summary += "\n"
        
        return summary
    
    def generate_report(self, output_file: str = None, html_output: bool = True, pdf_output: bool = True):
        """Generate comprehensive analysis report"""
        if output_file is None:
            output_file = f"{self.symbol}_analysis_report.txt"
        
        print(f"Generating comprehensive report...")
        
        # Get AI insights once (to use in both text and HTML reports)
        ai_insights = self.get_gemini_insights()
        
        # Generate text report
        with open(output_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"TECHNICAL ANALYSIS REPORT\n")
            f.write(f"Symbol: {self.symbol}\n")
            f.write(f"Period: {self.start_date} to {self.end_date}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for category, data in self.analysis_results.items():
                f.write(f"\n{category.upper()}\n")
                f.write("-"*80 + "\n")
                f.write(json.dumps(data, indent=2, default=str))
                f.write("\n\n")
            
            # Add AI insights
            f.write("\n" + "="*80 + "\n")
            f.write("AI-POWERED EXPERT INSIGHTS (Google Gemini 2.5 Flash)\n")
            f.write("="*80 + "\n\n")
            f.write(ai_insights)
            f.write("\n\n")
        
        print(f"Text report saved to: {output_file}")
        
        # Generate HTML report if requested and AI insights are available
        if html_output and self.model is not None:
            from html_report import generate_html_report, generate_pdf_report
            
            html_file = output_file.replace('.txt', '.html')
            html_content = generate_html_report(
                symbol=self.symbol,
                analysis_results=self.analysis_results,
                charts_dir='charts',
                ai_insights=ai_insights,
                start_date=self.start_date,
                end_date=self.end_date
            )
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML report saved to: {html_file}")
            
            # Generate PDF report if requested
            if pdf_output:
                try:
                    pdf_file = generate_pdf_report(html_file)
                    return output_file, html_file, pdf_file
                except ImportError as e:
                    print(f"Warning: {e}")
                    print("Skipping PDF generation. Install weasyprint to enable PDF reports.")
                    return output_file, html_file
                except Exception as e:
                    print(f"Warning: PDF generation failed: {e}")
                    print("HTML report is still available.")
                    return output_file, html_file
            
            return output_file, html_file
        
        return output_file
    
    def run_complete_analysis(self, include_live_data: bool = True):
        """
        Run complete technical analysis workflow
        
        Args:
            include_live_data: If True, includes today's intraday data
        """
        print("\n" + "="*80)
        print("STARTING TECHNICAL ANALYSIS")
        if include_live_data:
            print("Mode: Historical + Live Intraday Data")
        else:
            print("Mode: Historical Data Only")
        print("="*80 + "\n")
        
        self.fetch_data(include_today=include_live_data)
        self.calculate_all_indicators()
        self.create_visualizations()
        report_files = self.generate_report()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print(f"\nResults:")
        
        if isinstance(report_files, tuple):
            print(f"  - Text Report: {report_files[0]}")
            print(f"  - HTML Report: {report_files[1]} 🌐")
            if len(report_files) > 2:
                print(f"  - PDF Report: {report_files[2]} 📄")
        else:
            print(f"  - Report: {report_files}")
        
        print(f"  - Charts: charts/ directory")
        print(f"\nTrading Signal: {self.analysis_results['trading_signals']['overall_signal']}")
        print(f"Confidence: {self.analysis_results['trading_signals']['confidence']:.1f}%")
        
        if isinstance(report_files, tuple):
            if len(report_files) > 2:
                print(f"\n💡 Open {report_files[1]} in your browser or {report_files[2]} for a beautiful report!")
            else:
                print(f"\n💡 Open {report_files[1]} in your browser for a beautiful interactive report!")
        
        return self.analysis_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Technical Analysis Tool with Real-Time Data Support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze with today's live data (default)
  python technical_analysis.py AAPL
  
  # Analyze with custom date range and live data
  python technical_analysis.py AAPL --start 2024-01-01
  
  # Analyze without today's live data (historical only)
  python technical_analysis.py AAPL --no-live
  
  # With Gemini API key
  python technical_analysis.py AAPL --api-key YOUR_KEY
        """
    )
    parser.add_argument('symbol', type=str, help='Stock/Crypto/Commodity symbol (e.g., AAPL, BTC-USD, GC=F)')
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)', 
                       default=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)', 
                       default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--api-key', type=str, help='Google Gemini API key', default=None)
    parser.add_argument('--no-live', action='store_true', 
                       help='Disable live intraday data (use historical data only)')
    
    args = parser.parse_args()
    
    analyzer = TechnicalAnalyzer(args.symbol, args.start, args.end, args.api_key)
    analyzer.run_complete_analysis(include_live_data=not args.no_live)
