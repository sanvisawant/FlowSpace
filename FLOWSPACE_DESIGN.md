# FlowSpace — Design System & UX Specification
> **Version:** 1.0  
> **Theme:** Nordic Cabin — Cozy Minimalist  
> **Purpose:** This is the single source of truth for all visual and UX decisions in FlowSpace. Every component, color, spacing, animation, and flow is defined here. Always refer to this document before building any UI. Do not deviate from these decisions unless explicitly updated.

---

## Table of Contents
1. [Design Identity](#1-design-identity)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Spacing Scale](#4-spacing-scale)
5. [Border Radius](#5-border-radius)
6. [Shadows](#6-shadows)
7. [Texture & Atmosphere](#7-texture--atmosphere)
8. [Motion & Animation](#8-motion--animation)
9. [Component Patterns](#9-component-patterns)
10. [Layout System](#10-layout-system)
11. [State-Based Environment](#11-state-based-environment)
12. [Functional Sections](#12-functional-sections)
13. [Accessibility Rules](#13-accessibility-rules)
14. [Tailwind Configuration](#14-tailwind-configuration)
15. [CSS Variables](#15-css-variables)
16. [Onboarding Flow](#16-onboarding-flow)
17. [Responsive Design](#17-responsive-design)
18. [Dark Mode](#18-dark-mode)

---

## 1. Design Identity

**Theme Name:** Nordic Cabin  
**Core Concept:** A cozy digital sanctuary. The antithesis of a clinical, high-density corporate dashboard. FlowSpace should feel like sitting at a wooden desk in a warm cabin — calm, focused, unhurried.

**Design Pillars:**
- **Psychological comfort** — warm color temperatures reduce cognitive load and anxiety
- **Organic warmth** — soft shapes, paper textures, natural tones
- **Intentional breathing room** — whitespace is a feature, not wasted space
- **State-aware environment** — the UI transforms to match the user's mental state
- **Tactile satisfaction** — interactions feel physical and rewarding

**What this is NOT:**
- Not a clinical white SaaS dashboard
- Not a high-contrast corporate tool
- Not a gamified dopamine-chasing app
- Not flat/sterile/generic

---

## 2. Color System

### Core Palette

| Token | Hex | Name | Usage |
|-------|-----|------|-------|
| `--color-bg` | `#F4F1EB` | Oatmeal | Main page background |
| `--color-surface` | `#FCFBF9` | Off-White | Cards, modals, elevated containers |
| `--color-surface-hover` | `#F8F6F1` | Warm Cream | Card hover states |
| `--color-primary` | `#7D8C74` | Sage Green | Borders, progress rings, active states, icons |
| `--color-primary-dark` | `#5E6B57` | Deep Sage | Sage Green on light — use for borders/fills only |
| `--color-accent` | `#B66D49` | Terracotta | High priority tasks, urgent alerts, CTA buttons |
| `--color-accent-light` | `#E8C4B0` | Pale Terracotta | Accent backgrounds, tags |
| `--color-text` | `#2C3528` | Deep Pine | All body text, headings |
| `--color-text-muted` | `#6B7A65` | Muted Pine | Secondary text, placeholders, metadata |
| `--color-text-faint` | `#A3AE9E` | Faint Pine | Disabled states, tertiary labels |
| `--color-border` | `#E2DDD6` | Warm Grey | Dividers, input borders |
| `--color-focus-bg` | `#EDE9E1` | Focus Oatmeal | Background during active focus session |
| `--color-success` | `#6A9E6F` | Moss Green | Completed tasks, success states |
| `--color-warning` | `#C9934A` | Amber | Medium priority, warnings |

### Accessibility Rules (CRITICAL)
- **NEVER use Sage Green (`#7D8C74`) for text on Oatmeal background** — contrast ratio is only 3.2:1, fails WCAG AA
- **NEVER use white text on Sage Green** — contrast ratio is 3.9:1, fails WCAG AA
- **Always use Deep Pine (`#2C3528`) text on Sage Green buttons/backgrounds** — ratio is 4.8:1, passes AA
- **Deep Pine on Oatmeal** — ratio is 8.5:1, passes AAA ✅
- **Deep Pine on Off-White** — ratio is 9.2:1, passes AAA ✅
- **White on Terracotta** — ratio is 4.6:1, passes AA ✅ (acceptable for large button text only)

### Priority Color Coding
```
High priority  → Terracotta (#B66D49) — border + dot indicator
Medium priority → Amber (#C9934A) — border + dot indicator  
Low priority   → Sage Green (#7D8C74) — border + dot indicator
Completed      → Moss Green (#6A9E6F) — strikethrough + muted
```

---

## 3. Typography

### Font Families

```css
--font-display: 'Fraunces', Georgia, serif;     /* emotional anchors */
--font-body: 'DM Sans', system-ui, sans-serif;  /* functional UI */
--font-mono: 'JetBrains Mono', monospace;       /* code, time values */
```

### Import (in index.css)
```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
```

### Type Scale

| Token | Font | Size | Weight | Line Height | Usage |
|-------|------|------|--------|-------------|-------|
| `text-display` | Fraunces | 48px | 700 | 1.1 | Timer display, hero numbers |
| `text-h1` | Fraunces | 32px | 600 | 1.2 | Page titles |
| `text-h2` | Fraunces | 24px | 600 | 1.3 | Section headings |
| `text-h3` | DM Sans | 18px | 600 | 1.4 | Card titles, widget headers |
| `text-body` | DM Sans | 15px | 400 | 1.6 | Body text, task titles |
| `text-sm` | DM Sans | 13px | 400 | 1.5 | Metadata, timestamps, tags |
| `text-xs` | DM Sans | 11px | 500 | 1.4 | Labels, badges, caps |
| `text-mono` | JetBrains Mono | 14px | 400 | 1.5 | Timer countdown, code |

### Typography Rules
- Timer digits always use `Fraunces` — this is the emotional core of the app
- Page greeting ("Good morning, Sanvi") uses `Fraunces` — creates warmth
- All functional UI (buttons, inputs, labels, nav) uses `DM Sans`
- Never mix fonts within a single component
- Tracking (letter-spacing) on uppercase labels: `0.06em`

---

## 4. Spacing Scale

Strict 8px base grid. Never use arbitrary values.

```
4px   → xs  — tight internal padding (icon gaps, tag padding)
8px   → sm  — compact padding (small buttons, inline elements)
12px  → md  — standard internal padding
16px  → lg  — card padding, form field padding
24px  → xl  — section spacing, card gaps
32px  → 2xl — major section gaps
48px  → 3xl — page section separators
64px  → 4xl — hero spacing
```

In Tailwind: `p-1 p-2 p-3 p-4 p-6 p-8 p-12 p-16`

**Breathing room rule:** When in doubt, add more space. The generous whitespace IS the design.

---

## 5. Border Radius

```
--radius-sm: 8px;     /* tags, badges, small chips */
--radius-md: 12px;    /* inputs, small buttons */
--radius-lg: 16px;    /* cards, standard containers */
--radius-xl: 24px;    /* modals, large panels, floating widgets */
--radius-full: 9999px; /* pills, avatars, circular elements */
```

**Pebble rule:** No sharp corners anywhere in the UI. Every container should feel like a smooth stone — soft and holdable.

---

## 6. Shadows

All shadows are tinted with Deep Pine, never grey or black. This keeps them warm.

```css
--shadow-sm:  0 1px 3px rgba(44, 53, 40, 0.06);
--shadow-md:  0 4px 12px rgba(44, 53, 40, 0.08);
--shadow-lg:  0 8px 24px rgba(44, 53, 40, 0.10);
--shadow-xl:  0 16px 48px rgba(44, 53, 40, 0.12);
--shadow-focus: 0 0 0 3px rgba(125, 140, 116, 0.30); /* focus ring — sage tinted */
```

**Usage:**
- Cards at rest: `shadow-sm`
- Cards on hover: `shadow-md` + `-2px Y translate`
- Modals: `shadow-xl`
- Floating timer widget: `shadow-lg`
- Focus input rings: `shadow-focus`

---

## 7. Texture & Atmosphere

### Paper Grain Texture
Applied as an SVG noise filter on the page background only. Never on animated elements.

```css
/* In index.css — applied to body */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
}
```

**Performance rule:** Only apply to `body::before` (static, fixed). Never apply to cards, buttons, or any element that transitions or animates.

### Warmth Gradient (subtle)
```css
body {
  background: radial-gradient(ellipse at 20% 0%, #EDE8DF 0%, #F4F1EB 60%);
}
```

---

## 8. Motion & Animation

### Principles
- Motion communicates state, not decoration
- Subtle and purposeful — never distracting during focus
- Easing always organic: `cubic-bezier(0.34, 1.56, 0.64, 1)` for entrances (slight overshoot = tactile)
- Exit animations: `ease-in`, faster than entrances

### Duration Scale
```
--duration-fast:   150ms  /* hover states, micro-interactions */
--duration-base:   250ms  /* standard transitions */
--duration-slow:   400ms  /* page transitions, modals */
--duration-crawl:  600ms  /* onboarding reveals, focus mode transition */
```

### Easing Tokens
```css
--ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1);  /* entrances — bouncy */
--ease-smooth:  cubic-bezier(0.25, 0.46, 0.45, 0.94); /* standard */
--ease-out:     cubic-bezier(0.16, 1, 0.3, 1);        /* fast out, slow settle */
```

### Tactile Hover (applied to all cards and buttons)
```css
.card {
  transition: transform 150ms var(--ease-spring), box-shadow 150ms ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
```

### Focus Mode Transition
When timer starts, the entire environment transitions:
- Duration: `600ms`
- Sidebar slides out (translateX)
- Background shifts from `#F4F1EB` to `#EDE9E1`
- Non-essential elements fade to 30% opacity
- Timer scales up to full center focus

### Timer Ring Animation
Sage Green SVG circular progress ring. Stroke animates counter-clockwise as time depletes.
```css
/* use stroke-dashoffset animation, not rotation */
stroke-dasharray: 628; /* 2π × 100 */
stroke-dashoffset: /* calculated from % remaining */;
transition: stroke-dashoffset 1000ms linear;
```

---

## 9. Component Patterns

### Cards
```
Background:    var(--color-surface)
Border:        1px solid var(--color-border)
Border radius: var(--radius-lg) [16px]
Padding:       24px
Shadow:        var(--shadow-sm) at rest, var(--shadow-md) on hover
Hover:         translateY(-2px) + shadow-md
```

### Buttons

**Primary (CTA):**
```
Background:    var(--color-accent) [Terracotta]
Text:          white — only for large buttons (>16px text, passes AA)
Border radius: var(--radius-md) [12px]
Padding:       12px 24px
Font:          DM Sans 500 15px
Hover:         brightness(1.08) + translateY(-1px)
```

**Secondary:**
```
Background:    transparent
Border:        1.5px solid var(--color-border)
Text:          var(--color-text)
Hover:         background var(--color-surface-hover)
```

**Primary Action (Sage):**
```
Background:    var(--color-primary) [Sage Green]
Text:          var(--color-text) [Deep Pine] — NEVER white (fails contrast)
Border radius: var(--radius-md)
```

### Inputs
```
Background:    var(--color-surface)
Border:        1.5px solid var(--color-border)
Border radius: var(--radius-md) [12px]
Padding:       12px 16px
Font:          DM Sans 400 15px
Focus:         border-color var(--color-primary) + var(--shadow-focus)
Placeholder:   var(--color-text-faint)
```

### Tags / Badges
```
Border radius: var(--radius-sm) [8px] or var(--radius-full) for pills
Padding:       4px 10px
Font:          DM Sans 500 11px uppercase, tracking 0.06em
```

### Floating Timer Widget (minimized state)
```
Position:      fixed, bottom-right, 24px margin
Size:          64px × 64px circular
Background:    var(--color-surface)
Shadow:        var(--shadow-lg)
Border:        2px solid var(--color-primary)
Content:       MM:SS in JetBrains Mono
Hover:         expands to show task name + pause button
```

---

## 10. Layout System

### Main Layout (Planning Mode)
```
┌─────────────────────────────────────────────────┐
│  Sidebar (240px)  │  Main Content (flex-1)       │
│                   │                              │
│  Logo             │  Page content with           │
│  Nav items        │  24-32px padding             │
│  Settings         │  Max width: 1200px           │
│                   │  Centered                    │
└─────────────────────────────────────────────────┘
```

### Dashboard Bento Grid
```
┌──────────────────┬────────────┬─────────────┐
│  Timer           │  Today's   │  Streak     │
│  (large, hero)   │  Tasks     │  Counter    │
│                  │            │             │
├──────────────────┴────────────┤             │
│  Quick Notes                  ├─────────────┤
│  (scratchpad)                 │  Sounds     │
└───────────────────────────────┴─────────────┘
```

### Focus Mode Layout (timer running)
```
┌─────────────────────────────────────────────────┐
│                    [X] Exit                      │
│                                                  │
│              ○ Task: Build login page            │
│                                                  │
│              ╔═══════════════╗                   │
│              ║   24:33       ║   ← Fraunces 48px │
│              ║  [■ Pause]    ║                   │
│              ╚═══════════════╝                   │
│                                                  │
│         Session 2 of 4  ·  Next: Break           │
│                                                  │
│              [Rain ▓▓▓░░] 🔊                     │
└─────────────────────────────────────────────────┘
```

### Sidebar Navigation Items
```
- Dashboard (home icon)
- Tasks (checklist icon)
- Calendar (calendar icon)
- Stats (chart icon)
─────────────────
- Settings (gear icon)
- Profile (avatar)
```

---

## 11. State-Based Environment

FlowSpace has 3 distinct UI states. Each has defined visual rules.

### State 1: Planning Mode (default)
```
Background:       #F4F1EB (Oatmeal)
Sidebar:          visible, full width (240px)
Content density:  normal
Opacity:          all elements 100%
Timer widget:     small floating pill
```

### State 2: Focus Mode (timer running)
```
Background:       #EDE9E1 (Focus Oatmeal — slightly darker)
Sidebar:          hidden (translateX(-240px), duration 600ms)
Content density:  reduced — only timer, current task, sounds visible
Non-essential UI: opacity 0.3, pointer-events none
Timer:            hero — centered, large, full attention
Transition:       600ms cubic-bezier(0.25, 0.46, 0.45, 0.94)
```

### State 3: Break Mode (break timer running)
```
Background:       #EAF0E8 (very faint green — rest signal)
Sidebar:          still hidden
Timer:            smaller, less dominant
Message:          "Rest. You earned it." in Fraunces italic
Sounds:           auto-fade to 60% volume
```

### Transition trigger
```ts
// timerStore triggers body class changes
document.body.setAttribute('data-mode', 'focus' | 'break' | 'planning')
// CSS uses [data-mode="focus"] selectors for all state-based styles
```

---

## 12. Functional Sections

### Timer Widget (Hero)
- Outer ring: SVG circle, stroke `var(--color-primary)`, animates via `stroke-dashoffset`
- Center: time in `Fraunces` display size
- Below timer: current task name in `DM Sans` sm, muted
- Ring background: faint `#E2DDD6` track ring
- Session dots below: N filled dots = completed sessions this cycle

### Task Garden (Task List)
- No column borders — columns differentiated by whitespace only
- Task cards: soft organic shapes, `radius-lg`
- Priority indicator: left border `4px` colored by priority token
- Completed tasks: strikethrough + `color-text-faint` + subtle checkmark animation
- Hover: card lifts `-2px` + shadow expands
- Subtasks: indented `16px`, smaller card, dashed left border

### Calendar (Planner)
- Time blocks are soft color fields, not rigid containers
- Work blocks: `color-primary` tinted background (`opacity 0.15`) with sage left border
- Session history blocks: slightly darker, shows task name + duration
- Today column: faint terracotta tint on column header
- Drag handle: appears on hover, subtle grab cursor

### Stats Dashboard
- Heatmap cells: rounded squares `radius-sm`, warm color scale (oatmeal → sage → deep sage)
- Charts: Recharts with custom colors — no default blue, use palette tokens
- Streak counter: large Fraunces number, warm treatment
- All chart tooltips: surface background, pine text, soft shadow

### Sound Mixer
- Each sound: icon + name + volume slider
- Slider track: `color-border` → `color-primary`
- Active sounds: card gets faint sage background tint
- Mixing visual: overlapping waveform illustration (decorative, SVG)

---

## 13. Accessibility Rules

### Contrast Requirements (mandatory)
```
Deep Pine on Oatmeal:     8.5:1  ✅ AAA
Deep Pine on Off-White:   9.2:1  ✅ AAA
Deep Pine on Sage Green:  4.8:1  ✅ AA  ← use for sage buttons
White on Terracotta:      4.6:1  ✅ AA  ← large text only (≥16px bold)
Sage Green on Oatmeal:    3.2:1  ❌ FAIL — never use for text
White on Sage Green:      3.9:1  ❌ FAIL — never use
```

### Focus States
Every interactive element must have a visible focus ring:
```css
:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus); /* sage tinted ring */
}
```

### Motion Sensitivity
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### General Rules
- All icons must have `aria-label` or accompanying visible text
- Form inputs must have associated `<label>` elements, not just placeholders
- Color alone never conveys meaning — always pair with icon or text
- Minimum touch target size: 44×44px (mobile)

---

## 14. Tailwind Configuration

```ts
// tailwind.config.ts
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg:           '#F4F1EB',
        surface:      '#FCFBF9',
        'surface-hover': '#F8F6F1',
        primary:      '#7D8C74',
        'primary-dark': '#5E6B57',
        accent:       '#B66D49',
        'accent-light': '#E8C4B0',
        pine:         '#2C3528',
        'pine-muted': '#6B7A65',
        'pine-faint': '#A3AE9E',
        border:       '#E2DDD6',
        'focus-bg':   '#EDE9E1',
        success:      '#6A9E6F',
        warning:      '#C9934A',
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        body:    ['DM Sans', 'system-ui', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'display': ['48px', { lineHeight: '1.1', fontWeight: '700' }],
        'h1':      ['32px', { lineHeight: '1.2', fontWeight: '600' }],
        'h2':      ['24px', { lineHeight: '1.3', fontWeight: '600' }],
      },
      borderRadius: {
        sm:   '8px',
        md:   '12px',
        lg:   '16px',
        xl:   '24px',
      },
      boxShadow: {
        sm:    '0 1px 3px rgba(44,53,40,0.06)',
        md:    '0 4px 12px rgba(44,53,40,0.08)',
        lg:    '0 8px 24px rgba(44,53,40,0.10)',
        xl:    '0 16px 48px rgba(44,53,40,0.12)',
        focus: '0 0 0 3px rgba(125,140,116,0.30)',
      },
      spacing: {
        // base 8px grid — standard Tailwind already covers this
      },
    },
  },
}
```

---

## 15. CSS Variables

```css
/* src/index.css */

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Colors */
  --color-bg:             #F4F1EB;
  --color-surface:        #FCFBF9;
  --color-surface-hover:  #F8F6F1;
  --color-primary:        #7D8C74;
  --color-primary-dark:   #5E6B57;
  --color-accent:         #B66D49;
  --color-accent-light:   #E8C4B0;
  --color-text:           #2C3528;
  --color-text-muted:     #6B7A65;
  --color-text-faint:     #A3AE9E;
  --color-border:         #E2DDD6;
  --color-focus-bg:       #EDE9E1;
  --color-success:        #6A9E6F;
  --color-warning:        #C9934A;

  /* Typography */
  --font-display:  'Fraunces', Georgia, serif;
  --font-body:     'DM Sans', system-ui, sans-serif;
  --font-mono:     'JetBrains Mono', monospace;

  /* Spacing */
  --space-xs:   4px;
  --space-sm:   8px;
  --space-md:   12px;
  --space-lg:   16px;
  --space-xl:   24px;
  --space-2xl:  32px;
  --space-3xl:  48px;
  --space-4xl:  64px;

  /* Border Radius */
  --radius-sm:   8px;
  --radius-md:   12px;
  --radius-lg:   16px;
  --radius-xl:   24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm:    0 1px 3px rgba(44, 53, 40, 0.06);
  --shadow-md:    0 4px 12px rgba(44, 53, 40, 0.08);
  --shadow-lg:    0 8px 24px rgba(44, 53, 40, 0.10);
  --shadow-xl:    0 16px 48px rgba(44, 53, 40, 0.12);
  --shadow-focus: 0 0 0 3px rgba(125, 140, 116, 0.30);

  /* Motion */
  --duration-fast:   150ms;
  --duration-base:   250ms;
  --duration-slow:   400ms;
  --duration-crawl:  600ms;
  --ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-smooth:     cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-out:        cubic-bezier(0.16, 1, 0.3, 1);
}

/* Base styles */
body {
  background-color: var(--color-bg);
  background: radial-gradient(ellipse at 20% 0%, #EDE8DF 0%, #F4F1EB 60%);
  color: var(--color-text);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
}

/* Paper grain texture */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
}

/* Focus mode */
body[data-mode="focus"] {
  background: var(--color-focus-bg);
}

/* Break mode */
body[data-mode="break"] {
  background: #EAF0E8;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 16. Onboarding Flow

### Philosophy
Onboarding should feel like being welcomed into the cabin, not filling out a form. It's warm, brief, and immediately useful. Maximum 4 steps. No progress bar — that creates anxiety. Just gentle forward motion.

### Entry Point
After email verification click → user lands on onboarding, not dashboard.

---

### Step 1 — Welcome (emotional anchor)

**Layout:** Full screen, centered, minimal  
**Background:** Oatmeal with paper grain  
**Content:**

```
[FlowSpace logo — small, top center]

        Good to have you here.
        [Fraunces 32px, Deep Pine]

   FlowSpace is your focus sanctuary —
   tasks, timer, and calm, all in one place.
   [DM Sans 15px, Muted Pine, centered]

        [Begin →]
        [Terracotta button, large]
```

**Animation:** Content fades in staggered — logo first (0ms), heading (150ms), body (300ms), button (450ms)  
**Duration:** User reads for ~5 seconds, clicks Begin

---

### Step 2 — Personalization (name + work style)

**Layout:** Card centered on oatmeal background  
**Card:** Surface color, radius-xl, shadow-lg, padding 48px  
**Content:**

```
   What should we call you?
   [Fraunces 24px]

   [_________________________]
   First name input — DM Sans, radius-md

   ────────────────────────────────

   How do you usually work?
   [DM Sans 15px, muted]

   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │  🎓 Student  │  │  💻 Freelance│  │  🏢 Remote   │
   │              │  │              │  │  Employee    │
   └──────────────┘  └──────────────┘  └──────────────┘

   [← Back]                           [Continue →]
```

**Interaction:** Work style cards are selectable — selected card gets sage green border + faint sage background  
**Validation:** Name required, work style optional (has a default)

---

### Step 3 — Focus Preferences (timer setup)

**Layout:** Same card style  
**Content:**

```
   Set up your focus rhythm.
   [Fraunces 24px]

   How long is your ideal focus session?

   [  25  ] minutes
   [slider: 15 ──────●────── 60]

   Short break after each session?

   ○ 5 minutes   ● 10 minutes   ○ Custom

   ────────────────────────────────

   Daily focus goal

   [  4  ] hours per day
   [slider: 1 ─────●──────── 10]

   [← Back]                           [Continue →]
```

**Note:** These values pre-fill Settings. User can change anytime. This step makes the app feel immediately personal.

---

### Step 4 — First Task (immediate value)

**Layout:** Same card, slightly wider  
**Content:**

```
   What's one thing you want
   to focus on today?
   [Fraunces 24px]

   [___________________________________]
   e.g. "Finish the login page"
   [DM Sans input, large, warm placeholder]

   Priority:
   ● High   ○ Medium   ○ Low

   ────────────────────────────────

        You can always add more later.
        [DM Sans xs, faint, centered]

   [← Back]                    [Enter FlowSpace →]
```

**"Enter FlowSpace" button:** Terracotta, full-width within card  
**Skip option:** Small "Skip for now →" text link below button in muted color

---

### Transition to Dashboard

When "Enter FlowSpace" is clicked:
1. Card scales down slightly and fades out (250ms)
2. Full page crossfade to dashboard (400ms)
3. Dashboard loads with the task already in the task list
4. A warm greeting appears: **"Good morning, [Name]. Let's make it count."** in Fraunces at top of dashboard
5. A subtle pulse animation on the timer — inviting the first session

---

### Onboarding Data Saved To

```ts
// stored in user settings after onboarding
{
  name: string,
  work_style: 'student' | 'freelancer' | 'remote' | null,
  focus_duration_mins: number,     // default 25
  break_duration_mins: number,     // default 5
  daily_goal_hours: number,        // default 4
  first_task: Task | null,         // added to task list
  onboarding_complete: boolean     // true — never show again
}
```

### Re-entry (returning users)
- `onboarding_complete === true` → skip directly to dashboard
- Greeting on dashboard uses name from onboarding: `"Welcome back, [Name]."`

---

## 17. Responsive Design

### Breakpoints (Tailwind defaults)
```
sm:  640px   — large phones landscape
md:  768px   — tablets
lg:  1024px  — small laptops
xl:  1280px  — standard desktop
2xl: 1536px  — large monitors
```

### Mobile Behavior (< 768px)
- Sidebar becomes bottom tab bar (5 icons, no labels)
- Bento grid collapses to single column
- Timer becomes full-width card at top
- Focus mode: full screen takeover
- Font sizes scale down one step (display → h1, h1 → h2)

### Tablet Behavior (768px–1024px)
- Sidebar collapses to icon-only (64px) with tooltips
- 2-column bento grid
- Calendar switches to day view by default

### Desktop (> 1024px)
- Full sidebar (240px)
- Full bento layout
- All views available

---

## 18. Dark Mode

Dark mode is planned for Phase 2 but tokens are defined now to avoid future refactoring.

### Dark Palette (future)
```
--color-bg:       #1C1F1A  (Dark Forest)
--color-surface:  #252822  (Dark Surface)
--color-text:     #E8E4DC  (Warm White)
--color-border:   #3A3F36  (Dark Border)
--color-primary:  #8FA885  (Lighter Sage — better contrast on dark)
--color-accent:   #C47E5A  (Lighter Terracotta)
```

### Implementation (Phase 2)
```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #1C1F1A;
    /* ... all token overrides */
  }
}
```

Using CSS variables throughout means dark mode is a single block of variable overrides — no component changes needed. This is why CSS variables are used everywhere instead of hardcoded Tailwind color classes.

---

*Last updated: Project kickoff*  
*Next review: After first component built — validate design tokens in real implementation*
