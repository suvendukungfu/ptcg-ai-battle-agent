import React from 'react';
import {
  CheckCircle2,
  Shield,
} from 'lucide-react';


export interface DecisionNode {
  id: string;
  name: string;
  type: 'root' | 'action' | 'opponent' | 'outcome';
  score: number;
  bonus: number;
  retaliation: number;
  isChosen: boolean;
  explanation: string;
  children?: DecisionNode[];
}

interface DecisionTraceNodeGraphProps {
  onSelectNode?: (nodeId: string) => void;
  selectedNodeId?: string;
}

export const DecisionTraceNodeGraph: React.FC<DecisionTraceNodeGraphProps> = ({
  onSelectNode,
  selectedNodeId = 'action-0',
}) => {
  const rootNode: DecisionNode = {
    id: 'root',
    name: 'Turn 3: Active State (Bellibolt ex vs Tadbulb)',
    type: 'root',
    score: 310.0,
    bonus: 0,
    retaliation: 0,
    isChosen: true,
    explanation: 'Player has active Bellibolt ex (350 HP, 2⚡) facing opponent basic Tadbulb (70 HP, 1⚡).',
    children: [
      {
        id: 'action-0',
        name: 'Action 1: Electro Bullet (Attack Active)',
        type: 'action',
        score: 655.0,
        bonus: 220.0,
        retaliation: 45.0,
        isChosen: true,
        explanation: 'Deals 160 DMG to Tadbulb (KO guaranteed, claims 1 Prize). Opponent promotes Dwebble.',
        children: [
          {
            id: 'opp-0',
            name: 'Opponent Return: Dwebble Bug Bite (30 DMG)',
            type: 'opponent',
            score: -45.0,
            bonus: 0,
            retaliation: 45.0,
            isChosen: true,
            explanation: 'Dwebble deals 30 damage to 350 HP Bellibolt ex (Bellibolt remains at 320 HP).',
            children: [
              {
                id: 'outcome-0',
                name: 'Leaf State: +1 Prize Lead (350 HP Active / Opponent in KO Range)',
                type: 'outcome',
                score: 655.0,
                bonus: 0,
                retaliation: 0,
                isChosen: true,
                explanation: 'Optimal game state reached. Win probability increases from 64% to 88%.',
              },
            ],
          },
        ],
      },
      {
        id: 'action-1',
        name: 'Action 2: Electric Generator (Play Item)',
        type: 'action',
        score: 440.0,
        bonus: 110.0,
        retaliation: 90.0,
        isChosen: false,
        explanation: 'Accelerates 2⚡ onto benched Bellibolt, but misses active KO this turn.',
        children: [
          {
            id: 'opp-1',
            name: 'Opponent Return: Tadbulb Evolves into Bellibolt & Attacks',
            type: 'opponent',
            score: -90.0,
            bonus: 0,
            retaliation: 90.0,
            isChosen: false,
            explanation: 'Unchecked Tadbulb evolves and strikes active Bellibolt ex for 70 damage.',
            children: [
              {
                id: 'outcome-1',
                name: 'Leaf State: Equal Prizes (Missed Tempo Window)',
                type: 'outcome',
                score: 440.0,
                bonus: 0,
                retaliation: 0,
                isChosen: false,
                explanation: 'Sub-optimal line. Concedes prize race initiative.',
              },
            ],
          },
        ],
      },
      {
        id: 'action-2',
        name: 'Action 3: Pass Turn',
        type: 'action',
        score: 80.0,
        bonus: -50.0,
        retaliation: 180.0,
        isChosen: false,
        explanation: 'Concedes turn with 0 actions taken.',
        children: [
          {
            id: 'opp-2',
            name: 'Opponent Return: Free Setup & Evolution Strike',
            type: 'opponent',
            score: -180.0,
            bonus: 0,
            retaliation: 180.0,
            isChosen: false,
            explanation: 'Opponent claims initiative and accelerates energy.',
            children: [
              {
                id: 'outcome-2',
                name: 'Leaf State: Severe Deficit (-180 pts)',
                type: 'outcome',
                score: 80.0,
                bonus: 0,
                retaliation: 0,
                isChosen: false,
                explanation: 'Blunder line.',
              },
            ],
          },
        ],
      },
    ],
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6 select-none bg-radial from-slate-900/40 via-slate-950 to-[#030509]">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-white/8">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-slate-400">
            Search Visualizer // 2-Ply Lookahead
          </span>
          <h3 className="text-lg font-black text-white font-display">
            Forward State Projection Node Graph
          </h3>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="flex items-center gap-1.5 text-amber-300 font-bold">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
            Selected Action Path
          </span>
          <span className="flex items-center gap-1.5 text-slate-400">
            <span className="w-2.5 h-2.5 rounded-full bg-white/20" />
            Pruned Branches
          </span>
        </div>
      </div>

      {/* Root Node: Current State */}
      <div className="flex justify-center">
        <div className="p-3.5 px-6 rounded-2xl bg-indigo-950/40 border border-indigo-500/40 shadow-xl text-center space-y-1 max-w-md">
          <div className="text-[10px] font-mono text-indigo-300 font-bold tracking-wider uppercase">
            ROOT STATE // S_0 (Turn 3)
          </div>
          <div className="text-xs font-black text-white">{rootNode.name}</div>
          <div className="text-[11px] font-mono text-emerald-400 font-bold">
            Current Board Valuation: +{rootNode.score.toFixed(1)} pts
          </div>
        </div>
      </div>

      {/* Connecting Stem Line */}
      <div className="w-px h-6 bg-linear-to-b from-indigo-500/50 to-amber-400/50 mx-auto" />

      {/* Candidate Action Branches */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
        {rootNode.children?.map((actionNode) => {
          const isSelected = selectedNodeId === actionNode.id || actionNode.isChosen;
          const oppNode = actionNode.children?.[0];
          const outcomeNode = oppNode?.children?.[0];

          return (
            <div
              key={actionNode.id}
              onClick={() => onSelectNode?.(actionNode.id)}
              className={`p-4 rounded-2xl border transition-all duration-300 space-y-4 cursor-pointer relative ${
                isSelected
                  ? 'bg-amber-950/20 border-amber-400/60 shadow-xl shadow-amber-400/10 ring-1 ring-amber-400/30'
                  : 'bg-white/2 border-white/6 hover:bg-white/4 hover:border-white/12'
              }`}
            >

              {actionNode.isChosen && (
                <div className="absolute -top-3 right-3 px-2 py-0.5 rounded-full bg-amber-400 text-black text-[9px] font-mono font-black border border-amber-300 shadow-md flex items-center gap-1">
                  <CheckCircle2 className="w-2.5 h-2.5" />
                  OPTIMAL LINE (100%)
                </div>
              )}

              {/* 1. Candidate Action Node */}
              <div className="space-y-1.5 pb-3 border-b border-white/6 font-mono">
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-slate-400 uppercase tracking-wider">Candidate Move</span>
                  <span className="text-emerald-400 font-bold">+{actionNode.bonus} Bonus</span>
                </div>
                <div className="text-xs font-bold text-white leading-snug">{actionNode.name}</div>
                <div className="text-[11px] text-slate-300 font-sans">{actionNode.explanation}</div>
              </div>

              {/* 2. Opponent Predicted Retaliation Node */}
              {oppNode && (
                <div className="space-y-1.5 p-2.5 rounded-xl bg-black/40 border border-white/6 font-mono">
                  <div className="flex justify-between items-center text-[10px]">
                    <span className="text-rose-400 font-bold flex items-center gap-1">
                      <Shield className="w-3 h-3" />
                      Opponent Counter
                    </span>
                    <span className="text-rose-400 font-bold">-{oppNode.retaliation} Threat</span>
                  </div>
                  <div className="text-[11px] text-white font-bold">{oppNode.name}</div>
                  <div className="text-[10px] text-slate-400 font-sans leading-tight">{oppNode.explanation}</div>
                </div>
              )}

              {/* 3. Estimated Leaf Outcome Node */}
              {outcomeNode && (
                <div
                  className={`p-2.5 rounded-xl border flex justify-between items-center font-mono text-xs ${
                    actionNode.isChosen
                      ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-300'
                      : 'bg-white/2 border-white/6 text-slate-400'
                  }`}
                >
                  <span className="font-bold">Projected Net Value:</span>
                  <span
                    className={`font-black text-sm ${
                      actionNode.score > 500
                        ? 'text-emerald-400'
                        : actionNode.score > 200
                        ? 'text-amber-300'
                        : 'text-rose-400'
                    }`}
                  >
                    +{actionNode.score.toFixed(1)}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
