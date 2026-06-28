import React from 'react';
import { type LucideIcon } from 'lucide-react';

export type ViewOption = 'A' | 'B';

export interface CardProps {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  contentClassName?: string;
}

export interface PXNProject {
  id: number;
  name: string;
  is_meta: boolean;
  scriptural_basis: string;
  l_score: number;
  covenant_fidelity: number;
  grace_multiplier: number;
  gbe: GenerationalBridgeOverlay;
  tef_webs: ProbabilityWeb[];
  sabbath_status: SabbathStatus;
  status: string;
  loveCoefficient: number;
}

export type ArchiveEventType = 'SABBATH_VECTOR_ACTIVATED' | 'SABBATH_VECTOR_CLEARED' | 'MANDATE_COMPLETED' | 'COVENANT_EXPORT' | 'GRACE_SHIFT';

export interface PropheticArchiveEvent {
  id: string;
  timestamp: string;
  type: ArchiveEventType;
  project_name: string;
  title: string;
  description: string;
  impact_score: number;
  icon: LucideIcon;
  color: string;
}

export interface EntangledPath {
  path_id: string;
  probability: number;
  timeline: { time_step: number; l_score: number }[];
}

export interface SabbathStatus {
    is_in_audit: boolean;
    audit_until_timestamp: string;
    vef_score_trigger: number;
}

// The three core covenant dimensions
export type CovenantDimension = 'ecological' | 'social' | 'financial';

// Prophetic Presets System
export interface PropheticPreset {
  id: string;
  name: string;
  description: string;
  gamma_ecological: number; // γₑ
  gamma_social: number;     // γₛ
  gamma_financial: number;  // γƒ
  grace_bias: number;
}

// L-Score Display Architecture
export interface LScoreData {
  current: number; // 0.00-1.00
  weeklyDelta: number;
  monthlyTrend: 'ascending' | 'stable' | 'descending';
  covenantAlignment: number; // 0-100% vs. community median
}

// G-ROI Threshold Alerts
export interface CovenantAlert {
  severity: 'advisory' | 'warning' | 'critical';
  message: string;
  action: string;
  scriptureAnchor: string;
  visualCue: string;
  timestamp: Date;
}

// Data structure expected from G-ROI Chart
export type GROIVector = number[]; // G0-G9 values

// Prophetic Archive Timeline
export interface PredictivePath {
  timestamp: string;
  projectedLScore: number;
  scripture: string;
  principle: string;
}

export interface ArchiveEvent {
  timestamp: string;
  lScoreMedian: number;
  lScoreP25: number;
  lScoreP75: number;
  graceDistributed: number;
  syncWinks: { scripture: string; snippet: string }[];
  predictivePaths: PredictivePath[];
}

// Temporal Entanglement Forge Types
export interface PropheticMandate {
  id: string;
  title: string;
  description: string;
  scripture_basis: string;
  warning?: string;
  activation_conditions: {
    min_grace_flow: number;
    required_l_score: number;
    community_size_min: number;
    timing_window_days: number;
    prerequisite_mandates: string[];
  };
  projected_impact: {
    l_score_delta: number;
    g_roi_boost: number[];
    grace_multiplier: number;
    network_effects: string[];
  };
  urgency: 'kairos' | 'strategic' | 'foundational';
  expiration_timestamp?: string;
  completion_metrics: {
    progress: number;
    fruit_metrics: {
      souls_touched: number;
      covenants_formed: number;
      generational_impact: number;
    };
  };
}

export interface ProbabilityPath {
    path_id: string;
    probability: number;
    timeline: { l_score: number }[];
}
export interface ProbabilityWeb {
    steward_id: string;
    entangled_paths: (ProbabilityPath | EntangledPath)[];
}

export interface GenerationalBridgeOverlay {
  dimensions: {
    spiritual: number[];
    relational: number[];
    ecological: number[];
  };
  sustainability_index: number;
  covenant_fidelity: number;
  generational_momentum: number;
  threshold_violations: {
    generation: number;
    threshold: string;
    projected_impact: string;
  }[];
  g_roi_vector: number[];
}


// --- New Types for DashboardView ---

export interface BridgeData {
  id: string;
  name: string;
  integrity: number;
}

export interface WebData {
  id: string;
  alignment: number;
}

export interface TemporalTimelinePoint {
  id: string;
  label: string;
  coherence: number;
}
