import { useState, useEffect, useCallback } from 'react';
import AppStorage from '../utils/storage';

/**
 * Custom hook for managing application-level state
 * Handles routing, auto-save, and persistence
 */
export const useAppState = () => {
  // Initialize state based on URL or persisted data
  const getInitialStep = useCallback(() => {
    const path = window.location.pathname;
    if (path === '/admin' || path === '/admin/') {
      return 'admin';
    }

    // Try to restore from persisted state
    const savedState = AppStorage.getAppState();
    if (savedState && savedState.currentStep && savedState.currentStep !== 'landing') {
      const timeSinceLastUse = Date.now() - (savedState.lastUsed || 0);
      const maxRestoreTime = 24 * 60 * 60 * 1000; // 24 hours

      if (timeSinceLastUse < maxRestoreTime) {
        return savedState.currentStep;
      }
    }

    return 'landing';
  }, []);

  const [currentStep, setCurrentStep] = useState(getInitialStep);
  const [autoSaveInterval, setAutoSaveInterval] = useState(null);

  // Handle browser back/forward buttons
  useEffect(() => {
    const handlePopState = () => {
      setCurrentStep(getInitialStep());
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, [getInitialStep]);

  // Save app state when it changes
  useEffect(() => {
    if (currentStep !== 'landing') {
      AppStorage.saveAppState({
        currentStep,
        lastUsed: Date.now()
      });
    }
  }, [currentStep]);

  // Setup auto-save on mount
  useEffect(() => {
    const userPreferences = AppStorage.getUserPreferences();
    if (userPreferences.autoSave) {
      const interval = AppStorage.enableAutoSave(() => {
        if (currentStep !== 'landing') {
          AppStorage.saveAppState({
            currentStep,
            lastUsed: Date.now()
          });
        }
      }, 30000); // Auto-save every 30 seconds

      setAutoSaveInterval(interval);
    }

    // Cleanup expired data
    AppStorage.cleanupExpiredData();

    return () => {
      if (autoSaveInterval) {
        AppStorage.disableAutoSave(autoSaveInterval);
      }
    };
  }, [currentStep]);

  // Navigation functions
  const navigateToStep = useCallback((step, pushState = true) => {
    setCurrentStep(step);
    if (pushState) {
      const path = step === 'admin' ? '/admin' : '/';
      window.history.pushState({}, '', path);
    }
  }, []);

  const goToLanding = useCallback(() => {
    navigateToStep('landing');
  }, [navigateToStep]);

  const goToInput = useCallback(() => {
    navigateToStep('input');
  }, [navigateToStep]);

  const goToResults = useCallback(() => {
    navigateToStep('results');
  }, [navigateToStep]);

  const goToAdmin = useCallback(() => {
    navigateToStep('admin');
  }, [navigateToStep]);

  return {
    currentStep,
    setCurrentStep: navigateToStep,
    goToLanding,
    goToInput,
    goToResults,
    goToAdmin
  };
};

export default useAppState;
