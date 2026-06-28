import React from 'react';
import {
  PXNProject,
  PropheticMandate,
  BridgeData,
  TemporalTimelinePoint,
  WebData,
} from '../types';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Compass, Zap, Waypoints, AlertTriangle, ChevronRight, BrainCircuit } from 'lucide-react';
import Gauge from './Gauge';
import { TemporalEntanglementForge } from './TemporalEntanglementForge';

interface DashboardViewProps {
  projects: PXNProject[];
  mandates: PropheticMandate[];
  bridges: BridgeData[];
  timelines: TemporalTimelinePoint[];
  webs: WebData[];
}

/**
 * DashboardView — Prophetic Nexus Edition
 * Integrates covenant-aligned analytics, temporal entanglement overlays,
 * and real-time integrity fidelity metrics.
 */
export const DashboardView: React.FC<DashboardViewProps> = ({
  projects,
  mandates,
  bridges,
  timelines,
  webs
}) => {
  return (
    <div className="space-y-6">
      {/* Temporal Entanglement Forge - Hero Section */}
      <Card className="bg-gray-900 border-cyan-700/50 h-96 overflow-hidden p-0">
         <CardHeader className="absolute top-0 left-0 z-10 bg-gradient-to-b from-gray-950/80 to-transparent p-4">
            <CardTitle className="text-cyan-300 text-lg flex items-center gap-2 font-orbitron">
              <BrainCircuit className="w-5 h-5" />
              Temporal Entanglement Forge
            </CardTitle>
          </CardHeader>
        <TemporalEntanglementForge 
          projects={projects}
          bridges={bridges}
          timelines={timelines}
        />
      </Card>

      {/* Existing Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Generational Bridge Overlays */}
        {bridges.map((bridge) => (
          <Card key={bridge.id} className="bg-gray-900/80 border-cyan-700/50 hover:shadow-xl hover:border-cyan-600 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-cyan-300 text-base">{bridge.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400">
                Integrity Fidelity: {bridge.integrity.toFixed(2)} / 1.0
              </p>
              <Gauge value={bridge.integrity} max={1.0} />
              <Waypoints className="mt-2 text-blue-500" />
            </CardContent>
          </Card>
        ))}

        {/* Temporal Timeline Points */}
        {timelines.map((point) => (
          <Card key={point.id} className="bg-gray-900/80 border-cyan-700/50 hover:shadow-xl hover:border-cyan-600 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-cyan-300 text-base">{point.label}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400">Coherence Score: {point.coherence.toFixed(2)}</p>
              <Compass className="mt-2 text-green-500" />
            </CardContent>
          </Card>
        ))}

        {/* Probability Webs / Synchronicity */}
        {webs.map((web) => (
          <Card key={web.id} className="bg-gray-900/80 border-cyan-700/50 hover:shadow-xl hover:border-cyan-600 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-cyan-300 text-base">Synchronicity Web</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400">Predicted Alignment: {web.alignment.toFixed(2)}</p>
              <Zap className="mt-2 text-yellow-500" />
            </CardContent>
          </Card>
        ))}

        {/* Prophetic Mandates */}
        {mandates.map((mandate) => (
          <Card key={mandate.id} className="bg-gray-900/80 border-purple-500/50 hover:shadow-xl hover:border-purple-400 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-purple-300 text-base">{mandate.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400">{mandate.description}</p>
              {mandate.warning && (
                 <div className="flex items-center text-red-400 mt-2 text-xs">
                  <AlertTriangle className="h-4 w-4 mr-2" />
                  {mandate.warning}
                </div>
              )}
              <ChevronRight className="mt-2" />
            </CardContent>
          </Card>
        ))}

        {/* Active PXN Projects */}
        {projects.slice(0, 3).map((project) => ( // Limit for display
          <Card key={project.id} className="bg-gray-900/80 border-cyan-700/50 hover:shadow-xl hover:border-cyan-600 transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-cyan-300 text-base">{project.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400">Status: {project.status}</p>
              <p className="text-sm text-gray-400">Love Coefficient (𝓛): {project.loveCoefficient.toFixed(2)}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};