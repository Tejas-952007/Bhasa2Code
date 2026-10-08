# Frontend Foundation & Bhasha2Code Workspace UI (T20)

## Overview

Task **T20** implements the first real user interface for Bhasha2Code: a minimalist, white-first, professional developer and study workspace built with **React** and **Vite**.

In adherence to the core design authority [DESIGN.md](file:///home/tejas/Desktop/Bhasa2code/docs/07_design/DESIGN.md), the interface deliberately avoids generic AI tropes (neon gradients, purple glowing cards, AI sparkles, robot illustrations) and instead creates a quiet, technical, distraction-free environment optimized for long coding and study sessions.

---

## Architectural Flow

```text
React 18 + Vite 5 Frontend
         ↓
AppShell (Header + Collapsible Sidebar)
         ↓
Workspace Router / Views
  ├── Chat Workspace (Normal & Study Mode)
  ├── Notes Page (Notebook study view)
  ├── Saved Page (Bookmarked solutions)
  ├── Search Page (Local session & note querying)
  └── Settings Modal (Appearance, Model, Sandbox, Storage)
         ↓
Local Demo State Service (Deterministic Workspace Data)
         ↓
[Future T21: FastAPI Client ↔ T14–T19 NLP/LLM/Validation/Sandbox Pipeline]
```

> **API Boundary Note**: In accordance with the T20 scope, the frontend does **not** call backend FastAPI endpoints. Clean service boundaries are prepared in `src/services/` for subsequent integration in task **T21**.

---

## Technology Stack

- **Framework**: React 18 (`react`, `react-dom`)
- **Build Tool**: Vite 5 (`vite`, `@vitejs/plugin-react`)
- **Icons**: `lucide-react` (clean, technical, lightweight SVG icon set)
- **Styling**: Modern Vanilla CSS with CSS custom properties (`tokens.css`, `main.css`)
- **Bundle**: Zero heavy UI frameworks (no Tailwind, Bootstrap, Material UI, or bloated animation libraries)

---

## Component Architecture

```text
frontend/src/
├── components/
│   ├── common/
│   │   ├── Button.jsx            # Reusable button with variants (primary, secondary, ghost, subtle)
│   │   ├── Status.jsx            # Model status indicator (● Local · Ready)
│   │   └── EmptyState.jsx        # Refined empty workspace with prompt suggestions
│   ├── code/
│   │   ├── CodeArtifact.jsx      # Monospace code block, line numbers, inline editor & sandbox console
│   │   ├── CodeToolbar.jsx       # Action toolbar (Copy, Edit, Validate, Run)
│   │   └── ValidationStatus.jsx  # Status badges (Validated, Ran successfully, etc.)
│   ├── study/
│   │   ├── StudyToggle.jsx       # Segmented switch: Normal | Study
│   │   └── StudySections.jsx     # Problem understanding, Algorithm, Flowchart, Viva questions
│   ├── chat/
│   │   ├── ChatWorkspace.jsx     # Document-style message stream & context header
│   │   ├── UserMessage.jsx       # Document-style user message with language indicator
│   │   ├── AssistantMessage.jsx  # Modular response (Text, Code, Explanation, Example, Study)
│   │   └── Composer.jsx          # Multiline auto-expanding prompt input
│   └── layout/
│       ├── AppShell.jsx          # Top-level viewport wrapper & modal host
│       ├── Header.jsx            # Minimal header (Wordmark, Study toggle, Model status, Settings)
│       └── Sidebar.jsx           # Narrow quiet sidebar (New chat, Recent sessions, Nav, Settings)
├── pages/
│   ├── NotesPage.jsx             # Lightweight study notebook
│   ├── SavedPage.jsx             # Bookmarked items and code snippets
│   ├── SearchPage.jsx            # Instant workspace query interface
│   └── SettingsPage.jsx          # Compact settings dialog
├── services/
│   └── mockData.js               # Deterministic demo data (sessions, messages, notes)
├── styles/
│   ├── tokens.css                # Color, typography, spacing, and radius variables
│   └── main.css                  # Global reset, typography, and scrollbar styling
├── App.jsx                       # Session state management and view routing
└── main.jsx                      # Vite entrypoint
```

---

## Visual Design System

### 1. Color Palette (Restrained, White-First)
- **Canvas / App Background**: `#f8f9fa` (soft off-white)
- **Surface / Card Background**: `#ffffff` (crisp white)
- **Subtle Background / Active State**: `#f1f3f5` / `#f9fafb`
- **Primary Text**: `#111827` (near black, high contrast)
- **Secondary Text**: `#4b5563` (neutral slate)
- **Borders & Dividers**: `#e5e7eb` (subtle light gray)
- **Primary Accent**: `#2563eb` (professional blue)
- **Semantic Status**:
  - Success: `#059669` (emerald green badge & borders)
  - Error: `#dc2626` (subtle red)
  - Warning: `#d97706` (warm amber)

### 2. Typography
- **UI Elements**: Inter / system-ui sans-serif
- **Code Elements**: JetBrains Mono / monospace
- **Hierarchy**: Restrained sizing (`0.75rem` to `1.5rem`) without decorative display fonts

### 3. Code Artifact
- Displays source code with numbered lines and monospace formatting
- Includes language badge and status indicators (`✓ Validated`, `✓ Ran successfully (152ms)`)
- Provides an action toolbar with **Copy**, **Edit** (toggles inline editor with live line numbers), **Validate**, and **Run** (executes simulated sandbox output)
- Features a collapsible dark sandbox output console (`Duration: 152.4ms`)

### 4. Study Mode Integration
- Accessible via a persistent `Normal | Study` toggle in the top header
- Expands assistant messages to provide structured technical learning:
  - **Problem Understanding**
  - **Algorithm** (step-by-step procedural breakdown)
  - **Flowchart** (clean ASCII/Unicode decision tree)
  - **Important Points** (defensive practices and edge cases)
  - **Viva Questions & Answers** (exam and interview questions)

---

## Responsive Strategy

Tested and validated on desktop and laptop widths:
- **1920×1080 / 1440×900**: Spacious dual-column workspace with a 240px sidebar and centered 820px readable chat stream.
- **1024×768**: Header and composer adapt smoothly; code blocks and flowcharts feature horizontal scroll containers without breaking layout boundaries.
- **Collapsible Sidebar**: Sidebar can be hidden via the menu icon for maximum coding workspace focus.

---

## Accessibility Guarantees

- **Keyboard Navigation**: Multiline textarea sends on `Enter`, inserts line breaks on `Shift + Enter`.
- **Focus Rings**: Distinct, accessible `2px solid var(--accent-primary)` focus indicators on all interactive inputs.
- **Contrast**: Text contrast strictly complies with WCAG AA guidelines (dark slate on white/off-white surfaces).
- **Semantics**: Native `<button>`, `<textarea>`, `<header>`, `<main>`, `<aside>`, and semantic headings throughout.

---

## Build & Validation Commands

Install dependencies:
```bash
npm install
```

Start local dev server:
```bash
npm run dev
```

Build production bundle:
```bash
npm run build
```
*(Production build verified: 195 kB JS bundle, 3 kB CSS, zero warnings or errors).*
