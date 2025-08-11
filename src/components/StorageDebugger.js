import React, { useState, useEffect } from 'react';
import AppStorage from '../utils/storage';

const StorageDebugger = ({ show, onClose }) => {
  const [storageStats, setStorageStats] = useState({});
  const [storageData, setStorageData] = useState({});

  useEffect(() => {
    if (show) {
      loadStorageInfo();
    }
  }, [show]);

  const loadStorageInfo = () => {
    const stats = AppStorage.getStorageStats();
    setStorageStats(stats);

    const data = {
      resumeData: AppStorage.getResumeData(),
      jobDescription: AppStorage.getJobDescription(),
      optimizationResults: AppStorage.getOptimizationResults(),
      userEmail: AppStorage.getUserEmail(),
      appState: AppStorage.getAppState(),
      userPreferences: AppStorage.getUserPreferences(),
      recentJobs: AppStorage.getRecentJobs(),
      conversionHistory: AppStorage.getConversionHistory()
    };
    setStorageData(data);
  };

  const clearAllStorage = () => {
    if (window.confirm('Are you sure you want to clear all stored data? This cannot be undone.')) {
      AppStorage.clearAllData();
      loadStorageInfo();
      alert('All storage data has been cleared.');
    }
  };

  if (!show) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              <i className="bi bi-hdd-stack me-2"></i>
              Storage Debug Information
            </h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          
          <div className="modal-body">
            {/* Storage Statistics */}
            <div className="mb-4">
              <h6>Storage Statistics</h6>
              <div className="row g-3">
                <div className="col-md-4">
                  <div className="card">
                    <div className="card-body text-center">
                      <div className="h5 text-primary">{storageStats.usedFormatted || '0 Bytes'}</div>
                      <small className="text-muted">Used</small>
                    </div>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card">
                    <div className="card-body text-center">
                      <div className="h5 text-info">~10 MB</div>
                      <small className="text-muted">Available</small>
                    </div>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card">
                    <div className="card-body text-center">
                      <div className="h5 text-success">
                        {Object.values(storageData).filter(Boolean).length}
                      </div>
                      <small className="text-muted">Stored Items</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Stored Data Overview */}
            <div className="mb-4">
              <h6>Stored Data</h6>
              <div className="table-responsive">
                <table className="table table-sm">
                  <thead>
                    <tr>
                      <th>Data Type</th>
                      <th>Status</th>
                      <th>Size</th>
                      <th>Last Modified</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Resume Data</td>
                      <td>
                        {storageData.resumeData ? (
                          <span className="badge bg-success">Stored</span>
                        ) : (
                          <span className="badge bg-secondary">Empty</span>
                        )}
                      </td>
                      <td>
                        {storageData.resumeData ? 
                          `${JSON.stringify(storageData.resumeData).length} chars` : 
                          '0 chars'
                        }
                      </td>
                      <td>
                        {storageData.resumeData?.lastModified ? 
                          new Date(storageData.resumeData.lastModified).toLocaleString() : 
                          'Never'
                        }
                      </td>
                    </tr>
                    
                    <tr>
                      <td>Job Description</td>
                      <td>
                        {storageData.jobDescription ? (
                          <span className="badge bg-success">Stored</span>
                        ) : (
                          <span className="badge bg-secondary">Empty</span>
                        )}
                      </td>
                      <td>
                        {storageData.jobDescription ? 
                          `${storageData.jobDescription.length} chars` : 
                          '0 chars'
                        }
                      </td>
                      <td>-</td>
                    </tr>
                    
                    <tr>
                      <td>Optimization Results</td>
                      <td>
                        {storageData.optimizationResults ? (
                          <span className="badge bg-success">Stored</span>
                        ) : (
                          <span className="badge bg-secondary">Empty</span>
                        )}
                      </td>
                      <td>
                        {storageData.optimizationResults ? 
                          `${JSON.stringify(storageData.optimizationResults).length} chars` : 
                          '0 chars'
                        }
                      </td>
                      <td>
                        {storageData.optimizationResults?.savedAt ? 
                          new Date(storageData.optimizationResults.savedAt).toLocaleString() : 
                          'Never'
                        }
                      </td>
                    </tr>
                    
                    <tr>
                      <td>User Email</td>
                      <td>
                        {storageData.userEmail ? (
                          <span className="badge bg-success">Stored</span>
                        ) : (
                          <span className="badge bg-secondary">Empty</span>
                        )}
                      </td>
                      <td>
                        {storageData.userEmail ? 
                          `${storageData.userEmail.length} chars` : 
                          '0 chars'
                        }
                      </td>
                      <td>-</td>
                    </tr>
                    
                    <tr>
                      <td>Recent Jobs</td>
                      <td>
                        {storageData.recentJobs?.length > 0 ? (
                          <span className="badge bg-success">{storageData.recentJobs.length} items</span>
                        ) : (
                          <span className="badge bg-secondary">Empty</span>
                        )}
                      </td>
                      <td>
                        {storageData.recentJobs ? 
                          `${JSON.stringify(storageData.recentJobs).length} chars` : 
                          '0 chars'
                        }
                      </td>
                      <td>-</td>
                    </tr>
                    
                    <tr>
                      <td>Conversion History</td>
                      <td>
                        {storageData.conversionHistory?.length > 0 ? (
                          <span className="badge bg-success">{storageData.conversionHistory.length} items</span>
                        ) : (
                          <span className="badge bg-secondary">Empty</span>
                        )}
                      </td>
                      <td>
                        {storageData.conversionHistory ? 
                          `${JSON.stringify(storageData.conversionHistory).length} chars` : 
                          '0 chars'
                        }
                      </td>
                      <td>-</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* User Preferences */}
            {storageData.userPreferences && (
              <div className="mb-4">
                <h6>User Preferences</h6>
                <div className="card">
                  <div className="card-body">
                    <pre className="mb-0" style={{ fontSize: '0.85rem' }}>
                      {JSON.stringify(storageData.userPreferences, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-outline-danger"
              onClick={clearAllStorage}
            >
              <i className="bi bi-trash3 me-1"></i>
              Clear All Storage
            </button>
            <button 
              type="button" 
              className="btn btn-outline-secondary"
              onClick={loadStorageInfo}
            >
              <i className="bi bi-arrow-clockwise me-1"></i>
              Refresh
            </button>
            <button type="button" className="btn btn-primary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StorageDebugger;