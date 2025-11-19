import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer py-4 bg-dark text-white">
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <h5 className="mb-3">
              <i className="bi bi-robot me-2"></i>
              AI Resume Optimizer
            </h5>
            <p className="text-muted">
              Helping job seekers optimize their resumes and land their dream jobs
              using the power of AI and ATS optimization.
            </p>
          </div>
          <div className="col-md-3">
            <h6 className="mb-3">Quick Links</h6>
            <ul className="list-unstyled">
              <li><a href="#features" className="text-muted text-decoration-none">Features</a></li>
              <li><a href="#how-it-works" className="text-muted text-decoration-none">How It Works</a></li>
              <li><a href="#testimonials" className="text-muted text-decoration-none">Success Stories</a></li>
            </ul>
          </div>
          <div className="col-md-3">
            <h6 className="mb-3">Contact</h6>
            <ul className="list-unstyled text-muted">
              <li><i className="bi bi-envelope me-2"></i>support@resumeforge.com</li>
              <li><i className="bi bi-github me-2"></i>GitHub</li>
            </ul>
          </div>
        </div>
        <hr className="my-4 bg-secondary" />
        <div className="text-center text-muted">
          <small>&copy; {currentYear} AI Resume Optimizer. All rights reserved.</small>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
