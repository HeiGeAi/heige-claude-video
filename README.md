# heige-claude-video

**用 Claude Code 日更 AI 科普视频的完整生产系统，外加一套 341 种代码动画风格提示词库。**

给它一句选题或一段口播稿，它按固定生产线走完文案、配音、逐词卡点、原理动画、质检、封面和发布文案，产出一条 16:9 成片。这套流程来自个人 IP「问问黑哥」的真实日更实践（每天一条，持续更新中），不是理论方案。

仓库分两部分：

| 部分 | 是什么 | 来源 |
|---|---|---|
| `skills/heige-claude-video/` | 视频生产系统：方法、规范、自查清单、全流程规则 | 本仓库原创 |
| `skills/code-animation-prompts/` | 风格提示词库：341 种风格提示词、193 张参考静帧、离线挑选器、HTML 渲染工具 | 完整收录自 [XiaoyeCodes/code-animation-prompts](https://github.com/XiaoyeCodes/code-animation-prompts)（原始素材整理者：B 站 俯仰观照 等），来源与许可文件随目录保留 |

两者配合使用：生产系统决定「怎么做出一条合格的视频」，风格库提供「这一段想要什么画面质感」的参考。风格库按编号选型，画一段 12 秒的风格动画；生产系统管整条片的流程和验收。

## 为什么做这个

做 AI 科普视频，最难的从来不是某一帧画面，而是这三件事：

1. **日更。** 每天一条，靠灵感必死，靠流程才活。
2. **小白看得懂，光听也懂。** 画面只负责让观众更快懂，信息必须在口播里完整交代。
3. **AI 味。** 模板化的画面、念稿式的配音、随时穿帮的字幕，观众一秒划走。

这套系统的答案是：把整条生产线交给 Claude Code，并且**只沉淀流程，不沉淀画面**。每一集的画面按本集内容从零设计；真正可复用的资产是流程本身（配音、回读、时间轴、卡点、质检、合规）。

## 核心设计

这几条原则撑起整个系统，每一条都是实际踩坑踩出来的：

- **音频是时钟。** 稿子逐句配音后用 whisper 回读，和原稿逐字对齐生成词级时间戳；所有动画（关键词点亮、数字滚动、场景切换）都卡在字上，误差不超过 0.1 秒。画面卡的是稿子原文，不受语音识别听错影响。
- **回读挑最准。** 每句配音用 whisper 回读打分，低于阈值的句子换种子重新生成再挑最准的一版；外面再包一层大模型逐句复核，专抓「整段没念出来」「系统性读错」这类回读分数查不出的问题。
- **获得物先行。** 每条视频开头 10 秒讲明看完能拿走什么：免费开源项目、可照做的清单、可核实的数字。没有获得物的选题不进出片。
- **只听也懂。** 屏幕上出现的提示词、清单、对话原文，口播里都要说出来；引用谁的话先交代是谁说的。闭眼听一遍全片，是交付前的固定关卡。
- **视觉动效替代音效。** 成片只有人声和背景音乐两层声音。原来卡音效的位置（揭晓、数字、对比、警告、转场）全部改用视觉强调动效：冲击缩放、计数滚动、分屏对比、红色呼吸、运动模糊。两个声音叠在一起观感很差，这是实测结论。
- **不看图不交付。** 拼图、单帧、花屏扫描、碎片帧检测、成片回读，机器自查加人工看图，至少两轮；改完模板必须和基准片做全片逐帧 PSNR，不能只抽查改动的那一段。
- **合规先于一切。** 不写绝对化用语，不引导站外搜索，数字带来源，原创声明和「含 AI 生成内容」声明按平台规则勾选，发布前跑合规扫描。

## 快速开始

需要 Git 和 Python 3.10+。

```bash
git clone https://github.com/HeiGeAi/heige-claude-video.git
cd heige-claude-video

# 安装全部技能（生产系统 + 风格库）给 Claude Code
python scripts/install_skill.py --target claude

# 或安装给 Codex
python scripts/install_skill.py --target codex

# 两者都装
python scripts/install_skill.py --target both

# 只装其中一个
python scripts/install_skill.py --target claude --only heige-claude-video
python scripts/install_skill.py --target claude --only code-animation-prompts
```

安装脚本只复制 `skills/` 下的技能目录到对应技能目录，不下载任何依赖，已有同名技能时会停下并保留现有内容。

## 装好以后，直接这样说

```text
# 生产系统
用 heige-claude-video 把这份稿子做成原理动画视频，逐词卡点，出三张封面和发布文案。

用 heige-claude-video 讲清楚「Token 到底是什么」，2.5 到 3.5 分钟，
要有获得物，开头 10 秒讲明看完能得到什么。

# 风格库（按编号选风格做单段动画）
用 code-animation-prompts 用 B3 粒子聚形做一段 12 秒横屏动画，
主题是「把想法变成现实」，1920×1080，30fps，带中文字幕，无声。

# 两者配合
用 code-animation-prompts 帮我挑 3 个适合讲「AI 为什么会胡说八道」的风格，
再用 heige-claude-video 的规范做成整条片子。
```

视频本体由你自己的渲染管线（推荐 Remotion）实现，本仓库提供方法、规范、自查清单和全流程规则；不自动发布。

## 仓库结构

```text
heige-claude-video/
├── README.md
├── LICENSE                               # MIT，只覆盖本仓库原创部分
├── docs/
│   ├── SHOWCASE.md
│   ├── code-animation-prompts-LICENSE.md # 收录部分的来源与使用约定
│   └── code-animation-prompts-README.md  # 收录部分的完整说明
├── scripts/
│   └── install_skill.py                  # 安装器（claude / codex / both）
└── skills/
    ├── heige-claude-video/               # 视频生产系统（原创）
    │   ├── SKILL.md
    │   └── references/
    │       ├── production-pipeline.md    # 出片全流程
    │       ├── writing-rules.md          # 口播稿硬规则
    │       ├── animation-system.md       # 视觉系统
    │       ├── animation-techniques.md   # 动效技法库
    │       ├── qa-and-delivery.md        # 质检与交付
    │       └── compliance.md             # 合规红线
    └── code-animation-prompts/           # 风格提示词库（收录）
        ├── SKILL.md                      # 按编号选型、渲染接口、交付验收
        ├── assets/library/               # 341 份提示词、193 张静帧、风格挑选.html
        ├── references/                   # 风格索引、渲染与来源说明
        └── scripts/                      # styles.py 检索、render_video.py 导出
```

## 方法论地图（生产系统）

| 想解决什么 | 看哪篇 |
|---|---|
| 一条视频从选题到发布的完整路径 | production-pipeline.md |
| 稿子怎么写才有获得感、不像 AI 念的 | writing-rules.md |
| 画面规范：为什么这样排布、字幕怎么卡字 | animation-system.md |
| 揭晓、数字、对比这些时刻怎么用动效强调 | animation-techniques.md |
| 渲染完怎么证明它没有坏帧、没有穿帮 | qa-and-delivery.md |
| 什么词不能写、发布前查什么 | compliance.md |

风格库的用法看它自带的 `skills/code-animation-prompts/SKILL.md` 和 `docs/code-animation-prompts-README.md`。

## 实际效果

用这套流程产出的视频在抖音、B站、小红书、视频号日更更新（IP：问问黑哥）。样片截图和工程示例会陆续补充进 `docs/`。

## 收录说明与致谢

- `skills/code-animation-prompts/` 目录为完整收录，未做内容修改；收录自 [XiaoyeCodes/code-animation-prompts](https://github.com/XiaoyeCodes/code-animation-prompts)（commit 69ccbea，2026-10-29）。该仓库在原始素材基础上做了技能封装、工具脚本和文档；原始素材整理者是 B 站 UP 主 **俯仰观照**，另含 **LemoLab（Lemo-Opuscar）**、**Vincentwei1021（mg-styles-15）**、**Bae-ChangHyun（code-video）** 的第三方风格集。
- 收录部分**不适用本仓库的 MIT**，继续遵循其自带约定：免费使用、免费分享，请勿包装成付费课程、付费 skills 或其他收费内容出售；第三方风格集继续适用其各自许可。详见 `docs/code-animation-prompts-LICENSE.md` 和库内 `assets/library/许可与来源.md`、`assets/library/第三方许可/`。
- 本仓库不把收录素材重新声明为自己的原创；`skills/heige-claude-video/` 下的生产系统文档为原创，适用 MIT。

## License

本仓库原创部分（生产系统文档、安装脚本）采用 MIT。收录的风格库部分沿用其自带许可，见上方收录说明。
