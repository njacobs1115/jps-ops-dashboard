# JPS Engineering Controls Rollout

Ticket: JPS-924
Branch: ops/JPS-924-install-engineering-controls
Risk lane: critical
Repository risk: critical

## Purpose

Install the JPS Engineering System controls in jps-ops-dashboard.

The canonical package remains at:

C:\AI Workspaces\JPS\repo-hygiene\jps-engineering-system

## Scope

- .jps-repo.yml
- .github/pull_request_template.md
- .github/workflows/jps-hygiene.yml
- .github/workflows/adversarial-review.yml
- shared agent instruction block in AGENTS.md

## Intentionally Not Changed

- No app code changed.
- No API routes changed.
- No data schema changed.
- No production deployment is authorized by this PR.

## Verification

- git diff --check
- jps-preflight.ps1
- GitHub PR checks after push
- 2026-08-09 review fixes applied: workflow diff parsing hardened, protected-path coverage expanded, PR body evidence validation strengthened, added-line-only secret scanning added, Codex false-positive workflow normalized, and Pages/source deployment approval recorded before readying the PR.
- Existing adversarial protected-path gate updated to require exact-SHA protected-path review markers instead of blocking all protected-path changes without an approval path.
