# Phase 02: Snake Game Engine

## Context
- Parent plan: [plan.md](plan.md)
- Depends on: Phase 01

## Overview
- **Priority**: High
- **Status**: ✅ Complete
- **Effort**: 2h
- Pure Python Snake game engine, no rendering. Headless for fast training.

## Key Insights
- Game must be headless (no pygame) — rendering happens in browser
- Grid size: 20x20 (configurable)
- Must expose full state for both RL agent and WebSocket serialization
- Max steps without eating = 100 * snake_length (prevent infinite loops)

## Requirements
### Functional
- Snake moves in 4 directions (UP/DOWN/LEFT/RIGHT)
- Food spawns randomly on empty cell
- Collision detection: wall + self
- Score tracking (food eaten count)
- Game reset capability

### Non-functional
- Fast execution (>10k steps/sec for training)
- Serializable game state (dict/JSON)
- Deterministic with seed support

## Architecture
```python
class SnakeGame:
    def __init__(self, width=20, height=20)
    def reset(self) -> dict           # Reset game, return initial state
    def step(self, action) -> tuple   # (state, reward, done, info)
    def get_state(self) -> dict       # Full state for rendering
    def get_rl_state(self) -> tuple   # 11 boolean features for Q-table
```

### State representation (11 features for RL)
```
[danger_straight, danger_right, danger_left,   # 3: collision detection
 dir_left, dir_right, dir_up, dir_down,        # 4: current direction
 food_left, food_right, food_up, food_down]    # 4: food relative position
```

### Action space
- 0: Straight (continue current direction)
- 1: Turn right
- 2: Turn left
(Relative actions — simpler than absolute UP/DOWN/LEFT/RIGHT)

### Reward function
```python
if ate_food:     reward = 10
elif died:       reward = -10
elif closer:     reward = 1
elif farther:    reward = -1
if steps_without_food > max: reward = -10, done = True
```

## Related Code Files
**Create:**
- `backend/snake_game.py` — SnakeGame class

## Implementation Steps
1. Define Direction enum (UP, DOWN, LEFT, RIGHT) and Point namedtuple
2. Implement `__init__`: grid size, initial snake (center, length 3), random food
3. Implement `reset()`: reinitialize game state, return state dict
4. Implement `_place_food()`: random empty cell
5. Implement `_is_collision(point)`: check wall + self-body
6. Implement `step(action)`:
   - Convert relative action (straight/right/left) to absolute direction
   - Move snake head
   - Check collision → done
   - Check food eaten → grow + new food + reward
   - Calculate distance reward (closer/farther to food)
   - Check max steps without food
   - Return (rl_state, reward, done, info)
7. Implement `get_rl_state()`: compute 11 boolean features
8. Implement `get_state()`: return full state dict for rendering (snake body, food, score, direction)
9. Test: run 100 random episodes, verify no crashes, scores > 0 sometimes

## Todo
- [x] Direction enum + Point namedtuple
- [x] SnakeGame.__init__ + reset()
- [x] _place_food() + _is_collision()
- [x] step() with relative actions
- [x] Reward calculation
- [x] get_rl_state() — 11 boolean features
- [x] get_state() — full serializable state
- [x] Smoke test: 100 random episodes

## Success Criteria
- 100 random episodes run without errors
- Game correctly detects wall + self collision
- Food respawns after eating
- get_rl_state() returns tuple of 11 booleans
- >10k steps/sec on standard hardware

## Risk Assessment
- Reward shaping wrong → AI learns weird behavior. Mitigation: test reward independently
- Off-by-one in collision detection. Mitigation: edge case tests

## Next Steps
→ Phase 03: Q-Learning Agent
