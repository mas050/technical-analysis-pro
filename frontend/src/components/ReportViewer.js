import React, { useState, useEffect } from 'react';
import { Home, Download, Share2, Loader } from 'lucide-react';
import axios from 'axios';
import './ReportViewer.css';

const ReportViewer = ({ sessionId, analysisData, onBackToHome }) => {
  const [reportHtml, setReportHtml] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadReport();
  }, [sessionId]);

  const loadReport = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`http://localhost:5001/api/report/${sessionId}`);
      setReportHtml(response.data);
      setIsLoading(false);
    } catch (err) {
      console.error('Error loading report:', err);
      setError(err.response?.data?.error || 'Failed to load report');
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([reportHtml], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${analysisData?.symbol}_analysis_${new Date().toISOString().split('T')[0]}.html`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `Technical Analysis - ${analysisData?.symbol}`,
          text: `Check out this technical analysis for ${analysisData?.symbol}`,
          url: window.location.href
        });
      } catch (err) {
        console.log('Error sharing:', err);
      }
    } else {
      // Fallback: copy link to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  if (isLoading) {
    return (
      <div className="report-loading">
        <Loader size={48} className="spinner-icon" />
        <h2>Loading your report...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="report-error">
        <h2>Error Loading Report</h2>
        <p>{error}</p>
        <button onClick={onBackToHome} className="button">
          <Home size={20} style={{ marginRight: '8px' }} />
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="report-viewer">
      <div className="report-toolbar">
        <button onClick={onBackToHome} className="toolbar-button">
          <Home size={20} />
          <span>New Analysis</span>
        </button>
        <div className="toolbar-actions">
          <button onClick={handleDownload} className="toolbar-button">
            <Download size={20} />
            <span>Download</span>
          </button>
          <button onClick={handleShare} className="toolbar-button">
            <Share2 size={20} />
            <span>Share</span>
          </button>
        </div>
      </div>

      <div className="report-content">
        <iframe
          srcDoc={reportHtml}
          title="Analysis Report"
          className="report-iframe"
          sandbox="allow-same-origin"
        />
      </div>
    </div>
  );
};

export default ReportViewer;
