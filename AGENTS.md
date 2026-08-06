# Ops Dashboard â€” Agent Guide

## What This Repo Is
Status dashboard generator for JPS systems. It queries GitHub Actions and service status sources, then writes a static `index.html` dashboard.

## Read First
1. `generate_dashboard.py`
2. `index.html`
3. `FAST_LANE_PROOF.md`

## Agent Lanes
- Shared repo truth lives in `README.md`, `AGENTS.md`, and real dashboard/runbook docs.
- Codex private scratch lives under `.codex/`.
- Claude private scratch lives under `.claude/`.
- Do not edit the other agent's private lane.
- Shared files should contain durable facts, not temporary analysis.

## Merge Lane
- Fast lane repo.
- Branch -> PR -> `codex-review` + `adversarial-review`.
- Auto-merge is allowed only after both checks pass.

## Hard Rules
- This repo reports status; it should not mutate live systems.
- Never invent a green state when data is stale, missing, or failed.
- Keep time displays consistent and human-readable in ET.
- Do not hardcode credentials, PATs, or service secrets.
- Do not add hidden outbound actions behind "dashboard refresh" behavior.

## Change Boundaries
- Safe: rendering, status labeling, stale-data handling, docs.
- Sensitive: auth, API targets, workflow files, any new live write behavior.

# JPS Engineering System Agent Instructions

For JPS repository work, this protocol is mandatory.

Before editing code, docs, config, automation, workflows, deployment files, or live-system behavior:

1. Use `C:\AI Workspaces\JPS\repo-hygiene\jps-engineering-system\jps-change.ps1 start` to create a registered branch and dedicated worktree.
2. Work only inside the printed worktree path.
3. Follow SysFlow, Agent Gauntlet, GateKeeper, PR review, merge, deployment, and cleanup requirements for the selected risk lane.
4. Stage only explicit paths. Never run `git add .` or `git add -A`.
5. Run `jps-preflight.ps1` before PR, push, merge handoff, or deployment handoff.
6. Production deploys require separate Norman approval and `jps-deploy-record.ps1`.
7. Cleanup requires `jps-cleanup.ps1`; do not delete branches or worktrees manually.

If any check fails, stop and fix the cause or record an approved exception. Do not route around the system.
