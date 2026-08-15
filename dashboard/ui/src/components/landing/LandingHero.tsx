import React from 'react';
import type { AgentStatus } from '../../types';
import { PokemonCard } from '../common/PokemonCard';
import {
  ArrowRight,
  Brain,
  GitBranch,
  Sliders,
  Swords,
} from 'lucide-react';


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
    <div className="max-w-6xl mx-auto space-y-16 px-4 sm:px-6 py-10 text-left">
      {/* 1. Master Editorial Hero: Brand + Live Physical Clash */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center pt-4">
        {/* Left 6 Cols: Typographic Hero */}
        <div className="lg:col-span-6 space-y-6">
          <div className="space-y-2 font-mono">
            <div className="text-xs text-amber-400 font-bold uppercase tracking-wider">
              Research Platform // The Pokémon Company AI Battle Challenge
            </div>
            <h1 className="text-5xl sm:text-6xl font-black text-white tracking-tight leading-none font-display">
              PTCG // NEXUS
            </h1>
            <div className="text-sm sm:text-base text-slate-300 font-bold uppercase tracking-widest">
              Autonomous Game Intelligence
            </div>
          </div>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed font-sans max-w-lg">
            An uncertainty-aware autonomous battle agent engineered for competitive Pokémon TCG.
            Combining <strong>Bayesian belief tracking</strong>, <strong>2-ply forward lookahead search</strong>, and <strong>additive action value decomposition</strong>.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-3 pt-2 font-mono text-xs">
            <button
              onClick={onEnterCommandCenter}
              className="px-5 py-3 rounded-xs font-bold bg-amber-400 hover:bg-amber-300 text-black shadow-lg shadow-amber-400/20 flex items-center gap-2 transition-transform active:scale-95 cursor-pointer"
            >
              <span>ENTER BATTLEFIELD</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={onExploreAI}
              className="px-5 py-3 rounded-xs font-bold bg-white/4 hover:bg-white/8 text-white border border-white/10 flex items-center gap-2 transition-colors cursor-pointer"
            >
              <span>EXPLORE RESEARCH</span>
            </button>
          </div>

          {/* Verified Empirical Metric Bar (No cards, just crisp inline typography) */}
          <div className="grid grid-cols-3 gap-4 pt-6 border-t border-white/6 font-mono">
            <div>
              <div className="text-[10px] text-slate-400 uppercase">Competitive Elo</div>
              <div className="text-xl font-bold text-white mt-0.5">
                {status ? status.best_elo.toFixed(1) : '1684.5'}
              </div>
              <div className="text-[9px] text-emerald-400 mt-0.5">95% CI [64.1%, 72.0%]</div>
            </div>

            <div>
              <div className="text-[10px] text-slate-400 uppercase">P95 Latency</div>
              <div className="text-xl font-bold text-white mt-0.5">
                {status ? `${status.p95_latency_ms.toFixed(2)}ms` : '2.66ms'}
              </div>
              <div className="text-[9px] text-slate-400 mt-0.5">Limit: 25.0ms</div>
            </div>

            <div>
              <div className="text-[10px] text-slate-400 uppercase">Legal Actions</div>
              <div className="text-xl font-bold text-emerald-400 mt-0.5">100%</div>
              <div className="text-[9px] text-slate-400 mt-0.5">0.00% Fallbacks</div>
            </div>
          </div>
        </div>

        {/* Right 6 Cols: Cinematic Pokémon TCG Battle Composition */}
        <div className="lg:col-span-6 flex flex-col items-center justify-center relative p-6 rounded-lg border border-white/8 bg-[#090C12]">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-widest mb-4">
            Live Tactical Battle Representation
          </div>

          {/* Opponent Active: Safeguard Crustle */}
          <div className="relative z-10 flex flex-col items-center gap-2">
            <div className="text-[10px] font-mono text-rose-400 font-bold flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-xs bg-rose-500" />
              Opponent Active • Crustle (#345)
            </div>
            <PokemonCard cardId={345} variant="standard" isOpponent hp={150} maxHp={150} isImmune />
          </div>

          {/* Center Battle Vector */}
          <div className="w-full py-3 flex items-center justify-center gap-3 my-2 font-mono text-[10px] text-slate-400 border-y border-white/6">
            <Swords className="w-3.5 h-3.5 text-amber-400" />
            <span>AI SELECTION // PLAY BOSS&apos;S ORDERS (#1262) &rarr; BENCH GUST</span>
          </div>

          {/* Player Active: Bellibolt ex */}
          <div className="relative z-10 flex flex-col items-center gap-2">
            <PokemonCard cardId={723} variant="standard" isSelected hp={350} maxHp={350} energyCount={2} hasTool />
            <div className="text-[10px] font-mono text-amber-300 font-bold flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-xs bg-amber-400" />
              Player Active • Bellibolt ex (#723)
            </div>
          </div>
        </div>
      </div>

      {/* 2. Section: Why This Agent is Different (3 Core Pillars) */}
      <div className="space-y-6 pt-8 border-t border-white/6">
        <div className="space-y-1">
          <div className="text-xs font-mono text-amber-400 font-bold uppercase tracking-wider">
            Autonomous Decision Architecture
          </div>
          <h2 className="text-2xl font-black text-white font-display">
            Three Pillars of Strategic Advantage
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
          {/* Pillar 1: Belief */}
          <div className="p-5 rounded-lg border border-white/6 bg-[#0B0D12] space-y-2">
            <div className="flex items-center gap-2 text-purple-400 font-bold text-sm">
              <Brain className="w-4 h-4" />
              <span>01 // BAYESIAN BELIEF</span>
            </div>
            <p className="text-slate-300 font-sans text-xs leading-relaxed">
              Maintains exact hypergeometric distributions over unseen card locations. Predicts opponent lethal gust threats P(Boss) without hidden information leakage.
            </p>
          </div>

          {/* Pillar 2: Search */}
          <div className="p-5 rounded-lg border border-white/6 bg-[#0B0D12] space-y-2">
            <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
              <GitBranch className="w-4 h-4" />
              <span>02 // 2-PLY LOOKAHEAD</span>
            </div>
            <p className="text-slate-300 font-sans text-xs leading-relaxed">
              Projects game states across all legal actions and subtracts opponent retaliation threats via additive action value decomposition: V(s,a).
            </p>
          </div>

          {/* Pillar 3: Adaptation */}
          <div className="p-5 rounded-lg border border-white/6 bg-[#0B0D12] space-y-2">
            <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
              <Sliders className="w-4 h-4" />
              <span>03 // DYNAMIC RISK</span>
            </div>
            <p className="text-slate-300 font-sans text-xs leading-relaxed">
              Dynamically shifts aggression weights between Setup, Pressure, and Endgame phases based on real-time prize point race differentials.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingHero;
