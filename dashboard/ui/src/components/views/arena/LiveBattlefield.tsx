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
    <div className="space-y-6 text-left pb-12">
      {/* 1. Battlefield Top Control HUD */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-tactical-radar" />
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2 font-display">
              Live Arena Battlefield Twin
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/30 font-mono font-bold">
              3D PERSPECTIVE HUD
            </span>
          </div>
          <div className="flex items-center gap-3 text-xs font-mono text-slate-400 mt-1">
            <span>TURN // {String(step.turn || 1).padStart(2, '0')}</span>
            <span>•</span>
            <span>STEP // {String(currentStep + 1).padStart(2, '0')} / {timeline.length || 64}</span>
            <span>•</span>
            <span className="text-amber-400 font-bold">
              AI DECISION // {step.action_name || 'ELECTRO BULLET'}
            </span>
          </div>
        </div>

        {/* Action Triggers */}
        <div className="flex items-center gap-2">
          {onNavigateExplainer && (
            <button
              onClick={onNavigateExplainer}
              className="px-3.5 py-1.5 rounded-xl bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/40 text-indigo-200 text-xs font-mono font-bold flex items-center gap-1.5 transition-all shadow-md"
            >
              <GitBranch className="w-3.5 h-3.5 text-indigo-400" />
              TRACE DECISION
            </button>
          )}

          <button
            onClick={() => startNewSimulation('heuristic_v1')}
            disabled={isLoading}
            className="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-mono font-black text-xs flex items-center gap-1.5 transition-all shadow-lg shadow-amber-500/20 cursor-pointer disabled:opacity-50"
          >
            <RotateCcw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            NEW BATTLE
          </button>
        </div>
      </div>

      {/* 2. Main 3D Tactical Battlefield Canvas */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 space-y-8 relative overflow-hidden bg-radial from-slate-900/60 via-slate-950 to-[#030509]">
        {/* Opponent Zone */}
        <div className="space-y-4">
          <div className="flex justify-between items-center text-xs font-mono pb-2 border-b border-white/6">
            <div className="flex items-center gap-2 text-rose-300 font-bold">
              <span className="w-2 h-2 rounded-full bg-rose-500" />
              OPPONENT // HEURISTIC BASELINE V1
            </div>

            {/* Opponent Prize Tokens (6 Tokens) */}
            <div className="flex items-center gap-1.5">
              <span className="text-[10px] text-slate-400 mr-1">PRIZES:</span>
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`w-3 h-4 rounded-sm border transition-all ${
                    i < oppPrizesClaimed
                      ? 'bg-rose-500 border-rose-300 shadow-sm shadow-rose-500/50'
                      : 'bg-white/5 border-white/20'
                  }`}
                  title={i < oppPrizesClaimed ? 'Claimed Prize' : 'Remaining Prize'}
                />
              ))}
            </div>
          </div>

          {/* Opponent Bench & Active Layout */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-2">
            {/* Opponent Bench */}
            <div className="flex gap-3">
              <PokemonCard cardId={344} variant="battle-bench" isOpponent hp={70} maxHp={70} />
              <PokemonCard cardId={344} variant="battle-bench" isOpponent hp={70} maxHp={70} />
            </div>

            {/* Opponent Active */}
            <PokemonCard
              cardId={oppActiveId}
              variant="battle-active"
              isOpponent
              hp={oppActiveHp}
              maxHp={oppActiveMaxHp}
              energyCount={oppActiveEnergy}
              isImmune={oppActiveId === 345}
            />
          </div>
        </div>

        {/* Center Clash Telemetry Banner & Action Readout */}
        <div className="py-3 px-6 rounded-2xl bg-black/60 border border-white/8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-amber-400/10 text-amber-400 border border-amber-400/30">
              <Swords className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[10px] text-slate-400">LAST ACTION EXECUTED</div>
              <div className="text-white font-bold text-sm">
                {step.action_name || 'Electro Bullet (160 DMG)'}
              </div>
            </div>
          </div>

          {/* AI Decision Breakdown Chips */}
          <div className="flex items-center gap-3 text-[11px]">
            <div className="px-2.5 py-1 rounded-lg bg-white/4 border border-white/8">
              <span className="text-slate-400 mr-1">PRIZE:</span>
              <span className="text-emerald-400 font-bold">+220</span>
            </div>
            <div className="px-2.5 py-1 rounded-lg bg-white/4 border border-white/8">
              <span className="text-slate-400 mr-1">BOARD:</span>
              <span className="text-indigo-300 font-bold">+310</span>
            </div>
            <div className="px-2.5 py-1 rounded-lg bg-white/4 border border-white/8">
              <span className="text-slate-400 mr-1">RETALIATION:</span>
              <span className="text-rose-400 font-bold">-45</span>
            </div>
            <div className="px-3 py-1 rounded-lg bg-amber-400/10 border border-amber-400/40 text-amber-300 font-black">
              SCORE: +655
            </div>
          </div>
        </div>

        {/* Player Zone */}
        <div className="space-y-4">
          {/* Player Active & Bench Layout */}
          <div className="flex flex-col-reverse sm:flex-row items-center justify-center gap-6 pb-2">
            {/* Player Active (Dominant) */}
            <PokemonCard
              cardId={yourActiveId}
              variant="battle-active"
              isActive
              isSelected
              hp={yourActiveHp}
              maxHp={yourActiveMaxHp}
              energyCount={yourActiveEnergy}
              hasTool={true}
            />

            {/* Player Bench */}
            <div className="flex gap-3">
              <PokemonCard cardId={722} variant="battle-bench" hp={140} maxHp={140} energyCount={1} />
              <PokemonCard cardId={721} variant="battle-bench" hp={70} maxHp={70} energyCount={0} />
            </div>
          </div>

          <div className="flex justify-between items-center text-xs font-mono pt-2 border-t border-white/6">
            <div className="flex items-center gap-2 text-amber-300 font-bold">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-tactical-radar" />
              PLAYER // PTCG AI NEXUS AGENT (V3.0)
            </div>

            {/* Player Prize Tokens (6 Tokens) */}
            <div className="flex items-center gap-1.5">
              <span className="text-[10px] text-slate-400 mr-1">PRIZES CLAIMED:</span>
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`w-3 h-4 rounded-sm border transition-all ${
                    i < yourPrizesClaimed
                      ? 'bg-amber-400 border-amber-200 shadow-sm shadow-amber-400/50'
                      : 'bg-white/5 border-white/20'
                  }`}
                  title={i < yourPrizesClaimed ? 'Claimed Prize' : 'Remaining Prize'}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 3. Playback Controls & Speed Bar */}
      <div className="glass-panel p-4 rounded-2xl border border-white/8 flex flex-col sm:flex-row items-center justify-between gap-4 font-mono">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentStep(0)}
            className="p-2 rounded-xl bg-white/4 hover:bg-white/10 text-slate-300 transition-colors"
            title="Reset to Turn 1"
          >
            <SkipBack className="w-4 h-4" />
          </button>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="px-5 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-black text-xs flex items-center gap-1.5 shadow-lg shadow-amber-500/20 transition-all cursor-pointer"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current" />}
            <span>{isPlaying ? 'PAUSE BATTLE' : 'PLAY BATTLE'}</span>
          </button>
          <button
            onClick={() => setCurrentStep((p) => Math.min(timeline.length - 1, p + 1))}
            className="p-2 rounded-xl bg-white/4 hover:bg-white/10 text-slate-300 transition-colors"
            title="Step Forward"
          >
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        {/* Timeline Slider */}
        <div className="flex-1 w-full max-w-md flex items-center gap-3">
          <input
            type="range"
            min={0}
            max={Math.max(0, timeline.length - 1)}
            value={currentStep}
            onChange={(e) => setCurrentStep(Number(e.target.value))}
            className="w-full h-1.5 rounded-lg bg-white/10 accent-amber-400 cursor-pointer"
          />
          <span className="text-xs text-slate-300 whitespace-nowrap">
            Step {currentStep + 1} / {timeline.length}
          </span>
        </div>

        {/* Speed Controls */}
        <div className="flex items-center gap-1 bg-white/4 p-1 rounded-xl text-xs">
          {[0.5, 1, 2, 5].map((spd) => (
            <button
              key={spd}
              onClick={() => setPlaybackSpeed(spd)}
              className={`px-2 py-0.5 rounded-lg font-bold transition-all ${
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
