# Phase 1: Reset Brain

## Muc tieu

Them nut "Reset" de xoa sach Q-Table, dua AI ve trang thai ban dau (chua hoc gi).

## Thay doi

### Backend — `server.py`

Them API endpoint:

```python
@app.post("/api/reset")
async def reset_agent():
    """Reset Q-table and training stats."""
    if trainer.is_training():
        return {"status": "error", "message": "Cannot reset while training"}
    agent.q_table = np.zeros((agent.state_size, agent.action_size))
    agent.epsilon = 1.0
    trainer.stats.clear()
    trainer.best_score = 0
    trainer.recent_scores.clear()
    return {"status": "reset"}
```

Can them `import numpy as np` vao `server.py`.

### Frontend — `index.html`

Them nut Reset vao controls:

```html
<button id="btn-reset">Reset</button>
```

CSS cho nut:

```css
#btn-reset { background: #c0392b; color: #fff; }
```

### Frontend — `controls.js`

Them event listener:

```javascript
const btnReset = document.getElementById("btn-reset");

btnReset.addEventListener("click", async () => {
  if (!confirm("Reset AI brain? All training progress will be lost.")) return;
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
  }
});
```

Them `btnReset.disabled` vao ham `setButtons`:

```javascript
function setButtons(training, playing) {
  btnTrain.disabled = training || playing;
  btnPlay.disabled = training || playing;
  btnStop.disabled = !training;
  btnReset.disabled = training || playing;  // <-- them dong nay
  episodeInput.disabled = training || playing;
}
```

## Todo

- [x] Them `POST /api/reset` vao `server.py`
- [x] Them nut Reset vao `index.html` (HTML + CSS)
- [x] Them logic Reset vao `controls.js`
- [x] Disable nut Reset khi dang train/play

## Success Criteria

- Bam Reset → Q-Table ve 0, epsilon ve 1.0, chart xoa sach
- Nut Reset bi disable khi dang training hoac playing
- Co confirm dialog truoc khi reset
