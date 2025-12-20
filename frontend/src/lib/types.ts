export type SpreadType = 'one_card' | 'three_card' | 'shadow_work' | 'celtic_cross';

export interface CardInReading {
  id: string;
  name: string;
  position: string;
  is_reversed: boolean;
  image_url: string;
  number?: number;
  numeral?: string;
  keywords?: string[];
  archetype?: string;
  hermetic_principle?: string;
  upright?: string;
  reversed?: string;
}

export interface Reading {
  id: string;
  question: string;
  spread_type: SpreadType;
  cards: CardInReading[];
  interpretation: string;
  created_at: string;
}

export interface ReadingListItem {
  id: string;
  question: string;
  spread_type: SpreadType;
  created_at: string;
}

export interface ReadingListResponse {
  readings: ReadingListItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface SpreadPosition {
  position: number;
  name: string;
  meaning: string;
  guidance: string;
}

export interface Spread {
  name: string;
  spread_id: string;
  description: string;
  card_count: number;
  positions: SpreadPosition[];
  instructions: string;
}
