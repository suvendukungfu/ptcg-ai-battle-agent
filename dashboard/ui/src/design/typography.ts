/**
 * PTCG // NEXUS — Typography System
 * Strict 3-tier hierarchy: Display, Body, Telemetry
 */

export const typography = {
  fonts: {
    display: "'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    body: "'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    mono: "'JetBrains Mono', monospace",
  },
  sizes: {
    hero: 'clamp(2.5rem, 5vw, 4.5rem)',
    h1: 'clamp(1.75rem, 3vw, 2.5rem)',
    h2: 'clamp(1.25rem, 2vw, 1.75rem)',
    h3: '1.125rem',
    bodyLg: '1rem',
    body: '0.875rem',
    bodySm: '0.75rem',
    caption: '0.6875rem',
    telemetry: '0.75rem',
  },
  weights: {
    regular: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    black: '900',
  },
} as const;
