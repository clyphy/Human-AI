import React from 'react';
import { type PropheticArchiveEvent, type ArchiveEventType } from '../types';
import { History } from 'lucide-react';
import {Card, CardContent, CardHeader, CardTitle} from './ui/Card';


const PropheticArchiveTimeline: React.FC<{ archive: PropheticArchiveEvent[] }> = ({ archive }) => {
  
  const getEventTypeStyle = (type: ArchiveEventType) => {
    switch (type) {
      case 'SABBATH_VECTOR_ACTIVATED':
        return 'bg-red-900 border-red-500';
      case 'SABBATH_VECTOR_CLEARED':
        return 'bg-green-900 border-green-500';
      case 'MANDATE_COMPLETED':
        return 'bg-blue-900 border-blue-500';
      case 'COVENANT_EXPORT':
        return 'bg-purple-900 border-purple-500';
      case 'GRACE_SHIFT':
        return 'bg-yellow-900 border-yellow-500';
      default:
        return 'bg-gray-900 border-gray-500';
    }
  };

  const sortedArchive = [...archive].sort((a, b) => 
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );

  return (
    <Card className="bg-gray-900 border-gray-700 text-white shadow-2xl h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center text-lg text-green-300">
          <History className="h-5 w-5 mr-2" /> Prophetic Archive
        </CardTitle>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto space-y-8 pr-2">
        {sortedArchive.map((event, index) => {
          const Icon = event.icon;
          const eventStyle = getEventTypeStyle(event.type);
          const time = new Date(event.timestamp).toLocaleString('en-US', {
            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
          });

          return (
            <div key={event.id} className="relative flex">
              {index < sortedArchive.length - 1 && (
                <div className="absolute left-3.5 top-0 w-0.5 h-full bg-gray-700 z-0" />
              )}
              <div className="flex-shrink-0 z-10">
                <div className={`h-7 w-7 rounded-full flex items-center justify-center border-2 ${eventStyle}`}>
                  <Icon className={`h-4 w-4 ${event.color}`} />
                </div>
              </div>
              <div className="ml-5 pb-8 flex-1 min-w-0">
                <div className="text-sm font-semibold text-white truncate">{event.title}</div>
                <div className="text-xs text-gray-400 mt-0.5">{time}</div>
                <p className="text-xs text-gray-500 mt-2">
                  {event.description}
                </p>
                <div className="text-xs mt-1 font-mono">
                    <span className="font-medium text-gray-500">Impact:</span> <span className="text-white">{event.impact_score.toFixed(3)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </CardContent>
      
      {archive.length === 0 && (
        <div className="text-center p-10 text-gray-500">
          <History className="h-10 w-10 mx-auto mb-3" />
          No events recorded.
        </div>
      )}
    </Card>
  );
};

export default PropheticArchiveTimeline;