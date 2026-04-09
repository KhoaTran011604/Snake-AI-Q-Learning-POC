---
title: "Mini Zero-Human Company POC (paperclip fork)"
description: "4-week solo POC: fork paperclip, run 4 AI agents (CEO/Dev/Marketer/Support) that ship a Vietnamese Slug Generator micro-SaaS end-to-end"
status: pending
priority: P1
effort: 112h
branch: main
tags: [ai, agents, paperclip, multi-agent, poc, claude-api, vietnamese]
created: 2026-04-09
---

# Mini Zero-Human Company POC

Fork `paperclipai/paperclip` and operate an autonomous "company" of 4 AI agents that ship a real micro-SaaS (Vietnamese Slug Generator API) in 4 weeks. Demo-ready public dashboard + HITL governance + $50/month Claude budget cap.

## Context Links
- Research report: `../reports/research-260409-1339-ai-poc-ideas-trendshift.md`
- Base repo: https://github.com/paperclipai/paperclip
- Project rules: `../../.claude/rules/development-rules.md`
- Docs standards: `../../.claude/rules/documentation-management.md`

## Goals
1. Prove a 4-agent org can ship real code + marketing + support with $50 budget
2. Public demo: dashboard (read-only) + live Slug API + admin panel
3. Hybrid HITL: auto for internal dev, approval gates for public-facing actions
4. Weekly demo-able milestone — zero big-bang risk

## Phases

| # | Phase | Status | Effort | Milestone (demo-able) |
|---|---|---|---|---|
| 01 | [Setup fork + infra](./phase-01-setup-fork-and-infra.md) | pending | ~28h | paperclip running locally + deployed scaffold on Vercel, Claude API wired, $50 budget cap enforced |
| 02 | [Define agents + product](./phase-02-define-agents-and-product.md) | pending | ~30h | 4 agents configured, slug API v0 (manual) live, org chart + delegation rules loaded |
| 03 | [Autonomous loop + governance](./phase-03-autonomous-loop-and-governance.md) | pending | ~30h | First end-to-end autonomous run: CEO ticket → Dev codes → Marketer drafts announcement → human approves → shipped; kill switch verified |
| 04 | [Public demo + polish](./phase-04-public-demo-and-polish.md) | pending | ~24h | Public dashboard URL, demo video, README, casestudy doc, contingency buffer |

## Key Dependencies
- paperclip runtime maturity (agent scheduler, budget, heartbeat) — **riskiest assumption**
- Claude API access + billing (Anthropic account with spend cap)
- Vercel + Neon (free tier sufficient for demo)
- pnpm 9.15+, Node 20+, Git

## Top 3 Risks (see phase files for mitigations)
1. **Paperclip framework instability** — unknown maturity of runtime; mitigate by spiking paperclip in phase-01 day 1-2 before full commit
2. **Claude API cost overrun** — infinite agent loops can burn $50 in hours; mitigate via hard token caps per task, budget middleware, kill switch in phase-03
3. **Scope creep on slug API** — tempting to build "real" SaaS features; mitigate by locking spec day 1 of phase-02, no feature additions after

## Kill Switch (details in phase-03)
Single env flag `COMPANY_PAUSED=true` → paperclip scheduler halts all agents, pending tickets frozen, no new LLM calls. Accessible via admin panel button + CLI.

## Success Criteria (whole POC)
- [ ] Public dashboard URL live, read-only, shows agent activity + tickets
- [ ] Slug API responds correctly on ≥20 Vietnamese test cases
- [ ] ≥1 autonomous end-to-end run completed (CEO→Dev→Marketer→Support)
- [ ] Total Claude spend ≤ $50 for month
- [ ] Demo video (3-5 min) recorded
- [ ] README + casestudy doc merged
