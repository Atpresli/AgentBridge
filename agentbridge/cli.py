"""Minimal local-first AgentBridge CLI; standard library only."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".agentbridge")
TASKS = ROOT / "tasks.json"

def now():
    return datetime.now(timezone.utc).isoformat()

def load():
    if not TASKS.exists():
        raise SystemExit("Not initialized. Run: python3 -m agentbridge.cli init")
    return json.loads(TASKS.read_text(encoding="utf-8"))

def save(tasks):
    ROOT.mkdir(exist_ok=True)
    TASKS.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="AgentBridge local task queue")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    add = sub.add_parser("add")
    add.add_argument("title")
    sub.add_parser("list")
    handoff = sub.add_parser("handoff")
    handoff.add_argument("id", type=int)
    handoff.add_argument("--to", required=True)
    handoff.add_argument("--note", default="")
    args = parser.parse_args()

    if args.command == "init":
        if TASKS.exists():
            print("Already initialized; existing data preserved.")
        else:
            save([])
            print("Initialized .agentbridge/")
        return
    tasks = load()
    if args.command == "add":
        task = {"id": max((t["id"] for t in tasks), default=0) + 1,
                "title": args.title, "status": "open", "created_at": now()}
        tasks.append(task)
        save(tasks)
        print(f"Created task #{task['id']}: {task['title']}")
    elif args.command == "list":
        for task in tasks:
            print(f"#{task['id']} [{task['status']}] {task['title']}")
    elif args.command == "handoff":
        task = next((t for t in tasks if t["id"] == args.id), None)
        if task is None:
            raise SystemExit(f"Task #{args.id} not found")
        ROOT.joinpath("handoffs").mkdir(exist_ok=True)
        path = ROOT / "handoffs" / f"task-{args.id}-{len(list((ROOT / 'handoffs').glob(f'task-{args.id}-*.md'))) + 1}.md"
        path.write_text(
            f"# AgentBridge handoff\n\nTask: #{task['id']} — {task['title']}\n"
            f"Recipient: {args.to}\nCreated: {now()}\n"
            f"Status: {task['status']}\n\n## Instructions\n{args.note}\n",
            encoding="utf-8")
        print(f"Created {path} (not sent automatically)")

if __name__ == "__main__":
    main()
