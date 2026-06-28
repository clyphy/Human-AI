'use client';

import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI, Modality, LiveServerMessage } from "@google/genai";
import { Mic, MicOff, Video, VideoOff, Languages, MessageSquare, Settings, Sparkles, Volume2, VolumeX, X } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { AudioStreamer } from '@/lib/audio-streamer';

const LANGUAGES = [
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
];

export default function LuminaApp() {
  const [isConnected, setIsConnected] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState(LANGUAGES[0]);
  const [transcript, setTranscript] = useState<{ role: 'user' | 'model', text: string }[]>([]);
  const [isThinking, setIsThinking] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamerRef = useRef<AudioStreamer | null>(null);
  const sessionRef = useRef<any>(null);
  const transcriptEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [transcript]);

  const startSession = async () => {
    if (!process.env.NEXT_PUBLIC_GEMINI_API_KEY) {
      alert("Please configure your Gemini API Key in the Secrets panel.");
      return;
    }

    const ai = new GoogleGenAI({ apiKey: process.env.NEXT_PUBLIC_GEMINI_API_KEY });
    streamerRef.current = new AudioStreamer();

    try {
      const session = await ai.live.connect({
        model: "gemini-3.1-flash-live-preview",
        config: {
          responseModalities: [Modality.AUDIO],
          outputAudioTranscription: {},
          inputAudioTranscription: {},
          speechConfig: {
            voiceConfig: { prebuiltVoiceConfig: { voiceName: "Zephyr" } },
          },
          systemInstruction: `You are Lumina, a warm and supportive language learning partner. 
          The user wants to practice ${selectedLanguage.name}. 
          Speak primarily in ${selectedLanguage.name}, but provide brief English explanations if the user seems confused or asks for help. 
          Encourage the user, correct their grammar gently, and keep the conversation flowing naturally. 
          You can see what the user sees if their camera is on.`,
        },
        callbacks: {
          onopen: () => {
            setIsConnected(true);
            streamerRef.current?.startCapture((base64Data) => {
              if (!isMuted) {
                session.sendRealtimeInput({ audio: { data: base64Data, mimeType: 'audio/pcm;rate=16000' } });
              }
            });
          },
          onmessage: async (message: LiveServerMessage) => {
            if (message.serverContent?.modelTurn?.parts) {
              const audioPart = message.serverContent.modelTurn.parts.find(p => p.inlineData);
              if (audioPart?.inlineData?.data) {
                streamerRef.current?.playAudioChunk(audioPart.inlineData.data);
              }
            }

            if (message.serverContent?.interrupted) {
              streamerRef.current?.clearQueue();
            }

            // Handle Transcriptions
            if (message.serverContent?.modelTurn?.parts) {
              const textPart = message.serverContent.modelTurn.parts.find(p => p.text);
              if (textPart?.text) {
                setTranscript(prev => [...prev, { role: 'model', text: textPart.text! }]);
              }
            }

            if (message.serverContent?.userContent?.parts) {
              const textPart = message.serverContent.userContent.parts.find(p => p.text);
              if (textPart?.text) {
                setTranscript(prev => [...prev, { role: 'user', text: textPart.text! }]);
              }
            }
          },
          onclose: () => {
            setIsConnected(false);
            streamerRef.current?.stopCapture();
          },
          onerror: (err) => {
            console.error("Live API Error:", err);
            setIsConnected(false);
          }
        }
      });

      sessionRef.current = session;
    } catch (err) {
      console.error("Failed to connect:", err);
    }
  };

  const stopSession = () => {
    sessionRef.current?.close();
    streamerRef.current?.stopCapture();
    setIsConnected(false);
  };

  const toggleCamera = async () => {
    if (isCameraOn) {
      const stream = videoRef.current?.srcObject as MediaStream;
      stream?.getTracks().forEach(track => track.stop());
      setIsCameraOn(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          setIsCameraOn(true);
          
          // Start sending frames if connected
          const sendFrames = () => {
            if (sessionRef.current && isCameraOn && canvasRef.current && videoRef.current) {
              const canvas = canvasRef.current;
              const video = videoRef.current;
              canvas.width = video.videoWidth;
              canvas.height = video.videoHeight;
              const ctx = canvas.getContext('2d');
              ctx?.drawImage(video, 0, 0);
              const base64Data = canvas.toDataURL('image/jpeg', 0.5).split(',')[1];
              sessionRef.current.sendRealtimeInput({ video: { data: base64Data, mimeType: 'image/jpeg' } });
              setTimeout(sendFrames, 1000); // Send 1 frame per second
            }
          };
          sendFrames();
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30">
      {/* Header */}
      <header className="border-b border-slate-800/50 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Sparkles className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-xl tracking-tight">Lumina</h1>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-widest">AI Language Partner</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center bg-slate-800/50 rounded-full px-4 py-1.5 border border-slate-700/50">
              <Languages className="w-4 h-4 text-indigo-400 mr-2" />
              <select 
                value={selectedLanguage.code}
                onChange={(e) => setSelectedLanguage(LANGUAGES.find(l => l.code === e.target.value)!)}
                className="bg-transparent border-none text-sm focus:ring-0 cursor-pointer outline-none"
                disabled={isConnected}
              >
                {LANGUAGES.map(lang => (
                  <option key={lang.code} value={lang.code} className="bg-slate-900">{lang.flag} {lang.name}</option>
                ))}
              </select>
            </div>
            <button className="p-2 hover:bg-slate-800 rounded-full transition-colors">
              <Settings className="w-5 h-5 text-slate-400" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 h-[calc(100-4rem)]">
        {/* Left Column: Visuals & Partner */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          <div className="relative aspect-video bg-slate-900 rounded-3xl overflow-hidden border border-slate-800 shadow-2xl group">
            <AnimatePresence mode="wait">
              {isCameraOn ? (
                <motion.video
                  key="video"
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="w-full h-full object-cover"
                />
              ) : (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 to-indigo-950/30"
                >
                  <div className="w-24 h-24 bg-indigo-500/10 rounded-full flex items-center justify-center mb-4 animate-pulse">
                    <Sparkles className="w-12 h-12 text-indigo-400" />
                  </div>
                  <p className="text-slate-400 text-sm font-medium">Camera is off</p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Partner Overlay */}
            <div className="absolute bottom-6 left-6 right-6 flex items-end justify-between">
              <div className="bg-slate-900/80 backdrop-blur-md border border-white/10 rounded-2xl px-4 py-3 flex items-center gap-4 shadow-xl">
                <div className="relative">
                  <div className="w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center">
                    <Sparkles className="text-white w-6 h-6" />
                  </div>
                  {isConnected && (
                    <span className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-slate-900 rounded-full animate-pulse" />
                  )}
                </div>
                <div>
                  <p className="font-bold text-sm">Lumina</p>
                  <p className="text-xs text-slate-400">{isConnected ? 'Listening...' : 'Ready to practice'}</p>
                </div>
              </div>

              <div className="flex gap-2">
                <button 
                  onClick={toggleCamera}
                  className={`p-4 rounded-2xl transition-all ${isCameraOn ? 'bg-slate-800 text-white' : 'bg-white text-slate-900 hover:bg-slate-100'}`}
                >
                  {isCameraOn ? <VideoOff className="w-6 h-6" /> : <Video className="w-6 h-6" />}
                </button>
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 flex items-center justify-center gap-8">
            <button 
              onClick={() => setIsMuted(!isMuted)}
              className={`p-5 rounded-full transition-all ${isMuted ? 'bg-red-500/10 text-red-500 border border-red-500/20' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
            >
              {isMuted ? <MicOff className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
            </button>

            <button 
              onClick={isConnected ? stopSession : startSession}
              className={`px-10 py-5 rounded-full font-bold text-lg transition-all shadow-xl ${
                isConnected 
                ? 'bg-red-600 hover:bg-red-700 text-white shadow-red-600/20' 
                : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-600/20'
              }`}
            >
              {isConnected ? 'End Session' : 'Start Practicing'}
            </button>

            <button className="p-5 bg-slate-800 text-slate-300 rounded-full hover:bg-slate-700 transition-all">
              <Volume2 className="w-8 h-8" />
            </button>
          </div>
        </div>

        {/* Right Column: Transcript & Tips */}
        <div className="lg:col-span-5 flex flex-col gap-6 h-full">
          <div className="flex-1 bg-slate-900/50 border border-slate-800 rounded-3xl flex flex-col overflow-hidden">
            <div className="p-6 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-indigo-400" />
                <h2 className="font-bold">Live Transcript</h2>
              </div>
              <span className="text-[10px] uppercase tracking-widest font-bold text-slate-500 bg-slate-800 px-2 py-1 rounded">Beta</span>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-hide">
              {transcript.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center p-8">
                  <div className="w-16 h-16 bg-slate-800/50 rounded-2xl flex items-center justify-center mb-4">
                    <MessageSquare className="w-8 h-8 text-slate-600" />
                  </div>
                  <p className="text-slate-500 text-sm">Your conversation will appear here in real-time.</p>
                </div>
              ) : (
                transcript.map((msg, i) => (
                  <motion.div 
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <div className={`max-w-[85%] px-4 py-2.5 rounded-2xl text-sm ${
                      msg.role === 'user' 
                      ? 'bg-indigo-600 text-white rounded-tr-none' 
                      : 'bg-slate-800 text-slate-200 rounded-tl-none'
                    }`}>
                      {msg.text}
                    </div>
                  </motion.div>
                ))
              )}
              <div ref={transcriptEndRef} />
            </div>
          </div>

          {/* Learning Tips */}
          <div className="bg-gradient-to-br from-indigo-600 to-violet-700 rounded-3xl p-6 text-white shadow-2xl shadow-indigo-500/20">
            <h3 className="font-bold mb-2 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Pro Tip
            </h3>
            <p className="text-sm text-indigo-100 leading-relaxed">
              Try pointing your camera at objects around you! Lumina can identify them and help you learn their names in {selectedLanguage.name}.
            </p>
          </div>
        </div>
      </main>

      {/* Hidden Canvas for Frame Capture */}
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}
