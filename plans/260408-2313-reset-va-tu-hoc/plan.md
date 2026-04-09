# Plan: Reset Brain + Auto-Improve After Each Play

## Tong Quan

Them 2 tinh nang:
1. **Nut Reset** — Xoa sach Q-Table, dua AI ve trang thai "ngu ngoc" ban dau
2. **Auto-Improve** — Sau moi lan Play, AI tu dong huan luyen them tu kinh nghiem thua de lan sau co ti le pha ky luc cao hon

## Phases

| Phase | Ten | Trang thai | File |
|-------|-----|------------|------|
| 1 | Reset Brain (Backend + Frontend) | Hoan thanh | [phase-01](phase-01-reset-brain.md) |
| 2 | Auto-Improve sau moi lan Play | Hoan thanh | [phase-02](phase-02-auto-improve.md) |

## Dependencies

- Phase 1: Doc lap, lam truoc
- Phase 2: Doc lap voi Phase 1, co the lam song song

## Rui ro

- Auto-improve qua nhieu episode se lam UI bi treo → gioi han so episode tu hoc
- Reset nham khi dang train → can disable nut khi dang training
