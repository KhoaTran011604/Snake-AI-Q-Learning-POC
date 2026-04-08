# Snake AI — Q-Learning POC

AI learns to play Snake using tabular Q-Learning with a real-time web dashboard. Watch the agent evolve from random moves to strategic food-seeking behavior.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn backend.server:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

## How to Demo

1. **Train** — Set episodes (1000-5000) and click Train. Watch the reward chart climb.
2. **Play** — After training, click Play to watch the AI play live with Q-value visualization.
3. **Speed** — Adjust the slider to control playback speed.

## Tech Stack

- **Backend**: Python, FastAPI, WebSocket, NumPy
- **Frontend**: Vanilla JS, Canvas 2D, Chart.js
- **RL**: Tabular Q-Learning (11 boolean features → 2048 states, 3 actions)
