# Phase 03 — Benchmark Preparation

## Context Links
- Plan: [plan.md](./plan.md)
- Prev: [phase-02-dissect-core-source.md](./phase-02-dissect-core-source.md)
- Reference: graphify `benchmark.py` (harness có sẵn)

## Overview
- **Date**: 2026-04-19 → 2026-04-20
- **Priority**: P1
- **Status**: pending
- **Review**: đầu Week 2
- **Description**: Chọn 3 target repos, viết 15 realistic tasks, setup tiktoken counter, skeleton `baseline-runner.py` và `graphify-runner.py`.

## Key Insights
- Supabase monorepo là main target (~2000+ files TS/Py). Phải test build time trước; nếu >10 phút → fallback NestJS framework repo.
- Task phải realistic onboarding/debug: "tìm function X", "hàm nào gọi Y", "impact nếu đổi Z".
- Baseline = agent chỉ có `grep` + `read_file`. Graphify = agent có `query/path/explain` MCP tools.
- Token counter phải đồng nhất: tiktoken `cl100k_base` cho cả baseline và graphify runs.

## Requirements
**Functional**
- 3 repos pinned commit SHA: small (~50 files), medium (~500), large (~2000+).
- `bench/tasks.json`: 15 tasks với ground truth.
- Counter utility đo prompt + tool-call tokens.
- 2 runner skeletons callable CLI.
**Non-functional**
- Seed pinned (`random.seed`, `ANTHROPIC` temperature=0).
- Reproducible qua 1 command.

## Architecture
```
bench/
├── tasks.json            # [{id, repo, question, ground_truth, category}]
├── counter.py            # tiktoken wrapper
├── baseline-runner.py    # grep+read agent (Claude + basic tools)
├── graphify-runner.py    # graphify MCP agent
└── results/
    ├── baseline-{repo}-{task_id}.json
    └── graphify-{repo}-{task_id}.json
```

## Related Code Files
**Đọc**
- `graphifyy/benchmark.py` (xem pattern harness)
- `graphifyy/serve.py` (tool signatures để viết MCP client)

**Tạo**
- `bench/tasks.json`
- `bench/counter.py`
- `bench/baseline-runner.py` (skeleton)
- `bench/graphify-runner.py` (skeleton)
- `bench/README.md` (cách chạy)

## Implementation Steps
1. Chọn repos + pin SHA:
   - Small: `tj/commander.js` (~50 files) hoặc tương đương.
   - Medium: `vercel/next.js/examples/*` hoặc NestJS starter (~500).
   - Large: `supabase/supabase` (~2000+). Đo build time trước.
2. Clone vào `bench/repos/` (gitignored).
3. Viết 15 tasks (5/repo) phân category: find-function, callgraph, impact-analysis, onboarding-qna, refactor-scope. Ghi ground_truth.
4. Viết `counter.py` dùng tiktoken `cl100k_base`.
5. Viết `baseline-runner.py` skeleton: Anthropic SDK + tool `grep`, `read_file`, `list_dir`. Track tokens mỗi turn.
6. Viết `graphify-runner.py` skeleton: Anthropic SDK + MCP client tới `graphify serve`.
7. Unified output JSON schema: `{task_id, mode, tokens_in, tokens_out, tool_calls, answer, duration_s, correct}`.
8. Dry-run 1 task cả 2 runners → verify schema.
9. Đo build time Supabase. Nếu >10 phút → switch sang NestJS framework repo, update `tasks.json`.
10. Commit bench scaffold.

## Todo
- [ ] Chọn 3 repos + pin commit SHA
- [ ] Đo Supabase build time < 10 phút (không thì fallback NestJS)
- [ ] Viết `bench/tasks.json` 15 tasks
- [ ] Viết `bench/counter.py`
- [ ] Viết `bench/baseline-runner.py` skeleton
- [ ] Viết `bench/graphify-runner.py` skeleton
- [ ] Dry-run 1 task mỗi runner
- [ ] Document cách reproduce trong `bench/README.md`

## Success Criteria
- `python bench/baseline-runner.py --task T001` và `graphify-runner.py --task T001` đều chạy end-to-end.
- Output JSON validate theo schema.
- Supabase build time đo được < 2 phút (target) hoặc fallback ready.

## Risk Assessment
| Risk | Mitigation |
|------|-----------|
| Supabase quá lớn / build > 10 phút | Fallback NestJS framework repo, document lý do |
| tree-sitter TS coverage thiếu | Ghi chú trong `tasks.json`, tránh task đòi Rust/Swift |
| Benchmark bias (task ưu ái graphify) | Public tasks.json, ground_truth minh bạch, peer review nội bộ |
| Seed không reproducible | Pin temperature=0, `random.seed(42)`, version Anthropic SDK |

## Security Considerations
- `ANTHROPIC_API_KEY` qua `.env`, không commit.
- Cấm agent tools ghi ra filesystem ngoài `bench/results/`.

## Next Steps
→ Phase 04: execute runners, collect metrics.
