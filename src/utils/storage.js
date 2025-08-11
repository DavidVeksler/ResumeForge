/**
 * Browser Storage Utility for AI Resume Optimizer
 * Provides secure, persistent storage for user data and application state
 */

const STORAGE_KEYS = {
  RESUME_DATA: 'ai_resume_optimizer_resume_data',
  JOB_DESCRIPTION: 'ai_resume_optimizer_job_description',
  OPTIMIZATION_RESULTS: 'ai_resume_optimizer_optimization_results',
  USER_EMAIL: 'ai_resume_optimizer_user_email',
  APP_STATE: 'ai_resume_optimizer_app_state',
  USER_PREFERENCES: 'ai_resume_optimizer_user_preferences',
  RECENT_JOBS: 'ai_resume_optimizer_recent_jobs',
  CONVERSION_HISTORY: 'ai_resume_optimizer_conversion_history'
};

const STORAGE_VERSION = '1.0';

class StorageManager {
  constructor() {
    this.isLocalStorageAvailable = this.checkLocalStorageSupport();
    this.compressionEnabled = true;
    this.encryptionEnabled = false; // Set to true for production with proper key management
  }

  /**
   * Check if localStorage is available and functional
   */
  checkLocalStorageSupport() {
    try {
      const test = '__storage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch (e) {
      console.warn('localStorage is not available:', e);
      return false;
    }
  }

  /**
   * Get data from storage with error handling and validation
   */
  get(key, defaultValue = null) {
    if (!this.isLocalStorageAvailable) {
      return defaultValue;
    }

    try {
      const item = localStorage.getItem(key);
      if (item === null) {
        return defaultValue;
      }

      const parsedItem = JSON.parse(item);
      
      // Check for version compatibility
      if (parsedItem.version && parsedItem.version !== STORAGE_VERSION) {
        console.warn(`Storage version mismatch for key ${key}. Clearing outdated data.`);
        this.remove(key);
        return defaultValue;
      }

      // Check for expiration
      if (parsedItem.expires && Date.now() > parsedItem.expires) {
        this.remove(key);
        return defaultValue;
      }

      return parsedItem.data || parsedItem;
    } catch (error) {
      console.error(`Error retrieving data from storage for key ${key}:`, error);
      this.remove(key); // Remove corrupted data
      return defaultValue;
    }
  }

  /**
   * Store data with optional expiration and versioning
   */
  set(key, value, options = {}) {
    if (!this.isLocalStorageAvailable) {
      console.warn('localStorage not available, data will not persist');
      return false;
    }

    try {
      const dataToStore = {
        data: value,
        timestamp: Date.now(),
        version: STORAGE_VERSION
      };

      // Add expiration if specified
      if (options.expiresIn) {
        dataToStore.expires = Date.now() + options.expiresIn;
      }

      // Add metadata if specified
      if (options.metadata) {
        dataToStore.metadata = options.metadata;
      }

      const serializedData = JSON.stringify(dataToStore);
      
      // Check storage size limits
      if (serializedData.length > 5000000) { // 5MB limit
        console.warn(`Data too large for storage: ${serializedData.length} characters`);
        return false;
      }

      localStorage.setItem(key, serializedData);
      return true;
    } catch (error) {
      if (error.name === 'QuotaExceededError') {
        console.error('Storage quota exceeded. Attempting to clear old data...');
        this.cleanupExpiredData();
        try {
          localStorage.setItem(key, JSON.stringify({ data: value, timestamp: Date.now(), version: STORAGE_VERSION }));
          return true;
        } catch (retryError) {
          console.error('Failed to store data even after cleanup:', retryError);
          return false;
        }
      } else {
        console.error(`Error storing data for key ${key}:`, error);
        return false;
      }
    }
  }

  /**
   * Remove data from storage
   */
  remove(key) {
    if (!this.isLocalStorageAvailable) {
      return false;
    }

    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error(`Error removing data for key ${key}:`, error);
      return false;
    }
  }

  /**
   * Clear all application data
   */
  clear() {
    if (!this.isLocalStorageAvailable) {
      return false;
    }

    try {
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key);
      });
      return true;
    } catch (error) {
      console.error('Error clearing storage:', error);
      return false;
    }
  }

  /**
   * Clean up expired data
   */
  cleanupExpiredData() {
    if (!this.isLocalStorageAvailable) {
      return;
    }

    Object.values(STORAGE_KEYS).forEach(key => {
      try {
        const item = localStorage.getItem(key);
        if (item) {
          const parsedItem = JSON.parse(item);
          if (parsedItem.expires && Date.now() > parsedItem.expires) {
            localStorage.removeItem(key);
          }
        }
      } catch (error) {
        // Remove corrupted data
        localStorage.removeItem(key);
      }
    });
  }

  /**
   * Get storage usage statistics
   */
  getStorageStats() {
    if (!this.isLocalStorageAvailable) {
      return { used: 0, total: 0, available: 0 };
    }

    let used = 0;
    Object.values(STORAGE_KEYS).forEach(key => {
      const item = localStorage.getItem(key);
      if (item) {
        used += item.length;
      }
    });

    return {
      used: used,
      usedFormatted: this.formatBytes(used),
      total: 10 * 1024 * 1024, // Approximate 10MB limit
      available: (10 * 1024 * 1024) - used
    };
  }

  /**
   * Format bytes to human readable string
   */
  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// Create singleton instance
