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

# CODSOFT

A collection of Java projects completed as part of the **CodSoft Java Programming Internship**. Each task demonstrates core Java concepts including OOP, file I/O, API integration, and user interaction via the console.

---

## 📁 Project Structure

```
CODSOFT/
├── Task 1/
│   └── GuessingGame.java
├── Task 2/
│   └── StudentGradeCalculator.java
├── Task 3/
│   ├── ATM.java
│   └── BankAccount.java
├── Task 4/
│   └── CurrencyConverter.java
└── Task 5/
    ├── Main.java
    ├── Student.java
    └── StudentManagementSystem.java
```

---

## ✅ Tasks Overview

### Task 1 — Number Guessing Game
**File:** `Task 1/GuessingGame.java`

A console-based guessing game where the player tries to guess a randomly generated number between 1 and 100.

**Features:**
- Random number generation using `java.util.Random`
- Maximum of **7 attempts** per round
- Hints after each wrong guess (too high / too low)
- **Score system** — fewer attempts = higher score
- Multi-round support with a play-again prompt
- Input validation with graceful error handling

---

### Task 2 — Student Grade Calculator
**File:** `Task 2/StudentGradeCalculator.java`

Calculates the total marks, average percentage, and letter grade for a student based on subject-wise input.

**Features:**
- Accepts marks for any number of subjects (out of 100)
- Validates input to ensure marks are within range (0–100)
- Computes average percentage and assigns a letter grade:

| Percentage | Grade |
|------------|-------|
| ≥ 90       | A+    |
| ≥ 80       | A     |
| ≥ 70       | B     |
| ≥ 60       | C     |
| ≥ 50       | D     |
| < 50       | F     |

---

### Task 3 — ATM Interface
**Files:** `Task 3/ATM.java`, `Task 3/BankAccount.java`

Simulates a basic ATM machine with a linked bank account.

**Features:**
- Separate `BankAccount` class managing balance logic
- `ATM` class handles the user interface and menu
- Operations supported:
  - Check Balance
  - Deposit
  - Withdraw (with insufficient funds check)
- Default starting balance: **$1000.00**
- Input validation and clear feedback messages

---

### Task 4 — Currency Converter
**File:** `Task 4/CurrencyConverter.java`

Converts a given amount from one currency to another using live exchange rates fetched from an external API.

**Features:**
- Integrates with [ExchangeRate-API](https://www.exchangerate-api.com/) for real-time rates
- Supports any standard currency code (e.g., USD, EUR, INR, GBP)
- Raw JSON parsing without external libraries
- HTTP connection via `java.net.HttpURLConnection`
- Error handling for invalid currencies and failed API calls

> **Note:** Requires a valid API key in `CurrencyConverter.java` at the `API_KEY` constant.

---

### Task 5 — Student Management System
**Files:** `Task 5/Main.java`, `Task 5/Student.java`, `Task 5/StudentManagementSystem.java`

A full-featured student records management system with persistent file storage.

**Features:**
- Add, remove, search, edit, and display student records
- Each student has: **Name**, **Roll Number**, **Grade**
- Duplicate roll number prevention
- Data persisted to `students.dat` using Java **Serialization** (`ObjectOutputStream` / `ObjectInputStream`)
- Data auto-loads on startup if a save file exists
- Robust input validation and error handling throughout

---

## 🛠️ How to Run

**Prerequisites:** Java JDK 8 or higher installed.

```bash
# Compile
javac Task\ 1/GuessingGame.java

# Run
java -cp Task\ 1 GuessingGame
```

Repeat the same steps for each task folder. For **Task 3**, compile both files together:

```bash
javac Task\ 3/ATM.java Task\ 3/BankAccount.java
java -cp Task\ 3 ATM
```

For **Task 5**, compile all three files:

```bash
javac Task\ 5/Main.java Task\ 5/Student.java Task\ 5/StudentManagementSystem.java
java -cp Task\ 5 Main
```

---

## 🧰 Technologies Used

- **Language:** Java (JDK 8+)
- **Libraries:** Standard Java (`java.util`, `java.io`, `java.net`)
- **External API:** ExchangeRate-API (Task 4)
- **Concepts:** OOP, File I/O, Serialization, HTTP Networking, Exception Handling

---

## 👨‍💻 Author

Developed as part of the **CodSoft Java Internship Program**.

Project work link :
<a href="https://drive.google.com/drive/folders/1gbYNH_W-9n_HWmp5x0QLl3RhXGRCzYDe?usp=drive_link" target="_blank"><b><span style="color:blue;">Check out my Works 👇</span></b></a>

---

