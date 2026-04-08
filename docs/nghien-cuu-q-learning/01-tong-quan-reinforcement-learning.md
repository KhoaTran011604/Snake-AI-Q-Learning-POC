# 1. Tong Quan Ve Reinforcement Learning

[← Muc luc](00-muc-luc.md) | [Tiep: Q-Learning La Gi? →](02-q-learning-la-gi.md)

---

## Reinforcement Learning (RL) la gi?

Reinforcement Learning (Hoc Tang Cuong) la mot nhanh cua Machine Learning, noi **agent** (tac nhan) hoc cach hanh dong trong **moi truong** (environment) bang cach **thu va sai**, nhan **phan thuong** (reward) hoac **hinh phat** (penalty) sau moi hanh dong.

```
+------------------+     hanh dong (action)     +------------------+
|                  | =========================> |                  |
|      AGENT       |                            |   MOI TRUONG     |
|   (Bo nao AI)    | <========================= |   (Game Snake)   |
|                  |  trang thai + phan thuong   |                  |
+------------------+                            +------------------+
```

## So sanh voi cac phuong phap ML khac

```
+------------------------+--------------------------------------------------+
| Phuong phap            | Dac diem                                         |
+------------------------+--------------------------------------------------+
| Supervised Learning    | Hoc tu du lieu co nhan (label)                   |
|                        | VD: Phan loai hinh anh cho/meo                  |
+------------------------+--------------------------------------------------+
| Unsupervised Learning  | Hoc tu du lieu khong nhan                        |
|                        | VD: Phan nhom khach hang                         |
+------------------------+--------------------------------------------------+
| Reinforcement Learning | Hoc tu phan thuong khi tuong tac voi moi truong  |
|                        | VD: AI choi game, robot di chuyen                |
+------------------------+--------------------------------------------------+
```

## Tai sao chon RL cho game Snake?

- Con ran **khong co du lieu huan luyen** san → khong the dung Supervised Learning
- Moi truong game **co phan hoi ro rang**: an thuc an = tot, dam tuong = xau
- Agent phai tu **kham pha** chien luoc toi uu → RL la lua chon tu nhien
