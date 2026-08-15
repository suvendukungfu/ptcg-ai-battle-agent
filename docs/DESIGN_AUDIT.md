# PTCG // NEXUS — Comprehensive Product & Design Audit

**Role**: Senior Product Designer + Figma Design Systems Lead + Principal Frontend Engineer + Game UI/UX Designer  
**Product**: `PTCG // NEXUS` — *Autonomous Game Intelligence Platform*  
**Date**: August 15, 2026

---

## 1. Current Visual Architecture

### 1.1 Structural Foundations
- **Base Layout**: Fullscreen web application utilizing React 19 + TypeScript + Vite 8.2 + Tailwind CSS v4.
- **Color Model**: Obsidian void (`#030509`, `#080C14`) paired with Electric Yellow (`#FACC15`) primary tactical highlights and restrained energy type accents (Lightning `#EAB308`, Fire `#EF4444`, Grass `#10B981`, Water `#3B82F6`, Psychic `#A855F7`).
- **Active Navigation**: Left vertical navigation rail routing between 12 specialized platform views (`overview`, `arena`, `replay`, `decision`, `opponent`, `meta`, `decklab`, `mistakes`, `ablations`, `performance`, `research`, `presentation`).

### 1.2 Data Pipeline & Real Endpoints
1. `GET /api/status`: Verified agent telemetry (Elo: 1684.5, Meta Win Rate: 68.2%, P95 Latency: 2.665 ms, 0 fallbacks, 0 illegal moves).
2. `POST /api/simulate`: Live headless game simulation execution invoking `main.agent` against opponent bots and streaming turn-by-turn state step replays.
3. `GET /api/trends`: Elo progression series, Wilson 95% confidence intervals, and latency percentiles.
4. `GET /api/beliefs`: Bayesian hypergeometric probability distributions ($P(\text{Boss})$, $P(\text{Energy})$, $P(\text{Evolution})$, $P(\text{Switch})$) and inferred opponent archetypes.
5. `GET /api/matchup-matrix`: Pairwise empirical matrix across 6 archetypes.
6. `GET /api/ablations`: Empirical isolated contribution benchmark metrics for Variants A through F.
7. `GET /api/mistakes`: Forensic blunder mining records extracted from loss replays.
8. `GET /api/codex`: Permitted 60-card tournament deck registry with verified metadata from `data/EN Card Data.csv`.

---

## 2. Current UX Problems & Aesthetic Residue

1. **"Everything is a Box/Card" Problem**: Too much reliance on enclosed rectangular panels with repetitive borders, padding, and subtle shadows. Important data should breathe with typographic hierarchy, section dividers, negative space, and open editorial structure rather than being imprisoned in cards.
2. **Landing Page Game Disconnect**: The landing page currently has too much empty black space and developer-oriented metric blocks instead of immediately introducing the **tactical physical Pokémon TCG battle interface**.
3. **Information Density & Top Bar Overcrowding**: The top header displays too many permanent metrics simultaneously (Elo, Win Rate, Latency, Fallback, Deck, Operational status), which should be contextualized per view.
4. **Card Physicality & Scale**: Pokémon cards on the battlefield need authentic physical depth, micro-tilt perspective (2–4°), high-contrast active highlights, and crisp energy tokens without cartoonish AI glow.
5. **AI Explanation Dominance**: The AI explanation trace currently occupies too much vertical space; it must be an elegant, horizontal intelligence vector that frames the active battlefield without overshadowing it.

---

## 3. Component Taxonomy & Audit

### 3.1 Components to Preserve
- **API Client & State Layers** (`dashboard/ui/src/services/api.ts`): Clean typed fetch client connecting to FastAPI.
- **Card Data Mapping Engine** (`dashboard/ui/src/services/cardRegistry.ts`): Verified mapping from official `EN Card Data.csv` card IDs to high-resolution assets from `images.pokemontcg.io`.
- **Matchup Matrix & Meta Shifter Engine** (`MetaObservatoryView.tsx`): Empirical $N \times N$ matrix and dynamic population calculator ($E[V(D)] = \sum w_i \cdot \text{WR}_i$).
- **Loss Forensic Mining Engine** (`LossForensicsPanel.tsx`): Turning-point blunder detector with before/after win probability shifts.

