# Visitor-facing copy polish — 8 October 2026

## Recovered sources

The pre-redesign pages are intact in Git history at `f99dc2306f6bf778c33a0713eb8a25e0cb6bf080`. The revisions draw on the original Connect 4 introduction and gameplay pages, portfolio, capstone overview, and Product Manager's Note (`documents/product-manager-note.pdf`, read only). Disney's memorandum, Michelin presentation, and preserved Python programs provide project-specific substance.

Texas unemployment appears only in the redesign draft. A history search for unemployment and the reported estimate found no earlier HTML or Markdown write-up. Its route stays available as a brief coming-soon page but is excluded from the curated Work index and sitemap until substantive source material is available.

## Editorial changes

- Lead each project with its purpose and reader value, then explain the work in a first-person voice where supported by the original source.
- Replace “model route,” “playable interface,” “not benchmarked,” and repository-audit language in project cards and game entry points with direct descriptions and play links.
- Restore the capstone's actual high-level product/retrieval work and team credit from the owner's note. No new employer impact, client usage, performance figure, or confidential risk information is added.
- Describe Michelin's observed review phrases from the original slides, retaining the distinction between exploratory comparisons and award prediction.
- Keep substantive technical details in case studies: tools, process, architecture, financial assumptions and trade-offs. Remove placeholders, test plans and audit provenance from public prose.
- Keep visitor-relevant qualifications: Disney's historical valuation date, local setup for Python programs, and Connect 4's random-move fallback when inference is unavailable.
- Omit unverified dates instead of publishing “Date unverified.” Do not restore the unsupported capstone/ScanSense accuracy figures or infer Texas findings.
- Keep a short technical explanation of model families; do not restore inconsistent claims about two models, specific training datasets, or optimal play from the old Connect 4 copy.
- No résumé PDF, game algorithm, API integration, calculator formula, or download path changes.

## Examples

Before: “A playable experiment in model-backed decision making, with three opponent routes and a lightweight browser interface.”

After: “The classic game, with three AI opponents to play against and compare.”

Before: “Play the existing CNN API opponent. Mode names are inherited labels; comparative strength is not benchmarked here.”

After: “Put your strategy to the test against the CNN opponent.”

Before: “The existing narrative describes product and retrieval architecture work, but an individual contribution breakdown remains to be confirmed.”

After: “I worked on the product and retrieval design, including the move from in-memory storage to Chroma DB and iterations on the answer workflow.”

## Review notes retained internally

`content-review-needed.md` continues to record evidence gaps and factual follow-ups. Removing audit notes from public prose does not certify withheld performance figures or unresolved backend training details. The capstone's high-level account is sourced to the recovered owner-authored note; artifact confidentiality review still applies before adding prominent download links.

## Validation

The static build generated 34 pages. All four repository test groups and five financial formula test groups passed. Chromium checks covered 108 page/viewport/theme combinations, six legacy URL migrations, and five game scenarios, with zero axe accessibility violations. Additional mobile screenshots checked the Connect 4 selection page, game, and capstone case study. Preserved asset hashes match the original baseline, including all four résumé PDFs and the unchanged game JavaScript. These checks validate the interface and fallback behavior; they do not benchmark remote AI models.
