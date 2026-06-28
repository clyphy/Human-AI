import { CovenantAlert, GROIVector, LScoreData } from './types';

// Enforces 3.1 G-ROI Threshold Alerts and the MWRPI (implicitly via totalGRoi)
export class ThresholdMonitor {
  private readonly RIGHTEOUS_FLOOR = 0.85;
  private readonly WARNING_THRESHOLD = 0.70;
  private readonly MIN_TOTAL_GROI = 10.0; // The Generational Floor Mandate

  public evaluate(gRoiVector: GROIVector, lScore: number): CovenantAlert | null {
    const totalGRoi = gRoiVector.reduce((a, b) => a + b, 0);

    // CRITICAL FAILURE: L-Score below safety OR Generational commitment (Total G-ROI) failed.
    if (lScore < this.WARNING_THRESHOLD || totalGRoi < this.MIN_TOTAL_GROI) {
      return {
        severity: 'critical',
        message: 'Covenant alignment below prophetic threshold.',
        action: 'initiate_humility_protocol',
        scriptureAnchor: 'James 4:6', // God opposes the proud but shows favor to the humble.
        visualCue: 'red_pulse_border',
        timestamp: new Date()
      };
    }

    // WARNING ZONE: Approaching the edge of grace.
    if (lScore < this.RIGHTEOUS_FLOOR) {
      return {
        severity: 'warning',
        message: 'Approaching righteousness threshold.',
        action: 'increase_stewardship_focus',
        scriptureAnchor: 'Matthew 25:21', // Well done, good and faithful servant!
        visualCue: 'amber_glow',
        timestamp: new Date()
      };
    }

    return null; // Covenant is healthy (L >= 0.85 and G-ROI >= 10.0)
  }
}
