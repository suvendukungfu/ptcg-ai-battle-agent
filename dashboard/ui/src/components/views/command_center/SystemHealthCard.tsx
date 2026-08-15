import React from 'react';
import { ShieldCheck, HardDrive } from 'lucide-react';

interface SystemHealthCardProps {
  healthData?: {
    status: string;
    fallback_rate_pct: number;
    illegal_actions_count: number;
    unhandled_exceptions_count: number;
    timeout_violations_count: number;
    rss_memory_mb: number;
    memory_limit_mb: number;
    timebank_remaining_sec: number;
  };
}

export const SystemHealthCard: React.FC<SystemHealthCardProps> = ({ healthData }) => {
  const data = healthData || {
    status: 'HEALTHY',
    fallback_rate_pct: 0.0,
    illegal_actions_count: 0,
    unhandled_exceptions_count: 0,
    timeout_violations_count: 0,
    rss_memory_mb: 121.1,
    memory_limit_mb: 12492.8,
    timebank_remaining_sec: 580.0,
  };

  const memPercent = ((data.rss_memory_mb / data.memory_limit_mb) * 100).toFixed(1);

  return (
    <div className="glass-panel p-5 rounded-2xl border border-white/8 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-white/8">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <h3 className="text-base font-bold text-white tracking-tight">
            AI System Health & Integrity Cockpit
          </h3>
        </div>
        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          {data.status}
        </span>
      </div>

      {/* 4-Item Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {/* Fallback Rate */}
        <div className="p-3 rounded-xl bg-white/2 border border-white/5">
          <div className="text-[10px] font-mono text-slate-400 uppercase">Fallback Rate</div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-1">
            {data.fallback_rate_pct.toFixed(2)}%
          </div>
          <div className="text-[10px] text-slate-400 mt-0.5">0 / 14,820 calls</div>
        </div>

        {/* Illegal Actions */}
        <div className="p-3 rounded-xl bg-white/2 border border-white/5">
          <div className="text-[10px] font-mono text-slate-400 uppercase">Illegal Actions</div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-1">
            {data.illegal_actions_count}
          </div>
          <div className="text-[10px] text-slate-400 mt-0.5">Zero violations</div>
        </div>

        {/* Unhandled Exceptions */}
        <div className="p-3 rounded-xl bg-white/2 border border-white/5">
          <div className="text-[10px] font-mono text-slate-400 uppercase">Exceptions</div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-1">
            {data.unhandled_exceptions_count}
          </div>
          <div className="text-[10px] text-slate-400 mt-0.5">Zero runtime crashes</div>
        </div>

        {/* Time Bank Margin */}
        <div className="p-3 rounded-xl bg-white/2 border border-white/5">
          <div className="text-[10px] font-mono text-slate-400 uppercase">Time Bank Left</div>
          <div className="text-xl font-bold font-mono text-cyan-300 mt-1">
            {data.timebank_remaining_sec.toFixed(0)}s
          </div>
          <div className="text-[10px] text-cyan-400 mt-0.5">600s total budget</div>
        </div>
      </div>

      {/* Memory Footprint Bar */}
      <div className="p-3.5 rounded-xl bg-white/2 border border-white/5 space-y-2">
        <div className="flex justify-between items-center text-xs">
          <span className="text-slate-300 flex items-center gap-1.5">
            <HardDrive className="w-3.5 h-3.5 text-indigo-400" />
            Process Memory (RSS)
          </span>
          <span className="font-mono text-white">
            <strong>{data.rss_memory_mb.toFixed(1)} MiB</strong> / 12,492.8 MiB ({memPercent}%)
          </span>
        </div>

        <div className="w-full h-2 rounded-full bg-white/5 overflow-hidden">
          <div
            style={{ width: `${memPercent}%` }}
            className="h-full rounded-full bg-linear-to-r from-indigo-500 to-emerald-400"
          />
        </div>
      </div>
    </div>
  );
};
