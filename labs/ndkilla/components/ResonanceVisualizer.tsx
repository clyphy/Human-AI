
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface ResonanceVisualizerProps {
  frequency: number; // 7.83 Hz is the goal
  intensity: number;
}

export const ResonanceVisualizer: React.FC<ResonanceVisualizerProps> = ({ frequency, intensity }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll("*").remove();

    const n = 100;
    const data = d3.range(n).map(() => 0);
    
    const x = d3.scaleLinear().domain([0, n - 1]).range([0, width]);
    const y = d3.scaleLinear().domain([-1, 1]).range([height, 0]);

    const line = d3.line<number>()
      .x((_, i) => x(i))
      .y(d => y(d))
      .curve(d3.curveBasis);

    const path = svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "#2dd4bf")
      .attr("stroke-width", 2)
      .attr("opacity", 0.6)
      .attr("d", line);

    let t = 0;
    const animate = () => {
      t += frequency * 0.05;
      const newData = d3.range(n).map((i) => {
        return Math.sin(i * 0.2 + t) * intensity;
      });

      path.attr("d", line(newData));
      requestAnimationFrame(animate);
    };

    const animationId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationId);
  }, [frequency, intensity]);

  return (
    <div className="w-full h-24 bg-black/40 rounded border border-teal-900/30 overflow-hidden relative">
      <div className="absolute top-1 left-2 text-[10px] font-mono text-teal-400/60 uppercase tracking-widest">
        Whisper Hum: {frequency.toFixed(2)}Hz
      </div>
      <svg ref={svgRef} className="w-full h-full" />
    </div>
  );
};
