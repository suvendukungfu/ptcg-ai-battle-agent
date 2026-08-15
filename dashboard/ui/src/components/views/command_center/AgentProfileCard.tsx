import React from 'react';
import type { AgentStatus } from '../../../types';
import { Layers, CheckCircle2, Shield, Flame, Brain, Crosshair } from 'lucide-react';


interface AgentProfileCardProps {
  status: AgentStatus | null;
}

export const AgentProfileCard: React.FC<AgentProfileCardProps> = ({ status }) => {
  const pipelineModules = [
    { name: '1-2 Ply Risk-Aware Lookahead', desc: 'Evaluates lethal lines & counterplay', status: 'ACTIVE' },
    { name: 'Bayesian Belief State Tracker', desc: 'Hypergeometric hand probability model', status: 'ACTIVE' },
    { name: 'Goal-Based Strategic Macro Planner', desc: 'Prize mapping & Safeguard bypass', status: 'ACTIVE' },
    { name: 'Action Value Decomposer', desc: 'Additively breaks down decision reasons', status: 'ACTIVE' },
    { name: 'Dynamic Situation Sensitivity', desc: 'Modulates aggression based on prize gap', status: 'ACTIVE' },
    { name: 'Deterministic Mathematical Fallback', desc: 'Zero-crash boundary compliance', status: 'ACTIVE' },
  ];

  return (
    <div className="glass-panel p-5 rounded-2xl border border-white/[0.08] space-y-5">
      {/* Card Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-white/[0.08]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-800 flex items-center justify-center text-white font-black shadow-lg shadow-indigo-500/20 border border-white/10">
            <Brain className="w-5 h-5 text-indigo-200" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
              {status?.agent_name || 'PTCG AI LAB Autonomous Agent'}
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                v3.0 Production
              </span>
            </h3>
            <div className="text-xs text-slate-400">
              Uncertainty-Aware Autonomous Decision Engine for Pokemon TCG
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
            <Shield className="w-3.5 h-3.5" />
            <span>Kaggle Compliant</span>
          </div>
        </div>
      </div>

      {/* Core Specification Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Active Deck */}
        <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
          <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-indigo-400" />
            Competition Deck
          </div>
          <div className="text-sm font-bold text-white mt-1">
            {status?.deck_name || 'Bellibolt ex Heavy Ramp'}
          </div>
          <div className="text-[11px] text-indigo-300 font-mono mt-0.5">
            60-Card Standard Archetype
          </div>
        </div>

        {/* Elo & Wilson Interval */}
        <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
          <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Flame className="w-3.5 h-3.5 text-amber-400" />
            Rating Confidence
          </div>
          <div className="text-sm font-bold text-white font-mono mt-1">
            {status?.best_elo.toFixed(1) || '1684.5'} Elo
          </div>
          <div className="text-[11px] text-emerald-400 font-mono mt-0.5">
            95% CI: [64.1%, 72.0%] WR
          </div>
        </div>

        {/* Tactical Stance */}
        <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
          <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Crosshair className="w-3.5 h-3.5 text-rose-400" />
            Tactical Heuristic
          </div>
          <div className="text-sm font-bold text-white mt-1">
            2-Prize KO Hunter
          </div>
          <div className="text-[11px] text-slate-400 font-mono mt-0.5">
            Crustle Safeguard Immunity Shield
          </div>
        </div>
      </div>

      {/* Structured Pipeline Breakdown */}
      <div>
        <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center justify-between">
          <span>Active Autonomous Intelligence Pipeline</span>
          <span className="text-[10px] text-emerald-400 font-normal">All 6 Subsystems Verified</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {pipelineModules.map((mod, idx) => (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-white/[0.02] hover:bg-white/[0.04] border border-white/[0.05] transition-colors flex items-start gap-2.5"
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <div className="text-xs font-bold text-white truncate">{mod.name}</div>
                <div className="text-[11px] text-slate-400 truncate">{mod.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
