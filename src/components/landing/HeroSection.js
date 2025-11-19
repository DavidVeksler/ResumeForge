import React from 'react';
import StatsSection from './StatsSection';

const HeroSection = ({ content, stats, email, setEmail, onSubmit }) => {
  return (
    <section id="home" className="hero-section">
      <div className="container">
        <div className="row align-items-center py-4">
          <div className="col-lg-6">
            <div className="hero-content">
              <div className="badge bg-primary-subtle text-primary mb-3">
                <i className="bi bi-lightning-fill me-1"></i>
                {content.badge}
              </div>
              <h1 className="display-4 fw-bold mb-4">
                Beat ATS Systems &amp;
                <span className="text-primary"> {content.title.split('&')[1]}</span>
              </h1>
              <p className="lead text-muted mb-4">
                {content.description.split('300%')[0]}
                <strong>300%</strong>
                {content.description.split('300%')[1]}
              </p>

              <StatsSection stats={stats} />

              <form onSubmit={onSubmit} className="hero-form">
                <div className="input-group input-group-lg mb-3">
                  <input
                    type="email"
                    className="form-control"
                    placeholder={content.emailPlaceholder}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <button className="btn btn-primary btn-lg px-4" type="submit">
                    {content.ctaText} <i className="bi bi-arrow-right ms-1"></i>
                  </button>
                </div>
                <small className="text-muted">
                  <i className="bi bi-check-circle-fill text-success me-1"></i>
                  {content.trustText}
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
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
