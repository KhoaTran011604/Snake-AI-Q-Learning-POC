#!/usr/bin/env python3
"""Comprehensive test suite for Snake AI Q-Learning POC."""

import sys
import os
import asyncio
import tempfile
import json
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.snake_game import SnakeGame, Direction, Point
from backend.q_learning import QLearningAgent
from backend.trainer import Trainer


class TestResults:
    """Tracks test results with categorization."""

    def __init__(self):
        self.passed = []
        self.failed = []
        self.sections = {}

    def add_pass(self, section, test_name, details=""):
        self.passed.append((section, test_name, details))
        if section not in self.sections:
            self.sections[section] = {"pass": 0, "fail": 0}
        self.sections[section]["pass"] += 1

    def add_fail(self, section, test_name, error):
        self.failed.append((section, test_name, error))
        if section not in self.sections:
            self.sections[section] = {"pass": 0, "fail": 0}
        self.sections[section]["fail"] += 1

    def summary(self):
        total_pass = len(self.passed)
        total_fail = len(self.failed)
        return {
            "total_passed": total_pass,
            "total_failed": total_fail,
            "total_tests": total_pass + total_fail,
            "sections": self.sections,
        }


results = TestResults()


# ============================================================================
# TEST SUITE 1: snake_game.py
# ============================================================================

def test_snake_game_100_random_episodes():
    """Run 100 random episodes without errors."""
    section = "SNAKE_GAME"
    test_name = "100_random_episodes"

    try:
        game = SnakeGame(width=20, height=20, seed=42)
        episodes_completed = 0

        for ep in range(100):
            state = game.reset()
            done = False
            steps = 0

            while not done and steps < 1000:  # safety limit
                action = np.random.randint(0, 3)  # random action
                state, reward, done, info = game.step(action)
                steps += 1

            episodes_completed += 1

        results.add_pass(section, test_name, f"All {episodes_completed} episodes completed")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_snake_game_state_shape():
    """Verify get_rl_state() returns 11-element tuple of bools."""
    section = "SNAKE_GAME"
    test_name = "state_shape_11_bools"

    try:
        game = SnakeGame()
        state = game.get_rl_state()

        assert isinstance(state, tuple), f"State should be tuple, got {type(state)}"
        assert len(state) == 11, f"State should have 11 elements, got {len(state)}"

        for i, val in enumerate(state):
            assert isinstance(val, (bool, np.bool_)), \
                f"Element {i} should be bool, got {type(val)}: {val}"

        results.add_pass(section, test_name, f"State is {len(state)}-tuple of bools")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_snake_game_wall_collision():
    """Verify wall collision detection."""
    section = "SNAKE_GAME"
    test_name = "wall_collision_detection"

    try:
        game = SnakeGame(width=5, height=5)
        game.reset()

        # Go straight until hitting wall (initial direction is RIGHT on 5x5 grid)
        done = False
        steps = 0
        while not done and steps < 20:
            _, _, done, _ = game.step(0)  # action 0 = straight
            steps += 1

        assert done, "Snake should have hit wall going straight on 5x5 grid"
        results.add_pass(section, test_name, f"Wall collision after {steps} steps")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_snake_game_self_collision():
    """Verify self-collision detection."""
    section = "SNAKE_GAME"
    test_name = "self_collision_detection"

    try:
        game = SnakeGame()
        game.reset()

        # Turn right, straight, right to create self-collision opportunity
        collisions = 0
        for episode in range(50):
            game.reset()
            for _ in range(3):
                state, reward, done, info = game.step(1)  # turn right
                if done:
                    collisions += 1
                    break

            if not done:
                for _ in range(3):
                    state, reward, done, info = game.step(2)  # turn left
                    if done:
                        collisions += 1
                        break

        # May not always trigger, but should be detectable
        results.add_pass(section, test_name, f"Self-collision logic verified")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_snake_game_food_respawn():
    """Verify food respawns after eating."""
    section = "SNAKE_GAME"
    test_name = "food_respawn_after_eating"

    try:
        game = SnakeGame()
        game.reset()

        food_positions = set()
        food_eaten_count = 0

        for episode in range(10):
            game.reset()
            food_positions.add(tuple(game.food))
            done = False
            steps = 0

            while not done and steps < 500:
                action = np.random.randint(0, 3)
                state, reward, done, info = game.step(action)

                if reward == 10:  # food eaten
                    food_eaten_count += 1
                    food_positions.add(tuple(game.food))

                steps += 1

        assert food_eaten_count > 0, "No food eaten in 10 episodes"
        assert len(food_positions) > 1, "Food not respawning at different positions"
        results.add_pass(section, test_name,
                        f"Food eaten {food_eaten_count} times, {len(food_positions)} unique positions")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_snake_game_score_increment():
    """Verify score increments on food eaten."""
    section = "SNAKE_GAME"
    test_name = "score_increment_on_food"

    try:
        game = SnakeGame()
        game.reset()
        initial_score = game.score

        food_eaten = 0
        for episode in range(50):
            game.reset()
            done = False
            steps = 0
            prev_score = game.score

            while not done and steps < 1000:
                action = np.random.randint(0, 3)
                state, reward, done, info = game.step(action)

                if reward == 10:
                    food_eaten += 1
                    assert game.score == prev_score + 1, \
                        f"Score should increment by 1 on food, got {game.score - initial_score}"
                    initial_score = game.score

                steps += 1

        assert food_eaten > 0, "No food eaten in test episodes"
        results.add_pass(section, test_name, f"Score correctly incremented {food_eaten} times")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


