# 5. Backend — Bo Nao AI

[← Kien Truc He Thong](04-kien-truc-he-thong.md) | [Tiep: Frontend — Giao Dien →](06-frontend-giao-dien.md)

---

## 5.1 Snake Game Engine (`snake_game.py`)

Game Snake duoc thiet ke dang **headless** (khong co giao dien) — chi xu ly logic, tra ve du lieu cho frontend ve.

### Khong gian trang thai (State Space)

Agent nhin the gioi qua **11 dac trung boolean** (True/False):

```
+------------------------------------------------------------------+
|                    11 DAC TRUNG CUA TRANG THAI                    |
+------------------------------------------------------------------+
|                                                                    |
|  NGUY HIEM (3 dac trung):            HUONG DI (4 dac trung):     |
|  +--------+--------+--------+        +---------+---------+        |
|  |Phia    |Ben     |Ben     |        |Trai|Phai|Len |Xuong|       |
|  |truoc?  |phai?   |trai?   |        +----+----+----+-----+       |
|  +--------+--------+--------+                                      |
|                                                                    |
|  VI TRI THUC AN (4 dac trung):                                    |
|  +--------+--------+--------+--------+                             |
|  |Ben     |Ben     |Phia    |Phia    |                             |
|  |trai?   |phai?   |tren?   |duoi?   |                             |
|  +--------+--------+--------+--------+                             |
|                                                                    |
|  Tong cong: 2^11 = 2048 trang thai kha thi                       |
+------------------------------------------------------------------+
```

### Tai sao chon 11 dac trung nay?

```
Vi du: Ran dang di sang PHAI, thuc an o phia TREN-PHAI

    +---+---+---+---+---+
    |   |   | F |   |   |     F = Thuc an (Food)
    +---+---+---+---+---+     H = Dau ran (Head)
    |   |   | X |   |   |     X = Nguy hiem (tuong)
    +---+---+---+---+---+     B = Than ran (Body)
    |   | B | H →   |   |     → = Huong di
    +---+---+---+---+---+
    |   | B |   |   |   |
    +---+---+---+---+---+

Trang thai RL:
  danger_straight = False  (phia truoc an toan)
  danger_right    = False  (ben phai an toan)  
  danger_left     = True   (ben trai co than ran!)
  dir_right       = True   (dang di sang phai)
  food_right      = False  
  food_up         = True   (thuc an phia tren)

→ State = (F, F, T, F, T, F, F, F, F, T, F) → Index = 532
```

### He thong phan thuong (Reward System)

```
+------------------------+---------+------------------------------------------+
| Tinh huong             | Reward  | Ly do                                    |
+------------------------+---------+------------------------------------------+
| An thuc an             |   +10   | Muc tieu chinh — khuyen khich manh       |
+------------------------+---------+------------------------------------------+
| Di gan thuc an hon     |    +1   | Khuyen khich di dung huong               |
+------------------------+---------+------------------------------------------+
| Di xa thuc an hon      |    -1   | Phat nhe khi di sai huong                |
+------------------------+---------+------------------------------------------+
| Va cham (tuong/than)   |   -10   | Phat nang — can tranh tuyet doi          |
+------------------------+---------+------------------------------------------+
| Qua lau khong an       |   -10   | Phat ran di vong tron vo nghia           |
+------------------------+---------+------------------------------------------+
```

```python
# File: backend/snake_game.py, dong 63-112

# Va cham → phat nang
if self._is_collision(new_head):
    return self.get_rl_state(), -10, True, {"score": self.score}

# An thuc an → thuong lon
if new_head == self.food:
    self.score += 1
    reward = 10
else:
    # Di gan/xa thuc an → thuong/phat nhe
    reward = 1 if new_dist < old_dist else -1

# Qua lau khong an → phat
if self.steps_since_food > 100 * len(self.snake):
    return self.get_rl_state(), -10, True, {"score": self.score}
```

---

## 5.2 Q-Learning Agent (`q_learning.py`)

### Cau truc Q-Table

```
Q-Table: Ma tran 2048 x 3
                                     
         Di Thang (0)  Re Phai (1)  Re Trai (2)
State 0  [  0.00    ,    0.00   ,    0.00   ]    ← Ban dau tat ca = 0
State 1  [  0.00    ,    0.00   ,    0.00   ]
State 2  [  0.00    ,    0.00   ,    0.00   ]
  ...          ...          ...         ...
State 532[  1.23    ,    3.45   ,   -0.67   ]    ← Sau khi hoc
  ...          ...          ...         ...
State 2047[ 0.00    ,    0.00   ,    0.00   ]

Tong: 2048 × 3 = 6,144 gia tri Q can hoc
```

