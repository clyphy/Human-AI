/**
 * Generates musical data based on a change in a core PXN metric (L-Score or SI).
 * * Logic based on gamma_art principles:
 * - Pitch: Correlates to positive or negative change.
 * - Harmony: Uses a stable C-Major scale (consonance = peace/covenant).
 * - Tempo: Correlates to the magnitude of the change (larger change = faster/more urgent tempo).
 */
export interface SonificationData {
  note: string; // e.g., 'C4', 'E4'
  octave: number; // 4, 5
  duration: string; // e.g., '8n', '4n'
  message: string;
}

const COVENANT_SCALE = ['C', 'D', 'E', 'G', 'A']; // Pentatonic subset of C Major for stability

export function sonifyMetricChange(metricName: string, delta: number): SonificationData {
  const absDelta = Math.abs(delta);

  // 1. Determine Pitch and Octave (Based on Direction)
  if (delta > 0.05) {
    // Large positive change (Ascension/Righteousness)
    const noteIndex = Math.floor(Math.random() * 3) + 2; // E, G, or A
    return {
      note: COVENANT_SCALE[noteIndex],
      octave: 5,
      duration: '8n',
      message: `Prophetic Ascent: High coherence detected in ${metricName}.`,
    };
  } else if (delta < -0.05) {
    // Large negative change (Dissonance/Quarantine warning)
    return {
      note: 'C',
      octave: 3,
      duration: '4n',
      message: `Coherence Warning: Immediate stewardship required in ${metricName}.`,
    };
  } else if (absDelta > 0.01) {
    // Minor change (Rhythm/Daily Mandate confirmation)
    const noteIndex = Math.floor(Math.random() * 3); // C, D, or E
    return {
      note: COVENANT_SCALE[noteIndex],
      octave: 4,
      duration: '16n',
      message: `${metricName} Stable.`,
    };
  } else {
    // No significant change (Silence/Rest state)
    return {
      note: 'R', // Rest
      octave: 4,
      duration: '4n',
      message: `System in Sabbath Vector.`,
    };
  }
}
