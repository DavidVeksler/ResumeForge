import React, { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import TextResumeInput from './TextResumeInput';
import StorageDebugger from '../components/StorageDebugger';
import AppStorage from '../utils/storage';
import { useResumeData, useJobDescription } from '../hooks';

const InputSection = ({ onOptimize, isLoading, onBackToLanding }) => {
  // Use custom hooks for state management
  const resumeState = useResumeData();
  const jobDescState = useJobDescription();

  // Local UI state
  const [inputMethod, setInputMethod] = useState('file');
  const [error, setError] = useState('');
  const [recentJobs, setRecentJobs] = useState([]);
  const [showRecentJobs, setShowRecentJobs] = useState(false);
  const [showStorageDebugger, setShowStorageDebugger] = useState(false);

  // Load persisted data and preferences on mount
  useEffect(() => {
    const preferences = AppStorage.getUserPreferences();
    setInputMethod(preferences.inputMethod || 'file');

    const recent = AppStorage.getRecentJobs();
    setRecentJobs(recent);

    console.log('✅ Input section data loaded from storage');
  }, []);

  // Auto-save job description
  useEffect(() => {
    if (jobDescState.value.trim()) {
      const saveTimer = setTimeout(() => {
        AppStorage.saveJobDescription(jobDescState.value);
      }, 2000);
      return () => clearTimeout(saveTimer);
    }
  }, [jobDescState.value]);

  // Check if optimization can proceed
  const canOptimize = jobDescState.isValid && resumeState.isValid && !isLoading;

  // Event handlers
  const handleFileUpload = (data, name) => {
    resumeState.setData(data);
    resumeState.setFileName(name);
    setError('');
    AppStorage.saveResumeData(data, name);
  };

  const handleTextResumeConverted = (data, validation) => {
    resumeState.setData(data);
    resumeState.setFileName('Converted from text resume');
    setError('');

    AppStorage.addConversionHistory('Text resume', data);
    AppStorage.saveResumeData(data, 'Converted from text resume');

    if (validation?.warnings?.length > 0) {
      setError(`Conversion successful with recommendations: ${validation.warnings.slice(0, 2).join(', ')}`);
    }
  };

  const handleTextResumeError = (errorMessage) => {
    setError(errorMessage);
  };

  const handleInputMethodChange = (method) => {
    setInputMethod(method);
    resumeState.clearData();
    setError('');
    AppStorage.saveUserPreferences({ inputMethod: method });
  };

  const handleJobDescriptionChange = (e) => {
    const value = e.target.value;
    jobDescState.setValue(value);
    setError('');

    // Add to recent jobs if it's substantial (50+ words)
    const wordCount = value.trim().split(/\s+/).length;
    if (value.trim() && wordCount >= 50) {
      const preview = value.slice(0, 100) + '...';
      AppStorage.addRecentJob({ description: value, preview });
      setRecentJobs(AppStorage.getRecentJobs());
    }
  };

  const handleRecentJobSelect = (job) => {
    jobDescState.setValue(job.description);
    setShowRecentJobs(false);
    AppStorage.saveJobDescription(job.description);
  };

  const handleClearRecentJobs = () => {
    AppStorage.clearRecentJobs();
    setRecentJobs([]);
  };

  const handleOptimizeClick = () => {
    if (!resumeState.validate()) {
      setError('Please fix resume validation errors');
      return;
    }

    if (!jobDescState.isValid) {
      setError(`Job description must be at least 50 words (currently ${jobDescState.wordCount} words)`);
      return;
    }

    onOptimize(resumeState.data, jobDescState.value);
  };

  return (
    <div className="container-fluid">
      <div className="row mb-3">
        <div className="col">
          <button
            className="btn btn-outline-secondary"
            onClick={onBackToLanding}
            disabled={isLoading}
          >
            <i className="bi bi-arrow-left me-2"></i>
            Back to Home
          </button>
          <button
            className="btn btn-outline-info ms-2"
            onClick={() => setShowStorageDebugger(!showStorageDebugger)}
          >
            <i className="bi bi-info-circle me-2"></i>
            {showStorageDebugger ? 'Hide' : 'Show'} Storage Info
          </button>
        </div>
      </div>

      {showStorageDebugger && (
        <div className="row mb-3">
          <div className="col">
            <StorageDebugger />
          </div>
        </div>
      )}

      <div className="row">
        {/* Resume Input Column */}
        <div className="col-md-6">
          <div className="card shadow-sm mb-3">
            <div className="card-header bg-primary text-white">
              <h5 className="mb-0">
                <i className="bi bi-file-earmark-person me-2"></i>
                Step 1: Your Resume
              </h5>
            </div>
            <div className="card-body">
              {/* Input Method Selector */}
              <div className="btn-group w-100 mb-3" role="group">
                <button
                  type="button"
                  className={`btn ${inputMethod === 'file' ? 'btn-primary' : 'btn-outline-primary'}`}
                  onClick={() => handleInputMethodChange('file')}
                  disabled={isLoading}
                >
                  <i className="bi bi-file-earmark-arrow-up me-2"></i>
                  Upload JSON
                </button>
                <button
                  type="button"
                  className={`btn ${inputMethod === 'text' ? 'btn-primary' : 'btn-outline-primary'}`}
                  onClick={() => handleInputMethodChange('text')}
                  disabled={isLoading}
                >
                  <i className="bi bi-type me-2"></i>
                  Paste Resume Text
                </button>
              </div>

              {/* Resume Input Component */}
              {inputMethod === 'file' ? (
                <FileUpload
                  onFileUpload={handleFileUpload}
                  disabled={isLoading}
                  currentFileName={resumeState.fileName}
                />
              ) : (
                <TextResumeInput
                  onResumeConverted={handleTextResumeConverted}
                  onError={handleTextResumeError}
                  disabled={isLoading}
                />
              )}

              {/* Resume Status */}
              {resumeState.data && (
                <div className="alert alert-success mt-3">
                  <i className="bi bi-check-circle-fill me-2"></i>
                  Resume loaded: <strong>{resumeState.fileName}</strong>
                </div>
              )}

              {resumeState.validationErrors.length > 0 && (
                <div className="alert alert-warning mt-3">
                  <strong>Validation issues:</strong>
                  <ul className="mb-0 mt-2">
                    {resumeState.validationErrors.map((err, idx) => (
                      <li key={idx}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Job Description Column */}
        <div className="col-md-6">
          <div className="card shadow-sm mb-3">
            <div className="card-header bg-success text-white">
              <h5 className="mb-0">
                <i className="bi bi-briefcase me-2"></i>
                Step 2: Job Description
              </h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label htmlFor="jobDescription" className="form-label">
                  Paste the job description you're targeting
                </label>
                <textarea
                  id="jobDescription"
                  className="form-control"
                  rows="15"
                  value={jobDescState.value}
                  onChange={handleJobDescriptionChange}
                  placeholder="Paste the complete job description here..."
                  disabled={isLoading}
                />
                <small className="text-muted">
                  Word count: {jobDescState.wordCount} {!jobDescState.isValid && '(minimum 50 words)'}
                </small>
              </div>

              {recentJobs.length > 0 && (
                <div className="mb-3">
                  <button
                    className="btn btn-outline-secondary btn-sm"
                    onClick={() => setShowRecentJobs(!showRecentJobs)}
                    disabled={isLoading}
                  >
                    <i className="bi bi-clock-history me-2"></i>
                    {showRecentJobs ? 'Hide' : 'Show'} Recent Jobs ({recentJobs.length})
                  </button>

                  {showRecentJobs && (
                    <div className="mt-2">
                      <div className="list-group">
                        {recentJobs.map((job, index) => (
                          <button
                            key={index}
                            className="list-group-item list-group-item-action"
                            onClick={() => handleRecentJobSelect(job)}
                            disabled={isLoading}
                          >
                            <div className="d-flex justify-content-between">
                              <small>{job.preview}</small>
                              <small className="text-muted">{job.timestamp}</small>
                            </div>
                          </button>
                        ))}
                      </div>
                      <button
                        className="btn btn-outline-danger btn-sm mt-2"
                        onClick={handleClearRecentJobs}
                        disabled={isLoading}
                      >
                        Clear Recent Jobs
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="row">
          <div className="col">
            <div className="alert alert-warning alert-dismissible fade show" role="alert">
              {error}
              <button
                type="button"
                className="btn-close"
                onClick={() => setError('')}
              ></button>
            </div>
          </div>
        </div>
      )}

      {/* Optimize Button */}
      <div className="row">
        <div className="col text-center">
          <button
            className="btn btn-primary btn-lg px-5"
            onClick={handleOptimizeClick}
            disabled={!canOptimize}
          >
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2"></span>
                Optimizing...
              </>
            ) : (
              <>
                <i className="bi bi-magic me-2"></i>
                Optimize Resume
              </>
            )}
          </button>
          {!canOptimize && !isLoading && (
            <div className="text-muted mt-2">
              <small>
                Please provide both resume data and job description to continue
              </small>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InputSection;
