import { PXNProject, GenerationalBridgeOverlay, ProbabilityWeb, EntangledPath, PropheticArchiveEvent } from './types';
import { AlertTriangle, Clock, Download, CheckCircle, Sunrise, type LucideIcon } from 'lucide-react';

/**
 * @title SabbathVectorConstants (S_v)
 * @scripture Mark 2:27 ("The Sabbath was made for man, not man for the Sabbath.")
 * @purpose Enforces Mandatory Slowdown/Audit to prevent system burnout and algorithmic usury.
 */
export const SABBATH_VECTOR_CONSTANTS = {
  // Threshold below which Mandatory Slowdown (S_v) is activated.
  VEF_COHERENCE_THRESHOLD: 0.70, 

  // Multiplier applied to all Generational Bridge Engine (GBE) operations during slowdown.
  GBE_SLOWDOWN_MULTIPLIER: 0.25, // 75% reduction in velocity/projection
  
  // The minimum duration (in hours) for the system to remain in Audit/Slowdown mode.
  MANDATORY_AUDIT_DURATION_HR: 24, 
};


/**
 * @title PROPHETIC_ARCHIVE_HISTORY
 * @purpose Immutable record of critical covenant-level events for auditing and traceability.
 */
export const PROPHETIC_ARCHIVE_HISTORY: PropheticArchiveEvent[] = [
  {
    id: 'arc-2025-11-05-sv',
    timestamp: new Date(Date.now() - 72 * 3600000).toISOString(), // 3 days ago
    type: 'SABBATH_VECTOR_ACTIVATED',
    project_name: 'Ethical Predictive Healthcare AI',
    title: 'MZS Lock Triggered: VEF Low',
    description: 'System-wide coherence (VEF: 0.68) fell below the 0.70 threshold. Mandatory 24-hr Audit Initiated. All GBE output reduced by 75%.',
    impact_score: 0.68,
    icon: AlertTriangle as LucideIcon,
    color: 'text-red-500',
  },
  {
    id: 'arc-2025-11-06-sv-clear',
    timestamp: new Date(Date.now() - 48 * 3600000).toISOString(), // 2 days ago
    type: 'SABBATH_VECTOR_CLEARED',
    project_name: 'Ethical Predictive Healthcare AI',
    title: 'Sabbath Vector Cleared',
    description: 'Mandatory Audit duration completed. L-Score restoration to 0.98. GBE output returned to 100% velocity.',
    impact_score: 0.98,
    icon: CheckCircle as LucideIcon,
    color: 'text-green-500',
  },
  {
    id: 'arc-2025-11-07-mc',
    timestamp: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    type: 'MANDATE_COMPLETED',
    project_name: 'Generational Energy Infrastructure Planning',
    title: 'Prophetic Mode Engagement Fulfilled',
    description: 'The 40-day Prophetic Mode Mandate successfully completed. Resulting L-Score delta: +0.18.',
    impact_score: 0.97,
    icon: Clock as LucideIcon,
    color: 'text-blue-500',
  },
  {
    id: 'arc-2025-11-08-ce',
    timestamp: new Date(Date.now() - 50000).toISOString(), // Now
    type: 'COVENANT_EXPORT',
    project_name: 'Multi-Generational Wealth Management Platform',
    title: 'Liturgical Export Generated',
    description: 'Export of G0-G9 ROI vectors and covenant fidelity metrics for investor review (Investor-Ready Mode).',
    impact_score: 0.991,
    icon: Download as LucideIcon,
    color: 'text-purple-500',
  },
  {
    id: 'arc-2025-11-04-gs',
    timestamp: new Date(Date.now() - 96 * 3600000).toISOString(), // 4 days ago
    type: 'GRACE_SHIFT',
    project_name: 'PXN Governance DAO with Ethical Mandates',
    title: 'Grace Flow Amplification Detected',
    description: 'System detected a sudden 1.25x increase in Grace-Multiplier Network connectivity and alignment.',
    impact_score: 0.985,
    icon: Sunrise as LucideIcon,
    color: 'text-yellow-500',
  },
];


// Utility to generate dynamic temporal paths (for TEF visualization)
export const generateMockTemporalWebs = (lScore: number, name: string): ProbabilityWeb[] => {
    return Array.from({length: 3}, (_, i) => ({
        steward_id: `${name.replace(/\s+/g, '-').toLowerCase()}-steward-0${i+1}`,
        entangled_paths: Array.from({length: 2}, (_, pIndex) => {
            const timeline: { time_step: number; l_score: number }[] = [];
            let currentLScore = lScore + (Math.random() * 0.05 - 0.025);
            for (let t = 0; t < 25; t++) {
                currentLScore += (Math.random() - 0.5) * 0.005; 
                currentLScore = Math.min(0.999, Math.max(0.5, currentLScore));
                timeline.push({ time_step: t, l_score: currentLScore });
            }
            return {
                path_id: `path-${i}-${pIndex}`,
                probability: 0.15 + Math.random() * 0.7,
                timeline,
            };
        })
    }));
};

