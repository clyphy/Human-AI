import { PropheticMandate } from './types';

function addDays(date: Date, days: number): Date {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

export const MANDATE_CATALOG: PropheticMandate[] = [
  {
    id: 'covenant_acceleration_1',
    title: 'Sevenfold Covenant Activation',
    description: 'Activate seven consecutive days of covenant prayer and declaration over your generational line',
    scripture_basis: 'Joshua 6:3-4',
    warning: 'Activation window closing soon.',
    activation_conditions: {
      min_grace_flow: 0.75,
      required_l_score: 0.80,
      community_size_min: 1,
      timing_window_days: 7,
      prerequisite_mandates: []
    },
    projected_impact: {
      l_score_delta: 0.12,
      g_roi_boost: [0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02],
      grace_multiplier: 1.8,
      network_effects: ['grace_transfer', 'covenant_multiplication']
    },
    urgency: 'kairos',
    expiration_timestamp: addDays(new Date(), 7).toISOString(),
    completion_metrics: {
      progress: 0,
      fruit_metrics: {
        souls_touched: 0,
        covenants_formed: 0,
        generational_impact: 0
      }
    }
  },
  {
    id: 'prophetic_preset_activation',
    title: 'Prophetic Mode Engagement',
    description: 'Activate the Prophetic Mode preset for 40 days of intensified spiritual sensitivity',
    scripture_basis: 'Matthew 4:1-2',
    activation_conditions: {
      min_grace_flow: 0.65,
      required_l_score: 0.75,
      community_size_min: 1,
      timing_window_days: 14,
      prerequisite_mandates: []
    },
    projected_impact: {
      l_score_delta: 0.18,
      g_roi_boost: [0.08, 0.10, 0.12, 0.14, 0.13, 0.11, 0.09, 0.07, 0.05, 0.03],
      grace_multiplier: 2.2,
      network_effects: ['prayer_support', 'accountability']
    },
    urgency: 'strategic',
    completion_metrics: {
      progress: 0,
      fruit_metrics: {
        souls_touched: 0,
        covenants_formed: 0,
        generational_impact: 0
      }
    }
  },
  {
    id: 'covenant_council_formation',
    title: 'Threefold Covenant Council',
    description: 'Gather 2-3 like-hearted stewards for monthly covenant accountability',
    scripture_basis: 'Ecclesiastes 4:12',
    activation_conditions: {
      min_grace_flow: 0.60,
      required_l_score: 0.70,
      community_size_min: 3,
      timing_window_days: 30,
      prerequisite_mandates: []
    },
    projected_impact: {
      l_score_delta: 0.15,
      g_roi_boost: [0.12, 0.15, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04],
      grace_multiplier: 1.6,
      network_effects: ['accountability', 'covenant_multiplication', 'grace_transfer']
    },
    urgency: 'foundational',
    completion_metrics: {
      progress: 0,
      fruit_metrics: {
        souls_touched: 0,
        covenants_formed: 0,
        generational_impact: 0
      }
    }
  }
];