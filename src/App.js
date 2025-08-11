import React, { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import InputSection from './components/InputSection';
import ResultsSection from './components/ResultsSection';
import { optimizeResume } from './services/api';
import AppStorage from './utils/storage';
import './components/LandingPage.css';

function App() {
  const [currentStep, setCurrentStep] = useState('landing'); // 'landing', 'input', or 'results'
  const [optimizationData, setOptimizationData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadingStep, setLoadingStep] = useState('');
  const [autoSaveInterval, setAutoSaveInterval] = useState(null);

  // Load persisted data on app start
  useEffect(() => {
    loadPersistedData();
    setupAutoSave();
    
    // Cleanup on unmount
    return () => {
      if (autoSaveInterval) {
        AppStorage.disableAutoSave(autoSaveInterval);
      }
    };
  }, []);

  // Auto-save current state periodically
  useEffect(() => {
    if (currentStep !== 'landing') {
      saveAppState();
    }
  }, [currentStep, optimizationData]);

  const loadPersistedData = () => {
    try {
      // Load previous app state
      const savedState = AppStorage.getAppState();
      if (savedState && savedState.currentStep && savedState.currentStep !== 'landing') {
        // Only restore to input or results if user was actively using the app
        const timeSinceLastUse = Date.now() - (savedState.lastUsed || 0);
        const maxRestoreTime = 24 * 60 * 60 * 1000; // 24 hours
        
        if (timeSinceLastUse < maxRestoreTime) {
          setCurrentStep(savedState.currentStep);
          
          // Load optimization results if available
          const savedResults = AppStorage.getOptimizationResults();
          if (savedResults && savedState.currentStep === 'results') {
            setOptimizationData(savedResults);
          }
        }
      }

      // Clean up expired data
      AppStorage.cleanupExpiredData();
      
      console.log('✅ Persisted data loaded successfully');
    } catch (error) {
      console.error('Error loading persisted data:', error);
    }
  };

  const saveAppState = () => {
    try {
      AppStorage.saveAppState({
        currentStep,
        hasOptimizationData: !!optimizationData
      });
    } catch (error) {
      console.error('Error saving app state:', error);
    }
  };

  const setupAutoSave = () => {
    const userPreferences = AppStorage.getUserPreferences();
    if (userPreferences.autoSave) {
      const interval = AppStorage.enableAutoSave(() => {
        if (currentStep !== 'landing') {
          saveAppState();
        }
      }, 30000); // Auto-save every 30 seconds
      
      setAutoSaveInterval(interval);
    }
  };

  const handleOptimize = async (resumeData, jobDescription) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Save input data for persistence
      AppStorage.saveResumeData(resumeData);
      AppStorage.saveJobDescription(jobDescription);
      AppStorage.addRecentJob(jobDescription);
      
      setLoadingStep('Analyzing job description...');
      await new Promise(resolve => setTimeout(resolve, 800)); // Brief pause for UX
      
      setLoadingStep('Extracting keywords...');
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setLoadingStep('Optimizing resume content...');
      const result = await optimizeResume(resumeData, jobDescription);
      
      setLoadingStep('Calculating ATS scores...');
      await new Promise(resolve => setTimeout(resolve, 400));
      
      // Save optimization results
      AppStorage.saveOptimizationResults(result);
      
      setOptimizationData(result);
      setCurrentStep('results');
    } catch (err) {
      setError(err.message || 'An error occurred while optimizing your resume');
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  const handleGetStarted = () => {
    setCurrentStep('input');
    setError(null);
  };

  const handleBackToLanding = () => {
    setCurrentStep('landing');
    setOptimizationData(null);
    setError(null);
    setLoadingStep('');
  };

  const handleBackToInput = () => {
    setCurrentStep('input');
    setOptimizationData(null);
    setError(null);
    setLoadingStep('');
  };

  return (
    <div className="main-container">
      {error && (
        <div className="alert alert-danger alert-dismissible fade show mb-4" role="alert">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          {error}
          <button type="button" className="btn-close" onClick={() => setError(null)}></button>
        </div>
      )}
      
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-content">
            <div className="spinner-border text-primary mb-3" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <h5 className="mb-2">Optimizing Your Resume</h5>
            <p className="text-muted mb-0">{loadingStep}</p>
            <div className="progress mt-3" style={{width: '300px'}}>
              <div className="progress-bar progress-bar-striped progress-bar-animated" 
                   role="progressbar" 
                   style={{width: '100%'}}></div>
            </div>
          </div>
        </div>
      )}
      
      {currentStep === 'landing' ? (
        <LandingPage onGetStarted={handleGetStarted} />
      ) : currentStep === 'input' ? (
        <InputSection 
          onOptimize={handleOptimize} 
          isLoading={isLoading}
          onBackToLanding={handleBackToLanding}
        />
      ) : (
        <ResultsSection 
          data={optimizationData}
          onBackToInput={handleBackToInput}
        />
      )}
    </div>
  );
}

export default App;