import React from 'react';
import LandingPage from './pages/LandingPage';
import InputSection from './pages/InputSection';
import ResultsSection from './pages/ResultsSection';
import AdminPage from './pages/AdminPage';
import { useAppState, useResumeOptimization } from './hooks';
import './pages/LandingPage.css';

function App() {
  // Use custom hooks for state management
  const appState = useAppState();
  const optimization = useResumeOptimization();

  // Event handlers
  const handleGetStarted = () => {
    appState.goToInput();
    optimization.clearError();
  };

  const handleBackToLanding = () => {
    appState.goToLanding();
    optimization.clear();
  };

  const handleBackToInput = () => {
    appState.goToInput();
    optimization.clear();
  };

  const handleOptimize = async (resumeData, jobDescription) => {
    try {
      await optimization.optimize(resumeData, jobDescription);
      appState.goToResults();
    } catch (err) {
      // Error is handled by the hook
      console.error('Optimization failed:', err);
    }
  };

  return (
    <div className="main-container">
      {optimization.error && (
        <div className="alert alert-danger alert-dismissible fade show mb-4" role="alert">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          {optimization.error}
          <button type="button" className="btn-close" onClick={optimization.clearError}></button>
        </div>
      )}

      {optimization.isLoading && (
        <div className="loading-overlay">
          <div className="loading-content">
            <div className="spinner-border text-primary mb-3" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <h5 className="mb-2">Optimizing Your Resume</h5>
            <p className="text-muted mb-0">{optimization.loadingStep}</p>
            <div className="progress mt-3" style={{width: '300px'}}>
              <div className="progress-bar progress-bar-striped progress-bar-animated"
                   role="progressbar"
                   style={{width: '100%'}}></div>
            </div>
          </div>
        </div>
      )}

      {appState.currentStep === 'landing' ? (
        <LandingPage onGetStarted={handleGetStarted} />
      ) : appState.currentStep === 'input' ? (
        <InputSection
          onOptimize={handleOptimize}
          isLoading={optimization.isLoading}
          onBackToLanding={handleBackToLanding}
        />
      ) : appState.currentStep === 'admin' ? (
        <AdminPage onBackToLanding={handleBackToLanding} />
      ) : (
        <ResultsSection
          data={optimization.optimizationData}
          onBackToInput={handleBackToInput}
        />
      )}
    </div>
  );
}

export default App;
