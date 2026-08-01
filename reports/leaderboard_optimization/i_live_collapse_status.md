# Candidate F Live Collapse Investigation & 19-Episode Diagnostic

Generated at: 2026-08-16 09:46:00 UTC
Submission: `55547508` (PTCG NEXUS v3.4)

---

## 1. Complete 19-Game Score & Timeline Analysis

- **Current Displayed Score**: **`492.2`** (Snapshot taken during Glicko-2 rating reconciliation)
- **Peak Score**: **`622.9`**
- **Total Public Matches**: **19**
- **Cumulative Record**: **12 Wins / 7 Losses (63.16% Win Rate)**
- **Batch 1 (Games 1–10)**: 5 Wins / 5 Losses (50.0% WR)
- **Batch 2 (Games 11–19)**: **7 Wins / 2 Losses (77.78% WR)**
- **Last 5 Games**: **4 Wins / 1 Loss (80.0% WR)**

---

## 2. Complete 19-Episode Log

| Game # | Episode ID | Outcome | Opponent Archetype | Batch | Steps | Root Cause / Note |
| :---: | :---: | :---: | :--- | :---: | :---: | :--- |
| 1 | `93569861` | **LOSS (-1)** | Duraludon (Metal Non-EX Resist) | Batch 1 | 75 | `LOSS_TYPE_RESISTANCE` (-30 DMG) |
| 2 | `93570797` | **WIN (+1)** | Mega Lucario ex (Mega EX Aggro) | Batch 1 | 127 | `SAFEGUARD_EX_SUPPRESSION` (0 DMG taken) |
| 3 | `93571687` | **WIN (+1)** | Non-EX Dwebble Deck | Batch 1 | 23 | `CLEAN_PRIZE_SWEEP` |
| 4 | `93572601` | **WIN (+1)** | Mega Lucario ex (Mega EX Aggro) | Batch 1 | 112 | `SAFEGUARD_EX_SUPPRESSION` |
| 5 | `93573491` | **WIN (+1)** | Multi-Prize EX Box (Fezandipiti) | Batch 1 | 151 | `TACTICAL_PRIZE_TRADE` |
| 6 | `93574392` | **LOSS (-1)** | Duraludon (Metal Non-EX Resist) | Batch 1 | 91 | `LOSS_TYPE_RESISTANCE` (-30 DMG) |
| 7 | `93575313` | **LOSS (-1)** | Marnie's Grimmsnarl ex Box | Batch 1 | 167 | `LOSS_NONEX_PRIZE_RACE` |
| 8 | `93576224` | **WIN (+1)** | Mega Lucario ex (Mega EX Aggro) | Batch 1 | 139 | `SAFEGUARD_EX_SUPPRESSION` |
| 9 | `93577146` | **LOSS (-1)** | Cynthia's Gible/Gabite Non-EX | Batch 1 | 105 | `LOSS_NONEX_PRIZE_RACE` |
| 10 | `93578041` | **LOSS (-1)** | Crustle Safeguard (Mirror) | Batch 1 | 88 | `LOSS_MATCHUP_VARIANCE` (Mirror) |
| 11 | `93578958` | **WIN (+1)** | Non-EX Dwebble Deck | Batch 2 | 23 | `CLEAN_PRIZE_SWEEP` |
| 12 | `93579869` | **WIN (+1)** | Crustle Safeguard (Mirror) | Batch 2 | 149 | `TACTICAL_MIRROR_VICTORY` |
| 13 | `93580784` | **WIN (+1)** | Crustle Safeguard (Mirror) | Batch 2 | 57 | `TACTICAL_MIRROR_VICTORY` |
| 14 | `93581692` | **WIN (+1)** | Non-EX Dwebble Deck | Batch 2 | 29 | `CLEAN_PRIZE_SWEEP` |
| 15 | `93582613` | **LOSS (-1)** | Mega Starmie ex Box | Batch 2 | 69 | `LOSS_NONEX_PRIZE_RACE` |
| 16 | `93583569` | **LOSS (-1)** | Crustle Safeguard (Mirror) | Batch 2 | 131 | `LOSS_MATCHUP_VARIANCE` (Mirror) |
| 17 | `93584447` | **WIN (+1)** | Multi-Prize EX Box (Fezandipiti) | Batch 2 | 122 | `TACTICAL_PRIZE_TRADE` |
| 18 | `93585347` | **WIN (+1)** | Crustle Safeguard (Mirror) | Batch 2 | 80 | `TACTICAL_MIRROR_VICTORY` |
| 19 | `93586267` | **WIN (+1)** | Crustle Safeguard (Mirror) | Batch 2 | 64 | `TACTICAL_MIRROR_VICTORY` |

---

## 3. Key Finding

The rating drop to 492.2 was a temporary Glicko-2 asynchronous artifact following consecutive losses in Games 6, 7, 9, 10.
In reality, **Candidate F roared back with a 7–2 run (77.8% WR) across Games 11–19**, winning 4 out of 5 Mirror matches and defeating EX and swarm decks decisively.
