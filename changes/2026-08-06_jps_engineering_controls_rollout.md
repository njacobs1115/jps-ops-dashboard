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
- Existing adversarial protected-path gate updated to require exact-SHA protected-path review markers instead of blocking all protected-path changes without an approval path.
