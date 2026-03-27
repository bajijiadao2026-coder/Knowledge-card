import { CardList, KnowledgeCard, Tag } from "@/types/card";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // 提交链接创建卡片
  createCard: (url: string) =>
    request<KnowledgeCard>("/api/cards", {
      method: "POST",
      body: JSON.stringify({ url }),
    }),

  // 获取卡片列表
  listCards: (params?: {
    page?: number;
    size?: number;
    tag?: string;
    favorite?: boolean;
    q?: string;
  }) => {
    const qs = new URLSearchParams();
    if (params?.page) qs.set("page", String(params.page));
    if (params?.size) qs.set("size", String(params.size));
    if (params?.tag) qs.set("tag", params.tag);
    if (params?.favorite !== undefined) qs.set("favorite", String(params.favorite));
    if (params?.q) qs.set("q", params.q);
    return request<CardList>(`/api/cards?${qs}`);
  },

  // 获取单张卡片
  getCard: (id: number) => request<KnowledgeCard>(`/api/cards/${id}`),

  // 更新卡片
  updateCard: (id: number, data: { title?: string; tags?: string[]; is_favorite?: boolean }) =>
    request<KnowledgeCard>(`/api/cards/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // 删除卡片
  deleteCard: (id: number) =>
    request<void>(`/api/cards/${id}`, { method: "DELETE" }),

  // 切换收藏
  toggleFavorite: (id: number) =>
    request<KnowledgeCard>(`/api/cards/${id}/favorite`, { method: "POST" }),

  // 获取所有标签
  listTags: () => request<Tag[]>("/api/tags"),
};
