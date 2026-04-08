# 4. Kien Truc He Thong Demo

[← Cong Thuc Bellman](03-cong-thuc-bellman.md) | [Tiep: Backend — Bo Nao AI →](05-backend-bo-nao-ai.md)

---

## Tong quan

```
+================================================================+
|                        BROWSER (Frontend)                       |
|                                                                 |
|  +-------------------+  +-------------------+  +--------------+ |
|  |   Game Canvas     |  | Training Chart    |  | Q-Heatmap    | |
|  |  (game-canvas.js) |  | (training-chart.js)|  | (q-heatmap.js)| |
|  |                   |  |                   |  |              | |
|  |  Ve ran, thuc an, |  | Bieu do diem TB   |  | Thanh mau    | |
|  |  luoi grid        |  | theo episode      |  | Q-value      | |
|  +-------------------+  +-------------------+  +--------------+ |
|                                                                 |
|  +------------------------------------------------------------+ |
|  |              controls.js — Dieu khien + WebSocket           | |
|  |  [Train] [Play] [Stop]  |  Episodes: [1000]  |  Speed: ═══ | |
|  +------------------------------------------------------------+ |
|                          |         ↑                            |
+==========================|=========|============================+
                           |         |
                    WebSocket /ws/train
                    WebSocket /ws/play
                           |         |
+==========================|=========|============================+
|                      SERVER (Backend)                           |
|                                                                 |
|  +------------------------------------------------------------+ |
|  |              server.py — FastAPI + WebSocket                | |
|  |                                                             | |
|  |  POST /api/train    → Bat dau huan luyen                   | |
|  |  POST /api/stop     → Dung huan luyen                      | |
|  |  GET  /api/stats    → Lay lich su huan luyen               | |
|  |  GET  /api/config   → Lay cau hinh game + agent            | |
|  |  WS   /ws/train     → Stream tien trinh huan luyen         | |
|  |  WS   /ws/play      → Stream khung hinh game               | |
|  +------------------------------------------------------------+ |
|                    |              |                              |
|       +------------+    +--------+--------+                     |
|       |                 |                 |                      |
|  +----v------+   +------v-----+   +-------v--------+           |
|  | trainer.py|   |q_learning.py|   | snake_game.py  |           |
|  |           |   |            |   |                |           |
|  | Vong lap  |   | Q-Table    |   | Logic game     |           |
|  | huan luyen|   | Bellman    |   | Va cham        |           |
|  | Thong ke  |   | Epsilon    |   | Thuc an        |           |
|  +-----------+   +------------+   | Trang thai RL  |           |
|                                   +----------------+           |
+================================================================+
```

## Luong giao tiep

```
Browser                    Server
  |                          |
  |--- WS Connect ---------->|
  |--- {episodes: 1000} ---->|  
  |                          |--- Bat dau vong lap huan luyen
  |                          |       |
  |                          |   Moi 10 episode:
  |<-- {train_update} -------|       |
  |    (score, epsilon,      |       |
  |     avg_score, episode)  |       |
  |                          |       |
  |   ... lap lai ...        |   ... lap lai ...
  |                          |       |
  |<-- {train_complete} -----|--- Hoan thanh
  |                          |
  |--- WS Connect /ws/play ->|
  |--- {speed_ms: 100} ----->|
  |                          |--- Chay 1 van choi (greedy)
  |<-- {play_frame} ---------|    Gui tung khung hinh
  |<-- {play_frame} ---------|
  |<-- ... ------------------|
  |<-- {play_complete} ------|
  |                          |
```
