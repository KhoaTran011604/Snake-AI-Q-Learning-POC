# Phase 01 — Bot Foundation & Claude Code Loop (Week 1)

## Context Links
- Research: `../reports/research-260409-1339-ai-poc-ideas-trendshift.md`
- Reference arch: `chenhg5/cc-connect` (Go — inspiration only)
- Rules: `.claude/rules/development-rules.md`, `.claude/rules/documentation-management.md`

## Overview
- **Priority:** P1
- **Status:** pending
- **Effort:** ~30h / 5 days
- **Milestone:** `v0.1-oneshot` — one Discord message produces a real PR end-to-end on target repo

## Key Insights
- Reuse existing Discord bot app + token → zero onboarding friction
- `claude` CLI already respects `ANTHROPIC_BASE_URL` → no SDK integration needed
- discord.py runs an asyncio loop; long-running `claude` subprocess must be spawned via `asyncio.create_subprocess_exec` to avoid blocking gateway heartbeat
- GitPython is convenient but `git` subprocess is simpler + easier to audit → prefer subprocess
- Use a dedicated workdir per task: `workdirs/<task_id>/` = shallow clone of target repo, discarded on success

## Requirements

### Functional
- Command `!fix <free-text>` in whitelisted channel → creates Discord thread, acknowledges
- Bot creates branch `bot/<slug>-<timestamp>` off latest `main`
- Bot runs `claude -p "<instruction>"` inside workdir, captures stdout/stderr + exit code
- Bot commits all changes with generated message, pushes branch, opens PR
- Bot posts rich embed in thread: PR title, URL, files changed, +/- lines, Claude summary, CI status placeholder
- Bot refuses command if user OR channel not in allowlist → polite error reply
- Audit log entry written to `logs/audit.log` (append-only) for every invocation

### Non-Functional
- Each Python file ≤ 200 LoC (split if larger)
- Secrets via `.env` (`python-dotenv`)
- Crash in one task must not bring down the bot
- Per-user concurrency cap: 1 active task (bounce with "you already have a running task")

## Architecture

```
+-------------------+       +------------------+      +---------------+
| Discord Gateway   | <---> | bot/main.py      | ---> | claude CLI    |
| (websocket)       |       | discord.py Cog   |      | (subprocess)  |
+-------------------+       +------+-----------+      +------+--------+
                                   |                         |
                                   v                         v
                           +-------+---------+       +-------+--------+
                           | git_ops.py      |       | workdirs/<id>/ |
                           | (branch/commit/ |       | shallow clone  |
                           |  push)          |       +----------------+
                           +-------+---------+
                                   |
                                   v
                           +-------+---------+
                           | github_ops.py   |
                           | PyGithub + gh   |
                           +-----------------+
                                   |
                                   v
                           +-------+---------+
                           | tasks.db (sqlite)|
                           | + audit.log      |
                           +------------------+
```

## Related Code Files

### Create
- `pyproject.toml` — uv/poetry config, deps pinned
- `.env.example` — all required env vars with dummy values
- `.gitignore` — `.env`, `workdirs/`, `logs/`, `tasks.db`
- `src/bot/main.py` — entrypoint, loads config, starts discord client
- `src/bot/config.py` — pydantic or dataclass: token, allowlists, workdir root, target repo
- `src/bot/commands.py` — `!fix` command handler, orchestrates flow
- `src/bot/audit.py` — append-only audit log helper
- `src/core/claude_runner.py` — async subprocess wrapper around `claude -p`
- `src/core/git_ops.py` — clone, branch, commit, push (subprocess)
- `src/core/github_ops.py` — PR create via PyGithub, embed-ready result dict
- `src/core/task_store.py` — sqlite3 wrapper: create/get/update task rows
- `src/core/slug.py` — free-text → branch slug utility
- `README.md` — quickstart, credit cc-connect
- `scripts/smoke_test.py` — standalone run without Discord (dev aid)

### Modify
- None (greenfield project inside new subdir — e.g., repo root or `discord-bot/`)

### Delete
- None

