/**
 * Unit Tests for TextResumeInput React Component
 * Tests the text resume input functionality and API integration
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TextResumeInput from '../TextResumeInput';
import * as api from '../../services/api';

// Mock the API module
jest.mock('../../services/api');

describe('TextResumeInput Component', () => {
  const mockOnResumeConverted = jest.fn();
  const mockOnError = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const renderComponent = (props = {}) => {
    return render(
      <TextResumeInput
        onResumeConverted={mockOnResumeConverted}
        onError={mockOnError}
        {...props}
      />
    );
  };

  test('renders component with correct elements', () => {
    renderComponent();
    
    expect(screen.getByText('Convert Text Resume')).toBeInTheDocument();
    expect(screen.getByText('Paste Your Resume Text')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /convert to json/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /clear/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /help/i })).toBeInTheDocument();
  });

  test('shows help section when help button is clicked', () => {
    renderComponent();
    
    const helpButton = screen.getByRole('button', { name: /help/i });
    fireEvent.click(helpButton);
    
    expect(screen.getByText('How to use:')).toBeInTheDocument();
    expect(screen.getByText(/Paste your existing resume text/)).toBeInTheDocument();
  });

  test('updates character count as user types', () => {
    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    fireEvent.change(textarea, { target: { value: 'Test resume content' } });
    
    expect(screen.getByText('(19 characters)')).toBeInTheDocument();
  });

  test('shows word count and validation messages', () => {
    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    fireEvent.change(textarea, { target: { value: 'Short text' } });
    
    expect(screen.getByText(/Word count: ~2 words/)).toBeInTheDocument();
    expect(screen.getByText(/Too short - add more details/)).toBeInTheDocument();
  });

  test('enables convert button only when text is sufficient', () => {
    renderComponent();
    
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    const textarea = screen.getByRole('textbox');
    
    // Initially disabled
    expect(convertButton).toBeDisabled();
    
    // Still disabled with short text
    fireEvent.change(textarea, { target: { value: 'Too short' } });
    expect(convertButton).toBeDisabled();
    
    // Enabled with sufficient text
    const longText = 'A'.repeat(150);
    fireEvent.change(textarea, { target: { value: longText } });
    expect(convertButton).not.toBeDisabled();
  });

  test('calls API and handles successful conversion', async () => {
    const mockResumeData = {
      personal: { name: 'John Doe', email: 'john@example.com' },
      experience: []
    };
    
    const mockValidation = {
      valid: true,
      errors: [],
      warnings: []
    };

    api.parseTextResume.mockResolvedValueOnce({
      resumeData: mockResumeData,
      validation: mockValidation
    });

    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    
    const resumeText = 'John Doe\nSoftware Engineer\njohn@example.com\n' + 'A'.repeat(100);
    fireEvent.change(textarea, { target: { value: resumeText } });
    fireEvent.click(convertButton);
    
    expect(screen.getByText('Converting with AI...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(api.parseTextResume).toHaveBeenCalledWith(resumeText);
      expect(mockOnResumeConverted).toHaveBeenCalledWith(mockResumeData, mockValidation);
    });
  });

  test('handles API error during conversion', async () => {
    const errorMessage = 'OpenAI API key not configured';
    api.parseTextResume.mockRejectedValueOnce(new Error(errorMessage));

    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    
    const resumeText = 'A'.repeat(150);
    fireEvent.change(textarea, { target: { value: resumeText } });
    fireEvent.click(convertButton);
    
    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith(errorMessage);
    });
  });

  test('shows error for empty input', () => {
    renderComponent();
    
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    fireEvent.click(convertButton);
    
    expect(mockOnError).toHaveBeenCalledWith('Please enter your resume text');
  });

  test('shows error for too short input', () => {
    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    
    fireEvent.change(textarea, { target: { value: 'Too short' } });
    fireEvent.click(convertButton);
    
    expect(mockOnError).toHaveBeenCalledWith('Resume text is too short. Please provide more detailed information.');
  });

  test('clears textarea when clear button is clicked', () => {
    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const clearButton = screen.getByRole('button', { name: /clear/i });
    
    fireEvent.change(textarea, { target: { value: 'Some text' } });
    expect(textarea.value).toBe('Some text');
    
    fireEvent.click(clearButton);
    expect(textarea.value).toBe('');
  });

  test('disables buttons during conversion', async () => {
    api.parseTextResume.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    const clearButton = screen.getByRole('button', { name: /clear/i });
    
    const resumeText = 'A'.repeat(150);
    fireEvent.change(textarea, { target: { value: resumeText } });
    fireEvent.click(convertButton);
    
    expect(convertButton).toBeDisabled();
    expect(clearButton).toBeDisabled();
    expect(textarea).toBeDisabled();
  });

  test('handles validation warnings in successful response', async () => {
    const mockResumeData = {
      personal: { name: 'John Doe' },
      experience: []
    };
    
    const mockValidation = {
      valid: false,
      errors: ['Missing email address'],
      warnings: ['Consider adding more details']
    };

    api.parseTextResume.mockResolvedValueOnce({
      resumeData: mockResumeData,
      validation: mockValidation
    });

    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    
    const resumeText = 'A'.repeat(150);
    fireEvent.change(textarea, { target: { value: resumeText } });
    fireEvent.click(convertButton);
    
    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith(
        expect.stringContaining('Conversion successful but validation found issues')
      );
    });
  });

  test('clears text after successful conversion', async () => {
    api.parseTextResume.mockResolvedValueOnce({
      resumeData: { personal: { name: 'John Doe' } },
      validation: { valid: true, errors: [], warnings: [] }
    });

    renderComponent();
    
    const textarea = screen.getByRole('textbox');
    const convertButton = screen.getByRole('button', { name: /convert to json/i });
    
    const resumeText = 'A'.repeat(150);
    fireEvent.change(textarea, { target: { value: resumeText } });
    fireEvent.click(convertButton);
    
    await waitFor(() => {
      expect(textarea.value).toBe('');
    });
  });
});