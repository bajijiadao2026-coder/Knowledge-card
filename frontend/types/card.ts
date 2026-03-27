export type CardStatus = "processing" | "done" | "failed";

export interface KnowledgeCard {
  id: number;
  title: string;
  source_url: string;
  platform: string;
  author?: string;
  cover_url?: string;
  transcript?: string;
  core_value?: string;
  why_it_works?: string[];
  writing_techniques?: string[];
  reusable_structure?: string;
  tags?: string[];
  is_favorite: boolean;
  status: CardStatus;
  created_at: string;
  updated_at: string;
}

export interface CardList {
  total: number;
  items: KnowledgeCard[];
}

export interface Tag {
  name: string;
  count: number;
}
