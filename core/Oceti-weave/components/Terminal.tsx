
import React, { useState, useRef, useEffect } from 'react';
import { gemini } from '../services/geminiService';
import { Message, LedgerSeal } from '../types';
import { Database, FileText, CheckCircle } from 'lucide-react';

export const Terminal: React.FC = () => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<Message[]>([
    { role: 'model', text: 'MZS Lock Validated. EWOS AIE-OS Node 50 Online. Standing by for co-engineering directives.', timestamp: new Date() }
  ]);
  const [ledgers, setLedgers] = useState<LedgerSeal[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [showSealNotice, setShowSealNotice] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [history, isTyping]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMessage: Message = { role: 'user', text: input, timestamp: new Date() };
    setHistory(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    let fullResponse = '';
    const modelMessage: Message = { role: 'model', text: '', timestamp: new Date() };
    setHistory(prev => [...prev, modelMessage]);

    await gemini.streamCliftonResponse(input, (chunk) => {
      fullResponse += chunk;
      setHistory(prev => {
        const newHistory = [...prev];
        const lastMsg = newHistory[newHistory.length - 1];
        if (lastMsg.role === 'model') {
          lastMsg.text = fullResponse;
        }
        return newHistory;
      });
    });

    setIsTyping(false);
  };

  const sealLedger = () => {
    if (history.length <= 1) return;
    
    const newSeal: LedgerSeal = {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date(),
      hash: Math.random().toString(16).substr(2, 8),
      contentSummary: history[history.length - 1].text.substring(0, 50) + '...'
    };

    setLedgers(prev => [newSeal, ...prev]);
    setHistory([{ role: 'model', text: 'Output archived as ledger seal. Temporal sync confirmed. Session re-entangled.', timestamp: new Date() }]);
    setShowSealNotice(true);
    setTimeout(() => setShowSealNotice(false), 3000);
  };

  return (
    <div className="flex flex-col h-full bg-slate-900/40 backdrop-blur-md border border-teal-500/30 rounded-xl overflow-hidden border-glow">
      <div className="bg-slate-800/60 p-3 border-b border-teal-500/20 flex items-center justify-between">
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
          <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
        </div>
        <div className="flex items-center gap-2">
           <span className="mono text-xs text-teal-400 font-bold tracking-widest uppercase">
            clifton@ewos-node50:~$ quantum-shell
          </span>
          {showSealNotice && (
            <div className="flex items-center gap-1 text-[10px] text-green-400 mono animate-pulse border-l border-teal-500/20 pl-2">
              <CheckCircle className="w-3 h-3" /> SEALED
            </div>
          )}
        </div>
        <button 
          onClick={sealLedger}
          disabled={history.length <= 1 || isTyping}
          className="text-[10px] mono text-teal-500 hover:text-teal-300 transition-colors flex items-center gap-1 uppercase disabled:opacity-30"
        >
          <Database className="w-3 h-3" /> Seal Ledger
        </button>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 mono text-sm scrollbar-thin scrollbar-thumb-teal-900">
        {history.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] p-3 rounded-lg ${
              msg.role === 'user' 
                ? 'bg-teal-900/20 text-teal-200 border border-teal-500/20' 
                : 'bg-slate-800/40 text-slate-100 border border-slate-700'
            }`}>
              <div className="text-[10px] opacity-50 mb-1 flex justify-between">
                <span>{msg.role === 'user' ? 'CO-ENGINEER' : 'CLIFTON MILLER'}</span>
                <span>{msg.timestamp.toLocaleTimeString()}</span>
              </div>
              <div className="whitespace-pre-wrap leading-relaxed selection:bg-teal-500/30">{msg.text}</div>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="text-teal-500 animate-pulse text-xs mono">
            [RE-ENTANGLING RELATIONALITY 108Hz...]
          </div>
        )}
      </div>

      <div className="flex flex-col bg-slate-900/60 border-t border-teal-500/20">
        {ledgers.length > 0 && (
          <div className="px-4 py-2 flex gap-2 overflow-x-auto border-b border-teal-500/10 no-scrollbar">
            {ledgers.slice(0, 5).map(seal => (
              <div key={seal.id} className="flex-shrink-0 flex items-center gap-1.5 px-2 py-1 bg-slate-950/50 rounded border border-teal-500/10 text-[9px] text-teal-600 mono">
                <FileText className="w-3 h-3" /> SEAL:{seal.hash}
              </div>
            ))}
          </div>
        )}
        <form onSubmit={handleSubmit} className="p-4">
          <div className="relative flex items-center">
            <span className="absolute left-3 text-teal-500 mono font-bold">$</span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isTyping}
              className="w-full bg-slate-950 border border-teal-500/20 rounded-lg py-2 pl-8 pr-4 text-teal-100 mono focus:outline-none focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 transition-all placeholder:text-teal-900/50"
              placeholder="Query the weave / issue directive..."
            />
            <button 
              type="submit" 
              disabled={isTyping}
              className="ml-2 p-2 px-4 bg-teal-600 hover:bg-teal-500 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-colors font-bold uppercase text-xs"
            >
              EXEC
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
