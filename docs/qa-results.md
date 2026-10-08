# QA results — 8 October 2026

## Build and invariants

- `scripts/build.py` successfully generated 34 pages, robots.txt, and sitemap.xml.
- Rebuilding produced identical hashes for all 34 HTML outputs, robots.txt and sitemap.xml.
- Four offline unittest checks passed: all generated internal links and fragments, semantic/SEO structure, all original routes and resources, sitemap membership, and protected bytes.
- All 18 original HTML files remain available. Existing downloadable paths are retained.
- All 14 original PDF/Excel assets and the Connect 4 JavaScript match their baseline SHA-256 hashes. This includes every résumé variant, including the primary PDF. No document content was changed or regenerated.
- Python compilation and JavaScript syntax checks passed. `git diff --check` passed after normalizing whitespace in source listings and generated output.
- There was no pre-existing lint/type-check configuration. The implementation introduces no TypeScript or runtime framework requiring those checks.

## Financial calculations

Five Node test groups passed:

1. PV/FV inversion across negative, zero, near-zero, positive, and large rates; a known compound-value example.
2. Ordinary-annuity formula compared with independently discounted cash flows, including near-zero rates.
3. Bond pricing compared with coupon-by-coupon discounted cash flows plus principal; par bonds and zero yield.
4. Zero-period treatment and zero-amount extreme-rate case.
5. Invalid inputs, fractional/negative/excessive periods, rates at or below −100%, unsupported calculation types, and numeric overflow rejected.

Browser form submission also returned the expected $1,628.89 for $1,000 at 5% over 10 periods.

## Browser, responsive layout and accessibility

Chromium through Playwright checked all 28 indexable generated pages at desktop (1440×1000) and mobile (390×844), in both light and dark system themes: **112 page/theme/viewport combinations**. Final run: no horizontal page overflow, no JavaScript page errors, and **zero axe-core 4.10.3 violations** for the WCAG 2 A/AA, WCAG 2.1 AA, and best-practice tags tested.

Initial checks identified overflowing code blocks without keyboard focus and an unnecessary nested complementary landmark. These were corrected; final checks passed. Automated accessibility checks do not establish complete WCAG conformance.

Screenshots were captured for Home, About, Disney, Connect 4 Challenge, and Financial Tools in each viewport/theme combination. Home and mobile game screenshots were visually inspected. The final homepage uses a real Michelin presentation thumbnail rather than featuring the source-incomplete Texas draft.

Additional browser checks passed for the keyboard skip link and main focus, keyboard-focusable source code, a 320px homepage viewport, reduced-motion preference, system dark colors, saved manual theme persistence, JavaScript-disabled reading/navigation, no-JavaScript meta-refresh compatibility, and `/about` directory redirect handling.

## URL compatibility

Six browser migration scenarios passed, including `portfolio.html#amazonia` retaining its anchor, blog, Disney, Spotify, the explicit capstone `index.html`, and the Square hub. All compatibility pages have visible destination links, canonical destinations, noindex metadata, and meta refresh. They are HTML compatibility redirects; an actual HTTP redirect configuration is supplied as an optional example, not deployed.

## Connect 4

Reproducible browser tests use mocked inference, not a replaced game script. All three `transformer`, `cnn`, and `pg` routes passed:

- 42-cell board creation and correct API mode identifiers.
- User-first and AI-first player encoding.
- Vertical user win and persistent match-record count across reload.
- Resignation and reset.

Separate scenarios verified a legal fallback move on API failure and on an invalid column response. The tests passed without changing the original game script. Horizontal/diagonal/draw behavior remains implemented by the unchanged source but was not exhaustively exercised by these browser scenarios.

Live `/connect4-api/health` returned HTTP 200 with `{"status":"ok"}`. Direct move probes for all three modes received HTTP 403; a follow-up probe with the original site Origin returned edge error 1010. This prevents verification of real model inference from this environment. It does not establish that the service is unavailable to ordinary visitors. Actual inference and CORS must be checked on the reviewed preview host. No model strength, win-rate, or latency benchmark is claimed.

Known existing request/reset races, lack of timeout, late health messages, fractional-response handling, localStorage error handling, and incomplete board occupancy announcements remain follow-ups. The random fallback may conceal failed inference.

## External references and performance limits

The live website was fetched for reference before editing and differed from repository HTML. The self-checkout Substack request was denied by the network proxy (CONNECT 403), so current article availability and its publication date were not verified. Other external social/video links were preserved from the source; their presence does not certify ongoing availability.

No Lighthouse audit or scores were produced. No Vercel deployment, remote redirect configuration test, external Spotify execution, Python legacy formula certification, or PDF content update was performed. Generated pages have shared metadata, canonical URLs, sitemap, robots.txt, structured identity data, explicit image sizes and lazy nonessential visuals, but those features are not a substitute for a measured production performance audit.

## Reproduce

See `deployment.md` and `README.md`. `scripts/browser_qa.py` writes `.qa/browser-report.json` and screenshots. A copy of the final automated report is retained as `qa-browser-report.json`. Any owner-approved hosting preview still needs the release checks in the deployment document.
