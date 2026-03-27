import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "知识卡片",
  description: "将抖音短视频链接转化为结构化知识卡片",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-[#f8f7ff]">
        <header className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b border-slate-100">
          <div className="max-w-6xl mx-auto px-6 h-14 flex items-center gap-3">
            <span className="text-xl">🧠</span>
            <span className="font-bold text-slate-800 text-lg tracking-tight">知识卡片</span>
            <span className="text-xs text-slate-400 ml-1">· 短视频文案精华库</span>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
