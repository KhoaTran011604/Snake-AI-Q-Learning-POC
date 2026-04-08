# 6. Frontend — Giao Dien Truc Quan

[← Backend — Bo Nao AI](05-backend-bo-nao-ai.md) | [Tiep: Luong Du Lieu Realtime →](07-luong-du-lieu-realtime.md)

---

## 6.1 Game Canvas (`game-canvas.js`)

Ve game Snake tren Canvas 2D voi cac hieu ung:

```
+------------------------------------------+
|  GAME CANVAS (400 x 400 pixel)           |
|                                          |
|  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐       |
|  │  │  │  │  │  │  │  │  │  │  │  20x20 |
|  ├──┼──┼──┼──┼──┼──┼──┼──╋━━╋──┤  grid  |
|  │  │  │  │  │  │  │  │  ┃⦿┃  │       |
|  ├──┼──┼──┼──┼──┼──┼──┼──╋━━╋──┤       |
|  │  │  │  │  │██│██│██│OO│  │  │       |
|  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤       |
|  │  │  │  │  │██│  │  │  │  │  │       |
|  │  │  │  │  │  │  │  │  │  │  │       |
|  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘       |
|                                          |
|  ⦿ = Thuc an (nhap nhay do)            |
|  OO = Dau ran (mat, gradient do)         |
|  ██ = Than ran (gradient do → xanh dam)  |
|                                          |
+------------------------------------------+
```

**Dac diem ky thuat:**
- **Luoi grid**: 20x20 o, moi o = 20x20 pixel
- **Thuc an**: Hieu ung pulsing (nhap nhay) bang ham `sin()`
- **Than ran**: Gradient mau tu dau (do `#e94560`) den duoi (xanh dam `#0f3460`)
- **Dau ran**: Co 2 mat trang de phan biet

---

## 6.2 Training Chart (`training-chart.js`)

Bieu do realtime hien thi **diem trung binh 50 episode gan nhat**:

```
Avg Score
    ^
  6 |                                          ╱──
    |                                     ╱───╱
  4 |                                ╱───╱
    |                          ╱────╱
  2 |                    ╱────╱
    |              ╱────╱
  1 |        ╱────╱
    |  ╱────╱
  0 +───────────────────────────────────────────→ Episode
    0    200    400    600    800    1000   1200

    [████████████████████░░░░░░░░░░] 60% Training...
```

**Su dung**: Chart.js voi `animation: false` de cap nhat muot khi nhan du lieu qua WebSocket.

---

## 6.3 Q-Value Heatmap (`q-heatmap.js`)

Hien thi **Q-value cua 3 hanh dong** tai moi khung hinh khi AI choi:

```
+--------------------------------------------------+
|  Q-Values (action preferences)                    |
|                                                    |
|  Straight  ████████████████░░░░░░░░░░░  +2.34    |
|  Turn Right ██████████████████████████░  +3.45    |  ← Tot nhat!
|  Turn Left  ████░░░░░░░░░░░░░░░░░░░░░  -0.67    |
|                                                    |
|  Xanh = Q cao (tot)     Do = Q thap (xau)        |
|  Hanh dong co Q cao nhat → duoc AI chon           |
+--------------------------------------------------+
```

---

## 6.4 Dieu Khien (`controls.js`)

```
+------------------------------------------------------------------+
|  Header Bar                                                       |
|                                                                    |
|  Snake AI — Q-Learning                                            |
|                                                                    |
|  Episodes: [1000]  [Train]  [Play]  [Stop]  Speed: ═══●════      |
|                                                                    |
+------------------------------------------------------------------+
|                                                                    |
|  Trang thai nut bam:                                               |
|                                                                    |
|  Khi READY:    [Train OK] [Play OK] [Stop --]                    |
|  Khi TRAINING: [Train --] [Play --] [Stop OK]                    |
|  Khi PLAYING:  [Train --] [Play --] [Stop --]                    |
|                                                                    |
+------------------------------------------------------------------+
```
