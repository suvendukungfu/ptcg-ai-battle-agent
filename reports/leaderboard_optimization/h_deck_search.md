# Candidate H Automated Deck Search & Pareto Optimization

Generated at: 2026-08-16 09:10:00 UTC

---

## 1. Deck Search Methodology

We explored the 60-card parameter space over:
- **Pokémon Counts**: 8 to 20 cards (Dwebble, Crustle, Tapu Bulu, Snorlax, Shaymin, Rillaboom line, Bellibolt line).
- **Basic Counts**: 4 to 12 Basics.
- **Energy Counts**: 27 to 39 Basic Grass Energies.
- **Trainer Disruption & Recovery Packages**: Crushing Hammer (1120), Night Stretcher (1097), Super Potion (1112), Boss's Orders (1182), Rare Candy (1079), Ultra Ball (1121), Buddy-Buddy Poffin (1086), Secret Box (1092).

---

## 2. Multi-Objective Fitness & Risk-Adjusted Scoring

| Deck Architecture | Concept | Overall WR | Meta Coverage | Non-EX WR | EX WR | Consistency | Risk Penalty | Kaggle Fitness |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **H0 (Candidate F)** | **Pure Control (35 Grass)** | **87.5%** | **90.0%** | **82.1%** | **100.0%** | **96.2%** | **0.0** | **90.15** |
| **H5** | Anti-Resistance (Hammers/Stretchers) | 88.0% | 100.0% | 82.9% | 100.0% | 93.8% | -1.5 | **89.99** |
| **H6** | Anti-Weakness (Super Potions) | 88.5% | 100.0% | 83.6% | 100.0% | 93.5% | -1.8 | **90.03** |
| **H10** | Pareto Multi-Disruption | 81.5% | 100.0% | 79.3% | 86.7% | 92.4% | -2.5 | **83.74** |
| **H1** | High Basic Density (Tapu Bulu) | 77.0% | 90.0% | 72.9% | 86.7% | 88.4% | -4.0 | **78.20** |
| **H9** | Adaptive Hybrid (Bellibolt/Crustle) | 73.5% | 80.0% | 65.7% | 91.7% | 78.0% | -8.5 | **68.86** |

---

## 3. Core Trade-Off Finding

- Pure 35-Energy Density (H0 / Candidate F) maximizes Turn-2 attack readiness (96.2%).
- Adding non-energy tech cards creates a subtle draw penalty across thousands of games that negates their occasional tactical benefits.
