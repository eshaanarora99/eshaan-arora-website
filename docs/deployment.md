# Development and deployment

## Current state

No production deployment, main-branch push, production configuration overwrite, or hosting migration was performed. Generated HTML is available for review on a local redesign branch. The branch has not been pushed, so no automatic hosting preview is triggered by this task. Existing README identifies Vercel hosting, but actual dashboard settings and auto-deployment behavior need owner confirmation.

## Local authoring

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-build.txt
.venv/bin/python scripts/build.py
python3 -m http.server 8080
```

The site serves directly from the repository root. The compiler updates tracked HTML, robots.txt, sitemap.xml, and a page manifest in place. It checks SHA-256 hashes of the original game script and all PDF/Excel assets before and after generation. It never writes those files. An intentional future owner-managed PDF update requires updating the corresponding baseline hash manually after inspecting the exact document change.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node tests/financial-tools.test.js
python3 -m py_compile scripts/build.py scripts/browser_qa.py
```

Browser QA additionally requires Playwright, Chromium at `/usr/bin/chromium`, a running local server, and axe-core 4.10.3. For example, download axe-core's script from its official package/CDN, then run:

```sh
python3 scripts/browser_qa.py --axe /path/to/axe.min.js
```

Screenshots and JSON reports are saved to ignored `.qa/`. Browser inference tests mock API responses and are not model benchmarks. See `qa-results.md` for the performed checks and limits.

## Preview and release

1. Review the redesign branch and the factual flags in `content-review-needed.md`. Confirm the intended contact address and safe capstone naming/material.
2. Preview using the existing Vercel project only after checking its build/root settings and whether a feature branch automatically creates a preview. No production settings need changing for checked-in static output. The site's server root must be the repository root, with no Python build command required.
3. Verify slash and bare directory routes, asset paths, Connect 4 cross-origin requests, PDF downloads, and compatibility pages on that preview host. Local static-server checks cannot certify Vercel dashboard configuration or remote CORS behavior.
4. If proper HTTP 308 redirects are desired, review `vercel-redirects.example.json`, merge its rules with existing dashboard/configuration rules, and only then install them as `vercel.json`. Do not blindly replace production configuration. Current HTML compatibility redirects already work without it, but are not HTTP redirects.
5. After explicit owner approval, use the repository's normal reviewed merge/release process. Do not push this redesign directly to main.

Canonical and Open Graph URLs use `https://eshaanarora.com`. A shared social PNG and SVG source are included. robots.txt and sitemap.xml are generated. Preview deployments should be protected or noindexed using host-level settings where available; this task does not alter production SEO controls for previews.

## Independent game service

The Connect 4 API is not deployed with this repository. Its existing origin is `https://api-connect4.eshaanarora.com`, with `/connect4-api/health` and `/connect4-api/move`. No service URL, model routing, CORS policy, or backend settings were changed. Test live inference on the approved preview domain before releasing; the existing random fallback can conceal unavailable inference.

## Rollback

The generated redesign can be reverted using Git without touching PDFs. Existing downloads and game routes are preserved. Before reverting a release, account for any subsequent owner-managed résumé updates so they are not overwritten by a broad rollback.
