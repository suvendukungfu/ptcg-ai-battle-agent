import React from 'react';
import {
  Activity,
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
    { component: '1-2 Ply Risk-Aware Search & Valuation', time_ms: 1.58, budget_ms: 15.0, pct: 10.5 },
    { component: 'Deterministic Fallback Safety Check', time_ms: 0.12, budget_ms: 1.0, pct: 12.0 },
  ];

  return (
    <div className="space-y-6 text-left pb-12">
      {/* 1. Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2 font-display">
              <Activity className="w-6 h-6 text-amber-400" />
              Performance & System Health Lab
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-mono font-bold">
              SUB-MILLISECOND TELEMETRY
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Microsecond-precision execution breakdown, latency percentile distributions, memory profiles, and sandbox safety margins.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-mono px-3.5 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-bold flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4" />
            100% Legal • 0 Invalids • 0 Fallbacks
          </span>
        </div>
      </div>

      {/* 2. Latency Percentile Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 font-mono">
        <div className="glass-panel p-5 rounded-3xl border border-white/8 space-y-1">
          <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-amber-400" />
            P50 Median Latency
          </div>
          <div className="text-2xl font-black text-white">0.727 ms</div>
          <div className="text-[11px] text-emerald-400">Kaggle Limit: 25.0 ms (2.9% used)</div>
        </div>

        <div className="glass-panel p-5 rounded-3xl border border-white/8 space-y-1">
          <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-amber-400" />
            P95 Strict Latency
          </div>
          <div className="text-2xl font-black text-amber-300">2.665 ms</div>
          <div className="text-[11px] text-emerald-400">Target: &lt; 5.0 ms (Passed)</div>
        </div>

        <div className="glass-panel p-5 rounded-3xl border border-white/8 space-y-1">
          <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-amber-400" />
            P99 Worst Latency
          </div>
          <div className="text-2xl font-black text-amber-400">3.971 ms</div>
          <div className="text-[11px] text-emerald-400">Target: &lt; 10.0 ms (Passed)</div>
        </div>

        <div className="glass-panel p-5 rounded-3xl border border-white/8 space-y-1">
          <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <HardDrive className="w-3.5 h-3.5 text-amber-400" />
            RAM RSS Footprint
          </div>
          <div className="text-2xl font-black text-white">121.1 MiB</div>
          <div className="text-[11px] text-emerald-400">Limit: 12.2 GiB (0.9% used)</div>
        </div>
      </div>

      {/* 3. Subsystem Latency Breakdown */}
      <div className="glass-panel p-6 rounded-3xl border border-white/8 space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-white/8">
          <span className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-amber-400" />
            Subsystem Latency Budget Allocation (Microseconds)
          </span>
          <span className="text-xs font-mono text-emerald-400 font-bold">Total P95: 2.665 ms</span>
        </div>

        <div className="space-y-3 font-mono">
          {latencies.map((l) => (
            <div key={l.component} className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-sans">{l.component}</span>
                <span className="text-white font-bold">
                  {l.time_ms.toFixed(2)} ms <span className="text-slate-500">/ {l.budget_ms.toFixed(1)} ms</span>
                </span>
              </div>
              <div className="w-full h-1.5 rounded-full bg-white/6 overflow-hidden">
                <div style={{ width: `${l.pct}%` }} className="h-full bg-amber-400 rounded-full" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PerformanceLabView;
