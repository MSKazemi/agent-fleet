# Changelog

All notable changes to agent-fleet. Format follows [Keep a Changelog](https://keepachangelog.com/);
versions follow [SemVer](https://semver.org/).

## [0.2.1] - 2026-10-16

### Changed
- The PyPI distribution is named **`fleetq`** (`pipx install fleetq`): PyPI refuses `agent-fleet`
  because `agentfleet` already exists. The command is still `fleet`, and the repo, skill and plugin
  are still `agent-fleet`.
- Added `.github/workflows/release.yml`, a manual trusted-publishing (OIDC) workflow for PyPI.

## [0.2.0] - 2026-10-16

First tagged release.

### Added
- **Standalone terminal windows** — `fleet run --windows` opens one window per worker in
  gnome-terminal, kitty, alacritty, konsole, xfce4-terminal or xterm (`$FLEET_TERMINAL` picks one).
  Works on Wayland, needs no `xdotool`. `fleet run` now chooses visible terminals automatically
  (VS Code on X11, otherwise windows) and falls back to headless only with no display.
- `fleet run --vscode` to force VS Code terminals only.
- **A person in the loop** — `fleet run --ask` keeps workers interactive at a login, captcha, 2FA or
  question; `fleet unblock ID --answer "..."` appends your answer to the task's notes, and clearing a
  wall no longer counts as a failed attempt. `fleet blocked` shows how to answer each parked task.
- `AGENT_DIR` / `FLEET_WORKSPACE` — keep the queue under another name or below the repo root; the
  engine, launcher and ignore rule agree on where it is.
- `fleet --version`, a single `VERSION` source, and drift checks that keep `CITATION.cff` and the
  plugin manifests in step with it.
- **Packaging** — PyPI (`pipx install fleetq`, then `fleet install-skill`), a Claude Code plugin
  marketplace for the skill, and a release tarball with a SHA-256.
- Starter `TASKS.md` from `fleet init`; `checklist` / `checklist_user_marker` documented.
- Dispatch-flow diagram in the README.

### Changed
- The parallel lane is opt-in and collision-aware (was opt-out).
- Workers start as `claude --chrome`; the browser probe measures the mode workers actually run in.
- Self-test suite: 107 checks, no desktop alerts raised while it runs.

[0.2.1]: https://github.com/MSKazemi/agent-fleet/releases/tag/v0.2.1
[0.2.0]: https://github.com/MSKazemi/agent-fleet/releases/tag/v0.2.0
