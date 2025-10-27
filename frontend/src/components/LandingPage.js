import React, { useState, useEffect } from 'react';
import { TrendingUp, Calendar, Search, Sparkles } from 'lucide-react';
import axios from 'axios';
import './LandingPage.css';

const LandingPage = ({ onStartAnalysis }) => {
  const [formData, setFormData] = useState({
    symbol: '',
    start_date: '',
    end_date: '',
    api_key: ''
  });
  const [symbols, setSymbols] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Set default dates
    const today = new Date();
    const twelveMonthsAgo = new Date();
    twelveMonthsAgo.setMonth(today.getMonth() - 12);

    setFormData(prev => ({
      ...prev,
      start_date: twelveMonthsAgo.toISOString().split('T')[0],
      end_date: today.toISOString().split('T')[0]
    }));

    // Load symbols
    loadSymbols();
  }, []);

  const loadSymbols = async (query = '') => {
    try {
      const response = await axios.get(`/api/symbols/search?q=${query}`);
      setSymbols(response.data);
    } catch (error) {
      console.error('Error loading symbols:', error);
    }
  };

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    setFormData(prev => ({ ...prev, symbol: value }));
    setShowDropdown(true);
    loadSymbols(value);
  };

  const handleSymbolSelect = (symbol) => {
    setFormData(prev => ({ ...prev, symbol: symbol.symbol }));
    setSearchQuery(symbol.symbol);
    setShowDropdown(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.symbol) {
      alert('Please select a symbol');
      return;
    }

    setIsLoading(true);
    try {
      await onStartAnalysis(formData);
    } catch (error) {
      console.error('Error:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="landing-container">
      <div className="landing-header">
        <div className="logo">
          <TrendingUp size={48} />
        </div>
        <h1>📊 Technical Analysis Pro</h1>
        <p>AI-Powered Market Insights for Stocks, Crypto & Commodities</p>
        <div className="features">
          <span className="feature-badge">
            <Sparkles size={16} /> AI-Powered
          </span>
          <span className="feature-badge">
            <TrendingUp size={16} /> Real-Time Data
          </span>
          <span className="feature-badge">
            <Calendar size={16} /> Historical Analysis
          </span>
        </div>
      </div>

      <div className="landing-content">
        <form onSubmit={handleSubmit} className="analysis-form">
          <h2>Start Your Analysis</h2>
          
          <div className="input-group">
            <label htmlFor="symbol">
              <Search size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
              Select Symbol
            </label>
            <div className="symbol-search-container">
              <input
                type="text"
                id="symbol"
                name="symbol"
                value={searchQuery}
                onChange={handleSearchChange}
                onFocus={() => setShowDropdown(true)}
                placeholder="Search for stocks, crypto, or commodities..."
                required
                autoComplete="off"
              />
              {showDropdown && symbols.length > 0 && (
                <div className="symbol-dropdown">
                  {symbols.map((symbol) => (
                    <div
                      key={symbol.symbol}
                      className="symbol-option"
                      onClick={() => handleSymbolSelect(symbol)}
                    >
                      <span className="symbol-code">{symbol.symbol}</span>
                      <span className="symbol-name">{symbol.name}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <p className="input-hint">
              Examples: AAPL (Apple), BTC-USD (Bitcoin), GC=F (Gold Futures)
            </p>
          </div>

          <div className="date-inputs">
            <div className="input-group">
              <label htmlFor="start_date">
                <Calendar size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                Start Date
              </label>
              <input
                type="date"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="end_date">
                <Calendar size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                End Date
              </label>
              <input
                type="date"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="api_key">
              <Sparkles size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
              Google Gemini API Key (Optional)
            </label>
            <input
              type="password"
              id="api_key"
              name="api_key"
              value={formData.api_key}
              onChange={handleInputChange}
              placeholder="Enter your API key for AI insights..."
            />
            <p className="input-hint">
              Get your free API key at <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer">Google AI Studio</a>
            </p>
          </div>

          <button type="submit" className="button submit-button" disabled={isLoading}>
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Starting Analysis...
              </>
            ) : (
              <>
                <TrendingUp size={20} style={{ marginRight: '8px' }} />
                Generate Analysis
              </>
            )}
          </button>
        </form>

        <div className="info-section">
          <h3>What You'll Get:</h3>
          <ul className="features-list">
            <li>📈 Comprehensive trend analysis with moving averages</li>
            <li>📊 Advanced technical indicators (RSI, MACD, Bollinger Bands)</li>
            <li>🎯 Support & resistance levels with Fibonacci retracements</li>
            <li>💹 Volume analysis and money flow indicators</li>
            <li>✨ AI-powered insights from Google Gemini</li>
            <li>📉 Risk metrics and performance analysis</li>
            <li>🎨 Professional charts and visualizations</li>
            <li>💡 Clear buy/sell/hold recommendations</li>
          </ul>
        </div>
      </div>

      <div className="landing-footer">
        <p>⚠️ <strong>Disclaimer:</strong> This tool provides technical analysis for educational purposes only. Not financial advice.</p>
        <p>Powered by Sebastien Martineau Proprietary System</p>
      </div>
    </div>
  );
};

export default LandingPage;
