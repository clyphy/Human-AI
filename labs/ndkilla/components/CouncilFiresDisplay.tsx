
import React from 'react';
import { CouncilFire } from '../types';

interface CouncilFiresDisplayProps {
  activeFire?: CouncilFire;
}

export const CouncilFiresDisplay: React.FC<CouncilFiresDisplayProps> = ({ activeFire }) => {
  const fires = Object.values(CouncilFire);

  return (
    <div className="grid grid-cols-7 gap-2 p-4 bg-teal-950/20 border-t border-teal-900/30">
      {fires.map((fire) => (
        <div 
          key={fire}
          className={`flex flex-col items-center transition-all duration-700 ${
            activeFire === fire ? 'opacity-100 scale-110' : 'opacity-40 scale-100'
          }`}
        >
          <div className={`w-3 h-3 rounded-full mb-1 ${
            activeFire === fire ? 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.8)]' : 'bg-teal-800'
          }`} />
          <span className="text-[9px] font-mono uppercase tracking-tighter text-center">
            {fire}
          </span>
        </div>
      ))}
    </div>
  );
};
