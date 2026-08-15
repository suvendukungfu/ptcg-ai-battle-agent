import React from 'react';
import type { AgentStatus, ViewSuite } from '../../types';
import { RefreshCw } from 'lucide-react';

interface TopBarProps {
  status: AgentStatus | null;
  currentSuite?: ViewSuite;
  isLanding: boolean;
  onToggleLanding: () => void;
  onRefresh: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  status,
  currentSuite = 'overview',
  isLanding,
  onToggleLanding,
  onRefresh,
}) => {
  return (
    <header className="sticky top-0 z-50 h-14 w-full bg-[#07080B]/95 backdrop-blur-md border-b border-white/6 px-4 md:px-6 flex items-center justify-between select-none">
      {/* Brand Monogram */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleLanding}
          className="flex items-center gap-2 group focus:outline-none cursor-pointer text-left"
          title="Return to Landing Page"
        >
          <div className="w-7 h-7 rounded-xs bg-amber-400 flex items-center justify-center font-black text-black text-xs font-mono tracking-tighter">
            //N
          </div>
          <div>
            <div className="text-sm font-black text-white tracking-tight flex items-center gap-1.5 font-display leading-none">
              PTCG // NEXUS
            </div>
            <div className="text-[10px] text-slate-400 font-mono leading-tight mt-0.5">
              Autonomous Game Intelligence
            </div>
          </div>
        </button>
      </div>

      {/* Contextual Telemetry Line (Non-boxed, clean typography) */}
      <div className="hidden md:flex items-center gap-3 font-mono text-xs text-slate-400">
        {isLanding ? (
          <>
            <span className="text-slate-300">COMPETITION // THE POKÉMON COMPANY AI CHALLENGE</span>
            <span className="text-slate-600">•</span>
            <span className="text-amber-400 font-bold">PRODUCTION V3.0</span>
          </>
        ) : currentSuite === 'arena' ? (
          <>
            <span className="text-white font-bold">ARENA // ACTIVE BATTLE CLASH</span>
            <span className="text-slate-600">•</span>
            <span className="text-amber-400">TURN 03</span>
            <span className="text-slate-600">•</span>
            <span className="text-emerald-400">P95: 2.66ms</span>
            <span className="text-slate-600">•</span>
            <span className="text-slate-300">100% LEGAL</span>
          </>
        ) : currentSuite === 'decision' ? (
          <>
            <span className="text-white font-bold">DECISION LENS // 2-PLY LOOKAHEAD</span>
            <span className="text-slate-600">•</span>
            <span className="text-amber-400">P(RETALIATE) = 0.12</span>
            <span className="text-slate-600">•</span>
            <span className="text-emerald-400">OPTIMAL: ELECTRO BULLET</span>
          </>
        ) : (
          <>
            <span className="text-slate-300">AGENT // BELLIBOLT EX ENGINE</span>
            <span className="text-slate-600">•</span>
            <span className="text-amber-300 font-bold">ELO {status ? status.best_elo.toFixed(1) : '1684.5'}</span>
            <span className="text-slate-600">•</span>
            <span className="text-emerald-400 font-bold">{status ? `${status.win_rate_meta.toFixed(1)}%` : '68.2%'} WR</span>
            <span className="text-slate-600">•</span>
            <span className="text-slate-400">0.00% FALLBACK</span>
          </>
        )}
      </div>

      {/* Right Controls & Operational Status */}
      <div className="flex items-center gap-3 font-mono text-xs">
        <button
          onClick={onRefresh}
          className="p-1.5 rounded-xs text-slate-400 hover:text-white hover:bg-white/4 transition-colors cursor-pointer"
          title="Refresh Telemetry Data"
        >
          <RefreshCw className="w-3.5 h-3.5" />
        </button>

        <button
          onClick={onToggleLanding}
          className="px-3 py-1 rounded-xs bg-white/4 hover:bg-white/8 border border-white/8 text-slate-200 hover:text-white transition-colors cursor-pointer text-[11px] font-bold"
        >
          {isLanding ? 'ENTER ARENA' : 'LANDING'}
        </button>

        <div className="hidden sm:flex items-center gap-1.5 pl-2 border-l border-white/8">
          <span className="w-1.5 h-1.5 rounded-xs bg-emerald-400" />
          <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">
            ONLINE
          </span>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
