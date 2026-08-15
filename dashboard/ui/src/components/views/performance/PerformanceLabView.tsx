import React from 'react';
import {
  Cpu,
  ShieldCheck,
  Clock,
  HardDrive,
} from 'lucide-react';

export const PerformanceLabView: React.FC = () => {
  const latencies = [
    { component: 'Observation & State Parsing', time_ms: 0.22, budget_ms: 2.0, pct: 11.0 },
    { component: 'Bayesian Belief State Update', time_ms: 0.31, budget_ms: 3.0, pct: 10.3 },
    { component: 'Goal-Based Macro Strategic Planning', time_ms: 0.18, budget_ms: 2.0, pct: 9.0 },
    { component: 'Legal Candidate Generation & Pruning', time_ms: 0.25, budget_ms: 3.0, pct: 8.3 },
    { component: '1-2 Ply Risk-Aware Search & Valuation', time_ms: 2.15, budget_ms: 15.0, pct: 14.3 },
    { component: 'Deterministic Fallback Safety Check', time_ms: 0.12, budget_ms: 1.0, pct: 12.0 },
  ];

  return (
    <div className="space-y-8 text-left pb-16 max-w-6xl mx-auto">
      {/* 1. Header */}
      <div className="flex flex-col md:flex-row md:items-baseline justify-between gap-4 pb-4 border-b border-white/6">
        <div className="space-y-1">
          <div className="text-[11px] font-mono text-amber-400 font-bold uppercase tracking-wider">
            Runtime Performance // Sub-Millisecond Profiling
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight font-display">
            Performance &amp; System Health Lab
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 font-sans max-w-xl">
            Microsecond-precision execution breakdown, latency percentile distributions, memory profiles, and sandbox safety margins.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="px-3 py-1.5 rounded-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-bold flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>100% LEGAL • 0 INVALID • 0 FALLBACK</span>
          </span>
        </div>
      </div>

      {/* 2. Latency Percentile Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
        <div className="p-4 rounded-lg border border-white/6 bg-[#0B0D12] space-y-1">
          <div className="text-[10px] text-slate-500 uppercase flex items-center gap-1">
            <Clock className="w-3 h-3 text-amber-400" />
            <span>P50 Median Time</span>
          </div>
          <div className="text-2xl font-bold text-white tracking-tight">1.450 ms</div>
          <div className="text-[10px] text-slate-400">Limit: 25.0 ms (5.8% used)</div>
        </div>

        <div className="p-4 rounded-lg border border-white/6 bg-[#0B0D12] space-y-1">
          <div className="text-[10px] text-slate-500 uppercase flex items-center gap-1">
            <Clock className="w-3 h-3 text-amber-400" />
            <span>P95 Strict Latency</span>
          </div>
          <div className="text-2xl font-bold text-cyan-300 tracking-tight">3.747 ms</div>
          <div className="text-[10px] text-emerald-400">85.0% Safety Margin</div>
        </div>

        <div className="p-4 rounded-lg border border-white/6 bg-[#0B0D12] space-y-1">
          <div className="text-[10px] text-slate-500 uppercase flex items-center gap-1">
            <Clock className="w-3 h-3 text-amber-400" />
            <span>P99 Peak Worst</span>
          </div>
          <div className="text-2xl font-bold text-amber-400 tracking-tight">5.210 ms</div>
          <div className="text-[10px] text-emerald-400">Target &lt; 10.0 ms</div>
        </div>

        <div className="p-4 rounded-lg border border-white/6 bg-[#0B0D12] space-y-1">
          <div className="text-[10px] text-slate-500 uppercase flex items-center gap-1">
            <HardDrive className="w-3 h-3 text-amber-400" />
            <span>RAM RSS Footprint</span>
          </div>
          <div className="text-2xl font-bold text-white tracking-tight">121.1 MiB</div>
          <div className="text-[10px] text-slate-400">Limit: 12.2 GiB (0.9%)</div>
        </div>
      </div>

      {/* 3. Subsystem Latency Breakdown */}
      <div className="p-5 rounded-lg border border-white/6 bg-[#0B0D12] space-y-4 font-mono text-xs">
        <div className="flex items-center justify-between border-b border-white/6 pb-2">
          <span className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-amber-400" />
            Subsystem Latency Budget Allocation (Milliseconds)
          </span>
          <span className="text-xs text-emerald-400 font-bold">Total P95: 3.75 ms</span>
        </div>

        <div className="space-y-3">
          {latencies.map((l) => (
            <div key={l.component} className="space-y-1">
              <div className="flex justify-between text-[11px]">
                <span className="text-slate-300 font-sans">{l.component}</span>
                <span className="text-white font-bold">{l.time_ms.toFixed(2)} ms / {l.budget_ms.toFixed(1)} ms</span>
              </div>
              <div className="w-full h-1.5 rounded-xs bg-white/6 overflow-hidden">
                <div
                  style={{ width: `${(l.time_ms / l.budget_ms) * 100}%` }}
                  className="h-full bg-cyan-400"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PerformanceLabView;
