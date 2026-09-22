import { useState, useCallback } from 'react';
import { optimizeResume } from '../services/api';
import AppStorage from '../utils/storage';

/**
 * Custom hook for managing resume optimization workflow
 * Handles loading states, progress tracking, and data persistence
 */
export const useResumeOptimization = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadingStep, setLoadingStep] = useState('');
  const [optimizationData, setOptimizationData] = useState(null);

  /**
   * Optimize resume with progress tracking and persistence
   */
  const optimize = useCallback(async (resumeData, jobDescription) => {
    setIsLoading(true);
    setError(null);

    try {
      // Save input data for persistence
      AppStorage.saveResumeData(resumeData);
      AppStorage.saveJobDescription(jobDescription);
      AppStorage.addRecentJob(jobDescription);

      // Progress step 1
      setLoadingStep('Analyzing job description...');
      await new Promise(resolve => setTimeout(resolve, 800)); // Brief pause for UX

      // Progress step 2
      setLoadingStep('Extracting keywords...');
      await new Promise(resolve => setTimeout(resolve, 600));

      // Progress step 3
      setLoadingStep('Optimizing resume content...');
      const result = await optimizeResume(resumeData, jobDescription);

      // Progress step 4
      setLoadingStep('Calculating ATS scores...');
      await new Promise(resolve => setTimeout(resolve, 400));

      // Save optimization results
      AppStorage.saveOptimizationResults(result);

      setOptimizationData(result);
      return result;
    } catch (err) {
      const errorMessage = err.message || 'An error occurred while optimizing your resume';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  }, []);

  /**
   * Clear optimization data
   */
  const clear = useCallback(() => {
    setOptimizationData(null);
    setError(null);
    setLoadingStep('');
  }, []);

  /**
   * Clear error
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    optimize,
    isLoading,
    error,
    loadingStep,
    optimizationData,
    clear,
    clearError,
    hasData: optimizationData !== null
  };
};

export default useResumeOptimization;
