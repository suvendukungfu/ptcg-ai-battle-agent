import React, { useState } from 'react';
import { DecisionTraceNodeGraph } from './DecisionTraceNodeGraph';
import {
  GitBranch,
  CheckCircle2,
  Shield,
  Zap,
  Swords,
  TrendingUp,
  Sparkles,
  BarChart3,
  Target,
  Brain,
  Layers,
} from 'lucide-react';


interface CandidateAction {
  id: number;
  name: string;
  type: string;
  immediateBonus: number;
  boardVal: number;
  retaliationThreat: number;
  netScore: number;
  isChosen: boolean;
  decomposition: {
    winBonus: number;
    prizeBonus: number;
    boardVal: number;
    energyVal: number;
    retaliationPenalty: number;
  };
  explanation: string;
}

export const DecisionExplainerView: React.FC = () => {
  const [selectedCandidate, setSelectedCandidate] = useState<number>(0);
  const [activeTab, setActiveTab] = useState<'pipeline' | 'tree'>('pipeline');

  const candidates: CandidateAction[] = [
    {
      id: 0,
      name: 'Electro Bullet (Attack Opponent Active)',
      type: 'Attack',
      immediateBonus: 220.0,
      boardVal: 480.0,
      retaliationThreat: 45.0,
      netScore: 655.0,
      isChosen: true,
      decomposition: {
        winBonus: 0.0,
        prizeBonus: 220.0,
        boardVal: 310.0,
        energyVal: 60.0,
        retaliationPenalty: -45.0,
      },
      explanation:
        'Selected optimal line. Knocks out opponent Active Tadbulb, claims 1 prize card, and establishes 2-prize lead with negligible retaliation threat.',
    },
    {
      id: 1,
      name: 'Electric Generator (Play Item)',
      type: 'Item',
      immediateBonus: 110.0,
      boardVal: 420.0,
      retaliationThreat: 90.0,
      netScore: 440.0,
      isChosen: false,
      decomposition: {
        winBonus: 0.0,
        prizeBonus: 0.0,
        boardVal: 310.0,
        energyVal: 110.0,
        retaliationPenalty: -90.0,
      },
      explanation:
        'Counterfactual alternative. Accelerates energy onto bench, but misses immediate lethal attack opportunity this turn.',
    },
    {
      id: 2,
      name: 'Attach Basic Lightning Energy to Active',
      type: 'Energy Attachment',
      immediateBonus: 60.0,
      boardVal: 370.0,
      retaliationThreat: 90.0,
      netScore: 340.0,
      isChosen: false,
      decomposition: {
        winBonus: 0.0,
        prizeBonus: 0.0,
        boardVal: 310.0,
        energyVal: 60.0,
        retaliationPenalty: -90.0,
      },
      explanation:
        'Counterfactual alternative. Attaches manual energy, but Active Bellibolt ex already has 2 required energies for Electro Bullet.',
    },
    {
      id: 3,
      name: 'Pass Turn',
      type: 'Pass',
      immediateBonus: -50.0,
      boardVal: 310.0,
      retaliationThreat: 180.0,
      netScore: 80.0,
      isChosen: false,
      decomposition: {
        winBonus: 0.0,
        prizeBonus: 0.0,
        boardVal: 310.0,
        energyVal: 0.0,
        retaliationPenalty: -180.0,
      },
      explanation:
        'Severe blunder line. Concedes initiative, exposes active Pokémon to free opponent retaliation without claiming prizes.',
    },
  ];

  const current = candidates[selectedCandidate] || candidates[0];

  const pipelineStages = [
    {
      step: '01',
      title: 'STATE INGESTION',
      icon: <Layers className="w-4 h-4 text-indigo-400" />,
      desc: 'Parses raw board state, public Pokémon slots, HP, and private hand into normalized GameState.',
      status: 'PARSED IN 0.22ms',
    },
    {
      step: '02',
      title: 'GOAL PLANNING',
      icon: <Target className="w-4 h-4 text-emerald-400" />,
      desc: 'Evaluates macro phase (Setup -> Pressure -> Endgame). Goal: Eliminate opponent active for 1-prize lead.',
      status: 'PRESSURE PHASE',
    },
    {
      step: '03',
      title: 'CANDIDATES',
      icon: <Swords className="w-4 h-4 text-amber-400" />,
      desc: 'Generates all 100% legal moves (attacks, items, attachments, pass) and filters out illegal branches.',
      status: '4 CANDIDATES',
    },
    {
      step: '04',
      title: 'BAYESIAN RISK',
      icon: <Brain className="w-4 h-4 text-purple-400" />,
      desc: 'Computes hypergeometric probability of opponent lethal retaliation P(Retaliate) = 0.12.',
      status: 'LOW RISK (0.12)',
    },
    {
      step: '05',
      title: '2-PLY SEARCH',
      icon: <GitBranch className="w-4 h-4 text-cyan-400" />,
      desc: 'Forward projects board states and subtracts expected opponent counterplay values.',
      status: 'SEARCH DEPTH: 2',
    },
    {
      step: '06',
      title: 'OPTIMAL DECISION',
      icon: <CheckCircle2 className="w-4 h-4 text-amber-300" />,
      desc: 'Selects action index [0]: Electro Bullet (+655.0 Net Score). Zero fallback rate.',
      status: 'ELECTRO BULLET',
    },
  ];

  return (
    <div className="space-y-6 text-left pb-12">
      {/* 1. Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2 font-display">
              <GitBranch className="w-6 h-6 text-amber-400" />
              Decision Explainer & Explainable AI (XAI)
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/30 font-mono font-bold">
              2-PLY SEARCH SPACE
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Exhaustive 2-ply forward search lookahead tree, additive value decomposition, and counterfactual decision simulation.
          </p>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex items-center gap-1 bg-white/4 p-1 rounded-xl text-xs font-mono">
          <button
            onClick={() => setActiveTab('pipeline')}
            className={`px-3 py-1 rounded-lg font-bold transition-all ${
              activeTab === 'pipeline'
                ? 'bg-amber-400 text-black'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            PIPELINE TRACE
          </button>
          <button
            onClick={() => setActiveTab('tree')}
            className={`px-3 py-1 rounded-lg font-bold transition-all ${
              activeTab === 'tree'
                ? 'bg-amber-400 text-black'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            LOOKAHEAD TREE
          </button>
        </div>
      </div>

      {/* 2. Signature 6-Stage AI Decision Pipeline Trace */}
      {activeTab === 'pipeline' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/8 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/6">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              Signature Decision Flow
            </span>
            <span className="text-xs font-mono text-amber-300 font-bold">
              STATE → GOAL → CANDIDATES → RISK → SEARCH → DECISION
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3 pt-1">
            {pipelineStages.map((st) => (
              <div
                key={st.step}
                className="p-3.5 rounded-2xl bg-white/2 border border-white/6 space-y-2 flex flex-col justify-between"
              >
                <div className="space-y-1">
                  <div className="flex justify-between items-center text-[10px] font-mono text-slate-500">
                    <span>STAGE {st.step}</span>
                    {st.icon}
                  </div>
                  <div className="text-xs font-black text-white font-mono">{st.title}</div>
                  <div className="text-[11px] text-slate-400 font-sans leading-tight">
                    {st.desc}
                  </div>
                </div>
                <div className="pt-2 border-t border-white/6 text-[10px] font-mono font-bold text-amber-300 truncate">
                  {st.status}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. 2-Ply Lookahead Search Tree Node Graph */}
      {activeTab === 'tree' && <DecisionTraceNodeGraph />}

      {/* 4. Candidate Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {candidates.map((c, idx) => {
          const isSelected = idx === selectedCandidate;
          return (
            <div
              key={c.id}
              onClick={() => setSelectedCandidate(idx)}
              className={`p-4 rounded-2xl border cursor-pointer transition-all duration-300 relative select-none ${
                isSelected
                  ? 'bg-amber-950/30 border-amber-400 shadow-xl shadow-amber-400/10 ring-1 ring-amber-400/30'
                  : 'bg-white/2 border-white/8 hover:bg-white/4 hover:border-white/12'
              }`}
            >
              {c.isChosen && (
                <span className="absolute top-2.5 right-2.5 px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[9px] font-mono font-bold border border-emerald-500/40 flex items-center gap-1">
                  <CheckCircle2 className="w-2.5 h-2.5" />
                  CHOSEN
                </span>
              )}

              <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1">
                Candidate {idx + 1} • {c.type}
              </div>
              <div className="text-xs font-bold text-white truncate mb-2" title={c.name}>
                {c.name}
              </div>

              <div className="flex items-baseline justify-between pt-2 border-t border-white/6 font-mono">
                <span className="text-[10px] text-slate-400">Net Score:</span>
                <span
                  className={`text-sm font-black ${
                    c.netScore > 500 ? 'text-emerald-400' : c.netScore > 200 ? 'text-amber-300' : 'text-rose-400'
                  }`}
                >
                  +{c.netScore.toFixed(1)}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* 5. Deep Additive Decomposition & Counterfactual Sandbox */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 7 Cols: Additive Score Decomposition Chart */}
        <div className="lg:col-span-7 glass-panel p-5 rounded-2xl border border-white/8 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/8">
            <span className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
              <BarChart3 className="w-4 h-4 text-amber-400" />
              Additive Value Decomposition Breakdown
            </span>
            <span className="text-xs font-mono text-amber-300 font-bold">
              Score: +{current.netScore.toFixed(1)}
            </span>
          </div>

          {/* Component Bar Gauges */}
          <div className="space-y-3 pt-1">
            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-300 flex items-center gap-1.5">
                  <Swords className="w-3.5 h-3.5 text-emerald-400" />
                  Prize Gain / Lethal Yield (W_prize)
                </span>
                <span className="text-emerald-400 font-bold">+{current.decomposition.prizeBonus.toFixed(1)}</span>
              </div>
              <div className="w-full h-2 rounded-full bg-white/6 overflow-hidden">
                <div
                  style={{ width: `${Math.min(100, (current.decomposition.prizeBonus / 300) * 100)}%` }}
                  className="h-full bg-emerald-400 rounded-full"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-300 flex items-center gap-1.5">
                  <TrendingUp className="w-3.5 h-3.5 text-indigo-400" />
                  Board Presence & HP Differential (W_board)
                </span>
                <span className="text-indigo-300 font-bold">+{current.decomposition.boardVal.toFixed(1)}</span>
              </div>
              <div className="w-full h-2 rounded-full bg-white/6 overflow-hidden">
                <div
                  style={{ width: `${Math.min(100, (current.decomposition.boardVal / 400) * 100)}%` }}
                  className="h-full bg-indigo-500 rounded-full"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-300 flex items-center gap-1.5">
                  <Zap className="w-3.5 h-3.5 text-amber-400" />
                  Energy Acceleration Reservoir (W_energy)
                </span>
                <span className="text-amber-300 font-bold">+{current.decomposition.energyVal.toFixed(1)}</span>
              </div>
              <div className="w-full h-2 rounded-full bg-white/6 overflow-hidden">
                <div
                  style={{ width: `${Math.min(100, (current.decomposition.energyVal / 150) * 100)}%` }}
                  className="h-full bg-amber-400 rounded-full"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono mb-1">
                <span className="text-slate-300 flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-rose-400" />
                  Opponent Retaliation Threat (-W_retaliation)
                </span>
                <span className="text-rose-400 font-bold">{current.decomposition.retaliationPenalty.toFixed(1)}</span>
              </div>
              <div className="w-full h-2 rounded-full bg-white/6 overflow-hidden">
                <div
                  style={{ width: `${Math.min(100, (Math.abs(current.decomposition.retaliationPenalty) / 200) * 100)}%` }}
                  className="h-full bg-rose-500 rounded-full"
                />
              </div>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-white/2 border border-white/6 text-xs text-slate-300 leading-relaxed mt-4">
            <span className="font-bold text-white">Mathematical Value Formulation: </span>
            <span className="font-mono text-[11px] text-amber-300">
              V(s, a) = V_board(s') + W_prize·ΔP - γ·E[OppCounter(s')] + W_energy·ΔE
            </span>
          </div>
        </div>

        {/* Right 5 Cols: Counterfactual Reasoning Engine */}
        <div className="lg:col-span-5 glass-panel p-5 rounded-2xl border border-white/8 space-y-4 flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-white/8">
              <span className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-amber-400" />
                Counterfactual Sandbox
              </span>
              <span
                className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                  current.isChosen
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                }`}
              >
                {current.isChosen ? 'OPTIMAL LINE' : 'SUB-OPTIMAL ALTERNATIVE'}
              </span>
            </div>

            <div className="text-xs text-slate-200 leading-relaxed font-sans">
              {current.explanation}
            </div>

            <div className="p-3 rounded-xl bg-black/40 border border-white/8 space-y-2 text-xs font-mono">
              <div className="text-amber-300 font-bold">2-Ply Lookahead Summary:</div>
              <div className="text-slate-300 text-[11px]">
                • Immediate Action Yield: <span className="text-emerald-400 font-bold">+{current.immediateBonus} pts</span>
              </div>
              <div className="text-slate-300 text-[11px]">
                • Expected Opponent Return: <span className="text-rose-400 font-bold">-{current.retaliationThreat} pts</span>
              </div>
              <div className="text-slate-300 text-[11px]">
                • Score Delta vs Chosen: <span className="text-white font-bold">{(candidates[0].netScore - current.netScore).toFixed(1)} pts</span>
              </div>
            </div>
          </div>

          <div className="text-[11px] text-slate-400 font-mono pt-3 border-t border-white/6">
            Computed offline via <span className="text-amber-300">research/counterfactual.py</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DecisionExplainerView;
