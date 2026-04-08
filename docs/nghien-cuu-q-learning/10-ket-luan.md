# 10. Ket Luan

[← Ket Qua Va Nhan Xet](09-ket-qua-nhan-xet.md) | [Muc luc](00-muc-luc.md)

---

## Tom tat

Q-Learning la thuat toan **Reinforcement Learning co ban nhat** nhung **cuc ky manh me** cho cac bai toan co **state space nho**. Demo Snake AI minh hoa toan bo qua trinh:

1. **Agent** (ran) tuong tac voi **Environment** (game) qua **Actions** (3 hanh dong tuong doi)
2. **Q-Table** luu tru "tri thuc" cua agent — cap nhat qua **cong thuc Bellman**
3. **Epsilon-Greedy** can bang giua kham pha va khai thac
4. **Frontend** truc quan hoa qua trinh hoc bang Canvas, Chart.js, va WebSocket realtime
5. **Backend** tach biet logic game, agent, va vong lap huan luyen — kien truc sach, de mo rong

---

## Kien truc phan tang

```
+------------------------------------------------------------------+
|                                                                    |
|    PRESENTATION        COMMUNICATION         LOGIC                 |
|    (Frontend)          (WebSocket)           (Backend)             |
|                                                                    |
|  +--------------+    +---------------+    +------------------+     |
|  | Canvas       |    | /ws/train     |    | snake_game.py    |     |
|  | Chart.js     |<-->| /ws/play      |<-->| q_learning.py    |     |
|  | Q-Heatmap    |    | JSON messages |    | trainer.py       |     |
|  | Controls     |    |               |    | server.py        |     |
|  +--------------+    +---------------+    +------------------+     |
|                                                                    |
|  "Mat" cua he thong   "Duong truyen"      "Bo nao" cua he thong  |
|                                                                    |
+------------------------------------------------------------------+
```

---

## Huong phat trien tiep theo

- **Deep Q-Network (DQN)**: Thay Q-Table bang Neural Network de xu ly state space lon hon
- **Double DQN**: Giam hien tuong overestimation cua Q-values
- **Prioritized Experience Replay**: Hoc tu nhung trai nghiem quan trong hon
- **Multi-agent**: Nhieu ran cung hoc trong 1 moi truong

---

> **Tac gia**: Tao boi AI dua tren phan tich ma nguon du an Snake AI Q-Learning POC
> **Ngay**: 08/04/2026
> **Phien ban**: 1.0
