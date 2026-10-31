#!/usr/bin/env python3
"""Install the skills in this repository for Claude Code / Codex.

Copies every skill under skills/ into the target skills directory:
- heige-claude-video      视频生产系统（本仓库原创）
- code-animation-prompts  风格提示词库（完整收录自
                          https://github.com/XiaoyeCodes/code-animation-prompts，
                          遵循其免费分享约定，来源与许可文件随目录保留）

No network access, no extra dependencies. Existing installs are left untouched.
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"

TARGETS = {
    "claude": Path.home() / ".claude" / "skills",
    "codex": Path.home() / ".agents" / "skills",
}


def install_one(skill_dir: Path, target_base: Path) -> int:
    dest = target_base / skill_dir.name
    if not skill_dir.is_dir():
        print(f"跳过：源目录不存在 {skill_dir}", file=sys.stderr)
        return 2
    if dest.exists():
        print(f"跳过：{dest} 已存在，保留现有内容，不做覆盖。")
        print("如需重装，请先手动备份并删除该目录。")
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_dir, dest)
    n = sum(1 for p in dest.rglob("*") if p.is_file())
    print(f"已安装 {skill_dir.name} → {dest}（{n} 个文件）。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=[*TARGETS, "both"],
        required=True,
        help="安装目标：claude / codex / both",
    )
    parser.add_argument(
        "--only",
        metavar="SKILL",
        action="append",
        help="只安装指定的技能目录名（可多次出现），默认安装 skills/ 下全部",
    )
    args = parser.parse_args()

    skill_dirs = sorted(p for p in SKILLS_ROOT.iterdir() if p.is_dir())
    if args.only:
        wanted = set(args.only)
        skill_dirs = [d for d in skill_dirs if d.name in wanted]
        if not skill_dirs:
            parser.error(f"skills/ 下找不到：{', '.join(sorted(wanted))}")

    targets = list(TARGETS) if args.target == "both" else [args.target]
    codes = [install_one(d, TARGETS[t]) for t in targets for d in skill_dirs]
    return max(codes) if codes else 0


if __name__ == "__main__":
    sys.exit(main())
