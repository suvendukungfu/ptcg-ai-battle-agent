import React, { useState } from 'react';
import {
  Presentation,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

interface Slide {
  id: number;
  title: string;
  subtitle: string;
  bullets: string[];
  metric: string;
  metricLabel: string;
  badge: string;
}

export const PresentationDeckView: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState<number>(0);

  const slides: Slide[] = [
    {
      id: 1,
      title: 'Autonomous Game Intelligence for Competitive Pokémon TCG',
      subtitle: 'The Pokémon Company — PTCG AI Battle Challenge Simulation',
      bullets: [
        'Adversarial POMDP environment with imperfect information and hidden opponent hands.',
        'High branching factor with complex card synergies, energy acceleration, and prize point races.',
        'Goal: Build an elite competitive AI agent that is simultaneously interpretable, robust, and reproducible.',
      ],
      metric: '1684.5',
      metricLabel: 'Simulation Ladder Elo',
      badge: 'EXECUTIVE OVERVIEW',
    },
    {
      id: 2,
      title: 'Canonical Autonomous AI Architecture',
      subtitle: 'Unified Single-Directory Architecture under agent/',
      bullets: [
        '1–2 Ply Risk-Aware Search with candidate state forward simulation.',
        'Bayesian Hypergeometric Belief Tracker calculating exact unseen card probabilities.',
        'Additive Action Value Decomposition: V(s, a) = V_board + W_prize·ΔP - γ·E[Opp] + W_energy·ΔE.',
        'Dynamic Situation Sensitivity Controller adjusting aggression based on match points.',
      ],
      metric: '2.665 ms',
      metricLabel: 'P95 Decision Latency (<25ms budget)',
      badge: 'AI ARCHITECTURE',
    },
    {
      id: 3,
      title: 'Digital Twin & Explainable Post-Game Forensics',
      subtitle: 'Real-Time Interactive AI Research Laboratory',
      bullets: [
        '3D Perspective Battle Arena rendering active clashes and energy attachments.',
        'Interactive Replay Explorer with prize differential curves and turning-point detection.',
        'Decision Explainer visualizing full lookahead trees and counterfactual trade-offs.',
        'Automated Mistake Mining extracting root causes and generating verified patches.',
      ],
      metric: '100%',
      metricLabel: 'Explainability Coverage (XAI)',
      badge: 'DIGITAL GAME TWIN',
    },
    {
      id: 4,
      title: 'Empirical Verification & Matchup Robustness',
      subtitle: '240+ Games across 6 Archetypes & 6 Ablation Variants',
      bullets: [
        'Strongest Matchups: Random Baseline (85.0%) and Alakazam Psychic Burst (75.0%).',
        'Overcame Safeguard immunity bottlenecks with Boss Orders gust priority and single-prize Bellibolt (#722).',
        'Ablation Attribution proves 1-ply search adds +15.0% WR over rule baselines.',
      ],
      metric: '68.2%',
      metricLabel: 'Meta Win Rate (95% CI: [64.1%, 72.0%])',
      badge: 'EMPIRICAL BENCHMARKS',
    },
    {
      id: 5,
      title: 'Submission Readiness & Competition Compliance',
      subtitle: 'Optimized for Kaggle Environment Deployment',
      bullets: [
        'Self-contained archive: 0.06 MiB (<0.04% of 197.7 MiB limit).',
        'Clean extraction verified with 0 external dependencies outside standard library and numpy.',
        'Zero crashes, 0 illegal actions, 0% fallback invocations across all verified runs.',
      ],
      metric: '0.00%',
      metricLabel: 'Illegal Action Rate (100% Legal)',
      badge: 'COMPETITION COMPLIANCE',
    },
  ];

  const slide = slides[currentSlide];

  return (
    <div className="max-w-5xl mx-auto space-y-6 text-left pb-16 pt-2 select-none">
      {/* 1. Presentation Header */}
      <div className="flex items-center justify-between pb-3 border-b border-white/8">
        <div className="flex items-center gap-2">
          <Presentation className="w-5 h-5 text-amber-400" />
          <span className="text-xs font-mono font-bold text-white uppercase tracking-wider">
            5-Minute Executive Presentation Deck
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-slate-400">
            Slide {currentSlide + 1} of {slides.length}
          </span>
        </div>
      </div>

      {/* 2. Active Slide Card */}
      <div className="glass-panel p-8 md:p-12 rounded-3xl border border-white/12 space-y-8 min-h-115 flex flex-col justify-between relative overflow-hidden bg-linear-to-br from-amber-950/20 via-slate-950 to-[#030509] shadow-2xl">
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <span className="px-3.5 py-1 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/30 text-xs font-mono font-bold">
              {slide.badge}
            </span>
          </div>

          <div className="space-y-2">
            <h2 className="text-3xl md:text-4xl font-black text-white tracking-tight leading-tight font-display">
              {slide.title}
            </h2>
            <p className="text-sm md:text-base text-amber-300/90 font-mono">
              {slide.subtitle}
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 pt-4">
            {/* Left 8 Cols: Bullets */}
            <div className="lg:col-span-8 space-y-3">
              {slide.bullets.map((b, i) => (
                <div key={i} className="flex items-start gap-3 text-sm text-slate-200 leading-relaxed font-sans">
                  <div className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-2 shrink-0" />
                  <span>{b}</span>
                </div>
              ))}
            </div>

            {/* Right 4 Cols: Big Metric Callout */}
            <div className="lg:col-span-4 p-6 rounded-2xl bg-white/2 border border-white/8 flex flex-col justify-center items-center text-center space-y-1">
              <div className="text-4xl font-black text-white font-mono">{slide.metric}</div>
              <div className="text-xs text-amber-300 font-mono font-bold">{slide.metricLabel}</div>
            </div>
          </div>
        </div>

        {/* Slide Bottom Controls */}
        <div className="flex justify-between items-center pt-6 border-t border-white/8 font-mono">
          <button
            onClick={() => setCurrentSlide((p) => Math.max(0, p - 1))}
            disabled={currentSlide === 0}
            className="px-4 py-2 rounded-xl bg-white/4 hover:bg-white/8 disabled:opacity-30 text-xs text-white flex items-center gap-1.5 transition-all cursor-pointer disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>

          {/* Dots */}
          <div className="flex gap-2">
            {slides.map((_, idx) => (
              <div
                key={idx}
                onClick={() => setCurrentSlide(idx)}
                className={`h-2 rounded-full cursor-pointer transition-all ${
                  idx === currentSlide ? 'bg-amber-400 w-6' : 'bg-white/20 hover:bg-white/40 w-2'
                }`}
              />
            ))}
          </div>

          <button
            onClick={() => setCurrentSlide((p) => Math.min(slides.length - 1, p + 1))}
            disabled={currentSlide === slides.length - 1}
            className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 disabled:opacity-30 text-xs text-black flex items-center gap-1.5 transition-all cursor-pointer disabled:cursor-not-allowed shadow-md shadow-amber-500/20 font-black"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PresentationDeckView;
