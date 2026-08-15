/**
 * PTCG // NEXUS — Strict Color System
 * Premium dark mode palette with Electric Yellow primary accent and restrained energy type accents.
 */

export const colors = {
  // Base Surfaces
  bgVoid: '#07080B',
  bgObsidian: '#0B0D12',
  bgGraphite: '#11141A',
  bgSmoke: '#181C24',
  bgElevated: '#1E232D',

  // Borders & Dividers
  borderSubtle: 'rgba(255, 255, 255, 0.06)',
  borderMuted: 'rgba(255, 255, 255, 0.12)',
  borderStrong: 'rgba(255, 255, 255, 0.24)',
  borderTactical: 'rgba(250, 204, 21, 0.4)',

  // Typography
  textPrimary: '#F8FAFC',
  textSecondary: '#94A3B8',
  textMuted: '#64748B',
  textDim: '#475569',

  // Primary Tactical Accent: Electric Yellow
  electricYellow: '#FACC15',
  electricYellowBright: '#FFE600',
  electricYellowDim: 'rgba(250, 204, 21, 0.12)',
  electricYellowGlow: 'rgba(250, 204, 21, 0.25)',

  // Restrained Pokémon Energy Semantic Accents
  energy: {
    lightning: '#EAB308',
    fire: '#EF4444',
    water: '#3B82F6',
    grass: '#10B981',
    psychic: '#A855F7',
    fighting: '#F97316',
    darkness: '#64748B',
    metal: '#94A3B8',
    colorless: '#CBD5E1',
  },

  // Tactical Status
  status: {
    optimal: '#10B981',
    warning: '#F59E0B',
    critical: '#F43F5E',
    info: '#06B6D4',
  },
} as const;
