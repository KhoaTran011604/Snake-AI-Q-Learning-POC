# Phase 01 — Setup Fork & Infra (Week 1)

## Context Links
- Plan overview: `./plan.md`
- Base repo: https://github.com/paperclipai/paperclip
- Research: `../reports/research-260409-1339-ai-poc-ideas-trendshift.md`

## Overview
- **Priority:** P1 (blocks everything)
- **Status:** pending
- **Effort:** ~28h
- **Milestone:** paperclip running locally, minimal scaffold deployed to Vercel + Neon, Claude API wired with `$50/month` budget cap, admin panel accessible
- **Description:** Establish foundation. Spike paperclip first 2 days to de-risk. Get scaffold deployed publicly before any agent work.

## Key Insights
- **Spike before commit:** paperclip maturity is riskiest assumption — day 1-2 is a timeboxed spike. If blocker found, plan pivots (documented exit criteria below).
- **Deploy early:** Vercel + Neon setup on day 3 prevents last-week deploy surprises.
- **Budget first:** enforce `$50/month` cap before any agent runs a single token. Better to block on day than bankrupt on day 7.

## Requirements
### Functional
- Fork paperclip, clone locally, `pnpm install`, run dev server
- Postgres (Neon) provisioned, migrations applied
- Anthropic Claude API key configured, budget cap enforced at framework level
- Vercel project deployed with dummy homepage + admin route
- Basic auth on `/admin` (single password, env var)

### Non-functional
- Local `pnpm dev` starts in <60s
- Deploy via `git push` → Vercel auto-deploy <5min
- Cost: $0 (free tiers)

## Architecture
```
[Dev laptop] --git push--> [GitHub fork]
                                |
                                v
                          [Vercel deploy]
                                |
                                v
                   [Next.js app (paperclip UI)]
                         |             |
                         v             v
                    [Neon Postgres] [Claude API]
                                        |
                                        v
                              [Budget middleware $50/mo]
```

## Related Code Files
### To Create
- `.env.local` (local, gitignored) — Claude key, DB URL, admin pass
- `.env.example` — template
- `README.md` (project header)
- `docs/poc-overview.md` — 1-page context

### To Modify
- `package.json` — add any missing dev scripts
- paperclip config files (TBD after spike) — budget cap setting
- `vercel.json` — env var bindings

## Implementation Steps
1. **Day 1 — Spike (timeboxed 6h):** clone paperclip, read README + code layout, run locally, identify: scheduler, budget, agent definition, ticketing files. Write spike notes to `plans/260409-1420-paperclip-zero-human-company/reports/spike-paperclip-notes.md`. **Exit criteria:** if scheduler or budget system missing/broken → escalate, consider downscoping to 2 agents.
2. **Day 2 — Fork & local bootstrap:** fork on GitHub, clone, pnpm install, run `pnpm dev`, verify UI loads, create new branch `poc/zero-human-company`.
3. **Day 3 — Neon + Postgres:** provision Neon free tier, copy connection string, run paperclip migrations, verify tables.
4. **Day 4 — Vercel deploy:** connect Vercel to fork, bind env vars, deploy, verify public URL.
5. **Day 5 — Claude API + budget:** add Anthropic key, locate paperclip's budget module, set cap to `5000` cents ($50), add monthly reset logic if missing, write tiny test that mocks a 10-token call and verifies counter increments.
6. **Day 6 — Admin auth + smoke test:** single-password gate on `/admin`, manually create 1 test ticket via admin UI, verify persists in DB.
7. **Day 7 — Buffer/docs:** fix issues, commit clean, tag `v0.1-infra`, update plan status.

## Todo List
- [ ] Spike paperclip (timeboxed 6h, exit criteria documented)
- [ ] Fork + clone + local dev running
- [ ] Neon Postgres provisioned + migrated
- [ ] Vercel deploy live, public URL
- [ ] Claude API key wired
- [ ] Budget cap enforced + tested
- [ ] `/admin` password-gated
- [ ] Smoke test: create ticket via admin
- [ ] Spike notes committed
- [ ] `v0.1-infra` tag

## Success Criteria
- Public Vercel URL responds (even if homepage is skeleton)
- `pnpm dev` starts cleanly locally
- Admin panel reachable, protected by password
- Attempting to exceed budget in test throws `BudgetExceededError` (or equivalent)
- Git tag `v0.1-infra` pushed

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| paperclip scheduler is unstable | Med | High | Day 1 spike; exit plan = downscope to 2 agents or build minimal custom scheduler |
| Budget system missing in paperclip | Low-Med | High | Implement custom middleware wrapping Anthropic SDK calls |
| Neon free tier limits | Low | Low | Usage nowhere near limits; fallback = Supabase |
| Vercel env var mis-wire | Low | Med | Use `.env.example` as checklist |

## Security Considerations
- Never commit `.env.local`, Anthropic keys, or Neon URL
- Admin password via env var, not hardcoded
- Rate-limit admin login (even simple: 5 attempts/min)
- Claude API key stored only in Vercel env + `.env.local`
- Enable Vercel's deployment protection on preview URLs if paid tier; else accept public preview risk

## Next Steps
- Unblocks: phase-02 (can't define agents without runtime)
- Follow-up: document spike findings → inform phase-02 agent implementation style
