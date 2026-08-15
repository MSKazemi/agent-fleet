# Contributing

Thanks for looking. The bar is simple: **the self-test stays green and new
behaviour arrives with a check that proves it.**

```bash
./bin/selftest        # 52 checks, no browser or API key needed
./bin/selftest -v     # show each command as it runs
```

## Ground rules

- `libexec/fleet-queue` is python3 **stdlib only**. No dependencies, ever — the
  tool has to run on a machine you just SSH'd into.
- `bin/fleet` is bash. Keep it POSIX-ish and `bash -n` clean.
- Anything that touches the user's machine (memory, processes, windows) must
  degrade to a clear message rather than an obscure failure.
- Never make the tool type into a terminal. See the note in `bin/fleet`.
- A `done` in this system means evidence was observed. Do not weaken that.

## Good first issues

Look for `good first issue`. Ports of the launcher to other editors/terminals,
and better memory-cost estimates per platform, are especially welcome.
