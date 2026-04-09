# Phase 02 — Webhook Feedback Loop & Polish (Week 2)

## Context Links
- Phase 1: `./phase-01-bot-foundation-and-claude-code-loop.md`
- smee.io docs: https://smee.io
- GitHub webhook events: `check_suite`, `pull_request`, `pull_request_review`

## Overview
- **Priority:** P1
- **Status:** pending
- **Effort:** ~30h / 5 days
- **Milestone:** `v1.0-demo` — GitHub events update the originating Discord thread automatically

## Key Insights
- smee.io forwards webhooks over SSE → needs a local smee client OR direct HTTP post to local aiohttp server
- Simpler: run `smee -u <url> --target http://localhost:8000/webhook` as a sidecar (npm package) OR use `pysmee` stream client inside our asyncio loop (keeps one process)
- Mapping PR → Discord thread is trivial via `tasks.db` (PR URL stored in phase 1)
- Infinite-loop risk: if bot user merges/reviews its own PR, GitHub fires events → bot posts → nothing, BUT if bot also opens sub-PRs, filter by `sender.login == BOT_GH_USER`
- Fallback polling: every 60s scan open tasks, call GH API, detect state changes → covers smee.io downtime

## Requirements

### Functional
- aiohttp server on localhost:8000 handles `POST /webhook`
- Verify `X-Hub-Signature-256` HMAC against shared secret
- Route events: `check_suite.completed` → CI update; `pull_request_review.submitted` → review update; `pull_request.closed` (merged=true) → merged update
- Look up task by PR URL/number, find thread ID, post an embed update in that thread
- `!cancel <task_id>` command aborts a running task (best-effort: kill claude process, mark failed)
- Rate limit: max 3 concurrent tasks per user (queue overflow → reject with message)
- Fallback poller (disabled by default, enabled via env) polls open PRs every 60s

### Non-Functional
- Webhook handler replies ≤200ms (defer heavy work to background task)
- HMAC constant-time compare
- SQLite writes serialized via a single writer task
- Code files ≤ 200 LoC each

## Architecture

```
GitHub --push event--> smee.io -----SSE----> smee-client ---> aiohttp :8000/webhook
                                                                  |
                                                                  v
                                                        +---------+---------+
                                                        | webhook_router.py |
                                                        | HMAC verify +     |
                                                        | event dispatch    |
                                                        +---------+---------+
                                                                  |
                         +----------------------+-----------------+
                         v                      v
                 +-------+-------+      +-------+-------+
                 | thread_updater|      | task_store.py |
                 | (discord post)|      | (lookup by PR)|
                 +---------------+      +---------------+

Fallback poller (optional):
  asyncio.task every 60s -> GH API -> diff state vs tasks.db -> same thread_updater
```

## Related Code Files

### Create
- `src/webhook/server.py` — aiohttp app, starts alongside discord client in same loop
- `src/webhook/verify.py` — HMAC SHA256 signature check
- `src/webhook/router.py` — event type dispatch
- `src/webhook/handlers.py` — `handle_check_suite`, `handle_review`, `handle_merged`
- `src/core/thread_updater.py` — given task row + status, posts discord embed
- `src/core/poller.py` — optional fallback polling loop
- `src/bot/cancel_command.py` — `!cancel <task_id>` handler
- `scripts/start_smee.sh` — convenience: launch smee client pointing at local server
- `docs/demo-script.md` — demo video walkthrough script (≤ 3 min)
- `CONTRIBUTING.md` — short notes for future contributors

### Modify
- `src/bot/main.py` — start aiohttp runner alongside discord.py
- `src/bot/commands.py` — enforce 3-concurrent-task cap; register cancel command
- `src/core/task_store.py` — add columns: `ci_status`, `review_status`, `merged_at`, `cancelled`
- `src/bot/config.py` — add `WEBHOOK_SECRET`, `WEBHOOK_PORT`, `BOT_GH_USER`, `ENABLE_POLLER`
- `.env.example` — new vars
- `README.md` — webhook setup section + smee instructions

