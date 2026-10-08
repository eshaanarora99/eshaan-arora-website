# Site audit — 8 October 2026

Audited before redesign implementation. Source: `eshaanarora99/eshaan-arora-website`, main at `f99dc2306f6bf778c33a0713eb8a25e0cb6bf080`. Full page/link/anchor inventory: [original-route-inventory.json](original-route-inventory.json); complete original file inventory: [original-asset-inventory.json](original-asset-inventory.json).

## Architecture and deployment

18 static HTML documents, vanilla JavaScript, shared `css/styles.css`, archived stylesheet, and substantial inline styling on older pages. No package manifest, build, automated tests, server, routing configuration, database, or committed deployment workflow. README and CLAUDE.md describe Vercel with main automatically deploying. Directory indexes already serve Connect 4 and capstone pages. Existing deployment settings are outside the repository and must be checked before release.

Live homepage fetched independently on 8 October 2026: same broad design and positioning, but differs from repository HTML; it is reference only. Repository is the implementation source of truth.

## Pages and resources

- Main: `/index.html`, `/resume.html`, `/contact.html`, `/portfolio.html`, `/blog.html`.
- Projects and source listings: `/disney-analysis.html`, `/spotify-data-analysis.html`, `/bond-calculator-code.html`, `/present-future-value-calculator.html`, `/stock_quotes.html`.
- Historical market table: `/market_dashboard.html` (18 February 2025 snapshot, not live quotes).
- Application hubs: `/msba-capstone/`, `/square-apm-portfolio/`.
- Game: `/connect4/`, `/connect4/training-methodology/`, `/connect4/play-transformer/`, `/connect4/play-cnn/`, `/connect4/play-policy-gradient/`, with their explicit `index.html` URLs.
- Additional index content: ScanSense AI/Substack, Michelin restaurant text analysis/PDF, Amazonia Week/YouTube. No Texas unemployment code, dataset, report, or application in this checkout.
- Writing: Japan's Lost Decade PDF (dated 16 April 2021 on title page), AI self-checkout article hosted on Substack (no verified date in repository).
- Documents: 14 PDF/Excel files; include Disney memorandum and workbook, capstone artifacts, Michelin slides, study guides, and five résumé variants. Images include portrait, city photography, four Disney charts and Connect 4 logo.
- External links: GitHub profile and Spotify repository, LinkedIn, Substack publication and article, YouTube seminar, Prism CDN, Substack embed script, and Connect 4 API. Exact URLs retained in inventory. A URL's presence is not proof of availability.

## Résumé protection

Primary PDF: `documents/eshaan-arora-resume.pdf`; referenced by `resume.html`. All résumé variants, PDFs, and workbook have baseline SHA-256 hashes in `preserved-assets.json`. They must retain bytes, filenames, and paths. Any outdated résumé content is owner-managed; no PDF editing or generation is permitted.

## Content and technical debt

Homepage repeats About, education, skills, and full project list. Professional introduction omits current Uber role; undergraduate framing dominates. Footer years vary. Navigation differs between sections; Square hub fragment links target missing anchors. Disney refers to nonexistent `styles.css`. Some documents are unlinked. Older source-listing pages have no shared navigation or metadata and describe local Python programs as calculators. PV/FV multiphase implementation confuses growth and discount rates; do not port those formulas without validation. Spotify code needs personal export and local GeoIP database and is not a browser explorer. Market table is stale static data.

Existing unsupported claims include capstone 92% accuracy without scoring definition, model training/evaluation assertions without source, including the PG page calling its route a boosted CNN, and promotional difficulty claims. Capstone artifacts need owner confidentiality review before prominence. Disney memo verifies historical date (22 August 2025), $50.55 model value and $118.86 comparison; those must remain explicitly historical. Michelin slides verify group authorship and 78,838 review corpus; individual ownership and predictive quality cannot be inferred. No evidence for +2.62 percentage points exists here.

## Connect 4 findings

`connect4/assets/connect4.js` implements 6×7 gravity, four-direction win checks, draws, first/second player selection, reset, resignation, local match records and numeric 0/1/2 board encoding. Inference requests go to `https://api-connect4.eshaanarora.com/connect4-api/move` as `{modelType, board}`; `GET /health` is advisory. Transformer/Casual maps to `transformer`, CNN/Challenge to `cnn`, Policy gradient/Insane to `pg`.

No backend implementation, weights, training logs, dataset, architecture detail or benchmark exists in this repo. Methodology page says two approaches although three routes exist, and asserts shared training and match evaluation without evidence. On API errors, frontend chooses random legal moves; invalid numeric response falls back to first legal column. This is not model inference and must be disclosed. Existing risks include no timeout, reset/request race, late health messages overwriting state, and fractional moves not rejected. Preserve algorithms and behavior during redesign; record potential fixes separately.

## Accessibility and performance

Good starting points: skip links, game live status, buttons, theme tokens. Issues: portrait lacks dimensions, inconsistent focus/heading structure on older pages, embed without an accessible title, hidden sidebar still contains focusable links, visual cell labels omit occupancy, board declares grid without row/gridcell structure, and game sidebar overlays content on narrow screens. `localStorage` access may throw and reveal behavior depends on JavaScript. Many photographs are unoptimized. No Lighthouse scores or model benchmarks have been measured.

## Implementation direction

Retain static hosting and vanilla game, introduce shared generation templates and content files with checked-in HTML, consolidate five primary sections, and add optional offline compilation rather than a runtime framework. Preserve existing downloads and original source listings, create precise compatibility pages and an optional Vercel redirect configuration. Separate verified findings from visibly incomplete case studies. Never publish or push to production as part of this task.
