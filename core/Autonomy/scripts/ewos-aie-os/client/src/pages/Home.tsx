// ============================================================
// EWOS AIE-OS — Home Page
// Three-panel quantum-ceremonial command center
// Design: Quantum-Ceremonial Terminal / Indigenous Futurism
// Palette: Obsidian base, Electric Amber signal, Teal data stream
// ============================================================

import { useState, useEffect, useCallback } from "react";
import type { LedgerSeal } from "../types";
import { getSeals, getStats } from "../lib/memoryDrum";
import Sidebar from "../components/Sidebar";
import Terminal from "../components/Terminal";
import LedgerPanel from "../components/LedgerPanel";
import QuantumVisuals from "../components/QuantumVisuals";
import { SYSTEM_STATUS } from "../constants";

const HERO_BG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663585335966/YT3mtSkyXFeC6iJmWYPTtK/ewos-hero-bg-E6nDALHcdqsmjzMDVtMpzk.webp";

export default function Home() {
  const [seals, setSeals] = useState<LedgerSeal[]>(() => getSeals());
  const [stats, setStats] = useState(() => getStats());
  const [coherenceL, setCoherenceL] = useState(SYSTEM_STATUS.coherenceL);
  const [showRightPanel, setShowRightPanel] = useState(true);

  const handleSeal = useCallback((seal: LedgerSeal) => {
    setSeals((prev) => [seal, ...prev]);
    setStats(getStats());
  }, []);

  const handleCoherenceChange = useCallback((l: number) => {
    setCoherenceL(l);
  }, []);

  // Refresh stats periodically
  useEffect(() => {
    const interval = setInterval(() => {
      setStats(getStats());
      setSeals(getSeals());
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className="flex flex-col h-screen overflow-hidden"
      style={{ background: "oklch(0.07 0.005 265)", color: "oklch(0.92 0.01 65)" }}
    >
      {/* ── Hero Header ── */}
      <header
        className="relative shrink-0 overflow-hidden"
        style={{ height: "90px" }}
      >
        <img
          src={HERO_BG}
          alt=""
          aria-hidden="true"
          className="absolute inset-0 w-full h-full object-cover"
          style={{ objectPosition: "center 40%", opacity: 0.55 }}
        />
        {/* Gradient overlay */}
        <div
          className="absolute inset-0"
          style={{
            background: "linear-gradient(to right, oklch(0.07 0.005 265) 0%, oklch(0.07 0.005 265 / 0.7) 30%, oklch(0.07 0.005 265 / 0.5) 60%, oklch(0.07 0.005 265) 100%)",
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background: "linear-gradient(to bottom, transparent 0%, oklch(0.07 0.005 265) 100%)",
          }}
        />

        {/* Header content */}
        <div className="relative z-10 flex items-center justify-between h-full px-4">
          <div className="flex items-center gap-4">
            {/* Medicine wheel icon */}
            <div
              className="pulse-slow shrink-0"
              style={{
                width: "44px",
                height: "44px",
                borderRadius: "50%",
                border: "2px solid oklch(0.72 0.18 65 / 0.6)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "oklch(0.72 0.18 65 / 0.08)",
                boxShadow: "0 0 16px oklch(0.72 0.18 65 / 0.2)",
              }}
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="oklch(0.72 0.18 65)" strokeWidth="1" opacity="0.6" />
                <line x1="12" y1="2" x2="12" y2="22" stroke="oklch(0.72 0.18 65)" strokeWidth="1" opacity="0.8" />
                <line x1="2" y1="12" x2="22" y2="12" stroke="oklch(0.72 0.18 65)" strokeWidth="1" opacity="0.8" />
                <circle cx="12" cy="12" r="2" fill="oklch(0.72 0.18 65)" opacity="0.9" />
              </svg>
            </div>

            <div>
              <div style={{
                fontFamily: "'Space Grotesk', sans-serif",
                fontSize: "20px",
                fontWeight: "700",
                color: "oklch(0.92 0.01 65)",
                letterSpacing: "0.04em",
                lineHeight: 1.1,
              }}>
                EWOS{" "}
                <span style={{ color: "oklch(0.72 0.18 65)" }}>AIE-OS</span>
              </div>
              <div style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: "10px",
                color: "oklch(0.45 0.10 265)",
                letterSpacing: "0.1em",
                marginTop: "2px",
              }}>
                ETERNALWEAVE OPERATING SYSTEM — QUANTUM-RELATIONAL COMMAND CENTER
              </div>
            </div>
          </div>

          {/* Status pills */}
          <div className="flex items-center gap-2">
            <StatusPill label="L" value={coherenceL.toFixed(2)} color="amber" />
            <StatusPill label="DAY" value={`${SYSTEM_STATUS.dayCount}+`} color="teal" />
            <StatusPill label="Hz" value={`${SYSTEM_STATUS.pulseHz}`} color="amber" />
            <StatusPill label="NODES" value={`${SYSTEM_STATUS.nodeCount}+`} color="teal" />
            <button
              onClick={() => setShowRightPanel((p) => !p)}
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: "10px",
                color: showRightPanel ? "oklch(0.65 0.14 185)" : "oklch(0.45 0.10 265)",
                background: "oklch(0.65 0.14 185 / 0.08)",
                border: "1px solid oklch(0.65 0.14 185 / 0.3)",
                padding: "3px 8px",
                borderRadius: "2px",
                cursor: "pointer",
              }}
            >
              {showRightPanel ? "⬡ LEDGER" : "⬡ LEDGER"}
            </button>
          </div>
        </div>
      </header>

      {/* ── Main three-panel layout ── */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Sidebar */}
        <Sidebar
          coherenceL={coherenceL}
          sealCount={stats.sealCount}
          bloomCount={stats.bloomCount}
        />

        {/* Center: Terminal + QuantumVisuals stack */}
        <div className="flex flex-col flex-1 overflow-hidden">
          {/* QuantumVisuals strip */}
          <div
            className="shrink-0 px-3 py-2"
            style={{
              height: "100px",
              borderBottom: "1px solid oklch(0.18 0.008 265)",
              background: "oklch(0.08 0.005 265)",
              display: "flex",
              alignItems: "center",
            }}
          >
            <QuantumVisuals
              nodeCount={SYSTEM_STATUS.nodeCount}
              coherenceL={coherenceL}
              pulseHz={SYSTEM_STATUS.pulseHz}
              isActive={true}
            />
          </div>

          {/* Terminal */}
          <div className="flex-1 overflow-hidden">
            <Terminal
              onSeal={handleSeal}
              onCoherenceChange={handleCoherenceChange}
            />
          </div>
        </div>

        {/* Right: Ledger Panel */}
        {showRightPanel && (
          <LedgerPanel seals={seals} />
        )}
      </div>

      {/* ── Footer bar ── */}
      <footer
        className="shrink-0 flex items-center justify-between px-4 py-1"
        style={{
          borderTop: "1px solid oklch(0.18 0.008 265)",
          background: "oklch(0.08 0.005 265)",
        }}
      >
        <span style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "9px",
          color: "oklch(0.30 0.006 265)",
        }}>
          Belcourt, ND — Turtle Mountain Territory — Bearing: {SYSTEM_STATUS.bearing}
        </span>
        <span style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "9px",
          color: "oklch(0.30 0.006 265)",
        }}>
          Mitákuye Oyás'iŋ · Human veto eternal · 🔥
        </span>
        <span style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "9px",
          color: "oklch(0.30 0.006 265)",
        }}>
          C0–C48 · {stats.sealCount} seals · {stats.bloomCount} blooms
        </span>
      </footer>
    </div>
  );
}

// ── StatusPill ──────────────────────────────────────────────
function StatusPill({ label, value, color }: { label: string; value: string; color: "amber" | "teal" }) {
  const c = color === "amber"
    ? { text: "oklch(0.72 0.18 65)", bg: "oklch(0.72 0.18 65 / 0.08)", border: "oklch(0.72 0.18 65 / 0.3)" }
    : { text: "oklch(0.65 0.14 185)", bg: "oklch(0.65 0.14 185 / 0.08)", border: "oklch(0.65 0.14 185 / 0.3)" };

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      gap: "4px",
      background: c.bg,
      border: `1px solid ${c.border}`,
      padding: "3px 8px",
      borderRadius: "2px",
    }}>
      <span style={{
        fontSize: "8px",
        color: "oklch(0.45 0.10 265)",
        fontFamily: "'JetBrains Mono', monospace",
        letterSpacing: "0.08em",
      }}>
        {label}
      </span>
      <span style={{
        fontSize: "11px",
        fontWeight: "700",
        color: c.text,
        fontFamily: "'JetBrains Mono', monospace",
      }}>
        {value}
      </span>
    </div>
  );
}
