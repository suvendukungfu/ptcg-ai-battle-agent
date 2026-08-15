import React, { useState } from 'react';

export interface DataPoint {
  x: number | string;
  y: number;
  yLower?: number;
  yUpper?: number;
  label?: string;
}

interface TrendChartProps {
  data: DataPoint[];
  color?: string;
  height?: number;
  yMin?: number;
  yMax?: number;
  unit?: string;
  showConfidenceBand?: boolean;
}

export const TrendChart: React.FC<TrendChartProps> = ({
  data,
  color = '#6366f1',
  height = 180,
  yMin,
  yMax,
  unit = '',
  showConfidenceBand = false,
}) => {

  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-36 flex items-center justify-center text-xs text-slate-500 font-mono">
        Awaiting time-series telemetry data...
      </div>
    );
  }

  const computedMin = yMin !== undefined ? yMin : Math.min(...data.map((d) => (d.yLower !== undefined ? d.yLower : d.y))) * 0.96;
  const computedMax = yMax !== undefined ? yMax : Math.max(...data.map((d) => (d.yUpper !== undefined ? d.yUpper : d.y))) * 1.04;
  const yRange = computedMax - computedMin || 1;

  const paddingX = 40;
  const paddingY = 24;
  const svgWidth = 540;
  const svgHeight = height;
  const plotWidth = svgWidth - paddingX * 2;
  const plotHeight = svgHeight - paddingY * 2;

  const points = data.map((d, i) => {
    const x = paddingX + (i / (data.length - 1 || 1)) * plotWidth;
    const y = paddingY + plotHeight - ((d.y - computedMin) / yRange) * plotHeight;
    const yLower = d.yLower !== undefined ? paddingY + plotHeight - ((d.yLower - computedMin) / yRange) * plotHeight : y;
    const yUpper = d.yUpper !== undefined ? paddingY + plotHeight - ((d.yUpper - computedMin) / yRange) * plotHeight : y;
    return { x, y, yLower, yUpper, original: d };
  });

  // Construct smooth SVG Bezier path
  const linePath = points.reduce((acc, pt, i, arr) => {
    if (i === 0) return `M ${pt.x},${pt.y}`;
    const prev = arr[i - 1];
    const cp1x = prev.x + (pt.x - prev.x) / 2;
    const cp1y = prev.y;
    const cp2x = prev.x + (pt.x - prev.x) / 2;
    const cp2y = pt.y;
    return `${acc} C ${cp1x},${cp1y} ${cp2x},${cp2y} ${pt.x},${pt.y}`;
  }, '');

  // Fill area path under curve
  const firstPt = points[0];
  const lastPt = points[points.length - 1];
  const areaPath = `${linePath} L ${lastPt.x},${paddingY + plotHeight} L ${firstPt.x},${paddingY + plotHeight} Z`;

  // Shaded confidence band path
  let bandPath = '';
  if (showConfidenceBand) {
    const upperPath = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x},${p.yUpper}`).join(' ');
    const lowerPath = [...points].reverse().map((p) => `L ${p.x},${p.yLower}`).join(' ');
    bandPath = `${upperPath} ${lowerPath} Z`;
  }

  return (
    <div className="relative w-full overflow-hidden">
      <svg
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className="w-full h-auto overflow-visible select-none"
      >
        <defs>
          <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.3" />
            <stop offset="100%" stopColor={color} stopOpacity="0.0" />
          </linearGradient>
        </defs>

        {/* Horizontal Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => {
          const y = paddingY + plotHeight * ratio;
          const val = computedMax - ratio * yRange;
          return (
            <g key={i}>
              <line
                x1={paddingX}
                y1={y}
                x2={svgWidth - paddingX}
                y2={y}
                stroke="rgba(255, 255, 255, 0.05)"
                strokeDasharray="4 4"
              />
              <text
                x={paddingX - 8}
                y={y + 3}
                fill="#64748b"
                fontSize="9"
                fontFamily="monospace"
                textAnchor="end"
              >
                {val.toFixed(val > 100 ? 0 : 1)}
                {unit}
              </text>
            </g>
          );
        })}

        {/* Confidence Band */}
        {showConfidenceBand && bandPath && (
          <path d={bandPath} fill={color} fillOpacity="0.08" />
        )}

        {/* Gradient fill */}
        <path d={areaPath} fill="url(#areaGradient)" />

        {/* Main trend line */}
        <path d={linePath} fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" />

        {/* Data points */}
        {points.map((pt, i) => {
          const isHovered = hoveredIndex === i;
          return (
            <g
              key={i}
              className="cursor-pointer"
              onMouseEnter={() => setHoveredIndex(i)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              {/* Hit target */}
              <circle cx={pt.x} cy={pt.y} r="12" fill="transparent" />

              {/* Point dot */}
              <circle
                cx={pt.x}
                cy={pt.y}
                r={isHovered ? 5 : 3}
                fill={isHovered ? '#ffffff' : color}
                stroke="#05070d"
                strokeWidth="1.5"
                className="transition-all duration-150"
              />
            </g>
          );
        })}

        {/* Hover Tooltip Annotation */}
        {hoveredIndex !== null && points[hoveredIndex] && (
          <g transform={`translate(${points[hoveredIndex].x}, ${points[hoveredIndex].y - 28})`}>
            <rect
              x="-48"
              y="-10"
              width="96"
              height="24"
              rx="4"
              fill="#1e1b4b"
              stroke={color}
              strokeWidth="1"
              filter="drop-shadow(0 4px 6px rgba(0,0,0,0.5))"
            />
            <text
              x="0"
              y="5"
              fill="#ffffff"
              fontSize="10"
              fontWeight="bold"
              fontFamily="monospace"
              textAnchor="middle"
            >
              {points[hoveredIndex].original.y.toFixed(1)}
              {unit}
              {points[hoveredIndex].original.label ? ` (${points[hoveredIndex].original.label})` : ''}
            </text>
          </g>
        )}
      </svg>
    </div>
  );
};
