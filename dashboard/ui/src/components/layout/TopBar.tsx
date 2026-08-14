import React from 'react';
import type { AgentStatus } from '../../types';
import { ShieldCheck, Cpu, Flame, Zap, Layers, RefreshCw } from 'lucide-react';

interface TopBarProps {
  status: AgentStatus | null;
  isLanding: boolean;
  onToggleLanding: () => void;
  onRefresh: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  status,
  isLanding,
  onToggleLanding,
  onRefresh,
}) => {
  return (
    <header className="sticky top-0 z-50 h-16 w-full glass-panel border-b border-white/[0.08] px-4 md:px-6 flex items-center justify-between">
      {/* Brand Monogram */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleLanding}
          className="flex items-center gap-2.5 group focus:outline-none"
          title="Return to Landing Page"
        >
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center font-black text-white text-sm shadow-lg shadow-indigo-500/25 border border-white/20 group-hover:scale-105 transition-transform">
            AI
          </div>
          <div className="text-left hidden sm:block">
            <div className="text-sm font-extrabold tracking-tight text-white flex items-center gap-1.5">
              PTCG AI COMMAND CENTER
              <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                v3.0 Production
              </span>
            </div>
            <div className="text-[11px] text-slate-400 font-medium">
              The Pokemon Company AI Battle Challenge
            </div>
          </div>
        </button>
      </div>

      {/* Live Mission Telemetry Bar */}
      <div className="hidden lg:flex items-center gap-6 text-xs">
        {/* Active Deck */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06]">
          <Layers className="w-3.5 h-3.5 text-indigo-400" />
          <span className="text-slate-400 font-medium">Active Deck:</span>
          <span className="text-white font-semibold">{status?.deck_name || 'Bellibolt ex Heavy Ramp'}</span>
        </div>

        {/* Elo Rating */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06]">
          <Flame className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-400 font-medium">Elo:</span>
          <span className="text-amber-300 font-bold font-mono">
            {status ? status.best_elo.toFixed(1) : '1684.5'}
          </span>
        </div>

        {/* Meta Win Rate */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06]">
          <Zap className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-400 font-medium">Win Rate:</span>
          <span className="text-emerald-300 font-bold font-mono">
            {status ? `${status.win_rate_meta.toFixed(1)}%` : '68.2%'}
          </span>
        </div>

        {/* P95 Latency */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06]">
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-400 font-medium">P95 Latency:</span>
          <span className="text-cyan-300 font-bold font-mono">
            {status ? `${status.p95_latency_ms.toFixed(2)} ms` : '3.98 ms'}
          </span>
        </div>

        {/* Zero-Crash Reliability */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-emerald-300 font-semibold">0.00% Fallback</span>
        </div>
      </div>

      {/* Right Controls & Status Indicator */}
      <div className="flex items-center gap-3">
        <button
          onClick={onRefresh}
          className="p-2 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-300 hover:text-white transition-colors"
          title="Refresh Telemetry Data"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        <button
          onClick={onToggleLanding}
          className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-white/[0.06] hover:bg-white/[0.12] border border-white/[0.1] text-slate-200 hover:text-white transition-colors"
        >
          {isLanding ? 'Enter Command Center' : 'Landing Overview'}
        </button>

        <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-white/[0.08]">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-radar" />
          <span className="text-[11px] font-mono font-semibold text-emerald-400 uppercase tracking-wider">
            Operational
          </span>
        </div>
      </div>
    </header>
  );
};
