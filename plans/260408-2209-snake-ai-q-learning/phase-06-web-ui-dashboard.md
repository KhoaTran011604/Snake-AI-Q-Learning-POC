# Phase 06: Web UI Dashboard

## Context
- Parent plan: [plan.md](plan.md)
- Depends on: Phase 05

## Overview
- **Priority**: High
- **Status**: ⬜ Pending
- **Effort**: 3h
- Browser dashboard: game canvas, training chart, Q-value heatmap, controls.

## Key Insights
- Single page, no framework — Vanilla JS + Canvas + Chart.js CDN
- Dark theme for "tech demo" look
- Responsive layout: game left, charts right, controls top
- Chart.js for training curve, Canvas 2D for game + heatmap

## Architecture

### Layout
```
┌──────────────────────────────────────────────┐
│  🐍 Snake AI Q-Learning    [Train] [Play] ⚡ │
├──────────────────┬───────────────────────────┤
│                  │  Training Progress         │
│   Snake Game     │  ┌───────────────────┐    │
│   Canvas         │  │ reward chart      │    │
│   (400x400)      │  └───────────────────┘    │
│                  │  Q-Value Heatmap           │
│                  │  ┌───────────────────┐    │
│                  │  │ action heatmap    │    │
│                  │  └───────────────────┘    │
├──────────────────┴───────────────────────────┤
│  Episode: 1234  Score: 12  Epsilon: 0.05     │
└──────────────────────────────────────────────┘
```

### Components
1. **game-canvas.js**: Render snake (green segments), food (red), grid lines (subtle gray)
2. **training-chart.js**: Line chart — x: episode, y: avg score (rolling 50). Update realtime via Chart.js
3. **q-heatmap.js**: Show Q-values for 3 actions (straight/right/left) as colored bars below game — during play mode
4. **controls.js**: Train button (with episode input), Play button, Speed slider, Status display

### Color Scheme (dark theme)
- Background: #1a1a2e
- Grid: #16213e
- Snake: #0f3460 → #e94560 gradient (head red, body blue)
- Food: #e94560 (pulsing)
- Text: #eee

## Related Code Files
**Create:**
- `frontend/index.html` — Layout + CDN imports + inline critical CSS
- `frontend/game-canvas.js` — Snake game renderer
- `frontend/training-chart.js` — Chart.js training curve
- `frontend/q-heatmap.js` — Q-value action bars
- `frontend/controls.js` — UI controls + WebSocket management

## Implementation Steps
1. **index.html**: Layout with CSS Grid, import Chart.js CDN, dark theme CSS
2. **game-canvas.js**:
   - Init 400x400 canvas
   - `render(gameState)`: draw grid → food → snake body → head
   - Snake head = darker/larger, body gradient
   - Food pulsing animation (optional, time permitting)
3. **training-chart.js**:
   - Init Chart.js line chart (episode vs avg_score)
   - `addDataPoint(episode, avgScore)`: append + update
   - Auto-scroll x-axis, keep last 1000 points visible
   - Gradient fill under line
4. **q-heatmap.js**:
   - 3 horizontal bars: straight, right, left
   - Color: green (high Q) → red (low Q)
   - Labels: action names + Q-value numbers
   - Update per frame during play mode
5. **controls.js**:
   - Train button → POST /api/train + connect WS /ws/train
   - Play button → connect WS /ws/play
   - Speed slider → send speed message via WS
   - Episode counter, score display, epsilon display
   - Handle WS messages → dispatch to chart/canvas/heatmap
6. Wire everything together: controls.js acts as coordinator
7. Test: full flow — train 1000 episodes → play → verify all components update

## Todo
- [ ] index.html layout + dark theme CSS
- [ ] game-canvas.js — snake renderer
- [ ] training-chart.js — Chart.js reward curve
- [ ] q-heatmap.js — Q-value action bars
- [ ] controls.js — buttons + WS management
- [ ] Integration: wire all components
- [ ] Visual test in browser

## Success Criteria
- Dashboard loads, dark theme looks clean
- Game canvas renders snake smoothly during play
- Chart updates realtime during training
- Q-value bars show meaningful differences between actions
- Controls responsive, no dead buttons

## Risk Assessment
- Chart.js performance with many data points. Mitigation: keep last 1000 points
- Canvas rendering jank during fast play. Mitigation: requestAnimationFrame
- WebSocket reconnection if server restarts. Mitigation: auto-reconnect with backoff

## Next Steps
→ Phase 07: Integration & Polish
