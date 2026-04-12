# Brainstorm Summary: Graphify Deep-Dive Case Study

**Date:** 2026-04-12 20:04 (ICT)
**Status:** Agreed — proceed to `/plan`
**Scope lock:** Focus 100% vào `safishamsi/graphify`, KHÔNG build tool đối thủ.

---

## Decisions Locked

| # | Quyết định |
|---|---|
| 1 | Focus: học core graphify + chứng minh token reduction + case study onboarding |
| 2 | Target repo case study: **monorepo TS+Py** (ưu tiên Supabase — có cả TS lẫn Py, mixed docs; fallback NestJS nếu quá lớn) |
| 3 | Ngôn ngữ docs/blog: **Tiếng Việt** |
| 4 | KHÔNG đóng góp PR ngược graphify |
| 5 | Progress report: **weekly summary .md** (3 files: w1, w2, w3) |

---

## Problem Statement

Muốn:
- Hiểu sâu core graphify (Python 3.10+, tree-sitter, NetworkX, Leiden, MCP serve).
- Chứng minh token reduction bằng số liệu reproducible.
- Case study thực tế: dùng graphify làm onboarding assistant cho monorepo lớn.
- Output tái sử dụng được cho dự án khác (pattern + workflow).

## Graphify Core (đã khảo sát)

**Package structure (29 files, ~713KB):**
- `extract.py` (117KB) — core tree-sitter extractors
- `__main__.py` (36KB) — CLI orchestrator
- `export.py` (39KB) — multi-format output
- `analyze.py` (21KB) — hub/anomaly/god-node detection
- `serve.py` (15KB) — MCP server
- `cache.py` (5KB) — SHA256 incremental
- `cluster.py` (5KB) — Leiden via graspologic
- `benchmark.py` (5KB) — **benchmark harness có sẵn ⭐**
- `skill-*.md` × 9 platforms — prompt specs
- `watch.py`/`hooks.py` — auto-sync

**Pipeline:** `detect → extract → build → cluster → analyze → report → export`. Stateless, giao tiếp qua dict + NetworkX.

**Edge confidence tiers:** `EXTRACTED` | `INFERRED` | `AMBIGUOUS`.

## 3-Week Roadmap

### Week 1 — Dissect Core
- Install `graphifyy` từ PyPI, run trên `tests/` fixtures
- Đọc + trace: `__main__.py`, `extract.py`, `cache.py`, `build.py`, `serve.py`
- Viết `docs/graphify-internals.md` (tiếng Việt): sequence diagram Mermaid, node/edge schema, extractor pattern per language
- Deliverable: `reports/week-1-summary.md`

### Week 2 — Benchmark Reproducible
- 3 repos: small (~50 files), medium (~500), large (Supabase ~2000+)
- 15 realistic tasks (find flow, trace caller, explain module…)
- Baseline: grep+read agent, đếm tokens tiktoken
- Graphify: `query` / `path` / `explain`, đếm tokens response
- Charts: token/task, compression ratio, build time, cache hit
- Deliverable: `bench/` scripts + `docs/benchmark-report.md` + `reports/week-2-summary.md`

### Week 3 — Onboarding Assistant Demo
- Index Supabase (monorepo TS+Py) với graphify
- MCP serve cho Claude Code
- 10 onboarding questions kịch bản ("auth flow?", "nơi thêm endpoint?", "webhook handler ở đâu?")
- So sánh answer quality với/không graphify
- Blog post tiếng Việt + demo video (asciinema)
- Deliverable: public repo `graphify-casestudy-vn` + `reports/week-3-summary.md`

## Success Metrics

- ✅ Token reduction đo được ≥ 5× (medium), ≥ 10× (large)
- ✅ Build time < 2 phút cho 2000+ files
- ✅ Onboarding: ≥ 9/10 câu trả lời đúng với graphify context
- ✅ Scripts reproducible (seed + env pinned)
- ✅ 3 weekly reports + 1 blog tiếng Việt + 1 video

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Graphify bug trên Windows | WSL2 fallback, document rõ |
| Benchmark nhỏ không thuyết phục | Repo lớn ≥ 2000 files cho case chính |
| Semantic pass tốn token Claude | Proxy đã có, cache aggressive, disable semantic pass khi không cần |
| tree-sitter TS coverage không đều | So sánh per-language trong report, ghi limit |
| Supabase quá lớn → build lâu | Fallback NestJS nếu > 10 phút build |

## Security / Privacy

- Repo public case study chỉ index OSS repos (Supabase, NestJS…).
- Không index code nội bộ.
- Graphify chạy local, MCP bind localhost.

## Output Structure

```
graphify-casestudy-vn/
├── README.md                          # VN, tổng hợp + how to reproduce
├── docs/
│   ├── graphify-internals.md         # W1 deep-dive
│   ├── benchmark-report.md           # W2 charts + tables
│   └── onboarding-demo.md            # W3 case study
├── bench/
│   ├── tasks.json                    # 15 tasks
│   ├── baseline-runner.py
│   ├── graphify-runner.py
│   └── results/
├── demo/
│   ├── supabase-index/               # gitignored artifact
│   ├── questions.md
│   └── asciinema.cast
├── reports/
│   ├── week-1-summary.md
│   ├── week-2-summary.md
│   └── week-3-summary.md
└── plans/
    └── 260412-2004-graphify-casestudy/
```

## Next Step

Chạy `/plan` để tạo plan chi tiết với 7 phases + TODO tasks + file structure đầy đủ.

## Unresolved Questions

1. Repo case study cuối: Supabase (monorepo lớn) hay NestJS (TS clean) nếu Supabase quá nặng? → quyết trong W2 sau khi đo build time.
2. Blog host: dev.to VN / viblo / own site? → quyết ở W3.
3. Video demo: asciinema (terminal) hay OBS screen record? → asciinema mặc định, thêm OBS nếu cần kể story.
