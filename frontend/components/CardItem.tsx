"use client";
import Link from "next/link";
import { KnowledgeCard } from "@/types/card";
import { api } from "@/lib/api";
import { useState } from "react";

interface Props {
  card: KnowledgeCard;
  onUpdate: () => void;
}

const TAG_COLORS = [
  "bg-violet-100 text-violet-700",
  "bg-blue-100 text-blue-700",
  "bg-emerald-100 text-emerald-700",
  "bg-amber-100 text-amber-700",
  "bg-pink-100 text-pink-700",
];

export default function CardItem({ card, onUpdate }: Props) {
  const [favoriting, setFavoriting] = useState(false);

  async function toggleFav(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    setFavoriting(true);
    try {
      await api.toggleFavorite(card.id);
      onUpdate();
    } finally {
      setFavoriting(false);
    }
  }

  if (card.status === "processing") {
    return (
      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5 flex items-center gap-3 animate-pulse">
        <div className="w-8 h-8 rounded-full bg-violet-100 flex items-center justify-center shrink-0">
          <svg className="animate-spin h-4 w-4 text-violet-500" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
          </svg>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-slate-500">正在提取文案并分析...</p>
          <p className="text-xs text-slate-400 truncate mt-0.5">{card.source_url}</p>
        </div>
      </div>
    );
  }

  if (card.status === "failed") {
    return (
      <div className="bg-white rounded-2xl border border-red-100 shadow-sm p-5 flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center shrink-0 text-red-500">✕</div>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-red-500">处理失败</p>
          <p className="text-xs text-slate-400 truncate mt-0.5">{card.source_url}</p>
        </div>
      </div>
    );
  }

  return (
    <Link href={`/cards/${card.id}`} className="block group">
      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md hover:border-violet-200 transition-all duration-200 p-5 flex flex-col gap-3 h-full">
        {/* 标题行 */}
        <div className="flex items-start justify-between gap-2">
          <h2 className="font-semibold text-slate-800 text-sm leading-snug group-hover:text-violet-600 transition-colors line-clamp-2">
            {card.title}
          </h2>
          <button
            onClick={toggleFav}
            disabled={favoriting}
            className="shrink-0 text-lg leading-none mt-0.5 transition-transform hover:scale-110 disabled:opacity-50"
            title={card.is_favorite ? "取消收藏" : "收藏"}
          >
            {card.is_favorite ? "⭐" : "☆"}
          </button>
        </div>

        {/* 核心价值 */}
        {card.core_value && (
          <p className="text-xs text-slate-500 leading-relaxed line-clamp-2 bg-slate-50 rounded-lg px-3 py-2">
            {card.core_value}
          </p>
        )}

        {/* 可复用结构 */}
        {card.reusable_structure && (
          <div className="text-xs text-violet-600 bg-violet-50 rounded-lg px-3 py-2 font-mono leading-relaxed line-clamp-1">
            {card.reusable_structure}
          </div>
        )}

        {/* 底部：标签 + 来源 */}
        <div className="flex items-center justify-between mt-auto pt-1">
          <div className="flex flex-wrap gap-1">
            {(card.tags || []).slice(0, 3).map((tag, i) => (
              <span key={tag} className={`text-xs px-2 py-0.5 rounded-full font-medium ${TAG_COLORS[i % TAG_COLORS.length]}`}>
                {tag}
              </span>
            ))}
          </div>
          <span className="text-xs text-slate-400 shrink-0">
            {new Date(card.created_at).toLocaleDateString("zh-CN")}
          </span>
        </div>
      </div>
    </Link>
  );
}
