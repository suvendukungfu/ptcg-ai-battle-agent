import React, { useState } from 'react';
import { getCardMeta, type CardMeta } from '../../services/cardRegistry';
import {
  Shield,
  Zap,
  Swords,
  Skull,
} from 'lucide-react';

export type CardVariant =
  | 'battle'
  | 'bench'
  | 'standard'
  | 'compact'
  | 'codex'
  | 'preview'
  | 'thumbnail'
  | 'battle-active'
  | 'battle-bench';

export interface PokemonCardProps {
  cardId?: number;
  customMeta?: Partial<CardMeta>;
  variant?: CardVariant;
  hp?: number;
  maxHp?: number;
  energyCount?: number;
  hasTool?: boolean;
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

  // Sizing by physical card aspect ratio (~1:1.4)
  const sizeClasses: Record<CardVariant, string> = {
    battle: 'w-48 h-68 sm:w-56 sm:h-78',
    'battle-active': 'w-48 h-68 sm:w-56 sm:h-78',
    bench: 'w-20 h-28 sm:w-24 sm:h-34',
    'battle-bench': 'w-20 h-28 sm:w-24 sm:h-34',
    standard: 'w-44 h-62',
    compact: 'w-28 h-40',
    codex: 'w-full h-72 sm:h-80',
    preview: 'w-64 h-90',
    thumbnail: 'w-14 h-20',
  };