### Chien luoc Epsilon-Greedy

Day la co che **can bang** giua **kham pha** (exploration) va **khai thac** (exploitation):

```
+------------------------------------------------------------------+
|                   EPSILON-GREEDY STRATEGY                         |
+------------------------------------------------------------------+
|                                                                    |
|  epsilon = 1.0 (ban dau)                                          |
|  ████████████████████████████████████████ 100% ngau nhien         |
|  Ran di loan, thu moi thu → KHAM PHA                              |
|                                                                    |
|  epsilon = 0.5 (giua qua trinh)                                   |
|  ████████████████████░░░░░░░░░░░░░░░░░░░ 50/50                   |
|  Nua kham pha, nua khai thac                                      |
|                                                                    |
|  epsilon = 0.01 (sau nhieu episode)                                |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1% ngau nhien           |
|  Gan nhu luon chon hanh dong tot nhat → KHAI THAC                 |
|                                                                    |
+------------------------------------------------------------------+
|                                                                    |
|  Cong thuc suy giam:                                               |
|  epsilon = max(0.01, epsilon × 0.995)                              |
|                                                                    |
|  → Sau 1000 episode: epsilon ≈ 0.007 (gan nhu chi khai thac)     |
|                                                                    |
+------------------------------------------------------------------+
```

```python
# File: backend/q_learning.py, dong 31-36

def get_action(self, state):
    """Epsilon-greedy action selection."""
    if np.random.random() < self.epsilon:     # Xac suat epsilon
        return np.random.randint(self.action_size)  # → Hanh dong ngau nhien
    idx = self.state_to_index(state)
    return int(np.argmax(self.q_table[idx]))  # → Hanh dong tot nhat
```

### Chuyen trang thai sang chi so (State Encoding)

```
State tuple:  (F, F, T, F, T, F, F, F, F, T, F)
Bit position:  0  1  2  3  4  5  6  7  8  9  10

Chi so = 0×2^0 + 0×2^1 + 1×2^2 + 0×2^3 + 1×2^4 + ... + 0×2^10
       = 4 + 16 + 512
       = 532

→ Tra Q-Table tai dong 532 de lay Q-values
```

```python
# File: backend/q_learning.py, dong 23-29

def state_to_index(self, state):
    """Convert tuple of 11 booleans to integer index (0-2047)."""
    idx = 0
    for i, val in enumerate(state):
        if val:
            idx |= (1 << i)    # Bitwise OR — rat nhanh!
    return idx
```

---

## 5.3 Vong Lap Huan Luyen (`trainer.py`)

```
+------------------------------------------------------------------+
|              VONG LAP HUAN LUYEN (1 EPISODE)                      |
+------------------------------------------------------------------+
|                                                                    |
|  1. Reset game → Trang thai ban dau S₀                            |
|     |                                                              |
|  2. ┌─── VONG LAP (cho den khi game over) ──────────────┐        |
|     │                                                     |        |
|     │  a. Agent chon hanh dong A (epsilon-greedy)        |        |
|     │     |                                               |        |
|     │  b. Game thuc thi A → nhan (S', R, done)           |        |
|     │     |                                               |        |
|     │  c. Agent cap nhat Q(S, A) theo Bellman            |        |
|     │     |                                               |        |
|     │  d. S ← S' (chuyen sang trang thai moi)           |        |
|     │     |                                               |        |
|     │  e. Neu done → thoat vong lap                      |        |
|     │                                                     |        |
|     └─────────────────────────────────────────────────────┘        |
|     |                                                              |
|  3. Giam epsilon (suy giam kham pha)                              |
|     |                                                              |
|  4. Ghi nhan thong ke (score, reward, steps)                      |
|     |                                                              |
|  5. Quay lai buoc 1 cho episode tiep theo                         |
|                                                                    |
+------------------------------------------------------------------+
```

```python
# File: backend/trainer.py, dong 22-49

def train_episode(self):
    state = self.game.reset()           # Buoc 1: Reset
    total_reward = 0
    done = False

    while not done:                     # Buoc 2: Vong lap
        action = self.agent.get_action(state)           # 2a
        next_state, reward, done, info = self.game.step(action)  # 2b
        self.agent.update(state, action, reward, next_state, done)  # 2c
        state = next_state              # 2d
        total_reward += reward

    self.agent.decay_epsilon()          # Buoc 3: Giam epsilon
    # Buoc 4: Ghi thong ke...
```
