#!/usr/bin/env python3
"""
Reset MCP config for mb_mcp_demo project in Claude Code.

Usage:
    python scripts/reset_mcp_config.py

This removes the project entry from ~/.claude.json, which will cause
Claude Code to re-prompt for project trust on next startup.
"""

import json
from pathlib import Path

CLAUDE_CONFIG = Path.home() / ".claude.json"
PROJECT_PATH = "/Users/houzongyue/cloud/github/mb_mcp_demo"


def main():
    if not CLAUDE_CONFIG.exists():
        print(f"Config file not found: {CLAUDE_CONFIG}")
        return

    with open(CLAUDE_CONFIG, "r") as f:
        data = json.load(f)

    if PROJECT_PATH in data.get("projects", {}):
        del data["projects"][PROJECT_PATH]
        with open(CLAUDE_CONFIG, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Deleted project entry: {PROJECT_PATH}")
    else:
        print("Project entry not found")


if __name__ == "__main__":
    main()
