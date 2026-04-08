---
title: "Snake AI Q-Learning POC"
description: "AI learns to play Snake game using Q-Learning with real-time web visualization"
status: complete
priority: P2
effort: 12h
branch: master
tags: [ai, reinforcement-learning, q-learning, snake, poc, demo]
created: 2026-04-08
---

# Snake AI Q-Learning POC

## Overview
POC demo AI học chơi Snake bằng Q-Learning. Python backend train agent + Web UI visualize training progress realtime qua WebSocket.

**Brainstorm report**: [brainstorm-260408-2209-snake-ai-q-learning.md](../reports/brainstorm-260408-2209-snake-ai-q-learning.md)

## Architecture
```
backend/
├── snake_game.py      — Game engine (grid, snake, food, collision)
├── q_learning.py      — Q-Learning agent (Q-table, epsilon-greedy)
├── trainer.py         — Training loop, episode stats
└── server.py          — FastAPI + WebSocket (train, play, stats)

frontend/
├── index.html         — Layout + CDN imports
├── game-canvas.js     — Snake renderer (Canvas 2D)
├── training-chart.js  — Reward/score chart (Chart.js)
├── q-heatmap.js       — Q-value heatmap overlay
└── controls.js        — Train/Play/Speed controls

requirements.txt       — fastapi, uvicorn, numpy, websockets
```

## Phases

| # | Phase | Effort | Status |
|---|-------|--------|--------|
| 1 | [Project Setup](phase-01-project-setup.md) | 0.5h | ✅ Complete |
| 2 | [Snake Game Engine](phase-02-snake-game-engine.md) | 2h | ✅ Complete |
| 3 | [Q-Learning Agent](phase-03-q-learning-agent.md) | 2.5h | ✅ Complete |
| 4 | [Training Pipeline](phase-04-training-pipeline.md) | 1.5h | ✅ Complete |
| 5 | [FastAPI WebSocket Server](phase-05-fastapi-websocket-server.md) | 2h | ✅ Complete |
| 6 | [Web UI Dashboard](phase-06-web-ui-dashboard.md) | 3h | ✅ Complete |
| 7 | [Integration & Polish](phase-07-integration-polish.md) | 0.5h | ✅ Complete |

## Dependencies
- Phase 3 depends on Phase 2 (game engine)
- Phase 4 depends on Phase 2 + 3
- Phase 5 depends on Phase 4
- Phase 6 depends on Phase 5 (WebSocket API)
- Phase 2 & 3 core logic can be developed in parallel

## Key Decisions
- State: 11 boolean features → 2048 Q-table entries
- Reward: eat +10, die -10, closer +1, farther -1
- Q-params: lr=0.1, gamma=0.9, epsilon 1.0→0.01
- WebSocket throttle: send every N steps
- No PyTorch — numpy only

## Success Metrics
- AI avg score >10 after 5000 episodes
- Clear upward training curve
- Smooth browser demo
- Clean, commented code
