import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ShieldAlert,
  Sparkles,
} from 'lucide-react';


interface BlunderItem {
  id: number;
  matchup: string;
  turn: number;
  category: string;
  severity: string;
  chosen_action: string;
  optimal_action: string;
  score_gap: number;
  explanation: string;
  fix_status: 'RESOLVED' | 'PENDING';
}

export const MistakeLabView: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedBlunder, setSelectedBlunder] = useState<number>(0);

  const blunders: BlunderItem[] = [
    {
      id: 1,
      matchup: 'Crustle_Control_Safeguard',
      turn: 3,
      category: 'TACTICAL',
      severity: 'CRITICAL',
      chosen_action: 'Electro Bullet vs Safeguard Crustle (#345)',
      optimal_action: "Play Boss's Orders (#1262) on Bench Dwebble (#344)",
      score_gap: 220.0,
      explanation:
        "Bellibolt ex attacked into an active Crustle with 'Mysterious Rock Inn' ability, dealing 0 damage and wasting the entire attack turn.",
      fix_status: 'RESOLVED',
    },
    {
      id: 2,
      matchup: 'Crustle_Control_Safeguard',
      turn: 1,
      category: 'PRIZE_RACE',
      severity: 'HIGH',
      chosen_action: 'Selected item search while opponent active was in KO range',
      optimal_action: 'Execute lethal knockout attack for immediate prize lead',
      score_gap: 300.0,
      explanation:
        'Missed match point window. Prioritized secondary search over claiming the final prize card.',
      fix_status: 'RESOLVED',
    },
    {
      id: 3,
      matchup: 'Bellibolt_Mirror_SelfPlay',
      turn: 2,
      category: 'ENERGY_PLANNING',
      severity: 'MEDIUM',
      chosen_action: 'Attached manual energy to benched Tadbulb without checking Generator',
      optimal_action: 'Play Electric Generator (#1219) before manual attachment',
      score_gap: 140.0,
      explanation:
        'Sub-optimal attachment order left active Bellibolt ex with 1 energy instead of 2 required for Turn 2 Electro Bullet.',
      fix_status: 'RESOLVED',
    },
    {
      id: 4,
      matchup: 'Bellibolt_Mirror_SelfPlay',
      turn: 4,
      category: 'RESOURCE_MANAGEMENT',
      severity: 'MEDIUM',
      chosen_action: "Played Professor's Research with Switch and Ultra Ball in hand",
      optimal_action: 'Play Switch / Ultra Ball before discarding hand',
      score_gap: 75.0,
      explanation:
        'Premature discard burned 2 key utility cards without gaining board value.',
      fix_status: 'RESOLVED',
    },
  ];

  const filteredBlunders = blunders.filter((b) => {
    if (selectedCategory === 'all') return true;
    return b.category.toLowerCase() === selectedCategory.toLowerCase();
  });

  const current = blunders[selectedBlunder] || blunders[0];

  return (
    <div className="space-y-6 text-left pb-12">
      {/* 1. Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
              <AlertTriangle className="w-6 h-6 text-amber-400" />
              Mistake Lab & Failure Forensic Mining
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 font-mono font-bold">
              Automated Blunder Mining
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Forensic mining across 30+ loss replays, root cause classification, counterfactual delta scoring, and patch verification.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {['all', 'TACTICAL', 'PRIZE_RACE', 'ENERGY_PLANNING', 'RESOURCE_MANAGEMENT'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-xl text-xs font-mono font-bold capitalize transition-all ${
                selectedCategory === cat
                  ? 'bg-amber-600 text-white shadow-md shadow-amber-600/30'
                  : 'bg-white/4 text-slate-400 hover:text-white hover:bg-white/8'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* 2. Loss Breakdown KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-4 rounded-2xl border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Total Losses Mined</div>
          <div className="text-2xl font-black text-white font-mono">30 Matches</div>
          <div className="text-[11px] text-slate-400">195 Total Blunders Identified</div>
        </div>

        <div className="glass-panel p-4 rounded-2xl border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Tactical Immunity Share</div>
          <div className="text-2xl font-black text-rose-400 font-mono">79.5%</div>
          <div className="text-[11px] text-slate-400">Attacking Safeguard target</div>
        </div>

        <div className="glass-panel p-4 rounded-2xl border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Prize Race Blunders</div>
          <div className="text-2xl font-black text-amber-400 font-mono">20.5%</div>
          <div className="text-[11px] text-slate-400">Delayed knockout line</div>
        </div>

        <div className="glass-panel p-4 rounded-2xl border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Fix Verification</div>
          <div className="text-2xl font-black text-emerald-400 font-mono">100% Patched</div>
          <div className="text-[11px] text-emerald-300">Immunity ID updated (345/533)</div>
        </div>
      </div>

      {/* 3. Blunder Catalog & Deep Side-by-Side Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 5 Cols: Blunder List */}
        <div className="lg:col-span-5 glass-panel p-5 rounded-2xl border border-white/8 space-y-3">
          <div className="text-xs font-bold text-white uppercase tracking-wider font-mono pb-2 border-b border-white/8">
            Mined Blunder Incidents ({filteredBlunders.length})
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
            {filteredBlunders.map((b, idx) => {
              const isSelected = idx === selectedBlunder;
              return (
                <div
                  key={b.id}
                  onClick={() => setSelectedBlunder(idx)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-amber-950/40 border-amber-500 text-white shadow-lg'
                      : 'bg-white/2 border-white/6 text-slate-300 hover:bg-white/4'
                  }`}
                >
                  <div className="flex justify-between items-center text-[10px] font-mono mb-1">
                    <span className="text-amber-400 font-bold">
                      {b.matchup.replace('_', ' ')} • T{b.turn}
                    </span>
                    <span className="text-rose-400 font-bold">-{b.score_gap} pts</span>
                  </div>
                  <div className="text-xs font-bold text-white truncate">{b.chosen_action}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right 7 Cols: Detailed Comparison & Fix Inspector */}
        <div className="lg:col-span-7 glass-panel p-5 rounded-2xl border border-white/8 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/8">
            <span className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              Side-by-Side Blunder Comparison
            </span>
            <span className="text-xs font-mono font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30">
              STATUS: {current.fix_status}
            </span>
          </div>

          {/* Side by side cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-rose-300 font-mono">
                <XCircle className="w-4 h-4" />
                Chosen Blunder
              </div>
              <div className="text-xs font-bold text-white">{current.chosen_action}</div>
              <div className="text-[11px] text-rose-300/80 font-mono pt-1">
                Score Penalty: -{current.score_gap} pts
              </div>
            </div>

            <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/30 space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-300 font-mono">
                <CheckCircle2 className="w-4 h-4" />
                Optimal Counterfactual
              </div>
              <div className="text-xs font-bold text-white">{current.optimal_action}</div>
              <div className="text-[11px] text-emerald-300/80 font-mono pt-1">
                Yield Advantage: +{current.score_gap} pts
              </div>
            </div>
          </div>

          {/* Root Cause & Fix Explanation */}
          <div className="p-4 rounded-xl bg-white/2 border border-white/6 space-y-2">
            <div className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
              Root Cause & Engineering Resolution
            </div>
            <div className="text-xs text-slate-300 leading-relaxed font-sans">{current.explanation}</div>
            <div className="pt-2 border-t border-white/6 text-[11px] text-indigo-300 font-mono">
              Patched in <span className="text-white font-bold">agent/evaluator.py</span> and <span className="text-white font-bold">agent/policy.py</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
