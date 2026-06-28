import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

// Fix: Export GROIDataPoint interface so it can be used by other components.
export interface GROIDataPoint {
  generation: string;
  ecological: number;
  social: number;
  financial: number;
  total: number;
}

// G-ROI Calculation Parameters
const DOMAIN_WEIGHTS = {
  ecological: 0.4,   // w₁ - Higher weight for ecological value
  social: 0.35,      // w₂ - Social value weight
  financial: 0.25    // w₃ - Financial value weight
};

const COMPOUNDING_FACTORS = {
  ecological: 0.12,  // γ₁ - Ecological compounding
  social: 0.08,      // γ₂ - Social compounding  
  financial: 0.06    // γ₃ - Financial compounding
};

const BASELINE_VALUES = {
  ecological: 40,    // V₁(0) - Baseline ecological value
  social: 35,        // V₂(0) - Baseline social value
  financial: 25      // V₃(0) - Baseline financial value
};

// Calculate G-ROI using the mathematical model
const calculateGROIData = (): GROIDataPoint[] => {
  const data: GROIDataPoint[] = [];
  const generations = ['G1', 'G2', 'G3', 'G4', 'G5'];

  generations.forEach((gen, t) => {
    // Calculate value for each domain using: V_i(t) = V_i(0) * (1 + γ_i)^t
    const ecologicalValue = BASELINE_VALUES.ecological * Math.pow(1 + COMPOUNDING_FACTORS.ecological, t);
    const socialValue = BASELINE_VALUES.social * Math.pow(1 + COMPOUNDING_FACTORS.social, t);
    const financialValue = BASELINE_VALUES.financial * Math.pow(1 + COMPOUNDING_FACTORS.financial, t);

    // Calculate weighted G-ROI: Σ [w_i * (V_i(t) - V_i(0))]
    const ecologicalROI = DOMAIN_WEIGHTS.ecological * (ecologicalValue - BASELINE_VALUES.ecological);
    const socialROI = DOMAIN_WEIGHTS.social * (socialValue - BASELINE_VALUES.social);
    const financialROI = DOMAIN_WEIGHTS.financial * (financialValue - BASELINE_VALUES.financial);
    
    const totalGROI = ecologicalROI + socialROI + financialROI;

    data.push({
      generation: gen,
      ecological: Math.round(ecologicalValue * 10) / 10,
      social: Math.round(socialValue * 10) / 10,
      financial: Math.round(financialValue * 10) / 10,
      total: Math.round(totalGROI * 10) / 10
    });
  });

  return data;
};

// Fix: Add a `data` prop to allow the simulator to pass dynamic data.
interface GRoiChartProps {
  data?: GROIDataPoint[];
}

const GRoiChart: React.FC<GRoiChartProps> = ({ data: dataProp }) => {
  const data = dataProp ?? calculateGROIData();

  return (
    <div>
      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="generation" 
              stroke="#9CA3AF"
              label={{ value: 'Generations', position: 'insideBottom', offset: -10, fill: '#9CA3AF' }}
            />
            <YAxis 
              stroke="#9CA3AF"
              label={{ value: 'G-ROI Value', angle: -90, position: 'insideLeft', offset: -10, fill: '#9CA3AF' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1F2937', 
                border: '1px solid #374151',
                borderRadius: '0.5rem',
                color: '#F3F4F6'
              }}
              formatter={(value: number, name: string) => [
                name === 'total' ? `${value} G-ROI points` : `${value} units`,
                name.charAt(0).toUpperCase() + name.slice(1)
              ]}
              labelStyle={{ color: '#60A5FA', fontWeight: 'bold' }}
            />
            <Legend />
            <Area 
              type="monotone" 
              dataKey="ecological" 
              stackId="1"
              stroke="#10B981" 
              fill="url(#colorEcological)" 
              name="Ecological Value"
            />
            <Area 
              type="monotone" 
              dataKey="social" 
              stackId="1"
              stroke="#3B82F6" 
              fill="url(#colorSocial)" 
              name="Social Value"
            />
            <Area 
              type="monotone" 
              dataKey="financial" 
              stackId="1"
              stroke="#F59E0B" 
              fill="url(#colorFinancial)" 
              name="Financial Value"
            />
            <Area 
              type="monotone" 
              dataKey="total" 
              stroke="#8B5CF6"
              strokeWidth={3}
              fill="none"
              dot={{ fill: '#8B5CF6', strokeWidth: 2, r: 4 }}
              name="Total G-ROI"
            />
            <defs>
              <linearGradient id="colorEcological" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="colorSocial" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="colorFinancial" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
          </AreaChart>
        </ResponsiveContainer>
      </div>
      
      {/* Formula Display */}
      <div className="mt-4 p-4 bg-gray-800 rounded-lg border border-cyan-500/20">
        <div className="text-sm font-mono text-cyan-300 mb-2">G-ROI Formula Implementation:</div>
        <div className="text-xs text-gray-300 space-y-1">
          <div>Vᵢ(t) = Vᵢ(0) × (1 + γᵢ)ᵗ</div>
          <div>G-ROI(t) = Σ [wᵢ × (Vᵢ(t) - Vᵢ(0))]</div>
          <div className="text-gray-400 mt-2">
            Where: γₑ = 12% (ecological), γₛ = 8% (social), γƒ = 6% (financial)
          </div>
        </div>
      </div>
    </div>
  );
};

export default GRoiChart;