## Implementation Steps
1. Scaffold project with `uv init` (or `poetry new`), commit empty skeleton
2. Add deps: `discord.py`, `PyGithub`, `python-dotenv`, `aiohttp` (for phase 2 placeholder)
3. Write `config.py` loading env: `DISCORD_TOKEN`, `GITHUB_TOKEN`, `TARGET_REPO`, `WORKDIR_ROOT`, `ALLOWED_USER_IDS`, `ALLOWED_CHANNEL_IDS`, `ANTHROPIC_BASE_URL`
4. Write `audit.py` — single function `log(event, **kwargs)` → JSONL append
5. Write `slug.py` — slugify + timestamp suffix
6. Write `git_ops.py` — `clone_fresh`, `create_branch`, `commit_all`, `push_branch` (each ≤ 40 LoC)
7. Write `claude_runner.py` — `async run(instruction, cwd) -> RunResult` with timeout
8. Write `github_ops.py` — `open_pr(repo, branch, title, body) -> PRInfo`
9. Write `task_store.py` — schema: `tasks(id TEXT PK, user_id, channel_id, status, branch, pr_url, created_at)`
10. Write `commands.py`:
    - Register `!fix` handler
    - Allowlist check → audit → sqlite task row → thread create
    - Git clone → branch → claude → commit → push → PR → embed
    - On exception: post error embed, mark task failed
11. Write `main.py` — load config, init client, load Cog, run
12. Create `scripts/smoke_test.py` — takes `--instruction` arg, runs core flow WITHOUT Discord
13. Manual run: smoke test first, then real Discord command against test repo
14. Tag `v0.1-oneshot`, record demo video (1 full happy path)

## Todo List
- [ ] Project scaffold + deps locked
- [ ] `.env.example` + `.gitignore` + README stub
- [ ] `config.py` with allowlists
- [ ] `audit.py`
- [ ] `slug.py`
- [ ] `git_ops.py`
- [ ] `claude_runner.py`
- [ ] `github_ops.py`
- [ ] `task_store.py` + sqlite schema init
- [ ] `commands.py` — !fix orchestration
- [ ] `main.py` entrypoint
- [ ] `scripts/smoke_test.py` passes against real repo
- [ ] Live Discord test run succeeds
- [ ] Tag `v0.1-oneshot` + record demo video

## Success Criteria
- Running `python -m src.bot.main` connects and responds to `!fix` in allowlisted channel
- A real PR is opened on the target test repo within ~60s of the command
- Embed in Discord thread shows PR URL + files changed + additions/deletions
- Audit log contains one JSONL line per command with user/channel/prompt/result
- Non-allowlisted user in allowlisted channel → denied with audit entry
- Every Python file ≤ 200 LoC

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Claude CLI not idempotent (reruns differ) | High | Med | One-shot per task; no auto-retry; store exit code + diff hash |
| Git conflict branching off stale `main` | Med | Med | Always `clone_fresh` per task (shallow); fail fast on conflict |
| Discord rate limit (50 msg/s global) | Low | Low | Single embed per state change; exponential backoff from discord.py |
| Claude CLI hang / infinite loop | Med | High | Hard timeout 5 min via asyncio; kill process group |
| Arbitrary code exec (untrusted user) | **Critical if unmitigated** | **Critical** | User ID allowlist + channel allowlist + workdir whitelist (only configured repos) |
| Blocking event loop with sync git calls | Med | Med | Use `asyncio.to_thread` for GitPython or async subprocess for git |
| Secrets leak via audit log | Low | High | Audit logs only prompts + user IDs, never env vars / tokens |

## Security Considerations
- `.env` MUST be in `.gitignore`; CI check via pre-commit hook
- Allowlists enforced BEFORE any subprocess spawn
- Workdir root configurable but defaults outside home dir (e.g., `./workdirs/`)
- Target repo hard-coded in config; bot refuses any other path reference
- GitHub PAT scoped to single repo via fine-grained token
- Audit log file mode 0600 where supported
- No `shell=True` in subprocess calls; always arg lists

## Next Steps
- Enter Phase 02: add webhook receiver + feedback loop
- Phase 02 depends on: task_store.py schema stable, PR number captured per task
