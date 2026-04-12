# Brainstorm Summary: Code-Graph MCP + Semantic Diff Review

**Date:** 2026-04-12 20:04 (ICT)
**Decision status:** Agreed — proceed to `/plan`

---

## Problem Statement

Claude Code (và các AI coding assistant khác) tốn token khủng khi làm task trên repo lớn vì phải grep + read nhiều file. Graphify/CodeGraph chứng minh code graph giảm ~10× token, nhưng:

1. Không có tool focus sâu TS/Py với benchmark reproducible.
2. Chưa có sản phẩm dùng graph cho **semantic diff review** — một bài toán khó thực sự (reviewer không hiểu impact chỉ từ `git diff` text).

## Requirements

- Audience: dev cá nhân + team (global).
- Runtime: TypeScript (MCP SDK mature, npm distribution).
- Languages indexed: TS + Python (v0.1).
- Budget: Claude qua proxy (cost không phải rào cản benchmark).
- Timeline: 2–3 tuần.
- Output: public repo + progress report (weekly) + benchmark charts + blog.

## Approaches Evaluated

### A. Pure token-reduction clone (như graphify/codegraph)
- ❌ Thị trường đã đông, khó khác biệt.

### B. Multi-agent parallel orchestrator (OmX-style)
- ❌ Effort cao (3+ tuần), merge logic dễ fail thành demo toy.

### C. Vietnamese document LLM pipeline (markitdown + VietOCR)
- ✅ Market fit VN cao, nhưng lệch target global dev.

### D. **Code-Graph MCP + Semantic Diff Review (CHỌN)**
- ✅ Reuse 1 engine → 2 giá trị: token reduction + impact analysis.
- ✅ Diff rõ so với đối thủ: semantic diff là feature độc, TS-first, MCP-native.
- ✅ Vừa 2–3 tuần, benchmark đo được.

## Final Solution

**Stack:** TypeScript, tree-sitter (TS + Py grammars), SQLite + FTS5, MCP SDK, tiktoken cho token counting.

**Core modules:**
- `indexer` — AST pass, 2-phase (symbol discovery → edge resolution)
- `graph-store` — SQLite nodes/edges/FTS
- `cache` — SHA256 per file, incremental
- `query` — k-hop BFS, FTS search, impact analysis
- `diff` — AST graph diff giữa 2 commits → impact report
- `mcp-server` — expose tools cho Claude Code
- `cli` — index/query/path/diff/stats
- `bench` — reproducible benchmark harness

**Output artifacts (per repo indexed):**
```
.code-graph/
├── graph.db          # SQLite
├── cache/            # SHA256
└── report.md         # god nodes + stats
```

## Rationale

1. **Proven pattern.** DKB paper + graphify + codegraph đều validate AST graph > LLM-extracted > vector-only cho code.
2. **Semantic diff là moat.** Đối thủ chưa làm; reviewer thực sự đau vấn đề này.
3. **TS-first tránh chạy đua 22 languages** — depth > breadth cho POC.
4. **MCP-native = zero-friction adoption** cho Claude Code users.

## Roadmap (3 tuần)

**W1: Graph Engine** — indexer, store, cache, CLI. Target: index 1000 files <30s.
**W2: MCP + Benchmark** — MCP tools, 15 tasks × 3 repos, report token/toolcall/correctness/latency. Target: ≥5× token reduction, ≥70% fewer tool calls.
**W3: Semantic Diff + Polish** — `graph_diff` command, impact reports, demo 5 PRs, README + blog + progress report. Target: catch ≥80% impact cases.

## Success Metrics

- Token reduction ≥ 5× trên corpus ≥ 500 files (vs grep+read baseline)
- Tool calls giảm ≥ 70%
- Semantic diff accuracy ≥ 80% vs manual review
- Install < 2 phút (`npx @your/code-graph init`)
- ≥ 50 GitHub stars tuần đầu release

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| TS dynamic types làm call resolution sai | Tag edge `confidence < 1.0`, document known-limits |
| Benchmark nghi cherry-picked | Public corpus + reproducible scripts, include failure cases |
| Overlap với graphify/codegraph | Diff rõ: semantic diff, TS-first, proxy-friendly |
| Scope creep sang nhiều languages | Lock TS+Py cho v0.1, roadmap lang khác ở v0.2+ |
| SQLite scale kém nếu >100K nodes | Migration path sang DuckDB/LMDB ghi rõ trong ADR |

## Security Considerations

- Không upload code ra ngoài (local-first, giống codegraph).
- MCP server bind localhost.
- Cache không chứa source snippets raw; chỉ signatures + metadata.

## Next Steps

1. `/plan` → tạo plan chi tiết với 7–8 phases, TODO tasks, file structure.
2. Init repo + CI (lint + test).
3. Week 1 kickoff: tree-sitter TS spike.

## Unresolved Questions

1. Repo name? (suggestion: `code-graph-mcp` hoặc branded)
2. License? MIT hay AGPL (chống fork commercial)?
3. Benchmark corpus: chọn repo OSS nào? (đề xuất: `nestjs/nest` cho TS, `fastapi/fastapi` cho Py, `supabase/supabase` cho mixed)
4. Blog host: dev.to / medium / own site?
5. Progress report cadence: daily commit log hay weekly summary?
