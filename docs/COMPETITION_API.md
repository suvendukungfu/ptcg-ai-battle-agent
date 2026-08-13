# Pokémon TCG AI Battle Challenge — Official Engine & Competition API Reference

This document describes the native engine APIs and Python bindings powering **The Pokémon Company – PTCG AI Battle Challenge Simulation** (`cabt` / `cg`).

---

## 1. Engine Architecture & CTypes Native Layer (`cg/sim.py` & `cg/game.py`)

The simulator is implemented as high-performance C/C++ native shared libraries:
- `libcg.dylib` (macOS arm64 / Intel)
- `libcg.so` (Linux x86_64)
- `libcg-arm64.so` (Linux aarch64 / arm64)
- `cg.dll` (Windows x64)

### Core CTypes Entry Points

| Symbol | Signature | Description |
| :--- | :--- | :--- |
| `lib.GameInitialize()` | `void -> void` | Initializes card catalog and static lookup tables. |
| `lib.BattleStart(arg)` | `int[120] -> StartData` | Starts a battle given Player 0 (60 cards) and Player 1 (60 cards). Returns `battlePtr`. |
| `lib.GetBattleData(ptr)`| `void* -> SerialData` | Extracts serialized JSON observation & search byte payload for current active player. |
| `lib.Select(ptr, sel, cnt)` | `(void*, int*, int) -> int` | Submits selected action option indices to advance the game state. |
| `lib.BattleFinish(ptr)` | `void* -> void` | Frees allocated memory and cleans up battle instance. |
| `lib.AllCard()` | `void -> char*` | Returns full JSON list containing all 1,267 competition card records. |
| `lib.SearchBegin(data, cnt)` | `(char*, int) -> void*` | Initiates fast C++ lookahead search from serialized game state. |
| `lib.SearchStep(searchPtr)` | `void* -> int` | Advances search step in tree expansion. |
| `lib.SearchEnd(searchPtr)` | `void* -> void` | Finalizes search lookahead and cleans up search buffers. |
| `lib.VisualizeData(ptr)` | `void* -> char*` | Generates replay payload for interactive HTML visualizer. |

---

## 2. Data Structures & Schemas

### A. Observation Dictionary Schema (`obs`)
```json
{
  "current": {
    "turn": 3,
    "yourIndex": 0,
    "players": [
      {
        "prize": [1, 2, 3],
        "deckCount": 38,
        "hand": [721, 723, 1219, 3],
        "active": [
          {
            "id": 723,
            "hp": 350,
            "maxHp": 350,
            "energies": [3, 3],
            "retreatCost": 4
          }
        ],
        "bench": [
          {
            "id": 721,
            "hp": 150,
            "maxHp": 150,
            "energies": [3]
          }
        ],
        "discard": []
      },
      {
        "prize": [1, 2, 3, 4, 5, 6],
        "deckCount": 42,
        "active": [{ "id": 721, "hp": 150, "energies": [] }],
        "bench": []
      }
    ]
  },
  "select": {
    "type": 0,
    "minCount": 1,
    "maxCount": 1,
    "option": [
      { "type": 7, "index": 0 },
      { "type": 8, "inPlayArea": 4, "inPlayIndex": 0 },
      { "type": 14 }
    ]
  }
}
```

### B. SelectContext & OptionType Reference

| OptionType Code | Semantic Meaning | Associated Fields in Option |
| :---: | :--- | :--- |
| **0** | Generic Option / Card Select | `id`, `area`, `index` |
| **1** | Select Card from Deck / Hand | `id`, `index` |
| **2** | Play Trainer Card | `id`, `targetArea` |
| **3** | Evolution (Stage 1 / Stage 2 / ex) | `id`, `targetArea`, `targetIndex` |
| **4** | Play Basic Pokémon to Bench | `id` |
| **5** | Select In-Play Pokémon Target | `inPlayArea`, `inPlayIndex` |
| **6** | Select Destination Slot | `area`, `index` |
| **7** | Execute Attack | `index` (Attack index: 0, 1) |
| **8** | Energy Attachment | `inPlayArea` (4=Active, 5=Bench), `inPlayIndex` |
| **9** | Retreat Active Pokémon | `index` (Bench target index) |
| **10** | Select Prize Card | `index` |
| **13** | Confirm / Acknowledge Action | `None` |
| **14** | Pass / End Turn | `None` |
| **15** | Reject / Decline Optional Action | `None` |

### C. AreaType Enum
- `0`: None / Unknown
- `1`: Hand
- `2`: Deck
- `3`: Discard Pile
- `4`: Active Spot (Battle Area)
- `5`: Bench Area (Slots 0..4)
- `6`: Prize Cards
- `7`: Lost Zone / Looking Zone

### D. EnergyType Enum
- `0`: Colorless
- `1`: Grass (`{G}`)
- `2`: Fire (`{R}`)
- `3`: Water (`{W}`)
- `4`: Lightning (`{L}`)
- `5`: Psychic (`{P}`)
- `6`: Fighting (`{F}`)
- `7`: Darkness (`{D}`)
- `8`: Metal (`{M}`)
- `9`: Dragon (`{N}`)
