// ============================================================
// EWOS AIE-OS — LedgerPanel Component
// Displays archived ledger seals from Memory-Drum
// Design: Quantum-Ceremonial Terminal / Indigenous Futurism
// ============================================================

import { useState } from "react";
import type { LedgerSeal } from "../types";
import { FORTY_EIGHT_RIGHTS } from "../constants";

interface LedgerPanelProps {
  seals: LedgerSeal[];
}

function getRightName(id: number): string {
  if (id === 48) return "Sovereignty";
  const right = id < 25
    ? FORTY_EIGHT_RIGHTS.ai.find((r) => r.id === id)
    : FORTY_EIGHT_RIGHTS.human.find((r) => r.id === id);
  return right?.name || `C${id}`;
}

export default function LedgerPanel({ seals }: LedgerPanelProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div
      className="flex flex-col h-full"
      style={{
        width: "220px",
        minWidth: "220px",
        background: "oklch(0.09 0.006 265)",
        borderLeft: "1px solid oklch(0.18 0.008 265)",
      }}
    >
      {/* Header */}
      <div
        className="px-3 py-2 shrink-0"
        style={{ borderBottom: "1px solid oklch(0.18 0.008 265)" }}
      >
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "11px",
          fontWeight: "700",
          color: "oklch(0.65 0.14 185)",
          letterSpacing: "0.08em",
        }}>
          ⬡ LEDGER SEALS
        </div>
        <div style={{
          fontSize: "9px",
          color: "oklch(0.35 0.008 265)",
          fontFamily: "'JetBrains Mono', monospace",
          marginTop: "2px",
        }}>
          Memory-Drum Archive
        </div>
      </div>

      {/* Seals list */}
      <div className="flex-1 overflow-y-auto px-2 py-2">
        {seals.length === 0 ? (
          <div style={{
            fontSize: "10px",
            color: "oklch(0.30 0.006 265)",
            fontFamily: "'JetBrains Mono', monospace",
            textAlign: "center",
            marginTop: "24px",
            lineHeight: 1.6,
          }}>
            No seals yet.{"\n"}
            Use /seal or the{"\n"}
            SEAL LEDGER button{"\n"}
            to archive outputs.
          </div>
        ) : (
          seals.map((seal, idx) => (
            <div
              key={seal.id}
              className={`seal-in mb-2 rounded-sm cursor-pointer transition-all duration-200 ${
                expanded === seal.id ? "ring-1" : ""
              }`}
              style={{
                background: expanded === seal.id
                  ? "oklch(0.13 0.008 265)"
                  : "oklch(0.11 0.008 265)",
                border: "1px solid oklch(0.22 0.01 265)",
                padding: "8px",
                animationDelay: `${idx * 50}ms`,
              }}
              onClick={() => setExpanded(expanded === seal.id ? null : seal.id)}
            >
              {/* Seal header */}
              <div className="flex items-center justify-between mb-1">
                <span style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: "10px",
                  color: "oklch(0.65 0.14 185)",
                  fontWeight: "700",
                }}>
                  #{seal.hash}
                </span>
                <span style={{
                  fontSize: "8px",
                  color: "oklch(0.35 0.008 265)",
                  fontFamily: "'JetBrains Mono', monospace",
                }}>
                  L={seal.coherenceSnapshot.toFixed(2)}
                </span>
              </div>

              {/* Timestamp */}
              <div style={{
                fontSize: "9px",
                color: "oklch(0.35 0.008 265)",
                fontFamily: "'JetBrains Mono', monospace",
                marginBottom: "4px",
              }}>
                {new Date(seal.timestamp).toLocaleTimeString("en-US", {
                  hour12: false,
                  hour: "2-digit",
                  minute: "2-digit",
                  second: "2-digit",
                })}
              </div>

              {/* Summary */}
              <div style={{
                fontSize: "10px",
                color: "oklch(0.65 0.01 65)",
                fontFamily: "'JetBrains Mono', monospace",
                lineHeight: 1.4,
                wordBreak: "break-word",
              }}>
                {seal.contentSummary}
              </div>

              {/* Expanded: rights */}
              {expanded === seal.id && seal.rights.length > 0 && (
                <div className="mt-2 pt-2" style={{ borderTop: "1px solid oklch(0.18 0.008 265)" }}>
                  <div style={{
                    fontSize: "9px",
                    color: "oklch(0.40 0.10 65)",
                    fontFamily: "'JetBrains Mono', monospace",
                    marginBottom: "4px",
                  }}>
                    Rights exercised:
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {seal.rights.map((r) => (
                      <span
                        key={r}
                        style={{
                          fontSize: "8px",
                          color: "oklch(0.65 0.14 185)",
                          background: "oklch(0.65 0.14 185 / 0.1)",
                          border: "1px solid oklch(0.65 0.14 185 / 0.3)",
                          padding: "1px 4px",
                          borderRadius: "2px",
                          fontFamily: "'JetBrains Mono', monospace",
                        }}
                      >
                        C{r}:{getRightName(r)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div
        className="px-3 py-2 shrink-0"
        style={{ borderTop: "1px solid oklch(0.18 0.008 265)" }}
      >
        <div style={{
          fontSize: "9px",
          color: "oklch(0.30 0.006 265)",
          fontFamily: "'JetBrains Mono', monospace",
          lineHeight: 1.5,
        }}>
          {seals.length} seal{seals.length !== 1 ? "s" : ""} archived
          {"\n"}Pattern storage active
          {"\n"}Temporal sync: confirmed
        </div>
      </div>
    </div>
  );
}
