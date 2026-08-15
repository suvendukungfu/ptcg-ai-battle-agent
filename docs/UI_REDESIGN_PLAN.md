# PTCG // NEXUS — Comprehensive UI Redesign & Product Architecture Plan

**Product Name**: `PTCG // NEXUS`  
**Subtitle**: *Autonomous Game Intelligence*  
**Role**: Lead Product Designer + Principal Frontend Engineer + Motion Designer + Data Visualization Engineer + Game UI Designer  
**Target Platform**: The Pokémon Company — PTCG AI Battle Challenge Simulation  
**Date**: August 15, 2026

---

## 1. Current UI Architecture & Forensic Inspection

### 1.1 Active Components & Directory Tree
- **Active Frontend Entry Point**: `dashboard/ui/src/main.tsx` $\to$ `dashboard/ui/src/App.tsx` (Vite 8.2 + React 19 + TypeScript).
- **Active Backend API Server**: `dashboard/backend/app.py` (FastAPI + Uvicorn on `http://0.0.0.0:8000`, serving `/api/*` endpoints and static bundle from `dashboard/frontend/`).
- **Production Build Target**: `dashboard/frontend/` (built via `npm run build` from `dashboard/ui/`).
- **Unused/Legacy Frontend**: `tools/web_app.py` (standalone single-file prototype, preserved for reference).

### 1.2 Active Real Data Sources & Endpoints
1. `GET /api/status`: Real-time agent metadata (Elo: 1684.5, Win Rate: 68.2%, P95 latency: 2.665 ms, 0 fallbacks, 0 invalids).
2. `GET /api/trends`: Elo progression series, Wilson 95% confidence intervals across match counts, and microsecond latency component percentiles.
3. `GET /api/beliefs`: Bayesian hypergeometric probability distributions ($P(\text{Boss})$, $P(\text{Energy})$, $P(\text{Evolution})$, $P(\text{Switch})$) and inferred opponent archetypes.
4. `GET /api/matchup-matrix`: Pairwise empirical matrix with Wilson 95% score bounds across 6 archetypes.
5. `GET /api/ablations`: Empirical isolated contribution benchmark metrics for Variants A through F.
6. `GET /api/mistakes`: Forensic blunder mining records extracted from loss replays.
7. `GET /api/codex`: Permitted 60-card deck registry with verified metadata from `data/EN Card Data.csv` and high-resolution official asset mappings.
8. `POST /api/simulate`: Live headless game simulation execution invoking `main.agent` against opponent bots.

---

## 2. Current Problems & Design Gaps

1. **Generic Aesthetic Residue**: Too much reliance on standard indigo/purple tech accents and floating blur cards, making it feel closer to SaaS than an esports tactical command center.
2. **Missing Authentic Card Physicality**: While card slots exist, they lack physical depth, micro-tilt perspective, authentic energy type badges, and high-fidelity game object presence.
3. **Typography Flattening**: Standard sans-serif font throughout creates flat hierarchy without strong editorial display or crisp military HUD telemetry contrast.
4. **Information Hierarchy in Battle Arena**: The active clash should be visually commanding with immediate tactical priority, rather than occupying symmetrical card blocks.
5. **Brand Identity**: Needs transition to the bold, human-designed `PTCG // NEXUS` identity with dark obsidian surfaces and Electric Yellow primary tactical highlights.

---

## 3. Proposed Visual Language

The visual identity fuses **Competitive Esports + High-End Tactical Game HUDs + Japanese UI Precision + Future Mission Control**.

- **Surfaces**: Deep void (`#030509`), Obsidian (`#080C14`), Graphite (`#0F1626`), Smoke (`#182238`).
- **Tactical Primary Accent**: **Electric Yellow** (`#FACC15` / `#FFE600`), representing active tactical decision vectors and critical priority plays.
- **Energy Type Accents** (used with strict restraint):
  - ⚡ *Lightning*: `#EAB308` (Selected AI action / Acceleration)
  - 🔥 *Fire*: `#EF4444` (Offensive lethal threat)
  - 💧 *Water*: `#3B82F6` (Defensive barrier)
  - 🌿 *Grass*: `#10B981` (Recovery / Setup)
  - 👁️ *Psychic*: `#A855F7` (Bayesian prediction / Beliefs)
  - 🥊 *Fighting*: `#F97316` (Direct incoming combat damage)
  - 🌑 *Darkness*: `#64748B` (Opponent risk / Unseen hand)
  - ⚙️ *Metal*: `#94A3B8` (System health & telemetry)
  - ⚪ *Colorless*: `#E2E8F0` (Neutral baseline)
- **Materials**: 1px technical hair-lines (`rgba(255, 255, 255, 0.08)`), subtle micro-grain texture, 0.5px scanline grid, non-distracting specular reflections.

---

## 4. Typography System

| Role | Font Family | Weight / Style | Usage |
|---|---|---|---|
| **Display** | `'Space Grotesk'`, `'Plus Jakarta Sans'`, sans-serif | 800 / 900 Black | `PTCG // NEXUS`, major suite headings, match result headers |
| **Body** | `'Plus Jakarta Sans'`, `'Inter'`, sans-serif | 400 / 500 Medium | Descriptions, card roles, tactical rationale, documentation |
| **Telemetry / HUD** | `'JetBrains Mono'`, monospace | 500 / 700 Bold | `AGENT // V3.0`, `LATENCY // 2.66ms`, coordinates, probabilities |