### Delete
- None

## Implementation Steps
1. Extend `task_store.py` with new columns + migration (single-file `schema.sql` re-run is fine for POC)
2. Write `verify.py` — constant-time HMAC compare using `hmac.compare_digest`
3. Write `router.py` — parse event header + JSON, dispatch to handlers
4. Write `handlers.py` — each handler: lookup task by PR number (repo + number), call `thread_updater`
5. Write `thread_updater.py` — renders embed per event type; drops update if sender == `BOT_GH_USER`
6. Write `server.py` — aiohttp app factory, mount on port from config
7. Modify `main.py` — `asyncio.gather(discord_client.start(...), web_runner.start())`
8. Add `cancel_command.py` — look up active task, SIGTERM claude subprocess (keep PID in task row)
9. Enforce concurrency cap in `commands.py` via `task_store.count_active(user_id)`
10. Write `poller.py` — opt-in loop, reuses `thread_updater`
11. Set up smee.io channel, run `start_smee.sh`, add real GitHub webhook on target repo
12. End-to-end test: open PR, push bad commit → CI fails → Discord thread shows failure
13. End-to-end test: merge PR manually → Discord thread shows merged
14. Write demo script, record 2-3 min video
15. Tag `v1.0-demo`

## Todo List
- [ ] `task_store.py` migrated with new columns
- [ ] `verify.py` HMAC
- [ ] `router.py` dispatch
- [ ] `handlers.py` — check_suite / review / merged
- [ ] `thread_updater.py` posts embeds
- [ ] `server.py` aiohttp on configured port
- [ ] `main.py` runs discord + web together
- [ ] `!cancel` command working
- [ ] 3-concurrent-task cap enforced
- [ ] Optional poller implemented + env-gated
- [ ] smee.io tunnel live + GitHub webhook registered
- [ ] E2E: CI fail event → thread update
- [ ] E2E: PR merged event → thread update
- [ ] README + CONTRIBUTING + demo script
- [ ] Demo video recorded
- [ ] Tag `v1.0-demo`

## Success Criteria
- Local bot receives a signed webhook and updates the correct Discord thread within 5s
- Invalid HMAC signature is rejected with 401
- `!cancel` kills an in-flight `claude` run and posts a cancellation embed
- Demo video clearly shows: command → PR → CI status → merge status, all in one thread
- No secrets in repo; `.env.example` fully documents required vars

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| smee.io downtime | Med | Med | Optional polling fallback; document manual override |
| Infinite loop (bot event → bot post → event) | Med | High | Ignore events where `sender.login == BOT_GH_USER`; `!cancel` kill switch |
| Webhook flood / replay | Low | Med | HMAC verify + idempotency via `delivery_id` dedupe in task_store |
| SQLite concurrency write conflicts | Low | Low | Single writer task, WAL mode |
| Discord 50-msg/s global limit | Low | Low | One embed per state transition only |
| Event ordering (merge before check_suite) | Med | Low | Store last state; only update if new state > old state in enum |
| Port 8000 conflict on user machine | Low | Low | Configurable via `WEBHOOK_PORT` |

## Security Considerations
- Webhook secret stored only in `.env`, never logged
- HMAC verify via `hmac.compare_digest` (timing-safe)
- Bind aiohttp to `127.0.0.1` only — smee forwards locally, no external exposure
- `!cancel` restricted to task owner OR allowlisted admin IDs
- Fallback poller uses same fine-grained PAT from phase 1 (no broader scope)
- Audit log extended with webhook events (delivery_id, event type, PR number)

## Next Steps
- If time permits (stretch): reply-to-thread triggers follow-up Claude run on same branch
- If time permits: `!status` command listing active tasks across channels
- Post-POC: consider splitting webhook receiver to its own process for HA
