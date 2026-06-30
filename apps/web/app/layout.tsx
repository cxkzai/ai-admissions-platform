import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'AI-Admissions Platform · 教培机构 AI 招生顾问',
  description:
    '多智能体 + RAG 知识库 + 自动化工作流，让招生主管 + 一线顾问团队效能翻倍。',
  keywords: ['AI', '教育', '招生', '智能体', 'RAG', '教培'],
  authors: [{ name: '张艺达' }],
  openGraph: {
    title: 'AI-Admissions Platform',
    description: '教培机构 AI 招生顾问平台',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" className={inter.variable}>
      <body className="min-h-screen bg-gray-50 font-sans">{children}</body>
    </html>
  );
}