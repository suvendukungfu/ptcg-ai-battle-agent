export interface AgentStatus {
  status: string;
  agent_name: string;
  version: string;
  best_elo: number;
  win_rate_meta: number;
  avg_decision_time_ms: number;
  p95_latency_ms: number;
  p99_latency_ms: number;
  fallback_rate_pct: number;
  total_decisions: number;
  deck_name: string;
  deck_archetype: string;
  active_models: string[];
  diagnostics: Record<string, any>;
}

export interface BeliefData {
  gust_probability: number;
  energy_probability: number;
  switch_probability: number;
  evolution_probability: number;
  supporter_probability: number;
  opponent_archetype: string;
  threat_level: string;
  inferred_goal: string;
}

export interface MistakeSummary {
  total_mistakes_mined: number;
  breakdown: {
    CRITICAL_MISTAKE: number;
    MISSED_OPPORTUNITY: number;
    TACTICAL_MISTAKE: number;
    RESOURCE_MISTAKE: number;
    STRATEGIC_MISTAKE: number;
  };
  recent_mistakes: Array<{
    game_id: string;
    turn: number;
    step: number;
    category: string;
    severity: string;
    chosen_action_desc: string;
    optimal_action_desc: string;
    score_delta: number;
    explanation: string;
  }>;
}

export interface MetaDeckRanking {
  deck_name: string;
  expected_win_rate: number;
  robustness_score: number;
  min_matchup_win_rate: number;
  max_matchup_win_rate: number;
  variance: number;
  confidence_interval_95: [number, number];
  recommended_tier: string;
  rationale: string;
}

export interface MatchupMatrixData {
  archetypes: string[];
  data: Array<{
    name: string;
    [key: string]: any;
  }>;
}

export interface AblationVariant {
  variant: string;
  elo: number;
  win_rate: number;
  latency_ms: number;
  fallback_rate: number;
  description: string;
  advantage: string;
  bottleneck: string;
}

export interface BenchmarkMetrics {
  games_evaluated: number;
  total_steps: number;
  win_rate_pct: number;
  latency_avg_ms: number;
  latency_p50_ms: number;
  latency_p95_ms: number;
  latency_p99_ms: number;
  latency_max_ms: number;
  throughput_decisions_per_sec: number;
  memory_end_mb: number;
  fallback_rate_pct: number;
}

export interface CardCodexItem {
  id: number;
  name: string;
  category: string;
  type: string;
  element: string;
  hp: number;
  damage: number;
  retreat: number;
  copies: number;
  role: string;
  description: string;
  ai_priority: string;
  img: string;
}

export interface PerformanceTrends {
  elo_progression: Array<{ match: number; elo: number }>;
  win_rate_trend: Array<{ games: number; win_rate: number; ci_lower: number; ci_upper: number }>;
  latency_breakdown: {
    state_parsing_ms: number;
    belief_update_ms: number;
    goal_planning_ms: number;
    candidate_generation_ms: number;
    search_and_eval_ms: number;
    fallback_check_ms: number;
    total_avg_ms: number;
    p50_ms: number;
    p95_ms: number;
    p99_ms: number;
    max_ms: number;
  };
  meta_radar: Array<{
    archetype: string;
    share: number;
    trend: string;
    threat: string;
    color: string;
  }>;
  system_health: {
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

export type ViewSuite =

  | 'overview'
  | 'arena'
  | 'replay'
  | 'decision'
  | 'opponent'
  | 'meta'
  | 'decklab'
  | 'mistakes'
  | 'experiments'
  | 'ablations'
  | 'performance'
  | 'research'
  | 'presentation';
