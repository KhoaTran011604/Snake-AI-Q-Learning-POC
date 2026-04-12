# Research Report: Graphify Core + Token-Reduction POC

**Date:** 2026-04-12 20:04 (ICT)
**Goal:** Học core của `safishamsi/graphify`, thiết kế POC chứng minh graph giảm token khi LLM làm task.

---

## Executive Summary

Graphify = **deterministic code-graph skill** cho AI coding assistants. Core = tree-sitter AST pass (không LLM) + NetworkX + Leiden community + SHA256 cache. Claim: **71.5× ít token/query** trên 52 files mixed corpus.

Pattern này được validate bởi 2 nguồn độc lập:
- **Codebase-Memory** (arXiv 2603.27277): 10× token reduction, 2.1× ít tool calls, 49K nodes index trong 6s.
- **CodeGraph** (colbymchenry): 94% ít tool calls, 82% nhanh hơn, 56.6k vs 89.4k tokens trên VS Code TS repo (4K files).
- **DKB paper** (arXiv 2601.08773): AST graph > LLM-extracted graph cho multi-hop reasoning, build nhanh 10× hơn, correctness 15/15 vs 13/15 vs 6/15.

Kết luận: **Deterministic AST graph > LLM-extracted graph > vector-only RAG** cho code tasks. POC nên tập trung reproduce core loop: index → query → retrieve subgraph → so sánh token với baseline grep/read.

---

## Graphify Core Architecture

### Three-Pass Pipeline

