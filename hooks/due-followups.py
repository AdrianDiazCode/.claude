#!/usr/bin/env python3
"""SessionStart hook: print the follow-ups whose date has arrived.

Usage: due-followups.py <checklist.md>

Reads a markdown checklist of lines shaped `- [ ] YYYY-MM-DD  text` and
emits Claude Code hook JSON. Unchecked items dated today or earlier become a
systemMessage (shown to the user) and additionalContext (seen by Claude, so it
can offer to act on them). Nothing is printed when nothing is due, so quiet
sessions stay quiet. Never fails the session: any problem exits 0 silently.
"""
import datetime
import json
import re
import sys

LINE = re.compile(r"^- \[( |x|X)\] (\d{4}-\d{2}-\d{2})\s+(.*\S)\s*$")


def main() -> int:
    if len(sys.argv) < 2:
        return 0
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return 0

    today = datetime.date.today().isoformat()
    due, upcoming = [], 0
    for line in lines:
        m = LINE.match(line)
        if not m or m.group(1).lower() == "x":
            continue
        date, text = m.group(2), m.group(3)
        if date <= today:
            due.append((date, text))
        else:
            upcoming += 1

    if not due:
        return 0

    due.sort()
    bullets = "\n".join(f"  • [{d}] {t}" for d, t in due)
    headline = f"{len(due)} security follow-up{'s' if len(due) != 1 else ''} due"
    if upcoming:
        headline += f" ({upcoming} more scheduled later)"
    message = f"{headline}:\n{bullets}\n  List: {sys.argv[1]}"

    print(json.dumps({
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "Security follow-ups due today (from the incident checklist at "
                f"{sys.argv[1]}). Mention them briefly and offer to act; when one "
                "is done, tick it [x] in that file, or move a recurring item's "
                f"date forward.\n{bullets}"
            ),
        },
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
