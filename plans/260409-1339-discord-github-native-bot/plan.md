---
title: "Discord GitHub-Native Bot (Python POC)"
description: "Discord bot that turns a chat message into a branch, Claude Code run, PR, and thread updates via GitHub webhooks."
status: pending
priority: P1
effort: 60h
branch: main
tags: [python, discord, claude-code, github, webhook, poc]
created: 2026-04-09
---

# Discord GitHub-Native Bot — Plan Overview

## Goal
User types `!fix <description>` in Discord → bot spawns a branch, runs Claude Code CLI, commits, pushes, opens PR, posts embed link in a thread. GitHub webhook feeds CI / review / merge status back into the same thread.

## Stack (locked)
- Python 3.11+, `discord.py` (or py-cord), `uv` or `poetry`
- `claude` CLI via subprocess (respects `ANTHROPIC_BASE_URL` env for user's proxy)
- Git ops: `GitPython` or raw `git` subprocess
- GitHub: `PyGithub` + `gh` CLI fallback
- Webhook receiver: `aiohttp` (shares event loop with discord.py)
- Tunnel: `smee.io` (primary) → polling fallback if down
- Persistence: single SQLite file (`tasks.db`) — no ORM, raw `sqlite3`

## Phases

| # | Phase | Effort | Milestone | Status |
|---|---|---|---|---|
| 01 | Bot Foundation & Claude Code Loop | ~30h (Week 1) | `v0.1-oneshot` — end-to-end: msg → branch → Claude → PR → link posted | pending |
| 02 | Webhook Feedback Loop & Polish | ~30h (Week 2) | `v1.0-demo` — CI/review/merge updates in thread + README + demo video | pending |

- [phase-01-bot-foundation-and-claude-code-loop.md](./phase-01-bot-foundation-and-claude-code-loop.md)
- [phase-02-webhook-feedback-loop-and-polish.md](./phase-02-webhook-feedback-loop-and-polish.md)

## Key Dependencies
- Existing Discord bot app + token (reused, no new app)
- GitHub PAT with `repo` scope (fine-grained, single target repo)
- Target test repo (user owns, non-production)
- `claude` CLI installed + authed against proxy
- `gh` CLI installed + authed
- smee.io channel URL (free, no account)

## Locked Decisions
1. Python, NOT Go (cc-connect is reference only — credit in README)
2. Local machine deploy, no public IP, outbound websocket + smee tunnel
3. Single repo scope for POC
4. 2-week strict deadline; Week 1 must demo a full one-shot flow
5. Stretch goals (reply-to-thread follow-up, approval reactions, `!status`) ONLY if phase 2 is ahead of schedule

## Top Risks (summary)
1. **Arbitrary code execution surface** → allowlist users + channels + workdirs (non-negotiable, phase 1)
2. **Claude CLI non-idempotent** → single-shot per task, store task state, no auto-retry
3. **Webhook infinite loop** (bot PR → webhook → bot post → webhook …) → filter events where sender == bot's own GitHub user

## Success Criteria
- One working demo video (≤3 min) showing full round-trip including a CI status update
- Zero secrets in git; `.env.example` provided
- Audit log file lists every Claude invocation with user, channel, prompt, branch, result
