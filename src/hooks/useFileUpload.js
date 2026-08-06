import { useState, useCallback } from 'react';
import { validateResume } from '../services/api';

/**
 * Custom hook for managing file upload state
 * Handles drag-and-drop, validation, and error states
 */
export const useFileUpload = () => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState('');
  const [validationWarnings, setValidationWarnings] = useState([]);
  const [isValidating, setIsValidating] = useState(false);

  /**
   * Handle drag over event
   */
  const handleDragOver = useCallback((e, disabled = false) => {
    e.preventDefault();
    e.stopPropagation();
    if (!disabled) {
      setIsDragOver(true);
    }
  }, []);

  /**
   * Handle drag leave event
   */
  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  /**
   * Handle drop event
   */
  const handleDrop = useCallback((e, disabled = false) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (disabled) return null;

    const files = Array.from(e.dataTransfer.files);
    return files.length > 0 ? files[0] : null;
  }, []);

  /**
   * Validate a file before processing
   */
  const validateFile = useCallback((file) => {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.json')) {
      setError('Please upload a JSON file (.json)');
      return false;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return false;
    }

    return true;
  }, []);

  /**
   * Process and validate file content
   */
  const processFile = useCallback(async (file) => {
    setError('');
    setValidationWarnings([]);

    if (!validateFile(file)) {
      return null;
    }

    setIsValidating(true);

    try {
      const text = await file.text();
      const data = JSON.parse(text);

      // Server-side validation
      try {
        const validation = await validateResume(data);

        if (!validation.valid) {
          setError(`Resume validation failed: ${validation.errors.join(', ')}`);
          setIsValidating(false);
          return null;
        }

        if (validation.warnings && validation.warnings.length > 0) {
          setValidationWarnings(validation.warnings);
        }

        setIsValidating(false);
        return { data, fileName: file.name };
      } catch (validationError) {
        // Fallback to basic validation if server is unavailable
        if (!data.personal || !data.personal.name) {
          setError('Invalid resume format: missing personal information');
          setIsValidating(false);
          return null;
        }

        setIsValidating(false);
        return { data, fileName: file.name };
      }
    } catch (err) {
      setError('Invalid JSON format. Please check your file.');
      setIsValidating(false);
      return null;
    }
  }, [validateFile]);

  /**
   * Clear all state
   */
  const reset = useCallback(() => {
    setError('');
    setValidationWarnings([]);
    setIsDragOver(false);
    setIsValidating(false);
  }, []);

  /**
   * Clear error
   */
  const clearError = useCallback(() => {
    setError('');
  }, []);

  return {
    isDragOver,
    error,
    validationWarnings,
    isValidating,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    validateFile,
    processFile,
    reset,
    clearError,
    hasError: !!error
  };
};

export default useFileUpload;
