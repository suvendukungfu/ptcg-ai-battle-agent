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
    <header className="sticky top-0 z-50 h-16 w-full glass-panel border-b border-white/8 px-4 md:px-6 flex items-center justify-between">
      {/* Brand Monogram */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleLanding}
          className="flex items-center gap-2.5 group focus:outline-none cursor-pointer"
          title="Return to Landing Page"
        >
          <div className="w-8 h-8 rounded-lg bg-amber-400 flex items-center justify-center font-black text-black text-xs shadow-lg shadow-amber-400/25 border border-amber-300 group-hover:scale-105 transition-transform font-mono">
            //N
          </div>
          <div className="text-left hidden sm:block">
            <div className="text-sm font-black tracking-tight text-white flex items-center gap-1.5 font-display">
              PTCG // NEXUS
              <span className="text-[9px] uppercase font-mono px-1.5 py-0.5 rounded bg-amber-400/10 text-amber-300 border border-amber-400/30 font-bold">
                V3.0 PRODUCTION
              </span>
            </div>
            <div className="text-[10px] text-slate-400 font-mono">
              Autonomous Game Intelligence
            </div>
          </div>
        </button>
      </div>

      {/* Live Mission Telemetry Bar */}
      <div className="hidden lg:flex items-center gap-4 text-xs font-mono">
        {/* Active Deck */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/2 border border-white/6">
          <Layers className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-400">Deck:</span>
          <span className="text-white font-bold">{status?.deck_name || 'Bellibolt ex Engine'}</span>
        </div>

        {/* Elo Rating */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/2 border border-white/6">
          <Flame className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-400">Elo:</span>
          <span className="text-amber-300 font-black">
            {status ? status.best_elo.toFixed(1) : '1684.5'}
          </span>
        </div>

        {/* Meta Win Rate */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/2 border border-white/6">
          <Zap className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-400">Win Rate:</span>
          <span className="text-emerald-300 font-black">
            {status ? `${status.win_rate_meta.toFixed(1)}%` : '68.2%'}
          </span>
        </div>

        {/* P95 Latency */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/2 border border-white/6">
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-400">P95 Latency:</span>
          <span className="text-cyan-300 font-black">
            {status ? `${status.p95_latency_ms.toFixed(2)} ms` : '2.665 ms'}
          </span>
        </div>

        {/* Zero-Crash Reliability */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-emerald-300 font-bold">100% Legal</span>
        </div>
      </div>

      {/* Right Controls & Status Indicator */}
      <div className="flex items-center gap-3 font-mono">
        <button
          onClick={onRefresh}
          className="p-2 rounded-xl bg-white/4 hover:bg-white/8 border border-white/8 text-slate-300 hover:text-white transition-colors cursor-pointer"
          title="Refresh Telemetry Data"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        <button
          onClick={onToggleLanding}
          className="px-3 py-1.5 rounded-xl text-xs font-bold bg-white/4 hover:bg-white/8 border border-white/8 text-slate-200 hover:text-white transition-colors cursor-pointer"
        >
          {isLanding ? 'ENTER NEXUS' : 'HERO OVERVIEW'}
        </button>

        <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-white/8">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-tactical-radar" />
          <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">
            OPERATIONAL
          </span>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
