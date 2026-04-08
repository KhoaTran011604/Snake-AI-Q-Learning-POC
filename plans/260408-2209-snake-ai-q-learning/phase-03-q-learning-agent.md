# Phase 03: Q-Learning Agent

## Context
- Parent plan: [plan.md](plan.md)
- Depends on: Phase 02 (SnakeGame.get_rl_state() interface)

## Overview
- **Priority**: High
- **Status**: ✅ Complete
- **Effort**: 2.5h
- Tabular Q-Learning agent using numpy. Core RL algorithm for the POC.

## Key Insights
- 11 boolean features → state = integer index (0-2047) via binary encoding
- 3 actions (straight, right, left) → Q-table shape: (2048, 3)
- Epsilon-greedy exploration with decay
- Q-table is small enough to serialize as JSON for heatmap visualization

## Requirements
### Functional
- Epsilon-greedy action selection
- Q-value update via Bellman equation
- Epsilon decay per episode
- Save/load Q-table (numpy .npy)
- Get Q-values for current state (for visualization)

### Non-functional
- Train >1000 episodes/sec (tabular = instant lookup)
- Q-table serializable to JSON

## Architecture
```python
class QLearningAgent:
    def __init__(self, state_size=2048, action_size=3,
                 lr=0.1, gamma=0.9, epsilon=1.0,
                 epsilon_min=0.01, epsilon_decay=0.995)

    def state_to_index(self, state: tuple) -> int    # Binary encode 11 bools
    def get_action(self, state: tuple) -> int         # Epsilon-greedy
    def update(self, state, action, reward, next_state, done)  # Q-update
    def decay_epsilon(self)                           # Call after each episode
    def get_q_values(self, state: tuple) -> list      # For heatmap viz
    def save(self, path: str)                         # numpy save
    def load(self, path: str)                         # numpy load
```

### Q-Learning Update Rule
```
Q(s,a) ← Q(s,a) + lr * [reward + gamma * max(Q(s',a')) - Q(s,a)]
if done: target = reward (no future value)
```

### Epsilon Decay Strategy
- Start: 1.0 (full random)
- Decay: multiply by 0.995 after each episode
- Min: 0.01 (always some exploration)
- ~920 episodes to reach min

## Related Code Files
**Create:**
- `backend/q_learning.py` — QLearningAgent class

## Implementation Steps
1. Implement `__init__`: initialize Q-table as numpy zeros (2048, 3), store hyperparams
2. Implement `state_to_index(state)`: convert tuple of 11 bools to int (binary encoding)
3. Implement `get_action(state)`:
   - Random float < epsilon → random action
   - Else → argmax of Q-values for state
4. Implement `update(state, action, reward, next_state, done)`:
   - Convert states to indices
   - Calculate target: reward + gamma * max(Q[next]) if not done, else reward
   - Update: Q[s][a] += lr * (target - Q[s][a])
5. Implement `decay_epsilon()`: epsilon = max(epsilon_min, epsilon * epsilon_decay)
6. Implement `get_q_values(state)`: return Q[state_index].tolist()
7. Implement `save/load`: numpy save/load Q-table + metadata dict
8. Test: verify Q-table updates correctly with manual state transitions

## Todo
- [x] QLearningAgent.__init__ with Q-table
- [x] state_to_index() binary encoding
- [x] get_action() epsilon-greedy
- [x] update() Bellman equation
- [x] decay_epsilon()
- [x] get_q_values() for visualization
- [x] save/load Q-table
- [x] Unit test: manual Q-update verification

## Success Criteria
- state_to_index maps all 2048 states uniquely
- Q-values update correctly per Bellman equation
- Epsilon decays from 1.0 → 0.01 over ~920 episodes
- Save/load preserves Q-table exactly

## Risk Assessment
- Binary encoding bug → wrong state mapping. Mitigation: test all edge cases
- Low risk overall — tabular Q-learning is well-understood

## Next Steps
→ Phase 04: Training Pipeline
