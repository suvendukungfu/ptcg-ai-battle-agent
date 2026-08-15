import React, { useRef, useEffect } from 'react';
import { Swords, Zap, Trophy } from 'lucide-react';


export interface CombatEvent {
  turn: number;
  player: string;
  type: 'attack' | 'energy' | 'trainer' | 'evolution' | 'pass' | 'knockout' | 'system';
  message: string;
  damage?: number;
  score?: number;
}

interface CombatLogFeedProps {
  events: CombatEvent[];
  currentTurn?: number;
}

export const CombatLogFeed: React.FC<CombatLogFeedProps> = ({ events, currentTurn }) => {
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events.length]);

  return (
    <div className="glass-panel rounded-2xl border border-white/8 flex flex-col h-full overflow-hidden">
      {/* Feed Header */}
      <div className="p-3.5 border-b border-white/8 flex items-center justify-between bg-white/[0.02]">
        <div className="flex items-center gap-2">
          <Swords className="w-4 h-4 text-indigo-400" />
          <h4 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
            Battle Action Telemetry
          </h4>
        </div>
        <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
          Turn {currentTurn || 1}
        </span>
      </div>

      {/* Feed Body */}
      <div
        ref={scrollRef}
        className="flex-1 p-3 space-y-2 overflow-y-auto max-h-[360px] text-xs font-mono select-none"
      >
        {events.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-500 text-[11px] py-12">
            Awaiting battle start or playback...
          </div>
        ) : (
          events.map((evt, idx) => {
            const isP0 = evt.player === 'YOU' || evt.player === 'Agent_0' || evt.player === 'Player 0';
            const isAttack = evt.type === 'attack';
            const isKO = evt.type === 'knockout';
            const isEnergy = evt.type === 'energy';

            return (
              <div
                key={idx}
                className={`p-2 rounded-lg border transition-all text-[11px] ${
                  isKO
                    ? 'bg-amber-500/10 border-amber-500/30 text-amber-200'
                    : isAttack
                    ? isP0
                      ? 'bg-indigo-950/40 border-indigo-500/30 text-slate-200'
                      : 'bg-rose-950/40 border-rose-500/30 text-slate-200'
                    : 'bg-white/[0.02] border-white/5 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between text-[10px] text-slate-400 mb-0.5">
                  <span className="font-bold flex items-center gap-1">
                    <span
                      className={`w-1.5 h-1.5 rounded-full ${
                        isP0 ? 'bg-indigo-400' : 'bg-rose-400'
                      }`}
                    />
                    {isP0 ? 'YOU (Bellibolt ex)' : 'OPPONENT'}
                  </span>
                  <span>T{evt.turn}</span>
                </div>

                <div className="flex items-start gap-1.5">
                  {isAttack && <Swords className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />}
                  {isEnergy && <Zap className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />}
                  {isKO && <Trophy className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />}
                  <span className="flex-1 leading-snug">{evt.message}</span>
                </div>

                {evt.damage !== undefined && (
                  <div className="text-[10px] text-rose-400 font-bold mt-0.5">
                    Damage Dealt: -{evt.damage} HP
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
