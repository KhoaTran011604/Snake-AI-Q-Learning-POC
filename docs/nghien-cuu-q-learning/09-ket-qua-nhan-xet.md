# 9. Ket Qua Va Nhan Xet

[← Phan Tich Chi Tiet](08-phan-tich-chi-tiet.md) | [Tiep: Ket Luan →](10-ket-luan.md)

---

## Ket qua du kien sau huan luyen

```
+------------------+----------+----------+----------+
| Chi so           | 500 ep   | 1000 ep  | 3000 ep  |
+------------------+----------+----------+----------+
| Diem TB (50 ep)  | ~2-3     | ~4-6     | ~6-8     |
| Diem cao nhat    | ~5-7     | ~8-12    | ~12-15   |
| Epsilon          | ~0.08    | ~0.007   | ~0.0     |
| Thoi gian        | ~5 giay  | ~10 giay | ~30 giay |
+------------------+----------+----------+----------+
```

---

## Uu diem cua Q-Learning trong demo nay

```
+ Don gian, de hieu, de implement
+ Khong can GPU — chay tren CPU binh thuong
+ Hoi tu nhanh voi state space nho (2048 trang thai)
+ Minh bach — co the xem toan bo Q-Table
+ Phu hop cho muc dich giao duc va demo
```

---

## Han che

```
- Khong scale duoc voi state space lon
  (VD: Game co hinh anh → hang trieu trang thai → can Deep Q-Network)
- 11 dac trung la "hand-crafted" — con nguoi phai chon
  (Deep RL tu dong hoc dac trung tu pixel)
- Khong nho "lich su" — chi dua tren trang thai hien tai
  (Khong co "nho" ran da di qua dau)
```

---

## So sanh Q-Learning voi Deep Q-Network (DQN)

```
+--------------------+--------------------+--------------------+
|                    | Q-Learning         | Deep Q-Network     |
+--------------------+--------------------+--------------------+
| Luu tru Q-value    | Bang (table)       | Mang neural (NN)   |
| State input        | Dac trung thu cong | Pixel/raw data     |
| State space        | Nho (< 10K)        | Lon (vo han)       |
| Tinh minh bach     | Cao (doc bang)     | Thap (hop den)     |
| Tai nguyen         | CPU, < 1MB RAM     | GPU, hang GB RAM   |
| Do phuc tap code   | ~80 dong Python    | ~500+ dong Python  |
| Thoi gian huan luyen| Giay → Phut       | Phut → Gio         |
+--------------------+--------------------+--------------------+
```
