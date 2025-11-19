import React from 'react';

const Navigation = ({ onGetStarted }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light fixed-top bg-white shadow-sm">
      <div className="container">
        <a className="navbar-brand fw-bold" href="#home">
          <i className="bi bi-robot me-2 text-primary"></i>
          AI Resume Optimizer
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
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
          <button className="btn btn-primary" onClick={onGetStarted}>
            Get Started Free
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