---

## 5. Color System & Design Tokens (`design-tokens.css`)

```css
:root {
  /* Base Backgrounds */
  --nexus-bg-void: #030509;
  --nexus-bg-obsidian: #080c14;
  --nexus-bg-graphite: #0f1626;
  --nexus-bg-smoke: #182238;

  /* Typography */
  --nexus-text-primary: #f8fafc;
  --nexus-text-secondary: #94a3b8;
  --nexus-text-muted: #475569;

  /* Primary Tactical Accent */
  --nexus-electric-yellow: #facc15;
  --nexus-electric-glow: rgba(250, 204, 21, 0.35);

  /* Energy Accents */
  --nexus-energy-lightning: #eab308;
  --nexus-energy-fire: #ef4444;
  --nexus-energy-water: #3b82f6;
  --nexus-energy-grass: #10b981;
  --nexus-energy-psychic: #a855f7;
  --nexus-energy-fighting: #f97316;
  --nexus-energy-darkness: #64748b;
  --nexus-energy-metal: #94a3b8;

  /* UI Status */
  --nexus-status-optimal: #10b981;
  --nexus-status-warning: #f59e0b;
  --nexus-status-critical: #f43f5e;
  --nexus-border-subtle: rgba(255, 255, 255, 0.08);
  --nexus-border-tactical: rgba(250, 204, 21, 0.4);
}
```

---

## 6. Component System Architecture

1. `<PokemonCard />`: Universal physical game card object (variants: `battle-active`, `battle-bench`, `codex`, `thumbnail`, `compact`). Features real artwork from `images.pokemontcg.io`, foil shimmer, energy badges, HP gauges, and status badges.
2. `<BattleField />`: Asymmetric 3D perspective battle arena featuring dominating active Pokémon slots, compact benched cards, 6-slot prize tokens, and interactive energy particle trajectories.
3. `<DecisionNodeGraph />`: 2-ply search lookahead graph visualizing candidate moves, opponent retaliation threats, and leaf values.
4. `<TacticalOverlay />`: Compact AI decision breakdown showing $W_{\text{win}}, W_{\text{prize}}, W_{\text{board}}, W_{\text{energy}}, -W_{\text{retaliation}}$.
5. `<MomentumScrubber />`: Interactive SVG replay timeline with prize differential curve and blunder flags.
6. `<HypergeometricGauge />`: Bayesian belief dial with exact mathematical formulas and probability envelopes.
7. `<MetaHeatmap />`: Interactive $N \times N$ matrix with Wilson 95% confidence intervals and real-time Meta Shifter sliders.

---

## 7. Page Architecture & Route Mapping

- **Hero Landing (`/`)**: High-impact introductory arena, live Elo leaderboard readout, Enter Battle and Explore AI triggers.
- **NEXUS Command (`overview`)**: Asymmetric command center featuring live battlefield preview, active agent status, performance trends, and dynamic meta radar.
- **Battle Arena (`arena`)**: Fullscreen tactical battle twin with step execution, combat feed, and live simulation triggers.
- **Replay Explorer (`replay`)**: Post-game forensic scrubber with prize curve and event stream.
- **Decision Space (`decision`)**: Full lookahead search tree and counterfactual sandbox.
- **Opponent Intel (`opponent`)**: Real-time Bayesian probability gauges and archetype prediction.
- **Meta Observatory (`meta`)**: Matchup matrix heatmap and ladder population simulator.
- **Deck Laboratory (`decklab`)**: 60-card interactive codex and hypergeometric opening hand calculator.
- **Mistake Lab (`mistakes`)**: Mined blunder catalog and verified patch recommendations.
- **Ablation Studio (`ablations`)**: Empirical component attribution (Variants A through F).
- **Performance Lab (`performance`)**: Microsecond telemetry, memory footprint, and timebank margin.
- **Research Paper (`research`)**: Academic journal format with LaTeX equations and citations.
- **Executive Deck (`presentation`)**: 5-minute interactive presentation slide deck.

---

## 8. Card Asset & Image Strategy

- Direct mapping from card ID to official high-resolution tournament card art from `images.pokemontcg.io`.
- Client-side lazy-loading with graceful CSS SVG skeleton fallbacks.
- WebP/compressed formats to ensure zero initial page load lag.

---

## 9. Implementation Roadmap

- **PHASE 1**: Forensic UI Audit & Architectural Blueprint (`docs/UI_REDESIGN_PLAN.md`) — **[ACTIVE]**
- **PHASE 2**: Design Tokens, Fonts & Tactical CSS Variables (`design-tokens.css`, `index.css`, `index.html`) — **[ACTIVE]**
- **PHASE 3**: Reusable Game Objects (`<PokemonCard />`, `<EnergyBadge />`, `<PrizeBar />`).
- **PHASE 4**: Live Battlefield & 3D Combat Zone.
- **PHASE 5**: Decision Trace & Counterfactual Node Graph.
- **PHASE 6**: Replay & Mistake Forensic Labs.
- **PHASE 7**: Meta Map & Deck Laboratory.
- **PHASE 8**: Micro-interactions, Motion, and Visual QA.
