import React from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  FastForward,
  Loader2,
  Swords,
} from 'lucide-react';

interface ArenaControlsProps {
  isPlaying: boolean;
  onTogglePlay: () => void;
  onStepBack: () => void;
  onStepForward: () => void;
  onReset: () => void;
  speed: number;
  onSpeedChange: (speed: number) => void;
  currentStep: number;
  totalSteps: number;
  onSeek: (step: number) => void;
  opponent: string;
  onOpponentChange: (opp: string) => void;
  onSimulateBattle: () => void;
  isSimulating: boolean;
}

export const ArenaControls: React.FC<ArenaControlsProps> = ({
  isPlaying,
  onTogglePlay,
  onStepBack,
  onStepForward,
  onReset,
  speed,
  onSpeedChange,
  currentStep,
  totalSteps,
  onSeek,
  opponent,
  onOpponentChange,
  onSimulateBattle,
  isSimulating,
}) => {
  return (
    <div className="glass-panel p-4 rounded-2xl border border-white/8 space-y-3 select-none">
      {/* Top Controls Row */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        {/* Playback Button Group */}
        <div className="flex items-center gap-1.5 bg-white/4 p-1 rounded-xl border border-white/6">
          <button
            onClick={onReset}
            className="p-2 rounded-lg hover:bg-white/10 text-slate-300 hover:text-white transition-colors"
            title="Reset to Step 0"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          <button
            onClick={onStepBack}
            disabled={currentStep <= 0}
            className="p-2 rounded-lg hover:bg-white/10 text-slate-300 hover:text-white disabled:opacity-40 transition-colors"
            title="Step Back"
          >
            <SkipBack className="w-4 h-4" />
          </button>

          <button
            onClick={onTogglePlay}
            disabled={totalSteps === 0}
            className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-lg shadow-indigo-600/20 disabled:opacity-40 transition-all"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current" />}
            <span>{isPlaying ? 'PAUSE' : 'PLAY'}</span>
          </button>

          <button
            onClick={onStepForward}
            disabled={currentStep >= totalSteps - 1}
            className="p-2 rounded-lg hover:bg-white/10 text-slate-300 hover:text-white disabled:opacity-40 transition-colors"
            title="Step Forward"
          >
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        {/* Speed Selector */}
        <div className="flex items-center gap-1 bg-white/4 p-1 rounded-xl border border-white/6 text-xs font-mono">
          <FastForward className="w-3.5 h-3.5 text-slate-400 ml-1.5" />
          {[0.5, 1, 2, 5].map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-2.5 py-1 rounded-lg font-bold transition-all ${
                speed === s
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>

        {/* Opponent Selection & Start Simulation */}
        <div className="flex items-center gap-2">
          <select
            value={opponent}
            onChange={(e) => onOpponentChange(e.target.value)}
            disabled={isSimulating}
            className="px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-200 font-semibold focus:outline-hidden focus:border-indigo-500 cursor-pointer"
          >
            <option value="heuristic_v1">Opponent: Heuristic Baseline v1</option>
            <option value="random">Opponent: Random Baseline</option>
            <option value="first">Opponent: First Legal Policy</option>
            <option value="self">Opponent: Self-Play (Bellibolt Mirror)</option>
          </select>

          <button
            onClick={onSimulateBattle}
            disabled={isSimulating}
            className="px-4 py-2 rounded-xl bg-linear-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-emerald-600/20 disabled:opacity-50 transition-all border border-white/10"
          >
            {isSimulating ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Swords className="w-4 h-4" />
            )}
            <span>{isSimulating ? 'Simulating...' : 'Start Battle'}</span>
          </button>
        </div>
      </div>

      {/* Scrubber Timeline Slider */}
      <div className="flex items-center gap-3 pt-2">
        <span className="text-[11px] font-mono text-slate-400 shrink-0">
          Step {Math.min(currentStep + 1, totalSteps)} / {totalSteps || 0}
        </span>
        <input
          type="range"
          min={0}
          max={Math.max(0, totalSteps - 1)}
          value={currentStep}
          onChange={(e) => onSeek(Number(e.target.value))}
          disabled={totalSteps <= 1}
          className="flex-1 h-1.5 rounded-lg bg-white/10 accent-indigo-500 cursor-pointer disabled:opacity-40"
        />
      </div>
    </div>
  );
};
