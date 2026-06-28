import React from 'react';
import Header from './components/Header';
import { DashboardView } from './components/DashboardView';
import { PROJECTS_DATA } from './constants';
import { MANDATE_CATALOG } from './MandateCatalog';
import { type BridgeData, type WebData, type TemporalTimelinePoint, PXNProject, PropheticMandate } from './types';

// Mock data for timelines as it's not derived from existing project data.
const mockTimelines: TemporalTimelinePoint[] = [
  { id: 'timeline-1', label: 'Q3 2042 Coherence', coherence: 0.92 },
  { id: 'timeline-2', label: 'Q4 2042 Projection', coherence: 0.95 },
  { id: 'timeline-3', label: 'Q1 2043 Kairos Window', coherence: 0.88 },
];

const App = () => {
  // Load static data
  const projects: PXNProject[] = PROJECTS_DATA;
  const mandates: PropheticMandate[] = MANDATE_CATALOG;

  // Transform project data into the structures required by the new DashboardView
  const bridges: BridgeData[] = projects.map(p => ({
    id: `bridge-${p.id}`,
    name: `${p.name}`,
    integrity: p.gbe.sustainability_index,
  }));

  const webs: WebData[] = projects.flatMap(p => 
    p.tef_webs.map(w => ({
      id: w.steward_id,
      alignment: w.entangled_paths.reduce((acc, path: any) => acc + path.probability, 0) / w.entangled_paths.length,
    }))
  ).slice(0, 6); // Limit for display purposes

  const timelines: TemporalTimelinePoint[] = mockTimelines;

  return (
    <div className="w-full min-h-screen bg-gray-950" style={{ fontFamily: '"Roboto", sans-serif' }}>
      <Header />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <DashboardView
          projects={projects}
          mandates={mandates}
          bridges={bridges.slice(0, 3)} // Limit for display
          timelines={timelines}
          webs={webs}
        />
      </main>
    </div>
  );
};

export default App;
