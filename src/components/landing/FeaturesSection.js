import React from 'react';

const FeatureCard = ({ icon, title, description }) => (
  <div className="col-md-4 mb-4">
    <div className="feature-card h-100">
      <div className="feature-icon">
        <i className={`bi ${icon}`}></i>
      </div>
      <h3 className="h5 mb-3">{title}</h3>
      <p className="text-muted mb-0">{description}</p>
    </div>
  </div>
);

const FeaturesSection = ({ features }) => {
  return (
    <section id="features" className="features-section py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold mb-3">
            Powerful Features to <span className="text-primary">Boost Your Career</span>
          </h2>
          <p className="lead text-muted">
            Everything you need to create an ATS-optimized resume that gets noticed
          </p>
        </div>
        <div className="row">
          {features.map((feature) => (
            <FeatureCard
              key={feature.id}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
