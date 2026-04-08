"""Tabular Q-Learning agent for Snake game."""

import numpy as np
import json
from pathlib import Path


class QLearningAgent:
    """Q-Learning with epsilon-greedy exploration. Q-table indexed by 11-bool state."""

    def __init__(self, state_size=2048, action_size=3,
                 lr=0.1, gamma=0.9, epsilon=1.0,
                 epsilon_min=0.01, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_table = np.zeros((state_size, action_size))

    def state_to_index(self, state):
        """Convert tuple of 11 booleans to integer index (0-2047)."""
        idx = 0
        for i, val in enumerate(state):
            if val:
                idx |= (1 << i)
        return idx

    def get_action(self, state):
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_size)
        idx = self.state_to_index(state)
        return int(np.argmax(self.q_table[idx]))

    def get_best_action(self, state):
        """Greedy action (no exploration)."""
        idx = self.state_to_index(state)
        return int(np.argmax(self.q_table[idx]))

    def update(self, state, action, reward, next_state, done):
        """Q-value update via Bellman equation."""
        s_idx = self.state_to_index(state)
        ns_idx = self.state_to_index(next_state)

        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[ns_idx])

        self.q_table[s_idx][action] += self.lr * (target - self.q_table[s_idx][action])

    def decay_epsilon(self):
        """Decay epsilon after each episode."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def get_q_values(self, state):
        """Return Q-values for state as list (for visualization)."""
        idx = self.state_to_index(state)
        return self.q_table[idx].tolist()

    def save(self, path):
        """Save Q-table and metadata."""
        p = Path(path)
        np.save(p.with_suffix(".npy"), self.q_table)
        meta = {
            "lr": self.lr, "gamma": self.gamma,
            "epsilon": self.epsilon, "epsilon_min": self.epsilon_min,
            "epsilon_decay": self.epsilon_decay,
            "state_size": self.state_size, "action_size": self.action_size,
        }
        with open(p.with_suffix(".json"), "w") as f:
            json.dump(meta, f)

    def load(self, path):
        """Load Q-table and metadata."""
        p = Path(path)
        self.q_table = np.load(p.with_suffix(".npy"))
        with open(p.with_suffix(".json")) as f:
            meta = json.load(f)
        self.epsilon = meta["epsilon"]
