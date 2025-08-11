import React, { useState, useRef } from 'react';
import { validateResume, getSampleResume } from '../services/api';

const FileUpload = ({ onFileUpload, fileName, disabled }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState('');
  const [validationWarnings, setValidationWarnings] = useState([]);
  const [isDownloadingSample, setIsDownloadingSample] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!disabled) {
      setIsDragOver(true);
    }
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
    
    if (disabled) return;
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (disabled) return;
    
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFile = async (file) => {
    setError('');
    setValidationWarnings([]);
    
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.json')) {
      setError('Please upload a JSON file (.json)');
      return;
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }
    
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      
      // Server-side validation
      try {
        const validation = await validateResume(data);
        
        if (!validation.valid) {
          setError(`Resume validation failed: ${validation.errors.join(', ')}`);
          return;
        }
        
        if (validation.warnings && validation.warnings.length > 0) {
          setValidationWarnings(validation.warnings);
        }
        
        onFileUpload(data, file.name);
      } catch (validationError) {
        // Fallback to basic validation if server is unavailable
        if (!data.personal || !data.personal.name) {
          setError('Invalid resume format: missing personal information');
          return;
        }
        onFileUpload(data, file.name);
      }
    } catch (err) {
      setError('Invalid JSON format. Please check your file.');
    }
  };

  const handleAreaClick = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleChangeFile = (e) => {
    e.preventDefault();
    if (!disabled) {
      onFileUpload(null, '');
      setValidationWarnings([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDownloadSample = async (e) => {
    e.preventDefault();
    setIsDownloadingSample(true);
    
    try {
      const response = await getSampleResume();
      
      // Create and download the sample file
      const blob = new Blob([JSON.stringify(response.sampleData, null, 2)], {
        type: 'application/json'
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'resume_template.json';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      setError('Failed to download sample resume template');
    } finally {
      setIsDownloadingSample(false);
    }
  };

  if (fileName) {
    return (
      <div className="file-success-state">
        <i className="bi bi-filetype-json"></i>
        <div>
          <div className="fw-bold">{fileName}</div>
          <a 
            href="#" 
            className="small text-decoration-none" 
            onClick={handleChangeFile}
          >
            Change file
          </a>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div
        className={`file-drop-area ${isDragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleAreaClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".json"
          onChange={handleFileSelect}
          disabled={disabled}
        />
        <i className="bi bi-filetype-json upload-icon"></i>
        <span className="upload-icon-text mt-3">
          {isDragOver ? 'Drop your file here' : 'Drag & drop your resume JSON here'}
        </span>
        <p className="text-muted mt-1 mb-0">or click to select a file</p>
        
        <div className="mt-3">
          <button 
            type="button" 
            className="btn btn-outline-primary btn-sm"
            onClick={handleDownloadSample}
            disabled={isDownloadingSample}
          >
            {isDownloadingSample ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                Downloading...
              </>
            ) : (
              <>
                <i className="bi bi-download me-2"></i>
                Download Sample Template
              </>
            )}
          </button>
        </div>
      </div>
      
      {validationWarnings.length > 0 && (
        <div className="alert alert-warning mt-2 mb-0" role="alert">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          <strong>Recommendations:</strong>
          <ul className="mb-0 mt-1">
            {validationWarnings.map((warning, index) => (
              <li key={index}>{warning}</li>
            ))}
          </ul>
        </div>
      )}
      
      {error && (
        <div className="alert alert-danger mt-2 mb-0" role="alert">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          {error}
        </div>
      )}
    </div>
  );
};

export default FileUpload;