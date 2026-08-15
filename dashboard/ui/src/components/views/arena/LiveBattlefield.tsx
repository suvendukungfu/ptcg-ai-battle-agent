import React, { useState, useEffect } from 'react';
import { PokemonCard } from '../../common/PokemonCard';
import { api } from '../../../services/api';
import {
  Swords,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  GitBranch,
} from 'lucide-react';


interface LiveBattlefieldProps {
  onNavigateExplainer?: () => void;
}

export const LiveBattlefield: React.FC<LiveBattlefieldProps> = ({ onNavigateExplainer }) => {
  const [simulationData, setSimulationData] = useState<any | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Load real battle simulation from backend
  const startNewSimulation = async (oppType: string = 'heuristic_v1') => {
    try {
      setIsLoading(true);
      const res = await api.simulateBattle('production_v2', oppType);
      setSimulationData(res);
      setCurrentStep(0);
      setIsPlaying(true);
    } catch (e) {
      console.error('Failed to run simulation:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    startNewSimulation();
  }, []);

  // Playback timer loop
  useEffect(() => {
    if (!isPlaying || !simulationData?.timeline) return;

    const intervalMs = Math.max(200, 1000 / playbackSpeed);
    const timer = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= simulationData.timeline.length - 1) {
          setIsPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isPlaying, simulationData, playbackSpeed]);

  const timeline = simulationData?.timeline || [];
  const step = timeline[currentStep] || {};

  // Extract board properties from timeline step or fallback defaults
  const yourActiveId = step.your_active?.id || 723;
  const yourActiveHp = step.your_active?.hp !== undefined ? step.your_active.hp : 350;
  const yourActiveMaxHp = step.your_active?.maxHp || 350;
  const yourActiveEnergy = step.your_active?.energies?.length !== undefined ? step.your_active.energies.length : 2;

  const oppActiveId = step.opp_active?.id || (step.turn > 2 ? 345 : 344);
  const oppActiveHp = step.opp_active?.hp !== undefined ? step.opp_active.hp : 70;
  const oppActiveMaxHp = step.opp_active?.maxHp || 150;
  const oppActiveEnergy = step.opp_active?.energies?.length !== undefined ? step.opp_active.energies.length : 1;

  const yourPrizesClaimed = step.your_prizes || Math.min(6, Math.floor(currentStep / 8));
  const oppPrizesClaimed = step.opp_prizes || Math.min(6, Math.floor(currentStep / 12));

  return (
    <div className="space-y-6 text-left pb-12 max-w-6xl mx-auto">
      {/* 1. Contextual Match HUD Bar (Non-boxed, open typographic header) */}
      <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-4 pb-3 border-b border-white/6">
        <div className="flex items-baseline gap-3 font-mono">
          <span className="text-xs text-amber-400 font-bold">MATCH // CABT-0824</span>
          <span className="text-slate-600">•</span>
          <span className="text-xs text-white font-bold">TURN {String(step.turn || 1).padStart(2, '0')}</span>
          <span className="text-slate-600">•</span>
          <span className="text-xs text-slate-400">STEP {currentStep + 1} OF {timeline.length || 64}</span>
          <span className="text-slate-600">•</span>
          <span className="text-xs text-emerald-400">P95 LATENCY: 2.66ms</span>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          {onNavigateExplainer && (
            <button
              onClick={onNavigateExplainer}
              className="px-3 py-1 rounded-xs bg-white/4 hover:bg-white/8 text-slate-300 hover:text-white border border-white/8 flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <GitBranch className="w-3.5 h-3.5 text-amber-400" />
              <span>TRACE DECISION</span>
            </button>
          )}

          <button
            onClick={() => startNewSimulation('heuristic_v1')}
            disabled={isLoading}
            className="px-3 py-1 rounded-xs bg-amber-400 hover:bg-amber-300 text-black font-bold flex items-center gap-1.5 transition-colors cursor-pointer disabled:opacity-50"
          >
            <RotateCcw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>NEW BATTLE</span>
          </button>
        </div>
      </div>

      {/* 2. Premium Digital Battlefield Arena */}
      <div className="relative rounded-lg border border-white/8 bg-[#090C12] overflow-hidden p-6 sm:p-8 space-y-6">
        {/* Subtle arena background pattern */}
        <div className="absolute inset-0 bg-radial from-amber-400/[0.02] via-transparent to-transparent pointer-events-none" />

        {/* ================= OPPONENT FIELD (TOP) ================= */}
        <div className="space-y-3 relative z-10">
          <div className="flex justify-between items-center text-xs font-mono">
            <div className="flex items-center gap-2 text-slate-300 font-bold">
              <span className="w-2 h-2 rounded-xs bg-rose-500" />
              <span>OPPONENT // HEURISTIC BASELINE V1</span>
              <span className="text-slate-500 font-normal">
                [Deck: {step.opp_deck_count || 42} • Hand: {step.opp_hand_count || 5}]
              </span>
            </div>

            {/* 6-Prize Slot Stack */}
            <div className="flex items-center gap-1">
              <span className="text-[10px] text-slate-500 mr-1">PRIZES:</span>
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`w-2.5 h-3.5 rounded-xs border transition-colors ${
                    i < oppPrizesClaimed
                      ? 'bg-rose-500 border-rose-400'
                      : 'bg-white/5 border-white/10'
                  }`}
                  title={i < oppPrizesClaimed ? 'Claimed Prize' : 'Remaining Prize'}
                />
              ))}
            </div>
          </div>

          {/* Opponent Bench & Active Spot */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-1">
            {/* Opponent Bench */}
            <div className="flex gap-2">
              <PokemonCard cardId={344} variant="bench" isOpponent hp={70} maxHp={70} />
              <PokemonCard cardId={344} variant="bench" isOpponent hp={70} maxHp={70} />
            </div>

            {/* Opponent Active Pokémon */}
            <PokemonCard
              cardId={oppActiveId}
              variant="battle"
              isOpponent
              hp={oppActiveHp}
              maxHp={oppActiveMaxHp}
              energyCount={oppActiveEnergy}
              isImmune={oppActiveId === 345}
            />
          </div>
        </div>

        {/* ================= CLASH ZONE & DECISION OVERLAY ================= */}
        <div className="relative py-2 flex flex-col md:flex-row items-center justify-between gap-4 border-y border-white/6 px-4 font-mono text-xs">
          <div className="flex items-center gap-3">
            <Swords className="w-4 h-4 text-amber-400" />
            <div>
              <span className="text-slate-500 text-[10px] uppercase">Executed Action: </span>
              <span className="text-white font-bold">
                {step.action_name || 'Electro Bullet (160 DMG)'}
              </span>
            </div>
          </div>

          {/* Value Breakdown Vector */}
          <div className="flex items-center gap-4 text-[11px]">
            <span className="text-slate-400">
              PRIZE <span className="text-emerald-400 font-bold">+220</span>
            </span>
            <span className="text-slate-400">
              BOARD <span className="text-slate-200 font-bold">+310</span>
            </span>
            <span className="text-slate-400">
              RISK <span className="text-rose-400 font-bold">-45</span>
            </span>
            <span className="text-amber-400 font-bold pl-2 border-l border-white/10">
              NET SCORE: +655
            </span>
          </div>
        </div>

        {/* ================= PLAYER FIELD (BOTTOM) ================= */}
        <div className="space-y-3 relative z-10">
          {/* Player Active & Bench */}
          <div className="flex flex-col-reverse sm:flex-row items-center justify-center gap-6 pb-1">
            {/* Player Active (Dominant) */}
            <PokemonCard
              cardId={yourActiveId}
              variant="battle"
              isSelected
              hp={yourActiveHp}
              maxHp={yourActiveMaxHp}
              energyCount={yourActiveEnergy}
              hasTool={true}
            />

            {/* Player Bench */}
            <div className="flex gap-2">
              <PokemonCard cardId={722} variant="bench" hp={140} maxHp={140} energyCount={1} />
              <PokemonCard cardId={721} variant="bench" hp={70} maxHp={70} energyCount={0} />
            </div>
          </div>

          <div className="flex justify-between items-center text-xs font-mono">
            <div className="flex items-center gap-2 text-slate-300 font-bold">
              <span className="w-2 h-2 rounded-xs bg-amber-400" />
              <span>PLAYER // PTCG AI NEXUS (V3.0)</span>
              <span className="text-slate-500 font-normal">
                [Deck: {step.your_deck_count || 45} • Hand: {step.your_hand_count || 5}]
              </span>
            </div>

            {/* 6-Prize Slot Stack */}
            <div className="flex items-center gap-1">
              <span className="text-[10px] text-slate-500 mr-1">PRIZES:</span>
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`w-2.5 h-3.5 rounded-xs border transition-colors ${
                    i < yourPrizesClaimed
                      ? 'bg-amber-400 border-amber-300'
                      : 'bg-white/5 border-white/10'
                  }`}
                  title={i < yourPrizesClaimed ? 'Claimed Prize' : 'Remaining Prize'}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 3. Streamlined Decision Pipeline Trace & Timeline Controls */}
      <div className="p-4 rounded-lg border border-white/6 bg-[#0B0D12] flex flex-col md:flex-row items-center justify-between gap-4 font-mono text-xs">
        {/* Playback Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentStep(0)}
            className="p-1.5 rounded-xs bg-white/4 hover:bg-white/8 text-slate-300 transition-colors cursor-pointer"
            title="Reset"
          >
            <SkipBack className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="px-4 py-1.5 rounded-xs bg-amber-400 hover:bg-amber-300 text-black font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5 fill-current" />}
            <span>{isPlaying ? 'PAUSE' : 'PLAY'}</span>
          </button>
          <button
            onClick={() => setCurrentStep((p) => Math.min(timeline.length - 1, p + 1))}
            className="p-1.5 rounded-xs bg-white/4 hover:bg-white/8 text-slate-300 transition-colors cursor-pointer"
            title="Step Forward"
          >
            <SkipForward className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Scrubber */}
        <div className="flex-1 w-full max-w-md flex items-center gap-3">
          <input
            type="range"
            min={0}
            max={Math.max(0, timeline.length - 1)}
            value={currentStep}
            onChange={(e) => setCurrentStep(Number(e.target.value))}
            className="w-full h-1 rounded-xs bg-white/10 accent-amber-400 cursor-pointer"
          />
          <span className="text-slate-400 whitespace-nowrap">
            {currentStep + 1} / {timeline.length}
          </span>
        </div>

        {/* Speed */}
        <div className="flex items-center gap-1 text-[11px]">
          {[1, 2, 5].map((spd) => (
            <button
              key={spd}
              onClick={() => setPlaybackSpeed(spd)}
              className={`px-2 py-0.5 rounded-xs font-bold transition-colors cursor-pointer ${
                playbackSpeed === spd
                  ? 'bg-amber-400 text-black'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {spd}x
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LiveBattlefield;
