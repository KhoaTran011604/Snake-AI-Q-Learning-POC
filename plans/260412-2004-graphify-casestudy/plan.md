---
title: "Graphify Case Study — Học core, benchmark token reduction, demo onboarding"
description: "Case study sâu safishamsi/graphify: dissect source, benchmark 5-10× token reduction, demo MCP onboarding trên Supabase monorepo."
status: pending
priority: P2
effort: 15d
branch: hd-poc2
tags: [case-study, graphify, code-graph, mcp, benchmark, vietnamese]
created: 2026-04-12
---

# Plan: Graphify Case Study (Tiếng Việt)

## Mục tiêu
Nghiên cứu sâu 100% vào package `graphifyy` (safishamsi/graphify, Python 3.10+, MIT). Mục đích:
1. Hiểu core pipeline: detect → extract → build → cluster → analyze → report → export.
2. Chứng minh token reduction ≥5× (medium) và ≥10× (large repo) qua benchmark realistic.
3. Demo MCP onboarding assistant trên Supabase monorepo (fallback NestJS nếu build >10 phút).
4. KHÔNG xây competitor, KHÔNG contribute upstream PR.

## Ràng buộc
- Timeline 3 tuần (~15 ngày làm việc).
- Environment ưu tiên: Windows native; fallback WSL2 nếu graphify có bug trên Windows.
- Docs tiếng Việt; identifiers kebab-case (python module snake_case).
- 3 weekly summary reports bắt buộc.

## Output Repository Structure
```
graphify-casestudy-vn/
├── README.md
├── requirements.txt
├── docs/
│   ├── graphify-internals.md
│   ├── benchmark-report.md
│   └── onboarding-demo.md
├── bench/
│   ├── tasks.json
│   ├── baseline-runner.py
│   ├── graphify-runner.py
│   └── results/
├── demo/
│   ├── questions.md
│   └── asciinema.cast
└── reports/
    ├── week-1-summary.md
    ├── week-2-summary.md
    └── week-3-summary.md
```

## Success Metrics
- Token reduction ≥5× (medium ~500 files), ≥10× (large ~2000+ files Supabase).
- Build time < 2 phút cho repo 2000+ files.
- Onboarding ≥9/10 câu đúng khi có graphify context.
- Tất cả scripts reproducible: seed pinned, `requirements.txt` khoá version.

## Phases

| # | Phase | File | Effort | Status |
|---|-------|------|--------|--------|
| 1 | Setup & Environment | [phase-01-setup-and-environment.md](./phase-01-setup-and-environment.md) | 1d | pending |
| 2 | Dissect Core Source | [phase-02-dissect-core-source.md](./phase-02-dissect-core-source.md) | 3d | pending |
| 3 | Benchmark Preparation | [phase-03-benchmark-preparation.md](./phase-03-benchmark-preparation.md) | 2d | pending |
| 4 | Benchmark Execution | [phase-04-benchmark-execution.md](./phase-04-benchmark-execution.md) | 2d | pending |
| 5 | Benchmark Analysis & Report | [phase-05-benchmark-analysis-and-report.md](./phase-05-benchmark-analysis-and-report.md) | 2d | pending |
| 6 | Onboarding Demo | [phase-06-onboarding-demo.md](./phase-06-onboarding-demo.md) | 3d | pending |
| 7 | Finalize & Publish | [phase-07-finalize-and-publish.md](./phase-07-finalize-and-publish.md) | 2d | pending |

## Context Links
- Brainstorm: `plans/reports/brainstorm-260412-2004-graphify-casestudy.md`
- Research: `plans/reports/research-260412-2004-graphify-poc.md`

## Tuần milestones
- **Week 1**: Phase 1–2 xong → `reports/week-1-summary.md` (setup + internals doc).
- **Week 2**: Phase 3–5 xong → `reports/week-2-summary.md` (benchmark report).
- **Week 3**: Phase 6–7 xong → `reports/week-3-summary.md` (demo + public).

## Unresolved Questions
- Model Claude dùng cho semantic pass (Haiku vs Sonnet) — quyết định ở Phase 4.
- Supabase commit SHA pin — chốt ở Phase 3.
