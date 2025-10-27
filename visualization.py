"""
Visualization module for technical analysis charts
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for thread safety
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os


def create_all_charts(data: pd.DataFrame, symbol: str, analysis_results: dict, output_dir: str = 'charts'):
    """Create all visualization charts"""
    os.makedirs(output_dir, exist_ok=True)
    
    create_main_chart(data, symbol, output_dir)
    create_advanced_indicators_chart(data, symbol, output_dir)
    create_fibonacci_chart(data, symbol, analysis_results, output_dir)
    create_heatmap_chart(data, symbol, output_dir)
    
    print(f"All charts saved to {output_dir}/")


def create_main_chart(df: pd.DataFrame, symbol: str, output_dir: str):
    """Create main technical analysis chart"""
    fig, axes = plt.subplots(4, 1, figsize=(16, 20))
    
    # Price and Moving Averages
    axes[0].plot(df.index, df['Close'], label='Close Price', linewidth=2, color='black')
    axes[0].plot(df.index, df['SMA_20'], label='SMA 20', alpha=0.7)
    axes[0].plot(df.index, df['SMA_50'], label='SMA 50', alpha=0.7)
    axes[0].plot(df.index, df['SMA_200'], label='SMA 200', alpha=0.7)
    axes[0].fill_between(df.index, df['BB_High'], df['BB_Low'], alpha=0.2, label='Bollinger Bands')
    axes[0].set_title(f'{symbol} - Price and Moving Averages', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Price')
    axes[0].legend(loc='best')
    axes[0].grid(True, alpha=0.3)
    
    # MACD
    axes[1].plot(df.index, df['MACD'], label='MACD', linewidth=2)
    axes[1].plot(df.index, df['MACD_Signal'], label='Signal', linewidth=2)
    axes[1].bar(df.index, df['MACD_Hist'], label='Histogram', alpha=0.3)
    axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[1].set_title('MACD Indicator', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('MACD')
    axes[1].legend(loc='best')
    axes[1].grid(True, alpha=0.3)
    
    # RSI
    axes[2].plot(df.index, df['RSI'], label='RSI', linewidth=2, color='purple')
    axes[2].axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought')
    axes[2].axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold')
    axes[2].fill_between(df.index, 30, 70, alpha=0.1)
    axes[2].set_title('RSI (Relative Strength Index)', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('RSI')
    axes[2].set_ylim(0, 100)
    axes[2].legend(loc='best')
    axes[2].grid(True, alpha=0.3)
    
    # Volume
    colors = ['green' if df['Close'].iloc[i] >= df['Open'].iloc[i] else 'red' for i in range(len(df))]
    axes[3].bar(df.index, df['Volume'], color=colors, alpha=0.5)
    axes[3].plot(df.index, df['OBV'], label='OBV', color='blue', linewidth=2)
    axes[3].set_title('Volume and OBV', fontsize=12, fontweight='bold')
    axes[3].set_ylabel('Volume')
    axes[3].legend(loc='best')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_technical_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_advanced_indicators_chart(df: pd.DataFrame, symbol: str, output_dir: str):
    """Create advanced indicators dashboard"""
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    
    # Stochastic Oscillator
    axes[0, 0].plot(df.index, df['Stoch_K'], label='%K', linewidth=2)
    axes[0, 0].plot(df.index, df['Stoch_D'], label='%D', linewidth=2)
    axes[0, 0].axhline(y=80, color='red', linestyle='--', alpha=0.5)
    axes[0, 0].axhline(y=20, color='green', linestyle='--', alpha=0.5)
    axes[0, 0].set_title('Stochastic Oscillator', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # ADX
    axes[0, 1].plot(df.index, df['ADX'], label='ADX', linewidth=2, color='black')
    axes[0, 1].plot(df.index, df['ADX_Pos'], label='+DI', linewidth=1.5, alpha=0.7)
    axes[0, 1].plot(df.index, df['ADX_Neg'], label='-DI', linewidth=1.5, alpha=0.7)
    axes[0, 1].axhline(y=25, color='red', linestyle='--', alpha=0.5, label='Trend Threshold')
    axes[0, 1].set_title('ADX (Trend Strength)', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # CMF
    axes[1, 0].plot(df.index, df['CMF'], label='CMF', linewidth=2, color='orange')
    axes[1, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[1, 0].fill_between(df.index, 0, df['CMF'], where=(df['CMF'] > 0), alpha=0.3, color='green')
    axes[1, 0].fill_between(df.index, 0, df['CMF'], where=(df['CMF'] < 0), alpha=0.3, color='red')
    axes[1, 0].set_title('Chaikin Money Flow', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # MFI
    axes[1, 1].plot(df.index, df['MFI'], label='MFI', linewidth=2, color='teal')
    axes[1, 1].axhline(y=80, color='red', linestyle='--', alpha=0.5, label='Overbought')
    axes[1, 1].axhline(y=20, color='green', linestyle='--', alpha=0.5, label='Oversold')
    axes[1, 1].set_title('Money Flow Index', fontweight='bold')
    axes[1, 1].set_ylim(0, 100)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # ATR
    axes[2, 0].plot(df.index, df['ATR'], label='ATR', linewidth=2, color='brown')
    axes[2, 0].set_title('Average True Range (Volatility)', fontweight='bold')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)
    
    # Bollinger Band Width
    axes[2, 1].plot(df.index, df['BB_Width'], label='BB Width', linewidth=2, color='navy')
    axes[2, 1].axhline(y=df['BB_Width'].mean(), color='red', linestyle='--', alpha=0.5, label='Average')
    axes[2, 1].set_title('Bollinger Band Width', fontweight='bold')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_advanced_indicators.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_fibonacci_chart(df: pd.DataFrame, symbol: str, analysis_results: dict, output_dir: str):
    """Create Fibonacci and Support/Resistance chart"""
    fig, ax = plt.subplots(figsize=(16, 8))
    
    ax.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='black')
    
    # Fibonacci levels
    fib = analysis_results.get('fibonacci', {})
    if fib and 'levels' in fib:
        for level, price in fib['levels'].items():
            ax.axhline(y=price, color='blue', linestyle='--', alpha=0.5, linewidth=1)
            ax.text(df.index[-1], price, f'Fib {level}', fontsize=8, va='center')
    
    # Support/Resistance
    sr = analysis_results.get('support_resistance', {})
    if sr:
        ax.axhline(y=sr['pivot'], color='purple', linestyle='-', alpha=0.7, linewidth=2, label='Pivot')
        ax.axhline(y=sr['resistance_1'], color='red', linestyle='--', alpha=0.6, label='R1')
        ax.axhline(y=sr['resistance_2'], color='red', linestyle='--', alpha=0.4, label='R2')
        ax.axhline(y=sr['support_1'], color='green', linestyle='--', alpha=0.6, label='S1')
        ax.axhline(y=sr['support_2'], color='green', linestyle='--', alpha=0.4, label='S2')
    
    ax.set_title(f'{symbol} - Fibonacci Retracement & Support/Resistance Levels', 
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('Price')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_fibonacci_sr.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_heatmap_chart(df: pd.DataFrame, symbol: str, output_dir: str):
    """Create correlation heatmap of indicators"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Select key indicators for correlation
    indicators = ['Close', 'RSI', 'MACD', 'ADX', 'MFI', 'ATR', 'OBV', 'CMF', 'BB_Width']
    available_indicators = [ind for ind in indicators if ind in df.columns]
    
    if len(available_indicators) > 1:
        corr_matrix = df[available_indicators].corr()
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        
        ax.set_title(f'{symbol} - Technical Indicators Correlation Matrix', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{symbol}_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    
    plt.close()
