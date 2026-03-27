"use client";
import { Tag } from "@/types/card";

interface Props {
  tags: Tag[];
  selectedTag: string;
  onTagSelect: (tag: string) => void;
  showFavorites: boolean;
  onFavoritesToggle: () => void;
  total: number;
}

export default function Sidebar({ tags, selectedTag, onTagSelect, showFavorites, onFavoritesToggle, total }: Props) {
  return (
    <aside className="w-52 shrink-0 flex flex-col gap-1">
      <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 mb-1">筛选</p>

      <button
        onClick={() => { onTagSelect(""); if (showFavorites) onFavoritesToggle(); }}
        className={`flex items-center justify-between px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
          !selectedTag && !showFavorites
            ? "bg-violet-100 text-violet-700"
            : "text-slate-600 hover:bg-slate-100"
        }`}
      >
        <span>全部卡片</span>
        <span className="text-xs text-slate-400">{total}</span>
      </button>

      <button
        onClick={onFavoritesToggle}
        className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
          showFavorites
            ? "bg-amber-100 text-amber-700"
            : "text-slate-600 hover:bg-slate-100"
        }`}
      >
        <span>⭐ 收藏</span>
      </button>

      {tags.length > 0 && (
        <>
          <div className="h-px bg-slate-100 my-2" />
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 mb-1">标签</p>
          {tags.map((tag) => (
            <button
              key={tag.name}
              onClick={() => onTagSelect(tag.name === selectedTag ? "" : tag.name)}
              className={`flex items-center justify-between px-3 py-2 rounded-xl text-sm transition-colors ${
                selectedTag === tag.name
                  ? "bg-violet-100 text-violet-700 font-medium"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <span className="truncate">{tag.name}</span>
              <span className="text-xs text-slate-400 shrink-0 ml-1">{tag.count}</span>
            </button>
          ))}
        </>
      )}
    </aside>
  );
}
