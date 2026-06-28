
import React from 'react';
import { CardProps } from '../types';

const Card: React.FC<CardProps> = ({ title, icon, children, className = '', contentClassName = '' }) => {
  return (
    <div className={`bg-gray-800/50 border border-cyan-800/50 rounded-lg shadow-lg shadow-cyan-900/20 backdrop-blur-md flex flex-col ${className}`}>
      <div className="p-4 border-b border-cyan-800/50 flex items-center justify-between flex-shrink-0">
        <h2 className="text-lg font-orbitron font-bold text-cyan-400">{title}</h2>
        {icon}
      </div>
      <div className={`p-4 md:p-6 flex-grow min-h-0 ${contentClassName}`}>
        {children}
      </div>
    </div>
  );
};

export default Card;