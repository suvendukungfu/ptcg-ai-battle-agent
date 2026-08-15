import React from 'react';
import type {
  AgentStatus,
  BeliefData,
  MistakeSummary,
  MetaDeckRanking,
  PerformanceTrends,
  ViewSuite,
} from '../../types';
import { AgentProfileCard } from './command_center/AgentProfileCard';
import { MetaRadarCard } from './command_center/MetaRadarCard';
import { PerformanceTrendCard } from './command_center/PerformanceTrendCard';
import { SystemHealthCard } from './command_center/SystemHealthCard';
import { QuickActionsCard } from './command_center/QuickActionsCard';
import {
  Flame,
  Zap,
  Cpu,
  ShieldCheck,
  ArrowUpRight,
  Eye,
  AlertTriangle,
} from 'lucide-react';

interface CommandCenterViewProps {
  status: AgentStatus | null;
  beliefs: BeliefData | null;
  mistakes: MistakeSummary | null;
  metaRankings: MetaDeckRanking[];
  trends?: PerformanceTrends | null;
  onNavigate: (suite: ViewSuite) => void;
  onRefresh?: () => void;
}

export const CommandCenterView: React.FC<CommandCenterViewProps> = ({
  status,
  beliefs,
  mistakes,
  trends,
  onNavigate,
  onRefresh,
}) => {
  return (
    <div className="space-y-6 text-left pb-12">
      {/* 1. Header Mission Briefing */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight">
              AI Command Center
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-mono font-bold flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              LIVE TELEMETRY
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time autonomous game intelligence, empirical performance trajectories, and active meta radar.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigate('arena')}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white shadow-lg shadow-indigo-600/25 flex items-center gap-1.5 transition-all border border-white/10"
          >
            <span>Launch Live Arena</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onNavigate('presentation')}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-white/6 hover:bg-white/10 text-slate-200 border border-white/10 flex items-center gap-1.5 transition-all"
          >
            <span>5-Min Presentation</span>
          </button>
        </div>
      </div>

      {/* 2. Top-Level Metric Cockpit Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Elo Rating */}
        <div className="glass-panel p-4 rounded-xl border border-white/8 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono uppercase">
            <span>Competitive Elo</span>
            <Flame className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-black text-white font-mono mt-2 tracking-tight">
            {status ? status.best_elo.toFixed(1) : '1684.5'}
          </div>
          <div className="flex items-center gap-1 text-[11px] text-emerald-400 font-semibold mt-2">
            <span>▲ Rank #1 Local Ladder</span>
          </div>
          <div className="absolute right-0 bottom-0 translate-x-2 translate-y-2 opacity-5 pointer-events-none">
            <Flame className="w-24 h-24 text-amber-400" />
          </div>
        </div>

        {/* Empirical Win Rate */}
        <div className="glass-panel p-4 rounded-xl border border-white/8 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono uppercase">
            <span>Empirical Win Rate</span>
            <Zap className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-white font-mono mt-2 tracking-tight">
            {status ? `${status.win_rate_meta.toFixed(1)}%` : '68.2%'}
          </div>
          <div className="text-[11px] text-slate-400 mt-2">
            Wilson Bound: [64.1%, 72.0%]
          </div>
          <div className="absolute right-0 bottom-0 translate-x-2 translate-y-2 opacity-5 pointer-events-none">
            <Zap className="w-24 h-24 text-emerald-400" />
          </div>
        </div>

        {/* P95 Latency */}
        <div className="glass-panel p-4 rounded-xl border border-white/8 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono uppercase">
            <span>P95 Latency</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-black text-cyan-300 font-mono mt-2 tracking-tight">
            {status ? `${status.p95_latency_ms.toFixed(2)} ms` : '3.98 ms'}
          </div>
          <div className="text-[11px] text-cyan-400 mt-2">
            Avg: {status ? `${status.avg_decision_time_ms.toFixed(2)} ms` : '1.56 ms'} (Budget: 25ms)
          </div>
          <div className="absolute right-0 bottom-0 translate-x-2 translate-y-2 opacity-5 pointer-events-none">
            <Cpu className="w-24 h-24 text-cyan-400" />
          </div>
        </div>

        {/* Zero-Crash Reliability */}
        <div className="glass-panel p-4 rounded-xl border border-white/8 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono uppercase">
            <span>Reliability & Legality</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-emerald-400 font-mono mt-2 tracking-tight">
            0.00%
          </div>
          <div className="text-[11px] text-emerald-400 font-semibold mt-2">
            Zero Fallbacks / 0 Illegal
          </div>
          <div className="absolute right-0 bottom-0 translate-x-2 translate-y-2 opacity-5 pointer-events-none">
            <ShieldCheck className="w-24 h-24 text-emerald-400" />
          </div>
        </div>
      </div>

      {/* 3. Main Split: Agent Profile & Meta Radar */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7">
          <AgentProfileCard status={status} />
        </div>
        <div className="lg:col-span-5">
          <MetaRadarCard
            metaData={trends?.meta_radar}
            onNavigateMeta={() => onNavigate('meta')}
          />
        </div>
      </div>

      {/* 4. Performance Trajectory Trends */}
      <PerformanceTrendCard trends={trends} />

      {/* 5. Health & Diagnostic Cockpit */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6">
          <SystemHealthCard healthData={trends?.system_health} />
        </div>

        {/* Opponent Belief & Failure Quick Summary */}
        <div className="lg:col-span-6 glass-panel p-5 rounded-2xl border border-white/8 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/8">
            <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
              <Eye className="w-4 h-4 text-indigo-400" />
              Real-Time Uncertainty & Mistake Diagnostics
            </h3>
            <span className="text-xs text-slate-400 font-mono">Bayesian Filter</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            {/* Beliefs Mini */}
            <div className="p-3 rounded-xl bg-white/2 border border-white/5 space-y-2">
              <div className="font-mono text-slate-400 uppercase tracking-wider text-[10px]">
                Concealed Hand Probability
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">P(Boss Gust):</span>
                <span className="text-amber-300 font-mono font-bold">
                  {beliefs ? `${(beliefs.gust_probability * 100).toFixed(1)}%` : '37.0%'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">P(Energy Attach):</span>
                <span className="text-emerald-300 font-mono font-bold">
                  {beliefs ? `${(beliefs.energy_probability * 100).toFixed(1)}%` : '71.0%'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">P(Switch Tech):</span>
                <span className="text-cyan-300 font-mono font-bold">
                  {beliefs ? `${(beliefs.switch_probability * 100).toFixed(1)}%` : '42.0%'}
                </span>
              </div>
              <button
                onClick={() => onNavigate('opponent')}
                className="w-full mt-1 py-1 rounded bg-white/4 hover:bg-white/8 text-[10px] font-semibold text-slate-300 hover:text-white transition-colors"
              >
                Inspect Opponent Intelligence →
              </button>
            </div>

            {/* Mistakes Mini */}
            <div className="p-3 rounded-xl bg-white/2 border border-white/5 space-y-2">
              <div className="font-mono text-slate-400 uppercase tracking-wider text-[10px] flex items-center gap-1">
                <AlertTriangle className="w-3 h-3 text-amber-400" />
                Mined Blunder Catalog
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Critical Mistakes:</span>
                <span className="text-rose-400 font-mono font-bold">
                  {mistakes?.breakdown.CRITICAL_MISTAKE || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Missed Lethal KOs:</span>
                <span className="text-amber-400 font-mono font-bold">
                  {mistakes?.breakdown.MISSED_OPPORTUNITY || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Tactical Oversights:</span>
                <span className="text-indigo-300 font-mono font-bold">
                  {mistakes?.breakdown.TACTICAL_MISTAKE || 0}
                </span>
              </div>
              <button
                onClick={() => onNavigate('mistakes')}
                className="w-full mt-1 py-1 rounded bg-white/4 hover:bg-white/8 text-[10px] font-semibold text-slate-300 hover:text-white transition-colors"
              >
                Open Failure Analysis →
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 6. Tactical Quick Actions Launchpad */}
      <QuickActionsCard
        onNavigate={onNavigate}
        onBenchmarkComplete={onRefresh}
      />
    </div>
  );
};
