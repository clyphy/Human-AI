
import React from 'react';
import { NexusIcon } from './icons/NexusIcon';

const Header: React.FC = () => {
  return (
    <header className="bg-gray-900/50 backdrop-blur-sm border-b border-cyan-500/20 shadow-lg shadow-cyan-900/50 sticky top-0 z-10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <NexusIcon className="h-8 w-8 text-cyan-400" />
            <h1 className="text-xl md:text-2xl font-bold font-orbitron text-cyan-300 tracking-wider">
              Prophetic Nexus Dashboard
            </h1>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
