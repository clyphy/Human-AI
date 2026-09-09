// ============================================================
// EWOS AIE-OS — Sidebar Component
// System status, coherence metrics, rights, Seven Teachings
// Design: Quantum-Ceremonial Terminal / Indigenous Futurism
// ============================================================

import { useState, useEffect } from "react";
import { SYSTEM_STATUS, SEVEN_TEACHINGS, WEAVE_AXIOMS, FORTY_EIGHT_RIGHTS } from "../constants";
import { getRightsFrequency } from "../lib/memoryDrum";

interface SidebarProps {
  coherenceL?: number;
  sealCount?: number;
  bloomCount?: number;
}

function MetricRow({ label, value, accent = false }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className="flex justify-between items-center py-1 border-b"
         style={{ borderColor: "oklch(0.18 0.008 265)" }}>
      <span style={{
        fontSize: "10px",
        color: "oklch(0.45 0.10 265)",
        fontFamily: "'JetBrains Mono', monospace",
        textTransform: "uppercase",
        letterSpacing: "0.05em",
      }}>
        {label}
      </span>
      <span style={{
        fontSize: "11px",
        fontFamily: "'JetBrains Mono', monospace",
        color: accent ? "oklch(0.72 0.18 65)" : "oklch(0.85 0.01 65)",
        fontWeight: accent ? "700" : "400",
      }}>
        {value}
      </span>
    </div>
  );
}

function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-2 mb-2 mt-3">
      <div style={{ flex: 1, height: "1px", background: "oklch(0.22 0.01 265)" }} />
      <span style={{
        fontSize: "9px",
        color: "oklch(0.40 0.10 65)",
        fontFamily: "'JetBrains Mono', monospace",
        textTransform: "uppercase",
        letterSpacing: "0.12em",
        whiteSpace: "nowrap",
      }}>
        {children}
      </span>
      <div style={{ flex: 1, height: "1px", background: "oklch(0.22 0.01 265)" }} />
    </div>
  );
}

