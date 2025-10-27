import React, { useState, useEffect } from 'react';
import { Loader, CheckCircle, TrendingUp, Activity, BarChart3, Target, Brain } from 'lucide-react';
import './AnalysisProgress.css';

const AnalysisProgress = ({ sessionId, socket, analysisData, onComplete, onBackToHome }) => {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('Initializing...');
  const [currentStep, setCurrentStep] = useState('');
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!socket || !sessionId) return;

    // Listen for progress updates
    socket.on('progress_update', (data) => {
      if (data.session_id === sessionId) {
        setProgress(data.progress);
        setStatus(data.status);
        setCurrentStep(data.step);
      }
    });

    // Listen for completion
    socket.on('analysis_complete', (data) => {
      if (data.session_id === sessionId) {
        setIsComplete(true);
        setProgress(100);
        setStatus('Analysis Complete!');
        setTimeout(() => {
          onComplete(data.html_file);
        }, 2000);
      }
    });

    // Listen for errors
    socket.on('analysis_error', (data) => {
      if (data.session_id === sessionId) {
        setError(data.error);
        setStatus('Error occurred');
      }
    });

    return () => {
      socket.off('progress_update');
      socket.off('analysis_complete');
      socket.off('analysis_error');
    };
  }, [socket, sessionId, onComplete]);

  const getStepIcon = () => {
    if (error) return <span className="error-icon">❌</span>;
    if (isComplete) return <CheckCircle size={48} className="complete-icon" />;
    return <Loader size={48} className="spinner-icon" />;
  };

  const getProgressColor = () => {
    if (error) return '#ef4444';
    if (isComplete) return '#10b981';
    if (progress < 30) return '#667eea';
    if (progress < 70) return '#764ba2';
    return '#667eea';
  };

  const milestones = [
    { threshold: 15, icon: <Activity size={20} />, label: 'Fetching Data', completed: progress >= 15 },
    { threshold: 40, icon: <TrendingUp size={20} />, label: 'Calculating Indicators', completed: progress >= 40 },
    { threshold: 70, icon: <BarChart3 size={20} />, label: 'Analyzing Patterns', completed: progress >= 70 },
    { threshold: 90, icon: <Target size={20} />, label: 'Generating Signals', completed: progress >= 90 },
    { threshold: 95, icon: <Brain size={20} />, label: 'AI Insights', completed: progress >= 95 },
  ];

  return (
    <div className="progress-container">
      <div className="progress-header">
        <h1>Analyzing {analysisData?.symbol}</h1>
        <p>Period: {analysisData?.startDate} to {analysisData?.endDate}</p>
      </div>

      <div className="progress-content">
        <div className="progress-main">
          <div className="status-icon">
            {getStepIcon()}
          </div>

          <h2 className="status-text">{status}</h2>
          {currentStep && <p className="step-text">{currentStep}</p>}

          <div className="progress-bar-container">
            <div 
              className="progress-bar-fill"
              style={{ 
                width: `${progress}%`,
                backgroundColor: getProgressColor()
              }}
            >
              <span className="progress-percentage">{progress}%</span>
            </div>
          </div>

          {error && (
            <div className="error-box">
              <h3>Error Occurred</h3>
              <p>{error}</p>
              <button onClick={onBackToHome} className="button button-secondary">
                Back to Home
              </button>
            </div>
          )}

          {isComplete && (
            <div className="complete-box">
              <p>Redirecting to your report...</p>
            </div>
          )}
        </div>

        <div className="milestones">
          <h3>Analysis Pipeline</h3>
          <div className="milestones-list">
            {milestones.map((milestone, index) => (
              <div 
                key={index}
                className={`milestone ${milestone.completed ? 'completed' : ''} ${progress >= milestone.threshold - 5 && !milestone.completed ? 'active' : ''}`}
              >
                <div className="milestone-icon">
                  {milestone.completed ? <CheckCircle size={20} /> : milestone.icon}
                </div>
                <div className="milestone-label">{milestone.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="progress-footer">
        <p>⏱️ This usually takes 30-60 seconds depending on the date range</p>
        <p>🔒 Your analysis is being processed securely</p>
      </div>
    </div>
  );
};

export default AnalysisProgress;
