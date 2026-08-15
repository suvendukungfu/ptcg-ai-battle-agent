import React from 'react';
import { Compass, ArrowUpRight, AlertCircle } from 'lucide-react';

interface ArchetypeMetaItem {
  archetype: string;
  share: number;
  trend: string;
  threat: string;
  color: string;
}

interface MetaRadarCardProps {
  metaData?: ArchetypeMetaItem[];
  onNavigateMeta: () => void;
}

const DEFAULT_META: ArchetypeMetaItem[] = [
  { archetype: 'Bellibolt ex Heavy Ramp', share: 32.0, trend: '+2.5%', threat: 'LOW', color: '#6366f1' },
  { archetype: 'Miraidon ex Aggro', share: 26.5, trend: '-1.0%', threat: 'MEDIUM', color: '#f59e0b' },
  { archetype: 'Crustle Safeguard Stall', share: 18.0, trend: '+4.2%', threat: 'HIGH', color: '#f43f5e' },
  { archetype: 'Charizard ex Late Surge', share: 14.5, trend: '-3.1%', threat: 'MEDIUM', color: '#fb923c' },
  { archetype: 'Lost Box Tempo', share: 9.0, trend: '-2.6%', threat: 'LOW', color: '#06b6d4' },
];

export const MetaRadarCard: React.FC<MetaRadarCardProps> = ({ metaData = DEFAULT_META, onNavigateMeta }) => {
  return (
    <div className="glass-panel p-5 rounded-2xl border border-white/8 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-white/8">
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-emerald-400" />
          <h3 className="text-base font-bold text-white tracking-tight">
            Live Meta-Game Radar
          </h3>
        </div>
        <button
          onClick={onNavigateMeta}
          className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition-colors"
        >
          <span>Observatory</span>
          <ArrowUpRight className="w-3 h-3" />
        </button>
      </div>

      <p className="text-xs text-slate-400 leading-relaxed">
        Real-time ladder archetype share, shifting trends, and calculated threat vulnerability against our active deck.
      </p>

      {/* Meta Shares Stack Bar */}
      <div className="w-full h-3 rounded-full bg-white/5 overflow-hidden flex">
        {metaData.map((item, idx) => (
          <div
            key={idx}
            style={{ width: `${item.share}%`, backgroundColor: item.color }}
            className="h-full relative group cursor-pointer transition-all duration-300"
            title={`${item.archetype}: ${item.share}%`}
          />
        ))}
      </div>

      {/* List of Archetypes */}
      <div className="space-y-2">
        {metaData.map((item, idx) => {
          const isHighThreat = item.threat === 'HIGH';
          const isMedThreat = item.threat === 'MEDIUM';

          return (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-white/2 hover:bg-white/4 border border-white/5 flex items-center justify-between transition-colors"
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <span
                  className="w-2.5 h-2.5 rounded-full shrink-0"
                  style={{ backgroundColor: item.color }}
                />
                <div className="truncate">
                  <div className="text-xs font-bold text-white truncate">{item.archetype}</div>
                  <div className="text-[10px] text-slate-400 font-mono flex items-center gap-1.5 mt-0.5">
                    <span>{item.share}% share</span>
                    <span className={item.trend.startsWith('+') ? 'text-emerald-400' : 'text-slate-400'}>
                      ({item.trend})
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider ${
                    isHighThreat
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                      : isMedThreat
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  }`}
                >
                  {item.threat} Threat
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Meta Notice */}
      <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-[11px] text-indigo-300 flex items-start gap-2">
        <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-indigo-400" />
        <div>
          <strong>Meta Adaptation:</strong> Recent surge in Crustle (+4.2%) triggers our Safeguard counterplay heuristic (Tadbulb single-prize development).
        </div>
      </div>
    </div>
  );
};
