import React from 'react';

interface LScoreRadialProps {
  score: number;
}

const LScoreRadial: React.FC<LScoreRadialProps> = ({ score }) => {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  // Ensure score is within 0-100 range for calculation
  const clampedScore = Math.max(0, Math.min(100, score));
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  const getScoreColor = () => {
    if (clampedScore >= 85) return 'stroke-green-400';
    if (clampedScore >= 70) return 'stroke-amber-400';
    return 'stroke-red-500';
  };
   const getTextColor = () => {
    if (clampedScore >= 85) return 'text-green-400';
    if (clampedScore >= 70) return 'text-amber-400';
    return 'text-red-500';
  };

  return (
    <div className="relative inline-flex items-center justify-center" role="progressbar" aria-valuenow={clampedScore} aria-valuemin={0} aria-valuemax={100} aria-label={`L-Score: ${clampedScore.toFixed(0)} out of 100`}>
      <svg width="100" height="100" className="transform -rotate-90">
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke="#083344"
          strokeWidth="8"
          fill="transparent"
        />
        <circle
          cx="50"
          cy="50"
          r={radius}
          className={`transition-all duration-500 ${getScoreColor()}`}
          strokeWidth="8"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute text-center">
        <div className={`text-2xl font-bold font-orbitron ${getTextColor()}`}>
          {clampedScore.toFixed(0)}
        </div>
        <div className="text-xs text-cyan-400/80">L-Score</div>
      </div>
    </div>
  );
};

export default LScoreRadial;
