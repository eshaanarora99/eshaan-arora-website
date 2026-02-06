/* ===== Connect4 UI + ML Backend (Drop-in) =====
   - Calls your Django API: POST { board, modelType } -> { best_move }
   - board sent as 6x7 numeric (0 empty, 1/2 players)
   - Supports user going first/second
   - Tracks wins/losses/draws in localStorage
*/

const CONNECT4_ROWS = 6;
const CONNECT4_COLS = 7;
const AI_MOVE_DELAY_MS = 300;

const API_BASE = "https://api-connect4.eshaanarora.com/connect4-api";

const boardElement = document.getElementById("connect4-board");

const getStatsDefaults = () => ({ user: 0, ai: 0, draws: 0 });

const loadStats = (key) => {
  const stored = localStorage.getItem(key);
  if (!stored) return getStatsDefaults();
  try {
    const parsed = JSON.parse(stored);
    return { ...getStatsDefaults(), ...parsed };
  } catch {
    return getStatsDefaults();
  }
};

const saveStats = (key, stats) => {
  localStorage.setItem(key, JSON.stringify(stats));
};

// Convert UI board (null/'user'/'ai') -> API board (0/1/2)
const buildApiBoard = (uiBoard, userGoesFirst) => {
  const userVal = userGoesFirst ? 1 : 2;
  const aiVal = userGoesFirst ? 2 : 1;

  return uiBoard.map((row) =>
    row.map((cell) => {
      if (cell === null) return 0;
      if (cell === "user") return userVal;
      return aiVal; // "ai"
    })
  );
};

