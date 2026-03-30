#!/usr/bin/env python3
"""
JPS Ops Dashboard Generator
Queries GitHub Actions and Render services to produce a status dashboard.
Output: index.html (committed to repo, served by GitHub Pages)
"""

import os
import requests
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

# ── Config ─────────────────────────────────────────────────────────────────────
ET = ZoneInfo("America/New_York")
GH_PAT = os.environ.get("GH_PAT", "")
GH_OWNER = "njacobs1115"
GH_HEADERS = {
    "Authorization": f"Bearer {GH_PAT}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# ── Systems definition ─────────────────────────────────────────────────────────
# type: "github_actions" | "render_service" | "live_embed" | "make_scenario" | "on_demand"
SYSTEMS = [
    # ── Scheduled / GitHub Actions ──────────────────────────────────────────
    {
        "id": "pipeline_review",
        "name": "Pipeline Review",
        "category": "Scheduled",
        "type": "github_actions",
        "repo": "jps-daily-pipeline-review",
        "workflow": "nightly-review.yml",
        "schedule": "Mon–Fri ~7:30pm ET",
        "description": "Nightly GHL pipeline brief + next-morning texts",
        "logs_url": f"https://github.com/{GH_OWNER}/jps-daily-pipeline-review/actions",
    },
    {
        "id": "weekly_report",
        "name": "Weekly Marketing Report",
        "category": "Scheduled",
        "type": "github_actions",
        "repo": "jps-weekly-marketing-report",
        "workflow": "weekly-marketing-report.yml",
        "schedule": "Sundays 5pm ET",
        "description": "Leads, bookings, revenue, ads, GA4, GSC summary",
        "logs_url": f"https://github.com/{GH_OWNER}/jps-weekly-marketing-report/actions",
    },
    {
        "id": "marketing_intel",
        "name": "Marketing Intelligence",
        "category": "Scheduled",
        "type": "github_actions",
        "repo": "jps-marketing-intelligence",
        "workflow": "daily-intel.yml",
        "schedule": "Weekdays 7am ET",
        "description": "AI-powered anomaly detection across all channels",
        "logs_url": f"https://github.com/{GH_OWNER}/jps-marketing-intelligence/actions",
    },
    {
        "id": "ads_pruner",
        "name": "Ads Nightly Pruner",
        "category": "Scheduled",
        "type": "render_service",
        "health_url": "https://jps-ads-pruner.onrender.com/",
        "schedule": "Daily 6pm ET",
        "description": "Scans search terms, flags waste, emails approval batch",
        "logs_url": "https://jps-ads-pruner.onrender.com/",
    },
    # ── Live Services ────────────────────────────────────────────────────────
    {
        "id": "route_optimizer",
        "name": "Route Optimizer",
        "category": "Live Services",
        "type": "render_service",
        "health_url": "https://route-optimizer-jps.onrender.com/",
        "schedule": "Always on (paid Render)",
        "description": "Scheduling + booking engine — powers the funnel",
        "logs_url": "https://route-optimizer-jps.onrender.com/",
    },
    {
        "id": "booking_funnel",
        "name": "Booking Funnel",
        "category": "Live Services",
        "type": "live_embed",
        "health_url": "https://removemyoiltank.com/oil-tank-removal-cost",
        "schedule": "Always on (WordPress)",
        "description": "Customer-facing price estimator + booking flow",
        "logs_url": "https://removemyoiltank.com/oil-tank-removal-cost",
    },
    # ── Make.com Scenarios ───────────────────────────────────────────────────
    {
        "id": "make_booking",
        "name": "Booking Webhook (Make)",
        "category": "Make Scenarios",
        "type": "make_scenario",
        "scenario_id": "4603576",
        "schedule": "On booking submission",
        "description": "Receives booking → creates GHL contact",
        "logs_url": "https://www.make.com/en/scenarios/4603576",
    },
    {
        "id": "make_estimate",
        "name": "Estimate Email (Make)",
        "category": "Make Scenarios",
        "type": "make_scenario",
        "scenario_id": "4629605",
        "schedule": "On estimate request",
        "description": "Sends branded HTML estimate email via Gmail",
        "logs_url": "https://www.make.com/en/scenarios/4629605",
    },
    {
        "id": "make_social",
        "name": "Social Caption Generator (Make)",
        "category": "Make Scenarios",
        "type": "make_scenario",
        "scenario_id": "4630774",
        "schedule": "On new image in Drive",
        "description": "AI captions for before/after job photos (FB, IG, GBP)",
        "logs_url": "https://www.make.com/en/scenarios/4630774",
    },
    # ── On-Demand Tools ──────────────────────────────────────────────────────
    {
        "id": "permit_bot",
        "name": "Permit Bot",
        "category": "On-Demand",
        "type": "on_demand",
        "schedule": "Manual trigger",
        "description": "Auto-fills MA permit PDF from job data → emails PDF",
        "logs_url": f"https://github.com/{GH_OWNER}/jps-permit-bot",
    },
]

# ── Data fetchers ──────────────────────────────────────────────────────────────

def get_workflow_run(repo, workflow):
    """Fetch the latest GitHub Actions run for a workflow."""
    url = f"https://api.github.com/repos/{GH_OWNER}/{repo}/actions/workflows/{workflow}/runs"
    try:
        r = requests.get(url, headers=GH_HEADERS, params={"per_page": 1}, timeout=15)
        r.raise_for_status()
        runs = r.json().get("workflow_runs", [])
        if not runs:
            return {"conclusion": "never_run", "created_at": None, "html_url": None}
        run = runs[0]
        # conclusion is set on completion; status shows in-progress state
        conclusion = run.get("conclusion") or run.get("status") or "unknown"
        return {
            "conclusion": conclusion,
            "created_at": run.get("created_at"),
            "html_url": run.get("html_url"),
            "run_number": run.get("run_number"),
        }
    except Exception as e:
        return {"conclusion": "error", "error": str(e), "created_at": None, "html_url": None}


def check_http(url):
    """Ping an HTTP endpoint and return up/down."""
    try:
        r = requests.get(url, timeout=20, allow_redirects=True)
        return "up" if r.status_code < 500 else "down"
    except Exception:
        return "down"


# ── Formatters ─────────────────────────────────────────────────────────────────

def relative_time(iso_str):
    if not iso_str:
        return "Never"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        secs = (datetime.now(timezone.utc) - dt).total_seconds()
        if secs < 60:
            return "Just now"
        if secs < 3600:
            return f"{int(secs/60)}m ago"
        if secs < 86400:
            return f"{int(secs/3600)}h ago"
        return f"{int(secs/86400)}d ago"
    except Exception:
        return "—"


def et_time(iso_str):
    if not iso_str:
        return "—"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00")).astimezone(ET)
        return dt.strftime("%a %b %-d %-I:%M %p ET")
    except Exception:
        return iso_str


def status_badge(conclusion):
    mapping = {
        "success":     ("🟢", "SUCCESS",     "#22c55e"),
        "up":          ("🟢", "UP",           "#22c55e"),
        "failure":     ("🔴", "FAILED",       "#ef4444"),
        "down":        ("🔴", "DOWN",         "#ef4444"),
        "in_progress": ("🟡", "RUNNING",      "#eab308"),
        "queued":      ("🟡", "QUEUED",       "#eab308"),
        "cancelled":   ("⚫", "CANCELLED",    "#6b7280"),
        "skipped":     ("⚫", "SKIPPED",      "#6b7280"),
        "timed_out":   ("🔴", "TIMED OUT",    "#ef4444"),
        "never_run":   ("⚪", "NEVER RUN",    "#6b7280"),
        "manual":      ("⚪", "MANUAL",       "#6b7280"),
        "enabled":     ("🟢", "ENABLED",      "#22c55e"),
        "unknown":     ("🟡", "UNKNOWN",      "#eab308"),
        "error":       ("🔴", "ERROR",        "#ef4444"),
    }
    icon, label, color = mapping.get(conclusion, ("🟡", conclusion.upper(), "#eab308"))
    return icon, label, color


# ── Main ───────────────────────────────────────────────────────────────────────

def fetch_all_statuses():
    results = {}
    for s in SYSTEMS:
        sid = s["id"]
        stype = s["type"]

        if stype == "github_actions":
            run = get_workflow_run(s["repo"], s["workflow"])
            results[sid] = {
                "conclusion": run["conclusion"],
                "last_run_rel": relative_time(run.get("created_at")),
                "last_run_abs": et_time(run.get("created_at")),
                "run_url": run.get("html_url"),
            }

        elif stype == "render_service":
            status = check_http(s["health_url"])
            results[sid] = {
                "conclusion": status,
                "last_run_rel": "—",
                "last_run_abs": "Live service",
                "run_url": s["health_url"],
            }

        elif stype == "live_embed":
            status = check_http(s["health_url"])
            results[sid] = {
                "conclusion": status,
                "last_run_rel": "—",
                "last_run_abs": "Live embed",
                "run_url": s["health_url"],
            }

        elif stype == "make_scenario":
            # No API key available — show as enabled/available
            results[sid] = {
                "conclusion": "enabled",
                "last_run_rel": "—",
                "last_run_abs": "Event-driven",
                "run_url": s["logs_url"],
            }

        elif stype == "on_demand":
            results[sid] = {
                "conclusion": "manual",
                "last_run_rel": "—",
                "last_run_abs": "Manual trigger",
                "run_url": s["logs_url"],
            }

    return results


def render_html(statuses):
    now_et = datetime.now(ET).strftime("%a %b %-d %Y %-I:%M %p ET")

    categories = ["Scheduled", "Live Services", "Make Scenarios", "On-Demand"]

    cards_html = ""
    for cat in categories:
        cat_systems = [s for s in SYSTEMS if s["category"] == cat]
        if not cat_systems:
            continue

        cards_html += f'<div class="category-label">{cat}</div>\n<div class="grid">\n'

        for s in cat_systems:
            sid = s["id"]
            st = statuses.get(sid, {})
            conclusion = st.get("conclusion", "unknown")
            icon, label, color = status_badge(conclusion)
            last_rel = st.get("last_run_rel", "—")
            last_abs = st.get("last_run_abs", "—")
            run_url = st.get("run_url") or s["logs_url"]
            schedule = s["schedule"]
            desc = s["description"]
            logs_url = s["logs_url"]

            cards_html += f"""
<div class="card">
  <div class="card-header">
    <span class="card-name">{s["name"]}</span>
    <span class="badge" style="background:{color}22; color:{color}; border:1px solid {color}44;">
      {icon} {label}
    </span>
  </div>
  <div class="card-desc">{desc}</div>
  <div class="card-meta">
    <div class="meta-row"><span class="meta-key">Schedule</span><span class="meta-val">{schedule}</span></div>
    <div class="meta-row"><span class="meta-key">Last run</span><span class="meta-val">{last_abs} <span class="dim">({last_rel})</span></span></div>
  </div>
  <div class="card-footer">
    <a href="{logs_url}" target="_blank" class="link-btn">View logs →</a>
  </div>
</div>
"""

        cards_html += "</div>\n"

    # summary counts
    total = len(SYSTEMS)
    green = sum(1 for s in SYSTEMS if statuses.get(s["id"], {}).get("conclusion") in ("success", "up", "enabled"))
    red = sum(1 for s in SYSTEMS if statuses.get(s["id"], {}).get("conclusion") in ("failure", "down", "error", "timed_out"))
    neutral = total - green - red

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>JPS Ops Dashboard</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0a0a0a;
      color: #e5e7eb;
      min-height: 100vh;
      padding: 32px 24px 64px;
    }}

    .header {{
      max-width: 1100px;
      margin: 0 auto 32px;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .header-left h1 {{
      font-size: 22px;
      font-weight: 700;
      color: #f9fafb;
      letter-spacing: -0.3px;
    }}

    .header-left p {{
      font-size: 13px;
      color: #6b7280;
      margin-top: 4px;
    }}

    .summary {{
      display: flex;
      gap: 16px;
      align-items: center;
    }}

    .summary-chip {{
      font-size: 12px;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 9999px;
    }}

    .chip-green {{ background: #22c55e22; color: #22c55e; border: 1px solid #22c55e44; }}
    .chip-red   {{ background: #ef444422; color: #ef4444; border: 1px solid #ef444444; }}
    .chip-gray  {{ background: #6b728022; color: #9ca3af; border: 1px solid #6b728044; }}

    .updated {{
      font-size: 12px;
      color: #4b5563;
      margin-top: 8px;
    }}

    .content {{ max-width: 1100px; margin: 0 auto; }}

    .category-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #4b5563;
      margin: 32px 0 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #1f2937;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 12px;
    }}

    .card {{
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: border-color 0.15s;
    }}

    .card:hover {{ border-color: #374151; }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    .card-name {{
      font-size: 14px;
      font-weight: 600;
      color: #f3f4f6;
    }}

    .badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 9999px;
      white-space: nowrap;
    }}

    .card-desc {{
      font-size: 12px;
      color: #6b7280;
      line-height: 1.5;
    }}

    .card-meta {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 12px;
    }}

    .meta-row {{
      display: flex;
      gap: 8px;
    }}

    .meta-key {{
      color: #4b5563;
      min-width: 64px;
      font-weight: 500;
    }}

    .meta-val {{ color: #d1d5db; }}
    .dim {{ color: #4b5563; }}

    .card-footer {{ margin-top: 4px; }}

    .link-btn {{
      font-size: 12px;
      color: #6b7280;
      text-decoration: none;
      transition: color 0.15s;
    }}

    .link-btn:hover {{ color: #9ca3af; }}

    @media (max-width: 600px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .header {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="header-left">
      <h1>JPS Ops Dashboard</h1>
      <p>RemoveMyOilTank.com · All systems</p>
      <p class="updated">Updated {now_et} · Auto-refreshes every 30 min</p>
    </div>
    <div class="summary">
      <span class="summary-chip chip-green">🟢 {green} OK</span>
      {"<span class='summary-chip chip-red'>🔴 " + str(red) + " Failed</span>" if red else ""}
      <span class="summary-chip chip-gray">⚪ {neutral} Neutral</span>
    </div>
  </div>

  <div class="content">
{cards_html}
  </div>
</body>
</html>"""


if __name__ == "__main__":
    print("Fetching system statuses...")
    statuses = fetch_all_statuses()

    for s in SYSTEMS:
        sid = s["id"]
        st = statuses.get(sid, {})
        print(f"  {s['name']}: {st.get('conclusion', '?')}")

    html = render_html(statuses)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nDashboard written to index.html ({len(html):,} bytes)")
