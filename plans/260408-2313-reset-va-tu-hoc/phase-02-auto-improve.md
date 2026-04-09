# Phase 2: Auto-Improve Sau Moi Lan Play

## Muc tieu

Sau moi lan Play ket thuc (game over), AI tu dong huan luyen them mot so episode ngan de **rut kinh nghiem** tu lan choi do. Muc dich: lan Play sau co ti le pha ky luc cao hon.

## Thiet ke

### Co che hoat dong

```
Play game → Game over → Auto-train 50 episodes (im lang) → Thong bao xong
                                                            → Lan Play tiep se kha hon
```

### Tai sao hieu qua?

- Sau khi play, epsilon dang rat thap (~0.01) → AI gan nhu chi khai thac
- Auto-train 50 episode voi epsilon tang nhe (0.1) → AI kham pha them vung chua biet
- Sau do ha epsilon lai → AI khai thac tri thuc moi

### Backend — `trainer.py`

Them method `improve()`:

```python
def improve(self, episodes=50):
    """Quick self-improvement: train with slight exploration."""
    old_epsilon = self.agent.epsilon
    self.agent.epsilon = max(0.1, self.agent.epsilon)  # tang exploration tam
    
    for _ in range(episodes):
        self.train_episode()
    
    self.agent.epsilon = old_epsilon * 0.95  # giam nhe sau moi lan improve
```

### Backend — `server.py`

Them API endpoint:

```python
@app.post("/api/improve")
async def auto_improve():
    """Run quick improvement after a play session."""
    if trainer.is_training():
        return {"status": "error", "message": "Already training"}
    trainer.improve(episodes=50)
    return {
        "status": "improved",
        "total_episodes": len(trainer.stats),
        "best_score": trainer.best_score,
        "epsilon": round(agent.epsilon, 4),
    }
```

### Frontend — `index.html`

Them toggle cho auto-improve:

```html
<label class="toggle-label">
  <input type="checkbox" id="auto-improve" checked>
  Auto-improve
</label>
```

CSS:

```css
.toggle-label { font-size: 0.85rem; color: #aaa; display: flex; align-items: center; gap: 4px; }
.toggle-label input { accent-color: #e94560; }
```

### Frontend — `controls.js`

Sua lai phan `play_complete` trong event listener cua nut Play:

```javascript
const autoImproveToggle = document.getElementById("auto-improve");

// Trong ws.onmessage cua Play:
} else if (msg.type === "play_complete") {
  const finalScore = msg.data.final_score;
  
  if (autoImproveToggle.checked) {
    setStatus(`Score: ${finalScore} — Improving...`);
    // Goi auto-improve
    const res = await fetch("/api/improve", { method: "POST" });
    const data = await res.json();
    setStatus(`Score: ${finalScore} — Improved! (${data.total_episodes} ep total)`);
    statEpsilon.textContent = data.epsilon;
    statBest.textContent = data.best_score;
  } else {
    setStatus(`Game over — Score: ${finalScore}`);
  }
  
  setButtons(false, false);
  ws.close();
  ws = null;
}
```

**Luu y**: Vi `onmessage` khong ho tro `async` truc tiep, can wrap:

```javascript
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  if (msg.type === "play_frame") {
    // ... render
  } else if (msg.type === "play_complete") {
    handlePlayComplete(msg.data);
  }
};

async function handlePlayComplete(data) {
  const finalScore = data.final_score;
  if (autoImproveToggle.checked) {
    setStatus(`Score: ${finalScore} — Improving...`);
    const res = await fetch("/api/improve", { method: "POST" });
    const result = await res.json();
    setStatus(`Score: ${finalScore} — Improved! (${result.total_episodes} ep)`);
    statEpsilon.textContent = result.epsilon;
  } else {
    setStatus(`Game over — Score: ${finalScore}`);
  }
  setButtons(false, false);
  ws.close();
  ws = null;
}
```

## Todo

- [x] Them `improve()` method vao `trainer.py`
- [x] Them `POST /api/improve` vao `server.py`
- [x] Them checkbox Auto-improve vao `index.html` (HTML + CSS)
- [x] Sua logic `play_complete` trong `controls.js`
- [x] Xu ly async dung cach trong `onmessage`

## Success Criteria

- Sau moi lan Play xong, neu Auto-improve bat → AI tu train 50 episode
- Status bar hien thi "Improving..." trong luc train
- Epsilon giam dan sau moi lan improve → AI ngay cang thong minh
- Co the tat Auto-improve bang checkbox
- Khong block UI trong luc improve (50 ep rat nhanh, ~1 giay)

## Rui ro

- 50 episode co the chua du de thay su khac biet → co the tang len 100 neu can
- Neu user spam Play lien tuc, improve chong cheo → da co guard `is_training()`
