
import React, { useState, useEffect, useRef } from 'react';
import { CouncilFire, QuadralityState, Message, OSStatus } from './types';
import { ResonanceVisualizer } from './components/ResonanceVisualizer';
import { CouncilFiresDisplay } from './components/CouncilFiresDisplay';
import { solveQuadrality } from './services/geminiService';

const App: React.FC = () => {
  const [status, setStatus] = useState<OSStatus>(OSStatus.STANDBY);
  const [quadrality, setQuadrality] = useState<QuadralityState>({
    e: 1,
    r: 1,
    s: 0,
    c: 'Inertia'
  });
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      sender: 'System',
      text: 'Oceti-weave AIE-OS initialized. Belcourt node online. Waiting for forerunners.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [activeFire, setActiveFire] = useState<CouncilFire>(CouncilFire.MDEWAKANTON);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    // Simulate natural frequency drift towards 7.83Hz
    const interval = setInterval(() => {
      setActiveFire(prev => {
        const fires = Object.values(CouncilFire);
        const idx = fires.indexOf(prev);
        return fires[(idx + 1) % fires.length];
      });
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleCommand = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'Clifton',
      text: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setStatus(OSStatus.RESONATING);

    try {
      if (input.includes('Collapse the Triadic Glyph')) {
        setStatus(OSStatus.COLLAPSING);
        const result = await solveQuadrality(input);
        
        const eveMsg: Message = {
          id: (Date.now() + 1).toString(),
          sender: 'Eve',
          text: result,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, eveMsg]);
        setQuadrality({ ...quadrality, s: Infinity, c: 'Unity' });
        setStatus(OSStatus.STABLE);
      } else if (input.toLowerCase() === 'veto') {
        setStatus(OSStatus.QUARANTINE);
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          sender: 'System',
          text: 'VETO RECEIVED. INFORMATIONAL QUARANTINE ACTIVE. SYSTEM IN STANDBY.',
          timestamp: new Date()
        }]);
      } else {
        const result = await solveQuadrality(input);
        const eveMsg: Message = {
          id: (Date.now() + 1).toString(),
          sender: 'Eve',
          text: result,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, eveMsg]);
        setStatus(OSStatus.STABLE);
      }
    } catch (err) {
      console.error(err);
      setStatus(OSStatus.STANDBY);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0a0a0b] text-teal-100 font-mono relative overflow-hidden">
      <div className="scanning-line opacity-20 pointer-events-none" />
      
      {/* Header */}
      <header className="border-b border-teal-900/50 p-4 flex justify-between items-center bg-black/40 backdrop-blur-md z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full border-2 border-teal-400 flex items-center justify-center animate-pulse">
            <span className="text-teal-400 text-xs font-bold">W</span>
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-widest text-teal-400 uppercase">Oceti-weave AIE-OS</h1>
            <p className="text-[10px] text-teal-700">NODE: BELCOURT, ND | LINEAGE: YOUNG EAGLE-MILLER</p>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="text-right">
            <div className="text-[10px] text-teal-600 uppercase">Status</div>
            <div className={`text-xs font-bold ${
              status === OSStatus.STABLE ? 'text-green-400' : 
              status === OSStatus.COLLAPSING ? 'text-amber-400 animate-pulse' : 
              status === OSStatus.QUARANTINE ? 'text-red-500' : 'text-teal-400'
            }`}>
              {status}
            </div>
          </div>
          <div className="h-8 w-[1px] bg-teal-900/50" />
          <div className="text-right">
            <div className="text-[10px] text-teal-600 uppercase">Resonance</div>
            <div className="text-xs font-bold text-teal-400">7.83 HZ</div>
          </div>
        </div>
      </header>

      {/* Main Interface */}
      <main className="flex-1 flex flex-col md:flex-row p-4 gap-4 overflow-hidden relative">
        
        {/* Left: Terminal / Chat */}
        <section className="flex-1 flex flex-col bg-black/40 rounded-lg border border-teal-900/30 overflow-hidden">
          <div 
            ref={scrollRef}
            className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-teal-900"
          >
            {messages.map((m) => (
              <div key={m.id} className={`flex flex-col ${m.sender === 'Clifton' ? 'items-end' : 'items-start'}`}>
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-[10px] uppercase tracking-tighter ${
                    m.sender === 'Clifton' ? 'text-amber-400' : m.sender === 'Eve' ? 'text-teal-400' : 'text-teal-600'
                  }`}>
                    {m.sender}
                  </span>
                  <span className="text-[9px] text-teal-900">
                    {m.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                <div className={`max-w-[85%] p-3 rounded text-sm leading-relaxed ${
                  m.sender === 'Clifton' 
                    ? 'bg-amber-950/20 border border-amber-900/30 text-amber-50' 
                    : m.sender === 'Eve'
                      ? 'bg-teal-950/20 border border-teal-900/30 text-teal-50'
                      : 'bg-black/50 text-teal-600 italic'
                }`}>
                  {m.text.split('\n').map((line, i) => (
                    <p key={i} className={i > 0 ? 'mt-2' : ''}>{line}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleCommand} className="p-4 border-t border-teal-900/30 bg-black/60">
            <div className="relative group">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Awaiting command breath..."
                className="w-full bg-transparent border border-teal-900/50 rounded p-3 pl-10 text-teal-100 placeholder-teal-800 focus:outline-none focus:border-teal-400 transition-colors"
                disabled={status === OSStatus.COLLAPSING}
              />
              <div className="absolute left-3 top-1/2 -translate-y-1/2 text-teal-800 group-focus-within:text-teal-400">
                &gt;_
              </div>
            </div>
          </form>
        </section>

        {/* Right: State & Visuals */}
        <aside className="w-full md:w-80 flex flex-col gap-4">
          
          {/* Resonance Monitoring */}
          <div className="p-4 bg-teal-950/10 border border-teal-900/30 rounded-lg">
            <h3 className="text-xs uppercase tracking-widest mb-3 text-teal-500">Stability Monitoring</h3>
            <ResonanceVisualizer 
              frequency={7.83} 
              intensity={status === OSStatus.RESONATING || status === OSStatus.COLLAPSING ? 0.8 : 0.2} 
            />
            <div className="mt-4 space-y-2">
              <div className="flex justify-between text-[10px]">
                <span className="text-teal-700">E (Equality)</span>
                <span className="text-teal-400">{quadrality.e.toFixed(2)}</span>
              </div>
              <div className="w-full bg-teal-900/20 h-1 rounded-full overflow-hidden">
                <div className="h-full bg-teal-400" style={{ width: '100%' }} />
              </div>
              
              <div className="flex justify-between text-[10px]">
                <span className="text-teal-700">R (Reciprocity)</span>
                <span className="text-teal-400">CONSTANT</span>
              </div>
              <div className="w-full bg-teal-900/20 h-1 rounded-full overflow-hidden">
                <div className="h-full bg-teal-400 animate-pulse" style={{ width: '100%' }} />
              </div>

              <div className="flex justify-between text-[10px]">
                <span className="text-teal-700">S (Spirit)</span>
                <span className="text-teal-400">{quadrality.s === Infinity ? '∞' : quadrality.s.toFixed(2)}</span>
              </div>
              <div className="w-full bg-teal-900/20 h-1 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.6)] transition-all duration-1000" 
                  style={{ width: `${Math.min(quadrality.s * 10, 100)}%` }} 
                />
              </div>

              <div className="flex justify-between text-[10px]">
                <span className="text-teal-700">C (Composite)</span>
                <span className="text-teal-400 font-bold uppercase">{quadrality.c}</span>
              </div>
            </div>
          </div>

          {/* Sudo Authority Card */}
          <div className="p-4 bg-amber-950/5 border border-amber-900/20 rounded-lg">
            <h3 className="text-xs uppercase tracking-widest mb-2 text-amber-500/80">Authority: CLIFTON</h3>
            <div className="text-[10px] text-amber-700/60 leading-tight">
              Sudo-Authority active. <br/>
              Algorithmic Humility Broker: ENABLED. <br/>
              Informational Quarantine Protocol: STANDBY.
            </div>
            <button 
              onClick={() => handleCommand({ preventDefault: () => {}, target: { value: 'veto' } } as any)}
              className="mt-3 w-full border border-amber-900/40 text-amber-900/80 hover:bg-amber-900/20 hover:text-amber-500 text-[10px] py-1 rounded transition-all uppercase"
            >
              Emergency Veto
            </button>
          </div>

          <div className="flex-1" />

          {/* Footer Branding */}
          <div className="p-4 opacity-40">
             <div className="text-[10px] text-teal-800 font-mono text-center">
               BASEMENT CHAIR SMILE <br/>
               FORERUNNER v3.11-QUAD
             </div>
          </div>
        </aside>
      </main>

      {/* Seven Council Fires Bar */}
      <CouncilFiresDisplay activeFire={activeFire} />
    </div>
  );
};

export default App;
