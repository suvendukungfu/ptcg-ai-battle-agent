import React, { useState, useEffect, useCallback } from 'react';
import { api } from '../../../services/api';
import { PokemonCardSlot } from './PokemonCardSlot';
import { PrizeBar } from './PrizeBar';
import { CombatLogFeed } from './CombatLogFeed';
import type { CombatEvent } from './CombatLogFeed';
import { ArenaControls } from './ArenaControls';
import { Swords, Sparkles, Trophy, ArrowRight } from 'lucide-react';


interface LiveArenaViewProps {
  onNavigateExplainer?: () => void;
}

export const LiveArenaView: React.FC<LiveArenaViewProps> = ({ onNavigateExplainer }) => {
  const [opponentType, setOpponentType] = useState<string>('heuristic_v1');
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [replayData, setReplayData] = useState<any | null>(null);

  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);

  const [combatEvents, setCombatEvents] = useState<CombatEvent[]>([]);

  // Execute simulation match
  const handleSimulate = useCallback(async () => {
    try {
      setIsSimulating(true);
      setIsPlaying(false);
      const res = await api.simulateBattle('production_v2', opponentType);
      setReplayData(res);
      setCurrentStepIndex(0);

      // Extract combat timeline events
      const events: CombatEvent[] = (res.timeline || []).map((t: any) => ({
        turn: t.turn || 1,
        player: t.active_player === 0 ? 'YOU' : 'OPPONENT',
        type: t.action_name?.toLowerCase().includes('bullet') ? 'attack' : t.action_name?.toLowerCase().includes('energy') ? 'energy' : 'trainer',
        message: t.action_name ? `Played ${t.action_name}` : `Turn ${t.turn} action executed`,
        damage: t.damage_dealt,
      }));
      setCombatEvents(events);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setIsSimulating(false);
    }
  }, [opponentType]);

  // Load default battle simulation on mount if empty
  useEffect(() => {
    if (!replayData) {
      handleSimulate();
    }
  }, [handleSimulate, replayData]);

  // Auto playback timer
  useEffect(() => {
    if (!isPlaying || !replayData?.timeline) return;

    const intervalMs = Math.max(100, 1000 / playbackSpeed);
    const timer = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev >= replayData.timeline.length - 1) {
          setIsPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isPlaying, playbackSpeed, replayData]);

  const timeline = replayData?.timeline || [];
  const currentStep = timeline[currentStepIndex] || {};

  // Extract observable board state at current step
  const yourActive = currentStep.your_active || { id: 723, hp: 350, maxHp: 350, energies: [3, 3] };
  const oppActive = currentStep.opp_active || { id: 721, hp: 150, maxHp: 150, energies: [3] };

  const yourBench = currentStep.your_bench || [{ id: 721, hp: 150, maxHp: 150, energies: [3] }];
  const oppBench = currentStep.opp_bench || [{ id: 722, hp: 180, maxHp: 180, energies: [] }];

  const yourPrizes = currentStep.your_prizes !== undefined ? currentStep.your_prizes : 6;
  const oppPrizes = currentStep.opp_prizes !== undefined ? currentStep.opp_prizes : 6;

  const yourHandCount = currentStep.your_hand_count || 5;
  const oppHandCount = currentStep.opp_hand_count || 5;

  const currentTurn = currentStep.turn || 1;
  const isMatchOver = currentStepIndex >= timeline.length - 1 && timeline.length > 0;
  const winner = replayData?.winner || 'Undecided';

  return (
    <div className="space-y-6 text-left pb-12">
      {/* 1. Arena Header & Match Status */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
              <Swords className="w-6 h-6 text-indigo-400" />
              Live Battle Arena
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 font-mono font-bold">
              3D Tactical Perspective
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time interactive battle mat rendering observable board states, combat actions, and damage calculation.
          </p>
        </div>

        {/* Match State Banner */}
        <div className="flex items-center gap-3">
          <div className="p-2 px-3 rounded-xl bg-slate-900/80 border border-white/10 text-xs font-mono">
            <span className="text-slate-400 mr-2">Turn:</span>
            <span className="text-white font-bold text-sm">Turn {currentTurn}</span>
          </div>

          {isMatchOver && (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-300 text-xs font-bold font-mono">
              <Trophy className="w-4 h-4" />
              <span>Winner: {winner === 'YOU' ? 'Agent (Victory)' : winner}</span>
            </div>
          )}
        </div>
      </div>

      {/* 2. Playback & Simulation Controls */}
      <ArenaControls
        isPlaying={isPlaying}
        onTogglePlay={() => setIsPlaying(!isPlaying)}
        onStepBack={() => setCurrentStepIndex((p) => Math.max(0, p - 1))}
        onStepForward={() => setCurrentStepIndex((p) => Math.min(timeline.length - 1, p + 1))}
        onReset={() => setCurrentStepIndex(0)}
        speed={playbackSpeed}
        onSpeedChange={setPlaybackSpeed}
        currentStep={currentStepIndex}
        totalSteps={timeline.length}
        onSeek={setCurrentStepIndex}
        opponent={opponentType}
        onOpponentChange={setOpponentType}
        onSimulateBattle={handleSimulate}
        isSimulating={isSimulating}
      />

      {/* 3. Main Battle Mat & Combat Log Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 8 Cols: Pokémon Battle Mat */}
        <div className="lg:col-span-8 glass-panel p-5 rounded-2xl border border-white/8 space-y-6 relative overflow-hidden bg-linear-to-b from-slate-950/90 via-indigo-950/20 to-slate-950/90 shadow-2xl">
          {/* Tactical Mat Grid Pattern */}
          <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />

          {/* ================= OPPONENT FIELD (TOP) ================= */}
          <div className="space-y-3 relative z-10">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500 shadow-xs shadow-rose-500" />
                <span className="text-xs font-bold text-rose-300 uppercase tracking-wider font-mono">
                  Opponent Field ({opponentType.toUpperCase()})
                </span>
                <span className="text-[10px] text-slate-400 font-mono">
                  [Hand: {oppHandCount} | Deck: {currentStep.opp_deck_count || 40}]
                </span>
              </div>
              <PrizeBar prizesRemaining={oppPrizes} isOpponent={true} label="Opponent Prizes" />
            </div>

            {/* Opponent Bench */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider -rotate-90 origin-center shrink-0">
                BENCH
              </span>
              {Array.from({ length: 5 }).map((_, i) => (
                <PokemonCardSlot
                  key={i}
                  card={oppBench[i]}
                  label={`Bench ${i + 1}`}
                  isOpponent={true}
                />
              ))}
            </div>

            {/* Opponent Active Spot */}
            <div className="flex justify-center pt-2">
              <PokemonCardSlot
                card={oppActive}
                label="Opponent Active Spot"
                isOpponent={true}
                isActiveSpot={true}
              />
            </div>
          </div>

          {/* ================= BATTLE CENTER DIVIDER ================= */}
          <div className="relative py-2 flex items-center justify-center">
            <div className="w-full h-px bg-linear-to-r from-transparent via-white/20 to-transparent" />
            <div className="absolute px-3 py-1 rounded-full bg-slate-900 border border-white/10 text-[10px] font-mono text-slate-300 uppercase tracking-widest flex items-center gap-1.5">
              <Sparkles className="w-3 h-3 text-indigo-400" />
              <span>Active Combat Zone</span>
            </div>
          </div>

          {/* ================= PLAYER FIELD (BOTTOM) ================= */}
          <div className="space-y-3 relative z-10">
            {/* Player Active Spot */}
            <div className="flex justify-center pb-2">
              <PokemonCardSlot
                card={yourActive}
                label="Your Active Spot"
                isOpponent={false}
                isActiveSpot={true}
              />
            </div>

            {/* Player Bench */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider -rotate-90 origin-center shrink-0">
                BENCH
              </span>
              {Array.from({ length: 5 }).map((_, i) => (
                <PokemonCardSlot
                  key={i}
                  card={yourBench[i]}
                  label={`Bench ${i + 1}`}
                  isOpponent={false}
                />
              ))}
            </div>

            <div className="flex items-center justify-between pt-1">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-xs shadow-indigo-500" />
                <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider font-mono">
                  Your Field (Bellibolt ex Engine)
                </span>
                <span className="text-[10px] text-slate-400 font-mono">
                  [Hand: {yourHandCount} | Deck: {currentStep.your_deck_count || 45}]
                </span>
              </div>
              <PrizeBar prizesRemaining={yourPrizes} isOpponent={false} label="Your Prizes" />
            </div>
          </div>
        </div>

        {/* Right 4 Cols: Live Action Feed & Quick Inspect */}
        <div className="lg:col-span-4 space-y-4">
          <CombatLogFeed events={combatEvents} currentTurn={currentTurn} />

          {/* Decision Inspection Callout */}
          <div className="glass-panel p-4 rounded-2xl border border-white/8 space-y-2.5 bg-indigo-950/30">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                Explain Current Turn
              </span>
              <span className="text-[10px] font-mono text-indigo-300">Turn {currentTurn}</span>
            </div>
            <p className="text-xs text-slate-400">
              Inspect the AI's 2-ply lookahead search tree and additive value decomposition for this turn.
            </p>
            {onNavigateExplainer && (
              <button
                onClick={onNavigateExplainer}
                className="w-full py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 transition-all shadow-md shadow-indigo-600/20"
              >
                <span>Trace Decision in Explainer</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
