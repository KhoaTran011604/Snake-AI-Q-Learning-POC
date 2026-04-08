# Phase 05: FastAPI WebSocket Server

## Context
- Parent plan: [plan.md](plan.md)
- Depends on: Phase 04

## Overview
- **Priority**: High
- **Status**: ✅ Complete
- **Effort**: 2h
- FastAPI server with WebSocket for realtime training updates + REST for control.

## Key Insights
- WebSocket for streaming: training stats, game frames during play
- REST for control: start/stop training, get config
- Serve frontend static files from FastAPI (no CORS issues)
- Throttle WS messages to prevent browser lag

## Architecture

### API Endpoints
```
REST:
  POST /api/train          — Start training (body: {episodes: int})
  POST /api/stop           — Stop training
  POST /api/play           — Play one episode with best model
  GET  /api/stats          — Get training history
  GET  /api/config         — Get current config (grid size, hyperparams)

WebSocket:
  WS /ws/train             — Stream training stats (every 10 episodes)
  WS /ws/play              — Stream game frames for live replay
```

### WebSocket Message Types
```json
// Training update (every 10 episodes)
{"type": "train_update", "data": {"episode": 100, "score": 5, "avg_score_50": 3.2, "epsilon": 0.6}}

// Training complete
{"type": "train_complete", "data": {"total_episodes": 5000, "best_score": 25}}

// Play frame (step by step)
{"type": "play_frame", "data": {"snake": [[10,10],[10,11]], "food": [5,5], "score": 3, "q_values": [0.5, 0.8, 0.2]}}

// Play complete
{"type": "play_complete", "data": {"final_score": 15}}
```

## Related Code Files
**Create:**
- `backend/server.py` — FastAPI app with WebSocket

## Implementation Steps
1. Create FastAPI app with CORS middleware
2. Mount static files: `frontend/` → `/`
3. Initialize global SnakeGame, QLearningAgent, Trainer instances
4. Implement `POST /api/train`: start training in background task
5. Implement `POST /api/stop`: call trainer.stop()
6. Implement `GET /api/stats`: return trainer.get_stats()
7. Implement `GET /api/config`: return game/agent config
8. Implement `WS /ws/train`:
   - Connect → start receiving training updates
   - Trainer callback sends stats every 10 episodes
   - Send JSON messages, handle disconnect gracefully
9. Implement `WS /ws/play`:
   - On connect, play one episode
   - Stream frames with 100ms delay between (adjustable via message)
   - Send play_complete at end
10. Add error handling for all endpoints
11. Test: start server, verify WS connection with wscat or browser console

## Todo
- [x] FastAPI app + static mount
- [x] Global game/agent/trainer instances
- [x] REST endpoints (train, stop, stats, config)
- [x] WS /ws/train — training updates stream
- [x] WS /ws/play — game replay stream
- [x] Error handling + graceful disconnect
- [x] Manual test with browser

## Success Criteria
- Server starts on `localhost:8000`
- Frontend loads from `/`
- WS /ws/train streams updates every 10 episodes
- WS /ws/play streams frames with configurable speed
- No memory leaks on WS disconnect

## Risk Assessment
- WS disconnect during training → orphan task. Mitigation: training continues, stats stored server-side
- Multiple clients connecting → shared state issues. Mitigation: single trainer instance, broadcast to all clients

## Security Considerations
- Local demo only, no auth needed
- Validate episode count input (max 50000)

## Next Steps
→ Phase 06: Web UI Dashboard
