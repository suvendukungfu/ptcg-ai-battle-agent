import React, { useState } from 'react';
import { getCardMeta, type CardMeta } from '../../services/cardRegistry';
import {
  Shield,
  Zap,
  Swords,
  Skull,
} from 'lucide-react';


export type CardVariant = 'battle-active' | 'battle-bench' | 'standard' | 'compact' | 'codex' | 'thumbnail';

export interface PokemonCardProps {
  cardId?: number;
  customMeta?: Partial<CardMeta>;
  variant?: CardVariant;
  hp?: number;
  maxHp?: number;
  energyCount?: number;
  hasTool?: boolean;
  isActive?: boolean;
  isSelected?: boolean;
  isOpponent?: boolean;
  isFainted?: boolean;
  isImmune?: boolean;
  onClick?: () => void;
  className?: string;
}

export const PokemonCard: React.FC<PokemonCardProps> = ({
  cardId = 723,
  customMeta,
  variant = 'standard',
  hp,
  maxHp,
  energyCount = 0,
  hasTool = false,
  isSelected = false,
  isOpponent = false,
  isFainted = false,
  isImmune = false,
  onClick,
  className = '',

}) => {
  const meta: CardMeta = { ...getCardMeta(cardId), ...customMeta };
  const [imgSrc, setImgSrc] = useState<string>(meta.img);
  const [isHovered, setIsHovered] = useState<boolean>(false);

  const currentHp = hp !== undefined ? hp : meta.hp || 100;
  const totalHp = maxHp !== undefined ? maxHp : meta.hp || 100;
  const hpPct = Math.max(0, Math.min(100, (currentHp / Math.max(1, totalHp)) * 100));

  const hpBarColor =
    hpPct > 50 ? 'bg-emerald-500' : hpPct > 20 ? 'bg-amber-400' : 'bg-rose-500';

  // Sizing by variant
  const sizeClasses: Record<CardVariant, string> = {
    'battle-active': 'w-56 h-80 sm:w-64 sm:h-92',
    'battle-bench': 'w-24 h-36 sm:w-28 sm:h-40',
    standard: 'w-48 h-68',
    compact: 'w-32 h-44',
    codex: 'w-full h-84',
    thumbnail: 'w-16 h-24',
  };

  const isLarge = variant === 'battle-active' || variant === 'codex' || variant === 'standard';

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`relative select-none transition-all duration-300 rounded-2xl group ${
        sizeClasses[variant]
      } ${
        onClick ? 'cursor-pointer' : ''
      } ${
        isSelected
          ? 'ring-2 ring-amber-400 shadow-xl shadow-amber-400/30 scale-105'
          : isHovered
          ? 'scale-102 shadow-2xl'
          : 'shadow-md'
      } ${isFainted ? 'opacity-40 grayscale' : ''} ${className}`}
      style={{
        perspective: '1000px',
      }}
    >
      {/* 1. Physical Card Container */}
      <div
        className={`w-full h-full rounded-2xl overflow-hidden relative border transition-all duration-300 flex flex-col justify-between ${
          isOpponent
            ? 'bg-rose-950/20 border-rose-500/30 hover:border-rose-500/60'
            : isSelected
            ? 'bg-amber-950/30 border-amber-400'
            : 'bg-slate-900/90 border-white/10 hover:border-amber-400/50'
        }`}
      >
        {/* Card Artwork Image */}
        <div className="absolute inset-0 z-0 overflow-hidden bg-slate-950">
          <img
            src={imgSrc}
            alt={meta.name}
            onError={() => setImgSrc(meta.fallbackImg)}
            className="w-full h-full object-cover object-center transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
          {/* Subtle dark gradient overlay so text remains readable */}
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent" />
        </div>

        {/* Top Header Bar */}
        <div className="relative z-10 p-2.5 flex justify-between items-start bg-gradient-to-b from-black/80 via-black/40 to-transparent">
          <div>
            <div className="flex items-center gap-1.5">
              <span
                className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded tracking-wider ${
                  meta.isEx
                    ? 'bg-amber-400 text-black font-black'
                    : 'bg-white/20 text-white'
                }`}
              >
                {meta.isEx ? 'ex' : meta.stage || 'BASIC'}
              </span>
              <span className="text-xs font-black text-white truncate max-w-[120px] drop-shadow-md">
                {meta.name}
              </span>
            </div>
          </div>

          {/* HP Badge */}
          {meta.hp && (
            <div className="flex flex-col items-end">
              <div className="text-[11px] font-mono font-black text-emerald-400 flex items-center gap-0.5 drop-shadow">
                <span>{currentHp}</span>
                <span className="text-[9px] text-slate-400">/{totalHp}</span>
              </div>
            </div>
          )}
        </div>

        {/* Center Indicators: Immunity & Fainted Overlays */}
        {isImmune && (
          <div className="relative z-10 self-center px-3 py-1 rounded-full bg-emerald-500/90 text-black font-black text-xs font-mono border border-emerald-300 shadow-lg flex items-center gap-1">
            <Shield className="w-3.5 h-3.5" />
            SAFEGUARD IMMUNE
          </div>
        )}

        {isFainted && (
          <div className="relative z-10 self-center px-3 py-1 rounded-full bg-rose-600/90 text-white font-black text-xs font-mono border border-rose-300 shadow-lg flex items-center gap-1">
            <Skull className="w-3.5 h-3.5" />
            KNOCKED OUT
          </div>
        )}

        {/* Bottom Card Footer: HP Gauge, Energy Chips, Tool Badges */}
        <div className="relative z-10 p-2.5 space-y-1.5 bg-gradient-to-t from-black/90 via-black/60 to-transparent">
          {/* Real-Time HP Progress Bar */}
          {meta.hp && (
            <div className="w-full h-1.5 rounded-full bg-black/60 overflow-hidden border border-white/10">
              <div
                style={{ width: `${hpPct}%` }}
                className={`h-full transition-all duration-300 rounded-full ${hpBarColor}`}
              />
            </div>
          )}

          <div className="flex justify-between items-center text-[10px] font-mono">
            {/* Energy Attachments */}
            <div className="flex items-center gap-1 text-amber-300 font-bold">
              <Zap className="w-3 h-3 text-amber-400" />
              <span>{energyCount}⚡</span>
            </div>

            {/* Attack / Move readout */}
            {isLarge && meta.attacks && meta.attacks[0] && (
              <div className="text-slate-300 truncate max-w-[130px] flex items-center gap-1">
                <Swords className="w-3 h-3 text-indigo-400" />
                <span className="truncate">{meta.attacks[0].name}</span>
                <span className="font-bold text-white">({meta.attacks[0].damage})</span>
              </div>
            )}

            {/* Heavy Baton / Tool Badge */}
            {hasTool && (
              <span className="px-1.5 py-0.5 rounded bg-indigo-500/30 border border-indigo-400/40 text-indigo-200 text-[9px] font-bold">
                TOOL
              </span>
            )}
          </div>
        </div>
      </div>

      {/* 2. Hover Inspection Tactical Card Layer (Desktop Only) */}
      {isHovered && isLarge && (
        <div className="absolute left-1/2 -translate-x-1/2 -top-24 z-30 w-64 p-3.5 rounded-2xl bg-slate-950/95 border border-amber-400/40 shadow-2xl backdrop-blur-xl text-left space-y-1.5 pointer-events-none transition-all duration-200 animate-fadeIn font-mono">
          <div className="flex justify-between items-center text-[10px] text-slate-400 border-b border-white/10 pb-1">
            <span className="text-amber-400 font-bold">#{meta.id} • {meta.category}</span>
            <span>Retreat: {meta.retreat || 1}⚡</span>
          </div>

          <div className="text-xs font-black text-white">{meta.name}</div>

          {meta.ability && (
            <div className="text-[10px] text-emerald-300 font-sans leading-tight">
              <span className="font-bold font-mono text-emerald-400">Ability: {meta.ability.name} — </span>
              {meta.ability.text}
            </div>
          )}

          {meta.attacks && (
            <div className="space-y-0.5 text-[10px] text-slate-300">
              {meta.attacks.map((atk, i) => (
                <div key={i} className="flex justify-between">
                  <span>{atk.cost} {atk.name}</span>
                  <span className="font-bold text-amber-400">{atk.damage} DMG</span>
                </div>
              ))}
            </div>
          )}

          <div className="text-[9px] text-indigo-300/90 pt-1 border-t border-white/10 truncate">
            {meta.aiPriority}
          </div>
        </div>
      )}
    </div>
  );
};