  const isLarge =
    variant === 'battle' ||
    variant === 'battle-active' ||
    variant === 'codex' ||
    variant === 'standard' ||
    variant === 'preview';

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`relative select-none transition-transform duration-200 rounded-lg group ${
        sizeClasses[variant]
      } ${
        onClick ? 'cursor-pointer' : ''
      } ${
        isSelected
          ? 'ring-1 ring-amber-400 shadow-lg shadow-amber-400/20 -translate-y-1'
          : isHovered
          ? '-translate-y-1 shadow-xl'
          : 'shadow-md'
      } ${isFainted ? 'opacity-30 grayscale' : ''} ${className}`}
      style={{
        perspective: '800px',
      }}
    >
      {/* 1. Physical Game Card Object */}
      <div
        className={`w-full h-full rounded-lg overflow-hidden relative border transition-colors duration-200 flex flex-col justify-between ${
          isOpponent
            ? 'bg-[#11141A] border-rose-500/30 hover:border-rose-500/60'
            : isSelected
            ? 'bg-[#11141A] border-amber-400'
            : 'bg-[#0B0D12] border-white/8 hover:border-amber-400/50'
        }`}
      >
        {/* Card Artwork Image */}
        <div className="absolute inset-0 z-0 overflow-hidden bg-[#07080B]">
          <img
            src={imgSrc}
            alt={meta.name}
            onError={() => setImgSrc(meta.fallbackImg)}
            className="w-full h-full object-cover object-center transition-transform duration-300 group-hover:scale-102"
            loading="lazy"
          />
          {/* Controlled dark gradient overlay */}
          <div className="absolute inset-0 bg-linear-to-t from-[#07080B] via-[#07080B]/20 to-transparent" />
        </div>

        {/* Top Header Strip */}
        <div className="relative z-10 p-2 flex justify-between items-start bg-linear-to-b from-black/80 via-black/40 to-transparent">
          <div className="flex items-center gap-1">
            <span
              className={`text-[9px] font-mono font-bold px-1 py-0.2 rounded-xs tracking-wider ${
                meta.isEx
                  ? 'bg-amber-400 text-black font-black'
                  : 'bg-white/20 text-white'
              }`}
            >
              {meta.isEx ? 'ex' : meta.stage || 'BASIC'}
            </span>
            <span className="text-[11px] font-bold text-white truncate max-w-28 drop-shadow">
              {meta.name}
            </span>
          </div>

          {/* HP Badge */}
          {meta.hp && (
            <div className="text-[10px] font-mono font-black text-emerald-400 drop-shadow">
              {currentHp}
              <span className="text-[8px] text-slate-400 font-normal">/{totalHp}</span>
            </div>
          )}
        </div>

        {/* Center Safeguard Immunity / Fainted Overlays */}
        {isImmune && (
          <div className="relative z-10 self-center px-2 py-0.5 rounded-xs bg-emerald-500/90 text-black font-black text-[10px] font-mono border border-emerald-300 shadow flex items-center gap-1">
            <Shield className="w-3 h-3" />
            SAFEGUARD
          </div>
        )}

        {isFainted && (
          <div className="relative z-10 self-center px-2 py-0.5 rounded-xs bg-rose-600/90 text-white font-black text-[10px] font-mono border border-rose-300 shadow flex items-center gap-1">
            <Skull className="w-3 h-3" />
            KNOCKED OUT
          </div>
        )}

        {/* Bottom Card Footer: HP Gauge, Energy, Moves */}
        <div className="relative z-10 p-2 space-y-1 bg-linear-to-t from-black/90 via-black/60 to-transparent">
          {/* HP Bar */}
          {meta.hp && (
            <div className="w-full h-1 rounded-xs bg-black/60 overflow-hidden border border-white/10">
              <div
                style={{ width: `${hpPct}%` }}
                className={`h-full transition-all duration-300 rounded-xs ${hpBarColor}`}
              />
            </div>
          )}

          <div className="flex justify-between items-center text-[9px] font-mono">
            {/* Energy Attachments */}
            <div className="flex items-center gap-0.5 text-amber-300 font-bold">
              <Zap className="w-2.5 h-2.5 text-amber-400" />
              <span>{energyCount}⚡</span>
            </div>

            {/* Attack / Move readout */}
            {isLarge && meta.attacks && meta.attacks[0] && (
              <div className="text-slate-300 truncate max-w-28 flex items-center gap-1">
                <Swords className="w-2.5 h-2.5 text-amber-400" />
                <span className="truncate">{meta.attacks[0].name}</span>
                <span className="font-bold text-white">({meta.attacks[0].damage})</span>
              </div>
            )}

            {/* Heavy Baton / Tool Badge */}
            {hasTool && (
              <span className="px-1 py-0.2 rounded-xs bg-indigo-500/30 border border-indigo-400/40 text-indigo-200 text-[8px] font-bold">
                TOOL
              </span>
            )}
          </div>
        </div>
      </div>

      {/* 2. Hover Tactical Inspection Layer (Desktop Only) */}
      {isHovered && isLarge && (
        <div className="absolute left-1/2 -translate-x-1/2 -top-22 z-30 w-60 p-3 rounded-md bg-[#07080B]/98 border border-amber-400/40 shadow-2xl backdrop-blur-md text-left space-y-1 pointer-events-none transition-opacity duration-150 font-mono">
          <div className="flex justify-between items-center text-[9px] text-slate-400 border-b border-white/8 pb-1">
            <span className="text-amber-400 font-bold">#{meta.id} • {meta.category}</span>
            <span>Retreat: {meta.retreat || 1}⚡</span>
          </div>

          <div className="text-xs font-black text-white">{meta.name}</div>

          {meta.ability && (
            <div className="text-[9px] text-emerald-300 font-sans leading-tight">
              <span className="font-bold font-mono text-emerald-400">Ability: {meta.ability.name} — </span>
              {meta.ability.text}
            </div>
          )}

          {meta.attacks && (
            <div className="space-y-0.5 text-[9px] text-slate-300">
              {meta.attacks.map((atk, i) => (
                <div key={i} className="flex justify-between">
                  <span>{atk.cost} {atk.name}</span>
                  <span className="font-bold text-amber-400">{atk.damage} DMG</span>
                </div>
              ))}
            </div>
          )}

          <div className="text-[8px] text-slate-400 pt-1 border-t border-white/8 truncate">
            {meta.aiPriority}
          </div>
        </div>
      )}
    </div>
  );
};

export default PokemonCard;
