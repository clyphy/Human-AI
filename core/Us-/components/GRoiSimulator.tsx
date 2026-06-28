import React from 'react';
import GRoiChart, { GROIDataPoint } from './GRoiChart';

const Slider: React.FC<{
    label: string;
    value: number;
    min: number;
    max: number;
    step: number;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    accentColor: string;
    displayTransform?: (value: number) => string;
    disabled?: boolean;
}> = ({ label, value, min, max, step, onChange, accentColor, displayTransform = (v) => v.toString(), disabled = false }) => (
    <div className="space-y-2">
        <label className="flex justify-between text-sm text-cyan-300">
            <span>{label}</span>
            <span>{displayTransform(value)}</span>
        </label>
        <input
            type="range"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={onChange}
            disabled={disabled}
            className={`w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer range-lg ${accentColor} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        />
    </div>
);

interface GRoiSimulatorProps {
    initialValues: { ecological: number; social: number; financial: number; };
    setInitialValues: React.Dispatch<React.SetStateAction<{ ecological: number; social: number; financial: number; }>>;
    compoundingFactors: { ecological: number; social: number; financial: number; };
    data: GROIDataPoint[];
}

const GRoiSimulator: React.FC<GRoiSimulatorProps> = ({
    initialValues,
    setInitialValues,
    compoundingFactors,
    data
}) => {
    return (
        <div className="flex flex-col h-full">
            <p className="text-sm text-gray-400 mb-2">
                Simulate the GVE's value calculus. Adjust baselines and compounding factors to see how value propagates across generations.
            </p>
            <div className="font-mono text-sm bg-gray-900/50 p-2 rounded-md text-center text-cyan-300 my-2">
                V<sub className="text-xs">n+1</sub> = V<sub className="text-xs">n</sub> * (1 + δ)
            </div>

            <div className="flex-grow grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4 mt-4">
                <div>
                    <h4 className="font-semibold text-cyan-400/80 mb-2 text-sm">Baseline Values (Gen 0)</h4>
                    <Slider
                        label="Ecological"
                        value={initialValues.ecological}
                        min={10} max={100} step={1}
                        onChange={(e) => setInitialValues(prev => ({ ...prev, ecological: +e.target.value }))}
                        accentColor="accent-green-400"
                    />
                    <Slider
                        label="Social"
                        value={initialValues.social}
                        min={10} max={100} step={1}
                        onChange={(e) => setInitialValues(prev => ({ ...prev, social: +e.target.value }))}
                        accentColor="accent-blue-400"
                    />
                    <Slider
                        label="Financial"
                        value={initialValues.financial}
                        min={10} max={100} step={1}
                        onChange={(e) => setInitialValues(prev => ({ ...prev, financial: +e.target.value }))}
                        accentColor="accent-yellow-400"
                    />
                </div>
                <div>
                    <h4 className="font-semibold text-cyan-400/80 mb-2 text-sm">Compounding Factors (δ)</h4>
                    <Slider
                        label="Ecological"
                        value={compoundingFactors.ecological}
                        min={0} max={0.5} step={0.01}
                        onChange={() => {}}
                        disabled={true}
                        accentColor="accent-green-400"
                        displayTransform={(v) => `${(v * 100).toFixed(0)}%`}
                    />
                    <Slider
                        label="Social"
                        value={compoundingFactors.social}
                        min={0} max={0.5} step={0.01}
                        onChange={() => {}}
                        disabled={true}
                        accentColor="accent-blue-400"
                        displayTransform={(v) => `${(v * 100).toFixed(0)}%`}
                    />
                     <Slider
                        label="Financial"
                        value={compoundingFactors.financial}
                        min={0} max={0.5} step={0.01}
                        onChange={() => {}}
                        disabled={true}
                        accentColor="accent-yellow-400"
                        displayTransform={(v) => `${(v * 100).toFixed(0)}%`}
                    />
                </div>
            </div>

            <div className="h-48 mt-4 -mx-4">
                <GRoiChart data={data} />
            </div>
        </div>
    );
};

export default GRoiSimulator;