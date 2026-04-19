# Ops Dashboard — Agent Guide

## What This Repo Is
Status dashboard generator for JPS systems. It queries GitHub Actions and service status sources, then writes a static `index.html` dashboard.

## Read First
1. `generate_dashboard.py`
2. `index.html`
3. `FAST_LANE_PROOF.md`

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
