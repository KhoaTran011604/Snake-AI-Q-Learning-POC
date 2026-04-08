# 3. Cong Thuc Bellman — Trai Tim Cua Q-Learning

[← Q-Learning La Gi?](02-q-learning-la-gi.md) | [Tiep: Kien Truc He Thong →](04-kien-truc-he-thong.md)

---

## Cong thuc cap nhat Q-value

```
Q(s, a) ← Q(s, a) + α × [ r + γ × max Q(s', a') - Q(s, a) ]
                       ↑     ↑   ↑          ↑            ↑
                       |     |   |          |            |
                Learning  Reward Discount  Gia tri    Gia tri
                  Rate          Factor   tot nhat    hien tai
                 (α=0.1)       (γ=0.9) o buoc ke
```

## Giai thich tung thanh phan

| Ky hieu | Ten | Gia tri trong demo | Y nghia |
|---------|-----|-------------------|---------|
| `α` (alpha) | Learning Rate | 0.1 | Toc do hoc — qua lon se dao dong, qua nho se cham |
| `γ` (gamma) | Discount Factor | 0.9 | Muc quan tam den tuong lai — 0.9 = rat coi trong tuong lai |
| `r` | Reward | -10, -1, +1, +10 | Phan thuong tuc thoi |
| `s'` | Next State | — | Trang thai sau khi thuc hien hanh dong |
| `max Q(s', a')` | — | — | Gia tri Q tot nhat co the dat duoc o buoc ke |

## Code tuong ung trong du an

```python
# File: backend/q_learning.py, dong 43-53

def update(self, state, action, reward, next_state, done):
    """Q-value update via Bellman equation."""
    s_idx = self.state_to_index(state)
    ns_idx = self.state_to_index(next_state)

    if done:
        target = reward                                    # Ket thuc → chi co reward
    else:
        target = reward + self.gamma * np.max(self.q_table[ns_idx])  # Bellman!

    # Cap nhat Q-value
    self.q_table[s_idx][action] += self.lr * (target - self.q_table[s_idx][action])
```

## Minh hoa qua trinh cap nhat

```
Buoc 1: Ran dang o trang thai S, chon "Re Phai"
        Q(S, re_phai) = 0.0  (ban dau)

Buoc 2: Ran re phai, den gan thuc an hon → reward = +1
        Trang thai moi S' co max Q(S') = 2.0

Buoc 3: Cap nhat:
        target = 1 + 0.9 × 2.0 = 2.8
        Q(S, re_phai) = 0.0 + 0.1 × (2.8 - 0.0) = 0.28
                                                     ↑
                                            Q-value tang len!
                                    Ran "hoc" duoc re phai la tot

Buoc 4: Lan sau gap trang thai S, ran se co xu huong re phai
```
