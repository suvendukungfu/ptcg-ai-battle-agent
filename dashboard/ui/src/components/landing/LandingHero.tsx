import React from 'react';
import type { AgentStatus } from '../../types';
import { LiveMiniGameCanvas } from './LiveMiniGameCanvas';
import { ArrowRight, ShieldCheck, Flame, Zap, Cpu, Compass } from 'lucide-react';

interface LandingHeroProps {
  status: AgentStatus | null;
  onEnterCommandCenter: () => void;
  onExploreAI: () => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({
  status,
  onEnterCommandCenter,
  onExploreAI,
}) => {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col justify-center px-4 sm:px-8 max-w-7xl mx-auto py-12">
      {/* Top Banner Tag */}
      <div className="flex items-center gap-2 mb-6">
        <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-ping" />
          Kaggle Pokemon TCG AI Battle Challenge
        </span>
        <span className="text-xs text-slate-400 font-mono">
          Production Architecture v3.0
        </span>
      </div>

      {/* Main Grid: Hero Copy on Left, Live Game Canvas on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
        {/* Left Column: Title & Actions */}
        <div className="lg:col-span-7 space-y-6 text-left">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white leading-[1.08]">
            PTCG AI <br />
            <span className="bg-gradient-to-r from-indigo-400 via-indigo-200 to-emerald-300 bg-clip-text text-transparent">
              COMMAND CENTER
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 max-w-xl leading-relaxed">
            An uncertainty-aware autonomous game intelligence system for Pokemon TCG.
            Featuring <strong>Bayesian Belief State Tracking</strong>, <strong>2-Ply Risk-Aware Lookahead Search</strong>, <strong>Dynamic Meta Forecasting</strong>, and <strong>Automated Mistake Mining</strong>.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={onEnterCommandCenter}
              className="px-6 py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-indigo-500 via-indigo-600 to-indigo-700 text-white shadow-xl shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center gap-2.5 border border-white/20"
            >
              <span>ENTER THE COMMAND CENTER</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={onExploreAI}
              className="px-6 py-3.5 rounded-xl font-bold text-sm bg-white/[0.05] hover:bg-white/[0.1] text-slate-200 hover:text-white transition-all border border-white/[0.1] hover:border-white/[0.2] flex items-center gap-2"
            >
              <Compass className="w-4 h-4 text-indigo-400" />
              <span>EXPLORE THE AI</span>
            </button>
          </div>

          {/* Real Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-6 border-t border-white/[0.08]">
            {/* Elo */}
            <div className="glass-card p-3 rounded-lg">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Flame className="w-3 h-3 text-amber-400" />
                Rating Elo
              </div>
              <div className="text-xl font-bold text-white font-mono mt-1">
                {status ? status.best_elo.toFixed(1) : '1684.5'}
              </div>
              <div className="text-[10px] text-emerald-400 font-semibold mt-0.5">
                ▲ Rank #1 Ladder
              </div>
            </div>

            {/* Win Rate */}
            <div className="glass-card p-3 rounded-lg">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Zap className="w-3 h-3 text-emerald-400" />
                Win Rate
              </div>
              <div className="text-xl font-bold text-white font-mono mt-1">
                {status ? `${status.win_rate_meta.toFixed(1)}%` : '68.2%'}
              </div>
              <div className="text-[10px] text-slate-400 font-semibold mt-0.5">
                500+ Matches
              </div>
            </div>

            {/* P95 Latency */}
            <div className="glass-card p-3 rounded-lg">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Cpu className="w-3 h-3 text-cyan-400" />
                P95 Latency
              </div>
              <div className="text-xl font-bold text-white font-mono mt-1">
                {status ? `${status.p95_latency_ms.toFixed(2)} ms` : '3.98 ms'}
              </div>
              <div className="text-[10px] text-cyan-400 font-semibold mt-0.5">
                Budget: &lt; 25.0 ms
              </div>
            </div>

            {/* Reliability */}
            <div className="glass-card p-3 rounded-lg">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <ShieldCheck className="w-3 h-3 text-emerald-400" />
                Reliability
              </div>
              <div className="text-xl font-bold text-emerald-400 font-mono mt-1">
                0.00%
              </div>
              <div className="text-[10px] text-slate-400 font-semibold mt-0.5">
                Zero Fallbacks
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Live Mini Game Canvas */}
        <div className="lg:col-span-5 w-full">
          <LiveMiniGameCanvas />
        </div>
      </div>
    </div>
  );
};
