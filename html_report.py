"""
HTML Report Generator for Technical Analysis
Creates professional-looking HTML reports with embedded charts
"""

import base64
import os
import re
from datetime import datetime
from typing import Dict, Optional


def convert_markdown_to_html(markdown_text: str) -> str:
    """Convert markdown text to HTML with proper formatting"""
    if not markdown_text:
        return ""
    
    html = markdown_text
    
    # Convert headers (#### Header -> <h4>Header</h4>, etc.)
    # Process from most specific to least specific to avoid conflicts
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert bold (**text** or __text__ -> <strong>text</strong>)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    
    # Convert italic (*text* or _text_ -> <em>text</em>)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    
    # Convert bullet points (- item or * item -> <li>item</li>)
    lines = html.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            item_text = stripped[2:].strip()
            result_lines.append(f'<li>{item_text}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    html = '\n'.join(result_lines)
    
    # Convert numbered lists (1. item -> <li>item</li>)
    lines = html.split('\n')
    in_ordered_list = False
    result_lines = []
    
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d+\.\s+', stripped):
            if not in_ordered_list:
                result_lines.append('<ol>')
                in_ordered_list = True
            item_text = re.sub(r'^\d+\.\s+', '', stripped)
            result_lines.append(f'<li>{item_text}</li>')
        else:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            result_lines.append(line)
    
    if in_ordered_list:
        result_lines.append('</ol>')
    
    html = '\n'.join(result_lines)
    
    # Convert line breaks (double newline -> <br><br>)
    html = re.sub(r'\n\n', '<br><br>', html)
    
    # Convert inline code (`code` -> <code>code</code>)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    return html


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string"""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not encode image {image_path}: {e}")
        return ""


def format_number(value: float, decimals: int = 2, is_currency: bool = False, is_percentage: bool = False) -> str:
    """Format numbers for display"""
    if value is None:
        return "N/A"
    
    if is_percentage:
        return f"{value:.{decimals}f}%"
    elif is_currency:
        return f"${value:,.{decimals}f}"
    else:
        return f"{value:,.{decimals}f}"


def get_signal_badge_class(signal: str) -> str:
    """Get CSS class for signal badge"""
    signal_upper = signal.upper() if signal else ""
    if signal_upper == "BUY":
        return "badge-buy"
    elif signal_upper == "SELL":
        return "badge-sell"
    else:
        return "badge-hold"


def get_rsi_class(rsi_signal: str) -> str:
    """Get CSS class for RSI signal"""
    if rsi_signal == "Overbought":
        return "text-danger"
    elif rsi_signal == "Oversold":
        return "text-success"
    else:
        return "text-muted"


def generate_html_report(symbol: str, analysis_results: Dict, charts_dir: str = 'charts', 
                         ai_insights: Optional[str] = None, start_date: str = "", end_date: str = "") -> str:
    """Generate professional HTML report"""
    
    # Extract data from analysis results
    trend = analysis_results.get('trend', {})
    momentum = analysis_results.get('momentum', {})
    volatility = analysis_results.get('volatility', {})
    volume = analysis_results.get('volume', {})
    fibonacci = analysis_results.get('fibonacci', {})
    support_resistance = analysis_results.get('support_resistance', {})
    predictions = analysis_results.get('predictions', {})
    risk_metrics = analysis_results.get('risk_metrics', {})
    trading_signals = analysis_results.get('trading_signals', {})
    
    # Encode charts to base64
    chart_files = {
        'main': f'{charts_dir}/{symbol}_technical_analysis.png',
        'advanced': f'{charts_dir}/{symbol}_advanced_indicators.png',
        'fibonacci': f'{charts_dir}/{symbol}_fibonacci_sr.png',
        'heatmap': f'{charts_dir}/{symbol}_correlation_heatmap.png'
    }
    
    encoded_charts = {}
    for key, path in chart_files.items():
        if os.path.exists(path):
            encoded_charts[key] = encode_image_to_base64(path)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Analysis Report - {symbol}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .symbol {{
            font-size: 3em;
            font-weight: 800;
            margin: 20px 0;
            letter-spacing: 2px;
        }}
        
        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .signal-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        
        .signal-box .signal {{
            font-size: 3em;
            font-weight: 800;
            margin-bottom: 10px;
        }}
        
        .signal-box .confidence {{
            font-size: 1.5em;
            opacity: 0.9;
        }}
        
        .badge-buy {{
            background: #10b981;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
        }}
        
        .badge-sell {{
            background: #ef4444;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
        }}
        
        .badge-hold {{
            background: #f59e0b;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        
        .metric-card .label {{
            font-size: 0.9em;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-card .value {{
            font-size: 1.8em;
            font-weight: 700;
            color: #1e293b;
        }}
        
        .metric-card .subtext {{
            font-size: 0.85em;
            color: #64748b;
            margin-top: 5px;
        }}
        
        .text-success {{
            color: #10b981;
        }}
        
        .text-danger {{
            color: #ef4444;
        }}
        
        .text-warning {{
            color: #f59e0b;
        }}
        
        .text-muted {{
            color: #64748b;
        }}
        
        .signals-list {{
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        
        .signals-list h4 {{
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #1e293b;
        }}
        
        .signals-list ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .signals-list li {{
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 1.05em;
        }}
        
        .signals-list li:last-child {{
            border-bottom: none;
        }}
        
        .signals-list li:before {{
            content: "✓ ";
            color: #10b981;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .signals-list.bearish li:before {{
            content: "✗ ";
            color: #ef4444;
        }}
        
        .chart-container {{
            margin: 30px 0;
            text-align: center;
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 15px;
        }}
        
        .ai-insights {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #f59e0b;
            margin: 30px 0;
        }}
        
        .ai-insights h3 {{
            color: #92400e;
            font-size: 1.5em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .ai-insights h3:before {{
            content: "✨";
            margin-right: 10px;
            font-size: 1.2em;
        }}
        
        .ai-insights .content {{
            color: #451a03;
            line-height: 1.8;
            font-size: 1.05em;
        }}
        
        .ai-insights .content h1 {{
            color: #92400e;
            font-size: 1.8em;
            margin: 25px 0 15px 0;
            font-weight: 700;
        }}
        
        .ai-insights .content h2 {{
            color: #92400e;
            font-size: 1.5em;
            margin: 20px 0 12px 0;
            font-weight: 600;
        }}
        
        .ai-insights .content h3 {{
            color: #92400e;
            font-size: 1.3em;
            margin: 18px 0 10px 0;
            font-weight: 600;
        }}
        
        .ai-insights .content h3:before {{
            content: "";
            margin-right: 0;
        }}
        
        .ai-insights .content h4 {{
            color: #92400e;
            font-size: 1.15em;
            margin: 15px 0 8px 0;
            font-weight: 600;
        }}
        
        .ai-insights .content strong {{
            font-weight: 700;
            color: #78350f;
        }}
        
        .ai-insights .content em {{
            font-style: italic;
            color: #78350f;
        }}
        
        .ai-insights .content ul {{
            margin: 15px 0;
            padding-left: 25px;
        }}
        
        .ai-insights .content ol {{
            margin: 15px 0;
            padding-left: 25px;
        }}
        
        .ai-insights .content li {{
            margin: 8px 0;
            line-height: 1.6;
        }}
        
        .ai-insights .content code {{
            background: rgba(120, 53, 15, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            color: #78350f;
        }}
        
        .ai-insights .content p {{
            margin: 12px 0;
        }}
        
        .fibonacci-levels {{
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
        }}
        
        .fibonacci-levels table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .fibonacci-levels th,
        .fibonacci-levels td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .fibonacci-levels th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        
        .fibonacci-levels tr:hover {{
            background: #f1f5f9;
        }}
        
        .footer {{
            background: #1e293b;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .footer p {{
            margin: 10px 0;
            opacity: 0.8;
        }}
        
        .disclaimer {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }}
        
        .disclaimer h4 {{
            color: #991b1b;
            margin-bottom: 10px;
        }}
        
        .disclaimer p {{
            color: #7f1d1d;
            font-size: 0.95em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
        
        /* Print-optimized CSS for better PDF rendering */
        @media print {{
            @page {{
                size: A3 landscape;
                margin: 1cm;
            }}
            
            body {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                font-size: 0.9em;
            }}
            
            img, svg, canvas {{
                max-width: 100%;
                page-break-inside: avoid;
                image-rendering: -webkit-optimize-contrast;
            }}
            
            .chart-container, .section {{
                page-break-inside: avoid;
            }}
            
            h1, h2, h3, h4 {{
                page-break-after: avoid;
            }}
            
            table, .metric-card {{
                page-break-inside: avoid;
            }}
            
            .ai-insights {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Technical Analysis Report</h1>
            <div class="symbol">{symbol}</div>
            <div class="meta">
                Period: {start_date} to {end_date}<br>
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>
        
        <div class="content">
            <!-- Trading Signal -->
            <div class="signal-box">
                <div class="signal">
                    <span class="{get_signal_badge_class(trading_signals.get('overall_signal', 'HOLD'))}">
                        {trading_signals.get('overall_signal', 'HOLD')}
                    </span>
                </div>
                <div class="confidence">
                    Confidence: {format_number(trading_signals.get('confidence', 0), 1)}%
                </div>
            </div>
            
            <!-- Key Metrics -->
            <section class="section">
                <h2 class="section-title">📈 Key Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Current Price</div>
                        <div class="value">{format_number(trend.get('current_price', 0), 2, is_currency=True)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">RSI (14)</div>
                        <div class="value {get_rsi_class(momentum.get('rsi_signal', 'Neutral'))}">{format_number(momentum.get('rsi', 0), 2)}</div>
                        <div class="subtext">{momentum.get('rsi_signal', 'Neutral')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Total Return</div>
                        <div class="value {'text-success' if risk_metrics.get('total_return', 0) > 0 else 'text-danger'}">
                            {format_number(risk_metrics.get('total_return', 0), 2, is_percentage=True)}
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Volatility (Annual)</div>
                        <div class="value">{format_number(risk_metrics.get('volatility', 0), 2, is_percentage=True)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Sharpe Ratio</div>
                        <div class="value">{format_number(risk_metrics.get('sharpe_ratio', 0), 2)}</div>
                        <div class="subtext">{'Excellent' if risk_metrics.get('sharpe_ratio', 0) > 2 else 'Good' if risk_metrics.get('sharpe_ratio', 0) > 1 else 'Fair'}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Max Drawdown</div>
                        <div class="value text-danger">{format_number(risk_metrics.get('max_drawdown', 0), 2, is_percentage=True)}</div>
                    </div>
                </div>
            </section>
            
            <!-- Trading Signals -->
            <section class="section">
                <h2 class="section-title">🎯 Trading Signals</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="signals-list">
                        <h4>✅ Bullish Signals ({len(trading_signals.get('bullish_signals', []))})</h4>
                        <ul>
"""
    
    for signal in trading_signals.get('bullish_signals', []):
        html += f"                            <li>{signal}</li>\n"
    
    if not trading_signals.get('bullish_signals'):
        html += "                            <li style='color: #94a3b8;'>No bullish signals detected</li>\n"
    
    html += f"""                        </ul>
                    </div>
                    <div class="signals-list bearish">
                        <h4>⚠️ Bearish Signals ({len(trading_signals.get('bearish_signals', []))})</h4>
                        <ul>
"""
    
    for signal in trading_signals.get('bearish_signals', []):
        html += f"                            <li>{signal}</li>\n"
    
    if not trading_signals.get('bearish_signals'):
        html += "                            <li style='color: #94a3b8;'>No bearish signals detected</li>\n"
    
    html += """                        </ul>
                    </div>
                </div>
            </section>
            
            <!-- Trend Analysis -->
            <section class="section">
                <h2 class="section-title">📊 Trend Analysis</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">SMA 50</div>
                        <div class="value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">SMA 200</div>
                        <div class="value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Golden Cross</div>
                        <div class="value">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">MACD Status</div>
                        <div class="value {}">{}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">ADX</div>
                        <div class="value">{}</div>
                        <div class="subtext">Trend Strength: {}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Price vs SMA200</div>
                        <div class="value {}">{}</div>
                    </div>
                </div>
            </section>
""".format(
        format_number(trend.get('sma_50', 0), 2, is_currency=True),
        format_number(trend.get('sma_200', 0), 2, is_currency=True),
        '✅ Yes' if trend.get('golden_cross') else '❌ No',
        'text-success' if trend.get('macd_bullish') else 'text-danger',
        'Bullish' if trend.get('macd_bullish') else 'Bearish',
        format_number(trend.get('adx', 0), 2),
        trend.get('trend_strength', 'Unknown'),
        'text-success' if trend.get('price_above_sma200') else 'text-danger',
        'Above' if trend.get('price_above_sma200') else 'Below'
    )
    
    # Volatility & Volume
    html += f"""
            <!-- Volatility & Volume -->
            <section class="section">
                <h2 class="section-title">📉 Volatility & Volume Analysis</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Bollinger Band Position</div>
                        <div class="value">{volatility.get('bb_position', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">ATR</div>
                        <div class="value">{format_number(volatility.get('atr', 0), 2, is_currency=True)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Volatility Level</div>
                        <div class="value">{volatility.get('volatility_level', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Volume Trend</div>
                        <div class="value {'text-success' if volume.get('volume_trend') == 'Accumulation' else 'text-danger'}">
                            {volume.get('volume_trend', 'N/A')}
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="label">MFI</div>
                        <div class="value">{format_number(volume.get('mfi', 0), 2)}</div>
                        <div class="subtext">{volume.get('mfi_signal', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">CMF</div>
                        <div class="value">{format_number(volume.get('cmf', 0), 4)}</div>
                    </div>
                </div>
            </section>
            
            <!-- Fibonacci Levels -->
            <section class="section">
                <h2 class="section-title">🎯 Fibonacci Retracement Levels</h2>
                <div class="fibonacci-levels">
                    <table>
                        <thead>
                            <tr>
                                <th>Level</th>
                                <th>Price</th>
                                <th>Distance from Current</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    current_price = fibonacci.get('current_price', 0)
    for level, price in fibonacci.get('levels', {}).items():
        distance = ((price - current_price) / current_price * 100) if current_price else 0
        html += f"""                            <tr>
                                <td><strong>Fib {level}</strong></td>
                                <td>{format_number(price, 2, is_currency=True)}</td>
                                <td class="{'text-success' if distance > 0 else 'text-danger'}">{format_number(distance, 2, is_percentage=True)}</td>
                            </tr>
"""
    
    html += """                        </tbody>
                    </table>
                </div>
            </section>
            
            <!-- Support & Resistance -->
            <section class="section">
                <h2 class="section-title">📍 Support & Resistance Levels</h2>
                <div class="metrics-grid">
"""
    
    sr = support_resistance
    html += f"""                    <div class="metric-card" style="border-left-color: #ef4444;">
                        <div class="label">Resistance 2</div>
                        <div class="value text-danger">{format_number(sr.get('resistance_2', 0), 2, is_currency=True)}</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #f59e0b;">
                        <div class="label">Resistance 1</div>
                        <div class="value text-warning">{format_number(sr.get('resistance_1', 0), 2, is_currency=True)}</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #8b5cf6;">
                        <div class="label">Pivot Point</div>
                        <div class="value" style="color: #8b5cf6;">{format_number(sr.get('pivot', 0), 2, is_currency=True)}</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #10b981;">
                        <div class="label">Support 1</div>
                        <div class="value text-success">{format_number(sr.get('support_1', 0), 2, is_currency=True)}</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #059669;">
                        <div class="label">Support 2</div>
                        <div class="value text-success">{format_number(sr.get('support_2', 0), 2, is_currency=True)}</div>
                    </div>
                </div>
            </section>
"""
    
    # AI Insights
    if ai_insights:
        # Convert markdown to HTML for better rendering
        ai_insights_html = convert_markdown_to_html(ai_insights)
        
        html += f"""
            <!-- AI Insights -->
            <section class="section">
                <div class="ai-insights">
                    <h3>AI-Powered Expert Insights (Google Gemini 2.5 Flash)</h3>
                    <div class="content">{ai_insights_html}</div>
                </div>
            </section>
"""
    
    # Charts
    html += """
            <!-- Charts -->
            <section class="section">
                <h2 class="section-title">📊 Technical Analysis Charts</h2>
"""
    
    if 'main' in encoded_charts and encoded_charts['main']:
        html += f"""
                <div class="chart-container">
                    <div class="chart-title">Main Technical Analysis</div>
                    <img src="data:image/png;base64,{encoded_charts['main']}" alt="Main Technical Analysis Chart">
                </div>
"""
    
    if 'advanced' in encoded_charts and encoded_charts['advanced']:
        html += f"""
                <div class="chart-container">
                    <div class="chart-title">Advanced Indicators</div>
                    <img src="data:image/png;base64,{encoded_charts['advanced']}" alt="Advanced Indicators Chart">
                </div>
"""
    
    if 'fibonacci' in encoded_charts and encoded_charts['fibonacci']:
        html += f"""
                <div class="chart-container">
                    <div class="chart-title">Fibonacci Retracement & Support/Resistance</div>
                    <img src="data:image/png;base64,{encoded_charts['fibonacci']}" alt="Fibonacci Chart">
                </div>
"""
    
    if 'heatmap' in encoded_charts and encoded_charts['heatmap']:
        html += f"""
                <div class="chart-container">
                    <div class="chart-title">Indicator Correlation Heatmap</div>
                    <img src="data:image/png;base64,{encoded_charts['heatmap']}" alt="Correlation Heatmap">
                </div>
"""
    
    html += """
            </section>
            
            <!-- Disclaimer -->
            <div class="disclaimer">
                <h4>⚠️ Important Disclaimer</h4>
                <p>
                    This technical analysis report does not constitute financial advice, investment recommendations, or an offer to buy or sell any securities. 
                    Past performance is not indicative of future results. Always conduct your own research and consult with a 
                    qualified financial advisor before making any investment decisions. Trading and investing carry risk of loss.
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Expert Level Technical Analysis</strong></p>
            <p>Powered by Sebastien Martineau Proprietary System</p>
            <p>Generated: {}</p>
        </div>
    </div>
</body>
</html>
""".format(datetime.now().strftime('%B %d, %Y at %I:%M %p'))
    
    return html


def generate_pdf_report(html_file: str, pdf_file: str = None, high_quality: bool = True) -> str:
    """
    Convert HTML report to PDF using WeasyPrint with enhanced quality settings
    
    Args:
        html_file: Path to the HTML file to convert
        pdf_file: Optional path for the output PDF file. If not provided, 
                 will use the same name as html_file with .pdf extension
        high_quality: Use enhanced settings for better PDF quality (default: True)
    
    Returns:
        Path to the generated PDF file
    
    Raises:
        ImportError: If weasyprint is not installed
        FileNotFoundError: If html_file doesn't exist
    """
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        raise ImportError(
            "weasyprint is required for PDF generation. "
            "Install it with: pip install weasyprint"
        )
    
    if not os.path.exists(html_file):
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    
    # Generate PDF filename if not provided
    if pdf_file is None:
        pdf_file = html_file.replace('.html', '.pdf')
    
    print(f"Converting HTML to PDF: {html_file} -> {pdf_file}")
    
    if high_quality:
        # Font configuration for better text rendering
        font_config = FontConfiguration()
        
        # Enhanced CSS for PDF rendering
        # Using A3 landscape for more content per page
        pdf_css = CSS(string='''
            @page {
                size: A3 landscape;
                margin: 1cm;
            }
            
            body {
                font-family: 'Helvetica', 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                font-size: 0.9em;
            }
            
            /* Prevent page breaks inside elements */
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
                page-break-inside: avoid;
            }
            
            table, figure, img {
                page-break-inside: avoid;
            }
            
            .section {
                page-break-inside: avoid;
            }
            
            .metric-card {
                page-break-inside: avoid;
            }
            
            /* Higher quality images */
            img {
                max-width: 100%;
                height: auto;
                image-rendering: -webkit-optimize-contrast;
                image-rendering: crisp-edges;
            }
            
            /* Better chart rendering */
            svg {
                max-width: 100%;
                height: auto;
            }
        ''', font_config=font_config)
        
        # Generate PDF with higher DPI and quality settings
        html = HTML(filename=html_file)
        html.write_pdf(
            pdf_file,
            stylesheets=[pdf_css],
            font_config=font_config,
            resolution=300,  # 300 DPI for print quality (default is 96)
            presentational_hints=True,
            optimize_images=False  # Keep original image quality
        )
    else:
        # Standard quality conversion
        HTML(filename=html_file).write_pdf(pdf_file)
    
    print(f"PDF report saved to: {pdf_file}")
    return pdf_file
