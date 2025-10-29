import React, { useState, useEffect } from 'react';
import './App.css';
import AnimatedBackground from './components/AnimatedBackground';
import LandingPage from './components/LandingPage';
import AnalysisProgress from './components/AnalysisProgress';
import ReportViewer from './components/ReportViewer';
import axios from 'axios';
import io from 'socket.io-client';

// Use environment variable or detect based on hostname
const API_URL = process.env.REACT_APP_API_URL || 
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001'
    : `${window.location.protocol}//${window.location.hostname}:5001`);

function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing', 'progress', 'report'
  const [sessionId, setSessionId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io(`${API_URL}/analysis`, {
      transports: ['websocket', 'polling']
    });

    newSocket.on('connect', () => {
      console.log('Connected to analysis server');
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from analysis server');
    });

    setSocket(newSocket);

    return () => {
      if (newSocket) {
        newSocket.disconnect();
      }
    };
  }, []);

  const handleStartAnalysis = async (formData) => {
    console.log('handleStartAnalysis called with:', formData);
    console.log('API_URL:', API_URL);
    
    try {
      console.log('Making POST request to:', `${API_URL}/api/analyze`);
      const response = await axios.post(`${API_URL}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log('Response received:', response.data);
      
      const { session_id } = response.data;
      
      console.log('Setting session ID:', session_id);
      setSessionId(session_id);
      setAnalysisData({
        symbol: formData.symbol,
        startDate: formData.start_date,
        endDate: formData.end_date
      });
      console.log('Switching to progress view');
      setCurrentView('progress');
    } catch (error) {
      console.error('Error starting analysis:', error);
      console.error('Error response:', error.response);
      alert('Failed to start analysis: ' + (error.response?.data?.error || error.message));
      throw error;
    }
  };

  const handleAnalysisComplete = (htmlFile) => {
    setCurrentView('report');
  };

  const handleBackToHome = () => {
    setCurrentView('landing');
    setSessionId(null);
    setAnalysisData(null);
  };

  return (
    <>
      <AnimatedBackground />
      <div className="App">
        {currentView === 'landing' && (
          <LandingPage onStartAnalysis={handleStartAnalysis} />
        )}
        
        {currentView === 'progress' && (
          <AnalysisProgress
            sessionId={sessionId}
            socket={socket}
            analysisData={analysisData}
            onComplete={handleAnalysisComplete}
            onBackToHome={handleBackToHome}
          />
        )}
        
        {currentView === 'report' && (
          <ReportViewer
            sessionId={sessionId}
            analysisData={analysisData}
            onBackToHome={handleBackToHome}
          />
        )}
      </div>
    </>
  );
}

export default App;
