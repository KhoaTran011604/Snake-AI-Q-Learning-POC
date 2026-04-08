# Phase 04: Training Pipeline

## Context
- Parent plan: [plan.md](plan.md)
- Depends on: Phase 02 + Phase 03

## Overview
- **Priority**: High
- **Status**: ⬜ Pending
- **Effort**: 1.5h
- Training loop that connects SnakeGame + QLearningAgent, tracks stats, supports pause/resume.

## Key Insights
- Must be async-friendly (FastAPI runs in asyncio)
- Training runs in background, WebSocket streams updates
- Need callback mechanism for WebSocket to receive training progress
- Stats per episode: score, total_reward, steps, epsilon

## Architecture
```python
class Trainer:
    def __init__(self, game: SnakeGame, agent: QLearningAgent)

    async def train(self, num_episodes: int, callback=None)
    def train_episode(self) -> dict       # Single episode, return stats
    def play_episode(self) -> list[dict]  # Play with trained agent, return frames
    def get_stats(self) -> dict           # Training history
    def stop(self)                        # Stop training loop
    def is_training(self) -> bool
```

### Episode Stats (sent via callback)
```python
{
    "episode": int,
    "score": int,          # food eaten
    "total_reward": float,
    "steps": int,
    "epsilon": float,
    "avg_score_50": float  # rolling average last 50
}
```

### Play Mode (for demo replay)
```python
# Returns list of frames for step-by-step replay
[{"snake": [...], "food": [x,y], "score": int, "q_values": [...]}, ...]
```

## Related Code Files
**Create:**
- `backend/trainer.py` — Trainer class

## Implementation Steps
1. Implement `__init__`: store game + agent references, init stats lists
2. Implement `train_episode()`:
   - game.reset()
   - Loop: get_rl_state → agent.get_action → game.step → agent.update
   - Until done
   - agent.decay_epsilon()
   - Return episode stats dict
3. Implement `train(num_episodes, callback)`:
   - Async loop calling train_episode
   - Every N episodes (e.g., 10), await callback with stats batch
   - Check self._stop_flag for pause/stop
   - yield control with asyncio.sleep(0) periodically
4. Implement `play_episode()`:
   - Like train but no update, epsilon=0
   - Collect every frame (game state + q_values)
   - Return frame list for replay
5. Implement `get_stats()`: return full training history
6. Implement `stop()`: set stop flag
7. Test: train 100 episodes, verify stats collected correctly

## Todo
- [ ] Trainer.__init__
- [ ] train_episode() — single episode loop
- [ ] train() — async multi-episode with callback
- [ ] play_episode() — collect frames for replay
- [ ] get_stats() + stop()
- [ ] Smoke test: 100 episodes

## Success Criteria
- 1000 episodes train in <5 seconds
- Stats accurately track score/reward/epsilon per episode
- play_episode returns valid frame sequence
- stop() halts training within 1 episode

## Risk Assessment
- Async training blocking event loop. Mitigation: yield with asyncio.sleep(0)
- Memory growth from storing all stats. Mitigation: keep only last 10k episodes

## Next Steps
→ Phase 05: FastAPI WebSocket Server
