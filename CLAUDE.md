# Claude Agent Entrypoint

Read `AGENTS.md` first and treat it as the controlling repo instruction file.

For any code, configuration, automation, deployment, or live-system work, follow the JPS engineering protocol:

- use a dedicated JPS change branch and worktree
- keep the change scoped to the approved ticket
- run SysFlow, Gauntlet, and Gatekeeper when the risk lane requires them
- open a PR and wait for required checks
- deploy only an approved merged SHA
- clean up the branch and worktree after merge/deployment verification

Do not work directly on the default branch. Do not stage unrelated files. Do not bypass the JPS hygiene scripts or GitHub required checks.
