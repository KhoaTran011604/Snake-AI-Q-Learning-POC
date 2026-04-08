/**
 * Q-value heatmap: 3 horizontal bars showing action preferences.
 * Green = high Q, Red = low Q.
 */
const QHeatmap = (() => {
  const canvas = document.getElementById("q-canvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;
  const labels = ["Straight", "Turn Right", "Turn Left"];

  function render(qValues) {
    ctx.fillStyle = "#16213e";
    ctx.fillRect(0, 0, W, H);

    if (!qValues || qValues.length !== 3) return;

    const barH = 20;
    const gap = 6;
    const startY = 4;
    const labelW = 80;
    const maxBarW = W - labelW - 60;

    // Normalize Q-values for display
    const maxQ = Math.max(...qValues.map(Math.abs), 0.01);
    const bestAction = qValues.indexOf(Math.max(...qValues));

    for (let i = 0; i < 3; i++) {
      const y = startY + i * (barH + gap);
      const normalized = qValues[i] / maxQ;
      const barW = Math.abs(normalized) * maxBarW;

      // Label
      ctx.fillStyle = i === bestAction ? "#e94560" : "#888";
      ctx.font = i === bestAction ? "bold 12px sans-serif" : "12px sans-serif";
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";
      ctx.fillText(labels[i], labelW - 8, y + barH / 2);

      // Bar background
      ctx.fillStyle = "rgba(15, 52, 96, 0.5)";
      ctx.beginPath();
      ctx.roundRect(labelW, y, maxBarW, barH, 3);
      ctx.fill();

      // Bar fill — green-to-red gradient based on value
      const t = (normalized + 1) / 2; // 0=red, 1=green
      const r = Math.round(233 - t * 200);
      const g = Math.round(50 + t * 160);
      ctx.fillStyle = `rgb(${r},${g},80)`;
      ctx.beginPath();
      ctx.roundRect(labelW, y, barW, barH, 3);
      ctx.fill();

      // Value text
      ctx.fillStyle = "#ddd";
      ctx.font = "11px monospace";
      ctx.textAlign = "left";
      ctx.fillText(qValues[i].toFixed(2), labelW + maxBarW + 6, y + barH / 2);
    }
  }

  function clear() {
    ctx.fillStyle = "#16213e";
    ctx.fillRect(0, 0, W, H);
  }

  return { render, clear };
})();
