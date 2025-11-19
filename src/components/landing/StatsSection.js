import React from 'react';

const StatItem = ({ value, label }) => (
  <div className="col-4">
    <div className="stat-item text-center">
      <div className="h3 text-primary mb-1">{value}</div>
      <small className="text-muted">{label}</small>
    </div>
  </div>
);

const StatsSection = ({ stats }) => {
  return (
    <div className="hero-stats mb-4">
      <div className="row g-3">
        {stats.map((stat, index) => (
          <StatItem key={index} value={stat.value} label={stat.label} />
        ))}
      </div>
    </div>
  );
};

export default StatsSection;
