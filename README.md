# Eshaan Arora — Operations, Analytics, and AI

A static personal website balancing professional background, technical work, writing, and independent experiments. Live reference: https://eshaanarora.com. Existing hosting: Vercel; the redesign has not been deployed to production.

## Site structure

- `/` — introduction, snapshot, selected work, Connect 4, writing, contact.
- `/about/` — biography, background, education, credentials, timeline.
- `/work/` — seven Markdown-driven case studies.
- `/writing/` — categorized document overviews and canonical external essays.
- `/lab/` — Connect 4, browser financial tools, source programs, archive.
- `/connect4/` — preserved game modes and inference integration.
- `/resume.html` — existing PDF viewer; direct PDF link remains available.

Old HTML URLs remain available or forward to the appropriate migrated page.

## Run locally

The generated site needs no runtime dependencies:

```sh
python3 -m http.server 8080
```

Open http://localhost:8080. Do not edit generated HTML directly; update content/templates and rebuild.

## Edit and build

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-build.txt
.venv/bin/python scripts/build.py
```

Generated HTML is checked in, so production can keep serving the repository root without installing Python or running a build. Markdown compilation is an authoring step, not a new hosting requirement.

- `content/site.json` — identity, canonical origin, contact and résumé links.
- `content/work/*.md` — case studies with JSON front matter between `---` lines.
- `content/writing/*.md` — writing metadata, body, references, related slugs.
- `content/sources/*.py` — preserved original Python programs, not browser executables.
- `content/legacy/` — source markup for preserved game controls and historical table.
- `scripts/build.py` — shared layout, navigation, footer, indexes, case-study template, compatibility pages and SEO output.
- `css/styles.css` — shared light/dark tokens and responsive editorial design.
- `js/financial-tools.js` — pure formulas and calculator interface.
- `connect4/assets/connect4.js` — original game script, byte-identical.

To add a project, copy a case-study Markdown file and give it a unique slug, category, description, tools and status. The Work index discovers it automatically. `featured: true` includes it on Home; curate three or four entries. Follow the existing sections for overview, question, contribution, methodology, implementation, findings, limitations, resources. Images, code, tables, and trusted HTML formulas/embeds are supported.

To add writing, copy an article and update title, slug, category, description, and body. `date` is optional and must be supported by a source or the actual publication date. Supported categories are Economics & Finance, Technology & AI, Notes & Essays. Optional fields: `references` (title/url objects), `related` (article slugs), `external` (canonical external essay), `overview` (labels short source overviews), and `cover` (src/alt/width/height object). Reading time is calculated from the local Markdown. A full external essay is linked directly rather than duplicated. See the existing files for examples.

## Verify

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node tests/financial-tools.test.js
```

Browser checks: `scripts/browser_qa.py` uses Playwright, Chromium, and axe-core; see deployment instructions for setup. No Lighthouse score or model performance is implied by these checks.

**Never edit, replace, rename, regenerate, or delete résumé PDFs through the build.** All original PDF/Excel files and the game script are hash-protected in `docs/preserved-assets.json`. The owner updates résumé content manually.

## Review and release

Read [site audit](docs/site-audit.md), [design decisions](docs/redesign-decisions.md), [URL migration](docs/url-migration.md), [content review](docs/content-review-needed.md), [QA results](docs/qa-results.md), and [deployment instructions](docs/deployment.md).

Draft case studies identify missing evidence. Live game inference remains an independent service. No database, authentication, production config changes, or runtime framework were added. Do not merge or deploy until the owner approves the design and professional copy.