const storage = new StorageManager();

// Application-specific storage functions
export const AppStorage = {
  // Resume data persistence
  saveResumeData: (resumeData, fileName = null) => {
    return storage.set(STORAGE_KEYS.RESUME_DATA, {
      data: resumeData,
      fileName: fileName,
      lastModified: Date.now()
    }, { metadata: { type: 'resume' } });
  },

  getResumeData: () => {
    return storage.get(STORAGE_KEYS.RESUME_DATA);
  },

  clearResumeData: () => {
    return storage.remove(STORAGE_KEYS.RESUME_DATA);
  },

  // Job description persistence
  saveJobDescription: (jobDescription) => {
    return storage.set(STORAGE_KEYS.JOB_DESCRIPTION, {
      text: jobDescription,
      lastModified: Date.now()
    });
  },

  getJobDescription: () => {
    const stored = storage.get(STORAGE_KEYS.JOB_DESCRIPTION);
    return stored ? stored.text : null;
  },

  clearJobDescription: () => {
    return storage.remove(STORAGE_KEYS.JOB_DESCRIPTION);
  },

  // Optimization results persistence
  saveOptimizationResults: (results) => {
    return storage.set(STORAGE_KEYS.OPTIMIZATION_RESULTS, {
      ...results,
      savedAt: Date.now()
    }, { expiresIn: 24 * 60 * 60 * 1000 }); // Expire after 24 hours
  },

  getOptimizationResults: () => {
    return storage.get(STORAGE_KEYS.OPTIMIZATION_RESULTS);
  },

  clearOptimizationResults: () => {
    return storage.remove(STORAGE_KEYS.OPTIMIZATION_RESULTS);
  },

  // User email and preferences
  saveUserEmail: (email) => {
    return storage.set(STORAGE_KEYS.USER_EMAIL, email);
  },

  getUserEmail: () => {
    return storage.get(STORAGE_KEYS.USER_EMAIL);
  },

  // Application state persistence
  saveAppState: (state) => {
    return storage.set(STORAGE_KEYS.APP_STATE, {
      currentStep: state.currentStep,
      lastUsed: Date.now(),
      sessionId: Date.now().toString(36)
    });
  },

  getAppState: () => {
    return storage.get(STORAGE_KEYS.APP_STATE);
  },

  // User preferences
  saveUserPreferences: (preferences) => {
    return storage.set(STORAGE_KEYS.USER_PREFERENCES, {
      theme: preferences.theme || 'light',
      inputMethod: preferences.inputMethod || 'file',
      autoSave: preferences.autoSave !== false,
      notifications: preferences.notifications !== false,
      ...preferences
    });
  },

  getUserPreferences: () => {
    return storage.get(STORAGE_KEYS.USER_PREFERENCES, {
      theme: 'light',
      inputMethod: 'file',
      autoSave: true,
      notifications: true
    });
  },

  // Recent job descriptions for quick access
  addRecentJob: (jobDescription, title = null) => {
    const recent = storage.get(STORAGE_KEYS.RECENT_JOBS, []);
    const newJob = {
      id: Date.now().toString(),
      text: jobDescription.substring(0, 500), // Store first 500 chars
      title: title || 'Untitled Job',
      timestamp: Date.now()
    };

    // Add to beginning and limit to 5 recent jobs
    const updated = [newJob, ...recent.filter(job => job.text !== newJob.text)].slice(0, 5);
    return storage.set(STORAGE_KEYS.RECENT_JOBS, updated);
  },

  getRecentJobs: () => {
    return storage.get(STORAGE_KEYS.RECENT_JOBS, []);
  },

  // Conversion history for text-to-JSON feature
  addConversionHistory: (textResume, convertedData) => {
    const history = storage.get(STORAGE_KEYS.CONVERSION_HISTORY, []);
    const conversion = {
      id: Date.now().toString(),
      originalLength: textResume.length,
      convertedAt: Date.now(),
      success: !!convertedData,
      preview: textResume.substring(0, 100) + '...'
    };

    const updated = [conversion, ...history].slice(0, 10); // Keep last 10 conversions
    return storage.set(STORAGE_KEYS.CONVERSION_HISTORY, updated);
  },

  getConversionHistory: () => {
    return storage.get(STORAGE_KEYS.CONVERSION_HISTORY, []);
  },

  // Utility functions
  clearAllData: () => {
    return storage.clear();
  },

  getStorageStats: () => {
    return storage.getStorageStats();
  },

  cleanupExpiredData: () => {
    return storage.cleanupExpiredData();
  },

  // Auto-save functionality
  enableAutoSave: (callback, interval = 30000) => {
    return setInterval(() => {
      if (typeof callback === 'function') {
        callback();
      }
    }, interval);
  },

  disableAutoSave: (intervalId) => {
    if (intervalId) {
      clearInterval(intervalId);
    }
  }
};

// Export both the manager and the app-specific functions
export default AppStorage;
export { storage as StorageManager, STORAGE_KEYS };