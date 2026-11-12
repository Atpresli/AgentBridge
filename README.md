# AgentBridge

**Open-source, local-first coordination for AI coding agents.**

AgentBridge is a standalone project for managing tasks and generating portable handoffs between coding assistants.

## Current status
Early prototype. The CLI can store tasks and create handoff Markdown files. **It does not yet connect to, launch, or control Claude Code or Codex.**

## Quick start
Python 3.10+; no third-party dependencies.

```bash
python3 -m agentbridge.cli init
python3 -m agentbridge.cli add "Draft documentation"
python3 -m agentbridge.cli list
python3 -m agentbridge.cli handoff 1 --to codex --note "Please draft documentation"
```

Task data and handoffs stay in `.agentbridge/` in your current directory, excluded from Git by default. Handoffs are generated locally, **not sent automatically**.

## Design principles
- Local-first and free to run
- No required cloud account or API keys
- No connections to unrelated repositories, infrastructure, or credentials
- Future agent execution will require explicit opt-in and scoped permissions
- Clear activity logs and human approval gates

## Roadmap
- [x] Local task queue and handoff file generator
- [ ] Unit tests and continuous integration
- [ ] Read-only web dashboard
- [ ] Explicitly authorized Claude Code and Codex adapters
- [ ] Usage reporting and approval controls

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under MIT.
