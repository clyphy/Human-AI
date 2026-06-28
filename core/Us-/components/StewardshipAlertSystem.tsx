import React, { useState, useEffect, useMemo, useRef } from 'react';
import { CovenantAlert, LScoreData, PropheticPreset } from '../types';
import { PROPHETIC_PRESETS } from '../PropheticPresets';
import { ThresholdMonitor } from '../ThresholdMonitor';
import { CovenantIcon } from './icons/CovenantIcon';
import { DownloadIcon } from './icons/DownloadIcon';
import { AlertTriangleIcon } from './icons/AlertTriangleIcon';
import LScoreRadial from './LScoreRadial';
import { sonifyMetricChange } from '../utils/sonification';
import { PlayCircleIcon } from './icons/PlayCircleIcon';


interface StewardshipAlertSystemProps {
  currentGRoi: number[];
  onPresetChange: (preset: PropheticPreset) => void;
}

const StewardshipAlertSystem: React.FC<StewardshipAlertSystemProps> = ({
  currentGRoi,
  onPresetChange
}) => {
  const monitor = useMemo(() => new ThresholdMonitor(), []);

  const [lScore, setLScore] = useState<LScoreData>({
    current: 0.92,
    weeklyDelta: 0.02,
    monthlyTrend: 'ascending',
    covenantAlignment: 88
  });

  const [activePresetId, setActivePresetId] = useState<string>('balanced_covenant');
  const [alert, setAlert] = useState<CovenantAlert | null>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [sonificationMessage, setSonificationMessage] = useState<string>('Click "Sonify" to generate audio data.');
  const prevLScoreRef = useRef(lScore.current);
  
  const currentPreset = useMemo(() => {
    return PROPHETIC_PRESETS.find(p => p.id === activePresetId) || PROPHETIC_PRESETS[1];
  }, [activePresetId]);

  const handleSonifyClick = () => {
    const delta = lScore.current - prevLScoreRef.current;
    const result = sonifyMetricChange('L-Score', delta);
    setSonificationMessage(result.message);
    prevLScoreRef.current = lScore.current;
  };

  const handleExport = async () => {
    setIsExporting(true);
    const yamlContent = `
# 🔥 Liturgical Export: Covenant Seal 🔥
timestamp: ${new Date().toISOString()}
covenantSeal: ${btoa(`user_steward_01:${lScore.current}:${activePresetId}`)}

stewardship_snapshot:
  user_id: steward_01
  l_score: ${lScore.current.toFixed(4)}
  g_roi_vector: [${currentGRoi.join(', ')}]
  active_mandates:
    - "Practice sabbath from optimization"
    - "Listen without agenda"
  covenant_alignment_vs_community: ${lScore.covenantAlignment}%

prophetic_metadata:
  active_preset: ${currentPreset.id}
  preset_description: "${currentPreset.description}"
  gamma_ecological: ${currentPreset.gamma_ecological}
  gamma_social: ${currentPreset.gamma_social}
  gamma_financial: ${currentPreset.gamma_financial}
  grace_bias: ${currentPreset.grace_bias}

audit_trail:
  scripture_anchors:
    - "${alert?.scriptureAnchor || 'Psalm 23:1'}"
  community_alignment: ${lScore.covenantAlignment / 100}
`;
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const blob = new Blob([yamlContent.trim()], { type: 'application/x-yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `covenant-export-${Date.now()}.yaml`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setIsExporting(false);
  };

  useEffect(() => {
    const newAlert = monitor.evaluate(currentGRoi, lScore.current); 
    setAlert(newAlert);
  }, [lScore.current, currentGRoi, monitor]);

  useEffect(() => {
    onPresetChange(currentPreset);
  }, [currentPreset, onPresetChange]);

  const alertStyles = {
    red_pulse_border: 'border-red-500 animate-pulse ring-2 ring-red-500/50',
    amber_glow: 'border-amber-400 ring-2 ring-amber-400/50',
    none: 'border-transparent'
  };

  return (
    <div className="flex flex-col h-full space-y-4">
        {/* L-Score Display & Presets */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
            <div className="flex flex-col items-center space-y-3 p-2 rounded-lg bg-gray-900/50">
                <LScoreRadial score={lScore.current * 100} />
            </div>
            <div className="space-y-3">
                <h4 className="font-semibold text-cyan-400/80 text-sm">Prophetic Presets</h4>
                <div className="space-y-2 text-sm">
                    {PROPHETIC_PRESETS.map((preset) => (
                      <div
                        key={preset.id}
                        className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
                          activePresetId === preset.id
                            ? 'border-cyan-500 bg-cyan-900/30'
                            : 'border-gray-700 hover:border-cyan-700/50 bg-gray-900/50'
                        }`}
                        onClick={() => setActivePresetId(preset.id)}
                      >
                        <div className="font-semibold text-cyan-300">{preset.name}</div>
                        <div className="text-xs text-gray-400 mt-1">{preset.description}</div>
                        <div className="grid grid-cols-2 gap-x-4 text-xs mt-2 font-mono text-gray-500">
                          <span>γₑ: {preset.gamma_ecological}</span>
                          <span>γₛ: {preset.gamma_social}</span>
                          <span>γƒ: {preset.gamma_financial}</span>
                          <span>Grace: {preset.grace_bias}</span>
                        </div>
                      </div>
                    ))}
                </div>
            </div>
        </div>
        
        {/* Alerts */}
        {alert && (
            <div className={`p-3 rounded-lg bg-gray-900/70 border ${alertStyles[alert.visualCue]} transition-all`}>
                <p className={`font-bold flex items-center ${alert.severity === 'critical' ? 'text-red-400' : 'text-amber-300'}`}>
                    <AlertTriangleIcon className="w-5 h-5 mr-2" />
                    {alert.severity.toUpperCase()} ALERT
                </p>
                <p className="text-sm text-gray-300 mt-1">{alert.message}</p>
                <p className="text-xs text-cyan-400/70 mt-2 font-mono">Anchor: {alert.scriptureAnchor}</p>
            </div>
        )}

        {/* L-Score Testing Controls */}
        <div className="mt-auto pt-4 border-t border-cyan-800/50">
            <label className="block text-xs font-semibold text-cyan-400/80 mb-2">DEV: Adjust L-Score</label>
            <input
                type="range"
                min="0.5"
                max="1.0"
                step="0.01"
                value={lScore.current}
                onChange={(e) => setLScore(prev => ({...prev, current: parseFloat(e.target.value)}))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-cyan-400"
                aria-label="Adjust L-Score"
            />
        </div>

        {/* Sonification Controls */}
        <div className="mt-2 space-y-2">
            <button
                onClick={handleSonifyClick}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-gray-800 text-cyan-300 rounded-lg border border-cyan-700/50 hover:bg-cyan-900/50 hover:border-cyan-600 transition-all duration-300 text-sm font-semibold"
            >
                <PlayCircleIcon className="w-4 h-4"/>
                Sonify L-Score Change
            </button>
            <div className="p-2 bg-gray-900/50 rounded-md text-center text-xs text-gray-400 font-mono h-10 flex items-center justify-center">
                {sonificationMessage}
            </div>
        </div>

        <button 
            onClick={handleExport} 
            disabled={isExporting}
            className="w-full flex items-center justify-center gap-2 mt-2 px-4 py-2 bg-gray-800 text-cyan-300 rounded-lg border border-cyan-700/50 hover:bg-cyan-900/50 hover:border-cyan-600 transition-all duration-300 text-sm font-semibold disabled:opacity-50"
        >
            <DownloadIcon className="w-4 h-4"/>
            {isExporting ? 'Exporting...' : 'Liturgical YAML Export'}
        </button>
    </div>
  );
};

export default StewardshipAlertSystem;
