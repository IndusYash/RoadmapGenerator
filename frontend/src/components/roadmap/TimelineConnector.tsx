import React from 'react';

interface TimelineConnectorProps {
  isLast?: boolean;
}

export const TimelineConnector: React.FC<TimelineConnectorProps> = ({ isLast = false }) => {
  if (isLast) return null;

  return (
    <div className="flex justify-center my-1">
      <div className="flex flex-col items-center">
        <div className="w-px h-6 bg-gradient-to-b from-indigo-500/40 to-slate-700/30" />
        <div className="w-1.5 h-1.5 rounded-full bg-indigo-500/40" />
        <div className="w-px h-6 bg-gradient-to-b from-slate-700/30 to-transparent" />
      </div>
    </div>
  );
};
