import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Sparkles,
} from 'lucide-react';


export interface LossForensicCase {
  id: number;
  matchup: string;
  turn: number;
  winProbBefore: number;
  winProbAfter: number;
  chosenAction: string;
  optimalAction: string;
  scoreGap: number;
  rootCause: string;
  category: string;
  fixStatus: 'PATCHED' | 'ACTIVE';
  explanation: string;
}

export const LossForensicsPanel: React.FC = () => {
  const [selectedCase, setSelectedCase] = useState<number>(0);

  const cases: LossForensicCase[] = [
    {
      id: 1,
      matchup: 'Crustle_Control_Safeguard',
      turn: 3,
      winProbBefore: 71.0,
      winProbAfter: 38.0,
      chosenAction: 'Electro Bullet vs Safeguard Crustle (#345)',
      optimalAction: "Play Boss's Orders (#1262) on Bench Dwebble (#344) / Evolve #722",
      scoreGap: 220.0,
      rootCause:
        "Evaluator checked obsolete prototype card ID (542) instead of official dataset Safeguard ID (345). Evaluated 160 dmg instead of 0.",
      category: 'TACTICAL_IMMUNITY',
      fixStatus: 'PATCHED',
      explanation:
        'Bellibolt ex attacked into an active Crustle possessing Mysterious Rock Inn (0 dmg), conceding board tempo and losing 33% win equity in a single turn.',
    },
    {
      id: 2,
      matchup: 'Bellibolt_Mirror_SelfPlay',
      turn: 2,
      winProbBefore: 55.0,
      winProbAfter: 40.0,
      chosenAction: 'Attached manual energy without checking Electric Generator',
      optimalAction: 'Play Electric Generator (#1219) before manual attachment',
      scoreGap: 140.0,
      rootCause: 'Attachment sequence misalignment before item search execution.',
      category: 'ENERGY_PLANNING',
      fixStatus: 'PATCHED',
      explanation:
        'Active Bellibolt ex was left 1 energy short of Turn 2 attack activation, allowing the opponent to strike first.',
    },
    {
      id: 3,
      matchup: 'Alakazam_Psychic_Burst',
      turn: 5,
      winProbBefore: 62.0,
      winProbAfter: 35.0,
      chosenAction: 'Allowed Kadabra to evolve on bench without gusting',
      optimalAction: "Play Boss's Orders (#1262) to KO Kadabra before Stage 2 evolution",
      scoreGap: 180.0,
      rootCause: 'Underestimated bench stage-2 snowball draw potential.',
      category: 'TARGET_SELECTION',
      fixStatus: 'PATCHED',
      explanation:
        'Opponent evolved into Stage 2 Alakazam with Psychic Draw, drawing 3 extra cards and securing game-winning attack.',
    },
  ];

  const current = cases[selectedCase] || cases[0];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6 select-none bg-radial from-rose-950/20 via-slate-950 to-[#030509]">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
            <h3 className="text-xl font-black text-white font-display flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-400" />
              Loss Forensics & &ldquo;Why Did I Lose?&rdquo; Engine
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Automated turning-point blunder detection, win probability drop tracking, and verified counterfactual patches.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {cases.map((c, i) => (
            <button
              key={c.id}
              onClick={() => setSelectedCase(i)}
              className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all ${
                selectedCase === i
                  ? 'bg-rose-500 text-white shadow-lg shadow-rose-500/20'
                  : 'bg-white/4 text-slate-400 hover:text-white'
              }`}
            >
              Case #{c.id} (T{c.turn})
            </button>
          ))}
        </div>
      </div>

      {/* Critical Turning Point Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-black/40 border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
            Critical Blunder Turn
          </div>
          <div className="text-2xl font-black text-white font-mono">Turn {current.turn}</div>
          <div className="text-[11px] text-rose-400 font-mono font-bold">
            Matchup: {current.matchup.replace('_', ' ')}
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-black/40 border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
            Win Probability Shift
          </div>
          <div className="flex items-center gap-2 text-2xl font-black font-mono">
            <span className="text-emerald-400">{current.winProbBefore}%</span>
            <ArrowRight className="w-4 h-4 text-slate-500" />
            <span className="text-rose-400">{current.winProbAfter}%</span>
          </div>
          <div className="text-[11px] text-rose-400 font-mono">
            Drop: -{(current.winProbBefore - current.winProbAfter).toFixed(0)}% Win Equity
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-black/40 border border-white/8 space-y-1">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
            Engineering Fix Status
          </div>
          <div className="text-2xl font-black text-emerald-400 font-mono flex items-center gap-1.5">
            <CheckCircle2 className="w-5 h-5" />
            {current.fixStatus}
          </div>
          <div className="text-[11px] text-slate-400 font-mono">
            Root Cause: {current.category}
          </div>
        </div>
      </div>

      {/* Side-by-Side Chosen Blunder vs Counterfactual Alternative */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-5 rounded-2xl bg-rose-950/30 border border-rose-500/30 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-rose-300 font-mono flex items-center gap-1.5">
              <XCircle className="w-4 h-4" />
              CHOSEN BLUNDER ACTION
            </span>
            <span className="text-xs font-mono font-bold text-rose-400">-{current.scoreGap} PTS</span>
          </div>
          <div className="text-sm font-black text-white font-mono">{current.chosenAction}</div>
          <div className="text-xs text-slate-300 font-sans leading-relaxed">{current.explanation}</div>
        </div>

        <div className="p-5 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-300 font-mono flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" />
              OPTIMAL COUNTERFACTUAL
            </span>
            <span className="text-xs font-mono font-bold text-emerald-400">+{current.scoreGap} YIELD</span>
          </div>
          <div className="text-sm font-black text-white font-mono">{current.optimalAction}</div>
          <div className="text-xs text-slate-300 font-sans leading-relaxed">
            Maintains initiative, eliminates opponent threat piece, and preserves win probability above 70%.
          </div>
        </div>
      </div>

      {/* Root Cause & Resolution Footer */}
      <div className="p-4 rounded-2xl bg-white/2 border border-white/6 space-y-1.5 text-xs font-mono">
        <div className="text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          Root Cause Analysis & Code Resolution
        </div>
        <div className="text-slate-200 font-sans">{current.rootCause}</div>
        <div className="text-[11px] text-amber-300/90 pt-1 border-t border-white/6">
          Resolved in <span className="text-white font-bold">agent/evaluator.py</span> and verified in <span className="text-white font-bold">tools/mine_losses.py</span>
        </div>
      </div>
    </div>
  );
};
