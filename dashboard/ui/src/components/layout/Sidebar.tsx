import React from 'react';
import type { ViewSuite } from '../../types';
import {
  LayoutDashboard,
  Swords,
  Film,
  BrainCircuit,
  Eye,
  Compass,
  Layers,
  AlertTriangle,
  Sliders,
  Activity,
  BookOpen,
  Presentation,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

interface SidebarProps {
  currentSuite: ViewSuite;
  onSelectSuite: (suite: ViewSuite) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

interface NavItem {
  id: ViewSuite;
  label: string;
  icon: React.ElementType;
  shortcut: string;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'overview', label: 'Command Center', icon: LayoutDashboard, shortcut: '1' },
  { id: 'arena', label: 'Live Arena', icon: Swords, shortcut: '2' },
  { id: 'replay', label: 'Replay Explorer', icon: Film, shortcut: '3' },
  { id: 'decision', label: 'Decision Explainer', icon: BrainCircuit, shortcut: '4' },
  { id: 'opponent', label: 'Opponent Intelligence', icon: Eye, shortcut: '5' },
  { id: 'meta', label: 'Meta Observatory', icon: Compass, shortcut: '6' },
  { id: 'decklab', label: 'Deck Lab & Robustness', icon: Layers, shortcut: '7' },
  { id: 'mistakes', label: 'AI Mistake Lab', icon: AlertTriangle, shortcut: '8' },
  { id: 'ablations', label: 'Ablation Studio', icon: Sliders, shortcut: '9' },
  { id: 'performance', label: 'Performance Lab', icon: Activity, shortcut: '0' },
  { id: 'research', label: 'Research Paper', icon: BookOpen, shortcut: 'R' },
  { id: 'presentation', label: '5-Min Presentation', icon: Presentation, shortcut: 'P', badge: 'PRO' },
];

export const Sidebar: React.FC<SidebarProps> = ({
  currentSuite,
  onSelectSuite,
  collapsed,
  onToggleCollapse,
}) => {
  return (
    <aside
      className={`fixed left-0 top-16 bottom-0 z-40 glass-panel border-r border-white/[0.08] transition-all duration-300 flex flex-col justify-between ${
        collapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Navigation List */}
      <div className="p-3 space-y-1 overflow-y-auto max-h-[calc(100vh-8rem)]">
        <div className={`px-2 py-1.5 text-[10px] font-mono font-bold tracking-wider text-slate-400 uppercase ${collapsed ? 'text-center' : ''}`}>
          {collapsed ? 'LAB' : 'INTELLIGENCE SUITES'}
        </div>

        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = currentSuite === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onSelectSuite(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-semibold transition-all relative group ${
                isActive
                  ? 'bg-indigo-600/20 text-white border border-indigo-500/40 shadow-lg shadow-indigo-500/10'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.04] border border-transparent'
              }`}
              title={`${item.label} (Press ${item.shortcut})`}
            >
              <Icon
                className={`w-4 h-4 flex-shrink-0 ${
                  isActive ? 'text-indigo-400' : 'text-slate-400 group-hover:text-slate-200'
                }`}
              />

              {!collapsed && (
                <>
                  <span className="flex-1 text-left truncate">{item.label}</span>
                  {item.badge && (
                    <span className="px-1.5 py-0.5 text-[9px] font-mono font-bold rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                      {item.badge}
                    </span>
                  )}
                  <span className="px-1.5 py-0.5 text-[10px] font-mono text-slate-400 rounded bg-white/[0.05]">
                    {item.shortcut}
                  </span>
                </>
              )}

              {/* Active Indicator Bar */}
              {isActive && (
                <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-5 rounded-r bg-indigo-500" />
              )}
            </button>
          );
        })}
      </div>

      {/* Collapse Footer Toggle */}
      <div className="p-3 border-t border-white/[0.08] flex items-center justify-between">
        {!collapsed && (
          <div className="text-[11px] font-mono text-slate-400">
            Kaggle CABT Runtime
          </div>
        )}
        <button
          onClick={onToggleCollapse}
          className="p-1.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] text-slate-400 hover:text-white transition-colors"
          title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>
    </aside>
  );
};
