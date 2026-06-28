import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Text } from '@react-three/drei';
import * as THREE from 'three';
import { PXNProject, BridgeData, TemporalTimelinePoint } from '../types';

interface TemporalEntanglementForgeProps {
  projects: PXNProject[];
  bridges: BridgeData[];
  timelines: TemporalTimelinePoint[];
}

// Coherence Shimmer Field
const CoherenceField = ({ coherence }: { coherence: number }) => {
  const meshRef = useRef<THREE.Mesh>(null!);

  useFrame(({ clock }) => {
    const time = clock.getElapsedTime();
    // Pulsating effect for opacity
    if (meshRef.current && meshRef.current.material) {
        (meshRef.current.material as THREE.MeshStandardMaterial).opacity = coherence * 0.2 + Math.sin(time) * 0.05;
    }
  });

  return (
    <mesh ref={meshRef} position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[20, 20, 10, 10]} />
      <meshStandardMaterial
        color="#0891b2" // cyan-600
        emissive="#0e7490" // cyan-700
        emissiveIntensity={coherence * 2}
        transparent
        wireframe
      />
    </mesh>
  );
};

// Temporal Recursion Loops
const PropheticRings = ({ rotationSpeed }: { rotationSpeed: number }) => {
  const ringsRef = useRef<THREE.Group>(null!);

  useFrame(() => {
    if (ringsRef.current) {
        ringsRef.current.rotation.x += 0.001 * rotationSpeed;
        ringsRef.current.rotation.y += 0.002 * rotationSpeed;
    }
  });

  return (
    <group ref={ringsRef}>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[3, 0.05, 16, 100]} />
        <meshStandardMaterial color="#67e8f9" emissive="#06b6d4" emissiveIntensity={2} toneMapped={false} />
      </mesh>
      <mesh rotation={[Math.PI / 2, Math.PI / 3, 0]}>
        <torusGeometry args={[3.5, 0.05, 16, 100]} />
        <meshStandardMaterial color="#a5f3fc" emissive="#22d3ee" emissiveIntensity={2} toneMapped={false} />
      </mesh>
      <mesh rotation={[Math.PI / 2, -Math.PI / 3, 0]}>
        <torusGeometry args={[4, 0.05, 16, 100]} />
        <meshStandardMaterial color="#cffafe" emissive="#67e8f9" emissiveIntensity={2} toneMapped={false} />
      </mesh>
    </group>
  );
};

// Bridge and Timeline Nodes and connecting Beams
const AlignmentNodes = ({ bridges, timelines }: { bridges: BridgeData[], timelines: TemporalTimelinePoint[] }) => {
  const bridgePositions = useMemo(() => 
    bridges.map((_, i) => new THREE.Vector3(-5 + i * 5, 0.5, 3)),
  [bridges]);
  
  const timelinePositions = useMemo(() => 
    timelines.map((_, i) => new THREE.Vector3(-5 + i * 5, 0.5, -3)),
  [timelines]);

  const allPositions = [...bridgePositions, ...timelinePositions];
  const allLabels = [...bridges.map(b => b.name), ...timelines.map(t => t.label)];

  return (
    <group>
      {/* Nodes */}
      {allPositions.map((pos, i) => (
        <group key={i} position={pos.toArray()}>
            <mesh>
              <sphereGeometry args={[0.2, 16, 16]} />
              <meshStandardMaterial color={i < bridges.length ? "#a855f7" : "#ec4899"} emissive={i < bridges.length ? "#9333ea" : "#db2777"} emissiveIntensity={1} toneMapped={false} />
            </mesh>
             <Text
                position={[0, -0.5, 0]}
                fontSize={0.3}
                color="#e5e7eb"
                anchorX="center"
              >
                {allLabels[i].split(' ')[0]}
              </Text>
        </group>
      ))}

      {/* Beams */}
      {bridgePositions.map((bridgePos, i) => (
        <Line
          key={`line-${i}`}
          points={[bridgePos, timelinePositions[i] || new THREE.Vector3(0,0,0)]} // Fallback for mismatched lengths
          color={"#f472b6"}
          lineWidth={1.5}
          dashed
          dashScale={10}
          dashSize={0.5}
          gapSize={0.5}
        />
      ))}
    </group>
  );
};

export const TemporalEntanglementForge: React.FC<TemporalEntanglementForgeProps> = ({ projects, bridges, timelines }) => {
  const avgIntegrity = useMemo(() =>
    bridges.length > 0 ? bridges.reduce((sum, b) => sum + b.integrity, 0) / bridges.length : 0,
  [bridges]);

  const avgLove = useMemo(() =>
    projects.length > 0 ? projects.reduce((sum, p) => sum + p.loveCoefficient, 0) / projects.length : 0,
  [projects]);
  
  const avgLScore = useMemo(() =>
    projects.length > 0 ? projects.reduce((sum, p) => sum + p.l_score, 0) / projects.length : 0,
  [projects]);

  const coherence = (avgIntegrity + avgLove) / 2;
  const rotationSpeed = avgLScore * 2; // Scale for visible effect

  return (
    <div className="w-full h-full bg-gray-950 rounded-lg">
       <Canvas camera={{ position: [0, 5, 10], fov: 60 }}>
        <color attach="background" args={['#030712']} />
        <fog attach="fog" args={['#030712', 10, 25]} />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={100} color="#06b6d4" />
        <pointLight position={[-10, -5, -10]} intensity={80} color="#a855f7" />
        
        <CoherenceField coherence={coherence} />
        <PropheticRings rotationSpeed={rotationSpeed} />
        <AlignmentNodes bridges={bridges} timelines={timelines} />

        <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} minPolarAngle={Math.PI / 4} maxPolarAngle={Math.PI / 2} />
      </Canvas>
      <div className="absolute top-4 right-4 bg-gray-900/50 backdrop-blur-sm p-3 rounded-lg border border-cyan-700/50 text-cyan-300 text-xs font-mono pointer-events-none">
        <p>System Coherence: <span className="text-cyan-200 font-bold">{(coherence * 100).toFixed(1)}%</span></p>
        <p>Avg. L-Score: <span className="text-cyan-200 font-bold">{avgLScore.toFixed(3)}</span></p>
      </div>
    </div>
  );
};

export default TemporalEntanglementForge;
