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
- Production-coupled lane: every merge to `master` publishes GitHub Pages.
- Branch -> PR -> the required checks currently enforced on the exact head.
- No auto-merge. Stop once before merge because merge is the production-effect boundary; the bounded approval covers that merge and publication together.

## Hard Rules
- This repo reports status; it should not mutate live systems.
- Never invent a green state when data is stale, missing, or failed.
- Keep time displays consistent and human-readable in ET.
- Do not hardcode credentials, PATs, or service secrets.
- Do not add hidden outbound actions behind "dashboard refresh" behavior.

## Change Boundaries
- Safe: rendering, status labeling, stale-data handling, docs.
- Sensitive: auth, API targets, workflow files, any new live write behavior.

## Change Governance

- Canonical `CODING.md` owns risk classification, execution mode, approval, review, and production-effect boundaries.
- Preserve every repository-specific safety, data, scheduling, customer, and testing rule above.
- Use a clean topic branch/worktree when isolation is needed, stage explicit paths, and never run `git add .` or `git add -A`.
- Do not require SysFlow, Gauntlet, Gatekeeper, registered-worktree tooling, or repeated owner approval unless the validated risk/mode record contains the exact trigger.
- Required GitHub review checks on the exact PR head satisfy independent implementation review; do not duplicate them locally.
- Continue authorized internal stages automatically and never make Norman relay prompts between agents.
