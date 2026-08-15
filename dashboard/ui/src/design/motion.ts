/**
 * PTCG // NEXUS — Motion & Easing Curves
 */

export const motion = {
  durations: {
    instant: '75ms',
    fast: '150ms',
    normal: '250ms',
    slow: '400ms',
  },
  easings: {
    outExpo: 'cubic-bezier(0.16, 1, 0.3, 1)',
    outBack: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    easeInOut: 'cubic-bezier(0.65, 0, 0.35, 1)',
  },
} as const;
