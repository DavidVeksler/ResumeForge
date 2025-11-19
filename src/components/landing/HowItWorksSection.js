import React from 'react';

const StepCard = ({ step, icon, title, description, isLast }) => (
  <div className="col-md-6 col-lg-3 mb-4">
    <div className="step-card text-center">
      <div className="step-number">{step}</div>
      <div className="step-icon mb-3">
        <i className={`bi ${icon}`}></i>
      </div>
      <h4 className="h5 mb-2">{title}</h4>
      <p className="text-muted small mb-0">{description}</p>
      {!isLast && (
        <div className="step-arrow d-none d-lg-block">
          <i className="bi bi-arrow-right"></i>
        </div>
      )}
    </div>
  </div>
);

const HowItWorksSection = ({ steps }) => {
  return (
    <section id="how-it-works" className="how-it-works-section py-5 bg-light">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold mb-3">
            How It <span className="text-primary">Works</span>
          </h2>
          <p className="lead text-muted">
            Get your optimized resume in 4 simple steps
          </p>
        </div>
        <div className="row position-relative">
          {steps.map((stepData, index) => (
            <StepCard
              key={stepData.step}
              step={stepData.step}
              icon={stepData.icon}
              title={stepData.title}
              description={stepData.description}
              isLast={index === steps.length - 1}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
