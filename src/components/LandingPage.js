import React, { useState, useEffect } from 'react';
import AppStorage from '../utils/storage';

const LandingPage = ({ onGetStarted }) => {
  const [email, setEmail] = useState('');

  // Load saved email on mount
  useEffect(() => {
    const savedEmail = AppStorage.getUserEmail();
    if (savedEmail) {
      setEmail(savedEmail);
    }
  }, []);

  const handleGetStarted = () => {
    onGetStarted();
  };

  const handleEmailSubmit = (e) => {
    e.preventDefault();
    if (email) {
      // Store email using AppStorage
      AppStorage.saveUserEmail(email);
      onGetStarted();
    }
  };

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className="navbar navbar-expand-lg navbar-light fixed-top bg-white shadow-sm">
        <div className="container">
          <a className="navbar-brand fw-bold" href="#home">
            <i className="bi bi-robot me-2 text-primary"></i>
            AI Resume Optimizer
          </a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <a className="nav-link" href="#features">Features</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#how-it-works">How It Works</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#testimonials">Success Stories</a>
              </li>
            </ul>
            <button className="btn btn-primary" onClick={handleGetStarted}>
              Get Started Free
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero-section">
        <div className="container">
          <div className="row align-items-center min-vh-100 py-5">
            <div className="col-lg-6">
              <div className="hero-content">
                <div className="badge bg-primary-subtle text-primary mb-3">
                  <i className="bi bi-lightning-fill me-1"></i>
                  AI-Powered Resume Optimization
                </div>
                <h1 className="display-4 fw-bold mb-4">
                  Beat ATS Systems &amp; 
                  <span className="text-primary"> Land Your Dream Job</span>
                </h1>
                <p className="lead text-muted mb-4">
                  Our AI analyzes job descriptions and optimizes your resume for maximum ATS compatibility. 
                  Increase your interview callbacks by <strong>300%</strong> with personalized keyword matching 
                  and professional formatting.
                </p>
                
                <div className="hero-stats mb-4">
                  <div className="row g-3">
                    <div className="col-4">
                      <div className="stat-item text-center">
                        <div className="h3 text-primary mb-1">95%</div>
                        <small className="text-muted">ATS Score</small>
                      </div>
                    </div>
                    <div className="col-4">
                      <div className="stat-item text-center">
                        <div className="h3 text-primary mb-1">10K+</div>
                        <small className="text-muted">Resumes Optimized</small>
                      </div>
                    </div>
                    <div className="col-4">
                      <div className="stat-item text-center">
                        <div className="h3 text-primary mb-1">3x</div>
                        <small className="text-muted">More Interviews</small>
                      </div>
                    </div>
                  </div>
                </div>

                <form onSubmit={handleEmailSubmit} className="hero-form">
                  <div className="input-group input-group-lg mb-3">
                    <input
                      type="email"
                      className="form-control"
                      placeholder="Enter your email to get started"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                    <button className="btn btn-primary btn-lg px-4" type="submit">
                      Start Optimizing <i className="bi bi-arrow-right ms-1"></i>
                    </button>
                  </div>
                  <small className="text-muted">
                    <i className="bi bi-check-circle-fill text-success me-1"></i>
                    Free to start • No credit card required • Results in 30 seconds
                  </small>
                </form>
              </div>
            </div>
            <div className="col-lg-6">
              <div className="hero-visual">
                <div className="resume-preview-mockup position-relative">
                  <div className="mockup-window">
                    <div className="mockup-header">
                      <div className="mockup-controls">
                        <span className="dot red"></span>
                        <span className="dot yellow"></span>
                        <span className="dot green"></span>
                      </div>
                      <div className="mockup-title">AI Resume Optimizer</div>
                    </div>
                    <div className="mockup-content">
                      <div className="score-improvement">
                        <div className="score-before">
                          <div className="score-label">Before</div>
                          <div className="score-number text-danger">42%</div>
                        </div>
                        <div className="score-arrow">
                          <i className="bi bi-arrow-right"></i>
                        </div>
                        <div className="score-after">
                          <div className="score-label">After</div>
                          <div className="score-number text-success">94%</div>
                        </div>
                      </div>
                      <div className="optimization-preview">
                        <div className="optimization-item">
                          <i className="bi bi-check-circle-fill text-success"></i>
                          Added 15 relevant keywords
                        </div>
                        <div className="optimization-item">
                          <i className="bi bi-check-circle-fill text-success"></i>
                          Reordered achievements by relevance
                        </div>
                        <div className="optimization-item">
                          <i className="bi bi-check-circle-fill text-success"></i>
                          Enhanced technical skills section
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section py-5">
        <div className="container">
          <div className="text-center mb-5">
            <h2 className="display-5 fw-bold mb-3">Why Choose AI Resume Optimizer?</h2>
            <p className="lead text-muted">Advanced AI technology meets proven recruitment strategies</p>
          </div>
          
          <div className="row g-4">
            <div className="col-lg-4 col-md-6">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="bi bi-robot"></i>
                </div>
                <h4>AI-Powered Analysis</h4>
                <p className="text-muted">
                  Advanced GPT-4 technology analyzes job descriptions and automatically converts 
                  your text resume into ATS-optimized JSON format with intelligent keyword matching.
                </p>
                <div className="feature-highlight">
                  <small className="text-primary">
                    <i className="bi bi-lightning-fill me-1"></i>
                    90% faster than manual optimization
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4 col-md-6">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="bi bi-bullseye"></i>
                </div>
                <h4>ATS Score Optimization</h4>
                <p className="text-muted">
                  Get real-time ATS compatibility scores and see exactly how your resume performs 
                  against applicant tracking systems used by 95% of Fortune 500 companies.
                </p>
                <div className="feature-highlight">
                  <small className="text-success">
                    <i className="bi bi-graph-up-arrow me-1"></i>
                    Average 15-point score improvement
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4 col-md-6">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="bi bi-magic"></i>
                </div>
                <h4>Smart Keyword Integration</h4>
                <p className="text-muted">
                  Extract 50+ relevant keywords from job descriptions and seamlessly integrate 
                  them into your achievements while maintaining natural, professional language.
                </p>
                <div className="feature-highlight">
                  <small className="text-info">
                    <i className="bi bi-key-fill me-1"></i>
                    Matches 95% of job requirements
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4 col-md-6">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="bi bi-file-earmark-pdf"></i>
                </div>
                <h4>Multiple Export Formats</h4>
                <p className="text-muted">
                  Download your optimized resume as PDF, HTML, or keep the structured JSON format. 
                  All exports maintain professional formatting and ATS compatibility.
                </p>
                <div className="feature-highlight">
                  <small className="text-warning">
                    <i className="bi bi-download me-1"></i>
                    3 export formats available
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4 col-md-6">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="bi bi-shield-check"></i>
                </div>
                <h4>Privacy & Security</h4>
                <p className="text-muted">
                  Your personal information is encrypted and never stored permanently. 
                  All processing happens securely with enterprise-grade data protection.
                </p>
                <div className="feature-highlight">
                  <small className="text-danger">
                    <i className="bi bi-lock-fill me-1"></i>
                    Zero data retention policy
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4 col-md-6">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="bi bi-lightning-charge"></i>
                </div>
                <h4>Instant Results</h4>
                <p className="text-muted">
                  Get your optimized resume in under 30 seconds. No waiting, no manual review process. 
                  AI provides immediate feedback and actionable improvements.
                </p>
                <div className="feature-highlight">
                  <small className="text-purple">
                    <i className="bi bi-stopwatch me-1"></i>
                    Results in 10-30 seconds
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="how-it-works-section py-5 bg-light">
        <div className="container">
          <div className="text-center mb-5">
            <h2 className="display-5 fw-bold mb-3">How It Works</h2>
            <p className="lead text-muted">Three simple steps to a better resume</p>
          </div>
          
          <div className="row g-4">
            <div className="col-lg-4">
              <div className="step-card text-center">
                <div className="step-number">1</div>
                <div className="step-icon">
                  <i className="bi bi-file-text"></i>
                </div>
                <h4>Upload Your Resume</h4>
                <p className="text-muted">
                  Upload your existing resume as JSON or paste your text resume. 
                  Our AI will automatically convert and structure your information.
                </p>
                <div className="step-features">
                  <small className="text-muted">
                    <i className="bi bi-check me-1"></i>JSON upload
                  </small>
                  <br />
                  <small className="text-muted">
                    <i className="bi bi-check me-1"></i>Text-to-JSON conversion
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4">
              <div className="step-card text-center">
                <div className="step-number">2</div>
                <div className="step-icon">
                  <i className="bi bi-search"></i>
                </div>
                <h4>Paste Job Description</h4>
                <p className="text-muted">
                  Copy and paste the job description you're applying for. 
                  Our AI analyzes requirements and extracts key keywords automatically.
                </p>
                <div className="step-features">
                  <small className="text-muted">
                    <i className="bi bi-check me-1"></i>Keyword extraction
                  </small>
                  <br />
                  <small className="text-muted">
                    <i className="bi bi-check me-1"></i>Requirement analysis
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4">
              <div className="step-card text-center">
                <div className="step-number">3</div>
                <div className="step-icon">
                  <i className="bi bi-stars"></i>
                </div>
                <h4>Get Optimized Resume</h4>
                <p className="text-muted">
                  Receive your ATS-optimized resume with improved keyword matching, 
                  reordered achievements, and enhanced formatting in seconds.
                </p>
                <div className="step-features">
                  <small className="text-muted">
                    <i className="bi bi-check me-1"></i>ATS score improvement
                  </small>
                  <br />
                  <small className="text-muted">
                    <i className="bi bi-check me-1"></i>Instant download
                  </small>
                </div>
              </div>
            </div>
          </div>
          
          <div className="text-center mt-5">
            <button className="btn btn-primary btn-lg" onClick={handleGetStarted}>
              Try It Now - Free <i className="bi bi-arrow-right ms-2"></i>
            </button>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="testimonials-section py-5">
        <div className="container">
          <div className="text-center mb-5">
            <h2 className="display-5 fw-bold mb-3">Success Stories</h2>
            <p className="lead text-muted">See how professionals landed their dream jobs</p>
          </div>
          
          <div className="row g-4">
            <div className="col-lg-4">
              <div className="testimonial-card">
                <div className="testimonial-rating">
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                </div>
                <blockquote>
                  "My ATS score went from 65% to 94% in just one optimization. I got 3 interview calls 
                  in the first week after using this tool. The AI recommendations were spot-on!"
                </blockquote>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="bi bi-person-circle"></i>
                  </div>
                  <div className="author-info">
                    <strong>Sarah Chen</strong>
                    <div className="text-muted">Senior Software Engineer</div>
                    <div className="text-primary">Google</div>
                  </div>
                </div>
                <div className="testimonial-result">
                  <small className="text-success">
                    <i className="bi bi-graph-up me-1"></i>
                    65% → 94% ATS Score
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4">
              <div className="testimonial-card">
                <div className="testimonial-rating">
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                </div>
                <blockquote>
                  "The text-to-JSON conversion saved me hours of formatting. The AI perfectly captured 
                  my experience and optimized it for FinTech roles. Landed my dream job at a startup!"
                </blockquote>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="bi bi-person-circle"></i>
                  </div>
                  <div className="author-info">
                    <strong>Michael Rodriguez</strong>
                    <div className="text-muted">Product Manager</div>
                    <div className="text-primary">Stripe</div>
                  </div>
                </div>
                <div className="testimonial-result">
                  <small className="text-success">
                    <i className="bi bi-briefcase me-1"></i>
                    Dream job secured
                  </small>
                </div>
              </div>
            </div>
            
            <div className="col-lg-4">
              <div className="testimonial-card">
                <div className="testimonial-rating">
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                  <i className="bi bi-star-fill"></i>
                </div>
                <blockquote>
                  "As a career changer, I struggled with ATS systems. This tool helped me highlight 
                  transferable skills and match keywords perfectly. Got my first tech interview!"
                </blockquote>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="bi bi-person-circle"></i>
                  </div>
                  <div className="author-info">
                    <strong>Emily Johnson</strong>
                    <div className="text-muted">Data Analyst</div>
                    <div className="text-primary">Microsoft</div>
                  </div>
                </div>
                <div className="testimonial-result">
                  <small className="text-success">
                    <i className="bi bi-trophy me-1"></i>
                    Career transition success
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section py-5 bg-primary text-white">
        <div className="container">
          <div className="row g-4 text-center">
            <div className="col-lg-3 col-md-6">
              <div className="stat-item">
                <div className="stat-number h2 mb-1">10,000+</div>
                <div className="stat-label">Resumes Optimized</div>
              </div>
            </div>
            <div className="col-lg-3 col-md-6">
              <div className="stat-item">
                <div className="stat-number h2 mb-1">95%</div>
                <div className="stat-label">Average ATS Score</div>
              </div>
            </div>
            <div className="col-lg-3 col-md-6">
              <div className="stat-item">
                <div className="stat-number h2 mb-1">3x</div>
                <div className="stat-label">More Interview Callbacks</div>
              </div>
            </div>
            <div className="col-lg-3 col-md-6">
              <div className="stat-item">
                <div className="stat-number h2 mb-1">30 sec</div>
                <div className="stat-label">Average Processing Time</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="final-cta-section py-5">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-lg-8 text-center">
              <h2 className="display-5 fw-bold mb-3">Ready to Land Your Dream Job?</h2>
              <p className="lead text-muted mb-4">
                Join thousands of professionals who have successfully optimized their resumes and 
                increased their interview callback rates with our AI-powered platform.
              </p>
              <div className="cta-buttons">
                <button className="btn btn-primary btn-lg me-3 mb-2" onClick={handleGetStarted}>
                  <i className="bi bi-rocket-takeoff me-2"></i>
                  Start Optimizing Now
                </button>
                <a href="#features" className="btn btn-outline-primary btn-lg mb-2">
                  Learn More
                </a>
              </div>
              <div className="cta-assurance mt-3">
                <small className="text-muted">
                  <i className="bi bi-shield-check text-success me-1"></i>
                  Free to start • No credit card required • Secure & private
                </small>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer py-4 bg-dark text-white">
        <div className="container">
          <div className="row">
            <div className="col-lg-6">
              <div className="footer-brand">
                <h5>
                  <i className="bi bi-robot me-2"></i>
                  AI Resume Optimizer
                </h5>
                <p className="text-muted mb-3">
                  Helping professionals land their dream jobs with AI-powered resume optimization.
                </p>
              </div>
            </div>
            <div className="col-lg-3">
              <h6>Features</h6>
              <ul className="list-unstyled">
                <li><a href="#features" className="text-muted text-decoration-none">ATS Optimization</a></li>
                <li><a href="#features" className="text-muted text-decoration-none">Keyword Matching</a></li>
                <li><a href="#features" className="text-muted text-decoration-none">Text-to-JSON</a></li>
                <li><a href="#features" className="text-muted text-decoration-none">PDF Export</a></li>
              </ul>
            </div>
            <div className="col-lg-3">
              <h6>Company</h6>
              <ul className="list-unstyled">
                <li><a href="#" className="text-muted text-decoration-none">Privacy Policy</a></li>
                <li><a href="#" className="text-muted text-decoration-none">Terms of Service</a></li>
                <li><a href="#" className="text-muted text-decoration-none">Contact Us</a></li>
                <li><a href="#" className="text-muted text-decoration-none">FAQ</a></li>
              </ul>
            </div>
          </div>
          <hr className="my-4" />
          <div className="row align-items-center">
            <div className="col-md-6">
              <small className="text-muted">
                © 2024 AI Resume Optimizer. Built with ❤️ for job seekers.
              </small>
            </div>
            <div className="col-md-6 text-md-end">
              <small className="text-muted">
                Powered by OpenAI GPT-4 • React • Bootstrap
              </small>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;