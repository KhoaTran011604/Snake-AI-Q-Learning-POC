/**
 * UI controls + WebSocket management.
 * Coordinates Train/Play/Stop buttons and dispatches data to chart/canvas/heatmap.
 */
(() => {
  const btnTrain = document.getElementById("btn-train");
  const btnPlay = document.getElementById("btn-play");
  const btnStop = document.getElementById("btn-stop");
  const btnReset = document.getElementById("btn-reset");
  const episodeInput = document.getElementById("episode-input");
  const speedSlider = document.getElementById("speed-slider");
  const autoImproveToggle = document.getElementById("auto-improve");

  const statEpisode = document.getElementById("stat-episode");
  const statScore = document.getElementById("stat-score");
  const statBest = document.getElementById("stat-best");
  const statEpsilon = document.getElementById("stat-epsilon");
  const statStatus = document.getElementById("stat-status");

  let ws = null;

  // Init chart on load
  TrainingChart.init();
  GameCanvas.init();

  function setStatus(text) { statStatus.textContent = text; }

  function setButtons(training, playing) {
    btnTrain.disabled = training || playing;
    btnPlay.disabled = training || playing;
    btnStop.disabled = !training;
    btnReset.disabled = training || playing;
    episodeInput.disabled = training || playing;
  }

  function wsUrl(path) {
    const proto = location.protocol === "https:" ? "wss:" : "ws:";
    return `${proto}//${location.host}${path}`;
  }

  // --- TRAIN ---
  btnTrain.addEventListener("click", () => {
    const episodes = parseInt(episodeInput.value) || 1000;
    setButtons(true, false);
    setStatus("Training...");
    TrainingChart.reset();

    ws = new WebSocket(wsUrl("/ws/train"));
    ws.onopen = () => {
      ws.send(JSON.stringify({ episodes }));
    };
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === "train_update") {
        const d = msg.data;
        statEpisode.textContent = d.episode;
        statScore.textContent = d.score;
        statEpsilon.textContent = d.epsilon;
        TrainingChart.addPoint(d.episode, d.avg_score_50);
        statBest.textContent = TrainingChart.getBestAvg().toFixed(1);
      } else if (msg.type === "train_complete") {
        setStatus("Training complete");
        setButtons(false, false);
        ws.close();
        ws = null;
      }
    };
    ws.onerror = () => {
      setStatus("Connection error");
      setButtons(false, false);
    };
    ws.onclose = () => {
      setButtons(false, false);
    };
  });

  // --- PLAY ---
  btnPlay.addEventListener("click", () => {
    setButtons(false, true);
    setStatus("Playing...");

    const speedMs = 310 - parseInt(speedSlider.value); // invert: slider right = faster
    ws = new WebSocket(wsUrl("/ws/play"));
    ws.onopen = () => {
      ws.send(JSON.stringify({ speed_ms: speedMs }));
    };
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === "play_frame") {
        GameCanvas.render(msg.data);
        QHeatmap.render(msg.data.q_values);
        statScore.textContent = msg.data.score;
      } else if (msg.type === "play_complete") {
        handlePlayComplete(msg.data);
      }
    };
    ws.onerror = () => {
      setStatus("Connection error");
      setButtons(false, false);
    };
    ws.onclose = () => {
      setButtons(false, false);
    };
  });

  // --- RESET ---
  btnReset.addEventListener("click", async () => {
    if (!confirm("Reset AI brain? All training progress will be lost.")) return;
    try {
      const res = await fetch("/api/reset", { method: "POST" });
      const data = await res.json();
      if (data.status === "reset") {
        TrainingChart.reset();
        GameCanvas.clear();
        statEpisode.textContent = "0";
        statScore.textContent = "0";
        statBest.textContent = "0";
        statEpsilon.textContent = "1.0";
        setStatus("Brain reset!");
      } else {
        setStatus(data.message || "Reset failed");
      }
    } catch {
      setStatus("Reset failed — connection error");
    }
  });

  // --- PLAY COMPLETE (with optional auto-improve) ---
  async function handlePlayComplete(data) {
    const finalScore = data.final_score;
    if (autoImproveToggle.checked) {
      setStatus(`Score: ${finalScore} — Improving...`);
      try {
        const res = await fetch("/api/improve", { method: "POST" });
        if (!res.ok) throw new Error("Server error");
        const result = await res.json();
        setStatus(`Score: ${finalScore} — Improved! (${result.total_episodes} ep)`);
        statEpsilon.textContent = result.epsilon;
        statBest.textContent = result.best_score;
      } catch {
        setStatus(`Score: ${finalScore} — Improve failed`);
      }
    } else {
      setStatus(`Game over — Score: ${finalScore}`);
    }
    setButtons(false, false);
    if (ws) { ws.close(); ws = null; }
  }

  // --- STOP ---
  btnStop.addEventListener("click", () => {
    if (ws) {
      ws.close();
      ws = null;
    }
    fetch("/api/stop", { method: "POST" });
    setStatus("Stopped");
    setButtons(false, false);
  });
})();
