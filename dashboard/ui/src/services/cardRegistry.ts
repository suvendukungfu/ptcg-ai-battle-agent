/**
 * PTCG // NEXUS — Official Card Asset Registry & Metadata Store
 * Maps card IDs to verified official card artwork, types, HP, moves, and tactical roles.
 */

export interface CardMeta {
  id: number;
  name: string;
  category: 'Pokemon' | 'Item' | 'Supporter' | 'Tool' | 'Energy';
  type: 'Lightning' | 'Grass' | 'Psychic' | 'Fire' | 'Water' | 'Fighting' | 'Darkness' | 'Metal' | 'Colorless';
  stage?: 'Basic' | 'Stage 1' | 'Stage 2';
  isEx?: boolean;
  hp?: number;
  attacks?: Array<{ name: string; damage: number | string; cost: string }>;
  ability?: { name: string; text: string };
  retreat?: number;
  weakness?: string;
  img: string;
  fallbackImg: string;
  aiPriority: string;
}

export const CARD_REGISTRY: Record<number, CardMeta> = {
  // Bellibolt Line
  723: {
    id: 723,
    name: 'Bellibolt ex',
    category: 'Pokemon',
    type: 'Lightning',
    stage: 'Stage 1',
    isEx: true,
    hp: 350,
    attacks: [{ name: 'Electro Bullet', damage: 160, cost: '⚡⚡' }],
    retreat: 2,
    weakness: 'Fighting',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/939.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/939.png',
    aiPriority: 'P0: Evolve onto Tadbulb, charge with 2⚡, and execute Electro Bullet.',
  },
  722: {
    id: 722,
    name: 'Bellibolt',
    category: 'Pokemon',
    type: 'Lightning',
    stage: 'Stage 1',
    isEx: false,
    hp: 140,
    attacks: [{ name: 'Thunderbolt', damage: 140, cost: '⚡⚡' }],
    retreat: 2,
    weakness: 'Fighting',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/939.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/939.png',
    aiPriority: 'P1: Single-prize attacker used to bypass Safeguard / ex immunity.',
  },
  721: {
    id: 721,
    name: 'Tadbulb',
    category: 'Pokemon',
    type: 'Lightning',
    stage: 'Basic',
    isEx: false,
    hp: 70,
    attacks: [{ name: 'Thunder Jolt', damage: 30, cost: '⚡' }],
    retreat: 1,
    weakness: 'Fighting',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/938.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/938.png',
    aiPriority: 'P0: Search on Turn 1 to establish bench and active evolution anchor.',
  },

  // Crustle Line
  345: {
    id: 345,
    name: 'Crustle',
    category: 'Pokemon',
    type: 'Grass',
    stage: 'Stage 1',
    isEx: false,
    hp: 150,
    ability: {
      name: 'Mysterious Rock Inn',
      text: "Prevent all damage done to this Pokémon by attacks from your opponent's Pokémon {ex}.",
    },
    attacks: [{ name: 'Rock Slide', damage: 110, cost: '🌿🌿' }],
    retreat: 3,
    weakness: 'Fire',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/558.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/558.png',
    aiPriority: 'Opponent Threat: Safeguard Wall. Gust bench with Boss Orders or attack with #722.',
  },
  344: {
    id: 344,
    name: 'Dwebble',
    category: 'Pokemon',
    type: 'Grass',
    stage: 'Basic',
    isEx: false,
    hp: 70,
    attacks: [{ name: 'Bug Bite', damage: 30, cost: '🌿' }],
    retreat: 2,
    weakness: 'Fire',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/557.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/557.png',
    aiPriority: 'Target Snipe: Vulnerable basic prior to Safeguard evolution.',
  },

  // Alakazam Line
  743: {
    id: 743,
    name: 'Alakazam',
    category: 'Pokemon',
    type: 'Psychic',
    stage: 'Stage 2',
    isEx: false,
    hp: 140,
    ability: { name: 'Psychic Draw', text: 'When played from hand to evolve, draw 3 cards.' },
    attacks: [{ name: 'Mind Shock', damage: 130, cost: '👁️👁️' }],
    retreat: 1,
    weakness: 'Darkness',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png',
    aiPriority: 'Burst Attacker: High priority knockout before psychic draw snowball.',
  },
  742: {
    id: 742,
    name: 'Kadabra',
    category: 'Pokemon',
    type: 'Psychic',
    stage: 'Stage 1',
    isEx: false,
    hp: 80,
    attacks: [{ name: 'Psybeam', damage: 50, cost: '👁️' }],
    retreat: 1,
    weakness: 'Darkness',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/64.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/64.png',
    aiPriority: 'Target Snipe: KO in 1 hit with 160 dmg Electro Bullet.',
  },
  741: {
    id: 741,
    name: 'Abra',
    category: 'Pokemon',
    type: 'Psychic',
    stage: 'Basic',
    isEx: false,
    hp: 50,
    attacks: [{ name: 'Teleport', damage: 0, cost: '👁️' }],
    retreat: 1,
    weakness: 'Darkness',
    img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/63.png',
    fallbackImg: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/63.png',
    aiPriority: 'Basic Target: 50 HP fragile target.',
  },

  // Key Items & Trainers
  1219: {
    id: 1219,
    name: 'Electric Generator',
    category: 'Item',
    type: 'Lightning',
    img: 'https://images.pokemontcg.io/sv1/170_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sv1/170.png',
    aiPriority: 'P0 Energy Acceleration: Check top 5 cards and attach up to 2⚡ to bench.',
  },
  1262: {
    id: 1262,
    name: "Boss's Orders",
    category: 'Supporter',
    type: 'Colorless',
    img: 'https://images.pokemontcg.io/sv1/196_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sv1/196.png',
    aiPriority: "P0 Gust: Switch opponent's benched Pokémon into active spot for lethal KO.",
  },
  1092: {
    id: 1092,
    name: "Professor's Research",
    category: 'Supporter',
    type: 'Colorless',
    img: 'https://images.pokemontcg.io/sv1/189_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sv1/189.png',
    aiPriority: 'P1 Draw 7: Play after dumping unneeded items to rebuild hand.',
  },
  1121: {
    id: 1121,
    name: 'Ultra Ball',
    category: 'Item',
    type: 'Colorless',
    img: 'https://images.pokemontcg.io/sv1/194_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sv1/194.png',
    aiPriority: 'P1 Search: Discard 2 cards to fetch Bellibolt ex or basic Pokémon.',
  },
  1227: {
    id: 1227,
    name: 'Nest Ball',
    category: 'Item',
    type: 'Colorless',
    img: 'https://images.pokemontcg.io/sv1/257_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sv1/257.png',
    aiPriority: 'P0 Setup: Search deck for Basic Pokémon and place onto Bench.',
  },
  1145: {
    id: 1145,
    name: 'Switch',
    category: 'Item',
    type: 'Colorless',
    img: 'https://images.pokemontcg.io/sv1/194_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sv1/194.png',
    aiPriority: 'P1 Mobility: Switch Active Pokémon with Benched Pokémon with 0 retreat cost.',
  },
  1163: {
    id: 1163,
    name: 'Heavy Baton',
    category: 'Tool',
    type: 'Colorless',
    img: 'https://images.pokemontcg.io/tef/151_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/tef/151.png',
    aiPriority: 'P2 Tool: Retain up to 3⚡ energy when active tank is knocked out.',
  },

  // Basic Energies
  3: {
    id: 3,
    name: 'Basic Lightning Energy',
    category: 'Energy',
    type: 'Lightning',
    img: 'https://images.pokemontcg.io/sve/4_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sve/4.png',
    aiPriority: 'Fuel: Essential attack energy for Bellibolt ex and Tadbulb.',
  },
  4: {
    id: 4,
    name: 'Basic Lightning Energy',
    category: 'Energy',
    type: 'Lightning',
    img: 'https://images.pokemontcg.io/sve/4_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sve/4.png',
    aiPriority: 'Fuel: Essential attack energy for Bellibolt ex and Tadbulb.',
  },
  1: {
    id: 1,
    name: 'Basic Grass Energy',
    category: 'Energy',
    type: 'Grass',
    img: 'https://images.pokemontcg.io/sve/1_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sve/1.png',
    aiPriority: 'Fuel: Grass Energy.',
  },
  5: {
    id: 5,
    name: 'Basic Psychic Energy',
    category: 'Energy',
    type: 'Psychic',
    img: 'https://images.pokemontcg.io/sve/5_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sve/5.png',
    aiPriority: 'Fuel: Psychic Energy.',
  },
};

/** Get card metadata by ID with fallback default */
export function getCardMeta(cardId: number | undefined | null): CardMeta {
  if (cardId && CARD_REGISTRY[cardId]) {
    return CARD_REGISTRY[cardId];
  }
  return {
    id: cardId || 0,
    name: cardId ? `Card #${cardId}` : 'Unknown Card',
    category: 'Pokemon',
    type: 'Lightning',
    hp: 100,
    img: 'https://images.pokemontcg.io/sve/4_hires.png',
    fallbackImg: 'https://images.pokemontcg.io/sve/4.png',
    aiPriority: 'Standard game card.',
  };
}
