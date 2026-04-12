# Phase 04 — Benchmark Execution

## Context Links
- Plan: [plan.md](./plan.md)
- Prev: [phase-03-benchmark-preparation.md](./phase-03-benchmark-preparation.md)

## Overview
- **Date**: 2026-04-21 → 2026-04-22
- **Priority**: P1
- **Status**: pending
- **Review**: giữa Week 2
- **Description**: Build graph cho 3 repos, chạy baseline vs graphify runner trên 15 tasks, thu metrics đầy đủ.

## Key Insights
- Semantic pass (LLM re-rank node names) có thể đắt token → disable default, chỉ bật khi test isolated.
- Cache aggressive: build 1 lần, reuse cache cho tất cả tasks trên cùng repo.
- Phải chạy mỗi task 3 lần (n=3) để giảm variance.

## Requirements
**Functional**
- 3 graphs built + cache verified.
- 15 tasks × 2 modes × 3 runs = 90 result files.
- Metrics: `tokens_in`, `tokens_out`, `tool_calls`, `duration_s`, `correct` (bool), `compression_ratio`.
**Non-functional**
- Total budget < $50 API cost (ước tính).
- Resume nếu fail giữa chừng.

## Architecture
```
Graph build phase (once/repo):
  graphify build <repo> → ~/.graphify/cache/<hash>/

Execution matrix (per task):
  for mode in [baseline, graphify]:
    for run in [1,2,3]:
      run task → bench/results/<mode>-<repo>-<task>-run<n>.json
```

## Related Code Files
**Đọc**
- `graphifyy/cache.py` (verify cache hit)
- `graphifyy/serve.py` (MCP endpoint)

**Tạo/Update**
- `bench/run-all.py` (orchestrator, chạy full matrix, resumable)
- `bench/results/` (90+ files)
- `bench/build-log.md` (build time, cache size per repo)

## Implementation Steps
1. `graphify build` cho từng repo — ghi duration + cache size vào `build-log.md`.
2. Verify `graphify query` cache hit (build lần 2 phải gần instant).
3. Start `graphify serve` background process với cache pre-built.
4. Implement `bench/run-all.py` với resume logic (skip nếu file result tồn tại).
5. Chạy baseline matrix trước (15 tasks × 3 runs × 3 repos = 135 runs). Có thể chạy tuần tự để tránh rate limit.
6. Chạy graphify matrix (cùng ma trận). Log MCP tool call sequences.
7. Manual label `correct=true/false` dựa trên ground_truth (hoặc auto-eval script so sánh keyword).
8. Disable semantic pass test: chạy 5 tasks random với `--semantic` để đo extra cost.
9. Aggregate raw metrics vào `bench/results/summary.csv`.
10. Commit tất cả results (không gitignore — reproducibility).

## Todo
- [ ] Build graph cho 3 repos + ghi build-log
- [ ] Verify cache hit rate
- [ ] Implement `bench/run-all.py` resumable
- [ ] Chạy baseline 135 runs
- [ ] Chạy graphify 135 runs
- [ ] Label correctness (manual hoặc auto)
- [ ] Đo semantic-pass overhead (5 tasks)
- [ ] Aggregate `summary.csv`

## Success Criteria
- Tất cả 270 runs có file JSON output.
- Build time < 2 phút cho repo large (Supabase hoặc fallback).
- Cache hit rate > 95% ở run thứ 2+.
- Có data để so sánh tokens baseline vs graphify.

## Risk Assessment
| Risk | Mitigation |
|------|-----------|
| API rate limit | Sleep 2s giữa calls, retry exp backoff |
| Cost vượt ngân sách | Monitor sau mỗi 20 runs, kill nếu > $40 |
| MCP server crash | Supervisor script restart + resume |
| Semantic pass token blowup | Default OFF; isolated test thôi |
| Correctness judge bias | Ground truth rõ ràng trong `tasks.json`; 2-people review subset |

## Security Considerations
- API key qua env, rotate sau phase nếu leak suspected.
- Không log full prompt chứa source code của private repo (Supabase public OK).

## Next Steps
→ Phase 05: analysis + charts + report tiếng Việt.
