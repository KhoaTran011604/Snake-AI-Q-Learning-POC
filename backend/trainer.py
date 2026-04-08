"""Training loop connecting SnakeGame + QLearningAgent with async support."""

import asyncio
from collections import deque

from backend.snake_game import SnakeGame
from backend.q_learning import QLearningAgent


class Trainer:
    """Manages training loop, tracks stats, supports pause/resume."""

    def __init__(self, game: SnakeGame, agent: QLearningAgent):
        self.game = game
        self.agent = agent
        self.stats = deque(maxlen=10000)
        self.best_score = 0
        self.recent_scores = deque(maxlen=50)
        self._stop_flag = False
        self._training = False

    def train_episode(self):
        """Run single training episode. Returns stats dict."""
        state = self.game.reset()
        total_reward = 0
        done = False

        while not done:
            action = self.agent.get_action(state)
            next_state, reward, done, info = self.game.step(action)
            self.agent.update(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

        self.agent.decay_epsilon()
        self.recent_scores.append(info["score"])

        ep_stats = {
            "episode": len(self.stats) + 1,
            "score": info["score"],
            "total_reward": total_reward,
            "steps": self.game.steps,
            "epsilon": round(self.agent.epsilon, 4),
            "avg_score_50": round(sum(self.recent_scores) / len(self.recent_scores), 2),
        }
        self.stats.append(ep_stats)
        if info["score"] > self.best_score:
            self.best_score = info["score"]
        return ep_stats

    async def train(self, num_episodes, callback=None):
        """Async training loop with optional callback every 10 episodes."""
        self._stop_flag = False
        self._training = True

        try:
            for i in range(num_episodes):
                if self._stop_flag:
                    break
                ep_stats = self.train_episode()

                # Callback every 10 episodes
                if callback and (i + 1) % 10 == 0:
                    await callback(ep_stats)

                # Yield control every 10 episodes
                if (i + 1) % 10 == 0:
                    await asyncio.sleep(0)
        finally:
            self._training = False

        return {
            "total_episodes": len(self.stats),
            "best_score": self.best_score,
        }

    def play_episode(self):
        """Play one episode with greedy policy. Returns list of frames."""
        state = self.game.reset()
        frames = []
        done = False

        while not done:
            q_values = self.agent.get_q_values(state)
            action = self.agent.get_best_action(state)
            game_state = self.game.get_state()
            game_state["q_values"] = q_values
            frames.append(game_state)
            state, _, done, _ = self.game.step(action)

        # Add final frame
        game_state = self.game.get_state()
        game_state["q_values"] = self.agent.get_q_values(state)
        frames.append(game_state)
        return frames

    def get_stats(self):
        """Return training history (last 10k episodes)."""
        return list(self.stats)

    def stop(self):
        """Stop training loop."""
        self._stop_flag = True

    def is_training(self):
        return self._training
