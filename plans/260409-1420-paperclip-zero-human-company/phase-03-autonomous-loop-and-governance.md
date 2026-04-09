# Phase 03 — Autonomous Loop & Governance (Week 3)

## Context Links
- Plan overview: `./plan.md`
- Previous: `./phase-02-define-agents-and-product.md`
- Next: `./phase-04-public-demo-and-polish.md`

## Overview
- **Priority:** P1
- **Status:** pending
- **Effort:** ~30h
- **Milestone:** First end-to-end autonomous run — CEO assigns "ship slug API v1" → Dev writes code + opens PR → human approves merge → Marketer drafts launch post → human approves → published. Kill switch verified under load.
- **Description:** Turn on the scheduler. Add heartbeat, approval gates, audit logging, kill switch. This is the riskiest phase for cost/runaway agents — governance must land BEFORE autonomy.

## Key Insights
- **Governance before autonomy:** kill switch + hard token caps ship day 1 of this phase, before any scheduler turns on.
- **Approval gates are opinionated:** auto for internal dev work (branch commits, test runs); manual for anything public/paid (merge to main, blog publish, deploy to prod, outbound emails).
- **Heartbeat is slow on purpose:** 1 tick per 15 min, not 1 tick per second. Slow heartbeat = capped cost + easier to observe.
- **Audit log is append-only** — every agent action, every LLM call (tokens in/out/cost), every approval decision.

## Requirements
### Functional
- **Scheduler:** paperclip heartbeat runs every 15 min, picks up pending tickets, assigns to agents
- **Per-task token cap:** hard limit 20k tokens per ticket; violation → ticket marked `failed`, escalated to CEO
- **Approval gates:**
  - Auto: git commit to feature branch, run tests, draft blog/social, draft ticket reply
  - Manual (admin UI button): merge PR to main, deploy to prod, publish blog, send email, any $ spend >$0
- **Audit log:** table `audit_events` (timestamp, agent, action, ticket_id, tokens, cost_cents, payload_hash)
- **Kill switch:** env flag `COMPANY_PAUSED=true` + admin UI toggle → scheduler short-circuits, no LLM calls, pending tickets frozen
- **Weekly retro (CEO):** at heartbeat tick on Monday 09:00, CEO reads last week's audit, writes retro to ticket

### Non-functional
- Scheduler must be idempotent (re-entering a tick mid-flight must not double-charge)
- Kill switch must take effect within 1 heartbeat tick (≤15 min worst case, ideally instant on next LLM call)
- Audit log write must not fail silently — scheduler halts on log failure

## Architecture
```
                 [Heartbeat scheduler (15min)]
                            |
                            v
                 [COMPANY_PAUSED check] --yes--> [halt]
                            | no
                            v
                 [Load pending tickets]
                            |
                            v
             [For each ticket: assign agent]
                            |
                            v
             [Agent runs] --LLM call--> [Budget middleware]
                            |                   |
                            |<-- token cap ----|
                            v
                   [Action type?]
                   /              \
              [auto]            [manual]
                 |                  |
                 v                  v
           [execute]        [queue for approval]
                 |                  |
                 v                  v
           [audit log] <------[admin panel]
```

## Related Code Files
### To Create
- `lib/scheduler/heartbeat.ts` — cron-like tick runner
- `lib/scheduler/token-cap.ts` — per-task enforcement
- `lib/governance/approval-gate.ts` — decide auto vs manual per action type
- `lib/governance/kill-switch.ts` — env + DB flag reader
- `lib/audit/audit-logger.ts` — append-only write helper
- `app/api/admin/kill-switch/route.ts` — POST toggles flag
- `app/api/admin/approvals/route.ts` — list + approve/reject pending actions
- `app/admin/approvals/page.tsx` — UI for pending approvals
- `db/migrations/xxxx-audit-and-approvals.sql` — tables
- `config/action-policies.yaml` — maps action types → auto/manual
- `scripts/seed-first-run.ts` — creates initial "ship v1" ticket

### To Modify
- Paperclip agent runner — inject token cap + audit log hooks
- CEO agent — add weekly retro logic
- Admin panel navigation — add approvals + kill switch

## Implementation Steps
1. **Day 1 — Governance foundation:** kill switch (env + DB flag), audit log table + writer, token cap per task. Test: set flag true → mock scheduler tick does nothing.
2. **Day 2 — Approval gate config:** `action-policies.yaml`, gate logic, pending-approvals DB table. Manual test: fake "publish blog" action → lands in approvals queue.
3. **Day 3 — Admin approvals UI:** list page, approve/reject buttons, kill switch toggle button. Hooked to API routes.
4. **Day 4 — Heartbeat scheduler:** 15min tick, picks pending tickets, routes to agents, enforces token cap + audit log. Dry-run mode first (no real LLM calls).
5. **Day 5 — First real run:** seed "ship slug API v1" ticket assigned to CEO. Turn scheduler on. CEO should break it into sub-tickets for Dev (implement tests) + Marketer (draft launch post). Observe.
6. **Day 6 — Debug + weekly retro:** fix issues from day 5. Implement CEO weekly retro logic. Second dry-run.
7. **Day 7 — Kill switch drill + tag `v0.3-autonomous`:** simulate runaway (set token cap artificially low, run loop) → verify kill switch halts it. Buffer for fixes.

## Todo List
- [ ] Kill switch env + DB + API + UI button
- [ ] Audit log table + writer + integrated into agent runner
- [ ] Per-task token cap enforced (tested)
- [ ] Approval gate config + logic
- [ ] Pending approvals DB table + API + UI
- [ ] Heartbeat scheduler (15min) with dry-run mode
- [ ] Seed ticket "ship slug API v1"
- [ ] First real autonomous run observed + logged
- [ ] CEO weekly retro wired
- [ ] Kill switch drill passed
- [ ] `v0.3-autonomous` tag

## Success Criteria
- Kill switch halts scheduler within 1 tick, verified by drill
- First autonomous run completes with: ≥2 agents touched, ≤1 human approval, cost ≤$5
- Audit log contains row for every LLM call + every action
- Attempting a manual-gate action auto-executes → test fails (policy enforced)
- Total spend at end of phase ≤$15 (still under $50 cap)

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Agent infinite loop burns budget | Med | **Critical** | Token cap per task + global budget + kill switch + slow heartbeat |
| Scheduler race conditions | Med | Med | Idempotent tick, row-level lock on ticket pickup |
| CEO retro ticket loop (retro creates retro) | Low | Med | Guard: skip ticket if parent is a retro |
| Approval UI forgotten → blocks progress | Med | Low | Email/desktop notification on new pending |
| Kill switch flag cached stale | Low | Critical | Read DB flag every LLM call, not on scheduler start |

## Security Considerations
- Kill switch endpoint protected by admin password + rate limit
- Audit log immutable: no UPDATE/DELETE granted to runtime DB user
- Token cap enforced at middleware layer (not just prompt) — cannot be bypassed by agent
- Approvals API requires admin session — no anon approvals
- Secrets never logged: audit stores `payload_hash`, not raw prompts with PII
- CEO agent cannot modify its own budget or kill switch (tool allowlist enforced)

## Next Steps
- Unblocks: phase-04 (demo needs real autonomous run footage)
- Follow-up: capture screenshots/video of first run for demo material
