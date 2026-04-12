# Phase 05 — Benchmark Analysis & Report

## Context Links
- Plan: [plan.md](./plan.md)
- Prev: [phase-04-benchmark-execution.md](./phase-04-benchmark-execution.md)

## Overview
- **Date**: 2026-04-23 → 2026-04-24
- **Priority**: P1
- **Status**: pending
- **Review**: cuối Week 2
- **Description**: Phân tích `summary.csv`, vẽ charts matplotlib, viết `docs/benchmark-report.md` tiếng Việt.

## Key Insights
- Token reduction chính = skip reading raw source → chỉ cần node/edge metadata.
- Report phải minh bạch: nêu cả task graphify THUA baseline (nếu có).
- Cần confidence interval (n=3 runs) chứ không chỉ mean.

## Requirements
**Functional**
- Charts: bar tokens/task, box plot distribution, scatter correctness vs tokens, line build time vs repo size.
- Report có: executive summary, methodology, results, limitations, conclusions.
- Compression ratio tính: `tokens_baseline / tokens_graphify`.
**Non-functional**
- Report ≤ 800 dòng tiếng Việt.
- Charts export PNG 300dpi.

## Architecture
```
bench/results/summary.csv
  → bench/analyze.py (pandas + matplotlib)
    → bench/charts/*.png
    → docs/benchmark-report.md
```

## Related Code Files
**Tạo**
- `bench/analyze.py` (pandas aggregation + plotting)
- `bench/charts/tokens-per-task.png`
- `bench/charts/compression-ratio.png`
- `bench/charts/build-time.png`
- `bench/charts/correctness.png`
- `docs/benchmark-report.md`

## Implementation Steps
1. Load `summary.csv` vào pandas.
2. Tính mean/std cho mỗi (task, mode).
3. Tính `compression_ratio` per task, median per repo.
4. Vẽ 4 charts chính.
5. Identify outliers: task nào graphify thua baseline? Tại sao?
6. Viết `docs/benchmark-report.md` sections:
   - Tóm tắt kết quả (1 đoạn)
   - Phương pháp (repos, tasks, runners, seed)
   - Kết quả chính (bảng + charts)
   - Phân tích theo category task
   - Hạn chế (tree-sitter TS coverage, bias, sample size)
   - Kết luận + khi nào graphify worth-it
7. Cross-link charts PNG.
8. Peer review nội bộ (self-critique).

## Todo
- [ ] `bench/analyze.py` load + aggregate
- [ ] Compute compression ratio + CI
- [ ] Render 4 charts PNG
- [ ] Identify + explain outliers
- [ ] Viết `docs/benchmark-report.md` tiếng Việt
- [ ] Cross-check vs success metrics (≥5× medium, ≥10× large)

## Success Criteria
- Compression ratio medium ≥ 5× (median).
- Compression ratio large ≥ 10× (median).
- Report không lảng tránh case graphify thua.
- Tất cả charts reproducible: `python bench/analyze.py` regen.

## Risk Assessment
| Risk | Mitigation |
|------|-----------|
| Metrics không đạt target | Report trung thực + phân tích lý do (có thể do task category) |
| Sample size nhỏ (n=3) | Nêu rõ limitation, khuyến nghị n=10 cho future work |
| Matplotlib font VN lỗi | Dùng DejaVu Sans hoặc noto-sans |

## Security Considerations
- Không expose snippet source code private trong report.
- Nếu dùng Supabase (public OK), vẫn redact credentials trong output examples.

## Next Steps
→ Phase 06: onboarding demo với MCP server.
