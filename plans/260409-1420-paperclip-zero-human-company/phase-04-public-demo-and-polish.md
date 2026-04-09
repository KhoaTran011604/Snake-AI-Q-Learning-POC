# Phase 04 — Public Demo & Polish (Week 4)

## Context Links
- Plan overview: `./plan.md`
- Previous: `./phase-03-autonomous-loop-and-governance.md`

## Overview
- **Priority:** P1
- **Status:** pending
- **Effort:** ~24h (intentionally light — contingency buffer)
- **Milestone:** Public read-only dashboard URL, 3-5 min demo video, README + casestudy doc, PR-ready commits, contingency time absorbed by slipped earlier work
- **Description:** No new features. Polish, record, document. Week 4 deliberately under-scoped because weeks 1-3 will slip.

## Key Insights
- **Zero new features** — if a "nice to have" appears, it goes in `FUTURE.md`, not week 4
- **Video > live demo** — avoid live-demo gods laughing at you; record once, show to everyone
- **Two audiences, one artifact:** casestudy doc addresses both devs (architecture) and stakeholders (outcomes/cost/ROI)
- **Reserve 30% as buffer** — earlier phase slippage absorbs here

## Requirements
### Functional
- **Public dashboard** (read-only, no auth):
  - Live agent activity feed (last 50 events from audit log)
  - Ticket board (Kanban: pending / in-progress / done)
  - Budget gauge (spent / $50)
  - Product stats (slug API req count, uptime)
- **Admin panel:** already exists; polish layout + add "seed demo ticket" button
- **Demo video:** 3-5 min, shows: intro → org chart → create ticket → watch agents act → approval gate → shipped
- **README.md:** what it is, how to run locally, architecture diagram, demo video link, cost report
- **Casestudy doc (`docs/casestudy.md`):** problem, solution, architecture, results, learnings, cost breakdown

### Non-functional
- Dashboard loads in <2s
- Video <50MB or hosted on YouTube/Loom
- README renders cleanly on GitHub

## Architecture
```
[Public visitor] --> [/dashboard (read-only)]
                              |
                              v
                   [Read-only DB queries]
                              |
                              v
                [audit_events + tickets + budget]

[Admin] --> [/admin] (password-gated) --> [full control]
```
No new backend components — reuse phase-03 infra.

## Related Code Files
### To Create
- `app/dashboard/page.tsx` — public dashboard
- `app/dashboard/components/agent-activity-feed.tsx`
- `app/dashboard/components/ticket-board.tsx`
- `app/dashboard/components/budget-gauge.tsx`
- `docs/casestudy.md`
- `docs/architecture-diagram.png` (exported from mermaid or excalidraw)
- `FUTURE.md` — parked ideas
- Demo video file or link in README

### To Modify
- `README.md` — full project README
- `docs/poc-overview.md` — finalize
- Admin panel — add "seed demo ticket" button

## Implementation Steps
1. **Day 1 — Public dashboard scaffold:** `/dashboard` route, 3 components (feed, board, gauge), pull from existing DB tables.
2. **Day 2 — Dashboard polish:** styling (Tailwind, keep default palette — YAGNI on design), mobile responsive, live refresh every 30s.
3. **Day 3 — Demo rehearsal run:** seed fresh ticket, run scheduler, capture screenshots, take notes on flow gaps. Fix any small UX blockers.
4. **Day 4 — Record demo video:** script 5 bullets, record with Loom/OBS, trim, upload.
5. **Day 5 — README + casestudy doc:** write both, include cost report ($X of $50 used), include architecture diagram.
6. **Day 6 — Commit cleanup:** squash WIP commits, verify all phases tagged, PR-ready branch. Run linter + tests.
7. **Day 7 — Contingency buffer:** absorb any slipped work from phases 1-3. If none, write blog post about the POC for bonus value.

## Todo List
- [ ] Public `/dashboard` route live
- [ ] Agent activity feed component
- [ ] Ticket board component
- [ ] Budget gauge component
- [ ] Demo rehearsal run + screenshots
- [ ] Demo video recorded + uploaded
- [ ] README.md complete (architecture, how-to-run, video link, cost)
- [ ] `docs/casestudy.md` written
- [ ] Architecture diagram exported
- [ ] `FUTURE.md` with parked ideas
- [ ] Commit history cleaned
- [ ] Final tag `v1.0-demo`
- [ ] Plan status updated in `plan.md` → completed

## Success Criteria
- Public dashboard URL loads for anonymous visitor, shows live data
- Demo video viewable, ≤5 min, covers full flow
- README answers "what is this?" in <30s of reading
- Casestudy doc includes actual cost breakdown (not hypothetical)
- Linter + tests pass on final commit
- Total POC spend ≤$50 confirmed from audit log

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Earlier phases slip into week 4 | **High** | Med | Week 4 pre-scoped at 24h (not 30h) for buffer |
| Live dashboard leaks sensitive ticket content | Med | Med | Filter audit feed to public-safe fields only; whitelist columns |
| Demo video re-record loop | Med | Low | Hard limit: 3 takes max, ship the least-bad |
| Casestudy doc scope creep | Med | Low | Template cap at 2 pages |
| Final commit breaks build | Low | High | Test pipeline before tagging v1.0 |

## Security Considerations
- Public dashboard: explicit column whitelist — no raw prompts, no customer emails, no API keys
- Rate limit `/dashboard` endpoint (10 req/sec/IP) to prevent scraping DoS
- Screenshots/video: redact any real API keys, emails, or tokens visible in admin
- README must not include real env values
- Casestudy must not include real customer data (all synthetic for POC)

## Next Steps
- Post-POC: retro doc, team presentation, decide extend vs archive
- If extend: features parked in `FUTURE.md` become next plan's inputs
- Follow-up: monitor public dashboard for 1 week, confirm budget stays under cap
