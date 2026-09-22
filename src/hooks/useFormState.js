import { useState, useCallback } from 'react';

/**
 * Custom hook for managing form state with validation
 */
export const useFormState = (initialValue = '', validator = null) => {
  const [value, setValue] = useState(initialValue);
  const [error, setError] = useState('');
  const [touched, setTouched] = useState(false);

  /**
   * Handle input change
   */
  const handleChange = useCallback((e) => {
    const newValue = e.target?.value ?? e;
    setValue(newValue);

    if (touched && validator) {
      const validationError = validator(newValue);
      setError(validationError || '');
    }
  }, [touched, validator]);

  /**
   * Handle blur event
   */
  const handleBlur = useCallback(() => {
    setTouched(true);

    if (validator) {
      const validationError = validator(value);
      setError(validationError || '');
    }
  }, [value, validator]);

  /**
   * Validate the current value
   */
  const validate = useCallback(() => {
    setTouched(true);

    if (validator) {
      const validationError = validator(value);
      setError(validationError || '');
      return !validationError;
    }

    return true;
  }, [value, validator]);

  /**
   * Reset form state
   */
  const reset = useCallback(() => {
    setValue(initialValue);
    setError('');
    setTouched(false);
  }, [initialValue]);

  /**
   * Clear error
   */
  const clearError = useCallback(() => {
    setError('');
  }, []);

  return {
    value,
    setValue,
    error,
    touched,
    handleChange,
    handleBlur,
    validate,
    reset,
    clearError,
    isValid: !error && (validator ? !validator(value) : true)
  };
};

export default useFormState;