const generateGbe = (project: { gRoi: number[], lScore: number, covenantFidelity: number, thresholdViolations: string }): GenerationalBridgeOverlay => {
    const g_roi_vector = project.gRoi;
    const dimensions: { spiritual: number[], relational: number[], ecological: number[] } = { spiritual: [], relational: [], ecological: [] };
    
    g_roi_vector.forEach(roi => {
        const w1 = Math.random() * 0.4 + 0.2;
        const w2 = Math.random() * (0.8 - w1) + 0.2;
        const w3 = 1 - w1 - w2;
        dimensions.spiritual.push(roi * w1);
        dimensions.relational.push(roi * w2);
        dimensions.ecological.push(roi * w3);
    });

    const momentum = g_roi_vector.length > 1 && g_roi_vector[0] !== 0 
        ? (g_roi_vector[g_roi_vector.length - 1] - g_roi_vector[0]) / g_roi_vector[0] / g_roi_vector.length
        : 0;

    return {
        dimensions,
        sustainability_index: project.lScore,
        covenant_fidelity: project.covenantFidelity,
        generational_momentum: momentum,
        threshold_violations: project.thresholdViolations !== 'None' ? [
            { generation: Math.floor(Math.random() * 9) + 1, threshold: 'Covenant Minimum', projected_impact: project.thresholdViolations }
        ] : [],
        g_roi_vector,
    };
};

