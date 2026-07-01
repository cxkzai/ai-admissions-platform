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
        // ===== 浅色主题：ink 数字越大颜色越深 =====
        ink: {
          50:  '#FAF8F5',   // 主背景（温暖米白）
          100: '#FFFFFF',   // 卡片背景
          200: '#F5F5F4',   // 次背景
          300: '#E7E5E4',   // 边框/分隔线
          400: '#D6D3D1',   // 强边框
          500: '#A8A29E',   // 辅助文本
          600: '#78716C',   // 次文本
          700: '#57534E',   // 主次文本
          800: '#44403C',   // 强文本
          900: '#1C1917',   // 主文本
          950: '#0C0A09',   // 最深文本/标题
        },
        // ===== 品牌色：light mode 用稍深版本保证对比度 =====
        spark: {
          DEFAULT: '#EA580C',  // 暖橙（orange-600）
          light:   '#F97316',
          dark:    '#C2410C',
        },
        grow: {
          DEFAULT: '#16A34A',  // 绿（green-600）
          dark:    '#15803D',
        },
        signal: {
          DEFAULT: '#0284C7',  // 青（sky-600）
          dark:    '#0369A1',
        },
      },
      fontFamily: {
        // 显示字体 - 程序员字体（保留作为 signature element）
        display: ['JetBrains Mono', 'Fira Code', 'Menlo', 'monospace'],
        // 正文字体 - 现代无衬线（家长友好）
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
        'grid': "linear-gradient(rgba(28,25,23,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(28,25,23,0.04) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};