# FlowSpace — Product Requirements Document
> **Version:** 1.0  
> **Status:** Active  
> **Purpose:** This is the single source of truth for the FlowSpace project. Every architectural decision, feature, tech choice, and implementation detail is documented here. Always refer to this document before making any decision. Do not deviate from this unless explicitly updated.

---

## Table of Contents
1. [Product Overview](#1-product-overview)
2. [Target Users](#2-target-users)
3. [Core Problem](#3-core-problem)
4. [Competitors & Differentiation](#4-competitors--differentiation)
5. [Complete Feature List](#5-complete-feature-list)
6. [Tech Stack](#6-tech-stack)
7. [Architecture](#7-architecture)
8. [Folder Structure](#8-folder-structure)
9. [Database Schema](#9-database-schema)
10. [API Routes](#10-api-routes)
11. [Authentication Flow](#11-authentication-flow)
12. [AI Layer](#12-ai-layer)
13. [Chrome Extension](#13-chrome-extension)
14. [PWA](#14-pwa)
15. [Monetization](#15-monetization)
16. [Build Phases](#16-build-phases)
17. [Deployment](#17-deployment)
18. [Environment Variables](#18-environment-variables)
19. [Key Decisions & Rationale](#19-key-decisions--rationale)

---

## 1. Product Overview

**Name:** FlowSpace  
**Tagline:** Your entire work session, one tab.  
**Type:** Web app (PWA) + Chrome Extension  
**Description:** FlowSpace is an all-in-one focus and productivity web app that replaces the need for separate Pomodoro timers, task managers, calendars, note apps, and ambient sound tools. Everything needed for a focused work session lives in one place. Open it, work, close it.

---

## 2. Target Users

- Students
- Freelancers / solo workers
- Remote employees
- Anyone who uses 4+ productivity tools simultaneously

---

## 3. Core Problem

Productivity tools are scattered. People have:
- Notion for notes
- Todoist for tasks
- Toggl for time tracking
- Forest for focus
- Spotify for ambient sounds
- Google Calendar for scheduling

Switching between 6 apps kills focus. FlowSpace consolidates everything into one session-first workspace.

---

## 4. Competitors & Differentiation

| App | What it does | Gap |
|-----|-------------|-----|
| Focusplan | Timer + tasks + calendar | iPad only, no AI, no site blocking |
| Routine | Tasks + calendar + basic AI | No timer, no site blocking, no mood tracking |
| Focus To-Do | Timer + tasks + white noise | No calendar, no AI, no site blocking |
| Opal | Site blocking only | Does nothing else |
| Flow | Timer + site blocking | Mac only, no web, no AI |

**FlowSpace differentiators:**
- Only web-first (works on all devices, no install needed beyond PWA)
- Built-in Chrome Extension for real site blocking
- Mood tracking + burnout detection (nobody does this)
- LangGraph agentic AI pipeline (not just a single GPT call)
- Full session-linked calendar
- Ambient sound mixing built in

---

## 5. Complete Feature List

### 5.1 Authentication
- Email + password signup/login via Supabase Auth
- Google OAuth via Supabase Auth
- Guest mode (localStorage only, no account needed)
- Auth state managed in Zustand on frontend
- JWT verification on all FastAPI routes via Supabase JWT secret

### 5.2 Task Management
- Create, edit, delete tasks
- Priority levels: high, medium, low
- Due dates + time estimates (in minutes)
- Subtasks (nested under parent task)
- Tags / categories
- Mark complete
- Recurring tasks: daily, weekly
- Archive completed tasks
- Search tasks by title
- Filter by priority, tag, due date, completion status

### 5.3 Focus Timer
- Pomodoro mode: 25 min work / 5 min break
- Custom mode: user sets work duration, break duration, long break duration
- Long break after N sessions (configurable, default 4)
- Auto-start next session toggle
- Link session to a specific task
- Floating minimizable timer widget (visible across all pages)
- Timer state persists if user navigates within app
- Session is auto-logged to DB when completed

### 5.4 Calendar
- Day view, Week view, Month view
- Tasks appear on their due date, color coded by priority (red = high, amber = medium, blue = low)
- Completed focus sessions appear as time blocks on the calendar
- Manual deep work blocks: drag on calendar to create a block
- Drag and drop tasks to reschedule
- Click any time slot to instantly create a task or work block
- Click a logged session block to see details (duration, task, mood, focus score)
- Google Calendar sync (Phase 2)
- iCal export (Phase 2)

### 5.5 Focus Lock
**Soft Lock (default, all users):**
- Uses the Page Visibility API (`document.addEventListener('visibilitychange', ...)`)
- When user switches tab or minimizes during a session, session is flagged as "broken"
- Shame banner appears when user returns: "You left during your session"
- Broken session is logged in stats

**Hard Lock (via Chrome Extension, Pro users):**
- User defines a blocklist of domains (e.g. twitter.com, instagram.com, youtube.com)
- When timer starts, extension activates blocking rules via `declarativeNetRequest`
- Blocked sites redirect to `blocked.html` — a page showing the FlowSpace timer countdown and a motivational message
- Extension reads session state from `localStorage` key `flowspace_session`
- Blocking deactivates when timer stops or session ends

**Mobile Lock (PWA):**
- Full screen overlay if user tries to navigate away during session
- Cannot prevent OS-level app switching but logs every visibility loss

### 5.6 Chrome Extension
- Manifest V3
- Background service worker (`background.js`) reads session state
- `declarativeNetRequest` for blocking (no need to read page content — safer, faster)
- Popup (`popup.html`) shows current session status and blocklist manager
- Communicates with FlowSpace via `localStorage` (same origin) or a local API call
- `blocked.html` — redirect page with countdown timer and "Go back to FlowSpace" button
- Distributed as a separate installable extension, linked from FlowSpace settings page

### 5.7 Notes / Scratchpad
- Per-session scratchpad: opens fresh each session, auto-saved to DB on session end
- Global notepad: always-accessible freeform notes, persists indefinitely
- Markdown rendering support
- Notes can be optionally linked to a task
- Search across all notes

### 5.8 Ambient Sounds
- Built-in soundscapes: rain, café, forest, white noise, ocean, lo-fi beats
- Mix multiple sounds simultaneously (e.g. rain + café)
- Individual volume slider per active sound
- Sounds play during focus session
- Auto-pause on break (configurable toggle)
- Implemented with Web Audio API (no external service, no Spotify dependency)

### 5.9 Mood Check-in
- Shown before and after every focus session
- 1–5 emoji rating scale
- Optional one-line text note (e.g. "feeling tired", "very focused")
- Stored in session record in DB
- Used for mood vs productivity correlation in stats

### 5.10 Session Logging
Every completed focus session automatically logs:
- `user_id`
- `task_id` (if linked)
- `duration_minutes`
- `planned_duration_minutes`
- `mood_before` (1–5)
- `mood_after` (1–5)
- `focus_score` (0–100, calculated from: distraction attempts, breaks taken, completion)
- `distraction_attempts` (tab switches during session)
- `was_broken` (boolean)
- `started_at`, `ended_at`

### 5.11 Stats & Insights Dashboard
- Today summary: tasks completed, hours focused, focus score
- Weekly heatmap (GitHub contribution graph style) — days × intensity of work
- Most productive time of day (bar chart of focus hours by hour)
- Average session length over time (line chart)
- Streak tracker: consecutive days with at least 1 completed session
- Broken session rate (% of sessions marked broken)
- Distraction attempts over time (line chart)
- Daily / weekly / monthly total hours (toggle)
- Mood vs productivity scatter plot (Phase 2, after enough data)
- All charts built with Recharts

### 5.12 Settings
- Default timer durations (work, break, long break)
- Number of sessions before long break
- Daily work hours goal
- Notification preferences (break reminder, daily plan reminder)
- Theme: light / dark / system
- Accent color picker
- Start of week: Monday or Sunday
- Default calendar view: day / week / month
- Blocklist manager (for Chrome Extension)
- Sound preferences (default sounds, volumes)

### 5.13 PWA
- Vite PWA plugin with Workbox
- `manifest.json` with name, icons, theme color
- Service worker with offline caching for: timer, tasks, notes (cached from last sync)
- Push notifications: break reminders, daily plan prompt (8am)
- Installable on desktop and mobile from browser
- Full screen, no browser UI bar
- Mobile-optimized responsive layout

---

## 6. Tech Stack

### Frontend
| Tool | Purpose |
|------|---------|
| React 18 | UI framework |
| TypeScript | Type safety throughout |
| Vite | Build tool + dev server |
| Tailwind CSS v4 | Styling (via `@tailwindcss/vite` plugin) |
| Zustand | Global state management |
| React Router v6 | Client-side routing |
| Axios | HTTP client for FastAPI calls |
| Supabase JS Client | Auth only (login, signup, OAuth, session state) |
| Recharts | Charts and data visualizations |
| Vite PWA Plugin | PWA + service worker generation |
| Web Audio API | Ambient sound mixing (native browser API) |

### Backend
| Tool | Purpose |
|------|---------|
| Python 3.11+ | Language |
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| SQLAlchemy 2.0 | ORM |
| Alembic | Database migrations |
| Pydantic v2 | Request/response schemas |
| pydantic-settings | Environment variable management |
| PyJWT | Supabase JWT verification |
| PydanticAI | Structured AI outputs for simple agents |
| LangGraph | Multi-step agentic AI pipelines |
| Anthropic Python SDK | Claude API access |
| psycopg2-binary | PostgreSQL driver |

### Database
| Tool | Purpose |
|------|---------|
| PostgreSQL (via Supabase) | Primary database |
| Supabase Auth | Authentication + JWT issuance |

### Infrastructure
| Service | Purpose |
|---------|---------|
| Vercel | Frontend hosting |
| Railway | Backend (FastAPI) hosting |
| Supabase | PostgreSQL DB + Auth |
| UptimeRobot | Pings `/health` every 5 min to prevent Supabase free tier pausing |

### Chrome Extension
| Tool | Purpose |
|------|---------|
| Manifest V3 | Extension format |
| `declarativeNetRequest` | Site blocking API |
| Vanilla JS | No framework needed |

---

## 7. Architecture

### High-level flow
```
┌─────────────────────────────────────────┐
│           Frontend (React PWA)          │
│                                         │
│  Supabase JS ──→ Supabase Auth          │
│  (login/signup/OAuth/session state)     │
│                                         │
│  Axios ──→ FastAPI Backend              │
│  (tasks, sessions, AI, stats, notes,    │
│   calendar, settings — everything else) │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend (Railway)       │
│                                         │
│  1. Verifies Supabase JWT on every req  │
│  2. Extracts user_id from token         │
│  3. Runs business logic                 │
│  4. Calls AI layer (PydanticAI /        │
│     LangGraph) when needed              │
│  5. Reads/writes PostgreSQL             │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Supabase (PostgreSQL + Auth)       │
│                                         │
│  Auth: issues JWTs, handles OAuth       │
│  DB: stores all app data                │
└─────────────────────────────────────────┘
```

### JWT verification middleware
```python
# backend/app/core/deps.py
async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(
        token,
        settings.SUPABASE_JWT_SECRET,
        algorithms=["HS256"],
        audience="authenticated"
    )
    return payload["sub"]  # user UUID from Supabase
```

### Axios interceptor (auto-attaches token)
```ts
// frontend/src/api/client.ts
client.interceptors.request.use(async (config) => {
  const token = await getToken()  // from Supabase JS client
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
```

### Rule: Frontend never queries Supabase DB directly
The frontend only uses the Supabase JS client for auth. All data fetching goes through FastAPI. This keeps business logic centralized and the backend testable.

---

## 8. Folder Structure

```
flowspace/
├── .env.example
├── .gitignore
├── README.md
├── docker-compose.yml              # only for local dev reference, not used in prod

├── frontend/
│   ├── index.html
│   ├── vite.config.ts              # Vite + PWA plugin + Tailwind plugin
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── .eslintrc.json
│   ├── public/
│   │   ├── manifest.json           # PWA manifest
│   │   └── icons/                  # 192x192, 512x512 app icons
│   └── src/
│       ├── main.tsx
│       ├── App.tsx                 # routes + auth init
│       ├── index.css
│       ├── lib/
│       │   └── supabase.ts         # Supabase client instance (single source)
│       ├── components/
│       │   ├── ui/                 # Button, Modal, Input, Badge, Toggle
│       │   ├── layout/             # Sidebar, Navbar, PageWrapper
│       │   ├── timer/              # TimerWidget, TimerControls, SessionLinker
│       │   ├── tasks/              # TaskList, TaskCard, TaskForm, SubtaskList
│       │   ├── calendar/           # CalendarView, DayView, WeekView, MonthView
│       │   ├── notes/              # Scratchpad, GlobalNotepad
│       │   ├── sounds/             # SoundMixer, SoundTrack, VolumeSlider
│       │   ├── stats/              # Heatmap, FocusChart, StreakCounter
│       │   └── ai/                 # PlanMyDay, TaskBreakdown, SessionKickstarter
│       ├── pages/
│       │   ├── Dashboard.tsx       # main workspace (timer + tasks + notes)
│       │   ├── Login.tsx
│       │   ├── Register.tsx
│       │   ├── Calendar.tsx
│       │   ├── Stats.tsx
│       │   └── Settings.tsx
│       ├── store/
│       │   ├── authStore.ts        # user, loading, init()
│       │   ├── taskStore.ts        # tasks[], addTask, updateTask, deleteTask
│       │   ├── timerStore.ts       # mode, timeLeft, isRunning, sessionCount
│       │   └── sessionStore.ts     # currentSession, logs[]
│       ├── hooks/
│       │   ├── useTimer.ts         # timer tick logic, session transitions
│       │   ├── useAuth.ts          # current user, loading state
│       │   └── useVisibility.ts    # Page Visibility API, tab switch detection
│       ├── api/
│       │   ├── client.ts           # axios instance + JWT interceptor
│       │   ├── auth.ts             # Supabase auth wrappers (signIn, signUp, etc.)
│       │   ├── tasks.ts            # getTasks, createTask, updateTask, deleteTask
│       │   ├── sessions.ts         # logSession, getSessions
│       │   ├── notes.ts            # getNotes, saveNote
│       │   └── ai.ts               # breakdownTask, planDay, kickstarter
│       ├── types/
│       │   ├── auth.ts             # User interface
│       │   ├── task.ts             # Task, Subtask, Priority, Tag interfaces
│       │   └── session.ts          # Session, MoodRating interfaces
│       └── utils/
│           ├── formatTime.ts       # seconds → MM:SS
│           └── dateHelpers.ts      # week ranges, heatmap data formatting

├── backend/
│   ├── main.py                     # FastAPI app, CORS, router registration
│   ├── requirements.txt
│   ├── .env                        # never committed
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/               # migration files (auto-generated)
│   └── app/
│       ├── api/
│       │   ├── auth.py             # /me endpoint only (Supabase handles actual auth)
│       │   ├── tasks.py            # CRUD for tasks + subtasks
│       │   ├── sessions.py         # log session, get sessions, stats
│       │   ├── notes.py            # CRUD for notes
│       │   └── ai.py               # AI feature endpoints
│       ├── models/
│       │   ├── user.py             # User (mirrors Supabase auth.users)
│       │   ├── task.py             # Task, Subtask
│       │   ├── session.py          # FocusSession
│       │   └── note.py             # Note
│       ├── schemas/
│       │   ├── task.py             # TaskCreate, TaskUpdate, TaskResponse
│       │   ├── session.py          # SessionCreate, SessionResponse
│       │   └── note.py             # NoteCreate, NoteResponse
│       ├── services/
│       │   └── session_service.py  # focus score calculation logic
│       ├── ai/
│       │   ├── breakdown.py        # PydanticAI — task breakdown agent
│       │   ├── kickstarter.py      # PydanticAI — session kickstarter agent
│       │   ├── planner.py          # LangGraph — plan my day pipeline
│       │   ├── review.py           # LangGraph — weekly review agent
│       │   ├── summary.py          # PydanticAI — end of day summary
│       │   ├── prioritizer.py      # PydanticAI — smart task prioritization
│       │   ├── burnout.py          # LangGraph — burnout detection
│       │   ├── notes_ai.py         # PydanticAI — note summarizer
│       │   └── prompts.py          # all prompt templates in one place
│       └── core/
│           ├── config.py           # Settings class via pydantic-settings
│           ├── database.py         # SQLAlchemy engine, SessionLocal, Base
│           └── deps.py             # get_current_user, get_db FastAPI dependencies

└── extension/
    ├── manifest.json               # Manifest V3
    ├── background.js               # service worker, reads session state, controls blocking
    ├── content.js                  # injected script (minimal — just overlay if needed)
    ├── popup.html                  # extension popup UI
    ├── popup.js                    # popup logic
    ├── blocked.html                # redirect page shown on blocked sites
    ├── rules.json                  # declarativeNetRequest rules (dynamic, updated by background.js)
    └── icons/                      # 16, 48, 128px icons
```

---

## 9. Database Schema

### users
```sql
id          UUID PRIMARY KEY  -- mirrors Supabase auth.users.id
email       VARCHAR NOT NULL UNIQUE
name        VARCHAR
avatar_url  VARCHAR
created_at  TIMESTAMP DEFAULT now()
```

### tasks
```sql
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id         UUID REFERENCES users(id) ON DELETE CASCADE
parent_id       UUID REFERENCES tasks(id) ON DELETE CASCADE  -- for subtasks, NULL = root task
title           VARCHAR NOT NULL
priority        VARCHAR CHECK (priority IN ('high', 'medium', 'low')) DEFAULT 'medium'
due_date        DATE
estimate_mins   INTEGER
is_complete     BOOLEAN DEFAULT false
is_archived     BOOLEAN DEFAULT false
is_recurring    BOOLEAN DEFAULT false
recur_type      VARCHAR CHECK (recur_type IN ('daily', 'weekly'))
tags            TEXT[]
created_at      TIMESTAMP DEFAULT now()
updated_at      TIMESTAMP DEFAULT now()
```

### focus_sessions
```sql
id                      UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id                 UUID REFERENCES users(id) ON DELETE CASCADE
task_id                 UUID REFERENCES tasks(id) ON DELETE SET NULL
duration_mins           INTEGER NOT NULL
planned_duration_mins   INTEGER NOT NULL
mood_before             SMALLINT CHECK (mood_before BETWEEN 1 AND 5)
mood_after              SMALLINT CHECK (mood_after BETWEEN 1 AND 5)
mood_note               VARCHAR(280)
focus_score             SMALLINT CHECK (focus_score BETWEEN 0 AND 100)
distraction_attempts    INTEGER DEFAULT 0
was_broken              BOOLEAN DEFAULT false
started_at              TIMESTAMP NOT NULL
ended_at                TIMESTAMP NOT NULL
```

### notes
```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id     UUID REFERENCES users(id) ON DELETE CASCADE
task_id     UUID REFERENCES tasks(id) ON DELETE SET NULL  -- optional link
session_id  UUID REFERENCES focus_sessions(id) ON DELETE SET NULL
content     TEXT
is_global   BOOLEAN DEFAULT false  -- true = global notepad, false = session note
created_at  TIMESTAMP DEFAULT now()
updated_at  TIMESTAMP DEFAULT now()
```

### work_blocks (for calendar deep work blocks)
```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id     UUID REFERENCES users(id) ON DELETE CASCADE
title       VARCHAR
start_time  TIMESTAMP NOT NULL
end_time    TIMESTAMP NOT NULL
color       VARCHAR DEFAULT '#6366f1'
created_at  TIMESTAMP DEFAULT now()
```

---

## 10. API Routes

All routes prefixed with `/api`. All routes except `/api/auth/me` require `Authorization: Bearer <token>` header.

### Auth
```
GET  /api/auth/me          → returns current user profile (creates user row on first login)
```

### Tasks
```
GET    /api/tasks              → list all tasks for user (supports ?tag=, ?priority=, ?complete=)
POST   /api/tasks              → create task
GET    /api/tasks/{id}         → get single task with subtasks
PUT    /api/tasks/{id}         → update task
DELETE /api/tasks/{id}         → delete task
POST   /api/tasks/{id}/complete → toggle complete
GET    /api/tasks/{id}/subtasks → list subtasks
POST   /api/tasks/{id}/subtasks → create subtask
```

### Sessions
```
POST /api/sessions             → log a completed focus session
GET  /api/sessions             → get all sessions (supports ?start=&end= date range)
GET  /api/sessions/stats       → aggregated stats (streaks, totals, heatmap data, avg score)
GET  /api/sessions/today       → today's sessions summary
```

### Notes
```
GET    /api/notes              → list all notes (?global=true for global notepad only)
POST   /api/notes              → create note
PUT    /api/notes/{id}         → update note
DELETE /api/notes/{id}         → delete note
```

### Work Blocks (Calendar)
```
GET    /api/blocks             → list blocks in date range (?start=&end=)
POST   /api/blocks             → create work block
PUT    /api/blocks/{id}        → update (drag/resize)
DELETE /api/blocks/{id}        → delete block
```

### AI
```
POST /api/ai/breakdown         → { task_title, task_description } → subtasks[]
POST /api/ai/kickstarter       → { streak, pending_tasks, time_of_day } → message string
POST /api/ai/plan-day          → { tasks[], available_hours, calendar_blocks[] } → schedule[]
POST /api/ai/end-of-day        → { sessions[], completed_tasks[], pending_tasks[] } → summary
POST /api/ai/prioritize        → { tasks[], available_hours, mood } → ordered tasks[]
POST /api/ai/weekly-review     → { week_sessions[], mood_data[], last_review? } → review
POST /api/ai/burnout-check     → { last_14_days_sessions[], mood_data[] } → { risk, message }
POST /api/ai/summarize-note    → { content } → { summary, action_items[] }
```

---

## 11. Authentication Flow

### Signup
```
1. User fills Register.tsx form
2. Frontend calls supabase.auth.signUp({ email, password })
3. Supabase creates user in auth.users, sends confirmation email
4. On email confirmation, onAuthStateChange fires with session
5. Frontend Zustand authStore.init() catches this, sets user
6. Frontend calls GET /api/auth/me (with Supabase JWT)
7. FastAPI verifies JWT, creates user row in public.users table if not exists
8. User is now logged in
```

### Login
```
1. User fills Login.tsx form
2. Frontend calls supabase.auth.signInWithPassword({ email, password })
3. Supabase returns session with access_token (JWT)
4. onAuthStateChange fires, Zustand sets user + token
5. All subsequent axios calls auto-attach token via interceptor
```

### Google OAuth
```
1. User clicks "Continue with Google"
2. Frontend calls supabase.auth.signInWithOAuth({ provider: 'google' })
3. Supabase redirects to Google, handles callback
4. Session returned to frontend via onAuthStateChange
5. Same flow as login from step 4 onwards
```

### JWT Verification on Every FastAPI Request
```python
async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(
        token,
        settings.SUPABASE_JWT_SECRET,
        algorithms=["HS256"],
        audience="authenticated"
    )
    return payload["sub"]  # UUID string
```

### Guest Mode
- Guest users get a temporary UUID stored in `localStorage`
- All data stored in `localStorage` (tasks, notes, timer state)
- Prompt to create account shown after 3 sessions
- Data migrated to account on signup

---

## 12. AI Layer

### Architecture Rule
All AI calls happen on the **FastAPI backend only**. The Anthropic API key is never exposed to the frontend. Frontend calls FastAPI endpoints, FastAPI calls Claude.

```
Frontend → POST /api/ai/breakdown → FastAPI → Claude API → structured response → Frontend
```

### Model
Always use: `claude-sonnet-4-20250514`

### Framework split
| Feature | Framework | Reason |
|---------|-----------|--------|
| Task breakdown | PydanticAI | Single shot, structured JSON output |
| Session kickstarter | PydanticAI | Single shot, string output |
| End-of-day summary | PydanticAI | Single shot, structured output |
| Smart prioritization | PydanticAI | Single shot, reordered list |
| Note summarizer | PydanticAI | Single shot, action items list |
| Plan my day | LangGraph | Multi-step pipeline with retry loop |
| Weekly review | LangGraph + checkpointing | Stateful, remembers previous weeks |
| Burnout detection | LangGraph | Multi-step analysis over 14 days of data |

### PydanticAI pattern (all simple agents)
```python
from pydantic import BaseModel
from pydantic_ai import Agent

class Subtask(BaseModel):
    title: str
    estimate_minutes: int
    order: int

class TaskBreakdownResult(BaseModel):
    subtasks: list[Subtask]
    total_estimate_minutes: int

agent = Agent(
    model='claude-sonnet-4-20250514',
    result_type=TaskBreakdownResult
)

async def breakdown_task(title: str, description: str = "") -> TaskBreakdownResult:
    result = await agent.run(
        f"Break down this task into concrete subtasks:\nTitle: {title}\nDescription: {description}"
    )
    return result.data
```

### LangGraph pattern (Plan My Day)
Multi-step pipeline:
```
analyze_tasks → fetch_calendar_gaps → generate_schedule → validate_plan → [retry if conflicts] → return
```

Each node is a function that takes and returns `PlannerState`. The graph has a conditional edge on `validate_plan` that loops back to `generate_schedule` if there are time conflicts, up to 3 retries.

### All prompt templates
All prompt strings live in `backend/app/ai/prompts.py`. No prompt strings anywhere else. This makes prompt tuning easy — one file to edit.

### Phase 1 AI features (vacation build)
- Task breakdown
- Session kickstarter

### Phase 2 AI features (post vacation)
- Plan my day (LangGraph)
- End-of-day summary
- Smart prioritization
- Note summarizer
- Weekly review (LangGraph + checkpointing)
- Burnout detection (LangGraph)

---

## 13. Chrome Extension

### How it communicates with FlowSpace
When a session starts, the React app writes to `localStorage`:
```js
localStorage.setItem('flowspace_session', JSON.stringify({
  active: true,
  endsAt: Date.now() + durationMs,
  blocklist: ['twitter.com', 'instagram.com', 'reddit.com', 'youtube.com']
}))
```

The extension background service worker polls this key every 10 seconds (or listens via `chrome.storage` if on same origin).

### Blocking mechanism
Uses `chrome.declarativeNetRequest.updateDynamicRules()`:
```js
// background.js
function activateBlocking(domains) {
  const rules = domains.map((domain, i) => ({
    id: i + 1,
    priority: 1,
    action: {
      type: 'redirect',
      redirect: { extensionPath: '/blocked.html' }
    },
    condition: {
      urlFilter: `*://*.${domain}/*`,
      resourceTypes: ['main_frame']
    }
  }))
  chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: rules.map(r => r.id),
    addRules: rules
  })
}
```

### blocked.html
Shows:
- FlowSpace logo
- "You're in a focus session"
- Countdown timer (reads `flowspace_session.endsAt` from localStorage)
- "Go back to work" button that opens FlowSpace tab

### Permissions required
```json
"permissions": ["declarativeNetRequest", "storage", "tabs", "alarms"]
```

---

## 14. PWA

### Vite PWA config
```ts
VitePWA({
  registerType: 'autoUpdate',
  manifest: {
    name: 'FlowSpace',
    short_name: 'FlowSpace',
    theme_color: '#6366f1',
    background_color: '#ffffff',
    display: 'standalone',
    icons: [
      { src: '/icons/192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icons/512.png', sizes: '512x512', type: 'image/png' }
    ]
  },
  workbox: {
    globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
    runtimeCaching: [{
      urlPattern: /^https:\/\/.*\.railway\.app\/api\/.*/i,
      handler: 'NetworkFirst',
      options: { cacheName: 'api-cache', networkTimeoutSeconds: 5 }
    }]
  }
})
```

### Offline behavior
- Timer works fully offline (Zustand state in memory)
- Tasks cached from last sync, readable offline
- Notes scratchpad readable offline
- API calls queue and retry when back online (future enhancement)

### Push notifications
- Break reminder: fires when timer transitions from work → break
- Daily plan reminder: 8am every day (uses Web Push via service worker)
- Implemented with `self.registration.showNotification()` in service worker

---

## 15. Monetization

### Free tier
- Focus timer (Pomodoro + custom)
- Task management (unlimited)
- Calendar (day/week/month)
- Notes (scratchpad + global)
- Ambient sounds (3 sounds: rain, white noise, lo-fi)
- Soft Focus Lock
- Basic stats (7 day history)
- Guest mode

### Pro tier ($5/month)
- All free features
- All 6 ambient sounds + mixing
- Hard Focus Lock (Chrome Extension)
- Full stats history (unlimited)
- Mood tracking
- AI Task Breakdown
- AI Session Kickstarter
- AI Plan My Day
- AI Weekly Review
- AI Burnout Detection
- Google Calendar sync
- iCal export

### Implementation (Phase 2)
- Stripe for payment processing
- `is_pro` boolean on user model
- FastAPI checks `is_pro` before allowing Pro-only routes
- Frontend shows upgrade prompt when Pro feature is accessed on free plan

---

## 16. Build Phases

### Phase 1 — Vacation (4 weeks)

**Week 1 — Project setup & foundation**
- Initialize frontend (Vite + React + TypeScript + Tailwind + PWA plugin)
- Initialize backend (FastAPI + SQLAlchemy + Alembic)
- Set up Supabase project (Auth + DB)
- Implement auth flow (Supabase JS client + FastAPI JWT verification)
- Create all DB tables + run first Alembic migration
- Deploy skeleton: frontend → Vercel, backend → Railway
- Set up UptimeRobot to ping `/health` every 5 minutes
- Commit: working login/signup/logout, live URLs

**Week 2 — Core features**
- Task management (full CRUD, priorities, due dates, subtasks, tags, recurring)
- Focus timer (Pomodoro + custom, auto-start, session linking, floating widget)
- Notes / scratchpad (per-session + global, markdown)
- Ambient sounds (6 soundscapes, mixing, Web Audio API)
- Session auto-logging to DB on completion

**Week 3 — Calendar + Focus Lock**
- Calendar (day/week/month views, tasks on dates, session blocks, drag-to-reschedule)
- Soft Focus Lock (Page Visibility API, broken session detection)
- Chrome Extension skeleton + Hard Lock (blocklist, declarativeNetRequest, blocked.html)
- Session logging with focus score calculation

**Week 4 — Stats + PWA + AI v1**
- Stats dashboard (heatmap, charts, streaks — all via Recharts)
- PWA finalization (offline caching, push notifications, installable)
- AI: Task Breakdown (PydanticAI)
- AI: Session Kickstarter (PydanticAI)
- Polish, bug fixes, mobile responsiveness

### Phase 2 — Post Vacation

**Week 5–6 — AI core**
- Plan My Day (LangGraph multi-step pipeline)
- Smart Prioritization (PydanticAI)
- End-of-Day Summary (PydanticAI)
- Note Summarizer (PydanticAI)

**Week 7–8 — AI advanced + monetization**
- Weekly Review (LangGraph + checkpointing)
- Burnout Detection (LangGraph)
- Mood tracking UI + correlation charts
- Stripe integration + Pro gating
- Google Calendar sync
- iCal export
- Landing page

---

## 17. Deployment

### Frontend (Vercel)
```bash
cd frontend && vercel
# Set env vars in Vercel dashboard:
# VITE_SUPABASE_URL
# VITE_SUPABASE_ANON_KEY
# VITE_API_URL
```

### Backend (Railway)
- Connect Railway to GitHub repo
- Set root directory to `/backend`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Set env vars in Railway dashboard (see Section 18)

### Database (Supabase)
- Create project at supabase.com
- Copy DB connection string from Settings → Database
- Copy JWT secret from Settings → API → JWT Settings
- Enable Google OAuth in Authentication → Providers

### Uptime (UptimeRobot)
- Free account at uptimerobot.com
- HTTP monitor → `https://your-app.railway.app/health`
- Interval: 5 minutes
- Prevents Supabase free tier from pausing (requires activity within 7 days)

---

## 18. Environment Variables

### Frontend (`frontend/.env`)
```
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
VITE_API_URL=https://your-app.railway.app
```

### Backend (`backend/.env`)
```
DATABASE_URL=postgresql://postgres:[password]@db.xxxx.supabase.co:5432/postgres
SUPABASE_JWT_SECRET=your-jwt-secret-from-supabase-dashboard
ANTHROPIC_API_KEY=sk-ant-...
```

### Never commit
- `backend/.env`
- `frontend/.env`
- Both are in `.gitignore`

---

## 19. Key Decisions & Rationale

| Decision | Choice | Reason |
|----------|--------|--------|
| Auth provider | Supabase Auth | Saves 2 days vs manual JWT, Google OAuth free, handles token refresh |
| Database host | Supabase PostgreSQL | Bundled with auth, free tier, real Postgres |
| DB pausing fix | UptimeRobot | Free, 2 min setup, pings every 5 min |
| Frontend → DB | Never direct | All data through FastAPI. Keeps business logic centralized |
| AI framework | PydanticAI + LangGraph | PydanticAI for simple structured outputs, LangGraph for multi-step agentic flows |
| AI model | claude-sonnet-4-20250514 | Best balance of speed + quality for this use case |
| Site blocking | Chrome Extension (MV3) | Only way to truly block sites on desktop browsers |
| Blocking API | declarativeNetRequest | MV3 standard, no page content access needed, more performant |
| State management | Zustand | Simpler than Redux, works great with TypeScript |
| Charts | Recharts | Best React charting library, composable, TypeScript support |
| PWA build tool | Vite PWA plugin | First-class Vite integration, Workbox under the hood |
| Backend framework | FastAPI | Async, fast, auto Swagger docs, Pydantic native |
| Migrations | Alembic | Standard SQLAlchemy migration tool |
| Backend host | Railway | Simple Python deployments, free starter tier |
| Frontend host | Vercel | Best for React/Vite, free tier, instant deployments |

---

## 20. What This Project Is NOT

To prevent scope creep and keep the vacation build focused:

- NOT a team collaboration tool (single user only in Phase 1)
- NOT a full project management suite (no Gantt charts, no dependencies between tasks)
- NOT a habit tracker (streaks exist but no full habit module)
- NOT a note-taking app like Notion (scratchpad only, no rich blocks editor)
- NOT a time billing tool (no client/invoice features)
- NOT a native mobile app (PWA covers mobile use case)

---

*Last updated: Project kickoff*  
*Next review: After Week 1 build complete*
