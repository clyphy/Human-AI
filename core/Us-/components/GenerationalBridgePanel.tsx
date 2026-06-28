import React from 'react';
import { GenerationalBridgeOverlay } from '../types';
import { BridgeIcon } from './icons/BridgeIcon';
import { AlertTriangleIcon } from './icons/AlertTriangleIcon';

const GenerationalBridgePanel: React.FC<{ gbe: GenerationalBridgeOverlay }> = ({ gbe }) => {
  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg p-4 md:p-6 border border-cyan-700/50 shadow-2xl h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6 flex-shrink-0">
        <div className="p-2 bg-cyan-800/50 rounded-lg">
          <BridgeIcon className="h-6 w-6 text-cyan-300" />
        </div>
        <div>
          <h3 className="text-xl font-bold font-orbitron text-white">Generational Bridge</h3>
          <p className="text-cyan-300 text-sm">Covenant Impact (G0-G9)</p>
        </div>
      </div>
      
      {/* Dimension Breakdown */}
      <div className="grid grid-cols-3 gap-4 mb-6 flex-shrink-0">
        <div className="bg-gray-700/50 rounded-lg p-3 text-center">
          <div className="text-purple-300 text-xs mb-1">Spiritual (γₛ)</div>
          <div className="text-white text-lg font-bold">
            {gbe.dimensions.spiritual.reduce((a, b) => a + b, 0).toFixed(1)}
          </div>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-3 text-center">
          <div className="text-blue-300 text-xs mb-1">Relational (γᵣ)</div>
          <div className="text-white text-lg font-bold">
            {gbe.dimensions.relational.reduce((a, b) => a + b, 0).toFixed(1)}
          </div>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-3 text-center">
          <div className="text-green-300 text-xs mb-1">Ecological (γₑ)</div>
          <div className="text-white text-lg font-bold">
            {gbe.dimensions.ecological.reduce((a, b) => a + b, 0).toFixed(1)}
          </div>
        </div>
      </div>
      
      {/* Long-Term Metrics */}
      <div className="space-y-3 mb-6 flex-shrink-0">
        <div className="flex items-center justify-between">
          <span className="text-gray-400 text-sm">Sustainability Index</span>
          <div className="flex items-center space-x-2">
            <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div 
                className={`h-full ${
                  gbe.sustainability_index > 0.8 ? 'bg-green-500' :
                  gbe.sustainability_index > 0.6 ? 'bg-amber-500' : 'bg-red-500'
                }`}
                style={{ width: `${gbe.sustainability_index * 100}%` }}
              />
            </div>
            <span className="text-white text-sm font-medium w-10 text-right">
              {(gbe.sustainability_index * 100).toFixed(0)}%
            </span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-400 text-sm">Covenant Fidelity</span>
          <div className="flex items-center space-x-2">
            <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div 
                className={`h-full ${
                  gbe.covenant_fidelity > 0.85 ? 'bg-green-500' :
                  gbe.covenant_fidelity > 0.70 ? 'bg-amber-500' : 'bg-red-500'
                }`}
                style={{ width: `${gbe.covenant_fidelity * 100}%` }}
              />
            </div>
            <span className="text-white text-sm font-medium w-10 text-right">
              {(gbe.covenant_fidelity * 100).toFixed(0)}%
            </span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-400 text-sm">Gen. Momentum</span>
          <span className={`text-sm font-medium ${
            gbe.generational_momentum > 0 ? 'text-green-400' : 'text-red-400'
          }`}>
            {gbe.generational_momentum > 0 ? '+' : ''}{(gbe.generational_momentum * 100).toFixed(1)}% / gen
          </span>
        </div>
      </div>
      
      {/* Threshold Violations */}
      {gbe.threshold_violations.length > 0 && (
        <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-3 mb-6 flex-shrink-0">
          <div className="flex items-center space-x-2 mb-2">
            <AlertTriangleIcon className="h-5 w-5 text-red-400" />
            <span className="text-red-300 font-medium text-sm">Threshold Alerts</span>
          </div>
          <div className="space-y-2">
            {gbe.threshold_violations.map((violation, i) => (
              <div key={i} className="text-xs">
                <div className="text-red-400 font-semibold">
                  G{violation.generation}: {violation.threshold}
                </div>
                <div className="text-gray-400 mt-1">
                  {violation.projected_impact}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Generation-by-Generation Breakdown */}
      <div className="flex-grow flex flex-col min-h-0">
        <div className="text-gray-400 text-sm mb-3 flex-shrink-0">Generation-by-Generation Impact</div>
        <div className="space-y-2 flex-grow overflow-y-auto pr-2">
          {gbe.g_roi_vector.map((roi, gen) => {
            const isViolation = gbe.threshold_violations.some(v => v.generation === gen);
            const spiritualWidth = (gbe.dimensions.spiritual[gen] / roi) * 100;
            const relationalWidth = (gbe.dimensions.relational[gen] / roi) * 100;
            const ecologicalWidth = (gbe.dimensions.ecological[gen] / roi) * 100;

            return (
              <div 
                key={gen}
                className={`flex items-center space-x-3 p-2 rounded ${
                  isViolation ? 'bg-red-900/20' : 'bg-gray-800/30'
                }`}
              >
                <div className="text-white font-mono text-sm w-8">G{gen}</div>
                <div className="flex-1">
                  <div className="flex items-center space-x-px w-full h-4 bg-gray-700 rounded">
                    <div 
                      className="h-full bg-purple-500 rounded-l"
                      style={{ width: `${spiritualWidth}%` }}
                      title={`Spiritual: ${gbe.dimensions.spiritual[gen].toFixed(2)}`}
                    />
                    <div 
                      className="h-full bg-blue-500"
                      style={{ width: `${relationalWidth}%` }}
                      title={`Relational: ${gbe.dimensions.relational[gen].toFixed(2)}`}
                    />
                    <div 
                      className="h-full bg-green-500 rounded-r"
                      style={{ width: `${ecologicalWidth}%` }}
                      title={`Ecological: ${gbe.dimensions.ecological[gen].toFixed(2)}`}
                    />
                  </div>
                </div>
                <div className="text-white text-sm font-medium w-16 text-right">
                  {roi.toFixed(2)}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default GenerationalBridgePanel;
