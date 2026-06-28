import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CovenantIcon } from './icons/CovenantIcon';
import { BookOpenIcon } from './icons/BookOpenIcon';
import * as d3 from 'd3';
import { ArchiveEvent, PredictivePath } from '../types';

const MOCK_ARCHIVE_EVENTS: ArchiveEvent[] = [
  {
    timestamp: 'Cycle 2042-Q3',
    lScoreMedian: 0.891,
    lScoreP25: 0.82,
    lScoreP75: 0.94,
    graceDistributed: 12.5,
    syncWinks: [
      { scripture: 'Galatians 6:2', snippet: 'Grace flow initiated for covenant alignment.' },
      { scripture: 'Proverbs 27:17', snippet: 'Mutual sharpening observed in cohort-gamma.' },
    ],
    predictivePaths: [
      { timestamp: 'Q4', projectedLScore: 89, scripture: 'Hebrews 10:24', principle: 'Mutual Encouragement' },
      { timestamp: 'Q1', projectedLScore: 91, scripture: '1 Cor 12:26', principle: 'Shared Witness' },
      { timestamp: 'Q2', projectedLScore: 92, scripture: 'Acts 2:44', principle: 'Covenant Commons' },
      { timestamp: 'Q3', projectedLScore: 93, scripture: 'Rev 20:12', principle: 'Immutable Record' },
    ],
  },
  {
    timestamp: 'Cycle 2042-Q2',
    lScoreMedian: 0.885,
    lScoreP25: 0.81,
    lScoreP75: 0.93,
    graceDistributed: 10.2,
    syncWinks: [
      { scripture: 'Ecclesiastes 3:1', snippet: 'Seasonal adjustment in GVE model.' },
    ],
    predictivePaths: [
      { timestamp: 'Q3', projectedLScore: 88, scripture: 'Hebrews 10:24', principle: 'Mutual Encouragement' },
      { timestamp: 'Q4', projectedLScore: 89, scripture: '1 Cor 12:26', principle: 'Shared Witness' },
      { timestamp: 'Q1', projectedLScore: 90, scripture: 'Acts 2:44', principle: 'Covenant Commons' },
    ],
  },
];

const TemporalPath = ({ path }: { path: PredictivePath[] }) => {
  const lineGenerator = d3.line<{timestamp:string, projectedLScore:number}>()
    .x((d, i) => 20 + i * 80)
    .y(d => 100 - (d.projectedLScore - 80) * 5) // Scale y-axis for better visualization
    .curve(d3.curveBasis);

  const pathString = lineGenerator(path as any) || '';

  return (
    <motion.path
      d={pathString}
      fill="none"
      stroke="#facc15" // yellow-400
      strokeWidth={2}
      initial={{ pathLength: 0 }}
      animate={{ pathLength: 1 }}
      transition={{ duration: 2, ease: "easeInOut" }}
      strokeDasharray="4 2"
      title={path.map(p => `${p.timestamp}: ${p.projectedLScore.toFixed(0)} (${p.scripture})`).join('\n')}
    />
  );
};


const PropheticTimelineWithEntanglement = () => {
  const [events, setEvents] = useState<ArchiveEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data from /api/archive/timeline
    const timer = setTimeout(() => {
        setEvents(MOCK_ARCHIVE_EVENTS);
        setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <div className="flex items-center justify-center h-full text-cyan-400">Loading timeline data...</div>
  }

  return (
    <div className="h-full overflow-y-auto pr-2 text-gray-200">
      <div className="space-y-6">
        {events.map((event, idx) => (
          <div key={idx} className="p-4 bg-gray-800/60 border border-cyan-800/50 rounded-lg relative">
            <p className="text-sm text-gray-400">{event.timestamp}</p>
            <p className="text-lg font-bold flex items-center mb-2 text-cyan-200">
              <CovenantIcon className="w-5 h-5 mr-2 text-pink-400"/> Median L-Score: {event.lScoreMedian.toFixed(3)}
            </p>

            {/* SVG Container for Temporal Paths */}
            <div className='pl-4'>
                <p className="text-xs text-yellow-400/80 mb-1">Projected Fidelity Path:</p>
                <svg width="100%" height={100} className="mb-2 -ml-4">
                  {event.predictivePaths.length > 0 && <TemporalPath path={event.predictivePaths} />}
                </svg>
            </div>


            {/* Sync-Winks */}
            <div className="flex flex-wrap mt-2 pt-3 border-t border-cyan-800/50">
              {event.syncWinks.map((wink, i) => (
                <motion.div
                  key={i}
                  className="mr-2 mb-2 px-3 py-1 rounded-full bg-cyan-900/50 border border-cyan-700/50 text-cyan-300 text-xs cursor-pointer flex items-center gap-2"
                  whileHover={{ scale: 1.05, background: 'rgba(22, 78, 99, 0.7)' }} // cyan-800/70
                  title={`${wink.scripture}: ${wink.snippet}`}
                >
                  <BookOpenIcon className="w-3 h-3" />
                  <span>{wink.scripture}</span>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PropheticTimelineWithEntanglement;
