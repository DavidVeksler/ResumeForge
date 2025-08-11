import React, { useRef, useState } from 'react';
import { exportPDF } from '../services/api';

const ResumeDisplay = ({ html, isOptimized }) => {
  const resumeRef = useRef(null);
  const [isExportingPDF, setIsExportingPDF] = useState(false);

  const handleDownload = () => {
    if (!html) return;
    
    const fileName = `resume_${isOptimized ? 'optimized' : 'default'}_${new Date().toISOString().split('T')[0]}.html`;
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(html);
      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
      printWindow.close();
    }
  };

  const handleExportPDF = async () => {
    if (!html) return;
    
    setIsExportingPDF(true);
    try {
      const fileName = `resume_${isOptimized ? 'optimized' : 'default'}_${new Date().toISOString().split('T')[0]}.pdf`;
      await exportPDF(html, fileName);
    } catch (error) {
      console.error('PDF export failed:', error);
      // Could add a toast notification here
      alert('PDF export failed. Please try again or use the download HTML option.');
    } finally {
      setIsExportingPDF(false);
    }
  };

  return (
    <div className="resume-paper" ref={resumeRef}>
      {/* Action buttons */}
      <div className="position-absolute top-0 end-0 m-3">
        <div className="btn-group">
          <button 
            className="btn btn-primary btn-sm"
            onClick={handleExportPDF}
            title="Export as PDF"
            disabled={isExportingPDF}
          >
            {isExportingPDF ? (
              <>
                <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                Exporting...
              </>
            ) : (
              <>
                <i className="bi bi-file-earmark-pdf me-1"></i>
                PDF
              </>
            )}
          </button>
          <button 
            className="btn btn-outline-primary btn-sm"
            onClick={handleDownload}
            title="Download HTML"
          >
            <i className="bi bi-download me-1"></i>
            HTML
          </button>
          <button 
            className="btn btn-outline-primary btn-sm"
            onClick={handlePrint}
            title="Print Resume"
          >
            <i className="bi bi-printer me-1"></i>
            Print
          </button>
        </div>
      </div>

      {/* Resume content */}
      <div 
        dangerouslySetInnerHTML={{ __html: html || '<p>No resume content available</p>' }}
        style={{ 
          minHeight: '800px',
          fontFamily: 'Inter, sans-serif',
          lineHeight: '1.6'
        }}
      />
    </div>
  );
};

export default ResumeDisplay;