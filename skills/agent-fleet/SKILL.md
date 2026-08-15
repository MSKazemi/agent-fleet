---
name: agent-fleet
description: Run many Claude Code sessions in parallel against one shared task queue, in any project — bulk web work, migrations, audits, research, anything with a list. The number of terminals comes from the queue instead of being guessed, work that needs no browser gets no terminal, and anything needing a human (login, captcha, 2FA) is parked with a reason instead of stalling the run. Triggers — "set up the fleet here", "fleet init", "queue these tasks", "run these in parallel", "run the fleet", "how many terminals do I need", "what is blocked", "open N terminals", "start N agents", "spawn parallel claude sessions", "work the queue", "claim the next task", "run the worker loop", "promote my checklist into the queue".
---

# agent-fleet

Two audiences. Route first:

**Are you a worker?** If `$AGENT_ID` is set, or your prompt says you are `agent-N`
in a fleet: read `references/worker-protocol.md` now and follow it exactly.
Nothing else on this page applies to you.

**Otherwise you are the orchestrator** — helping queue work, size the run, and
clear blockers. Read on. `fleet help` lists every subcommand; this page carries
the judgement the help text cannot.

## Set up a project

```bash
cd ~/any/project && fleet init     # queue + git exclude rule
fleet where                        # which project's queue is in scope
fleet doctor                       # can anything leak; is the work runnable
fleet probe-browser                # can a worker actually open a Chrome tab
```

Run `probe-browser` once per machine before the first browser lane. A worker does
**not** inherit the Chrome connection of the session you type in, and a worker
without it blocks every browser task instead of doing it. `fleet doctor` reports
the last probe; with no probe on file it says the answer is unknown rather than
assuming one.

The queue resolves from **where you are**: `$AGENT_ROOT`, else the nearest
ancestor holding `.agents/`, else the git root, else `$PWD`. Every project keeps
an independent queue, and several fleets can run at once without seeing each
other's work.

## Queue work

```bash
fleet add "https://example.com/form/12" --title "vendor form" --priority 2
fleet add "summarise the three RFCs into a table" --kind research
fleet add "regenerate the API docs" --serial
cat urls.txt | fleet add-batch -            # 'URL | title | note' per line
fleet from-note                             # from TASKS.md / BACKLOG.md / TODO.md
```

A task is a URL or a sentence. `--kind` is your own label — the worker reads it
and the config can route it. `--priority 1` runs first, `5` is the default.

**From a checklist.** `fleet from-note` reads the markdown checklist the project
already keeps (`TASKS.md`, `BACKLOG.md`, `TODO.md`, or `"checklist"` in
`.agents/config.json`), taking unchecked items from any NOW / READY / TODO
section. Markers carry over: `⇉` parallel, `⇒` serial, `!!`/`!` raise priority,
`~` lowers it. `?`, `🔒`, `-x` and ticked items are never queued — a `?` is a
decision for the human, not an agent. Sub-steps indented under an item travel
with it as `notes`. `fleet to-note` ticks what finished with evidence and appends
one `## LOG` line; it never deletes or reorders anything a human wrote.

## Three lanes — only one costs a terminal

A terminal exists to hold a browser tab. Anything else is cheaper without one.

| Lane | Runs as | Terminal |
|---|---|---|
| `browser` | own Chrome tab, own agent session | yes, one per concurrent worker |
| `agent` | in-session subagent | no |
| `serial` | one at a time, in this session | no |

Inferred at `add` time — a live URL, or a kind listed in `browser_kinds`, means
`browser`; anything else means `agent`. `--exec` and `--serial` override.

```bash
fleet plan            # the schedule: lanes, terminals, and why it is capped
fleet run             # start the browser lane
fleet run 6           # override the count
fleet run --headless  # detached workers logging to .agents/logs (no X11 needed)
fleet run --dry       # show or write what would start, start nothing
```

Terminals = `min(browser tasks, max_workers, distinct sites)`. The site term is
deliberate: several workers against one host is a rate-limit ban, not more speed.
Tune `max_workers` in `.agents/config.json` or pass `--max`.

`fleet run` uses VS Code terminals when X11 and `xdotool` are available, and falls
back to detached processes otherwise, announcing which it chose. `--terminals` and
`--headless` force either.

**When `plan` says 0 terminals, open none.** `fleet run` refuses and points at the
in-session path — the fast route, not a fallback:

```bash
fleet claim orchestrator --exec agent    # then hand it to a subagent
fleet claim orchestrator --exec serial   # one at a time, in order
```

Run the agent lane by claiming and dispatching to subagents (up to
`max_subagents`, default 6), reporting each with `fleet done/block/fail` exactly
as a terminal worker would. **The quality bar is identical in every lane:**
evidence in `--result`, never a `done` without proof.

## Skills follow the work

Claude resolves skills from the working directory, so work whose skills live in
another repo must start there. Configure it once; never move the queue for it:

```json
{ "workers_start_in_by_kind": { "apply": "~/work/profile-repo" } }
```

The worker starts in that directory while `$AGENT_ROOT` keeps it on this
project's queue. `fleet doctor` fails only if a configured directory is missing.

## While it runs

```bash
fleet status / watch / list
fleet blocked          # what needs a human, grouped by reason
fleet unblock --all    # after the logins / captchas are cleared
fleet reset            # recover tasks from an agent that died
```

Workers never interrupt: a login wall, captcha, 2FA prompt or an unanswerable
question becomes a `blocked` task with a precise reason and a desktop
notification, and the worker takes the next task. Clearing blockers in batches is
the intended rhythm.

## Nothing leaks into the host project

`.agents/` and `.vscode/tasks.json` are excluded through `.git/info/exclude` —
per-clone, never committed, so the project's tracked files including its
`.gitignore` are untouched. A `tasks.json` the project commits is left tracked and
merged into, and `fleet clean` restores it. Artifacts already in committed history
are reported, never rewritten: that needs `git filter-repo` and a force-push,
which is the user's call per repo.

## Never type into a terminal

`xdotool type` is banned in this tool. Synthetic keystrokes go to whatever holds
keyboard focus inside VS Code, which is *not* reliably the terminal just created:
in testing the text landed in a running Claude session's prompt and was submitted
as user input. Terminals are created with a keystroke; commands are started only
by VS Code tasks or as detached processes.

## Requirements

`python3` for everything; X11 + `xdotool` only for the terminal path (focus is
taken briefly), `notify-send` for blocked alerts. `fleet doctor` and `bin/selftest`
(70 checks, no browser needed) report what is missing instead of failing
obscurely — run the self-test after changing the tool.
