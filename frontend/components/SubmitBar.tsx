"use client";
import { useState } from "react";
import { api } from "@/lib/api";

interface Props {
  onCreated: () => void;
}

export default function SubmitBar({ onCreated }: Props) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;
    setError("");
    setLoading(true);
    try {
      await api.createCard(url.trim());
      setUrl("");
      onCreated();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "提交失败，请重试");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🔗</span>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="粘贴抖音视频链接，例如 https://v.douyin.com/xxxxxx"
            className="w-full pl-9 pr-4 py-3 rounded-xl border border-slate-200 bg-white text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-400 focus:border-transparent text-sm shadow-sm"
            disabled={loading}
          />
        </div>
        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="px-6 py-3 rounded-xl bg-violet-600 text-white font-medium text-sm hover:bg-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm whitespace-nowrap"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              处理中
            </span>
          ) : (
            "生成卡片"
          )}
        </button>
      </div>
      {error && <p className="mt-2 text-red-500 text-xs">{error}</p>}
    </form>
  );
}
