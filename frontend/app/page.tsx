"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { KnowledgeCard, Tag } from "@/types/card";
import SubmitBar from "@/components/SubmitBar";
import CardItem from "@/components/CardItem";
import SearchBar from "@/components/SearchBar";
import Sidebar from "@/components/Sidebar";

export default function HomePage() {
  const [cards, setCards] = useState<KnowledgeCard[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [selectedTag, setSelectedTag] = useState("");
  const [showFavorites, setShowFavorites] = useState(false);
  const [query, setQuery] = useState("");
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchCards = useCallback(async () => {
    try {
      const [list, tagList] = await Promise.all([
        api.listCards({
          tag: selectedTag || undefined,
          favorite: showFavorites || undefined,
          q: query || undefined,
        }),
        api.listTags(),
      ]);
      setCards(list.items);
      setTotal(list.total);
      setTags(tagList);
    } finally {
      setLoading(false);
    }
  }, [selectedTag, showFavorites, query]);

  useEffect(() => {
    setLoading(true);
    fetchCards();
  }, [fetchCards]);

  // 轮询：当有"处理中"的卡片时，每3秒刷新一次
  useEffect(() => {
    const hasProcessing = cards.some((c) => c.status === "processing");
    if (hasProcessing) {
      pollRef.current = setInterval(fetchCards, 3000);
    } else {
      if (pollRef.current) clearInterval(pollRef.current);
    }
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [cards, fetchCards]);

  function handleSearch(q: string) {
    setQuery(q);
  }

  return (
    <div className="flex flex-col gap-6">
      {/* 提交栏 */}
      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
        <p className="text-sm font-medium text-slate-600 mb-3">
          粘贴抖音短视频链接，自动提取文案 · AI 分析亮点
        </p>
        <SubmitBar onCreated={fetchCards} />
      </div>

      {/* 主体：侧边栏 + 卡片区 */}
      <div className="flex gap-6 items-start">
        <Sidebar
          tags={tags}
          selectedTag={selectedTag}
          onTagSelect={setSelectedTag}
          showFavorites={showFavorites}
          onFavoritesToggle={() => setShowFavorites((v) => !v)}
          total={total}
        />

        <div className="flex-1 min-w-0 flex flex-col gap-4">
          <SearchBar onSearch={handleSearch} />

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="bg-white rounded-2xl h-44 animate-pulse border border-slate-100" />
              ))}
            </div>
          ) : cards.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-24 text-center">
              <span className="text-5xl mb-4">📭</span>
              <p className="text-slate-500 font-medium">还没有知识卡片</p>
              <p className="text-slate-400 text-sm mt-1">在上方粘贴抖音链接，开始收集吧</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {cards.map((card) => (
                <CardItem key={card.id} card={card} onUpdate={fetchCards} />
              ))}
            </div>
          )}

          {!loading && total > 0 && (
            <p className="text-xs text-slate-400 text-center">共 {total} 张卡片</p>
          )}
        </div>
      </div>
    </div>
  );
}
