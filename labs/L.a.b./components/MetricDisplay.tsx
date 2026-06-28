import React from 'react';

interface MetricDisplayProps {
  title: string;
  value: number;
  unit: string;
  description: string;
  progressMax?: number;
  progressValue?: number;
  progressColor?: string;
  className?: string;
  children?: React.ReactNode;
}

export const MetricDisplay: React.FC<MetricDisplayProps> = ({
  title,
  value,
  unit,
  description,
  progressMax,
  progressValue,
  progressColor = 'bg-indigo-500',
  className = '',
  children,
}) => {
  const displayValue = value.toFixed(2);
  const percentage = (progressMax && progressValue !== undefined)
    ? (progressValue / progressMax) * 100
    : undefined;

  return (
    <div className={`p-6 rounded-lg shadow-lg border relative flex flex-col justify-between ${className}`}>
      <div>
        <h3 className="text-xl font-semibold mb-3 text-gray-50">{title}</h3>
        <p className="text-4xl font-bold text-white mb-4">
          {displayValue} <span className="text-indigo-300 text-xl">{unit}</span>
        </p>
        <p className="text-sm text-gray-300">{description}</p>
      </div>
      {percentage !== undefined && (
        <div className="w-full bg-gray-600 rounded-full h-2.5 mt-4">
          <div
            className={`h-2.5 rounded-full ${progressColor}`}
            style={{ width: `${percentage}%` }}
          ></div>
        </div>
      )}
      {children}
    </div>
  );
};