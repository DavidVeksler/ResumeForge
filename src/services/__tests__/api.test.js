/**
 * Unit Tests for API Service - Text Resume Parsing
 * Tests the parseTextResume API function with various scenarios
 */

import axios from 'axios';
import { parseTextResume } from '../api';

// Mock axios
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    post: jest.fn(),
    get: jest.fn(),
  })),
}));

describe('API Service - parseTextResume', () => {
  let mockAxiosInstance;

  beforeEach(() => {
    mockAxiosInstance = {
      post: jest.fn(),
      get: jest.fn(),
    };
    axios.create.mockReturnValue(mockAxiosInstance);
    jest.clearAllMocks();
  });

  const sampleTextResume = `
    John Smith
    Senior Software Engineer
    john.smith@example.com | (555) 123-4567 | San Francisco, CA
    
    EXPERIENCE
    Senior Engineer | TechCorp | 2020-Present
    • Built scalable systems serving 1M+ users
    • Led team of 5 engineers
  `;

  const sampleResumeData = {
    personal: {
      name: 'John Smith',
      email: 'john.smith@example.com',
      phone: '(555) 123-4567',
      location: 'San Francisco, CA'
    },
    experience: [
      {
        title: 'Senior Engineer',
        company: 'TechCorp',
        duration: '2020-Present',
        achievements: [
          {
            text: 'Built scalable systems serving 1M+ users',
            keywords: ['scalable', 'systems'],
            metrics: { value: 1000000, type: 'users' }
          }
        ]
      }
    ]
  };

  test('successful text resume parsing', async () => {
    const mockResponse = {
      data: {
        success: true,
        resumeData: sampleResumeData,
        validation: {
          valid: true,
          errors: [],
          warnings: []
        },
        message: 'Resume successfully converted to structured JSON format'
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    const result = await parseTextResume(sampleTextResume);

    expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/parse-resume', {
      textResume: sampleTextResume,
    });

    expect(result).toEqual(mockResponse.data);
    expect(result.success).toBe(true);
    expect(result.resumeData).toEqual(sampleResumeData);
  });

  test('handles server error with error message', async () => {
    const errorResponse = {
      response: {
        data: {
          error: 'OpenAI API key not configured'
        }
      }
    };

    mockAxiosInstance.post.mockRejectedValueOnce(errorResponse);

    await expect(parseTextResume(sampleTextResume)).rejects.toThrow(
      'OpenAI API key not configured'
    );

    expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/parse-resume', {
      textResume: sampleTextResume,
    });
  });

  test('handles network error', async () => {
    const networkError = {
      request: {}
    };

    mockAxiosInstance.post.mockRejectedValueOnce(networkError);

    await expect(parseTextResume(sampleTextResume)).rejects.toThrow(
      'Unable to connect to the server. Please check if the backend is running.'
    );
  });

  test('handles generic error', async () => {
    const genericError = new Error('Something went wrong');

    mockAxiosInstance.post.mockRejectedValueOnce(genericError);

    await expect(parseTextResume(sampleTextResume)).rejects.toThrow(
      'An unexpected error occurred during text resume parsing'
    );
  });

  test('handles unsuccessful response from server', async () => {
    const mockResponse = {
      data: {
        success: false,
        error: 'Text resume parsing failed'
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    await expect(parseTextResume(sampleTextResume)).rejects.toThrow(
      'Text resume parsing failed'
    );
  });

  test('handles server error without specific error message', async () => {
    const errorResponse = {
      response: {
        data: {}
      }
    };

    mockAxiosInstance.post.mockRejectedValueOnce(errorResponse);

    await expect(parseTextResume(sampleTextResume)).rejects.toThrow(
      'Server error occurred during parsing'
    );
  });

  test('handles response with validation warnings', async () => {
    const mockResponse = {
      data: {
        success: true,
        resumeData: sampleResumeData,
        validation: {
          valid: true,
          errors: [],
          warnings: ['Consider adding more quantified achievements']
        },
        message: 'Resume successfully converted to structured JSON format'
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    const result = await parseTextResume(sampleTextResume);

    expect(result.validation.warnings).toHaveLength(1);
    expect(result.validation.warnings[0]).toBe('Consider adding more quantified achievements');
  });

  test('handles response with validation errors', async () => {
    const mockResponse = {
      data: {
        success: true,
        resumeData: sampleResumeData,
        validation: {
          valid: false,
          errors: ['Missing required field: email'],
          warnings: []
        },
        message: 'Resume successfully converted to structured JSON format'
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    const result = await parseTextResume(sampleTextResume);

    expect(result.validation.valid).toBe(false);
    expect(result.validation.errors).toHaveLength(1);
    expect(result.validation.errors[0]).toBe('Missing required field: email');
  });

  test('sends correct payload structure', async () => {
    const mockResponse = {
      data: {
        success: true,
        resumeData: sampleResumeData,
        validation: { valid: true, errors: [], warnings: [] }
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    await parseTextResume(sampleTextResume);

    const [endpoint, payload] = mockAxiosInstance.post.mock.calls[0];
    
    expect(endpoint).toBe('/api/parse-resume');
    expect(payload).toEqual({
      textResume: sampleTextResume
    });
    expect(typeof payload.textResume).toBe('string');
  });

  test('handles empty response data', async () => {
    const mockResponse = {
      data: null
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    await expect(parseTextResume(sampleTextResume)).rejects.toThrow(
      'Text resume parsing failed'
    );
  });

  test('processes large resume text', async () => {
    const largeResumeText = 'Large resume content '.repeat(1000);
    
    const mockResponse = {
      data: {
        success: true,
        resumeData: sampleResumeData,
        validation: { valid: true, errors: [], warnings: [] }
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(mockResponse);

    const result = await parseTextResume(largeResumeText);

    expect(result.success).toBe(true);
    expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/parse-resume', {
      textResume: largeResumeText,
    });
  });
});

describe('API Service - Integration Tests', () => {
  let mockAxiosInstance;

  beforeEach(() => {
    mockAxiosInstance = {
      post: jest.fn(),
      get: jest.fn(),
    };
    axios.create.mockReturnValue(mockAxiosInstance);
    jest.clearAllMocks();
  });

  test('parseTextResume integrates correctly with other API functions', async () => {
    // Mock successful parseTextResume
    const parseResponse = {
      data: {
        success: true,
        resumeData: sampleResumeData,
        validation: { valid: true, errors: [], warnings: [] }
      }
    };

    mockAxiosInstance.post.mockResolvedValueOnce(parseResponse);

    const result = await parseTextResume('test resume');
    
    // Verify the result could be used with other API functions
    expect(result.resumeData).toBeDefined();
    expect(result.resumeData.personal).toBeDefined();
    expect(result.resumeData.experience).toBeInstanceOf(Array);
    
    // This structure should be compatible with optimizeResume function
    expect(typeof result.resumeData).toBe('object');
  });
});