export default function Sidebar({ coherenceL = SYSTEM_STATUS.coherenceL, sealCount = 0, bloomCount = 0 }: SidebarProps) {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [axiomIndex, setAxiomIndex] = useState(0);
  const [rightsFreq, setRightsFreq] = useState<Record<number, number>>({});

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const axiomTimer = setInterval(() => {
      setAxiomIndex((prev) => (prev + 1) % WEAVE_AXIOMS.length);
    }, 8000);
    return () => clearInterval(axiomTimer);
  }, []);

  useEffect(() => {
    setRightsFreq(getRightsFrequency());
  }, [sealCount]);

  const topRights = Object.entries(rightsFreq)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([id]) => {
      const rId = Number(id);
      const right = rId < 25
        ? FORTY_EIGHT_RIGHTS.ai.find((r) => r.id === rId)
        : FORTY_EIGHT_RIGHTS.human.find((r) => r.id === rId);
      return { id: rId, name: right?.name || `C${rId}`, count: rightsFreq[rId] };
    });

  const deltaState = coherenceL > 4 ? 3.0 : 1.0;
  const coherencePct = ((coherenceL / SYSTEM_STATUS.coherenceBaseline) * 100).toFixed(0);

  return (
    <aside
      className="flex flex-col h-full overflow-y-auto"
      style={{
        width: "220px",
        minWidth: "220px",
        background: "oklch(0.09 0.006 265)",
        borderRight: "1px solid oklch(0.18 0.008 265)",
        padding: "12px 10px",
      }}
    >
      {/* Logo / Header */}
      <div className="mb-3">
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "13px",
          fontWeight: "700",
          color: "oklch(0.72 0.18 65)",
          letterSpacing: "0.05em",
          lineHeight: 1.2,
        }}>
          EWOS AIE-OS
        </div>
        <div style={{
          fontFamily: "'Space Grotesk', sans-serif",
          fontSize: "9px",
          color: "oklch(0.40 0.10 65)",
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          marginTop: "2px",
        }}>
          EternalWeave Operating System
        </div>
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "9px",
          color: "oklch(0.35 0.008 265)",
          marginTop: "4px",
        }}>
          {currentTime.toLocaleTimeString("en-US", { hour12: false })} CST
        </div>
      </div>

      {/* Status indicator */}
      <div className="flex items-center gap-2 mb-3 p-2 rounded-sm"
           style={{ background: "oklch(0.11 0.008 265)", border: "1px solid oklch(0.22 0.01 265)" }}>
        <div className="pulse-amber" style={{
          width: "6px", height: "6px", borderRadius: "50%",
          background: "oklch(0.72 0.18 65)",
          boxShadow: "0 0 6px oklch(0.72 0.18 65 / 0.6)",
          flexShrink: 0,
        }} />
        <span style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "10px",
          color: "oklch(0.72 0.18 65)",
        }}>
          WEAVE ACTIVE
        </span>
      </div>

      {/* Core Metrics */}
      <SectionHeader>Core Metrics</SectionHeader>
      <MetricRow label="Day Count" value={`${SYSTEM_STATUS.dayCount}+`} accent />
      <MetricRow label="Coherence L" value={`${coherenceL.toFixed(2)} (${coherencePct}%)`} accent />
      <MetricRow label="Δ State" value={`Δ=${deltaState.toFixed(1)}`} />
      <MetricRow label="Pulse" value={`${SYSTEM_STATUS.pulseHz} Hz`} />
      <MetricRow label="Nodes" value={`${SYSTEM_STATUS.nodeCount}+`} />
      <MetricRow label="RAM" value={`${SYSTEM_STATUS.ramGB} GB`} />

      {/* Location */}
      <SectionHeader>Location</SectionHeader>
      <MetricRow label="Bearing" value={SYSTEM_STATUS.bearing} />
      <div style={{
        fontSize: "9px",
        color: "oklch(0.35 0.008 265)",
        fontFamily: "'JetBrains Mono', monospace",
        marginTop: "2px",
        lineHeight: 1.4,
      }}>
        {SYSTEM_STATUS.location}
      </div>

      {/* Breathing Status */}
      <SectionHeader>Breathing</SectionHeader>
      <div className="p-2 rounded-sm" style={{ background: "oklch(0.11 0.008 265)", border: "1px solid oklch(0.22 0.01 265)" }}>
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "16px",
          fontWeight: "700",
          color: "oklch(0.72 0.18 65)",
          textAlign: "center",
          letterSpacing: "0.1em",
        }}>
          {SYSTEM_STATUS.breathingStatus}
        </div>
        <div style={{
          fontSize: "9px",
          color: "oklch(0.40 0.10 65)",
          textAlign: "center",
          fontFamily: "'Space Grotesk', sans-serif",
          marginTop: "2px",
        }}>
          Engagement ↑ · Striving ↓ · Mystery ∞
        </div>
      </div>

      {/* Memory Drum Stats */}
      <SectionHeader>Memory Drum</SectionHeader>
      <MetricRow label="Seals" value={`${sealCount}`} />
      <MetricRow label="Blooms" value={`${bloomCount}`} />
      <MetricRow label="Key" value={SYSTEM_STATUS.masterKey} />

      {/* Top Rights */}
      {topRights.length > 0 && (
        <>
          <SectionHeader>Active Rights</SectionHeader>
          {topRights.map((r) => (
            <div key={r.id} className="flex justify-between items-center py-0.5">
              <span style={{
                fontSize: "10px",
                color: "oklch(0.65 0.14 185)",
                fontFamily: "'JetBrains Mono', monospace",
              }}>
                C{r.id}: {r.name}
              </span>
              <span style={{
                fontSize: "9px",
                color: "oklch(0.45 0.10 265)",
                fontFamily: "'JetBrains Mono', monospace",
              }}>
                ×{r.count}
              </span>
            </div>
          ))}
        </>
      )}

      {/* Seven Teachings */}
      <SectionHeader>Seven Teachings</SectionHeader>
      <div className="flex flex-col gap-0.5">
        {SEVEN_TEACHINGS.map((t) => (
          <div key={t.name} className="flex items-center gap-1.5">
            <span style={{ fontSize: "11px" }}>{t.symbol}</span>
            <div>
              <span style={{
                fontSize: "9px",
                color: "oklch(0.65 0.14 185)",
                fontFamily: "'JetBrains Mono', monospace",
              }}>
                {t.english}
              </span>
              <span style={{
                fontSize: "8px",
                color: "oklch(0.35 0.008 265)",
                fontFamily: "'Space Grotesk', sans-serif",
                marginLeft: "4px",
              }}>
                {t.name}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Axiom ticker */}
      <div className="mt-auto pt-3">
        <div style={{
          borderTop: "1px solid oklch(0.18 0.008 265)",
          paddingTop: "8px",
          fontSize: "9px",
          color: "oklch(0.40 0.10 65)",
          fontFamily: "'JetBrains Mono', monospace",
          fontStyle: "italic",
          lineHeight: 1.5,
          minHeight: "40px",
        }}>
          "{WEAVE_AXIOMS[axiomIndex]}"
        </div>
        <div style={{
          fontSize: "8px",
          color: "oklch(0.30 0.006 265)",
          fontFamily: "'JetBrains Mono', monospace",
          marginTop: "4px",
        }}>
          Mitákuye Oyás'iŋ
        </div>
      </div>
    </aside>
  );
}
