"""Headless Snake game engine for Q-Learning training."""

import random
from enum import IntEnum
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


# Direction vectors: [RIGHT, DOWN, LEFT, UP]
DIR_VECTORS = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]


class SnakeGame:
    """Snake game with relative actions (straight/right/left) for RL training."""

    def __init__(self, width=20, height=20, seed=None):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        """Reset game to initial state. Returns RL state tuple."""
        cx, cy = self.width // 2, self.height // 2
        self.direction = Direction.RIGHT
        self.snake = [Point(cx, cy), Point(cx - 1, cy), Point(cx - 2, cy)]
        self.score = 0
        self.steps = 0
        self.steps_since_food = 0
        self.food = None
        self._place_food()
        return self.get_rl_state()

    def _place_food(self):
        """Place food on a random empty cell."""
        snake_set = set(self.snake)
        empty = [
            Point(x, y)
            for x in range(self.width)
            for y in range(self.height)
            if Point(x, y) not in snake_set
        ]
        self.food = self.rng.choice(empty) if empty else None

    def _is_collision(self, point):
        """Check if point collides with wall or snake body."""
        if point.x < 0 or point.x >= self.width:
            return True
        if point.y < 0 or point.y >= self.height:
            return True
        if point in self.snake[1:]:
            return True
        return False

    def step(self, action):
        """
        Execute one step with relative action.
        action: 0=straight, 1=turn right, 2=turn left
        Returns: (rl_state, reward, done, info)
        """
        self.steps += 1
        self.steps_since_food += 1

        # Convert relative action to absolute direction
        if action == 1:  # turn right
            self.direction = Direction((self.direction + 1) % 4)
        elif action == 2:  # turn left
            self.direction = Direction((self.direction - 1) % 4)

        # Move head
        dx, dy = DIR_VECTORS[self.direction]
        new_head = Point(self.snake[0].x + dx, self.snake[0].y + dy)

        # Check collision
        if self._is_collision(new_head):
            return self.get_rl_state(), -10, True, {"score": self.score}

        # No food left (snake filled the grid) — win
        if self.food is None:
            return self.get_rl_state(), 10, True, {"score": self.score}

        # Distance reward (before moving)
        old_dist = abs(self.snake[0].x - self.food.x) + abs(self.snake[0].y - self.food.y)
        new_dist = abs(new_head.x - self.food.x) + abs(new_head.y - self.food.y)

        # Move snake
        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.steps_since_food = 0
            self._place_food()
            reward = 10
        else:
            self.snake.pop()
            reward = 1 if new_dist < old_dist else -1

        # Too many steps without eating → die
        max_steps = 100 * len(self.snake)
        if self.steps_since_food > max_steps:
            return self.get_rl_state(), -10, True, {"score": self.score}

        return self.get_rl_state(), reward, False, {"score": self.score}

    def get_rl_state(self):
        """
        Return 11 boolean features as tuple for Q-table indexing.
        [danger_straight, danger_right, danger_left,
         dir_left, dir_right, dir_up, dir_down,
         food_left, food_right, food_up, food_down]
        """
        head = self.snake[0]
        d = self.direction

        # Direction vectors for straight, right, left
        straight = DIR_VECTORS[d]
        right_dir = DIR_VECTORS[(d + 1) % 4]
        left_dir = DIR_VECTORS[(d - 1) % 4]

        # Danger detection
        danger_s = self._is_collision(Point(head.x + straight.x, head.y + straight.y))
        danger_r = self._is_collision(Point(head.x + right_dir.x, head.y + right_dir.y))
        danger_l = self._is_collision(Point(head.x + left_dir.x, head.y + left_dir.y))

        return (
            danger_s, danger_r, danger_l,
            d == Direction.LEFT, d == Direction.RIGHT,
            d == Direction.UP, d == Direction.DOWN,
            self.food.x < head.x if self.food else False,  # food left
            self.food.x > head.x if self.food else False,  # food right
            self.food.y < head.y if self.food else False,  # food up
            self.food.y > head.y if self.food else False,  # food down
        )

    def get_state(self):
        """Return full game state dict for rendering."""
        return {
            "snake": [[p.x, p.y] for p in self.snake],
            "food": [self.food.x, self.food.y] if self.food else None,
            "score": self.score,
            "direction": self.direction.name.lower(),
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
        }
