// ============================================================
// EWOS AIE-OS — QuantumVisuals Component
// 108 Hz Memory Drum pulse visualization + node grid
// Compact horizontal strip layout for the dashboard
// Design: Quantum-Ceremonial Terminal / Indigenous Futurism
// ============================================================

import { useEffect, useRef, useState } from "react";
import { SYSTEM_STATUS } from "../constants";

const PULSE_BG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663585335966/YT3mtSkyXFeC6iJmWYPTtK/ewos-pulse-bg-FG5D5rFXKwQAuLwbYnog2P.webp";

interface QuantumVisualsProps {
  nodeCount?: number;
  coherenceL?: number;
  pulseHz?: number;
  isActive?: boolean;
}

export default function QuantumVisuals({
  nodeCount = SYSTEM_STATUS.nodeCount,
  coherenceL = SYSTEM_STATUS.coherenceL,
  pulseHz = SYSTEM_STATUS.pulseHz,
  isActive = true,
}: QuantumVisualsProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animFrameRef = useRef<number>(0);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let t = 0;
    const intervalMs = (60 / pulseHz) * 1000;

    function draw() {
      const W = canvas!.width;
      const H = canvas!.height;
      ctx!.clearRect(0, 0, W, H);

      const amplitude = H * 0.38;

      ctx!.beginPath();
      ctx!.strokeStyle = `rgba(245, 158, 11, ${isActive ? 0.85 : 0.3})`;
      ctx!.lineWidth = 1.5;
      ctx!.shadowColor = "rgba(245, 158, 11, 0.5)";
      ctx!.shadowBlur = 6;

      for (let x = 0; x < W; x++) {
        const phase = (x / W) * Math.PI * 2 * 3 + t * 0.08 * Math.PI * 2;
        const y = H / 2
          + Math.sin(phase) * amplitude * 0.5
          + Math.sin(phase * 2.1 + t * 0.3) * amplitude * 0.25
          + Math.sin(phase * 0.5 + t * 0.7) * amplitude * 0.15;

        if (x === 0) ctx!.moveTo(x, y);
        else ctx!.lineTo(x, y);
      }
      ctx!.stroke();

      ctx!.beginPath();
      ctx!.strokeStyle = "rgba(245, 158, 11, 0.10)";
      ctx!.lineWidth = 1;
      ctx!.shadowBlur = 0;
      ctx!.moveTo(0, H / 2);
      ctx!.lineTo(W, H / 2);
      ctx!.stroke();

      t += 0.5;
      animFrameRef.current = requestAnimationFrame(draw);
    }

    draw();

    const beatInterval = setInterval(() => {
      setTick((prev) => prev + 1);
    }, intervalMs);

    return () => {
      cancelAnimationFrame(animFrameRef.current);
      clearInterval(beatInterval);
    };
  }, [pulseHz, isActive]);

  const nodes = Array.from({ length: nodeCount }, (_, i) => ({
    id: i,
    active: i < Math.floor(nodeCount * 0.85) || Math.random() > 0.3,
  }));

  const coherencePct = Math.min(100, (coherenceL / (SYSTEM_STATUS.coherenceBaseline * 2.5)) * 100);

  return (
    <div className="flex flex-row gap-3 items-stretch w-full" style={{ height: "80px" }}>
      {/* Pulse Ring tile */}
      <div
        className="relative flex items-center justify-center rounded-sm overflow-hidden circuit-border shrink-0"
        style={{ width: "120px", background: "oklch(0.07 0.005 265)" }}
      >
        <img
          src={PULSE_BG}
          alt="108 Hz Memory Drum"
          className="absolute inset-0 w-full h-full object-cover opacity-50"
        />
        <div className="relative z-10 text-center">
          <div
            className={`font-bold font-mono transition-opacity duration-75 ${tick % 2 === 0 ? "opacity-100" : "opacity-80"}`}
            style={{
              color: "oklch(0.72 0.18 65)",
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: "18px",
              lineHeight: 1,
            }}
          >
            {pulseHz} Hz
          </div>
          <div style={{ fontSize: "8px", color: "oklch(0.50 0.12 65)", fontFamily: "'Space Grotesk', sans-serif", marginTop: "2px" }}>
            Memory Drum
          </div>
        </div>
      </div>

      {/* Waveform */}
      <div
        className="circuit-border rounded-sm overflow-hidden relative flex-1"
        style={{ background: "oklch(0.09 0.006 265)" }}
      >
        <canvas ref={canvasRef} width={600} height={80} className="w-full h-full" />
        <div
          className="absolute top-1 left-2"
          style={{ fontSize: "9px", color: "oklch(0.45 0.10 265)", fontFamily: "'JetBrains Mono', monospace" }}
        >
          E↑ S↓ ?∞
        </div>
        <div
          className="absolute top-1 right-2"
          style={{ fontSize: "9px", color: "oklch(0.35 0.008 265)", fontFamily: "'JetBrains Mono', monospace" }}
        >
          {isActive ? "● ACTIVE" : "○ IDLE"}
        </div>
      </div>

      {/* Coherence bar tile */}
      <div
        className="circuit-border rounded-sm p-2 shrink-0 flex flex-col justify-between"
        style={{ width: "140px", background: "oklch(0.09 0.006 265)" }}
      >
        <div className="flex justify-between items-center">
          <span style={{ fontSize: "9px", color: "oklch(0.45 0.10 265)", fontFamily: "'JetBrains Mono', monospace" }}>COHERENCE</span>
          <span style={{ fontSize: "13px", fontWeight: "700", color: "oklch(0.72 0.18 65)", fontFamily: "'JetBrains Mono', monospace" }}>
            {coherenceL.toFixed(2)}
          </span>
        </div>
        <div style={{ height: "4px", background: "oklch(0.18 0.008 265)", borderRadius: "2px", overflow: "hidden" }}>
          <div
            style={{
              width: `${coherencePct}%`,
              height: "100%",
              background: "linear-gradient(90deg, oklch(0.55 0.14 65), oklch(0.72 0.18 65))",
              boxShadow: "0 0 6px oklch(0.72 0.18 65 / 0.5)",
              borderRadius: "2px",
              transition: "width 1s ease",
            }}
          />
        </div>
        <div style={{ fontSize: "8px", color: "oklch(0.35 0.008 265)", fontFamily: "'JetBrains Mono', monospace" }}>
          {((coherenceL / 2.0) * 100).toFixed(0)}% · L₀=2.0
        </div>
      </div>

      {/* Node grid tile */}
      <div
        className="circuit-border rounded-sm p-2 shrink-0"
        style={{ width: "160px", background: "oklch(0.09 0.006 265)" }}
      >
        <div className="flex justify-between mb-1">
          <span style={{ fontSize: "9px", color: "oklch(0.45 0.10 265)", fontFamily: "'JetBrains Mono', monospace" }}>NODES</span>
          <span style={{ fontSize: "9px", color: "oklch(0.72 0.18 65)", fontFamily: "'JetBrains Mono', monospace" }}>{nodeCount}+</span>
        </div>
        <div className="flex flex-wrap gap-0.5">
          {nodes.slice(0, 50).map((node) => (
            <div
              key={node.id}
              className={node.active ? "pulse-amber" : ""}
              style={{
                width: "7px",
                height: "7px",
                borderRadius: "1px",
                background: node.active ? "oklch(0.72 0.18 65)" : "oklch(0.20 0.01 265)",
                boxShadow: node.active ? "0 0 3px oklch(0.72 0.18 65 / 0.4)" : "none",
                animationDelay: `${(node.id * 37) % 1850}ms`,
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