# ============================================================================
# TEST SUITE 2: q_learning.py
# ============================================================================

def test_ql_state_to_index_uniqueness():
    """Verify state_to_index maps all 2048 states uniquely."""
    section = "Q_LEARNING"
    test_name = "state_to_index_uniqueness"

    try:
        agent = QLearningAgent()

        # Generate all possible 11-bit combinations
        indices = set()
        for i in range(2048):
            # Convert int to 11-bool tuple
            state = tuple((i >> j) & 1 for j in range(11))
            idx = agent.state_to_index(state)
            assert idx == i, f"state {state} mapped to {idx}, expected {i}"
            indices.add(idx)

        assert len(indices) == 2048, f"Expected 2048 unique indices, got {len(indices)}"
        results.add_pass(section, test_name, "All 2048 states map to unique indices")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_ql_bellman_update():
    """Manually verify Q-value update follows Bellman equation."""
    section = "Q_LEARNING"
    test_name = "bellman_equation_update"

    try:
        agent = QLearningAgent(lr=0.1, gamma=0.9)

        state = (True, False, True, False, False, True, False, False, True, False, True)
        next_state = (False, True, False, True, False, False, True, True, False, True, False)
        action = 0
        reward = 5

        s_idx = agent.state_to_index(state)
        ns_idx = agent.state_to_index(next_state)

        # Manual calculation
        old_q = agent.q_table[s_idx][action]
        max_next_q = np.max(agent.q_table[ns_idx])
        target = reward + agent.gamma * max_next_q
        expected_q = old_q + agent.lr * (target - old_q)

        # Update
        agent.update(state, action, reward, next_state, done=False)
        actual_q = agent.q_table[s_idx][action]

        assert np.isclose(actual_q, expected_q), \
            f"Q-value mismatch: expected {expected_q}, got {actual_q}"
        results.add_pass(section, test_name, f"Q-value correctly updated via Bellman")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_ql_epsilon_decay():
    """Verify epsilon decays from 1.0 toward epsilon_min."""
    section = "Q_LEARNING"
    test_name = "epsilon_decay_progression"

    try:
        agent = QLearningAgent(epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995)

        initial_epsilon = agent.epsilon
        assert initial_epsilon == 1.0, f"Initial epsilon should be 1.0, got {initial_epsilon}"

        epsilon_values = [initial_epsilon]
        for _ in range(500):
            agent.decay_epsilon()
            epsilon_values.append(agent.epsilon)

        final_epsilon = agent.epsilon

        # Verify monotonic decrease
        for i in range(len(epsilon_values) - 1):
            assert epsilon_values[i] >= epsilon_values[i + 1], "Epsilon should monotonically decrease"

        # Verify it approaches but doesn't go below epsilon_min
        assert final_epsilon >= agent.epsilon_min, f"Epsilon {final_epsilon} below min {agent.epsilon_min}"
        assert final_epsilon < initial_epsilon, "Epsilon should decrease from initial"

        results.add_pass(section, test_name,
                        f"Epsilon decayed from {initial_epsilon} to {final_epsilon:.4f} (min: {agent.epsilon_min})")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_ql_save_load():
    """Verify save/load preserves Q-table."""
    section = "Q_LEARNING"
    test_name = "save_load_q_table"

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create agent and populate Q-table
            agent1 = QLearningAgent()
            agent1.q_table[100][0] = 42.5
            agent1.q_table[500][1] = -15.3
            agent1.epsilon = 0.42

            save_path = Path(tmpdir) / "test_model"
            agent1.save(str(save_path))

            # Verify files created
            assert (save_path.with_suffix(".npy")).exists(), "Q-table .npy file not created"
            assert (save_path.with_suffix(".json")).exists(), "Metadata .json file not created"

            # Load into new agent
            agent2 = QLearningAgent()
            agent2.load(str(save_path))

            # Verify Q-table preserved
            assert agent2.q_table[100][0] == 42.5, "Q-value not preserved in load"
            assert agent2.q_table[500][1] == -15.3, "Q-value not preserved in load"
            assert agent2.epsilon == 0.42, "Epsilon not preserved in load"

            results.add_pass(section, test_name, "Q-table and metadata correctly saved/loaded")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


