import React, { useState, useEffect, useCallback } from 'react';
import type { ViewSuite, AgentStatus, BeliefData, MistakeSummary, MetaDeckRanking } from './types';
import { api } from './services/api';
import { TopBar } from './components/layout/TopBar';
import { Sidebar } from './components/layout/Sidebar';
import { LandingHero } from './components/landing/LandingHero';
import { CommandCenterView } from './components/views/CommandCenterView';

export const App: React.FC = () => {
  const [isLanding, setIsLanding] = useState<boolean>(true);
  const [currentSuite, setCurrentSuite] = useState<ViewSuite>('overview');
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);

  const [status, setStatus] = useState<AgentStatus | null>(null);
  const [beliefs, setBeliefs] = useState<BeliefData | null>(null);
  const [mistakes, setMistakes] = useState<MistakeSummary | null>(null);
  const [metaRankings, setMetaRankings] = useState<MetaDeckRanking[]>([]);

  // Load telemetry data from FastAPI backend
  const loadData = useCallback(async () => {
    try {
      const [statusRes, beliefsRes, mistakesRes, metaRes] = await Promise.allSettled([
        api.getStatus(),
        api.getBeliefs(),
        api.getMistakes(),
        api.getMetaPredictions(),
      ]);

      if (statusRes.status === 'fulfilled') setStatus(statusRes.value);
      if (beliefsRes.status === 'fulfilled') setBeliefs(beliefsRes.value);
      if (mistakesRes.status === 'fulfilled') setMistakes(mistakesRes.value);
      if (metaRes.status === 'fulfilled') setMetaRankings(metaRes.value);
    } catch (err) {
      console.warn('Could not load telemetry data:', err);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Global Keyboard Shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) {
        return;
      }

      if (e.key === 'Escape') {
        setIsLanding(true);
        return;
      }

      const keyMap: Record<string, ViewSuite> = {
        '1': 'overview',
        '2': 'arena',
        '3': 'replay',
        '4': 'decision',
        '5': 'opponent',
        '6': 'meta',
        '7': 'decklab',
        '8': 'mistakes',
        '9': 'ablations',
        '0': 'performance',
        'r': 'research',
        'R': 'research',
        'p': 'presentation',
        'P': 'presentation',
      };

      if (keyMap[e.key]) {
        setCurrentSuite(keyMap[e.key]);
        setIsLanding(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSelectSuite = (suite: ViewSuite) => {
    setCurrentSuite(suite);
    setIsLanding(false);
  };

  return (
    <div className="min-h-screen bg-[#05070d] text-slate-100 flex flex-col font-sans">
      {/* Top Telemetry Header */}
      <TopBar
        status={status}
        isLanding={isLanding}
        onToggleLanding={() => setIsLanding((prev) => !prev)}
        onRefresh={loadData}
      />

      {/* Main App Canvas */}
      {isLanding ? (
        <main className="flex-1">
          <LandingHero
            status={status}
            onEnterCommandCenter={() => {
              setCurrentSuite('overview');
              setIsLanding(false);
            }}
            onExploreAI={() => {
              setCurrentSuite('decision');
              setIsLanding(false);
            }}
          />
        </main>
      ) : (
        <div className="flex-1 flex">
          {/* Left Aerospace Sidebar */}
          <Sidebar
            currentSuite={currentSuite}
            onSelectSuite={handleSelectSuite}
            collapsed={sidebarCollapsed}
            onToggleCollapse={() => setSidebarCollapsed((prev) => !prev)}
          />

          {/* Main Suite Viewport */}
          <main
            className={`flex-1 p-4 md:p-8 transition-all duration-300 ${
              sidebarCollapsed ? 'ml-16' : 'ml-64'
            } max-w-7xl`}
          >
            {currentSuite === 'overview' && (
              <CommandCenterView
                status={status}
                beliefs={beliefs}
                mistakes={mistakes}
                metaRankings={metaRankings}
                onNavigate={handleSelectSuite}
              />
            )}

            {currentSuite !== 'overview' && (
              <div className="glass-panel p-8 rounded-2xl border border-white/[0.08] text-center space-y-4">
                <div className="text-xs font-mono font-bold text-indigo-400 uppercase tracking-wider">
                  Suite Initialized (Stage 1 Complete)
                </div>
                <h2 className="text-2xl font-black text-white capitalize">
                  {currentSuite.replace('-', ' ')} Suite Ready
                </h2>
                <p className="text-sm text-slate-400 max-w-lg mx-auto">
                  Stage 1 Design System, TopBar, Sidebar, and Command Center Shell are active.
                  Proceeding to next stage modules.
                </p>
                <button
                  onClick={() => setCurrentSuite('overview')}
                  className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-colors"
                >
                  Return to Command Center
                </button>
              </div>
            )}
          </main>
        </div>
      )}
    </div>
  );
};

export default App;
