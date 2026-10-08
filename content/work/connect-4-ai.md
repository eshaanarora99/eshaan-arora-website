---
{"title":"Connect 4 AI","slug":"connect-4-ai","category":"AI · Interactive systems","description":"The classic game, with three AI opponents to play against and compare.","tools":["JavaScript","Machine learning","Web development"],"image":"/assets/connect4-board.svg","image_alt":"Illustration of a six-row, seven-column Connect 4 board","featured":true,"status":"Play now"}
---
## A familiar game, different opponents

Connect 4 has simple rules and plenty of room for strategy. One move can block a threat, set a trap, or open a path to victory. That makes it an appealing setting for exploring how different approaches to machine learning show up in a game you can actually play.

I built this project to bring those ideas into the browser. Choose an opponent, decide who goes first, and try to connect four before the AI does.

[Play Connect 4 →](/connect4/)

## What I built

The game combines an interactive board with AI opponents served from a separate backend. I built the browser experience around clear turn-by-turn feedback: choosing the first move, dropping pieces, seeing the result, and starting another match.

Wins, losses, and draws are saved in your browser, both for each opponent and across all modes. You can reset a board or resign at any point.

## Three ways to play

| Mode | Opponent |
| --- | --- |
| [Casual](/connect4/play-transformer/) | Transformer |
| [Challenge](/connect4/play-cnn/) | Convolutional neural network (CNN) |
| [Insane](/connect4/play-policy-gradient/) | Policy gradient |

The models give the project three different approaches to move selection. CNNs are commonly used to recognize spatial patterns, transformers model relationships across an input, and policy-gradient methods learn how to choose actions. Here, the shared board and rules provide a way to explore those approaches through play.

## How it works

The browser handles the rules: pieces fall to the lowest available space, and four connected pieces win horizontally, vertically, or diagonally. After your move, it sends the current board to the selected opponent and places the returned move.

![A move travels from the browser board to the AI service and back](/assets/connect4-flow.svg)

The board is represented as a six-by-seven grid. Keeping the game interface separate from model inference lets the website stay lightweight while the backend handles the opponent's decisions.

## Design trade-offs

A game is a practical test of an AI interface. The player needs to know when to act, when the opponent is thinking, and when a match is over. Responsiveness and clear feedback matter alongside the model's choices.

Hosting inference separately also makes the game dependent on a network connection. If the AI service is unavailable, the game uses random legal moves so a match can continue. Those moves are a fallback, not the selected model's decisions.

## What I’d explore next

A useful next step would be a controlled comparison of the opponents: alternating the first player, using consistent match conditions, and separating model moves from fallback moves. Clearer connection feedback and faster responses would also improve the playing experience.

## Try it yourself

- [Choose an opponent and play](/connect4/)
- [How to play and what the modes mean](/connect4/training-methodology/)
- [Explore the game code on GitHub](https://github.com/eshaanarora99/eshaan-arora-website/blob/main/connect4/assets/connect4.js)
