# Phase 02 — Define Agents & Product (Week 2)

## Context Links
- Plan overview: `./plan.md`
- Previous phase: `./phase-01-setup-fork-and-infra.md`
- Spike notes (from phase-01): `../reports/spike-paperclip-notes.md`

## Overview
- **Priority:** P1
- **Status:** pending
- **Effort:** ~30h
- **Milestone:** 4 agents instantiated in paperclip, Vietnamese Slug Generator API v0 deployed and manually callable, org chart + delegation rules loaded, agents can receive tickets (but not yet act autonomously)
- **Description:** Transform empty scaffold into recognizable "company" with 4 roles + the product they'll sell. No autonomy yet — manual ticket creation tests delegation.

## Key Insights
- **Lock product spec day 1** — slug API is trivially scoped; resist adding "bulk endpoint", "auth tokens", etc. (YAGNI)
- **Agents share 1 system prompt template** — differ only in role block + tools allowed (DRY)
- **Delegation rules as data, not code** — simple JSON/YAML config so CEO can re-assign without deploy
- **Manual before auto:** phase-02 validates routing by hand; phase-03 adds the autonomous loop

## Requirements
### Functional
- **Product — Vietnamese Slug Generator API:**
  - `POST /api/slug` body `{ text: string, maxLength?: number }` → `{ slug: string }`
  - Handles diacritics (đ→d, ă/â/ê/ô/ơ/ư, all tone marks)
  - Edge cases: empty, >500 chars, only-numbers, emoji (strip), mixed EN/VN
  - Rate limit: 10 req/min anon (IP-based), 100 req/min with API key
  - Free tier = 1000 req/day, paid = unlimited (no billing for POC — track only)
- **Agents (4):** CEO, Dev, Marketer, Support — each with role prompt + tool allowlist
- **Org chart:** CEO → {Dev, Marketer, Support}; CEO can create any ticket; Dev/Marketer/Support can only create tickets upward (to CEO) or sideways with CEO cc
- **Delegation rules config:** YAML file mapping ticket types → target agent

### Non-functional
- Slug API p95 latency <100ms (pure function)
- Agent response time <30s per ticket (Claude API latency dominates)

## Architecture
```
                    [CEO agent]
                  /     |      \
                 v      v       v
            [Dev]   [Marketer]  [Support]
              |         |          |
              v         v          v
         [Slug API] [Blog/Social] [Tickets]
              \         |          /
               v        v         v
              [Shared Postgres + paperclip runtime]
              [Budget middleware] [Org chart YAML]
```

## Related Code Files
### To Create
- `agents/ceo.ts` — role prompt + config
- `agents/dev.ts`
- `agents/marketer.ts`
- `agents/support.ts`
- `agents/base-role-template.ts` — shared system prompt skeleton (DRY)
- `config/org-chart.yaml` — hierarchy + delegation rules
- `app/api/slug/route.ts` — the product endpoint
- `lib/slug/vietnamese-slugify.ts` — pure slug function
- `lib/slug/vietnamese-slugify.test.ts` — unit tests (≥20 cases)
- `lib/rate-limit.ts` — simple in-memory/Redis rate limiter

### To Modify
- Paperclip agent registry (wherever agents are loaded)
- Admin panel — add "create ticket" form for manual testing

## Implementation Steps
1. **Day 1 — Product spec lock + slug function:** write `vietnamese-slugify.ts` with 20+ test cases, commit. Lock spec in `docs/poc-overview.md`.
2. **Day 2 — Slug API endpoint:** wire `POST /api/slug`, add rate limit, deploy, smoke test with `curl`.
3. **Day 3 — Agent base template + CEO:** define shared role template, instantiate CEO with goals + budget allocation logic.
4. **Day 4 — Dev + Marketer + Support agents:** instantiate remaining three, each with tool allowlist (Dev: git/file-edit, Marketer: blog-post/social-draft, Support: ticket-reply).
5. **Day 5 — Org chart YAML + delegation:** write config, wire loader, manually create ticket "add emoji stripping" via admin → verify routes to Dev.
6. **Day 6 — Manual E2E test:** create 4 tickets (1 per agent), verify each agent receives + drafts response. No auto-action yet.
7. **Day 7 — Buffer + tag `v0.2-agents`.**

## Todo List
- [ ] Slug function + tests (≥20 VN cases)
- [ ] `/api/slug` endpoint + rate limit + deploy
- [ ] Product spec locked in docs
- [ ] CEO agent defined
- [ ] Dev agent defined
- [ ] Marketer agent defined
- [ ] Support agent defined
- [ ] Shared role template extracted
- [ ] `org-chart.yaml` + loader
- [ ] Manual ticket → correct agent (4/4 routes work)
- [ ] Admin "create ticket" form
- [ ] `v0.2-agents` tag

## Success Criteria
- `curl -X POST .../api/slug -d '{"text":"Xin chào Việt Nam"}'` → `{"slug":"xin-chao-viet-nam"}`
- All 20 slug unit tests pass
- Manually creating a ticket in admin, each of 4 agents picks up correct type
- Budget counter still reads $0 (agents haven't autonomously acted)

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Paperclip agent API unclear from spike | Med | High | Reference paperclip's own example agents; worst case, simpler wrapper class |
| Slug edge cases break in prod | Low | Low | 20+ test cases + fuzz with real VN text |
| Rate limiter too restrictive for demo | Low | Low | Configurable, relax for demo day |
| Agent prompts too long → token cost spike | Med | Med | Keep role blocks <500 tokens each, monitor in phase-03 |

## Security Considerations
- Rate limit BEFORE any LLM call (prevents abuse → cost attack)
- API keys for paid tier stored hashed in DB (even if unused, for demo realism)
- Agent tool allowlist enforced — Dev cannot post to social; Marketer cannot touch git
- Org chart validation: reject ticket creations violating hierarchy
- Sanitize slug input (`maxLength` cap at 500, strip control chars)

## Next Steps
- Unblocks: phase-03 (autonomous loop needs agents + delegation wired)
- Follow-up: phase-03 adds scheduler + approval gates on top of this manual flow