// Call backend to get AI move
const getAIMove = async (uiBoard, opponentType, userGoesFirst) => {
  const res = await fetch(`${API_BASE}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      modelType: opponentType, // 'cnn' or 'transformer'
      board: buildApiBoard(uiBoard, userGoesFirst),
    }),
  });

  if (!res.ok) throw new Error(`Move API failed: ${res.status}`);
  const data = await res.json();
  if (data?.error) throw new Error(data.error);

  const move = data?.best_move;
  if (typeof move !== "number") throw new Error("No best_move returned");
  return move;
};

window.getAIMove = getAIMove;

const initConnect4 = () => {
  if (!boardElement) return;

  const opponentType = document.body.dataset.opponent || "cnn";
  const statsKey = `connect4:stats:${opponentType}`;
  const totalStatsKey = "connect4:stats:total";

  const statusElement = document.getElementById("connect4-status");
  const startButton = document.getElementById("connect4-start");
  const resetButton = document.getElementById("connect4-reset");
  const resignButton = document.getElementById("connect4-resign");
  const userColorElement = document.getElementById("connect4-user-color");
  const aiColorElement = document.getElementById("connect4-ai-color");
  const userWinsElement = document.getElementById("connect4-user-wins");
  const aiWinsElement = document.getElementById("connect4-ai-wins");
  const drawsElement = document.getElementById("connect4-draws");
  const totalUserWinsElement = document.getElementById("connect4-total-user-wins");
  const totalAiWinsElement = document.getElementById("connect4-total-ai-wins");
  const totalDrawsElement = document.getElementById("connect4-total-draws");

  let board = [];
  let cells = [];
  let currentPlayer = "user";
  let gameActive = false;
  let userGoesFirst = true;

  const updateStatus = (message) => {
    if (statusElement) statusElement.textContent = message;
  };

  const updateStatsDisplay = () => {
    const stats = loadStats(statsKey);
    const totalStats = loadStats(totalStatsKey);

    if (userWinsElement) userWinsElement.textContent = stats.user;
    if (aiWinsElement) aiWinsElement.textContent = stats.ai;
    if (drawsElement) drawsElement.textContent = stats.draws;

    if (totalUserWinsElement) totalUserWinsElement.textContent = totalStats.user;
    if (totalAiWinsElement) totalAiWinsElement.textContent = totalStats.ai;
    if (totalDrawsElement) totalDrawsElement.textContent = totalStats.draws;
  };

  const recordResult = (result) => {
    const stats = loadStats(statsKey);
    const totalStats = loadStats(totalStatsKey);

    if (result === "user") {
      stats.user += 1;
      totalStats.user += 1;
    } else if (result === "ai") {
      stats.ai += 1;
      totalStats.ai += 1;
    } else if (result === "draw") {
      stats.draws += 1;
      totalStats.draws += 1;
    }

    saveStats(statsKey, stats);
    saveStats(totalStatsKey, totalStats);
    updateStatsDisplay();
  };

  const setColors = () => {
    if (!userColorElement || !aiColorElement) return;

    if (userGoesFirst) {
      userColorElement.textContent = "Red";
      aiColorElement.textContent = "Blue";
    } else {
      userColorElement.textContent = "Blue";
      aiColorElement.textContent = "Red";
    }
  };

  const createBoard = () => {
    boardElement.innerHTML = "";
    cells = [];

    for (let row = 0; row < CONNECT4_ROWS; row += 1) {
      const rowCells = [];
      for (let col = 0; col < CONNECT4_COLS; col += 1) {
        const cell = document.createElement("button");
        cell.type = "button";
        cell.className = "connect4-cell";
        cell.dataset.row = row;
        cell.dataset.col = col;
        cell.setAttribute("aria-label", `Column ${col + 1}`);
        boardElement.appendChild(cell);
        rowCells.push(cell);
      }
      cells.push(rowCells);
    }
  };

  const resetBoard = () => {
    board = Array.from({ length: CONNECT4_ROWS }, () =>
      Array.from({ length: CONNECT4_COLS }, () => null)
    );

    for (let row = 0; row < CONNECT4_ROWS; row += 1) {
      for (let col = 0; col < CONNECT4_COLS; col += 1) {
        const cell = cells[row][col];
        cell.classList.remove("is-red", "is-blue");
      }
    }
  };

  const applyPieceToCell = (row, col, player) => {
    const cell = cells[row][col];
    if (!cell) return;

    if (player === "user") {
      cell.classList.add(userGoesFirst ? "is-red" : "is-blue");
    } else {
      cell.classList.add(userGoesFirst ? "is-blue" : "is-red");
    }
  };

  const dropPiece = (col, player) => {
    for (let row = CONNECT4_ROWS - 1; row >= 0; row -= 1) {
      if (board[row][col] === null) {
        board[row][col] = player;
        applyPieceToCell(row, col, player);
        return row;
      }
    }
    return -1;
  };

  const checkLine = (row, col, deltaRow, deltaCol, player) => {
    let count = 0;
    let currentRow = row;
    let currentCol = col;

    while (
      currentRow >= 0 &&
      currentRow < CONNECT4_ROWS &&
      currentCol >= 0 &&
      currentCol < CONNECT4_COLS &&
      board[currentRow][currentCol] === player
    ) {
      count += 1;
      currentRow += deltaRow;
      currentCol += deltaCol;
    }

    return count;
  };

  const isWinningMove = (player) => {
    for (let row = 0; row < CONNECT4_ROWS; row += 1) {
      for (let col = 0; col < CONNECT4_COLS; col += 1) {
        if (board[row][col] !== player) continue;

        const horizontal =
          checkLine(row, col, 0, 1, player) + checkLine(row, col, 0, -1, player) - 1;
        const vertical =
          checkLine(row, col, 1, 0, player) + checkLine(row, col, -1, 0, player) - 1;
        const diagonalDown =
          checkLine(row, col, 1, 1, player) + checkLine(row, col, -1, -1, player) - 1;
        const diagonalUp =
          checkLine(row, col, -1, 1, player) + checkLine(row, col, 1, -1, player) - 1;

        if (horizontal >= 4 || vertical >= 4 || diagonalDown >= 4 || diagonalUp >= 4) {
          return true;
        }
      }
    }
    return false;
  };

  const isBoardFull = () => board[0].every((cell) => cell !== null);

  const endGame = (result, message) => {
    gameActive = false;
    boardElement.classList.add("is-disabled");

    if (result === "user") updateStatus(message || "You win! Great game.");
    else if (result === "ai") updateStatus(message || "AI wins. Try again!");
    else updateStatus(message || "It's a draw.");

    recordResult(result);
  };

  const handleAIMove = async () => {
    if (!gameActive) return;

    let chosenMove;
    try {
      chosenMove = await getAIMove(board, opponentType, userGoesFirst);
    } catch {
      // Fallback: random legal move if API fails
      const legal = [];
      for (let col = 0; col < CONNECT4_COLS; col += 1) {
        if (board[0][col] === null) legal.push(col);
      }
      if (!legal.length) {
        endGame("draw", "No moves left.");
        return;
      }
      chosenMove = legal[Math.floor(Math.random() * legal.length)];
    }

    // Validate returned move
    if (
      typeof chosenMove !== "number" ||
      chosenMove < 0 ||
      chosenMove >= CONNECT4_COLS ||
      board[0][chosenMove] !== null
    ) {
      const fallbackMove = board[0].findIndex((cell) => cell === null);
      if (fallbackMove === -1) {
        endGame("draw", "No moves left.");
        return;
      }
      chosenMove = fallbackMove;
    }

    dropPiece(chosenMove, "ai");

    if (isWinningMove("ai")) return endGame("ai");
    if (isBoardFull()) return endGame("draw");

    currentPlayer = "user";
    updateStatus("Your turn.");
  };

  const requestAIMove = () => {
    updateStatus("AI is thinking...");
    setTimeout(() => {
      handleAIMove();
    }, AI_MOVE_DELAY_MS);
  };

  const handleUserMove = (col) => {
    if (!gameActive || currentPlayer !== "user") return;

    const row = dropPiece(col, "user");
    if (row === -1) return;

    if (isWinningMove("user")) return endGame("user");
    if (isBoardFull()) return endGame("draw");

    currentPlayer = "ai";
    requestAIMove();
  };

  const startGame = async () => {
    const selection = document.querySelector('input[name="first-move"]:checked');
    userGoesFirst = selection ? selection.value === "user" : true;

    resetBoard();
    setColors();
    gameActive = true;
    boardElement.classList.remove("is-disabled");
    currentPlayer = userGoesFirst ? "user" : "ai";

    updateStatus(userGoesFirst ? "Your turn. You are Red." : "AI is going first... You are Blue.");

    if (!userGoesFirst) requestAIMove();
  };

  const resetGame = () => {
    gameActive = false;
    currentPlayer = "user";
    resetBoard();
    boardElement.classList.add("is-disabled");
    updateStatus("Choose who goes first, then start the game.");
  };

  boardElement.addEventListener("click", (event) => {
    const cell = event.target.closest("button[data-col]");
    if (!cell) return;
    const col = Number(cell.dataset.col);
    if (Number.isNaN(col)) return;
    handleUserMove(col);
  });

  if (startButton) startButton.addEventListener("click", startGame);
  if (resetButton) resetButton.addEventListener("click", resetGame);

  if (resignButton) {
    resignButton.addEventListener("click", () => {
      if (!gameActive) return;
      endGame("ai", "You resigned. AI takes the win.");
    });
  }

  // Optional: quick connectivity ping (won't block gameplay)
  fetch(`${API_BASE}/health`)
    .then((r) => r.json())
    .then(() => updateStatus("Server connected. Choose who goes first, then start the game."))
    .catch(() => updateStatus("Server not reachable. AI may fall back."));

  createBoard();
  resetBoard();
  setColors();
  updateStatsDisplay();
  resetGame();
};

initConnect4();
