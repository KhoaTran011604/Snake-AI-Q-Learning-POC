# 7. Luong Du Lieu Realtime

[← Frontend — Giao Dien](06-frontend-giao-dien.md) | [Tiep: Phan Tich Chi Tiet →](08-phan-tich-chi-tiet.md)

---

## WebSocket — Tai sao khong dung REST API?

```
REST API (HTTP):                    WebSocket:
                                    
Browser → Server: Cho toi data!     Browser ↔ Server: Ket noi lien tuc
Server → Browser: Day ne.           
Browser → Server: Cho toi data!     Server: Co data moi ne! (tu dong)
Server → Browser: Day ne.           Server: Lai co data moi!
Browser → Server: Cho toi data!     Server: Tiep tuc day!
...                                 ...

→ Ton kem, cham (polling)           → Nhe, nhanh (push)
                                    → Phu hop cho realtime updates
```

---

## Luong huan luyen qua WebSocket

```
Browser                              Server
   |                                    |
   |──── WS Connect /ws/train ────────>|
   |                                    |
   |──── {episodes: 3000} ───────────>|
   |                                    |
   |                              [Episode 1-10 chay]
   |<─── train_update ──────────────── |  {episode: 10, score: 1, 
   |     Cap nhat chart + status bar    |   avg_score_50: 0.3,
   |                                    |   epsilon: 0.95}
   |                              [Episode 11-20 chay]
   |<─── train_update ──────────────── |  {episode: 20, score: 2, ...}
   |                                    |
   |     ... (moi 10 episode 1 lan)    |
   |                                    |
   |                              [Episode 2990-3000 chay]
   |<─── train_update ──────────────── |  {episode: 3000, score: 8,
   |                                    |   avg_score_50: 5.2,
   |                                    |   epsilon: 0.01}
   |                                    |
   |<─── train_complete ─────────────── |  {total_episodes: 3000,
   |     Kich hoat nut Play             |   best_score: 12}
   |                                    |
```

---

## Luong choi game qua WebSocket

```
Browser                              Server
   |                                    |
   |──── WS Connect /ws/play ────────>|
   |──── {speed_ms: 100} ───────────>|
   |                                    |
   |                              [Frame 1: Ran bat dau]
   |<─── play_frame ─────────────────  |  {snake: [[10,10],[9,10],[8,10]],
   |     Ve len Canvas                  |   food: [15, 5],
   |     Cap nhat Q-Heatmap            |   q_values: [1.2, 3.4, -0.5],
   |                                    |   score: 0}
   |                                    |
   |     ... (100ms/frame)             |
   |                                    |
   |<─── play_frame ─────────────────  |  {snake: [[14,5],...],
   |     Ran an thuc an!                |   score: 5}
   |                                    |
   |     ... (tiep tuc)                |
   |                                    |
   |<─── play_complete ──────────────  |  {final_score: 8}
   |     Hien "Game over — Score: 8"   |
   |                                    |
```