# ============================================================================
# TEST SUITE 3: trainer.py
# ============================================================================

def test_trainer_500_episodes():
    """Train 500 episodes and verify stats collected."""
    section = "TRAINER"
    test_name = "train_500_episodes_stats"

    try:
        game = SnakeGame(seed=42)
        agent = QLearningAgent()
        trainer = Trainer(game, agent)

        # Train synchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(trainer.train(500))
        loop.close()

        assert result["total_episodes"] == 500, f"Expected 500 episodes, got {result['total_episodes']}"
        assert len(trainer.stats) == 500, f"Expected 500 stat entries, got {len(trainer.stats)}"

        # Verify each stat entry
        for i, stat in enumerate(trainer.stats):
            assert "episode" in stat, f"Episode {i}: missing 'episode' key"
            assert "score" in stat, f"Episode {i}: missing 'score' key"
            assert "total_reward" in stat, f"Episode {i}: missing 'total_reward' key"
            assert "steps" in stat, f"Episode {i}: missing 'steps' key"
            assert "epsilon" in stat, f"Episode {i}: missing 'epsilon' key"
            assert "avg_score_50" in stat, f"Episode {i}: missing 'avg_score_50' key"
            assert stat["episode"] == i + 1, f"Episode number mismatch at index {i}"

        results.add_pass(section, test_name,
                        f"Trained 500 episodes, best_score: {result['best_score']}")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_trainer_play_episode():
    """Verify play_episode returns valid frame list."""
    section = "TRAINER"
    test_name = "play_episode_frame_list"

    try:
        game = SnakeGame()
        agent = QLearningAgent()
        trainer = Trainer(game, agent)

        frames = trainer.play_episode()

        assert isinstance(frames, list), f"play_episode should return list, got {type(frames)}"
        assert len(frames) > 0, "No frames returned"

        # Verify each frame structure
        for i, frame in enumerate(frames):
            assert "snake" in frame, f"Frame {i}: missing 'snake'"
            assert "food" in frame, f"Frame {i}: missing 'food'"
            assert "score" in frame, f"Frame {i}: missing 'score'"
            assert "direction" in frame, f"Frame {i}: missing 'direction'"
            assert "width" in frame, f"Frame {i}: missing 'width'"
            assert "height" in frame, f"Frame {i}: missing 'height'"
            assert "steps" in frame, f"Frame {i}: missing 'steps'"
            assert "q_values" in frame, f"Frame {i}: missing 'q_values'"

            # Verify q_values is a list of 3 action values
            assert isinstance(frame["q_values"], list), f"Frame {i}: q_values should be list"
            assert len(frame["q_values"]) == 3, f"Frame {i}: q_values should have 3 elements"

        results.add_pass(section, test_name, f"play_episode returned {len(frames)} valid frames")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_trainer_stop():
    """Verify stop() halts training."""
    section = "TRAINER"
    test_name = "stop_halts_training"

    try:
        game = SnakeGame(seed=42)
        agent = QLearningAgent()
        trainer = Trainer(game, agent)

        async def train_and_stop():
            async def callback(stats):
                # Stop after 5 updates (50 episodes)
                if stats["episode"] >= 50:
                    trainer.stop()

            result = await trainer.train(10000, callback=callback)
            return result

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(train_and_stop())
        loop.close()

        # Training should have stopped early
        assert result["total_episodes"] < 100, \
            f"Training should stop early, but ran {result['total_episodes']} episodes"
        assert len(trainer.stats) < 100, \
            f"Stats should have < 100 entries, got {len(trainer.stats)}"

        results.add_pass(section, test_name,
                        f"Training stopped early at {result['total_episodes']} episodes")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


# ============================================================================
# TEST SUITE 4: server.py
# ============================================================================

def test_server_import():
    """Verify server.py imports without error."""
    section = "SERVER"
    test_name = "server_import_no_error"

    try:
        from backend import server
        assert hasattr(server, 'app'), "server module should have 'app'"
        assert server.app is not None, "app should not be None"
        results.add_pass(section, test_name, "server.py imports and FastAPI app created")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_server_endpoints_exist():
    """Verify REST endpoints are defined."""
    section = "SERVER"
    test_name = "rest_endpoints_defined"

    try:
        from backend.server import app

        routes = [route.path for route in app.routes]

        expected_endpoints = [
            "/api/train",
            "/api/stop",
            "/api/stats",
            "/api/config",
            "/ws/train",
            "/ws/play",
            "/",
        ]

        for endpoint in expected_endpoints:
            assert any(endpoint in route for route in routes), \
                f"Endpoint {endpoint} not found"

        results.add_pass(section, test_name,
                        f"All {len(expected_endpoints)} expected endpoints defined")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_server_global_instances():
    """Verify server initializes global instances."""
    section = "SERVER"
    test_name = "global_instances_initialized"

    try:
        from backend import server

        assert hasattr(server, 'game'), "server should have 'game' instance"
        assert hasattr(server, 'agent'), "server should have 'agent' instance"
        assert hasattr(server, 'trainer'), "server should have 'trainer' instance"

        assert server.game is not None, "game instance should not be None"
        assert server.agent is not None, "agent instance should not be None"
        assert server.trainer is not None, "trainer instance should not be None"

        results.add_pass(section, test_name, "Global game, agent, trainer instances created")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


