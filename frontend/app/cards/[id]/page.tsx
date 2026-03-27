"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { KnowledgeCard } from "@/types/card";

const TAG_COLORS = [
  "bg-violet-100 text-violet-700",
  "bg-blue-100 text-blue-700",
  "bg-emerald-100 text-emerald-700",
  "bg-amber-100 text-amber-700",
  "bg-pink-100 text-pink-700",
];

export default function CardDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);

  const [card, setCard] = useState<KnowledgeCard | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [copied, setCopied] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    api.getCard(id).then((c) => {
      setCard(c);
      setEditTitle(c.title);
    }).finally(() => setLoading(false));
  }, [id]);

  async function saveTitle() {
    if (!card || editTitle === card.title) { setEditing(false); return; }
    const updated = await api.updateCard(id, { title: editTitle });
    setCard(updated);
    setEditing(false);
  }

  async function toggleFav() {
    if (!card) return;
    const updated = await api.toggleFavorite(id);
    setCard(updated);
  }

  async function handleDelete() {
    if (!confirm("确定删除这张卡片？")) return;
    setDeleting(true);
    await api.deleteCard(id);
    router.push("/");
  }

  async function copyStructure() {
    if (!card?.reusable_structure) return;
    await navigator.clipboard.writeText(card.reusable_structure);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-slate-200 rounded-xl w-2/3" />
          <div className="h-4 bg-slate-100 rounded-lg w-1/3" />
          <div className="h-32 bg-slate-100 rounded-2xl mt-6" />
          <div className="h-48 bg-slate-100 rounded-2xl" />
        </div>
      </div>
    );
  }

  if (!card) {
    return (
      <div className="text-center py-24">
        <p className="text-slate-500">卡片不存在</p>
        <Link href="/" className="text-violet-600 text-sm mt-2 inline-block hover:underline">← 返回首页</Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto flex flex-col gap-6">
      {/* 返回 */}
      <Link href="/" className="flex items-center gap-1 text-slate-400 text-sm hover:text-slate-600 transition-colors w-fit">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        返回
      </Link>

      {/* 标题卡 */}
      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            {editing ? (
              <div className="flex items-center gap-2">
                <input
                  autoFocus
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") saveTitle(); if (e.key === "Escape") setEditing(false); }}
                  className="flex-1 text-xl font-bold text-slate-800 border-b-2 border-violet-400 outline-none bg-transparent"
                />
                <button onClick={saveTitle} className="text-xs px-3 py-1 bg-violet-600 text-white rounded-lg">保存</button>
                <button onClick={() => setEditing(false)} className="text-xs px-3 py-1 bg-slate-100 text-slate-600 rounded-lg">取消</button>
              </div>
            ) : (
              <h1
                className="text-xl font-bold text-slate-800 cursor-pointer hover:text-violet-700 transition-colors"
                onClick={() => setEditing(true)}
                title="点击编辑标题"
              >
                {card.title}
              </h1>
            )}
            <div className="flex items-center gap-3 mt-2 text-xs text-slate-400">
              {card.author && <span>@{card.author}</span>}
              <span>{new Date(card.created_at).toLocaleString("zh-CN")}</span>
              <a
                href={card.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-violet-500 hover:underline flex items-center gap-1"
              >
                🔗 原视频
              </a>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <button onClick={toggleFav} className="text-2xl hover:scale-110 transition-transform" title="收藏">
              {card.is_favorite ? "⭐" : "☆"}
            </button>
            <button onClick={handleDelete} disabled={deleting} className="text-slate-400 hover:text-red-500 transition-colors p-1" title="删除">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* 标签 */}
        {card.tags && card.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4">
            {card.tags.map((tag, i) => (
              <span key={tag} className={`text-xs px-3 py-1 rounded-full font-medium ${TAG_COLORS[i % TAG_COLORS.length]}`}>
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* 核心价值 */}
      {card.core_value && (
        <Section icon="💡" title="核心价值">
          <p className="text-slate-700 text-sm leading-relaxed">{card.core_value}</p>
        </Section>
      )}

      {/* 为什么写得好 */}
      {card.why_it_works && card.why_it_works.length > 0 && (
        <Section icon="✨" title="为什么写得好">
          <ul className="flex flex-col gap-3">
            {card.why_it_works.map((point, i) => (
              <li key={i} className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-violet-100 text-violet-600 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <p className="text-slate-700 text-sm leading-relaxed">{point}</p>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* 文案技巧 */}
      {card.writing_techniques && card.writing_techniques.length > 0 && (
        <Section icon="🎯" title="使用的文案技巧">
          <div className="flex flex-wrap gap-2">
            {card.writing_techniques.map((t) => (
              <span key={t} className="text-sm px-3 py-1.5 bg-slate-100 text-slate-700 rounded-lg font-medium">
                {t}
              </span>
            ))}
          </div>
        </Section>
      )}

      {/* 可复用结构 */}
      {card.reusable_structure && (
        <Section icon="🔧" title="可复用文案结构">
          <div className="flex items-start justify-between gap-3">
            <p className="text-violet-700 font-mono text-sm leading-relaxed bg-violet-50 rounded-xl px-4 py-3 flex-1">
              {card.reusable_structure}
            </p>
            <button
              onClick={copyStructure}
              className="shrink-0 text-xs px-3 py-2 rounded-lg bg-slate-100 text-slate-600 hover:bg-violet-100 hover:text-violet-700 transition-colors"
            >
              {copied ? "✓ 已复制" : "复制"}
            </button>
          </div>
        </Section>
      )}

      {/* 原始文案 */}
      {card.transcript && (
        <Section icon="📝" title="原始文案">
          <pre className="text-slate-600 text-sm leading-relaxed whitespace-pre-wrap font-sans bg-slate-50 rounded-xl p-4">
            {card.transcript}
          </pre>
        </Section>
      )}
    </div>
  );
}

function Section({ icon, title, children }: { icon: string; title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
      <h2 className="flex items-center gap-2 font-semibold text-slate-700 text-sm mb-4">
        <span>{icon}</span>
        <span>{title}</span>
      </h2>
      {children}
    </div>
  );
}
