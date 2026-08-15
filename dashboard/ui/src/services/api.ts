import type {
  AgentStatus,
  BeliefData,
  MistakeSummary,
  MetaDeckRanking,
  MatchupMatrixData,
  AblationVariant,
  BenchmarkMetrics,
  CardCodexItem,
  PerformanceTrends
} from '../types';

const API_BASE = '/api';

export const api = {
  async getStatus(): Promise<AgentStatus> {
    const res = await fetch(`${API_BASE}/status`);
    if (!res.ok) throw new Error('Failed to fetch status');
    return res.json();
  },

  async getTrends(): Promise<PerformanceTrends> {
    const res = await fetch(`${API_BASE}/trends`);
    if (!res.ok) throw new Error('Failed to fetch trends');
    return res.json();
  },

  async getBeliefs(): Promise<BeliefData> {
    const res = await fetch(`${API_BASE}/beliefs`);
    if (!res.ok) throw new Error('Failed to fetch beliefs');
    return res.json();
  },

  async getMistakes(): Promise<MistakeSummary> {
    const res = await fetch(`${API_BASE}/mistakes`);
    if (!res.ok) throw new Error('Failed to fetch mistakes');
    return res.json();
  },

  async getMetaPredictions(): Promise<MetaDeckRanking[]> {
    const res = await fetch(`${API_BASE}/meta-prediction`);
    if (!res.ok) throw new Error('Failed to fetch meta predictions');
    return res.json();
  },

  async getMatchupMatrix(): Promise<MatchupMatrixData> {
    const res = await fetch(`${API_BASE}/matchup-matrix`);
    if (!res.ok) throw new Error('Failed to fetch matchup matrix');
    return res.json();
  },

  async getAblations(): Promise<AblationVariant[]> {
    const res = await fetch(`${API_BASE}/ablations`);
    if (!res.ok) throw new Error('Failed to fetch ablations');
    return res.json();
  },

  async getCodex(): Promise<CardCodexItem[]> {
    const res = await fetch(`${API_BASE}/codex`);
    if (!res.ok) throw new Error('Failed to fetch codex');
    return res.json();
  },

  async runBenchmark(games: number = 10): Promise<BenchmarkMetrics> {
    const res = await fetch(`${API_BASE}/benchmark`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ games }),
    });
    if (!res.ok) throw new Error('Failed to execute benchmark');
    return res.json();
  },

  async simulateBattle(p0: string = 'production_v2', opponent: string = 'random'): Promise<any> {
    const res = await fetch(`${API_BASE}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ p0_agent: p0, opponent }),
    });
    if (!res.ok) throw new Error('Failed to simulate battle');
    return res.json();
  }
};
