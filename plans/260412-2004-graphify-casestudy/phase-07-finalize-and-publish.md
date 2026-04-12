# Phase 07 — Finalize & Publish

## Context Links
- Plan: [plan.md](./plan.md)
- Prev: [phase-06-onboarding-demo.md](./phase-06-onboarding-demo.md)

## Overview
- **Date**: 2026-04-29 → 2026-04-30
- **Priority**: P2
- **Status**: pending
- **Review**: cuối Week 3
- **Description**: Viết README tiếng Việt, 3 weekly summary reports, blog post, cleanup repo, public release.

## Key Insights
- Weekly summaries phải viết dần (không dồn cuối) — đã kế hoạch ghi cuối mỗi tuần.
- Blog post = condensation của `docs/benchmark-report.md` + `docs/onboarding-demo.md`.
- Attribution rõ ràng: credit safishamsi, license MIT, link upstream.

## Requirements
**Functional**
- `README.md` tiếng Việt đầy đủ: intro, install, reproduce, results highlight.
- 3 files `reports/week-{1,2,3}-summary.md`.
- 1 blog post `docs/blog-post-vn.md` (~1500 từ).
- Repo public, license MIT (tương thích upstream), attribution rõ.
**Non-functional**
- Không leak API keys / private data.
- Cleanup `_upstream/`, `.venv/`, large cache.

## Architecture
```
graphify-casestudy-vn/ (final)
├── README.md              (VN, hero + highlights)
├── LICENSE                (MIT)
├── requirements.txt
├── docs/
│   ├── graphify-internals.md
│   ├── benchmark-report.md
│   ├── onboarding-demo.md
│   └── blog-post-vn.md
├── bench/ (tasks, runners, results, charts)
├── demo/ (questions, transcripts, asciinema)
└── reports/week-{1,2,3}-summary.md
```

## Related Code Files
**Tạo/Update**
- `README.md` (tiếng Việt, include badges, quick-start, links to docs)
- `LICENSE` (MIT + attribution)
- `reports/week-1-summary.md` (retrospective Phase 1–2)
- `reports/week-2-summary.md` (Phase 3–5)
- `reports/week-3-summary.md` (Phase 6–7)
- `docs/blog-post-vn.md`
- `.gitignore` final review

## Implementation Steps
1. Viết `reports/week-1-summary.md`: setup, internals doc highlights, blockers.
2. Viết `reports/week-2-summary.md`: benchmark results TL;DR, compression ratios, surprises.
3. Viết `reports/week-3-summary.md`: onboarding demo outcome, overall verdict.
4. Viết `README.md` tiếng Việt: 
   - Giới thiệu case study + disclaimer KHÔNG phải competitor.
   - Quick-start reproduce (< 10 bước).
   - Key results (1 bảng).
   - Links sang 3 docs + 3 weekly summaries.
   - Attribution safishamsi + upstream link + license.
5. Viết blog post `docs/blog-post-vn.md`: hook, methodology, 3 charts, verdict, khi nào nên dùng graphify.
6. Cleanup: xóa `_upstream/`, `bench/repos/` (gitignored), trim large files.
7. Review sensitive data: grep API keys, tokens.
8. Tag release `v1.0.0`, push public.
9. (Optional) Post blog lên Dev.to/Medium tiếng Việt.

## Todo
- [ ] Viết `reports/week-1-summary.md`
- [ ] Viết `reports/week-2-summary.md`
- [ ] Viết `reports/week-3-summary.md`
- [ ] Viết `README.md` tiếng Việt
- [ ] Viết `docs/blog-post-vn.md`
- [ ] Cleanup repo (remove upstream clone, caches)
- [ ] Security sweep (no secrets)
- [ ] Add `LICENSE` MIT + attribution
- [ ] Tag `v1.0.0`, make repo public
- [ ] (Optional) publish blog externally

## Success Criteria
- Repo public, clone + `pip install -r requirements.txt` + reproduce < 30 phút.
- README tiếng Việt có ≥ 1 chart preview + results table.
- Attribution rõ ràng, không vi phạm MIT.
- 0 secrets leaked (verify qua `trufflehog` hoặc manual grep).

## Risk Assessment
| Risk | Mitigation |
|------|-----------|
| Leak API key khi push public | Pre-push hook grep `sk-ant-`; manual review |
| License conflict | Case study code MIT; reference graphify không re-distribute source |
| Blog bị hiểu lầm như competitor | Disclaimer rõ đầu README + blog |
| Repo size lớn (charts, cast) | Optimize PNG, trim cast, no binary raw |

## Security Considerations
- Chạy `git log -p | grep -iE "sk-ant|api[_-]key|password"` trước khi public.
- `.env` trong `.gitignore`, chỉ commit `.env.example`.
- Nếu dùng private repo cho demo → chuyển sang public target trước publish.

## Next Steps
- Sau publish: monitor issues, trả lời feedback.
- Optional follow-up: porting insights sang `HD-POC` personal toolchain.
