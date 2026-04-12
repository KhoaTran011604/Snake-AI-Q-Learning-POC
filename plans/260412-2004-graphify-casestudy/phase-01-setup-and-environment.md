# Phase 01 — Setup & Environment

## Context Links
- Plan: [plan.md](./plan.md)
- Research: `plans/reports/research-260412-2004-graphify-poc.md`
- Upstream: https://github.com/safishamsi/graphify (PyPI: `graphifyy`)

## Overview
- **Date**: 2026-04-12 → 2026-04-13
- **Priority**: P1 (blocker cho mọi phase sau)
- **Status**: pending
- **Review**: cuối Week 1
- **Description**: Cài `graphifyy` trên Windows, xác nhận pipeline chạy được trên `tests/` fixtures của chính graphify, khởi tạo repo case study `graphify-casestudy-vn/`.

## Key Insights
- Graphify yêu cầu Python 3.10+, tree-sitter binding nhiều ngôn ngữ → Windows hay lỗi compile native.
- Có sẵn `tests/` fixtures nhỏ trong repo gốc — dùng làm smoke test trước khi thử repo thật.
- Phải pin version ngay từ đầu để reproducible.

## Requirements
**Functional**
- `graphify --version` chạy OK.
- `graphify build <fixture>` hoàn tất không error.
- `graphify query`, `graphify path`, `graphify explain` trả kết quả trên fixture.
**Non-functional**
- Reproducible qua `requirements.txt`.
- Env vars documented trong `README.md` stub.

## Architecture
```
Host OS (Windows 11)
  └── Python 3.11 venv (.venv/)
        └── graphifyy (pinned version)
              ├── tree-sitter grammars (bundled)
              └── CLI entrypoint `graphify`
Fallback: WSL2 Ubuntu 22.04 nếu tree-sitter build fail
```

## Related Code Files
**Đọc (upstream graphify)**
- `graphify/__main__.py` (CLI surface)
- `graphify/cache.py` (SHA256 cache dir layout)
- `tests/` fixtures

**Tạo (case study repo `graphify-casestudy-vn/`)**
- `README.md` (stub tiếng Việt)
- `requirements.txt` (pin `graphifyy==<x.y.z>`, `tiktoken`, `matplotlib`, `anthropic`)
- `.gitignore` (`.venv/`, `bench/results/`, `*.cast`)
- `docs/.gitkeep`, `bench/.gitkeep`, `demo/.gitkeep`, `reports/.gitkeep`

## Implementation Steps
1. Tạo folder `graphify-casestudy-vn/` tại workspace cha.
2. `git init`, set remote (private tạm thời).
3. Tạo `.venv` Python 3.11, activate.
4. `pip install graphifyy` → ghi version thực tế vào `requirements.txt`.
5. Clone upstream `safishamsi/graphify` tạm thời (read-only) vào `_upstream/` (gitignore).
6. Chạy `graphify build _upstream/tests/fixtures/<small>` — ghi log.
7. Nếu lỗi native build trên Windows → chuyển sang WSL2, lặp lại bước 3–6.
8. Verify cache tại `~/.graphify/cache/` (hoặc path equivalent).
9. Chạy `graphify query "function X"`, `graphify path A B`, `graphify explain <node>`.
10. Commit initial scaffold với message `chore: init case study scaffold`.

## Todo
- [ ] Tạo repo scaffold `graphify-casestudy-vn/`
- [ ] Python 3.11 venv + pin versions vào `requirements.txt`
- [ ] `pip install graphifyy` thành công
- [ ] Smoke test build fixture OK
- [ ] Test 3 CLI commands (query/path/explain)
- [ ] Document env setup trong `README.md` stub
- [ ] Ghi lại platform dùng (Windows hay WSL2) vào README

## Success Criteria
- `graphify build` trên fixture chạy < 30s, không error.
- 3 CLI subcommands trả về output hợp lệ.
- `requirements.txt` checked-in với versions cụ thể.

## Risk Assessment
| Risk | Mitigation |
|------|-----------|
| tree-sitter native build fail trên Windows | Fallback WSL2 Ubuntu 22.04, ghi rõ trong README |
| Version drift PyPI | Pin exact version ngay trong `requirements.txt` |
| Cache dir khác nhau Win/WSL | Document cả 2 paths |

## Security Considerations
- Không commit `.venv/`, `_upstream/`, API keys.
- `.env.example` chứa placeholder `ANTHROPIC_API_KEY=`.

## Next Steps
→ Phase 02: dissect source code để viết `docs/graphify-internals.md`.
