# Phase 06 — Onboarding Demo

## Context Links
- Plan: [plan.md](./plan.md)
- Prev: [phase-05-benchmark-analysis-and-report.md](./phase-05-benchmark-analysis-and-report.md)

## Overview
- **Date**: 2026-04-26 → 2026-04-28
- **Priority**: P2
- **Status**: pending
- **Review**: giữa Week 3
- **Description**: Index Supabase (hoặc fallback), start `graphify serve` MCP, hỏi 10 câu onboarding thực tế, so sánh answer có/không graphify, record asciinema.

## Key Insights
- Onboarding dev mới = câu hỏi dạng "code này đâu?", "hàm này ai gọi?", "làm sao add feature X?".
- Value rõ nhất khi new dev zero context về repo.
- Asciinema ghi terminal + MCP interactions là deliverable visual thuyết phục.

## Requirements
**Functional**
- 10 câu onboarding trong `demo/questions.md` với ground_truth.
- 2 transcripts: with-graphify và without.
- `demo/asciinema.cast` record ≤ 10 phút.
- Score ≥ 9/10 correct khi có graphify.
**Non-functional**
- Demo reproducible qua 1 README section.

## Architecture
```
Supabase monorepo (pinned SHA)
  → graphify build (cached từ Phase 4)
  → graphify serve (MCP stdio)
       ↕ Claude Desktop / custom client
  → answers with tool traces
Baseline:
  → Claude + grep/read_file only
```

## Related Code Files
**Đọc**
- `graphifyy/serve.py`
- `graphifyy/skill-*.md` (9 platform skill files — reference cho MCP client setup)

**Tạo**
- `demo/questions.md` (10 Q + ground_truth)
- `demo/transcript-with-graphify.md`
- `demo/transcript-baseline.md`
- `demo/asciinema.cast`
- `demo/setup.md` (cách chạy lại)
- `docs/onboarding-demo.md` (writeup tiếng Việt)

## Implementation Steps
1. Xác nhận repo target (Supabase pinned hoặc NestJS fallback).
2. Build graph (reuse cache Phase 4 nếu cùng SHA).
3. Soạn 10 câu onboarding categories: architecture overview, entry points, data flow, auth flow, test locations, deployment config, new feature how-to, debugging tips, dependency graph, refactor impact.
4. Start `graphify serve` → connect via Claude Desktop MCP config hoặc CLI client.
5. Run 10 Q với graphify enabled, capture transcripts.
6. Run 10 Q baseline (Claude + grep/read), capture transcripts.
7. Manual score correctness mỗi Q (0–1).
8. Record asciinema: 3 câu đại diện (1 easy, 1 medium, 1 hard).
9. Viết `docs/onboarding-demo.md`: setup, transcript comparison, score table, observations.
10. Embed asciinema playback link.

## Todo
- [ ] Finalize target repo (Supabase or NestJS)
- [ ] Build/reuse graph cache
- [ ] Viết 10 câu `demo/questions.md` + ground_truth
- [ ] MCP client config (document trong `demo/setup.md`)
- [ ] Run + capture 2 transcripts
- [ ] Score correctness
- [ ] Record `demo/asciinema.cast`
- [ ] Viết `docs/onboarding-demo.md`

## Success Criteria
- Score ≥ 9/10 với graphify.
- Score baseline < score graphify (chứng minh value).
- Asciinema chạy được trên GitHub/web.
- Setup reproducible < 15 phút cho người mới.

## Risk Assessment
| Risk | Mitigation |
|------|-----------|
| MCP client setup Windows phức tạp | Fallback WSL2; document cả 2 |
| Câu hỏi ambiguous → scoring bias | 2-người score, hoặc rubric rõ ràng |
| Supabase thay đổi giữa chừng | Pin SHA, reference commit trong demo |
| Asciinema file lớn | Trim, giới hạn 10 phút |

## Security Considerations
- Supabase public OK; nếu dùng private repo, redact.
- Không để API key xuất hiện trong asciinema (dùng env var).

## Next Steps
→ Phase 07: finalize, weekly summaries, blog post, publish.
