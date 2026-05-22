import React, { useState } from 'react';
import { exportToPDF } from '../../utils/pdfExporter';

interface ExportButtonProps {
  elementId: string;
  userName?: string;
  className?: string;
}

export const ExportButton: React.FC<ExportButtonProps> = ({ elementId, userName, className = '' }) => {
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    setExporting(true);
    const filename = userName 
      ? `${userName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-career-roadmap.pdf` 
      : 'career-roadmap.pdf';
    
    try {
      await exportToPDF(elementId, filename);
    } catch (error) {
      console.error('Failed to export roadmap to PDF:', error);
    } finally {
      setExporting(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={exporting}
      className={`no-print flex items-center gap-2 border border-[#2e2e2e] bg-[#0f0f0f] px-3.5 py-1.5 font-mono text-[11px] font-medium tracking-tight text-[#e4e4e7] hover:border-[#444] hover:bg-[#161616] hover:text-white disabled:opacity-50 transition-all duration-150 rounded active:scale-[0.98] ${className}`}
      title="Export Roadmap as high-fidelity PDF"
    >
      {exporting ? (
        <>
          <svg className="animate-spin h-3.5 w-3.5 text-[#a1a1aa]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>PREPARING...</span>
        </>
      ) : (
        <>
          <svg className="w-3.5 h-3.5 text-[#a1a1aa] group-hover:text-white transition-colors" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
          </svg>
          <span>EXPORT PDF</span>
        </>
      )}
    </button>
  );
};
