# Nghien Cuu Thuat Toan Q-Learning

## Ung Dung Trong Game Snake AI — Proof of Concept

> **Tai lieu nghien cuu noi bo** — Phan tich thuat toan Q-Learning thong qua demo Snake AI voi kien truc Frontend (UI) + Backend (AI Brain).

---

## Muc Luc

| # | Chuong | File |
|---|--------|------|
| 1 | [Tong Quan Ve Reinforcement Learning](01-tong-quan-reinforcement-learning.md) | Khai niem RL, so sanh voi ML khac |
| 2 | [Q-Learning La Gi?](02-q-learning-la-gi.md) | Dinh nghia, Q-Table, y nghia Q = Quality |
| 3 | [Cong Thuc Bellman](03-cong-thuc-bellman.md) | Trai tim cua Q-Learning, vi du so cu the |
| 4 | [Kien Truc He Thong Demo](04-kien-truc-he-thong.md) | So do tong quan Frontend ↔ Backend |
| 5 | [Backend — Bo Nao AI](05-backend-bo-nao-ai.md) | Game engine, Q-Agent, Trainer |
| 6 | [Frontend — Giao Dien Truc Quan](06-frontend-giao-dien.md) | Canvas, Chart, Heatmap, Controls |
| 7 | [Luong Du Lieu Realtime](07-luong-du-lieu-realtime.md) | WebSocket, sequence diagram Train/Play |
| 8 | [Phan Tich Chi Tiet Thuat Toan](08-phan-tich-chi-tiet.md) | 3 giai doan hoc, epsilon, distance reward |
| 9 | [Ket Qua Va Nhan Xet](09-ket-qua-nhan-xet.md) | Bang ket qua, uu/nhuoc diem, so sanh DQN |
| 10 | [Ket Luan](10-ket-luan.md) | Tom tat, kien truc phan tang, huong phat trien |

---

### Tech Stack

- **Backend**: Python, FastAPI, WebSocket, NumPy
- **Frontend**: Vanilla JS, Canvas 2D, Chart.js
- **RL**: Tabular Q-Learning (11 boolean features → 2048 states, 3 actions)
