# RETIRED / HISTORICAL — jps-ops-dashboard

**Status:** Retired 2026-09-26. Archived. Not a current JPS system.

**Superseded by:** Command Center Cockpit (`jps-command-center`, `/cockpit` and
`/api/cockpit/status` on the Hetzner Command Center). Use Cockpit for current
operational status.

This repository published a static status page to GitHub Pages
(`njacobs1115.github.io/jps-ops-dashboard/`). Its data froze on 2026-04-19, the
30-minute `update-dashboard.yml` updater failed from 2026-06-08, and GitHub
disabled its schedule for inactivity. At retirement the updater was disabled
and GitHub Pages publication was turned off.

The service list in `generate_dashboard.py` and `index.html` is stale
(it references retired Render, Make.com, and Route Optimizer endpoints). Do not
treat anything here as current system truth. Canonical repository status lives in
`njacobs1115/brain` → `REPOSITORIES.md`.
