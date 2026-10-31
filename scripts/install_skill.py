#!/usr/bin/env python3
"""Install heige-claude-video skill for Claude Code / Codex.

Copies skills/heige-claude-video/ into the target skills directory.
No network access, no extra dependencies. Existing installs are left untouched.
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_SRC = REPO_ROOT / "skills" / "heige-claude-video"

TARGETS = {
    "claude": Path.home() / ".claude" / "skills" / "heige-claude-video",
    "codex": Path.home() / ".agents" / "skills" / "heige-claude-video",
}


def install(target: str) -> int:
    dest = TARGETS[target]
    if not SKILL_SRC.is_dir():
        print(f"错误：找不到技能源目录 {SKILL_SRC}", file=sys.stderr)
        return 2
    if dest.exists():
        print(f"跳过：{dest} 已存在，保留现有内容，不做覆盖。")
        print(f"如需重装，请先手动备份并删除该目录。")
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_SRC, dest)
    n = sum(1 for p in dest.rglob("*") if p.is_file())
    print(f"已安装到 {dest}（{n} 个文件）。")
    print("新开一个会话即可使用；调用示例：")
    print("  用 heige-claude-video 把这份稿子做成原理动画视频。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=[*TARGETS, "both"],
        required=True,
        help="安装目标：claude / codex / both",
    )
    args = parser.parse_args()

    targets = list(TARGETS) if args.target == "both" else [args.target]
    codes = [install(t) for t in targets]
    return max(codes) if codes else 0


if __name__ == "__main__":
    sys.exit(main())
