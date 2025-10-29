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
        /* CSS Variables - Design System */
        :root {{
            --primary: #1e40af;
            --primary-light: #3b82f6;
            --secondary: #ec4899;
            --success: #10b981;
            --success-light: #34d399;
            --warning: #f59e0b;
            --error: #ef4444;
            --gradient-primary: linear-gradient(135deg, #1e40af 0%, #764ba2 100%);
            --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-success: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-bg-light: rgba(255, 255, 255, 0.06);
            --glass-bg-dark: rgba(0, 0, 0, 0.2);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-border-light: rgba(255, 255, 255, 0.2);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.2);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.3);
            --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.4);
            --shadow-glow: 0 0 40px rgba(30, 64, 175, 0.3);
            --shadow-glow-success: 0 0 40px rgba(16, 185, 129, 0.3);
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --radius-full: 9999px;
            --transition-base: 0.3s ease;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #f8fafc;
            background: #0f172a;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }}
        
        /* Animated Background */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
            z-index: -10;
        }}
        
        /* Floating Orbs - Multiple animated orbs */
        .orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.6;
            pointer-events: none;
            z-index: -1;
        }}
        
        .orb-1 {{
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(30, 64, 175, 0.4) 0%, rgba(30, 64, 175, 0) 70%);
            top: -10%;
            left: -10%;
            animation: float 20s ease-in-out infinite;
        }}
        
        .orb-2 {{
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(236, 72, 153, 0.35) 0%, rgba(236, 72, 153, 0) 70%);
            top: 20%;
            right: -5%;
            animation: float 25s ease-in-out infinite 5s;
        }}
        
        .orb-3 {{
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, rgba(139, 92, 246, 0) 70%);
            bottom: -15%;
            left: 20%;
            animation: float 30s ease-in-out infinite 10s;
        }}
        
        .orb-4 {{
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.35) 0%, rgba(59, 130, 246, 0) 70%);
            bottom: 10%;
            right: 15%;
            animation: float 22s ease-in-out infinite 15s;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(50px, -50px) scale(1.1); }}
            66% {{ transform: translate(-50px, 50px) scale(0.9); }}
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes shimmer {{
            100% {{ transform: translateX(100%); }}
        }}
        
        @keyframes gradient-shift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: transparent;
            border: none;
            border-radius: 0;
            box-shadow: none;
            overflow: visible;
            animation: fadeInUp 1s ease-out;
        }}
        
        .header {{
            background: rgba(30, 64, 175, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-xl);
            color: white;
            padding: 60px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            margin-bottom: 40px;
            box-shadow: var(--shadow-lg);
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: translateX(-100%);
            animation: shimmer 3s infinite;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
            position: relative;
            z-index: 1;
        }}
        
        .header .symbol {{
            font-size: 3.5em;
            font-weight: 800;
            margin: 20px 0;
            letter-spacing: 2px;
            background: linear-gradient(135deg, #fff 0%, #ec4899 50%, #f093fb 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient-shift 5s ease infinite;
            position: relative;
            z-index: 1;
        }}
        
        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }}
        
        .content {{
            padding: 40px;
            background: transparent;
        }}
        
        .section {{
            margin-bottom: 60px;
            animation: fadeInUp 0.8s ease-out;
        }}
        
        .section-title {{
            font-size: 1.8em;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid rgba(30, 64, 175, 0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .signal-box {{
            background: var(--glass-bg-light);
            backdrop-filter: blur(20px);
            border: 2px solid var(--glass-border-light);
            color: white;
            padding: 40px;
            border-radius: var(--radius-lg);
            text-align: center;
            margin-bottom: 30px;
            box-shadow: var(--shadow-glow);
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
            background: var(--gradient-success);
            color: white;
            padding: 12px 28px;
            border-radius: var(--radius-full);
            font-weight: 700;
            display: inline-block;
            box-shadow: var(--shadow-glow-success);
        }}
        
        .badge-sell {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 12px 28px;
            border-radius: var(--radius-full);
            font-weight: 700;
            display: inline-block;
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.3);
        }}
        
        .badge-hold {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 12px 28px;
            border-radius: var(--radius-full);
            font-weight: 700;
            display: inline-block;
            box-shadow: 0 0 40px rgba(245, 158, 11, 0.3);
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            padding: 20px;
            border-radius: var(--radius-md);
            border: 1px solid var(--glass-border);
            border-left: 4px solid var(--primary);
            transition: all var(--transition-base);
            box-shadow: var(--shadow-md);
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            border-color: var(--glass-border-light);
        }}
        
        .metric-card .label {{
            font-size: 0.9em;
            color: rgba(248, 250, 252, 0.6);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-card .value {{
            font-size: 1.8em;
            font-weight: 700;
            color: #f8fafc;
        }}
        
        .metric-card .subtext {{
            font-size: 0.85em;
            color: rgba(248, 250, 252, 0.6);
            margin-top: 5px;
        }}
        
        .text-success {{
            color: var(--success-light);
        }}
        
        .text-danger {{
            color: var(--error);
        }}
        
        .text-warning {{
            color: var(--warning);
        }}
        
        .text-muted {{
            color: rgba(248, 250, 252, 0.5);
        }}
        
        .signals-list {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 20px;
            border-radius: var(--radius-md);
            margin-bottom: 20px;
            box-shadow: var(--shadow-md);
        }}
        
        .signals-list h4 {{
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #f8fafc;
            font-weight: 700;
        }}
        
        .signals-list ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .signals-list li {{
            padding: 10px 0;
            border-bottom: 1px solid var(--glass-border);
            font-size: 1.05em;
            color: rgba(248, 250, 252, 0.9);
        }}
        
        .signals-list li:last-child {{
            border-bottom: none;
        }}
        
        .signals-list li:before {{
            content: "✓ ";
            color: var(--success);
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .signals-list.bearish li:before {{
            content: "✗ ";
            color: var(--error);
        }}
        
        .chart-container {{
            margin: 30px 0;
            text-align: center;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 20px;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-xl);
        }}
        
        .chart-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 15px;
        }}
        
        .ai-insights {{
            background: var(--glass-bg-light);
            backdrop-filter: blur(20px);
            border: 2px solid rgba(245, 158, 11, 0.3);
            padding: 30px;
            border-radius: var(--radius-lg);
            border-left: 5px solid var(--warning);
            margin: 30px 0;
            box-shadow: 0 0 40px rgba(245, 158, 11, 0.2);
        }}
        
        .ai-insights h3 {{
            color: #fbbf24;
            font-size: 1.5em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            font-weight: 700;
        }}
        
        .ai-insights h3:before {{
            content: "✨";
            margin-right: 10px;
            font-size: 1.2em;
        }}
        
        .ai-insights .content {{
            color: rgba(248, 250, 252, 0.9);
            line-height: 1.8;
            font-size: 1.05em;
        }}
        
        .ai-insights .content h1 {{
            color: #fbbf24;
            font-size: 1.8em;
            margin: 25px 0 15px 0;
            font-weight: 700;
        }}
        
        .ai-insights .content h2 {{
            color: #fbbf24;
            font-size: 1.5em;
            margin: 20px 0 12px 0;
            font-weight: 600;
        }}
        
        .ai-insights .content h3 {{
            color: #fbbf24;
            font-size: 1.3em;
            margin: 18px 0 10px 0;
            font-weight: 600;
        }}
        
        .ai-insights .content h3:before {{
            content: "";
            margin-right: 0;
        }}
        
        .ai-insights .content h4 {{
            color: #fbbf24;
            font-size: 1.15em;
            margin: 15px 0 8px 0;
            font-weight: 600;
        }}
        
        .ai-insights .content strong {{
            font-weight: 700;
            color: #fde68a;
        }}
        
        .ai-insights .content em {{
            font-style: italic;
            color: #fde68a;
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
            background: rgba(245, 158, 11, 0.2);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            color: #fde68a;
        }}
        
        .ai-insights .content p {{
            margin: 12px 0;
        }}
        
        .fibonacci-levels {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 20px;
            border-radius: var(--radius-md);
            margin: 20px 0;
            box-shadow: var(--shadow-md);
        }}
        
        .fibonacci-levels table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .fibonacci-levels th,
        .fibonacci-levels td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--glass-border);
            color: rgba(248, 250, 252, 0.9);
        }}
        
        .fibonacci-levels th {{
            background: var(--gradient-primary);
            color: white;
            font-weight: 600;
        }}
        
        .fibonacci-levels tr:hover {{
            background: var(--glass-bg-light);
        }}
        
        .footer {{
            background: rgba(15, 23, 42, 0.3);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-xl);
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 60px;
            box-shadow: var(--shadow-lg);
        }}
        
        .footer p {{
            margin: 10px 0;
            opacity: 0.8;
        }}
        
        .disclaimer {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 2px solid var(--error);
            border-left: 4px solid var(--error);
            padding: 20px;
            border-radius: var(--radius-md);
            margin: 30px 0;
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.2);
        }}
        
        .disclaimer h4 {{
            color: var(--error);
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .disclaimer p {{
            color: rgba(248, 250, 252, 0.8);
            font-size: 0.95em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            body::before,
            body::after,
            .orb {{
                display: none !important;
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
    <!-- Animated Background Orbs -->
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    
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
                    <h3>Asset Evaluation & Risk Profile</h3>
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
