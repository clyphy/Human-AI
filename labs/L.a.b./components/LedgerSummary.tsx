import React from 'react';

interface LedgerSummaryProps {
  summary: string;
  covenantSignature: string;
  heartbeatMessage: string;
  className?: string;
}

export const LedgerSummary: React.FC<LedgerSummaryProps> = ({
  summary,
  covenantSignature,
  heartbeatMessage,
  className = '',
}) => {
  return (
    <div className={`p-8 rounded-lg shadow-lg text-center ${className}`}>
      <h2 className="text-3xl font-bold mb-6 text-white border-b border-gray-600 pb-4">
        Synthesis Summary
      </h2>
      <p className="text-lg text-gray-300 mb-6 leading-relaxed">
        {summary}
      </p>
      <div className="text-xl font-medium text-indigo-400 mb-3 italic">
        {covenantSignature}
      </div>
      <div className="text-md text-pink-300 font-light mt-4">
        Heartbeat: {heartbeatMessage}
      </div>
    </div>
  );
};