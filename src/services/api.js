import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const optimizeResume = async (resumeData, jobDescription) => {
  try {
    const response = await api.post('/api/optimize', {
      resumeData,
      jobDescription,
    });
    
    if (response.data.success) {
      return response.data;
    } else {
      throw new Error(response.data.error || 'Optimization failed');
    }
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Server error occurred');
    } else if (error.request) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    } else {
      throw new Error('An unexpected error occurred');
    }
  }
};

export const exportPDF = async (htmlContent, filename = 'resume.pdf') => {
  try {
    const response = await api.post('/api/export-pdf', {
      html: htmlContent,
      filename: filename,
    }, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    return { success: true };
  } catch (error) {
    throw new Error(error.response?.data?.error || 'PDF export failed');
  }
};

export const validateResume = async (resumeData) => {
  try {
    const response = await api.post('/api/validate-resume', {
      resumeData,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Resume validation failed');
  }
};

export const getSampleResume = async () => {
  try {
    const response = await api.get('/api/sample-resume');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to load sample resume');
  }
};

export const parseTextResume = async (textResume) => {
  try {
    const response = await api.post('/api/parse-resume', {
      textResume,
    });
    
    if (response.data.success) {
      return response.data;
    } else {
      throw new Error(response.data.error || 'Text resume parsing failed');
    }
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Server error occurred during parsing');
    } else if (error.request) {
      throw new Error('Unable to connect to the server. Please check if the backend is running.');
    } else {
      throw new Error('An unexpected error occurred during text resume parsing');
    }
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend service is not available');
  }
};

export default api;