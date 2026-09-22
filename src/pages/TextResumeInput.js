import React, { useState, useEffect } from 'react';
import { parseTextResume } from '../services/api';
import AppStorage from '../utils/storage';

const TextResumeInput = ({ onResumeConverted, onError }) => {
  const [textResume, setTextResume] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [conversionHistory, setConversionHistory] = useState([]);

  // Load conversion history on mount
  useEffect(() => {
    const history = AppStorage.getConversionHistory();
    setConversionHistory(history);
  }, []);

  // Auto-save text as user types
  useEffect(() => {
    if (textResume.trim() && textResume.length > 50) {
      const saveTimer = setTimeout(() => {
        localStorage.setItem('draft_text_resume', textResume);
      }, 3000); // Save after 3 seconds of inactivity
      
      return () => clearTimeout(saveTimer);
    }
  }, [textResume]);

  // Load draft on mount
  useEffect(() => {
    const draft = localStorage.getItem('draft_text_resume');
    if (draft && draft.length > 50) {
      setTextResume(draft);
    }
  }, []);

  const handleConvert = async () => {
    if (!textResume.trim()) {
      onError('Please enter your resume text');
      return;
    }

    if (textResume.trim().length < 100) {
      onError('Resume text is too short. Please provide more detailed information.');
      return;
    }

    setIsConverting(true);
    try {
      const result = await parseTextResume(textResume.trim());
      
      // Save conversion to history
      AppStorage.addConversionHistory(textResume, result.resumeData);
      
      // Update local history state
      const updatedHistory = AppStorage.getConversionHistory();
      setConversionHistory(updatedHistory);
      
      if (result.validation && !result.validation.valid) {
        onError(`Conversion successful but validation found issues: ${result.validation.errors.join(', ')}`);
      }
      
      onResumeConverted(result.resumeData, result.validation);
      
      // Clear draft and text area
      localStorage.removeItem('draft_text_resume');
      setTextResume('');
    } catch (error) {
      onError(error.message);
    } finally {
      setIsConverting(false);
    }
  };

  const handleClear = () => {
    setTextResume('');
    localStorage.removeItem('draft_text_resume');
  };

  const sampleText = `John Smith
Senior Software Engineer
john.smith@email.com | (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Experienced software engineer with 8+ years developing scalable web applications and fintech solutions. Led teams of 5+ engineers and delivered $10M+ in revenue impact through innovative payment processing systems.

EXPERIENCE

Senior Software Engineer | TechCorp Inc | San Francisco, CA | 2020 - Present
• Built microservices architecture serving 1M+ daily users with 99.9% uptime
• Led migration to cloud infrastructure reducing costs by 40%
• Implemented real-time payment processing handling $50M monthly volume
• Mentored 3 junior developers and established code review processes

Software Engineer | StartupXYZ | San Francisco, CA | 2018 - 2020  
• Developed React/Node.js applications for cryptocurrency trading platform
• Integrated blockchain APIs for DeFi protocols with $100M+ TVL
• Optimized database queries improving performance by 60%

SKILLS
Programming: Python, JavaScript, TypeScript, Java, Go
Web Technologies: React, Node.js, Express, Django, PostgreSQL
Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Terraform
FinTech: Blockchain, DeFi, Payment Processing, API Integration

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018

PROJECTS
• DeFi Yield Optimizer - Built automated yield farming bot generating 15% APY
• Payment Gateway API - Developed secure payment processing for e-commerce platform`;

  return (
    <div className="card h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="card-title mb-0">
            <i className="bi bi-file-text me-2"></i>
            Convert Text Resume
          </h5>
          <button
            type="button"
            className="btn btn-outline-info btn-sm"
            onClick={() => setShowHelp(!showHelp)}
          >
            <i className="bi bi-question-circle me-1"></i>
            Help
          </button>
        </div>

        {showHelp && (
          <div className="alert alert-info mb-3">
            <h6><i className="bi bi-lightbulb me-2"></i>How to use:</h6>
            <ul className="mb-0 small">
              <li>Paste your existing resume text (any format)</li>
              <li>Include contact info, experience, skills, and education</li>
              <li>AI will automatically structure it into JSON format</li>
              <li>Requires OpenAI API key to be configured</li>
              <li>More detailed resumes get better results</li>
            </ul>
          </div>
        )}

        <div className="mb-3">
          <label htmlFor="textResumeInput" className="form-label">
            Paste Your Resume Text
            <span className="text-muted ms-2">({textResume.length} characters)</span>
          </label>
          <textarea
            id="textResumeInput"
            className="form-control"
            rows="12"
            value={textResume}
            onChange={(e) => setTextResume(e.target.value)}
            placeholder={`Paste your resume text here (name, contact info, experience, skills, etc.)

Example:
${sampleText.substring(0, 200)}...`}
            disabled={isConverting}
            style={{ fontFamily: 'monospace', fontSize: '0.9rem', lineHeight: '1.4' }}
          />
          <div className="form-text">
            Tip: Include quantifiable achievements and specific technologies for better ATS optimization.
          </div>
        </div>

        <div className="d-flex gap-2">
          <button
            className="btn btn-primary flex-grow-1"
            onClick={handleConvert}
            disabled={!textResume.trim() || isConverting}
          >
            {isConverting ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Converting with AI...
              </>
            ) : (
              <>
                <i className="bi bi-robot me-2"></i>
                Convert to JSON
              </>
            )}
          </button>
          
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={handleClear}
            disabled={!textResume.length || isConverting}
          >
            <i className="bi bi-x-circle me-1"></i>
            Clear
          </button>
        </div>

        {textResume.length > 0 && (
          <div className="mt-2">
            <small className="text-muted">
              Word count: ~{textResume.split(/\s+/).filter(word => word.length > 0).length} words
              {textResume.length < 100 && (
                <span className="text-warning ms-2">
                  <i className="bi bi-exclamation-triangle me-1"></i>
                  Too short - add more details
                </span>
              )}
            </small>
          </div>
        )}
      </div>
    </div>
  );
};

export default TextResumeInput;