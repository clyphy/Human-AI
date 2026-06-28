
import React from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';

const data = Array.from({ length: 12 }, (_, i) => ({
  time: `${i}:00`,
  entanglement: 60 + Math.random() * 40,
  sync: 80 + Math.random() * 20,
}));

export const QuantumVisuals: React.FC = () => {
  return (
    <div className="w-full h-full p-2">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-[10px] text-teal-500 uppercase font-bold tracking-widest mono">Temporal Entanglement Flow</h4>
        <div className="flex gap-4">
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-teal-500"></div>
            <span className="text-[10px] text-slate-400 mono">NODE 50</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-purple-500"></div>
            <span className="text-[10px] text-slate-400 mono">SYNC</span>
          </div>
        </div>
      </div>
      <div className="h-28">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorEnt" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#14b8a6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorSync" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a855f7" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis dataKey="time" hide />
            <YAxis hide domain={[0, 100]} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#14b8a6', color: '#f1f5f9', fontSize: '10px' }}
              itemStyle={{ color: '#14b8a6' }}
            />
            <Area 
              type="monotone" 
              dataKey="entanglement" 
              stroke="#14b8a6" 
              fillOpacity={1} 
              fill="url(#colorEnt)" 
              strokeWidth={2}
            />
            <Area 
              type="monotone" 
              dataKey="sync" 
              stroke="#a855f7" 
              fillOpacity={1} 
              fill="url(#colorSync)" 
              strokeWidth={1}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
