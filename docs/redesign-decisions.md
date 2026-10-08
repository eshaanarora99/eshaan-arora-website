# Redesign decisions

## Architecture

Keep static HTML, vanilla CSS/JavaScript, existing document paths, and the separate Connect 4 API. There is no runtime framework or new backend. A small Python authoring script renders shared templates and Markdown content to checked-in HTML. One pinned build-only dependency, Python-Markdown, provides tables and fenced code. Any static server can serve the generated files without installing it.

This adds a reproducible authoring step to the former hand-edited site. It avoids repeating navigation and case-study markup across pages and avoids migrating a functioning application to a new stack. No database, authentication, npm runtime packages, or deployment workflow was introduced.

## Information architecture

Home introduces current work, a compact snapshot, four featured case-study entries (Connect 4, financial AI draft, Disney, and Michelin), Connect 4, two selected writing entries, and contact. About expands the background, education, credentials, and a timeline without invented dates or job titles. Work curates seven substantial or shorter project pages. Writing groups two source-linked document overviews and an external essay into three categories. Lab distinguishes browser tools, a playable interface, and archived local programs.

The SS&C and Texas case studies are explicitly marked drafts. Their presence is a place for evidence and review, not a claim of verified performance. Professional positioning uses the owner's provided Uber background and credentials. No confidential Uber work, invented quantitative impact, employer-specific responsibilities, or job dates were added.

## Design

Warm paper, dark ink, muted blue, teal, and a darker gold chosen for readable text. System sans-serif typography and Georgia editorial headings avoid external font requests and licensing dependencies. Restrained borders, two-column cards, clear section numbering, generous spacing, and readable article widths establish the hierarchy. The portrait is an existing asset. Disney charts are original exhibits and the Michelin thumbnail is rendered from the existing presentation; new SVGs illustrate conceptual workflows or a game board and are not fabricated data visualizations.

Navigation remains visible at narrow widths rather than relying on a JavaScript menu. Light and dark tokens cover the whole shared design. CSS follows system preference; an early script applies a saved manual override. Theme control and year updates tolerate unavailable storage. No reveal animations or hidden-on-load content remain.

## Content authoring

Project and writing content live in `content/work/*.md` and `content/writing/*.md`. Front matter is a JSON object between `---` lines: deliberately simple and readable using the standard library. Shared templates render metadata, table-of-contents links, references, related articles, and optional article covers. Markdown supports tables, fenced code, links, images, and trusted HTML for formulas or embedded demos. Raw HTML is only for trusted owner-authored content, never visitor input.

Substack retains the full AI self-checkout essay, with direct index links rather than copied text. PDF writing stays intact with local original overviews and explicit historical dates. Reading time describes each overview, not the linked PDF. A future full Markdown article uses “min read.”

## Application preservation

The original Connect 4 JavaScript remains byte-identical, including board logic, move identifiers, fallback algorithms, match persistence, and first/second-player behavior. Game HTML retains every required ID, replaces overlapping sidebar navigation with an inline mode bar, and corrects the inappropriate grid role to an accessible group. The PG mode's original boosted-CNN wording is removed because its actual request uses `pg`; backend architecture is unverified.

Known behavioral issues are documented rather than silently changed. Existing Connect 4 CSS stays isolated. No backend changes or new model benchmark claims are made.

Financial tools are new and explicitly distinguish the original Python listings. The calculator supports single cash flows, ordinary annuities, and fixed-coupon bonds using per-period rates. It validates inputs, handles zero rates and zero periods, uses stable near-zero calculations, and rejects nonfinite outputs. Multiphase growth, live stock quotes, and a Spotify upload explorer are not implemented.

## Hosting and migration

Existing Vercel settings are untouched. All original HTML paths have pages or compatibility files. Compatibility pages supply canonical destinations, noindex, an accessible link, meta refresh, and a local script preserving fragments. An optional redirect file is supplied under `docs`, not installed as production configuration. Directory routes use trailing-slash canonicals; bare paths work through normal directory-index handling.

Original PDFs, workbook, résumé variants, images, and downloadable resources remain at their original paths. Immutable asset checks run before and after generation.
