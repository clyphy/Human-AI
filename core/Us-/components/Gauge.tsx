import React from 'react';

interface GaugeProps {
  value: number;
  max: number;
}

const Gauge: React.FC<GaugeProps> = ({ value, max }) => {
  const percentage = Math.max(0, Math.min(100, (value / max) * 100));
  const color = percentage > 85 ? '#4ade80' : percentage > 70 ? '#facc15' : '#f87171'; // green, yellow, red

  return (
    <div className="w-full bg-gray-700 rounded-full h-2.5 my-2">
      <div
        className="h-2.5 rounded-full"
        style={{ width: `${percentage}%`, backgroundColor: color, transition: 'width 0.5s ease-in-out' }}
      ></div>
    </div>
  );
};

export default Gauge;
