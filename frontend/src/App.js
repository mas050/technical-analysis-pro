import React, { useState, useEffect } from 'react';
import './App.css';
import LandingPage from './components/LandingPage';
import AnalysisProgress from './components/AnalysisProgress';
import ReportViewer from './components/ReportViewer';
import axios from 'axios';
import io from 'socket.io-client';

function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing', 'progress', 'report'
  const [sessionId, setSessionId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io('http://localhost:5001/analysis', {
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
    try {
      const response = await axios.post('http://localhost:5001/api/analyze', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const { session_id } = response.data;
      
      setSessionId(session_id);
      setAnalysisData({
        symbol: formData.symbol,
        startDate: formData.start_date,
        endDate: formData.end_date
      });
      setCurrentView('progress');
    } catch (error) {
      console.error('Error starting analysis:', error);
      alert('Failed to start analysis: ' + (error.response?.data?.error || error.message));
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
  );
}

export default App;
