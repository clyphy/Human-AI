import React from 'react';
import { ProbabilityWeb } from '../types';

const TemporalPathRenderer: React.FC<{
  webs: ProbabilityWeb[];
  viewMode: 'individual' | 'networked';
  onPathHover: (stewardId: string | null) => void;
}> = ({ webs, viewMode, onPathHover }) => {
  return (
    <group onPointerMiss={() => onPathHover(null)}>
      {webs.map((web, webIndex) => {
        const basePosition: [number, number, number] = [
          (webIndex % 3) * 8 - 8,
          Math.floor(webIndex / 3) * 6 - 6,
          0
        ];
        
        return (
          <group key={web.steward_id} position={basePosition}>
            <mesh 
              position={[0, 0, 0]}
              onPointerEnter={() => onPathHover(web.steward_id)}
            >
              <sphereGeometry args={[0.3, 16, 16]} />
              <meshBasicMaterial color="#9333ea" />
            </mesh>
            
            {web.entangled_paths.map((path, pathIndex) => {
              const points = path.timeline.map((point, t) => [
                t * 0.5,
                point.l_score * 4 - 2,
                (pathIndex - web.entangled_paths.length / 2) * 0.8
              ]);
              
              const vertices = new Float32Array(points.flat());

              return (
                <group key={path.path_id}>
                  <line>
                    <bufferGeometry>
                      <bufferAttribute
                        attach="attributes-position"
                        count={points.length}
                        array={vertices}
                        itemSize={3}
                      />
                    </bufferGeometry>
                    <lineBasicMaterial 
                      color={path.probability > 0.2 ? '#10b981' : '#ef4444'}
                      transparent
                      opacity={path.probability}
                      linewidth={2}
                    />
                  </line>
                  
                  {points.map((point, t) => (
                    (t % 5 === 0 && t > 0) && (
                      <mesh key={t} position={[point[0], point[1], point[2]]}>
                        <sphereGeometry args={[0.1, 8, 8]} />
                        <meshBasicMaterial 
                          color={path.timeline[t].l_score > 0.8 ? '#10b981' : '#f59e0b'}
                          transparent
                          opacity={0.6}
                        />
                      </mesh>
                    )
                  ))}
                </group>
              );
            })}
          </group>
        );
      })}
    </group>
  );
};

export default TemporalPathRenderer;
