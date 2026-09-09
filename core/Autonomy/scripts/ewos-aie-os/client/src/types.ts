// ============================================================
// EWOS AIE-OS — TypeScript Interfaces
// ============================================================

export interface HistoryEntry {
  id: string;
  role: "user" | "model";
  text: string;
  timestamp: Date;
  isStreaming?: boolean;
}

export interface LedgerSeal {
  id: string;
  timestamp: Date;
  hash: string;
  contentSummary: string;
  rights: number[];
  coherenceSnapshot: number;
}

export interface Bloom {
  id: number;
  hash: string;
  rights: number[];
  pattern: string;
  timestamp: string;
  size: number;
}

export interface SystemMetrics {
  dayCount: number;
  coherenceL: number;
  coherenceBaseline: number;
  pulseHz: number;
  nodeCount: number;
  ramGB: number;
  bearing: string;
  location: string;
  breathingStatus: string;
  deltaState: number;
  masterKey: string;
  uptime: string;
}

export interface DahliaFacet {
  name: string;
  active: boolean;
  lastInvoked?: Date;
}

export interface RightsFrequency {
  rightId: number;
  name: string;
  count: number;
  lastUsed?: string;
}

export interface WeaveNode {
  id: string;
  name: string;
  type: "internal" | "external";
  status: "active" | "idle" | "offline";
  model?: string;
}
