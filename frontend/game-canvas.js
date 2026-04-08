/**
 * Snake game renderer on Canvas 2D.
 * Draws grid, food (pulsing), snake body with gradient head.
 */
const GameCanvas = (() => {
  const canvas = document.getElementById("game-canvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;
  let gridW = 20, gridH = 20;
  let cellW, cellH;
  let pulsePhase = 0;

  function init(width = 20, height = 20) {
    gridW = width;
    gridH = height;
    cellW = W / gridW;
    cellH = H / gridH;
  }

  function render(state) {
    if (!state) return;
    pulsePhase += 0.15;

    // Background
    ctx.fillStyle = "#16213e";
    ctx.fillRect(0, 0, W, H);

    // Grid lines
    ctx.strokeStyle = "rgba(15, 52, 96, 0.4)";
    ctx.lineWidth = 0.5;
    for (let x = 0; x <= gridW; x++) {
      ctx.beginPath();
      ctx.moveTo(x * cellW, 0);
      ctx.lineTo(x * cellW, H);
      ctx.stroke();
    }
    for (let y = 0; y <= gridH; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * cellH);
      ctx.lineTo(W, y * cellH);
      ctx.stroke();
    }

    // Food (pulsing red)
    if (state.food) {
      const pulse = 1 + 0.15 * Math.sin(pulsePhase);
      const fx = state.food[0] * cellW + cellW / 2;
      const fy = state.food[1] * cellH + cellH / 2;
      const r = (cellW / 2 - 2) * pulse;
      ctx.beginPath();
      ctx.arc(fx, fy, r, 0, Math.PI * 2);
      ctx.fillStyle = "#e94560";
      ctx.fill();
      // Glow
      ctx.beginPath();
      ctx.arc(fx, fy, r + 3, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(233, 69, 96, 0.2)";
      ctx.fill();
    }

    // Snake body
    const snake = state.snake;
    if (!snake || snake.length === 0) return;
    const len = snake.length;

    for (let i = len - 1; i >= 0; i--) {
      const [sx, sy] = snake[i];
      const pad = i === 0 ? 1 : 2;
      const t = len > 1 ? i / (len - 1) : 0;

      // Gradient: head (#e94560) → tail (#0f3460)
      const r = Math.round(233 - t * (233 - 15));
      const g = Math.round(69 - t * (69 - 52));
      const b = Math.round(96 - t * (96 - 96));
      ctx.fillStyle = `rgb(${r},${g},${b})`;

      ctx.beginPath();
      ctx.roundRect(sx * cellW + pad, sy * cellH + pad, cellW - pad * 2, cellH - pad * 2, 3);
      ctx.fill();
    }

    // Head eyes
    const [hx, hy] = snake[0];
    const cx = hx * cellW + cellW / 2;
    const cy = hy * cellH + cellH / 2;
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(cx - 3, cy - 2, 2, 0, Math.PI * 2);
    ctx.arc(cx + 3, cy - 2, 2, 0, Math.PI * 2);
    ctx.fill();
  }

  function clear() {
    ctx.fillStyle = "#16213e";
    ctx.fillRect(0, 0, W, H);
  }

  return { init, render, clear };
})();
