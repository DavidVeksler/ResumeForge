import React, { useState, useEffect } from 'react';
import { healthCheck } from '../services/api';

const AdminPage = ({ onBackToLanding }) => {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastRefresh, setLastRefresh] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(null);

  const fetchHealthData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await healthCheck();
      setHealthData(data);
      setLastRefresh(new Date());
    } catch (err) {
      setError(err.message);
      setHealthData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealthData();
    
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, []);

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(fetchHealthData, 30000); // Refresh every 30 seconds
      setRefreshInterval(interval);
    } else {
      if (refreshInterval) {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    }

    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [autoRefresh]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'success';
      case 'warning': return 'warning'; 
      case 'unhealthy': return 'danger';
      default: return 'secondary';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy': return 'bi-check-circle-fill';
      case 'warning': return 'bi-exclamation-triangle-fill';
      case 'unhealthy': return 'bi-x-circle-fill';
      default: return 'bi-question-circle-fill';
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const renderDependencyStatus = (name, status) => (
    <div key={name} className="d-flex justify-content-between align-items-center py-1">
      <span className="text-capitalize">{name.replace('_', ' ')}</span>
      <span className={`badge bg-${status ? 'success' : 'danger'}`}>
        <i className={`bi ${status ? 'bi-check-lg' : 'bi-x-lg'} me-1`}></i>
        {status ? 'Available' : 'Missing'}
      </span>
    </div>
  );

  const renderFeatureStatus = (name, status) => (
    <div key={name} className="d-flex justify-content-between align-items-center py-1">
      <span className="text-capitalize">{name.replace('_', ' ')}</span>
      <span className={`badge bg-${status ? 'success' : 'secondary'}`}>
        <i className={`bi ${status ? 'bi-check-lg' : 'bi-dash'} me-1`}></i>
        {status ? 'Enabled' : 'Disabled'}
      </span>
    </div>
  );

  return (
    <div className="container-fluid py-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h2 mb-1">
            <i className="bi bi-gear-fill me-2"></i>
            System Administration
          </h1>
          <p className="text-muted mb-0">Monitor system health and configuration</p>
        </div>
        <div>
          <button 
            className="btn btn-outline-secondary me-2"
            onClick={onBackToLanding}
          >
            <i className="bi bi-arrow-left me-1"></i>
            Back to Home
          </button>
          <button 
            className="btn btn-primary me-2" 
            onClick={fetchHealthData}
            disabled={loading}
          >
            <i className={`bi ${loading ? 'bi-arrow-clockwise spin' : 'bi-arrow-clockwise'} me-1`}></i>
            Refresh
          </button>
          <div className="btn-group">
            <input 
              className="btn-check" 
              type="checkbox" 
              id="autoRefresh"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            <label className="btn btn-outline-info" htmlFor="autoRefresh">
              <i className="bi bi-clock me-1"></i>
              Auto-refresh
            </label>
          </div>
        </div>
      </div>

      {/* Last Refresh Info */}
      {lastRefresh && (
        <div className="alert alert-info mb-4">
          <i className="bi bi-info-circle me-2"></i>
          Last updated: {lastRefresh.toLocaleString()}
          {autoRefresh && <span className="ms-2">(Auto-refresh: ON)</span>}
        </div>
      )}

      {/* Loading State */}
      {loading && !healthData && (
        <div className="text-center py-5">
          <div className="spinner-border text-primary mb-3" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>Checking system health...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="alert alert-danger mb-4">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Health Data */}
      {healthData && (
        <div className="row g-4">
          {/* Overall Status */}
          <div className="col-12">
            <div className={`card border-${getStatusColor(healthData.status)}`}>
              <div className="card-body">
                <div className="d-flex align-items-center">
                  <div className={`p-3 rounded-circle bg-${getStatusColor(healthData.status)} bg-opacity-10 me-3`}>
                    <i className={`bi ${getStatusIcon(healthData.status)} fs-1 text-${getStatusColor(healthData.status)}`}></i>
                  </div>
                  <div className="flex-grow-1">
                    <h3 className="card-title mb-1">
                      System Status: <span className={`text-${getStatusColor(healthData.status)}`}>
                        {healthData.status.charAt(0).toUpperCase() + healthData.status.slice(1)}
                      </span>
                    </h3>
                    <p className="card-text text-muted mb-0">{healthData.message}</p>
                    <small className="text-muted">Version {healthData.version} • {formatTimestamp(healthData.timestamp)}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* System Information */}
          <div className="col-lg-6">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title mb-0">
                  <i className="bi bi-cpu me-2"></i>
                  System Information
                </h5>
              </div>
              <div className="card-body">
                <div className="row g-3">
                  <div className="col-12">
                    <div className="border rounded p-3">
                      <h6 className="text-muted">Platform</h6>
                      <p className="mb-0 font-monospace small">{healthData.system?.platform}</p>
                    </div>
                  </div>
                  <div className="col-12">
                    <div className="border rounded p-3">
                      <h6 className="text-muted">Python Version</h6>
                      <p className="mb-0">{healthData.system?.python_version}</p>
                    </div>
                  </div>
                  {healthData.system?.memory && (
                    <div className="col-12">
                      <div className="border rounded p-3">
                        <h6 className="text-muted">Memory Usage</h6>
                        <div className="d-flex justify-content-between align-items-center mb-2">
                          <small>Used: {(healthData.system.memory.total_gb - healthData.system.memory.available_gb).toFixed(2)} GB</small>
                          <small>Available: {healthData.system.memory.available_gb} GB</small>
                        </div>
                        <div className="progress">
                          <div className="progress-bar" style={{width: `${healthData.system.memory.used_percent}%`}}>
                            {healthData.system.memory.used_percent}%
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  {healthData.system?.disk && (
                    <div className="col-12">
                      <div className="border rounded p-3">
                        <h6 className="text-muted">Disk Usage</h6>
                        <div className="d-flex justify-content-between align-items-center mb-2">
                          <small>Used: {(healthData.system.disk.total_gb - healthData.system.disk.free_gb).toFixed(2)} GB</small>
                          <small>Free: {healthData.system.disk.free_gb} GB</small>
                        </div>
                        <div className="progress">
                          <div className="progress-bar" style={{width: `${healthData.system.disk.used_percent}%`}}>
                            {healthData.system.disk.used_percent}%
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Dependencies */}
          <div className="col-lg-6">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title mb-0">
                  <i className="bi bi-box-seam me-2"></i>
                  Dependencies
                </h5>
              </div>
              <div className="card-body">
                {healthData.dependencies && Object.entries(healthData.dependencies).map(([name, status]) =>
                  renderDependencyStatus(name, status)
                )}
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="col-lg-6">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title mb-0">
                  <i className="bi bi-toggles me-2"></i>
                  Features
                </h5>
              </div>
              <div className="card-body">
                {healthData.features && Object.entries(healthData.features).map(([name, status]) =>
                  renderFeatureStatus(name, status)
                )}
              </div>
            </div>
          </div>

          {/* AI Provider Status */}
          <div className="col-lg-6">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title mb-0">
                  <i className="bi bi-robot me-2"></i>
                  AI Provider
                </h5>
              </div>
              <div className="card-body">
                {healthData.ai_provider && (
                  <div>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <span>Provider</span>
                      <span className="badge bg-primary">{healthData.ai_provider.provider}</span>
                    </div>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <span>Model</span>
                      <code>{healthData.ai_provider.model}</code>
                    </div>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <span>Configuration</span>
                      <span className={`badge bg-${healthData.ai_provider.configured ? 'success' : 'danger'}`}>
                        <i className={`bi ${healthData.ai_provider.configured ? 'bi-check-lg' : 'bi-x-lg'} me-1`}></i>
                        {healthData.ai_provider.configured ? 'Valid' : 'Invalid'}
                      </span>
                    </div>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <span>Connectivity</span>
                      <span className={`badge bg-${healthData.ai_provider.connectivity_test ? 'success' : 'warning'}`}>
                        <i className={`bi ${healthData.ai_provider.connectivity_test ? 'bi-wifi' : 'bi-wifi-off'} me-1`}></i>
                        {healthData.ai_provider.connectivity_test ? 'Connected' : 'Disconnected'}
                      </span>
                    </div>
                    {healthData.ai_provider.last_test && (
                      <small className="text-muted">
                        Last test: {formatTimestamp(healthData.ai_provider.last_test)}
                      </small>
                    )}
                    {healthData.ai_provider.connectivity_error && (
                      <div className="alert alert-warning mt-2 mb-0 small">
                        <i className="bi bi-exclamation-triangle me-1"></i>
                        {healthData.ai_provider.connectivity_error}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Environment Configuration */}
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">
                  <i className="bi bi-sliders me-2"></i>
                  Environment Configuration
                </h5>
              </div>
              <div className="card-body">
                <div className="row g-3">
                  {healthData.environment && Object.entries(healthData.environment).map(([key, value]) => (
                    <div key={key} className="col-md-6 col-lg-4">
                      <div className="border rounded p-3">
                        <h6 className="text-muted small mb-1">{key.replace(/_/g, ' ')}</h6>
                        <code className="small">
                          {typeof value === 'boolean' ? (value ? 'true' : 'false') : (value || 'Not set')}
                        </code>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Issues */}
          {(healthData.issues?.critical?.length > 0 || healthData.issues?.warnings?.length > 0) && (
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h5 className="card-title mb-0">
                    <i className="bi bi-exclamation-triangle me-2"></i>
                    Issues & Warnings
                  </h5>
                </div>
                <div className="card-body">
                  {healthData.issues.critical?.length > 0 && (
                    <div className="mb-3">
                      <h6 className="text-danger">Critical Issues</h6>
                      {healthData.issues.critical.map((issue, index) => (
                        <div key={index} className="alert alert-danger py-2">
                          <i className="bi bi-x-circle-fill me-2"></i>
                          {issue}
                        </div>
                      ))}
                    </div>
                  )}
                  {healthData.issues.warnings?.length > 0 && (
                    <div>
                      <h6 className="text-warning">Warnings</h6>
                      {healthData.issues.warnings.map((warning, index) => (
                        <div key={index} className="alert alert-warning py-2">
                          <i className="bi bi-exclamation-triangle-fill me-2"></i>
                          {warning}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Add some CSS for spinning animation */}
      <style jsx>{`
        .spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default AdminPage;