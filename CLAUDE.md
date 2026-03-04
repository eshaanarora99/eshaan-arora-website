# CLAUDE.md — Eshaan Arora Personal Website

## Project overview

Static personal portfolio website for Eshaan Arora, a data and analytics professional. No build tools, no frameworks, no package manager. Every page is plain HTML with a shared CSS file and a shared JavaScript file. The site is deployed on Vercel at [eshaanarora.com](https://www.eshaanarora.com/).

---

## Repository structure

```
/
├── index.html                   # Home / landing page
├── resume.html                  # Resume embed page
├── contact.html                 # Contact page
├── portfolio.html               # Extended portfolio page
├── blog.html                    # Blog page (links to Substack)
├── disney-analysis.html         # Disney DCF project page
├── spotify-data-analysis.html   # Spotify analysis project page
├── bond-calculator-code.html    # Bond price calculator
├── present-future-value-calculator.html  # PV/FV calculator
├── stock_quotes.html            # Yahoo Finance data fetcher
├── market_dashboard.html        # Market dashboard
│
├── css/
│   ├── styles.css               # Global stylesheet (single source of truth for design)
│   └── styles_old.css           # Archived old styles — do not use
│
├── js/
│   └── main.js                  # Global JS: theme toggle, reveal animations, Connect4 sidebar
│
├── connect4/                    # Connect 4 game sub-section
│   ├── index.html               # Connect 4 landing page
│   ├── training-methodology/index.html  # How the AI works explainer
│   ├── play-cnn/index.html      # Challenge Mode (CNN opponent)
│   ├── play-transformer/index.html      # Casual Mode (Transformer opponent)
│   ├── play-policy-gradient/index.html  # Insane Mode (Policy Gradient opponent)
│   ├── assets/
│   │   ├── connect4.css         # Connect 4-specific styles (extends global CSS)
│   │   └── connect4.js          # Game logic + backend API calls
│   └── images/
│       └── connect-4-logo.png
│
├── msba-capstone/
│   └── index.html               # Financial Risk Insight Engine capstone page
│
├── square-apm-portfolio/
│   └── index.html               # Square APM application hub
│
├── images/                      # Site images (headshot, project screenshots, etc.)
├── documents/                   # PDFs, Excel files, resume downloads
└── Archive/                     # Unused/archived content — ignore
```

---

## Technology stack

- **HTML5** — semantic markup, ARIA attributes throughout
- **CSS3** — custom properties (design tokens), `color-mix()`, `clamp()`, CSS Grid
- **Vanilla JavaScript (ES2020+)** — no libraries or frameworks
- **No build step** — files are served directly; changes take effect immediately
- **Hosting** — Vercel (automatic deploys from `main` branch)

---

## CSS design system (`css/styles.css`)

All visual design is driven by CSS custom properties defined on `:root`. Never hard-code colors, spacing, or radii — always use these tokens.

### Color tokens

| Token | Light value | Dark value |
|---|---|---|
| `--bg` | `#f6f7fb` | `#0b1120` |
| `--surface` | `#ffffff` | `#111827` |
| `--text` | `#0f172a` | `#e2e8f0` |
| `--muted` | `#475569` | `#94a3b8` |
| `--border` | `#e2e8f0` | `#1f2937` |
| `--accent` | `#2563eb` | `#60a5fa` |
| `--accent-2` | `#0f766e` | `#2dd4bf` |

### Spacing scale

`--space-1` (4px) through `--space-10` (72px). Use these rather than raw pixel values.

### Border radii

- `--radius-lg`: 24px — hero cards, large containers
- `--radius-md`: 16px — standard `.card` elements
- `--radius-sm`: 12px — smaller UI components

### Core utility classes

| Class | Purpose |
|---|---|
| `.container` | Centered max-width wrapper (`min(1120px, 92vw)`) |
| `.section` | Standard vertical padding for page sections |
| `.card` | Rounded surface card with border, shadow, and hover lift |
| `.grid-2` | Responsive 2-column grid (collapses on small screens) |
| `.button` | Base button styles |
| `.button-primary` | Filled accent button |
| `.button-secondary` | Outlined button |
| `.tag` | Pill-shaped label for project tech tags |
| `.chip` | Pill-shaped skill chip |
| `.reveal` | Element that animates in via `IntersectionObserver` |
| `.section-title` | Standard heading with fluid font size |
| `.section-subtitle` | Muted descriptive text under headings |
| `.project-grid` | Responsive grid for project cards |
| `.project-links` | Flex row of project action links |
| `.contact-grid` | Responsive grid for contact info cards |
| `.media-frame` | 16:9 responsive iframe wrapper |

---

## JavaScript conventions (`js/main.js`)

`main.js` is loaded with `defer` on every page and handles three concerns:

### 1. Dark/light theme toggle
- Theme is stored in `localStorage` under the key `"theme"` (`"light"` or `"dark"`).
- Applied via `data-theme` attribute on `<html>` element.
- Respects `prefers-color-scheme` as initial default when no stored preference exists.
- The toggle button must have `data-theme-toggle` attribute; the label span must have `data-theme-label`.

### 2. Scroll reveal animations
- Elements with `data-reveal` are observed by an `IntersectionObserver` (threshold: 0.2).
- When visible, `is-visible` class is added which triggers the CSS transition defined on `.reveal`.
- Disabled entirely when `prefers-reduced-motion` is set.

### 3. Connect 4 sidebar toggle
- The fixed sidebar nav in all Connect 4 pages is toggled by an element with `data-connect4-nav-toggle`.
- The sidebar itself must have `data-connect4-sidebar`.
- Toggling adds/removes `is-collapsed` class on the sidebar.

---

## Connect 4 game (`connect4/`)

### Architecture

The frontend is pure HTML/CSS/JS. Game AI runs on a cloud backend (Django API):

```
API base: https://api-connect4.eshaanarora.com/connect4-api
Endpoints:
  POST /move    — body: { modelType, board }  → response: { best_move }
  GET  /health  — connectivity check
```

### Model types (`data-opponent` attribute on `<body>`)

| `data-opponent` value | Mode | Page |
|---|---|---|
| `transformer` | Casual Mode | `play-transformer/index.html` |
| `cnn` | Challenge Mode | `play-cnn/index.html` |
| `pg` | Insane Mode | `play-policy-gradient/index.html` |

The `connect4.js` script reads `document.body.dataset.opponent` to determine which model to request.

### Board encoding
- UI board uses `null / "user" / "ai"` per cell.
- API board uses `0 / 1 / 2` (0=empty, 1=player1, 2=player2; depends on who goes first).

### Stats persistence
- Per-opponent stats: `localStorage` key `connect4:stats:{modelType}`
- Combined totals: `localStorage` key `connect4:stats:total`
- Schema: `{ user: number, ai: number, draws: number }`

### Connect 4 required HTML IDs
The `connect4.js` script expects these element IDs on game pages:
- `connect4-board` — the board grid element
- `connect4-status` — status message (has `aria-live="polite"`)
- `connect4-start`, `connect4-reset`, `connect4-resign` — action buttons
- `connect4-user-color`, `connect4-ai-color` — color display spans
- `connect4-user-wins`, `connect4-ai-wins`, `connect4-draws` — per-opponent stats
- `connect4-total-user-wins`, `connect4-total-ai-wins`, `connect4-total-draws` — combined stats

### API failure fallback
If the backend is unreachable, the game falls back to a random legal move so gameplay is never fully blocked.

---

## HTML page conventions

### `<head>` boilerplate (root-level pages)
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Title | Eshaan Arora</title>
<meta name="description" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="images/headshot.jpeg">
<meta property="og:type" content="website">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="css/styles.css">
<script src="js/main.js" defer></script>
```

### Asset path rules

| Location | CSS/JS paths | Image paths |
|---|---|---|
| Root (`/`) | `css/styles.css`, `js/main.js` | `images/...` |
| One level deep (`/connect4/`) | `/css/styles.css`, `/js/main.js` | `/images/...` |
| Two levels deep (`/connect4/play-cnn/`) | `/css/styles.css`, `/js/main.js` | `/images/...` |
| Adjacent sub-folder (`/msba-capstone/`) | `../css/styles.css`, `../js/main.js` | `../images/...` |

Sub-pages under `connect4/` also load the Connect 4 stylesheet and, for game pages, the game script:
```html
<link rel="stylesheet" href="/connect4/assets/connect4.css">
<script src="/connect4/assets/connect4.js" defer></script>  <!-- game pages only -->
```

### Standard page header
Every page includes a sticky `<header class="site-header">` with the shared navigation and theme toggle. The Connect 4 sub-section pages additionally include the `<nav class="connect4-nav">` sidebar **before** the header.

### Skip link
Every page starts with `<a class="skip-link" href="#main">Skip to content</a>` for keyboard accessibility.

### Footer
```html
<footer class="footer">
  <div class="container">
    <p>&copy; 2026 Eshaan Arora · ...</p>
  </div>
</footer>
```

---

## Accessibility standards

- All interactive elements have `aria-label` or visible labels.
- The theme toggle uses `aria-pressed` to reflect state.
- Game status messages use `aria-live="polite"`.
- Connect 4 board cells have `aria-label="Column N"`.
- Focus styles use `outline: 3px solid var(--accent)`.
- `prefers-reduced-motion` disables animations site-wide.
- Skip-to-content link is present on all pages.

---

## Responsive design

Single breakpoint at `max-width: 720px`:
- Nav bar stacks vertically.
- Multi-column grids collapse to single column.
- The Connect 4 sidebar repositions to the bottom of the viewport.
- Fluid type sizes use `clamp()` throughout.

---

## Development workflow

This is a no-build static site. There is no `npm install`, no compile step, and no test suite.

### Local development
Serve files with any static server. For example:
```bash
python3 -m http.server 8080
# or
npx serve .
```

### Making changes
1. Edit HTML/CSS/JS files directly.
2. Refresh browser to see changes.
3. All styling goes in `css/styles.css`; page-specific overrides use inline `style` attributes only when adding a new reusable class would be overkill.
4. Never edit `css/styles_old.css`.

### Adding a new page
1. Copy the structure of the closest existing page.
2. Update `<title>`, `<meta name="description">`, OG tags.
3. Adjust asset paths based on the page's directory depth (see path rules above).
4. Add a link to the new page from `index.html` or the relevant section.

### Adding a new Connect 4 game mode
1. Create a new directory under `connect4/` (e.g., `connect4/play-new-mode/`).
2. Copy `connect4/play-cnn/index.html` as a starting template.
3. Set `data-opponent="new-model-type"` on `<body>`.
4. Ensure the backend supports the new `modelType` value.
5. Add a link to the new page in the sidebar nav (`connect4-nav-links`) of all Connect 4 pages and in `connect4/index.html`.

### Git workflow
- Primary development branch for AI-assisted changes: `claude/add-claude-documentation-Rmuvi`
- Production branch: `main` (auto-deploys to Vercel)
- Commit messages are imperative and descriptive (e.g., `Update Connect4 sidebar collapse behavior`).

---

## Key external dependencies

| Service | URL | Purpose |
|---|---|---|
| Connect 4 API | `https://api-connect4.eshaanarora.com/connect4-api` | AI move inference |
| Vercel | — | Hosting and deployment |
| Substack | `https://earora.substack.com` | Blog content |

---

## Things to avoid

- Do not introduce JavaScript frameworks, npm packages, or build tools.
- Do not hard-code colors or spacing — always use CSS custom properties.
- Do not create new CSS files for individual pages; add classes to `css/styles.css` or use minimal inline styles.
- Do not break the `data-reveal` / `is-visible` animation pattern when adding new sections.
- Do not remove the `aria-live="polite"` attribute from the game status element.
- Do not push to `main` without review; use feature branches.
