# URL migration map

All 18 original HTML files remain reachable. Existing PDF/Excel files and images retain their original paths. Directory indexes preserve explicit `index.html` forms as well as directory URLs.

| Original path | Canonical destination | Treatment |
| --- | --- | --- |
| `/blog.html` | `/writing/` | Compatibility page: noindex, canonical destination, visible link, meta refresh, fragment-preserving JS |
| `/bond-calculator-code.html` | `/bond-calculator-code.html` | Same route, archived source clearly labeled |
| `/connect4/index.html` | `/connect4/` | Same route, shared redesign; original application contract preserved |
| `/connect4/play-cnn/index.html` | `/connect4/play-cnn/` | Same route, shared redesign; original application contract preserved |
| `/connect4/play-policy-gradient/index.html` | `/connect4/play-policy-gradient/` | Same route, shared redesign; original application contract preserved |
| `/connect4/play-transformer/index.html` | `/connect4/play-transformer/` | Same route, shared redesign; original application contract preserved |
| `/connect4/training-methodology/index.html` | `/connect4/training-methodology/` | Same route, shared redesign; original application contract preserved |
| `/contact.html` | `/contact.html` | Same route, updated shared design |
| `/disney-analysis.html` | `/work/disney-valuation/` | Compatibility page: noindex, canonical destination, visible link, meta refresh, fragment-preserving JS |
| `/index.html` | `/` | Same route, updated shared design |
| `/market_dashboard.html` | `/market_dashboard.html` | Same route, historical snapshot clearly labeled |
| `/msba-capstone/index.html` | `/work/financial-ai-assistant/` | Compatibility page: noindex, canonical destination, visible link, meta refresh, fragment-preserving JS |
| `/portfolio.html` | `/work/` | Compatibility page: noindex, canonical destination, visible link, meta refresh, fragment-preserving JS |
| `/present-future-value-calculator.html` | `/present-future-value-calculator.html` | Same route, archived source clearly labeled |
| `/resume.html` | `/resume.html` | Same route, updated shared design |
| `/spotify-data-analysis.html` | `/work/spotify-analysis/` | Compatibility page: noindex, canonical destination, visible link, meta refresh, fragment-preserving JS |
| `/square-apm-portfolio/index.html` | `/work/` | Compatibility page: noindex, canonical destination, visible link, meta refresh, fragment-preserving JS |
| `/stock_quotes.html` | `/stock_quotes.html` | Same route, archived source clearly labeled |

## New canonical routes

- `/`, `/about/`, `/work/`, `/writing/`, `/lab/`. Bare directory paths use normal server directory redirects/index handling.
- Work: `/work/connect-4-ai/`, `/work/financial-ai-assistant/`, `/work/disney-valuation/`, `/work/texas-unemployment/`, `/work/spotify-analysis/`, `/work/scansense-ai/`, `/work/michelin-analysis/`.
- Writing: `/writing/japans-lost-decade/`, `/writing/finance-study-notes/`. AI self-checkout index entry links directly to its full essay on Substack.
- Lab: `/lab/financial-tools/`, `/lab/spotify-source/`, `/lab/archive/`.
- All existing Connect 4 directory routes are unchanged.

## Anchors

The homepage retains `#about`, `#experience`, `#projects`, `#skills`, and `#contact`. The corresponding snapshot anchors are concise pointers rather than duplicated full sections. `portfolio.html#amazonia` forwards to `/work/#amazonia`, which retains the seminar link. Compatibility scripts preserve fragments; without JavaScript, meta refresh and visible links reach the destination but may not preserve the fragment.

## HTTP versus HTML redirects

The installed compatibility files work under a basic static server and are excluded from the sitemap. They do not issue HTTP 301/308 responses. `vercel-redirects.example.json` supplies optional proper redirects after hosting review and owner approval; it is deliberately not installed as production `vercel.json`. Existing hosting configuration is untouched.

Explicit directory `index.html` pages share the directory canonical URL. Original source-listing URLs are canonical archive pages and do not pretend to run Python in the browser. All document downloads keep exact filenames and bytes; the primary résumé remains `/documents/eshaan-arora-resume.pdf`.

## Inventory

`original-route-inventory.json` records every original HTML page, link and anchor. `original-asset-inventory.json` records every original file. `generated-pages.json` records all redesigned outputs. External URLs are not redirected locally; their original destination is retained or normalized to its canonical form.
