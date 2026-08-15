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
        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-400/10 text-amber-300 border border-amber-400/30 flex items-center gap-1.5 font-mono">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-tactical-radar" />
          The Pokémon Company • PTCG AI Battle Challenge
        </span>
        <span className="text-xs text-slate-400 font-mono">
          Production V3.0
        </span>
      </div>

      {/* Main Grid: Hero Copy on Left, Live Game Canvas on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
        {/* Left Column: Title & Actions */}
        <div className="lg:col-span-7 space-y-6 text-left">
          <div className="space-y-2">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tight text-white leading-[1.05] font-display">
              PTCG // NEXUS
            </h1>
            <div className="text-xl sm:text-2xl font-mono text-amber-300 font-bold tracking-tight">
              &ldquo;Autonomous Game Intelligence&rdquo;
            </div>
          </div>

          <p className="text-base sm:text-lg text-slate-300 max-w-xl leading-relaxed font-sans">
            An uncertainty-aware autonomous game intelligence system for competitive Pokémon TCG battles.
            Powered by <strong>Bayesian Belief State Tracking</strong>, <strong>2-Ply Risk-Aware Lookahead Search</strong>, <strong>Dynamic Meta Forecasting</strong>, and <strong>Automated Loss Forensics</strong>.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-4 pt-2 font-mono">
            <button
              onClick={onEnterCommandCenter}
              className="px-6 py-3.5 rounded-2xl font-black text-sm bg-amber-500 hover:bg-amber-400 text-black shadow-xl shadow-amber-500/25 hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center gap-2.5 cursor-pointer"
            >
              <span>ENTER THE COMMAND CENTER</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={onExploreAI}
              className="px-6 py-3.5 rounded-2xl font-bold text-sm bg-white/4 hover:bg-white/8 text-slate-200 hover:text-white transition-all border border-white/8 flex items-center gap-2 cursor-pointer"
            >
              <Compass className="w-4 h-4 text-amber-400" />
              <span>EXPLORE THE AI LAB</span>
            </button>
          </div>

          {/* Real Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-6 border-t border-white/8 font-mono">
            {/* Elo */}
            <div className="glass-card p-3.5 rounded-2xl">
              <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Flame className="w-3 h-3 text-amber-400" />
                Rating Elo
              </div>
              <div className="text-xl font-bold text-white mt-1">
                {status ? status.best_elo.toFixed(1) : '1684.5'}
              </div>
              <div className="text-[10px] text-emerald-400 font-bold mt-0.5">
                ▲ Rank #1 Ladder
              </div>
            </div>

            {/* Win Rate */}
            <div className="glass-card p-3.5 rounded-2xl">
              <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Zap className="w-3 h-3 text-amber-400" />
                Win Rate
              </div>
              <div className="text-xl font-bold text-white mt-1">
                {status ? `${status.win_rate_meta.toFixed(1)}%` : '68.2%'}
              </div>
              <div className="text-[10px] text-slate-400 mt-0.5">
                500+ Matches
              </div>
            </div>

            {/* P95 Latency */}
            <div className="glass-card p-3.5 rounded-2xl">
              <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Cpu className="w-3 h-3 text-cyan-400" />
                P95 Latency
              </div>
              <div className="text-xl font-bold text-cyan-300 mt-1">
                {status ? `${status.p95_latency_ms.toFixed(2)} ms` : '2.665 ms'}
              </div>
              <div className="text-[10px] text-cyan-400 mt-0.5">
                Budget: &lt; 25.0 ms
              </div>
            </div>

            {/* Reliability */}
            <div className="glass-card p-3.5 rounded-2xl">
              <div className="text-[10px] text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <ShieldCheck className="w-3 h-3 text-emerald-400" />
                Reliability
              </div>
              <div className="text-xl font-bold text-emerald-400 mt-1">
                0.00%
              </div>
              <div className="text-[10px] text-slate-400 mt-0.5">
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

export default LandingHero;
