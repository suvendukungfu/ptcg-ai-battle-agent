import React, { useState, useEffect } from 'react';
import { api } from '../../../services/api';
import { PokemonCard } from '../../common/PokemonCard';
import { LossForensicsPanel } from './LossForensicsPanel';
import {
  Film,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  TrendingUp,
  Swords,
  Layers,
  Sparkles,
  AlertTriangle,
} from 'lucide-react';

export const ReplayExplorerView: React.FC = () => {
  const [simulationData, setSimulationData] = useState<any | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [selectedFilter, setSelectedFilter] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'timeline' | 'forensics'>('timeline');

  useEffect(() => {
    async function loadReplay() {
      try {
        const res = await api.simulateBattle('production_v2', 'heuristic_v1');
        setSimulationData(res);
        setCurrentStep(0);
      } catch (e) {
        console.error('Failed to load replay:', e);
      }
    }
    loadReplay();
  }, []);

  useEffect(() => {
    if (!isPlaying || !simulationData?.timeline) return;
    const timer = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= simulationData.timeline.length - 1) {
          setIsPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, 800);
    return () => clearInterval(timer);
  }, [isPlaying, simulationData]);

  const timeline = simulationData?.timeline || [];
  const prizeTraj = simulationData?.prize_trajectory || [];
  const stepData = timeline[currentStep] || {};

  // Filter events
  const filteredEvents = timeline.filter((item: any) => {
    if (selectedFilter === 'all') return true;
    if (selectedFilter === 'attack') return item.action_name?.toLowerCase().includes('bullet') || item.damage_dealt;
    if (selectedFilter === 'energy') return item.action_name?.toLowerCase().includes('energy') || item.action_name?.toLowerCase().includes('generator');
    if (selectedFilter === 'trainer') return item.action_name?.toLowerCase().includes('orders') || item.action_name?.toLowerCase().includes('ball') || item.action_name?.toLowerCase().includes('switch');
    return true;
  });

  return (
    <div className="space-y-6 text-left pb-12">
      {/* 1. Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-3 border-b border-white/8">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2 font-display">
              <Film className="w-6 h-6 text-amber-400" />
              Replay Explorer & Post-Game Forensics
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/30 font-mono font-bold">
              TURNING POINT ANALYSIS
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Turn-by-turn trajectory scrubber, prize race curve, board momentum differentials, and automated loss forensic mining.
          </p>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 bg-white/4 p-1 rounded-xl text-xs font-mono">
            <button
              onClick={() => setViewMode('timeline')}
              className={`px-3 py-1 rounded-lg font-bold transition-all ${
                viewMode === 'timeline'
                  ? 'bg-amber-400 text-black'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              MOMENTUM REPLAY
            </button>
            <button
              onClick={() => setViewMode('forensics')}
              className={`px-3 py-1 rounded-lg font-bold transition-all flex items-center gap-1.5 ${
                viewMode === 'forensics'
                  ? 'bg-rose-500 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <AlertTriangle className="w-3.5 h-3.5" />
              ANALYZE LOSS
            </button>
          </div>
        </div>
      </div>

      {/* 2. Loss Forensics Panel Mode */}
      {viewMode === 'forensics' && <LossForensicsPanel />}

      {/* 3. Momentum Timeline Mode */}
      {viewMode === 'timeline' && (
        <>
          {/* Prize Momentum Differential Curve (SVG) */}
          <div className="glass-panel p-5 rounded-3xl border border-white/8 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-amber-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
                  Prize Trade Differential Curve & Momentum Timeline
                </h3>
              </div>
              <div className="flex items-center gap-3 text-[11px] font-mono text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-0.5 bg-emerald-400 inline-block" /> Positive Advantage (+Prizes)
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-0.5 bg-rose-400 inline-block" /> Deficit (-Prizes)
                </span>
              </div>
            </div>

            {/* SVG Curve */}
            <div className="h-44 w-full relative">
              <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 800 160">
                {/* Zero Line */}
                <line x1="0" y1="80" x2="800" y2="80" stroke="rgba(255,255,255,0.15)" strokeDasharray="4 4" strokeWidth="1" />

                {/* Trajectory Path */}
                {prizeTraj.length > 1 && (
                  <path
                    d={prizeTraj
                      .map((pt: any, i: number) => {
                        const x = (i / (prizeTraj.length - 1)) * 800;
                        const diff = pt.prize_diff || 0;
                        const y = 80 - diff * 18;
                        return `${i === 0 ? 'M' : 'L'} ${x} ${Math.max(10, Math.min(150, y))}`;
                      })
                      .join(' ')}
                    fill="none"
                    stroke="#facc15"
                    strokeWidth="2.5"
                  />
                )}

                {/* Current Step Scrubber Line */}
                {timeline.length > 0 && (
                  <line
                    x1={(currentStep / (timeline.length - 1)) * 800}
                    y1="0"
                    x2={(currentStep / (timeline.length - 1)) * 800}
                    y2="160"
                    stroke="#38bdf8"
                    strokeWidth="2"
                    strokeDasharray="2 2"
                  />
                )}
              </svg>
            </div>

            {/* Playback Controls & Slider */}
            <div className="flex items-center gap-3 pt-2 border-t border-white/6 font-mono">
              <button
                onClick={() => setCurrentStep(0)}
                className="p-2 rounded-xl bg-white/4 hover:bg-white/10 text-slate-300 transition-colors cursor-pointer"
                title="Jump to Start"
              >
                <SkipBack className="w-4 h-4" />
              </button>
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="px-5 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-black text-xs flex items-center gap-1.5 shadow-lg shadow-amber-500/20 transition-all cursor-pointer"
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current" />}
                <span>{isPlaying ? 'PAUSE' : 'PLAY'}</span>
              </button>
              <button
                onClick={() => setCurrentStep((p) => Math.min(timeline.length - 1, p + 1))}
                className="p-2 rounded-xl bg-white/4 hover:bg-white/10 text-slate-300 transition-colors cursor-pointer"
                title="Step Forward"
              >
                <SkipForward className="w-4 h-4" />
              </button>

              <input
                type="range"
                min={0}
                max={Math.max(0, timeline.length - 1)}
                value={currentStep}
                onChange={(e) => setCurrentStep(Number(e.target.value))}
                className="flex-1 h-1.5 rounded-lg bg-white/10 accent-amber-400 cursor-pointer"
              />
              <span className="text-xs text-slate-300 w-24 text-right">
                Step {currentStep + 1} / {timeline.length}
              </span>
            </div>
          </div>

          {/* Step Snapshot & Event Log Split */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left 6 Cols: Step Snapshot Cards */}
            <div className="lg:col-span-6 glass-panel p-5 rounded-3xl border border-white/8 space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-white/8">
                <span className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-amber-400" />
                  Board Snapshot (Turn {stepData.turn || 1})
                </span>
                <span className="text-[11px] font-mono text-slate-400">Step {currentStep + 1}</span>
              </div>

              {/* Physical Active Pokemon Clash */}
              <div className="flex justify-center items-center gap-6 py-2">
                <PokemonCard
                  cardId={stepData.your_active?.id || 723}
                  variant="compact"
                  hp={stepData.your_active?.hp || 350}
                  maxHp={350}
                  energyCount={stepData.your_active?.energies?.length || 2}
                  isSelected
                />

                <div className="text-xs font-mono font-bold text-slate-500">VS</div>

                <PokemonCard
                  cardId={stepData.opp_active?.id || 344}
                  variant="compact"
                  isOpponent
                  hp={stepData.opp_active?.hp || 70}
                  maxHp={150}
                  energyCount={stepData.opp_active?.energies?.length || 0}
                />
              </div>

              {/* Action Taken at this step */}
              <div className="p-3.5 rounded-2xl bg-white/2 border border-white/6 text-xs font-mono space-y-1">
                <div className="text-slate-400 text-[10px] uppercase tracking-wider">Executed Action</div>
                <div className="text-white font-bold text-xs flex items-center gap-2">
                  <Swords className="w-4 h-4 text-amber-400" />
                  <span>{stepData.action_name || 'Turn Setup / Pass'}</span>
                </div>
                {stepData.damage_dealt && (
                  <div className="text-rose-400 font-bold text-[11px]">
                    Damage Dealt: {stepData.damage_dealt} HP
                  </div>
                )}
              </div>
            </div>

            {/* Right 6 Cols: Event Timeline Stream with Filters */}
            <div className="lg:col-span-6 glass-panel p-5 rounded-3xl border border-white/8 space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-white/8">
                <span className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <Layers className="w-4 h-4 text-amber-400" />
                  Game Action Timeline
                </span>

                {/* Filter Tabs */}
                <div className="flex items-center gap-1 bg-white/4 p-0.5 rounded-lg text-[10px] font-mono">
                  {['all', 'attack', 'energy', 'trainer'].map((f) => (
                    <button
                      key={f}
                      onClick={() => setSelectedFilter(f)}
                      className={`px-2 py-0.5 rounded capitalize font-bold transition-all ${
                        selectedFilter === f
                          ? 'bg-amber-400 text-black'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      {f}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2 max-h-80 overflow-y-auto pr-1 text-xs font-mono">
                {filteredEvents.map((ev: any, idx: number) => {
                  const isSelected = idx === currentStep;
                  return (
                    <div
                      key={idx}
                      onClick={() => setCurrentStep(idx)}
                      className={`p-2.5 rounded-xl border cursor-pointer transition-all ${
                        isSelected
                          ? 'bg-amber-950/40 border-amber-400 text-white shadow-md'
                          : 'bg-white/2 border-white/5 text-slate-300 hover:bg-white/4 hover:border-white/10'
                      }`}
                    >
                      <div className="flex justify-between items-center text-[10px] text-slate-400 mb-0.5">
                        <span className="font-bold text-amber-300">Turn {ev.turn || 1} • Step {idx + 1}</span>
                        <span>{ev.active_player === 0 ? 'YOU' : 'OPPONENT'}</span>
                      </div>
                      <div className="font-bold text-xs truncate">
                        {ev.action_name || 'Pass / Next Phase'}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ReplayExplorerView;