### 3.2 Components to Redesign
- **`<LandingHero />`**: Completely rebuild around the physical Pokémon TCG battlefield. Replace the abstract canvas with real card objects in active combat configuration.
- **`<LiveArenaView />` / `<LiveBattlefield />`**: Redesign into an esports-grade tactical digital arena with dominating active Pokémon slots, physical bench positions, authentic prize stacks, and a streamlined horizontal decision trace.
- **`<PokemonCard />`**: Upgrade to physical card object feel (subtle perspective, authentic card aspect ratio, crisp typography, clean energy counters, zero AI glow).
- **Navigation & TopBar**: Replace dense metric lists with clean contextual headers and a sleek left navigation rail.

### 3.3 New Reusable Design System Components (`src/design/`)
- `tokens.ts`: Strict 4px base spacing, elevation, colors, and motion durations.
- `typography.ts`: Display (*Space Grotesk*), UI Body (*Plus Jakarta Sans*), and Telemetry HUD (*JetBrains Mono*).
- `<PokemonCard />`: Universal physical game card component with 6 distinct variants (`battle`, `bench`, `standard`, `compact`, `codex`, `preview`).
- `<Battlefield />` & `<BattleSlot />`: Asymmetric esports battle arena with active and benched card drop zones.
- `<DecisionLens />`: Compact horizontal intelligence vector (`STATE → GOAL → OPTIONS → RISK → SEARCH → DECISION`).
- `<ReplayTimeline />`: Scrubber bar with key turn markers and instant state rewind.

---

## 4. Card Asset Availability & Dataset Mapping

From `data/EN Card Data.csv` (1,269 official cards), all tournament deck cards and opponent archetypes map to verified official card artwork:
- **Bellibolt ex** (`#723`): Stage 1, 350 HP, Lightning, Electro Bullet 160 dmg (`sv3/79_hires.png`).
- **Bellibolt** (`#722`): Stage 1, 140 HP, Lightning, Thunderbolt 140 dmg (`sv1/78_hires.png`).
- **Tadbulb** (`#721`): Basic, 70 HP, Lightning (`sv1/77_hires.png`).
- **Crustle** (`#345`): Stage 1, 150 HP, Grass, *Mysterious Rock Inn* Safeguard (`sv1/6_hires.png`).
- **Dwebble** (`#344`): Basic, 70 HP, Grass (`sv1/5_hires.png`).
- **Alakazam** (`#743`): Stage 2, 140 HP, Psychic, *Psychic Draw* (`sv1/107_hires.png`).
- **Kadabra** (`#742`): Stage 1, 80 HP, Psychic (`sv1/106_hires.png`).
- **Abra** (`#741`): Basic, 50 HP, Psychic (`sv1/105_hires.png`).
- **Trainers**: Electric Generator (`#1219`), Boss's Orders (`#1262`), Professor's Research (`#1092`), Ultra Ball (`#1121`), Nest Ball (`#1227`), Switch (`#1145`), Heavy Baton (`#1163`).
- **Energies**: Basic Lightning (`#3`, `#4`), Basic Grass (`#1`), Basic Psychic (`#5`).

---

## 5. Proposed Design System & Implementation Plan

### Step 1: Design Tokens (`src/design/tokens.ts`, `src/design/colors.ts`, `src/design/typography.ts`, `src/design/spacing.ts`)
- Strict 4px base spacing: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px.
- Reduced radii: 2px, 4px, 6px, 8px (avoid huge pill cards).
- Flat, open editorial layouts with thin rules (`1px solid rgba(255,255,255,0.06)`).

### Step 2: Physical `<PokemonCard />` & `<BattleSlot />` Component
- Physical proportions (width:height ~ 1:1.4), subtle perspective, crisp type, live HP bars, and energy badges.

### Step 3: Tactical Digital Battlefield (`/battle`)
- Central hero experience with physical active clash, bench slots, prize stacks, and streamlined decision trace.

### Step 4: Redesigned Landing Page
- Cinematic TCG-inspired hero: Title + Subtitle + Live Card Battle Visual + Three core pillars (Belief, Search, Adaptation) + Live performance metrics.

### Step 5: Visual QA Across Resolutions
- Test at 390px, 768px, 1280px, 1440px, and 1920px.
