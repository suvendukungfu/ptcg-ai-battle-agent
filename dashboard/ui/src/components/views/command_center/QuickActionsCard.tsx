import React, { useState } from 'react';
import type { ViewSuite } from '../../../types';
import { api } from '../../../services/api';
import {
  Swords,
  BrainCircuit,
  Zap,
  Presentation,
  Loader2,
  CheckCircle2,
} from 'lucide-react';

interface QuickActionsCardProps {
  onNavigate: (suite: ViewSuite) => void;
  onBenchmarkComplete?: () => void;
}

export const QuickActionsCard: React.FC<QuickActionsCardProps> = ({
  onNavigate,
  onBenchmarkComplete,
}) => {
  const [benchmarking, setBenchmarking] = useState<boolean>(false);
  const [benchmarkResult, setBenchmarkResult] = useState<string | null>(null);

  const handleRunBenchmark = async () => {
    try {
      setBenchmarking(true);
      setBenchmarkResult(null);
      const res = await api.runBenchmark(10);
      setBenchmarkResult(`10-Game Test: ${res.win_rate_pct.toFixed(1)}% WR | ${res.latency_avg_ms.toFixed(2)}ms avg latency`);
      if (onBenchmarkComplete) onBenchmarkComplete();
    } catch (err) {
      setBenchmarkResult('Benchmark failed to execute');
    } finally {
      setBenchmarking(false);
    }
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border border-white/8 space-y-4">
      <div className="pb-2 border-b border-white/8">
        <h3 className="text-base font-bold text-white tracking-tight">
          Tactical Mission Launchpad
        </h3>
        <p className="text-xs text-slate-400 mt-0.5">
          One-click shortcuts to live battle simulation, decision inspection, and automated diagnostics.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Action 1: Live Arena */}
        <button
          onClick={() => onNavigate('arena')}
          className="p-3.5 rounded-xl bg-linear-to-br from-indigo-600/30 to-indigo-900/30 hover:from-indigo-600/50 hover:to-indigo-900/50 border border-indigo-500/40 text-left space-y-1.5 transition-all group shadow-lg shadow-indigo-500/10"
        >
          <div className="flex items-center justify-between">
            <Swords className="w-5 h-5 text-indigo-400 group-hover:scale-110 transition-transform" />
            <span className="text-[10px] font-mono font-bold text-indigo-300">ARENA</span>
          </div>
          <div className="text-sm font-bold text-white">Live Battle Arena</div>
          <div className="text-[11px] text-slate-300">Watch agent play against heuristic baseline</div>
        </button>

        {/* Action 2: Decision Explainer */}
        <button
          onClick={() => onNavigate('decision')}
          className="p-3.5 rounded-xl bg-white/2 hover:bg-white/5 border border-white/6 hover:border-white/12 text-left space-y-1.5 transition-all group"
        >
          <div className="flex items-center justify-between">
            <BrainCircuit className="w-5 h-5 text-amber-400 group-hover:scale-110 transition-transform" />
            <span className="text-[10px] font-mono font-bold text-amber-300">EXPLAIN</span>
          </div>
          <div className="text-sm font-bold text-white">Decision Explainer</div>
          <div className="text-[11px] text-slate-400">Additive value decomposition & counterfactuals</div>
        </button>

        {/* Action 3: Micro Benchmark */}
        <button
          onClick={handleRunBenchmark}
          disabled={benchmarking}
          className="p-3.5 rounded-xl bg-white/2 hover:bg-white/5 border border-white/6 hover:border-white/12 text-left space-y-1.5 transition-all group disabled:opacity-50"
        >
          <div className="flex items-center justify-between">
            {benchmarking ? (
              <Loader2 className="w-5 h-5 text-cyan-400 animate-spin" />
            ) : (
              <Zap className="w-5 h-5 text-cyan-400 group-hover:scale-110 transition-transform" />
            )}
            <span className="text-[10px] font-mono font-bold text-cyan-300">BENCHMARK</span>
          </div>
          <div className="text-sm font-bold text-white">
            {benchmarking ? 'Evaluating Games...' : 'Run Micro-Benchmark'}
          </div>
          <div className="text-[11px] text-slate-400">Execute 10-game headless test</div>
        </button>

        {/* Action 4: Presentation */}
        <button
          onClick={() => onNavigate('presentation')}
          className="p-3.5 rounded-xl bg-linear-to-br from-purple-600/20 to-purple-900/20 hover:from-purple-600/30 hover:to-purple-900/30 border border-purple-500/30 text-left space-y-1.5 transition-all group"
        >
          <div className="flex items-center justify-between">
            <Presentation className="w-5 h-5 text-purple-400 group-hover:scale-110 transition-transform" />
            <span className="text-[10px] font-mono font-bold text-purple-300">5-MIN</span>
          </div>
          <div className="text-sm font-bold text-white">Presentation Mode</div>
          <div className="text-[11px] text-slate-300">Guided story for reviewers & judges</div>
        </button>
      </div>

      {/* Benchmark Result Feedback */}
      {benchmarkResult && (
        <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-xs font-mono text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{benchmarkResult}</span>
        </div>
      )}
    </div>
  );
};
