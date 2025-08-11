import React, { useState } from 'react';
import ResumeDisplay from './ResumeDisplay';
import Dashboard from './Dashboard';

const ResultsSection = ({ data, onBackToInput }) => {
  const [showOptimized, setShowOptimized] = useState(true);

  if (!data) {
    return <div>No data available</div>;
  }

  return (
    <section id="results-section">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="fw-bold mb-0">Your Optimized Resume</h2>
        <button 
          className="btn btn-outline-primary"
          onClick={onBackToInput}
        >
          <i className="bi bi-arrow-left me-2"></i>
          Back to Input
        </button>
      </div>
      
      <div className="row gx-5">
        {/* Left Column: Resume Preview */}
        <div className="col-lg-8">
          <div className="view-toggle-bar">
            <div className="form-check form-switch fs-5">
              <input
                className="form-check-input"
                type="checkbox"
                role="switch"
                id="viewToggle"
                checked={showOptimized}
                onChange={(e) => setShowOptimized(e.target.checked)}
              />
              <label className="form-check-label fw-bold" htmlFor="viewToggle">
                {showOptimized ? 'Optimized View' : 'Default View'}
              </label>
            </div>
          </div>
          
          <ResumeDisplay 
            html={showOptimized ? data.optimizedHtml : data.defaultHtml}
            isOptimized={showOptimized}
          />
        </div>
        
        {/* Right Column: Dashboard */}
        <div className="col-lg-4">
          <Dashboard data={data} />
        </div>
      </div>
    </section>
  );
};

export default ResultsSection;