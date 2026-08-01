# Candidate G Architecture & Design Specification

Generated at: 2026-08-16 08:35:00 UTC
Research Branch: `candidate-g-research`

---

## 1. Design Motivation & Diagnostic Findings

Live Kaggle monitoring of Candidate F (PTCG NEXUS v3.4) revealed:
- **Major Strength**: **100% Win Rate vs EX Multi-Prize Threats** (Episode `93570797` vs Mega Lucario ex 440 HP was a dominant 0-damage Safeguard sweep).
- **Observed Vulnerabilities**:
  1. **Grass Resistance (-30 Metal)** in Episode `93569861` (Duraludon #169) reducing damage from 120 to 90.
  2. **Turn-1 Fire Weakness Donk** in Episode `93571687` (Cinderace #666 Setup ability dealing 160+ Weakness damage to a lone basic).

Candidate G explores the minimal deck modifications that enhance Non-EX resilience and anti-weakness/resistance survival while strictly preserving the 100% EX Safeguard lock.

---

## 2. Tested Candidate G Variants (G0 through G9)

| Variant | Concept | Deck Composition | Key Additions / Modifications |
| :--- | :--- | :--- | :--- |
| **G0** | Candidate F Baseline | 4 Dwebble, 4 Crustle, 1 Secret Box, 4 Ultra Ball, 4 Poffin, 4 Candy, 4 Boss, 35 Grass | Control baseline |
| **G1** | High Basic Density | 4 Dwebble, 4 Crustle, 2 Tapu Bulu (140 HP), 1 Secret Box, 16 Trainers, 33 Grass | +2 140 HP Basics |
| **G2** | Alt Grass Attacker | 4 Dwebble, 4 Crustle, 2 Shaymin, 2 Tapu Bulu, 1 Secret Box, 16 Trainers, 35 Grass | Bench barrier + Bulu |
| **G3** | Rillaboom HP Line | 4 Dwebble, 4 Crustle, 3-2-3 Rillaboom line, 1 Secret Box, 16 Trainers, 27 Grass | Stage 2 180 HP |
| **G4** | Colorless Neutral | 4 Dwebble, 4 Crustle, 2 Snorlax (160 HP), 1 Secret Box, 16 Trainers, 37 Grass | Ignores Grass Resistance |
| **G5** | Minimal Backup | 4 Dwebble, 4 Crustle, 1 Tapu Bulu, 1 Secret Box, 16 Trainers, 38 Grass | +1 Single-Prize Tank |
| **G6** | Hybrid Bellibolt | 3 Tadbulb, 3 Bellibolt ex, 3 Dwebble, 3 Crustle, 17 Lightning, 18 Grass | Dual-type hybrid |
| **G7** | Anti-Resistance | 4 Dwebble, 4 Crustle, 2 Crushing Hammer, 2 Night Stretcher, 1 Secret Box, 16 Trainers, 35 Grass | Energy denial + recovery |
| **G8** | Anti-Weakness/Recovery| 4 Dwebble, 4 Crustle, 2 Super Potion, 1 Secret Box, 16 Trainers, 37 Grass | Fast HP restoration |
| **G9** | Optimized Combination | 4 Dwebble, 4 Crustle, 2 Tapu Bulu, 2 Crushing Hammer, 1 Secret Box, 16 Trainers, 35 Grass | Tank + denial |
