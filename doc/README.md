# pi-pdf-watermark 文档入口

English navigation, with the original Chinese text preserved below.

| Role | Location |
|------|----------|
| User guide | [../README.md](../README.md) (English) |
| 中文用户说明 | [../README-zh.md](../README-zh.md) |
| Agent boundary | [../AGENTS.md](../AGENTS.md) |
| Skill spec | [../skills/pdf-watermark/SKILL.md](../skills/pdf-watermark/SKILL.md) |
| Implementation | [../skills/pdf-watermark/references/watermark.py](../skills/pdf-watermark/references/watermark.py) |
| Evidence and history | [references/](./references/) |

**Contributing** — update the English `README.md` (npm default) and Chinese `README-zh.md` together. Record user-visible changes in `../CHANGELOG-zh.md` and translate them into `../CHANGELOG.md` when preparing each release. All four documents ship in the npm package. Verify with `python3 -m py_compile skills/pdf-watermark/references/watermark.py`. Committing, pushing, tagging and publishing require explicit maintainer approval.

---

本文件只做导航，不新写一套规格。各角色正文仍在原处：

| 角色 | 回答什么 | 位置 |
|---|---|---|
| 工程入口 | 功能、安装、用法、CLI 参数 | [../README.md](../README.md)（英文）、[../README-zh.md](../README-zh.md)（中文） |
| 协作规范 | 长期安全与交付边界、验证要求、文档与 Git 纪律 | [../AGENTS.md](../AGENTS.md) |
| Skill 规格 | 触发条件、交互流程、水印参数 | [../skills/pdf-watermark/SKILL.md](../skills/pdf-watermark/SKILL.md) |
| 现行实现 | 唯一可执行脚本（CLI 与调用共用） | [../skills/pdf-watermark/references/watermark.py](../skills/pdf-watermark/references/watermark.py) |
| 决策档案 | 难逆转决策刻碑 | 暂无独立档案；决策背景见 [references/](#证据与历史) 与 [../AGENTS.md](../AGENTS.md) |
| 执行状态 | 当前执行状态与接续位置 | 无（仓库未设 `PLAN.md`） |

`doc/references/` 只保存来源、验证记录与历史阶段快照，不是现行权威；现行机制、参数与安全边界以上表对应正文和现行实现为准。

## 证据与历史（`doc/references/`）

| 文件 | 内容 |
|---|---|
| [历史-SKILL内嵌脚本模板.md](./references/历史-SKILL内嵌脚本模板.md) | 原 `SKILL.md` 内嵌的脚本模板副本，已与现行实现漂移，仅作历史追溯 |
| [历史-文档沉淀出口三出口规范.md](./references/历史-文档沉淀出口三出口规范.md) | 旧 `AGENTS.md` 中「术语表 / 决策档案 / 经验笔记」三出口规范原文与相关提交记录 |

## 维护规则

- 参数、默认输出、字体选择、安全或安装行为变化 → 同步 [../README.md](../README.md) 与 [../README-zh.md](../README-zh.md) 以及 [../skills/pdf-watermark/SKILL.md](../skills/pdf-watermark/SKILL.md)。
- 安全边界与交付纪律变化 → 同步 [../AGENTS.md](../AGENTS.md)。
- 实现变化 → 只改 [../skills/pdf-watermark/references/watermark.py](../skills/pdf-watermark/references/watermark.py)，正文按上表对到它，不留并行副本。
- 历史快照只追加到 `doc/references/`，不改写其中原文。
- `README.md`（英文默认）与 `README-zh.md`（中文）在同一次提交中同步。日常把用户可感知的变化写入本仓 `../CHANGELOG-zh.md`，准备发布时按版本同步到英文 `../CHANGELOG.md`。四份文档都随 npm 包发布。
