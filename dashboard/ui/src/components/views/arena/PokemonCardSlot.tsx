import React from 'react';
import { Shield, Skull } from 'lucide-react';


export interface CardSlotData {
  id?: number;
  name?: string;
  hp?: number;
  maxHp?: number;
  damage?: number;
  energies?: any[];
  tool?: string;
  is_active?: boolean;
  stage?: string;
}

interface PokemonCardSlotProps {
  card?: CardSlotData | null;
  label?: string;
  isOpponent?: boolean;
  isActiveSpot?: boolean;
}

export const PokemonCardSlot: React.FC<PokemonCardSlotProps> = ({
  card,
  label,
  isOpponent = false,
  isActiveSpot = false,
}) => {
  if (!card || !card.id) {
    return (
      <div
        className={`rounded-xl border border-dashed border-white/10 flex flex-col items-center justify-center text-slate-500 font-mono text-[11px] transition-all ${
          isActiveSpot ? 'h-40 w-32 sm:h-44 sm:w-36 bg-white/[0.01]' : 'h-28 w-24 sm:h-32 sm:w-28 bg-white/[0.005]'
        }`}
      >
        <span className="text-slate-600">Empty</span>
        {label && <span className="text-[10px] text-slate-600">{label}</span>}
      </div>
    );
  }

  const hp = card.hp !== undefined ? card.hp : 100;
  const maxHp = card.maxHp || hp || 100;
  const hpPercent = Math.max(0, Math.min(100, (hp / maxHp) * 100));
  const isKnockedOut = hp <= 0;

  const energyCount = Array.isArray(card.energies) ? card.energies.length : typeof card.energies === 'number' ? card.energies : 0;

  // Resolve card name and type
  const cardName = card.name || (card.id === 723 ? 'Bellibolt ex' : card.id === 722 ? 'Bellibolt' : card.id === 721 ? 'Tadbulb' : card.id === 558 ? 'Crustle' : `Pokemon #${card.id}`);
  const isEx = cardName.toLowerCase().includes('ex') || card.id === 723;

  return (
    <div
      className={`relative rounded-xl border transition-all duration-300 flex flex-col justify-between p-2.5 group select-none shadow-lg ${
        isActiveSpot
          ? isOpponent
            ? 'h-40 w-32 sm:h-44 sm:w-36 bg-linear-to-b from-rose-950/40 to-slate-950/80 border-rose-500/40 shadow-rose-950/30'
            : 'h-40 w-32 sm:h-44 sm:w-36 bg-linear-to-b from-indigo-950/40 to-slate-950/80 border-indigo-500/40 shadow-indigo-950/30 ring-1 ring-indigo-500/30'
          : 'h-28 w-24 sm:h-32 sm:w-28 bg-slate-900/60 border-white/10 hover:border-white/20'
      } ${isKnockedOut ? 'opacity-40 grayscale' : ''}`}
    >
      {/* Top Header: Name & HP */}
      <div>
        <div className="flex items-center justify-between gap-1">
          <span
            className={`font-bold truncate text-[11px] sm:text-xs ${
              isOpponent ? 'text-rose-200' : 'text-slate-100'
            }`}
            title={cardName}
          >
            {cardName}
          </span>
          {isEx && (
            <span className="px-1 py-0.2 rounded bg-amber-500/20 text-amber-300 font-black text-[9px] border border-amber-500/30 shrink-0">
              ex
            </span>
          )}
        </div>

        {label && (
          <div className="text-[9px] font-mono text-slate-400 truncate">
            {label}
          </div>
        )}
      </div>

      {/* Center Visual / Knockout Overlay */}
      <div className="flex-1 flex items-center justify-center my-1 relative">
        {isKnockedOut ? (
          <div className="flex flex-col items-center text-rose-400">
            <Skull className="w-6 h-6" />
            <span className="text-[9px] font-mono font-bold mt-0.5">KNOCKED OUT</span>
          </div>
        ) : (
          <div
            className={`w-10 h-10 sm:w-12 sm:h-12 rounded-lg flex items-center justify-center font-bold text-xs font-mono shadow-inner ${
              isOpponent ? 'bg-rose-500/10 text-rose-300 border border-rose-500/20' : 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20'
            }`}
          >
            #{card.id}
          </div>
        )}
      </div>

      {/* Bottom Info: HP Bar & Energy Counters */}
      <div className="space-y-1">
        {/* HP Progress Bar */}
        <div>
          <div className="flex justify-between items-center text-[9px] font-mono mb-0.5">
            <span className="text-slate-400">HP</span>
            <span className={hp <= 60 ? 'text-rose-400 font-bold' : 'text-emerald-400'}>
              {Math.max(0, hp)}/{maxHp}
            </span>
          </div>
          <div className="w-full h-1.5 rounded-full bg-black/40 overflow-hidden">
            <div
              style={{ width: `${hpPercent}%` }}
              className={`h-full rounded-full transition-all duration-300 ${
                hpPercent > 50
                  ? 'bg-emerald-400'
                  : hpPercent > 25
                  ? 'bg-amber-400'
                  : 'bg-rose-500'
              }`}
            />
          </div>
        </div>

        {/* Energy Badges */}
        <div className="flex items-center justify-between pt-0.5">
          <div className="flex items-center gap-0.5">
            {Array.from({ length: Math.min(4, energyCount) }).map((_, i) => (
              <span
                key={i}
                className="w-3.5 h-3.5 rounded-full bg-amber-400/20 border border-amber-400/50 flex items-center justify-center text-[8px] text-amber-300 font-black"
                title="Lightning Energy"
              >
                ⚡
              </span>
            ))}
            {energyCount > 4 && (
              <span className="text-[9px] font-mono text-amber-300 font-bold">
                +{energyCount - 4}
              </span>
            )}
            {energyCount === 0 && (
              <span className="text-[9px] font-mono text-slate-500">0⚡</span>
            )}
          </div>

          {card.tool && (
            <span className="text-[9px] text-cyan-300 flex items-center gap-0.5" title={card.tool}>
              <Shield className="w-2.5 h-2.5" />
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
