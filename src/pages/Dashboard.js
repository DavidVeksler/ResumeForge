import React from 'react';

const Dashboard = ({ data }) => {
  if (!data) {
    return <div className="dashboard-card"><div className="card-body">No data available</div></div>;
  }
  
  const { 
    defaultScore = 0, 
    optimizedScore = 0, 
    improvement = 0, 
    optimizations = [] 
  } = data;

  const ScoreGauge = ({ score, label, isOptimized }) => {
    const strokeDasharray = 2 * Math.PI * 45; // Circumference of circle with radius 45
    const strokeDashoffset = strokeDasharray - (strokeDasharray * score) / 100;
    const color = isOptimized ? '#16a34a' : '#0d6efd';

    return (
      <div className="text-center">
        <div className="position-relative d-inline-block">
          <svg width="130" height="130" className="score-gauge">
            <circle
              cx="65"
              cy="65"
              r="45"
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="10"
            />
            <circle
              cx="65"
              cy="65"
              r="45"
              fill="none"
              stroke={color}
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray={strokeDasharray}
              strokeDashoffset={strokeDashoffset}
              transform="rotate(-90 65 65)"
              style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
            />
          </svg>
          <div className="position-absolute top-50 start-50 translate-middle">
            <div className="score-value" style={{ color, fontSize: '2rem', fontWeight: '700' }}>
              {score}%
            </div>
          </div>
        </div>
        <div className="score-label mt-2">{label}</div>
        {isOptimized && improvement > 0 && (
          <div className="score-improvement">
            <i className="bi bi-arrow-up"></i> +{improvement}%
          </div>
        )}
      </div>
    );
  };

  return (
    <div>
      {/* ATS Score Analysis */}
      <div className="dashboard-card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <span>ATS Score Analysis</span>
          <i 
            className="bi bi-info-circle-fill text-muted" 
            title="Applicant Tracking System (ATS) score predicts how well your resume matches the job description."
          ></i>
        </div>
        <div className="card-body p-4">
          <div className="row align-items-center">
            <div className="col-6 border-end">
              <ScoreGauge 
                score={defaultScore} 
                label="Default Score" 
                isOptimized={false}
              />
            </div>
            <div className="col-6">
              <ScoreGauge 
                score={optimizedScore} 
                label="Optimized Score" 
                isOptimized={true}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Optimizations Applied */}
      <div className="dashboard-card">
        <div className="card-header">Optimizations Applied</div>
        <ul className="list-group list-group-flush optimization-list">
          {optimizations.map((optimization, index) => (
            <li key={index} className="list-group-item d-flex align-items-start">
              <i className={`bi ${optimization.icon} ${optimization.iconClass}`}></i>
              <div dangerouslySetInnerHTML={{ __html: optimization.text }} />
            </li>
          ))}
        </ul>
      </div>

      {/* Keywords Section */}
      {data.keywords && data.keywords.length > 0 && (
        <div className="dashboard-card">
          <div className="card-header">Extracted Keywords</div>
          <div className="card-body">
            <div className="d-flex flex-wrap gap-1">
              {data.keywords.slice(0, 15).map((keyword, index) => (
                <span key={index} className="badge bg-light text-dark border">
                  {keyword}
                </span>
              ))}
              {data.keywords.length > 15 && (
                <span className="badge bg-secondary">
                  +{data.keywords.length - 15} more
                </span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;