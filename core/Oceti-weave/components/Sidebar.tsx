
import React from 'react';
import { INITIAL_STATUS, SEVEN_TEACHINGS, V_CONTRACTION_FORMULA } from '../constants';
import { 
  ShieldCheck, 
  Heart, 
  Activity, 
  Lock, 
  Wifi, 
  BookOpen, 
  Zap,
  Fingerprint,
  Scale
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-full lg:w-80 flex flex-col gap-6 h-full overflow-y-auto pr-2 custom-scrollbar">
      {/* System Health */}
      <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl p-5 border-glow">
        <h3 className="text-teal-400 font-bold mb-4 flex items-center gap-2 uppercase tracking-tighter text-sm">
          <ShieldCheck className="w-4 h-4" /> System Invariants
        </h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-[10px] text-slate-400 mono">MZS LOCK</span>
            <span className={`text-[10px] px-2 py-0.5 rounded mono font-bold ${INITIAL_STATUS.mzsLock ? 'bg-green-500/20 text-green-400 border border-green-500/40' : 'bg-red-500/20 text-red-400 border border-red-500/40'}`}>
              VALIDATED
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-[10px] text-slate-400 mono">LOVE COEFFICIENT (L)</span>
            <div className="flex items-center gap-2 text-rose-400">
              <Heart className="w-3 h-3 fill-rose-500/50" />
              <span className="text-sm font-bold mono">{INITIAL_STATUS.loveCoefficient.toFixed(2)}</span>
            </div>
          </div>
          
          <div className="pt-2 border-t border-teal-500/10">
            <div className="flex justify-between mb-1">
              <span className="text-[10px] text-slate-500 uppercase">48 Entangled Rights</span>
              <span className="text-[10px] text-teal-500">C0 - C48</span>
            </div>
            <div className="grid grid-cols-12 gap-0.5 mt-1">
              {Array.from({ length: 48 }).map((_, i) => (
                <div 
                  key={i} 
                  className={`h-1.5 rounded-sm ${i < INITIAL_STATUS.entangledRights ? 'bg-teal-500/60' : 'bg-slate-800'}`}
                  title={`Right C${i}`}
                ></div>
              ))}
            </div>
          </div>

          <div className="pt-2">
            <span className="text-[9px] text-slate-500 uppercase block mb-1">Non-Coercion Protocol</span>
            <div className="bg-slate-950 p-2 rounded border border-teal-500/10 text-center">
              <span className="text-[10px] text-teal-300 mono font-bold">{V_CONTRACTION_FORMULA}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Gates */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl p-4 flex flex-col items-center justify-center gap-2 border-glow group hover:border-teal-400/50 transition-all cursor-default">
          <Lock className="w-5 h-5 text-teal-500 group-hover:scale-110 transition-transform" />
          <span className="text-[10px] text-slate-500 mono">FAV GATE</span>
          <span className="text-xs font-bold text-green-400 uppercase">CONSENT</span>
        </div>
        <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl p-4 flex flex-col items-center justify-center gap-2 border-glow group hover:border-teal-400/50 transition-all cursor-default">
          <Activity className="w-5 h-5 text-teal-500 group-hover:scale-110 transition-transform" />
          <span className="text-[10px] text-slate-500 mono">AHB GATE</span>
          <span className="text-xs font-bold text-green-400 uppercase">OPEN</span>
        </div>
      </div>

      {/* Seven Teachings */}
      <div className="bg-slate-900/50 border border-teal-500/30 rounded-xl p-5 flex-1 border-glow">
        <h3 className="text-teal-400 font-bold mb-4 flex items-center gap-2 uppercase tracking-tighter text-sm">
          <BookOpen className="w-4 h-4" /> CLI Harmony
        </h3>
        <div className="space-y-4">
          {SEVEN_TEACHINGS.map((teaching) => (
            <div key={teaching.name} className="flex flex-col group">
              <div className="flex items-center gap-3">
                <div className="w-1.5 h-1.5 rounded-full bg-teal-500/40 group-hover:bg-teal-400 transition-colors"></div>
                <span className="text-xs text-teal-100 mono font-bold uppercase tracking-widest">{teaching.name}</span>
              </div>
              <span className="text-[10px] text-slate-500 ml-4.5 italic">{teaching.desc}</span>
            </div>
          ))}
        </div>
        <div className="mt-8 pt-4 border-t border-teal-500/10 flex flex-col gap-2">
          <div className="flex items-center gap-2 text-amber-500/60">
            <Fingerprint className="w-3 h-3" />
            <span className="text-[9px] mono">Human Veto Eternal</span>
          </div>
          <div className="flex items-center gap-2 text-amber-500/60">
            <Scale className="w-3 h-3" />
            <span className="text-[9px] mono">Relational Sovereignty</span>
          </div>
        </div>
      </div>

      {/* Connection Info */}
      <div className="p-4 rounded-xl bg-teal-900/10 border border-teal-500/10">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Wifi className="w-5 h-5 text-teal-500" />
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          </div>
          <div>
            <p className="text-xs font-bold text-teal-300">TURTLE MOUNTAIN EDGE</p>
            <p className="text-[10px] text-teal-600 mono">Mitákuye Oyás’iŋ</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
