# Dashboard & Web Architecture: PTCG AI Command Center

**Status**: FORENSIC AUDIT COMPLETE  
**Technology Stack**: FastAPI (Backend) + React 19 / TypeScript / Vite / Tailwind CSS v4 (Frontend)

---

## 1. Directory Structure & Asset Flow

```text
dashboard/
├── backend/
│   └── app.py                  # FastAPI REST server & static mount (Port 8000)
├── ui/                         # React 19 + TypeScript + Vite + Tailwind source code
│   ├── src/
│   │   ├── components/
│   │   │   ├── landing/        # Cinematic Hero & LiveMiniGameCanvas
│   │   │   ├── layout/         # TopBar telemetry & Collapsible Sidebar
│   │   │   └── views/          # Intelligence suites (CommandCenterView, etc.)
│   │   ├── services/api.ts     # Typed fetch client connecting to /api/*
│   │   ├── types/index.ts      # TypeScript interfaces
│   │   ├── App.tsx             # Root layout controller & keyboard shortcut dispatcher
│   │   └── index.css           # Aerospace / Dark Lab design system & utility classes
│   ├── package.json            # Node.js dependencies (React 19, Lucide, Tailwind v4)
│   └── vite.config.ts          # Build pipeline configured to output to ../frontend
└── frontend/                   # Compiled production static bundle (HTML, JS, CSS)
    ├── index.html
    └── assets/
        ├── index-BBDRr70M.js   # 251 KB (74 KB gzip)
        └── index-BJp-rSAp.css   # 45 KB (7.8 KB gzip)
```

---

## 2. API Endpoint Registry (`dashboard/backend/app.py`)

| Endpoint | Method | Response Payload Description | Data Source |
|---|---|---|---|
| `/api/status` | `GET` | Agent specs, version, best Elo, win rate, average/P95 latency, active models | Live Diagnostics & Registry |
| `/api/trends` | `GET` | Elo progression, win rate with Wilson 95% bounds, component latency breakdown, meta radar, system health | Empirical Benchmark Engine |
| `/api/beliefs` | `GET` | Current Bayesian belief probabilities ($P(\text{Gust}), P(\text{Energy}), P(\text{Switch})$), inferred opponent goal | `BeliefStateTracker` |
| `/api/mistakes` | `GET` | Catalog of detected blunders, missed lethal opportunities, and severity counts | `MistakeDatabase` |
| `/api/meta-prediction` | `GET` | Ranked deck evaluations with expected win rates and worst-case robustness scores | `MetaPredictor` |
| `/api/matchup-matrix` | `GET` | Pairwise win-rate matrix across top ladder archetypes | Local Tournament Engine |
| `/api/ablations` | `GET` | Performance matrix across ablation variants (Evaluator, Search, Opponent Model, Full) | `ABLATION_VARIANTS` Registry |
| `/api/codex` | `GET` | Complete 60-card metadata codex with roles, descriptions, and AI priority tags | `get_all_cards()` / Database |
| `/api/simulate` | `POST` | Full interactive simulation match returning turn-by-turn replay steps and decisions | `cabt.run([p0, p1])` |
| `/api/benchmark` | `POST` | Executes real-time $N$-game headless tournament and returns measured latency/win rates | Live Benchmark Runner |

---

## 3. Real vs Simulated Data Differentiation

- **Real Empirical Data**:
  - Live agent decision latency (P50, P95, P99, Max measured in milliseconds).
  - Decision count and 0.00% fallback rate from live Python diagnostic counters.
  - 60-card deck composition and card mechanics parsed directly from `deck.csv` and card data.
  - Headless match outcomes and win rates measured through the official `kaggle_environments` engine.
- **Simulated / Meta Model Data**:
  - Meta archetype shares and threat levels are projections calculated by `MetaPredictor` over tournament ladder simulations.
  - Bayesian belief distributions are computed online using hypergeometric statistics over hidden information.
