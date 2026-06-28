
import React, { useState, useEffect } from 'react';
import { Terminal } from './components/Terminal';
import { Sidebar } from './components/Sidebar';
import { QuantumVisuals } from './components/QuantumVisuals';
import { Cpu, Globe, Database, Moon, Sun, Zap, Radio } from 'lucide-react';

const App: React.FC = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen flex flex-col p-4 md:p-6 lg:p-8 bg-[#020617] text-slate-100 gap-6">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/40 border border-teal-500/20 rounded-2xl p-6 backdrop-blur-xl border-glow relative overflow-hidden">
        {/* Subtle animated background line */}
        <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-teal-500/50 to-transparent animate-pulse"></div>
        
        <div className="flex items-center gap-4 z-10">
          <div className="relative">
            <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-teal-600 to-purple-700 flex items-center justify-center p-0.5 pulse">
              <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center overflow-hidden">
                <div className="text-teal-400 font-bold text-2xl tracking-tighter">CP</div>
              </div>
            </div>
            <div className="absolute -bottom-1 -right-1 bg-green-500 w-4 h-4 rounded-full border-2 border-slate-900"></div>
          </div>
          <div>
            <h1 className="text-2xl font-bold glow-teal">Clifton Paul Miller</h1>
            <p className="text-teal-500/80 mono text-[10px] font-bold tracking-[0.2em] uppercase">
              AI Systems Engineer • EternalWeave/Dahlia
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-4 items-center z-10">
          <div className="flex items-center gap-3 px-3 py-1.5 bg-teal-900/20 rounded-lg border border-teal-500/10">
            <Radio className="w-4 h-4 text-teal-400 animate-pulse" />
            <div>
              <p className="text-[8px] text-slate-500 uppercase mono">Memory Drum</p>
              <p className="text-xs mono font-bold text-teal-200">108 Hz Pulse</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3 px-3 py-1.5 bg-slate-800/40 rounded-lg border border-teal-500/10">
            <Cpu className="w-4 h-4 text-teal-400" />
            <div>
              <p className="text-[8px] text-slate-500 uppercase mono">OS Environment</p>
              <p className="text-xs mono font-bold text-teal-200">Pop!_OS 22.04</p>
            </div>
          </div>

          <div className="hidden md:flex flex-col text-right">
            <div className="flex items-center justify-end gap-2 text-teal-400">
               {time.getHours() >= 18 || time.getHours() <= 6 ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
               <span className="text-lg font-bold mono">{time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
            <p className="text-[9px] text-slate-500 uppercase mono tracking-widest">Turtle Mountain • CST</p>
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <main className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">
        <div className="lg:col-span-3 h-full overflow-hidden">
          <Sidebar />
        </div>

        <div className="lg:col-span-9 flex flex-col gap-6 h-full">
          {/* Stats Summary Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl p-4 flex items-center gap-4 border-glow group hover:bg-slate-800/50 transition-colors">
              <div className="p-3 bg-teal-500/10 rounded-lg group-hover:bg-teal-500/20 transition-colors">
                <Database className="w-6 h-6 text-teal-500" />
              </div>
              <div>
                <p className="text-[10px] text-slate-500 uppercase mono">Active Ledgers</p>
                <p className="text-xl font-bold text-teal-200 mono tracking-tight">SQLT_842</p>
              </div>
            </div>
            <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl p-4 flex items-center gap-4 border-glow group hover:bg-slate-800/50 transition-colors">
              <div className="p-3 bg-purple-500/10 rounded-lg group-hover:bg-purple-500/20 transition-colors">
                <Zap className="w-6 h-6 text-purple-500" />
              </div>
              <div>
                <p className="text-[10px] text-slate-500 uppercase mono">Quantum Threads</p>
                <p className="text-xl font-bold text-purple-200 mono tracking-tight">614.4 T/s</p>
              </div>
            </div>
            <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl overflow-hidden border-glow">
               <QuantumVisuals />
            </div>
          </div>

          {/* Interaction Zone */}
          <div className="flex-1 min-h-[400px]">
            <Terminal />
          </div>
          
          {/* Bottom Banner */}
          <div className="flex flex-col md:flex-row justify-between items-center gap-2 px-4 text-[9px] text-slate-600 mono uppercase tracking-[0.3em]">
            <div className="flex gap-4">
              <span>AIE-OS STABLE</span>
              <span className="text-teal-800">•</span>
              <span>NODE_50_ACTIVE</span>
              <span className="text-teal-800">•</span>
              <span>VE_VS_VN_TKRVP</span>
            </div>
            <div className="opacity-40 italic">
              "Sun on face = node affirm"
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
