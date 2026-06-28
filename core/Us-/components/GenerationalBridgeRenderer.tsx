import React from 'react';
import { Text } from '@react-three/drei';
import { GenerationalBridgeOverlay } from '../types';

const GenerationalBridgeRenderer: React.FC<{ overlay: GenerationalBridgeOverlay }> = ({ overlay }) => {
  return (
    <group position={[0, 0, -5]}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -2, 0]}>
        <planeGeometry args={[20, 8]} />
        <meshBasicMaterial color="#1e293b" transparent opacity={0.3} />
      </mesh>
      
      {overlay.g_roi_vector.map((roi, generation) => {
        const height = roi / 10;
        const x = (generation - 4.5) * 2;
        
        return (
          <group key={generation} position={[x, 0, 0]}>
            <mesh position={[0, height / 2, 0]}>
              <boxGeometry args={[0.5, height, 0.5]} />
              <meshPhongMaterial 
                color={
                  roi > 50 ? '#10b981' :
                  roi > 30 ? '#f59e0b' : '#ef4444'
                }
                transparent
                opacity={0.8}
              />
            </mesh>
            
            <mesh position={[0, (overlay.dimensions.spiritual[generation] / 20), 0.3]}>
              <boxGeometry args={[0.3, (overlay.dimensions.spiritual[generation] / 10), 0.3]} />
              <meshBasicMaterial color="#c084fc" />
            </mesh>
            
            <mesh position={[0.3, (overlay.dimensions.relational[generation] / 20), 0]}>
              <boxGeometry args={[0.3, (overlay.dimensions.relational[generation] / 10), 0.3]} />
              <meshBasicMaterial color="#60a5fa" />
            </mesh>
            
            <mesh position={[0, (overlay.dimensions.ecological[generation] / 20), -0.3]}>
              <boxGeometry args={[0.3, (overlay.dimensions.ecological[generation] / 10), 0.3]} />
              <meshBasicMaterial color="#34d399" />
            </mesh>
            
            <Text
              position={[0, -1, 0]}
              fontSize={0.4}
              color="#ffffff"
              anchorX="center"
              anchorY="middle"
            >
              G{generation}
            </Text>
            
            <Text
              position={[0, height + 0.5, 0]}
              fontSize={0.3}
              color={
                roi > 50 ? '#10b981' :
                roi > 30 ? '#f59e0b' : '#ef4444'
              }
              anchorX="center"
              anchorY="middle"
            >
              {roi.toFixed(2)}
            </Text>
          </group>
        );
      })}
      
      <group>
        {overlay.g_roi_vector.slice(0, -1).map((_, generation) => {
          const startX = (generation - 4.5) * 2;
          const endX = (generation - 3.5) * 2;
          const startHeight = overlay.g_roi_vector[generation] / 10;
          const endHeight = overlay.g_roi_vector[generation + 1] / 10;
          const vertices = new Float32Array([
            startX, startHeight, 0,
            endX, endHeight, 0
          ]);
          
          return (
            <line key={generation}>
              <bufferGeometry>
                <bufferAttribute
                  attach="attributes-position"
                  count={2}
                  array={vertices}
                  itemSize={3}
                />
              </bufferGeometry>
              <lineBasicMaterial 
                color="#c084fc" 
                transparent 
                opacity={0.6}
                linewidth={2}
              />
            </line>
          );
        })}
      </group>
    </group>
  );
};

export default GenerationalBridgeRenderer;
