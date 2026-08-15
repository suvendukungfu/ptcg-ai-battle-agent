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

interface NavGroup {
  label: string;
  items: Array<{
    id: ViewSuite;
    label: string;
    icon: React.ElementType;
    shortcut: string;
  }>;
}

const NAV_GROUPS: NavGroup[] = [
  {
    label: 'INTELLIGENCE',
    items: [
      { id: 'overview', label: 'NEXUS', icon: LayoutDashboard, shortcut: '1' },
      { id: 'arena', label: 'Battle Arena', icon: Swords, shortcut: '2' },
      { id: 'replay', label: 'Replay Forensics', icon: Film, shortcut: '3' },
      { id: 'decision', label: 'Decision Lens', icon: BrainCircuit, shortcut: '4' },
      { id: 'opponent', label: 'Opponent Intel', icon: Eye, shortcut: '5' },
    ],
  },
  {
    label: 'RESEARCH & META',
    items: [
      { id: 'meta', label: 'Meta Observatory', icon: Compass, shortcut: '6' },
      { id: 'decklab', label: 'Deck Lab (60)', icon: Layers, shortcut: '7' },
      { id: 'mistakes', label: 'Loss Forensics', icon: AlertTriangle, shortcut: '8' },
      { id: 'ablations', label: 'Ablations (A–F)', icon: Sliders, shortcut: '9' },
      { id: 'performance', label: 'Telemetry Lab', icon: Activity, shortcut: '0' },
      { id: 'research', label: 'Research Paper', icon: BookOpen, shortcut: 'R' },
      { id: 'presentation', label: 'Executive Deck', icon: Presentation, shortcut: 'P' },
    ],
  },
];

export const Sidebar: React.FC<SidebarProps> = ({
  currentSuite,
  onSelectSuite,
  collapsed,
  onToggleCollapse,
}) => {
  return (
    <aside
      className={`fixed left-0 top-14 bottom-0 z-40 bg-[#07080B] border-r border-white/6 transition-all duration-200 flex flex-col justify-between select-none ${
        collapsed ? 'w-14' : 'w-56'
      }`}
    >
      {/* Navigation Groups */}
      <div className="p-2 space-y-4 overflow-y-auto">
        {NAV_GROUPS.map((group) => (
          <div key={group.label} className="space-y-0.5">
            {!collapsed && (
              <div className="px-3 py-1 text-[10px] font-mono font-bold tracking-widest text-slate-500 uppercase">
                {group.label}
              </div>
            )}

            {group.items.map((item) => {
              const Icon = item.icon;
              const isActive = currentSuite === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => onSelectSuite(item.id)}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xs text-xs font-mono transition-colors relative group cursor-pointer ${
                    isActive
                      ? 'bg-white/4 text-white font-bold'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-white/2'
                  }`}
                  title={`${item.label} (Press ${item.shortcut})`}
                >
                  <Icon
                    className={`w-3.5 h-3.5 shrink-0 ${
                      isActive ? 'text-amber-400' : 'text-slate-400 group-hover:text-slate-200'
                    }`}
                  />

                  {!collapsed && (
                    <>
                      <span className="flex-1 text-left truncate tracking-tight">{item.label}</span>
                      <span className="text-[10px] text-slate-400 opacity-60">
                        {item.shortcut}
                      </span>
                    </>
                  )}

                  {/* Clean thin Electric Yellow selected bar */}
                  {isActive && (
                    <span className="absolute left-0 top-1 bottom-1 w-0.5 bg-amber-400 rounded-r-xs" />
                  )}
                </button>
              );
            })}
          </div>
        ))}
      </div>

      {/* Collapse Footer Toggle */}
      <div className="p-2 border-t border-white/6 flex items-center justify-between font-mono text-[10px]">
        {!collapsed && (
          <div className="text-slate-400 px-2">
            PTCG // NEXUS V3.0
          </div>
        )}
        <button
          onClick={onToggleCollapse}
          className="p-1 rounded-xs hover:bg-white/4 text-slate-400 hover:text-white transition-colors cursor-pointer"
          title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {collapsed ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
