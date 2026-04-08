# Brainstorm: Snake AI với Q-Learning

**Date:** 2026-04-08
**Status:** Agreed
**Timeline:** 1.5-2 ngày

## Problem Statement
Tạo POC demo "AI học chơi game Snake" dùng Reinforcement Learning. Mục tiêu: dễ demo cho developer, dễ học RL, UI trực quan thấy AI tiến bộ từ random → smart.

## Requirements
- Audience: Developer / Kỹ sư
- RL experience: Người mới (chưa từng)
- Timeline: 1-3 ngày (target 1.5-2 ngày)
- Demo: visual rõ ràng, thấy AI improve over time

## Evaluated Approaches

### 1. Snake + Q-Learning ✅ CHOSEN
- **Pros**: State space nhỏ (2048 states), train nhanh, Q-table dễ visualize, dễ hiểu algorithm
- **Cons**: Không "deep learning" — nhưng đủ cho demo RL concepts

### 2. Flappy Bird + DQN ❌
- **Pros**: Game quen thuộc, dùng neural network
- **Cons**: 2-3 ngày, cần tune hyperparams, risk không converge cho người mới

### 3. Snake + NEAT ❌
- **Pros**: Visual neural net evolution rất cool
- **Cons**: Không phải mainstream RL, ít transferable knowledge

### 4. 2048 + Q-Learning ❌
- **Pros**: Simple game logic
- **Cons**: Visual kém hấp dẫn hơn Snake

## Final Solution

### Architecture
```
Python Backend (FastAPI + WebSocket)
├── snake_game.py      — Game engine
├── q_learning.py      — Q-Learning agent
├── trainer.py         — Training loop
└── server.py          — FastAPI + WS endpoints

Web Frontend (Vanilla JS)
├── index.html
├── game-canvas.js     — Snake renderer
├── training-chart.js  — Reward chart (Chart.js)
├── q-heatmap.js       — Q-value heatmap
└── controls.js        — Start/Stop/Speed
```

### Key Design Decisions

**State representation (11 boolean features → 2048 states)**:
- Danger: straight, left, right (3)
- Direction: up, down, left, right (4)
- Food relative: up, down, left, right (4)

**Reward function**:
- Eat food: +10
- Die: -10
- Move closer to food: +1
- Move away from food: -1
- Too many steps without eating: -10

**Tech stack**: Python + numpy (RL), FastAPI + WebSocket (API), Vanilla JS + Canvas + Chart.js (UI)

**WebSocket throttling**: Gửi game state mỗi N steps, không mỗi step → tránh lag

### Demo Flow
1. Start training → xem AI chết liên tục (random actions)
2. Fast-forward 1000 episodes → AI bắt đầu ăn food
3. Show Q-table heatmap = visualize AI "suy nghĩ"
4. Training reward chart tăng dần = bằng chứng AI học

## Risks
| Risk | Mitigation |
|------|-----------|
| Q-table state space lớn | Relative features giữ ở 2048 states |
| WebSocket lag | Throttle game state updates |
| Reward shaping sai | Test reward riêng trước khi build UI |

## Success Metrics
- AI đạt avg score > 10 food sau 5000 episodes
- Training chart cho thấy upward trend rõ ràng
- Demo chạy smooth trên browser, không lag
- Code dễ đọc, có comments giải thích RL concepts

## Next Steps
→ Tạo implementation plan chi tiết với phases
