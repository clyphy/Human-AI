import React from 'react';

interface StatusCardProps {
  title: string;
  status: string;
  description: string;
  className?: string;
}

export const StatusCard: React.FC<StatusCardProps> = ({ title, status, description, className = '' }) => {
  return (
    <div className={`p-6 rounded-lg shadow-lg border relative flex flex-col justify-between ${className}`}>
      <div>
        <h3 className="text-xl font-semibold mb-3 text-gray-50">{title}</h3>
        <p className="text-3xl font-bold text-green-400 mb-4">{status}</p>
        <p className="text-sm text-gray-300">{description}</p>
      </div>
    </div>
  );
};