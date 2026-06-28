import { PropheticPreset } from './types';

// Adheres to 3.2 Prophetic Presets System
export const PROPHETIC_PRESETS: PropheticPreset[] = [
  {
    id: 'prophetic_mode',
    name: 'Prophetic Mode',
    description: 'Maximum covenant sensitivity—for councils and seers',
    gamma_ecological: 0.12,
    gamma_social: 0.18,
    gamma_financial: 0.16,
    grace_bias: 0.15
  },
  {
    id: 'balanced_covenant',
    name: 'Balanced Covenant',
    description: 'Standard household stewardship model',
    gamma_ecological: 0.12,
    gamma_social: 0.14,
    gamma_financial: 0.13,
    grace_bias: 0.13
  },
  {
    id: 'covenantal_minimum',
    name: 'Covenant Minimum',
    description: 'Entry-level threshold—grace-enabled accessibility',
    gamma_ecological: 0.12,
    gamma_social: 0.10,
    gamma_financial: 0.10,
    grace_bias: 0.10
  }
];
