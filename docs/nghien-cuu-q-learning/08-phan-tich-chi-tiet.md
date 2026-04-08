# 8. Phan Tich Chi Tiet Thuat Toan

[← Luong Du Lieu Realtime](07-luong-du-lieu-realtime.md) | [Tiep: Ket Qua Va Nhan Xet →](09-ket-qua-nhan-xet.md)

---

## 8.1 Qua Trinh Hoc Cua AI Qua Cac Giai Doan

```
+==================================================================+
|  GIAI DOAN 1: KHAM PHA (Episode 1-200, epsilon ≈ 1.0 → 0.37)    |
+==================================================================+
|                                                                    |
|  Ran di NGAU NHIEN, chet lien tuc                                 |
|                                                                    |
|  ┌─────────────────┐    Score: 0-1                                |
|  │  →→→→↓          │    Reward: am lien tuc                       |
|  │      ↓          │    Q-Table: dang cap nhat tu tu               |
|  │      →→→→X      │    X = va tuong/than                         |
|  │                  │                                              |
|  └─────────────────┘    Ran chua "hieu" gi ca                     |
|                                                                    |
+==================================================================+
|  GIAI DOAN 2: HOC CO BAN (Episode 200-500, epsilon ≈ 0.37→0.08)  |
+==================================================================+
|                                                                    |
|  Ran bat dau TRANH TUONG, di ve phia thuc an                      |
|                                                                    |
|  ┌─────────────────┐    Score: 2-5                                |
|  │         F       │    Ran biet:                                  |
|  │         ↑       │    - Va tuong = xau (Q am)                    |
|  │    →→→→→↑       │    - Di gan thuc an = tot (Q duong)           |
|  │                  │    - Nhung van chet vi dam than               |
|  └─────────────────┘                                              |
|                                                                    |
+==================================================================+
|  GIAI DOAN 3: TINH CHINH (Episode 500-1000, epsilon ≈ 0.08→0.01) |
+==================================================================+
|                                                                    |
|  Ran di THONG MINH hon, tranh ca than minh                        |
|                                                                    |
|  ┌─────────────────┐    Score: 5-10+                              |
|  │  →→→↓    F      │    Ran biet:                                  |
|  │      ↓   ↑      │    - Luon cho path den thuc an                |
|  │      →→→→↑      │    - Tranh tu cat duong minh                  |
|  │                  │    - Toi uu duong di                          |
|  └─────────────────┘                                              |
|                                                                    |
+==================================================================+
```

---

## 8.2 Tai Sao Dung 3 Hanh Dong Tuong Doi?

```
HANH DONG TUYET DOI (4):          HANH DONG TUONG DOI (3):
Len, Xuong, Trai, Phai            Di Thang, Re Phai, Re Trai

Van de: Ran dang di PHAI,          Uu diem:
khong the di TRAI (quay dau)       - Khong bao gio quay dau (tu dong)
→ 1 hanh dong vo nghia              - Chi 3 hanh dong → Q-Table nho hon
→ Ton khong gian Q-Table            - Agent hoc nhanh hon
                                     - 2048 × 3 = 6,144 (thay vi 8,192)
```

---

## 8.3 Van De "Di Vong Tron" Va Cach Giai

```
Van de: Ran co the di vong tron mai ma khong chet

    ┌─────────┐
    │  →→→↓   │
    │  ↑  ↓   │    Ran di vong tron vinh vien
    │  ↑←←←   │    Reward: +1, -1, +1, -1, ... (trung hoa)
    │         │    Khong bao gio ket thuc!
    └─────────┘

Giai phap: GIOI HAN BUOC DI

    max_steps = 100 × len(snake)

    Ran dai 3 o  → toi da 300 buoc khong an
    Ran dai 10 o → toi da 1000 buoc khong an
    
    Vuot qua → Phat -10 va ket thuc game
    
    → Ran buoc phai tim thuc an, khong duoc lang vang!
```

---

## 8.4 Distance Reward — "La Ban" Cho Ran

```
Khong co distance reward:           Co distance reward:

Ran chi biet:                       Ran biet TUNG BUOC:
- An thuc an = +10 (hiem khi xay ra) - Di gan = +1 (thuong lien tuc)
- Chet = -10                          - Di xa = -1 (phat lien tuc)

→ Rat kho hoc vi reward "thua"       → Hoc nhanh vi co "la ban"
  (sparse reward problem)               huong dan moi buoc

Vi du:
  Thuc an o (15, 5), dau ran o (10, 10)
  Khoang cach cu: |10-15| + |10-5| = 10
  
  Ran di sang phai → (11, 10)
  Khoang cach moi: |11-15| + |10-5| = 9
  
  9 < 10 → Reward = +1 (tot lam, tiep tuc!)
```