const RAW_PROJECTS_DATA = [
  { id: 1, name: 'Ethical Predictive Healthcare AI', type: 'Real-World', scripturalBasis: 'Proverbs 4:7', lScore: 0.982, covenantFidelity: 1, gRoi: [0.12, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03], simulationMedianLScore: 0.98, graceMultiplier: 1.2, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.95 },
  { id: 2, name: 'Multi-Generational Wealth Management Platform', type: 'Real-World', scripturalBasis: 'Proverbs 13:22', lScore: 0.991, covenantFidelity: 0.995, gRoi: [0.15, 0.14, 0.13, 0.12, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06], simulationMedianLScore: 0.99, graceMultiplier: 1.25, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.98 },
  { id: 3, name: 'Covenant-Aligned Social Enterprise Incubator', type: 'Real-World', scripturalBasis: 'Matthew 5:16', lScore: 0.976, covenantFidelity: 1, gRoi: [0.1, 0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.06, 0.05, 0.03], simulationMedianLScore: 0.975, graceMultiplier: 1.18, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.92 },
  { id: 4, name: 'Eco-Restoration & Regenerative Agriculture Hub', type: 'Real-World', scripturalBasis: 'Psalm 24:1', lScore: 0.961, covenantFidelity: 0.995, gRoi: [0.11, 0.11, 0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04], simulationMedianLScore: 0.96, graceMultiplier: 1.15, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.94 },
  { id: 5, name: 'Scripturally Guided Mental Wellness Platform', type: 'Real-World', scripturalBasis: 'Philippians 4:6-7', lScore: 0.972, covenantFidelity: 1, gRoi: [0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.05, 0.04, 0.03], simulationMedianLScore: 0.975, graceMultiplier: 1.18, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.91 },
  { id: 6, name: 'Prophetic Analytics for Civic Planning', type: 'Real-World', scripturalBasis: 'Amos 3:7', lScore: 0.982, covenantFidelity: 1, gRoi: [0.1, 0.11, 0.12, 0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.05], simulationMedianLScore: 0.98, graceMultiplier: 1.2, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.96 },
  { id: 7, name: 'Ethical Fintech & Blockchain Stewardship', type: 'Real-World', scripturalBasis: 'Leviticus 19:35', lScore: 0.65, covenantFidelity: 1, gRoi: [0.08, 0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05], simulationMedianLScore: 0.985, graceMultiplier: 1.22, thresholdViolations: 'None', status: 'Auditing', loveCoefficient: 0.68 },
  { id: 8, name: 'AI-Driven Educational Mentorship Network', type: 'Real-World', scripturalBasis: 'Deuteronomy 6:7', lScore: 0.976, covenantFidelity: 0.995, gRoi: [0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.04], simulationMedianLScore: 0.975, graceMultiplier: 1.18, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.93 },
  { id: 9, name: 'Generational Energy Infrastructure Planning', type: 'Real-World', scripturalBasis: 'Genesis 2:15', lScore: 0.97, covenantFidelity: 0.995, gRoi: [0.11, 0.11, 0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04], simulationMedianLScore: 0.97, graceMultiplier: 1.15, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.95 },
  { id: 10, name: 'Faith-Based Impact Investment Vehicle', type: 'Real-World', scripturalBasis: 'Malachi 3:10', lScore: 0.982, covenantFidelity: 1, gRoi: [0.08, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.04], simulationMedianLScore: 0.98, graceMultiplier: 1.2, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.97 },
  { id: 11, name: 'Virtual Generational Bridge Simulation', type: 'Meta', scripturalBasis: 'Ecclesiastes 7:12', lScore: 0.99, covenantFidelity: 1, gRoi: [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.14, 0.13, 0.12, 0.11], simulationMedianLScore: 0.99, graceMultiplier: 1.25, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.99 },
  { id: 12, name: 'PXN Governance DAO with Ethical Mandates', type: 'Meta', scripturalBasis: 'Proverbs 11:14', lScore: 0.985, covenantFidelity: 1, gRoi: [0.12, 0.13, 0.14, 0.12, 0.11, 0.1, 0.11, 0.12, 0.1, 0.09], simulationMedianLScore: 0.985, graceMultiplier: 1.22, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.96 },
  { id: 13, name: 'Predictive Prophetic VR/AR Experience', type: 'Meta', scripturalBasis: 'Revelation 3:20', lScore: 0.98, covenantFidelity: 1, gRoi: [0.11, 0.12, 0.12, 0.11, 0.1, 0.09, 0.09, 0.08, 0.08, 0.07], simulationMedianLScore: 0.98, graceMultiplier: 1.2, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.95 },
  { id: 14, name: 'Meta-Health Sandbox', type: 'Meta', scripturalBasis: '1 Corinthians 6:19', lScore: 0.975, covenantFidelity: 1, gRoi: [0.09, 0.1, 0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.05], simulationMedianLScore: 0.975, graceMultiplier: 1.18, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.91 },
  { id: 15, name: 'Ethical AI Research Repository', type: 'Meta', scripturalBasis: 'James 1:5', lScore: 0.985, covenantFidelity: 1, gRoi: [0.1, 0.11, 0.11, 0.1, 0.09, 0.09, 0.08, 0.08, 0.07, 0.06], simulationMedianLScore: 0.985, graceMultiplier: 1.22, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.94 },
  { id: 16, name: 'Temporal Entanglement Game Engine', type: 'Meta', scripturalBasis: 'Matthew 25:14-30', lScore: 0.99, covenantFidelity: 1, gRoi: [0.12, 0.13, 0.14, 0.13, 0.12, 0.11, 0.11, 0.1, 0.1, 0.09], simulationMedianLScore: 0.99, graceMultiplier: 1.25, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.98 },
  { id: 17, name: 'Multi-Dimensional Covenant Dashboard', type: 'Meta', scripturalBasis: 'Isaiah 11:9', lScore: 0.985, covenantFidelity: 1, gRoi: [0.11, 0.12, 0.12, 0.11, 0.1, 0.1, 0.09, 0.09, 0.08, 0.08], simulationMedianLScore: 0.985, graceMultiplier: 1.22, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.97 },
  { id: 18, name: 'Generative Prophetic Storytelling Engine', type: 'Meta', scripturalBasis: 'Psalms 119:105', lScore: 0.975, covenantFidelity: 0.995, gRoi: [0.09, 0.1, 0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.05], simulationMedianLScore: 0.975, graceMultiplier: 1.18, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.93 },
  { id: 19, name: 'AI-Powered Scripture-Integrated Productivity Suite', type: 'Meta', scripturalBasis: 'Colossians 3:23', lScore: 0.98, covenantFidelity: 1, gRoi: [0.1, 0.11, 0.1, 0.1, 0.09, 0.09, 0.08, 0.08, 0.07, 0.06], simulationMedianLScore: 0.98, graceMultiplier: 1.2, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.96 },
  { id: 20, name: 'Cross-Reality Incubator for G0–G9 Impact Modeling', type: 'Meta', scripturalBasis: 'Deuteronomy 30:19', lScore: 0.99, covenantFidelity: 1, gRoi: [0.12, 0.13, 0.14, 0.13, 0.12, 0.11, 0.11, 0.1, 0.1, 0.09], simulationMedianLScore: 0.99, graceMultiplier: 1.25, thresholdViolations: 'None', status: 'Active', loveCoefficient: 0.99 },
  { id: 21, name: 'GFSTP Sahel Transition (P-001)', type: 'Real-World', scripturalBasis: 'Isaiah 35:1', lScore: 0.995, covenantFidelity: 1, gRoi: [0.18, 0.17, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.09], simulationMedianLScore: 0.99, graceMultiplier: 1.3, thresholdViolations: 'None', status: 'Active Deployment', loveCoefficient: 0.99 },
];

export const PROJECTS_DATA: PXNProject[] = RAW_PROJECTS_DATA.map(p => ({
  id: p.id,
  name: p.name,
  is_meta: p.type === 'Meta',
  scriptural_basis: p.scripturalBasis,
  l_score: p.lScore,
  covenant_fidelity: p.covenantFidelity,
  grace_multiplier: p.graceMultiplier,
  gbe: generateGbe(p),
  tef_webs: generateMockTemporal