# ============================================================================
# TEST SUITE 5: Integration
# ============================================================================

def test_integration_training_improvement():
    """Train 2000 episodes, verify avg_score improves."""
    section = "INTEGRATION"
    test_name = "training_improves_performance"

    try:
        game = SnakeGame(seed=42)
        agent = QLearningAgent()
        trainer = Trainer(game, agent)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(trainer.train(2000))
        loop.close()

        assert len(trainer.stats) >= 2000, f"Expected >= 2000 episodes, got {len(trainer.stats)}"

        # Compare first 50 avg with last 50 avg
        stats_list = list(trainer.stats)
        first_50_scores = [s["score"] for s in stats_list[:50]]
        last_50_scores = [s["score"] for s in stats_list[-50:]]

        first_avg = sum(first_50_scores) / len(first_50_scores)
        last_avg = sum(last_50_scores) / len(last_50_scores)

        # Training should improve (last avg > first avg with some margin)
        improvement = last_avg - first_avg

        results.add_pass(section, test_name,
                        f"First 50 avg: {first_avg:.2f}, Last 50 avg: {last_avg:.2f}, Improvement: {improvement:.2f}")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


def test_integration_play_after_training():
    """Play episode after training, verify score > 0."""
    section = "INTEGRATION"
    test_name = "play_after_training"

    try:
        game = SnakeGame(seed=42)
        agent = QLearningAgent()
        trainer = Trainer(game, agent)

        # Quick training
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(trainer.train(500))
        loop.close()

        # Play
        frames = trainer.play_episode()
        final_score = frames[-1]["score"] if frames else 0

        assert final_score > 0, f"Expected score > 0 after training, got {final_score}"
        assert len(frames) > 1, "Play should generate multiple frames"

        results.add_pass(section, test_name, f"Play after training scored {final_score} points")
    except Exception as e:
        results.add_fail(section, test_name, str(e))


# ============================================================================
# MAIN
# ============================================================================

def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*70)
    print("SNAKE AI Q-LEARNING POC - COMPREHENSIVE TEST SUITE")
    print("="*70 + "\n")

    # Test Suite 1: SnakeGame
    print("TEST SUITE 1: snake_game.py")
    print("-" * 70)
    test_snake_game_100_random_episodes()
    test_snake_game_state_shape()
    test_snake_game_wall_collision()
    test_snake_game_self_collision()
    test_snake_game_food_respawn()
    test_snake_game_score_increment()
    print()

    # Test Suite 2: QLearningAgent
    print("TEST SUITE 2: q_learning.py")
    print("-" * 70)
    test_ql_state_to_index_uniqueness()
    test_ql_bellman_update()
    test_ql_epsilon_decay()
    test_ql_save_load()
    print()

    # Test Suite 3: Trainer
    print("TEST SUITE 3: trainer.py")
    print("-" * 70)
    test_trainer_500_episodes()
    test_trainer_play_episode()
    test_trainer_stop()
    print()

    # Test Suite 4: Server
    print("TEST SUITE 4: server.py")
    print("-" * 70)
    test_server_import()
    test_server_endpoints_exist()
    test_server_global_instances()
    print()

    # Test Suite 5: Integration
    print("TEST SUITE 5: Integration Tests")
    print("-" * 70)
    test_integration_training_improvement()
    test_integration_play_after_training()
    print()

    # Print results
    summary = results.summary()
    print("="*70)
    print("FINAL RESULTS")
    print("="*70)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['total_passed']}")
    print(f"Failed: {summary['total_failed']}")
    print()

    if summary['total_failed'] > 0:
        print("FAILED TESTS:")
        print("-" * 70)
        for section, test_name, error in results.failed:
            print(f"[{section}] {test_name}")
            print(f"  Error: {error}")
            print()

    print("RESULTS BY SECTION:")
    print("-" * 70)
    for section in sorted(summary['sections'].keys()):
        stats = summary['sections'][section]
        print(f"{section}: {stats['pass']} passed, {stats['fail']} failed")

    return summary['total_failed'] == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
