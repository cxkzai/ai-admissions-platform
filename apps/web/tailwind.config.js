/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // ===== 深夜 IDE 主题色 =====
        ink: {
          950: '#0B1437',  // 主背景 - 深夜蓝
          900: '#11183D',  // 次背景
          800: '#1A1F4B',  // 卡片背景
          700: '#2D3470',  // 浮层
          500: '#6B7280',  // 辅助文本
          300: '#B8BCC9',  // 次文本
          100: '#F5F5F7',  // 主文本
        },
        // ===== 教培温暖 + 编程勇气 =====
        spark: {
          DEFAULT: '#FF6B35',  // 暖橙
          light: '#FF8F66',
          dark: '#E54B17',
        },
        // ===== 成功转化 =====
        grow: {
          DEFAULT: '#7FD959',  // 柠檬绿
          dark: '#5BBA38',
        },
        // ===== 信息青 =====
        signal: {
          DEFAULT: '#38BDF8',
          dark: '#0284C7',
        },
      },
      fontFamily: {
        // 显示字体 - 程序员字体（终端风）
        display: ['JetBrains Mono', 'Fira Code', 'Menlo', 'monospace'],
        // 正文字体 - 现代无衬线
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        // 等宽字体 - 代码 / 标签
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontSize: {
        // 故意把 display 字号做大，配合等宽字体形成冲击力
        'mega': ['clamp(3rem, 8vw, 6rem)', { lineHeight: '1', letterSpacing: '-0.04em' }],
      },
      animation: {
        'typing': 'typing 0.05s steps(1) forwards',
        'blink': 'blink 1s steps(1) infinite',
        'fade-in': 'fadeIn 0.4s ease-out forwards',
        'slide-up': 'slideUp 0.4s ease-out forwards',
        'pulse-dot': 'pulseDot 2s ease-in-out infinite',
      },
      keyframes: {
        typing: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        blink: {
          '0%, 50%': { opacity: '1' },
          '51%, 100%': { opacity: '0' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseDot: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.5', transform: 'scale(0.9)' },
        },
      },
      backgroundImage: {
        'grid': "linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};