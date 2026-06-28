import React from 'react';

interface WatchmanVisualProps {
  isActive: boolean;
}

export const WatchmanVisual: React.FC<WatchmanVisualProps> = ({ isActive }) => {
  return (
    <div className="flex justify-center items-center mt-6">
      <svg
        className={`h-24 w-24 transition-colors duration-500 ${isActive ? 'text-indigo-400' : 'text-gray-500'} animate-fade-in`}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Eye icon for the Watchman */}
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
        ></path>
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
        ></path>
      </svg>
    </div>
  );
};