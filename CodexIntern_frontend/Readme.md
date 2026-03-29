# CODEXINTERN

Frontend development work completed as part of the **CodexIntern Frontend Internship Program** — focused on building a pixel-perfect clone of the [Coding Ninjas](https://www.codingninjas.com) platform.

---

## 📁 Project Structure

```
CodeXIntern-Frontend-/
├── CodeNINJA actual/          ← Production-grade clone (shadcn-ui + TypeScript)
└── coding-ninjas-clone(MY try)/  ← Personal scratch-built attempt (vanilla React + JS)
```

---

## 🚀 Projects Overview

### 1. CodeNINJA Actual
> **Tech Stack:** React 18 · TypeScript · Vite · Tailwind CSS · shadcn/ui · React Query

A fully featured, production-quality Coding Ninjas landing page clone built with the **Lovable** platform and an extensive component library.

**Pages & Components:**
- `Navbar` — Sticky nav with dropdown menus for working professionals and college students, responsive mobile menu
- `Hero` — Full-screen hero with an embedded **CourseFinderForm** (experience selector, topic dropdown, contact fields)
- `CourseCategories` — 6-category grid covering Web Dev, DSA, ML, System Design, UI/UX, and Data Science
- `Features` — Why Choose Coding Ninjas section with icon-based cards
- `Testimonials` — Alumni success stories with star ratings
- `Footer` — Multi-column footer with social links and legal pages

**Key Technical Highlights:**
- Full **Radix UI** primitive suite via shadcn/ui (accordions, dialogs, dropdowns, toasts, and 30+ more components)
- Custom **design tokens** in `index.css` — Coding Ninjas orange theme (`hsl(16 100% 60%)`), dark mode support, and CSS gradient variables
- `tailwind.config.ts` extended with custom `gradient-hero`, `gradient-primary`, `fade-in`, and `slide-in` animations
- Path aliasing via `@/` for clean imports, TypeScript strict-lite config
- `TanStack React Query` wired up for async data management
- `react-router-dom` v6 with a catch-all 404 page
- `Plus Jakarta Sans` as the primary font

**Run locally:**
```bash
cd "CodeNINJA actual"
npm install
npm run dev        # starts on port 8080
npm run build      # production build
```

---

### 2. coding-ninjas-clone (MY try)
> **Tech Stack:** React 19 · JavaScript · Vite · Tailwind CSS v4

A Coding Ninjas clone built **from scratch** without any UI library — all components written manually in plain React and Tailwind.

**Components Built:**
- `Header` — Responsive sticky navbar with hamburger mobile menu and Login/Sign Up buttons
- `Hero` — Gradient hero section with key stats (50K+ students placed, 300+ mentors, 1000+ companies, 4.8/5 rating)
- `Features` — 6-feature grid highlighting expert learning, mentorship, and placement support
- `Courses` — 6-course cards with pricing, duration, level tags, and a "Most Popular" badge
- `Stats` — Impact section with a full-width gradient background
- `Testimonials` — 3 alumni testimonial cards with star rendering
- `Footer` — 4-column link footer with social icons and copyright

**Key Technical Highlights:**
- Zero external component library — all UI from scratch
- Custom `gradient-bg` and `hover-scale` utility classes in `index.css`
- Demonstrates clear understanding of React component architecture and props-free stateless design
- Uses Tailwind CSS v4 (latest)

**Run locally:**
```bash
cd "coding-ninjas-clone(MY try)"
npm install
npm run dev
```

---

## 🛠️ Technologies Used

| Tool | Version | Used In |
|------|---------|---------|
| React | 18 / 19 | Both |
| TypeScript | 5.8 | CodeNINJA actual |
| JavaScript (JSX) | ES2020 | My try |
| Vite | 5.x / 7.x | Both |
| Tailwind CSS | 3.4 / 4.1 | Both |
| shadcn/ui + Radix UI | Latest | CodeNINJA actual |
| TanStack React Query | 5.x | CodeNINJA actual |
| React Router DOM | 6.x | CodeNINJA actual |
| Lucide React | 0.462 / 0.546 | Both |
| Recharts | 2.x | CodeNINJA actual |

---

## 🎯 Internship Context

This repository represents **Slab 2** work for the CodexIntern Frontend program. The assignment was to clone the Coding Ninjas landing page, demonstrating proficiency in modern React development, responsive design, and component-driven UI architecture.

Two approaches were explored:
- A **guided, tool-assisted** approach using Lovable + shadcn (CodeNINJA actual)
- A **self-built** approach using raw React and Tailwind (MY try)

---
