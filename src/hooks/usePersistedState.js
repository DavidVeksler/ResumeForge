import { useState, useEffect, useCallback } from 'react';
import AppStorage from '../utils/storage';

/**
 * Custom hook for state that persists to localStorage
 *
 * @param {string} key - Storage key
 * @param {*} defaultValue - Default value if not in storage
 * @returns {[any, Function]} - [value, setValue] tuple
 */
export const usePersistedState = (key, defaultValue) => {
  const [value, setValue] = useState(() => {
    try {
      const item = AppStorage.get(key);
      return item !== null ? item : defaultValue;
    } catch (error) {
      console.error(`Error loading ${key} from storage:`, error);
      return defaultValue;
    }
  });

  useEffect(() => {
    try {
      if (value !== null && value !== undefined) {
        AppStorage.save(key, value);
      }
    } catch (error) {
      console.error(`Error saving ${key} to storage:`, error);
    }
  }, [key, value]);

  return [value, setValue];
};

/**
 * Custom hook for resume data with validation
 */
export const useResumeData = () => {
  const [data, setData] = usePersistedState('resumeData', null);
  const [fileName, setFileName] = usePersistedState('resumeFileName', '');
  const [validationErrors, setValidationErrors] = useState([]);

  const updateData = useCallback((newData) => {
    setData(newData);
    setValidationErrors([]);
  }, [setData]);

  const clearData = useCallback(() => {
    setData(null);
    setFileName('');
    setValidationErrors([]);
  }, [setData, setFileName]);

  const validate = useCallback(() => {
    if (!data) {
      setValidationErrors(['No resume data']);
      return false;
    }

    const errors = [];
    if (!data.personal?.name) errors.push('Missing personal name');
    if (!data.personal?.email) errors.push('Missing personal email');
    if (!data.experience?.length) errors.push('Missing experience');

    setValidationErrors(errors);
    return errors.length === 0;
  }, [data]);

  return {
    data,
    fileName,
    validationErrors,
    setData: updateData,
    setFileName,
    clearData,
    validate,
    isValid: data !== null && validationErrors.length === 0
  };
};

/**
 * Custom hook for job description management
 */
export const useJobDescription = () => {
  const [description, setDescription] = usePersistedState('jobDescription', '');
  const [wordCount, setWordCount] = useState(0);

  useEffect(() => {
    if (description) {
      const words = description.trim().split(/\s+/).length;
      setWordCount(words);
    } else {
      setWordCount(0);
    }
  }, [description]);

  const clear = useCallback(() => {
    setDescription('');
  }, [setDescription]);

  const isValid = description.trim().length > 50;

  return {
    value: description,
    setValue: setDescription,
    clear,
    wordCount,
    isValid
  };
};

/**
 * Custom hook for optimization results
 */
export const useOptimizationResults = () => {
  const [results, setResults] = usePersistedState('optimizationResults', null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const clear = useCallback(() => {
    setResults(null);
    setError(null);
  }, [setResults]);

  const setLoadingState = useCallback((loading) => {
    setIsLoading(loading);
    if (loading) {
      setError(null);
    }
  }, []);

  return {
    results,
    setResults,
    isLoading,
    setIsLoading: setLoadingState,
    error,
    setError,
    clear,
    hasResults: results !== null
  };
};

export default usePersistedState;
