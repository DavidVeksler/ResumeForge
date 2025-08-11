import React, { useState, useRef, useEffect } from 'react';
import FileUpload from './FileUpload';
import TextResumeInput from './TextResumeInput';
import StorageDebugger from './StorageDebugger';
import AppStorage from '../utils/storage';

const InputSection = ({ onOptimize, isLoading, onBackToLanding }) => {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeData, setResumeData] = useState(null);
  const [fileName, setFileName] = useState('');
  const [jobDescValidation, setJobDescValidation] = useState(null);
  const [validationTimer, setValidationTimer] = useState(null);
  const [inputMethod, setInputMethod] = useState('file'); // 'file' or 'text'
  const [error, setError] = useState('');
  const [recentJobs, setRecentJobs] = useState([]);
  const [showRecentJobs, setShowRecentJobs] = useState(false);
  const [showStorageDebugger, setShowStorageDebugger] = useState(false);

  // Load persisted data on component mount
  useEffect(() => {
    loadPersistedData();
  }, []);

  // Auto-save job description as user types
  useEffect(() => {
    if (jobDescription.trim()) {
      const saveTimer = setTimeout(() => {
        AppStorage.saveJobDescription(jobDescription);
      }, 2000); // Save after 2 seconds of inactivity
      
      return () => clearTimeout(saveTimer);
    }
  }, [jobDescription]);

  const loadPersistedData = () => {
    try {
      // Load user preferences
      const preferences = AppStorage.getUserPreferences();
      setInputMethod(preferences.inputMethod || 'file');

      // Load previous job description
      const savedJobDesc = AppStorage.getJobDescription();
      if (savedJobDesc) {
        setJobDescription(savedJobDesc);
      }

      // Load previous resume data
      const savedResume = AppStorage.getResumeData();
      if (savedResume && savedResume.data) {
        setResumeData(savedResume.data);
        setFileName(savedResume.fileName || 'Restored resume data');
      }

      // Load recent jobs
      const recent = AppStorage.getRecentJobs();
      setRecentJobs(recent);

      console.log('✅ Input section data loaded from storage');
    } catch (error) {
      console.error('Error loading persisted input data:', error);
    }
  };

  const canOptimize = jobDescription.trim() && resumeData && !isLoading && 
    (!jobDescValidation || jobDescValidation.valid);

  const handleFileUpload = (data, name) => {
    setResumeData(data);
    setFileName(name);
    setError('');
    
    // Save to storage
    AppStorage.saveResumeData(data, name);
  };

  const handleTextResumeConverted = (data, validation) => {
    setResumeData(data);
    setFileName('Converted from text resume');
    setError('');
    
    // Save conversion to history and storage
    AppStorage.addConversionHistory('Text resume', data);
    AppStorage.saveResumeData(data, 'Converted from text resume');
    
    if (validation && validation.warnings.length > 0) {
      setError(`Conversion successful with recommendations: ${validation.warnings.slice(0, 2).join(', ')}`);
    }
  };

  const handleTextResumeError = (errorMessage) => {
    setError(errorMessage);
  };

  const handleInputMethodChange = (method) => {
    setInputMethod(method);
    setResumeData(null);
    setFileName('');
    setError('');
    
    // Save preference
    const preferences = AppStorage.getUserPreferences();
    AppStorage.saveUserPreferences({ ...preferences, inputMethod: method });
  };

  const handleRecentJobSelect = (job) => {
    setJobDescription(job.text);
    setShowRecentJobs(false);
    AppStorage.saveJobDescription(job.text);
  };

  const clearStoredData = () => {
    AppStorage.clearResumeData();
    AppStorage.clearJobDescription();
    AppStorage.clearOptimizationResults();
    
    setResumeData(null);
    setFileName('');
    setJobDescription('');
    setError('');
    
    alert('All stored data has been cleared.');
  };

  const validateJobDescription = async (text) => {
    if (!text.trim()) {
      setJobDescValidation(null);
      return;
    }

    const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
    const validation = {
      valid: wordCount >= 50,
      warnings: [],
      word_count: wordCount
    };

    if (wordCount < 50) {
      validation.warnings.push(`Job description is quite short (${wordCount} words). Longer descriptions provide better optimization.`);
    } else if (wordCount > 2000) {
      validation.warnings.push(`Job description is very long (${wordCount} words). Consider focusing on key requirements.`);
    }

    // Check for common job description sections
    const commonSections = ['requirements', 'responsibilities', 'qualifications', 'skills', 'experience'];
    const foundSections = commonSections.filter(section => 
      text.toLowerCase().includes(section.toLowerCase())
    ).length;

    if (foundSections < 2) {
      validation.warnings.push('Job description may be missing key sections (requirements, responsibilities, qualifications)');
    }

    setJobDescValidation(validation);
  };

  const handleJobDescriptionChange = (e) => {
    const value = e.target.value;
    setJobDescription(value);

    // Clear existing timer
    if (validationTimer) {
      clearTimeout(validationTimer);
    }

    // Set new timer for validation (debounce)
    const newTimer = setTimeout(() => {
      validateJobDescription(value);
    }, 1000);
    
    setValidationTimer(newTimer);
  };

  const handleOptimizeClick = () => {
    if (canOptimize) {
      onOptimize(resumeData, jobDescription);
    }
  };

  return (
    <section id="input-section">
      <div className="text-center mb-5">
        <div className="d-flex justify-content-between align-items-center mb-3">
          {onBackToLanding && (
            <button className="btn btn-outline-secondary" onClick={onBackToLanding}>
              <i className="bi bi-arrow-left me-2"></i>
              Back to Home
            </button>
          )}
          <div className="flex-grow-1"></div>
        </div>
        <h1 className="fw-bold">AI Resume Optimizer</h1>
        <p className="lead text-muted">Get your optimized resume and ATS score in two simple steps.</p>
      </div>
      
      <div className="row g-4">
        <div className="col-lg-7">
          <div className="input-card">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">
                <i className="bi bi-file-text-fill"></i>
                1. Paste Job Description
              </h5>
              <div className="btn-group">
                {recentJobs.length > 0 && (
                  <button
                    type="button"
                    className="btn btn-outline-secondary btn-sm"
                    onClick={() => setShowRecentJobs(!showRecentJobs)}
                  >
                    <i className="bi bi-clock-history me-1"></i>
                    Recent ({recentJobs.length})
                  </button>
                )}
                <button
                  type="button"
                  className="btn btn-outline-info btn-sm"
                  onClick={() => setShowStorageDebugger(true)}
                  title="View storage information"
                >
                  <i className="bi bi-hdd-stack"></i>
                </button>
                <button
                  type="button"
                  className="btn btn-outline-danger btn-sm"
                  onClick={clearStoredData}
                  title="Clear all stored data"
                >
                  <i className="bi bi-trash3"></i>
                </button>
              </div>
            </div>
            <p className="text-muted small">
              Provide the full job description for the most accurate analysis.
              {jobDescription && (
                <span className="text-success ms-2">
                  <i className="bi bi-cloud-check-fill"></i> Auto-saved
                </span>
              )}
            </p>
            
            {/* Recent Jobs Dropdown */}
            {showRecentJobs && recentJobs.length > 0 && (
              <div className="recent-jobs-dropdown mb-3">
                <div className="card">
                  <div className="card-header bg-light py-2">
                    <small className="fw-semibold">Recent Job Descriptions</small>
                  </div>
                  <div className="card-body p-0">
                    {recentJobs.map((job, index) => (
                      <button
                        key={job.id}
                        className="btn btn-outline-light text-start w-100 border-0 rounded-0"
                        onClick={() => handleRecentJobSelect(job)}
                      >
                        <div className="d-flex justify-content-between align-items-start">
                          <div className="flex-grow-1">
                            <div className="fw-semibold small">{job.title}</div>
                            <div className="text-muted small text-truncate" style={{maxWidth: '300px'}}>
                              {job.text.substring(0, 80)}...
                            </div>
                          </div>
                          <small className="text-muted ms-2">
                            {new Date(job.timestamp).toLocaleDateString()}
                          </small>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div className="position-relative">
              <textarea
                className={`form-control ${jobDescValidation && !jobDescValidation.valid ? 'is-invalid' : jobDescValidation && jobDescValidation.valid ? 'is-valid' : ''}`}
                rows="16"
                placeholder="e.g., Senior FinTech Engineer at ACME Corp..."
                value={jobDescription}
                onChange={handleJobDescriptionChange}
                disabled={isLoading}
              />
              {jobDescription && (
                <div className="position-absolute top-0 end-0 m-2">
                  <small className="badge bg-secondary">
                    {jobDescValidation ? jobDescValidation.word_count : jobDescription.split(/\s+/).filter(w => w.length > 0).length} words
                  </small>
                </div>
              )}
            </div>
            
            {jobDescValidation && jobDescValidation.warnings.length > 0 && (
              <div className="alert alert-warning mt-2 mb-0" role="alert">
                <i className="bi bi-info-circle-fill me-2"></i>
                <ul className="mb-0">
                  {jobDescValidation.warnings.map((warning, index) => (
                    <li key={index}>{warning}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        
        <div className="col-lg-5">
          <div className="input-card d-flex flex-column">
            <h5>
              <i className="bi bi-file-earmark-code-fill me-2"></i>
              2. Provide Your Resume
            </h5>
            
            {/* Tab Navigation */}
            <ul className="nav nav-tabs nav-justified mb-3" role="tablist">
              <li className="nav-item" role="presentation">
                <button 
                  className={`nav-link ${inputMethod === 'file' ? 'active' : ''}`}
                  onClick={() => handleInputMethodChange('file')}
                  disabled={isLoading}
                  type="button"
                >
                  <i className="bi bi-filetype-json me-1"></i>
                  Upload JSON
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button 
                  className={`nav-link ${inputMethod === 'text' ? 'active' : ''}`}
                  onClick={() => handleInputMethodChange('text')}
                  disabled={isLoading}
                  type="button"
                >
                  <i className="bi bi-robot me-1"></i>
                  Convert Text
                </button>
              </li>
            </ul>
            
            {/* Tab Content */}
            <div className="flex-grow-1">
              {inputMethod === 'file' ? (
                <div>
                  <p className="text-muted small mb-3">
                    Upload your structured <code>.json</code> resume file.
                  </p>
                  <FileUpload 
                    onFileUpload={handleFileUpload}
                    fileName={fileName}
                    disabled={isLoading}
                  />
                  
                  {/* JSON Preview for uploaded files */}
                  {resumeData && fileName && (
                    <div className="mt-3">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <small className="text-muted fw-semibold">
                          <i className="bi bi-file-earmark-code me-1"></i>
                          JSON Preview: {fileName}
                        </small>
                        <div className="btn-group">
                          <button
                            className="btn btn-outline-secondary btn-sm"
                            onClick={() => {
                              navigator.clipboard.writeText(JSON.stringify(resumeData, null, 2));
                            }}
                            title="Copy JSON to clipboard"
                          >
                            <i className="bi bi-clipboard me-1"></i>
                            Copy
                          </button>
                          <button
                            className="btn btn-outline-primary btn-sm"
                            onClick={() => {
                              const blob = new Blob([JSON.stringify(resumeData, null, 2)], {
                                type: 'application/json'
                              });
                              const url = URL.createObjectURL(blob);
                              const link = document.createElement('a');
                              link.href = url;
                              link.download = fileName.endsWith('.json') ? fileName : `${fileName}.json`;
                              document.body.appendChild(link);
                              link.click();
                              document.body.removeChild(link);
                              URL.revokeObjectURL(url);
                            }}
                            title="Download JSON file"
                          >
                            <i className="bi bi-download me-1"></i>
                            Download
                          </button>
                        </div>
                      </div>
                      <div 
                        className="border rounded p-2 bg-light"
                        style={{ 
                          maxHeight: '200px', 
                          overflowY: 'auto',
                          fontSize: '0.75rem',
                          fontFamily: 'monospace'
                        }}
                      >
                        <pre className="mb-0 text-muted">
                          {JSON.stringify(resumeData, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <p className="text-muted small mb-3">
                    Paste your resume text and AI will convert it to structured JSON.
                  </p>
                  <TextResumeInput
                    onResumeConverted={handleTextResumeConverted}
                    onError={handleTextResumeError}
                  />
                  
                  {/* JSON Preview for converted data */}
                  {resumeData && (
                    <div className="mt-3">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <small className="text-muted fw-semibold">
                          <i className="bi bi-file-earmark-code me-1"></i>
                          Converted JSON Preview
                        </small>
                        <button
                          className="btn btn-outline-secondary btn-sm"
                          onClick={() => {
                            navigator.clipboard.writeText(JSON.stringify(resumeData, null, 2));
                            // Could add a temporary success indicator here
                          }}
                          title="Copy JSON to clipboard"
                        >
                          <i className="bi bi-clipboard me-1"></i>
                          Copy
                        </button>
                      </div>
                      <div 
                        className="border rounded p-2 bg-light"
                        style={{ 
                          maxHeight: '200px', 
                          overflowY: 'auto',
                          fontSize: '0.75rem',
                          fontFamily: 'monospace'
                        }}
                      >
                        <pre className="mb-0 text-muted">
                          {JSON.stringify(resumeData, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            {/* Success/Error Messages */}
            {fileName && (
              <div className="alert alert-success mt-2 mb-0" role="alert">
                <i className="bi bi-check-circle-fill me-2"></i>
                <strong>Resume loaded:</strong> {fileName}
              </div>
            )}
            
            {error && (
              <div className="alert alert-warning mt-2 mb-0" role="alert">
                <i className="bi bi-info-circle-fill me-2"></i>
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div id="optimize-btn-container">
        <button
          className="btn btn-optimize btn-lg"
          disabled={!canOptimize}
          onClick={handleOptimizeClick}
        >
          {isLoading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Optimizing...
            </>
          ) : (
            <>
              <i className="bi bi-stars me-2"></i>
              Optimize My Resume
            </>
          )}
        </button>
      </div>
      
      {/* Storage Debugger Modal */}
      <StorageDebugger 
        show={showStorageDebugger} 
        onClose={() => setShowStorageDebugger(false)} 
      />
    </section>
  );
};

export default InputSection;