---
{"title":"Connect 4 AI","slug":"connect-4-ai","category":"AI · Interactive systems","description":"A playable experiment in model-backed decision making, with three opponent routes and a lightweight browser interface.","tools":["JavaScript","HTTP API","Static hosting"],"image":"/assets/connect4-board.svg","image_alt":"Illustration of a six-row, seven-column Connect 4 board","featured":true,"status":"Playable interface"}
---
## Overview

Connect 4 makes a useful interface for exploring sequential decisions: the rules are simple, the board is small, and a move can change the direction of a game. This project pairs a browser game with a separately hosted inference API.

[Play Connect 4 →](/connect4/)

## Problem

Give players a clear way to try different AI opponents without installing software. The interface needs to communicate whose turn it is, enforce legal moves, and keep a game usable when the inference service is unavailable.

## My contribution

The public website presents this as a personal project. The implementation available here covers the browser board, controls, API integration, game results, and persistent match records. Model authorship and training details require the separate backend source before a more specific account can be published.

## Tools and methodology

The frontend uses vanilla JavaScript. A six-by-seven board holds empty cells, user pieces, and opponent pieces. Requests convert these to numeric values: 0 is empty; 1 and 2 identify the first and second players, respectively.

| Mode | API model identifier | Existing model description |
| --- | --- | --- |
| Casual | `transformer` | Transformer |
| Challenge | `cnn` | Convolutional neural network |
| Insane | `pg` | Policy gradient |

These names describe the existing interface and API contract. They are not verified rankings of difficulty. Architectures, layer counts, training objectives, and checkpoints are absent from this repository.

## Implementation and deployment

The static browser client sends the board and opponent identifier to a separate service. Move inference runs outside the website deployment.

![Verified request flow: browser board, move request, separate API, returned column](/assets/connect4-flow.svg)

```json
{"modelType":"cnn","board":[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0]]}
```

`POST /connect4-api/move` returns `best_move`. The client checks the returned column and applies gravity. It detects horizontal, vertical, and diagonal wins and full-board draws. Players can choose the first move, reset, or resign. Match records are stored in the browser, separately for each opponent and in total.

## Training methodology and evaluation

**Documentation pending.** The old methodology page referred to large-scale self-play and automated matches, but no code, training logs, dataset, or results support those details in this checkout. It also described two modeling approaches despite the three available routes.

Frontend tests can verify routing, encoding, controls, and game behavior. They cannot establish model strength. A reproducible model comparison would need fixed checkpoints, seeded matches, alternate starting players, a defined opponent baseline, and a record of service failures. No model win rate or latency benchmark is published here.

## Trade-offs and limitations

Separating inference keeps the site small and avoids distributing model files, while introducing a dependency on API availability and cross-origin access. On request failure, the existing client selects a random legal move. An invalid returned column falls back to the first legal column. A completed game therefore does not prove that a model answered every request.

The redesign preserves the game script and its algorithms. Known follow-ups include request cancellation during reset, a bounded request timeout, richer keyboard board announcements, and clearer per-move fallback reporting. These are future improvements, not completed features.

## Resources

- [Play all three modes](/connect4/)
- [Frontend implementation on GitHub](https://github.com/eshaanarora99/eshaan-arora-website/blob/main/connect4/assets/connect4.js)
- [Verified interface notes](/connect4/training-methodology/)
