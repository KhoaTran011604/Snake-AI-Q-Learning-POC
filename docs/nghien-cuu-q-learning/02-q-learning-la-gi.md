# 2. Q-Learning La Gi?

[← Tong Quan RL](01-tong-quan-reinforcement-learning.md) | [Tiep: Cong Thuc Bellman →](03-cong-thuc-bellman.md)

---

## Dinh nghia

Q-Learning la mot thuat toan **model-free** (khong can mo hinh moi truong) thuoc nhom **Temporal Difference Learning**. No hoc mot ham gia tri **Q(s, a)** — uoc luong "muc do tot" khi thuc hien hanh dong `a` tai trang thai `s`.

## Y nghia cua chu "Q"

**Q = Quality** (Chat luong). `Q(s, a)` tra loi cau hoi: *"Neu toi dang o trang thai `s` va thuc hien hanh dong `a`, tong phan thuong tuong lai se la bao nhieu?"*

## Minh hoa truc quan

```
                         Q-Table (Bang gia tri Q)
                    +------------+------------+------------+
                    | Di Thang   | Re Phai    | Re Trai    |
    Trang thai      | (action 0) | (action 1) | (action 2) |
+-------------------+------------+------------+------------+
| Khong nguy hiem,  |            |            |            |
| thuc an o ben phai|    -0.5    |   +3.2     |   -1.1     |
+-------------------+------------+------------+------------+
| Nguy hiem phia    |            |            |            |
| truoc, thuc an    |    -8.0    |   +2.5     |   +1.8     |
| ben trai          |            |            |            |
+-------------------+------------+------------+------------+
| An toan moi phia, |            |            |            |
| thuc an phia tren |    +1.2    |   -0.3     |   +2.7     |
+-------------------+------------+------------+------------+
                              ↑
                    Gia tri cang CAO = hanh dong cang TOT
```

Agent chon hanh dong co **gia tri Q cao nhat** → day la **chinh sach toi uu** (optimal policy).