1. **AST Pass (deterministic, no LLM)** — tree-sitter cho 22 ngôn ngữ (Python, TS, JS, Go, Rust, Java, C/C++, Ruby, C#, Kotlin, Scala, PHP…). Extract: classes, functions, imports, call graph.
2. **Transcription Pass** — faster-whisper local cho video/audio.
3. **Semantic Pass** — parallel Claude subagents extract concepts từ docs/papers/images.

### Graph Model

- **Nodes:** code symbols (function/class), doc concepts, paper citations. Có `degree` để detect "god nodes".
- **Edges:** tagged `EXTRACTED` | `INFERRED (confidence 0.0–1.0)` | `AMBIGUOUS`.
- **Storage:** `graph.json` persistent + NetworkX in-memory.
- **Clustering:** Leiden (graspologic) → communities → wiki/obsidian export cho agent navigation.
- **No embeddings / no vector DB** — similarity = relationship edges.

### Cache & Incremental

- SHA256 per file → `cache/` → `--update` chỉ reprocess changed files.
- Git hooks + file watcher → auto-sync.

### Output Artifacts

```
graphify-out/
├── graph.html          # vis.js interactive
├── graph.json          # queryable state (source of truth for LLM)
├── GRAPH_REPORT.md     # god nodes + suggested queries
├── wiki/               # agent-navigable markdown
├── obsidian/           # vault
└── cache/              # SHA256
```

### Query Surface

- `query "<intent>"` → semantic relationship discovery
- `path NodeA NodeB` → shortest path
- `explain <concept>` → definition extraction

---

## Tại Sao Giảm Token

| Mechanism | Tiết kiệm |
|---|---|
| Đọc `graph.json` compact thay vì raw source | Biểu diễn 1 function = ~50 tokens (name+sig+edges) vs ~500–2000 tokens raw |
| Subgraph retrieval (k-hop neighbors) thay vì grep + read nhiều file | Tránh load irrelevant context |
| Cache SHA256 | Index 1 lần, query nhiều lần — cost amortize |
| Leiden community → wiki summary | Agent đọc 1 wiki page thay vì 20 files |
| Deterministic (không LLM indexing) | Zero token cho extraction pass |

**Benchmark thực tế (từ các repo tương đương):**

| Tool | Corpus | Kết quả |
|---|---|---|
| Graphify | 52 files mixed | 71.5× ít token/query |
| CodeGraph | VS Code TS 4002 files | 52→3 tool calls, 89.4k→56.6k tokens |
| Codebase-Memory | 49K nodes | 10× token, 2.1× tool calls, index 6s |
| DKB (Shopizer) | Java enterprise | 15/15 correctness vs 6/15 no-graph, build 22s vs 215s |

---

## POC Design (Khuyến Nghị)

### Scope (KISS + YAGNI)

Build **minimal graph tool** reproduce core Graphify loop. **Chỉ 1 ngôn ngữ** (Python hoặc TS), **chỉ AST pass**, **bỏ qua** video/image/semantic pass. Focus: **đo token reduction có thật**.

### Stack Đề Xuất

- **Ngôn ngữ runner:** Python (tree-sitter bindings mature nhất) hoặc Node.js + `tree-sitter` npm.
- **Parser:** `tree-sitter` + `tree-sitter-python` (hoặc TS).
- **Graph:** `networkx` (Py) hoặc SQLite (giống CodeGraph — query nhanh hơn cho lớn).
- **Persistence:** `graph.json` + SHA256 cache file.
- **Query CLI:** 3 commands: `index`, `query`, `path`.

### Kiến Trúc POC

```
hd-poc-graph/
├── src/
│   ├── indexer.py          # tree-sitter → nodes/edges
│   ├── graph-store.py      # NetworkX + graph.json IO
│   ├── cache.py            # SHA256 incremental
│   ├── query.py            # k-hop neighborhood + search
│   └── cli.py              # index/query/path/stats
├── benchmark/
│   ├── corpus/             # test codebase (50–200 files)
│   ├── tasks.json          # 10 task prompts (find callers, trace flow, etc.)
│   ├── baseline-runner.py  # raw grep+read → count tokens
│   ├── graph-runner.py     # graph query → count tokens
│   └── report.md           # comparison
└── plans/
```

### Node/Edge Schema (Tối Thiểu)

**Node:**
```json
{
  "id": "src/auth.py::login",
  "type": "function",
  "name": "login",
  "file": "src/auth.py",
  "line": 42,
  "signature": "def login(user, pwd) -> Token",
  "docstring": "..."
}
```

**Edge:** `{from, to, type: "calls"|"imports"|"extends"|"references", confidence: 1.0}`

### Indexing Algorithm (2-Pass DKB-style)

1. **Pass 1 — Symbol discovery:** walk files, tree-sitter query extract `function_definition`, `class_definition`, `import_statement` → nodes + symbol table.
2. **Pass 2 — Edge resolution:** re-walk, resolve `call_expression` / `attribute` → match symbol table → edges.
3. Write `graph.json`, update `cache/{sha256}.json`.

### Query Algorithm

```
query(intent) →
  1. FTS/substring search trên node names → seeds (top-k=5)
  2. BFS k-hop (k=2) bidirectional neighbors
  3. Return subgraph (nodes + edges + signatures + docstrings)
  4. Optionally inline code snippets for top-3 nodes
```

### Benchmark Methodology (CRITICAL — proof of claim)

**Tasks** (10 realistic): "Find all callers of X", "Trace auth flow", "What depends on module Y", "Explain class Z's role", v.v.

**Baseline (naive LLM workflow):** giả lập agent dùng `grep` + `read_file` — đếm tokens = sum(file contents đọc được).

**Graph workflow:** agent gọi `query(intent)` → nhận subgraph JSON → đếm tokens.

**Metrics:**
- Tokens per task (tiktoken count)
- Tool calls per task
- Correctness (manual grade 0/1)
- Index build time + cache hit rate

**Deliverable:** bảng so sánh + chart giống benchmarks ở trên.

### Implementation Phases

| Phase | Effort | Output |
|---|---|---|
| P1 Setup + tree-sitter | 0.5d | parse 1 file → AST nodes |
| P2 Indexer + graph store | 1d | `index ./corpus` → graph.json |
| P3 Cache SHA256 | 0.5d | `--update` incremental |
| P4 Query (k-hop + search) | 1d | `query "auth"` → subgraph |
| P5 CLI + MCP wrapper | 0.5d | expose như MCP tool cho Claude Code |
| P6 Benchmark harness | 1d | baseline vs graph, token counts |
| P7 Report + visuals | 0.5d | markdown + vis.js HTML |

**Total: ~5 ngày** cho POC có số liệu thuyết phục.

---

## Critical Insights

1. **Đừng LLM-ize indexing.** DKB paper chứng minh LLM-extracted graphs miss ~30% files, build chậm 10×. AST pass deterministic là moat.
2. **Phải đo benchmark thật.** Claim "71.5×" của Graphify only holds on mixed corpus với docs+images. Code-only corpus nhỏ (6 files) chỉ ~1× — không tiết kiệm. POC phải chọn corpus đủ lớn (>50 files, >10K LOC).
3. **MCP wrapper là deployment path.** CodeGraph pattern: expose graph query qua MCP server → Claude Code tự dùng, không cần user gõ lệnh. Đây là cách "always-on graph awareness".
4. **Rule quan trọng từ CodeGraph:** "NEVER call context-builder directly trong main session — spawn subagent". Tránh context bloat chính là nơi token saving compound.
5. **Storage tradeoff:** NetworkX dễ prototype, SQLite+FTS5 scale tốt hơn cho >10K nodes. Bắt đầu NetworkX, migrate nếu cần.

---

## Áp Dụng Lại Cho Dự Án Khác (Case Study Value)

- **Reusable package:** `@your/code-graph` npm/pypi — init + MCP server + CLI.
- **Project bootstrap hook:** `postinstall` chạy index lần đầu.
- **Git hook:** `post-commit` → incremental sync.
- **Agent skill:** drop `.claude/skills/code-graph/` vào repo mới → plug&play.

---

## Resources & References

### Primary
- [Graphify GitHub](https://github.com/safishamsi/graphify/)
- [Graphify landing](https://graphify.net/)

### Comparable Implementations
- [CodeGraph (colbymchenry) — MCP + SQLite + tree-sitter](https://github.com/colbymchenry/codegraph)
- [GitNexus — client-side browser-based](https://github.com/abhigyanpatwari/GitNexus)

### Papers
- [Reliable Graph-RAG for Codebases: AST vs LLM-extracted (arXiv 2601.08773)](https://arxiv.org/abs/2601.08773)
- [Codebase-Memory: Tree-Sitter KG via MCP (arXiv 2603.27277)](https://arxiv.org/html/2603.27277)

### Tooling Docs
- tree-sitter bindings: https://tree-sitter.github.io/tree-sitter/
- NetworkX: https://networkx.org/
- graspologic (Leiden): https://github.com/graspologic-org/graspologic

### Tutorials
- [How I Built CodeRAG with Dependency Graph Using Tree-Sitter](https://medium.com/@shsax/how-i-built-coderag-with-dependency-graph-using-tree-sitter-0a71867059ae)

---

## Unresolved Questions

1. Ngôn ngữ target POC = Python hay TypeScript? (ảnh hưởng tree-sitter grammar + corpus chọn)
2. Corpus benchmark = dùng repo công khai nào? (VS Code, Shopizer, hay repo nội bộ?)
3. Có cần MCP server ngay trong POC hay CLI là đủ cho case study?
4. Chỉ so sánh với baseline grep+read, hay thêm vector RAG baseline (công bằng hơn nhưng tốn effort)?
5. Token counter dùng tiktoken (OpenAI) hay anthropic-tokenizer? (kết quả có thể lệch 10–20%)
