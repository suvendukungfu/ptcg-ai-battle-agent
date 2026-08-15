import React from 'react';
import { Award } from 'lucide-react';

interface PrizeBarProps {
  prizesRemaining: number;
  totalPrizes?: number;
  isOpponent?: boolean;
  label?: string;
}

export const PrizeBar: React.FC<PrizeBarProps> = ({
  prizesRemaining,
  totalPrizes = 6,
  isOpponent = false,
  label = 'Prizes Remaining',
}) => {
  const prizesTaken = Math.max(0, totalPrizes - prizesRemaining);

  return (
    <div className="flex items-center gap-2 p-2 rounded-xl bg-slate-900/60 border border-white/8 text-xs select-none">
      <Award
        className={`w-4 h-4 ${isOpponent ? 'text-rose-400' : 'text-indigo-400'}`}
      />
      <div className="flex flex-col">
        <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
          {label}
        </span>
        <div className="flex items-center gap-1.5 mt-1">
          {Array.from({ length: totalPrizes }).map((_, i) => {
            const isRemaining = i < prizesRemaining;
            return (
              <div
                key={i}
                className={`w-3.5 h-5 rounded-sm transition-all duration-300 border ${
                  isRemaining
                    ? isOpponent
                      ? 'bg-rose-500/30 border-rose-500/60 shadow-xs shadow-rose-500/20'
                      : 'bg-indigo-500/30 border-indigo-500/60 shadow-xs shadow-indigo-500/20'
                    : 'bg-white/5 border-white/10 opacity-30'
                }`}
                title={isRemaining ? 'Unclaimed Prize Card' : 'Prize Claimed'}
              />
            );
          })}
          <span className="font-mono font-bold text-white text-xs ml-1">
            {prizesRemaining} left ({prizesTaken} claimed)
          </span>
        </div>
      </div>
    </div>
  );
};
