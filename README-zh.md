# pi-pdf-watermark

[English](./README.md) | 简体中文

[![pi-package](https://img.shields.io/badge/pi-package-skill-blue)](https://pi.dev/packages)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Pi Skill** —— 给 PDF 文件添加自定义文字水印。支持居中单字或整页平铺，可调角度、字号、透明度与颜色。

## ✨ 功能

- **两种水印模式**：居中单个印章，或整页平铺重复
- **完全可定制**：水印文字、旋转角度、字号、透明度、颜色
- **自动识别页面尺寸**：支持 A4、Letter 以及任意自定义尺寸
- **跨平台**：自动检测 macOS / Linux / Windows 上的中文字体
- **默认写入新文件**：未指定 `-o` 时写入 `原文件名_水印版.pdf`。当前脚本不会拦截指向输入文件的输出路径，也不是原子写入 —— 不要把 `-o` 指向输入文件或任何需要保留的文件

## 🚀 安装

```bash
# 通过 npm（推荐）
pi install npm:pi-pdf-watermark

# 或通过 GitHub
pi install git:github.com/ssdiwu/pi-pdf-watermark
```

## 📖 用法

安装后直接说：

> "给这个 PDF 打水印"

skill 会询问水印文字，然后生成带水印的 PDF。

### 示例

| 你说的 | 结果 |
|---|---|
| "给 report.pdf 打水印" | 询问文字 → 默认满铺模式 |
| "给 report.pdf 打上「机密」水印" | 直接执行，满铺 |
| "打一个居中的 30° 水印" | 使用居中模式，30° 角度 |

### 命令行（独立使用）

不通过 Pi 也可以直接运行 `watermark.py`：

```bash
# 安装依赖
pip3 install pypdf reportlab

# 基本用法（默认满铺）
python3 skills/pdf-watermark/references/watermark.py input.pdf "模力无限"

# 居中模式
python3 skills/pdf-watermark/references/watermark.py input.pdf "CONFIDENTIAL" --mode center --angle 30 --opacity 0.2

# 自定义字号与透明度
python3 skills/pdf-watermark/references/watermark.py input.pdf "DRAFT" --mode tile --font-size 36 --opacity 0.1

# 自定义输出路径
python3 skills/pdf-watermark/references/watermark.py input.pdf "内部资料" -o output.pdf
```

#### 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | *（必填）* | 输入 PDF 文件路径 |
| `text` | *（必填）* | 水印文字 |
| `--mode` | `tile` | `center`（居中单个）或 `tile`（满铺整页） |
| `--angle` | `45` | 旋转角度（度） |
| `--font-size` | `42` | 字号 |
| `--opacity` | `0.15` | 透明度（0–1） |
| `--output`, `-o` | `*_水印版.pdf` | 输出文件路径 |

## 🔧 工作原理

```
用户说「打水印」
       ↓
Skill 问：「请问要打什么水印文字？」
       ↓
用户回复：「模力无限」
       ↓
脚本以默认满铺模式运行 → 输出 *_水印版.pdf
```

**默认行为：**
- 模式：**满铺（tile）** —— 以 45° 覆盖整页
- 只询问**水印文字**，其余全部使用合理默认值
- 只有用户明确要求时才切换到**居中模式**

## 📦 依赖

- [pypdf](https://pypdf.readthedocs.io/) —— PDF 读取/写入
- [reportlab](https://www.reportlab.com/) —— PDF 生成（水印层）

通过 Pi 运行时会自动安装，也可手动安装：
```bash
pip3 install pypdf reportlab
```

## 🏗️ 包结构

```
pi-pdf-watermark/
├── package.json              # Pi manifest + npm 元数据
├── README.md                 # 英文说明（本文的英文版）
├── README-zh.md              # 中文说明（本文）
├── doc/README.md             # 文档入口（只做导航）
├── LICENSE                   # MIT 许可证
└── skills/
    └── pdf-watermark/
        ├── SKILL.md          # Skill 定义（Pi 读取）
        └── references/
            └── watermark.py   # 水印脚本（可直接当 CLI 用）
```

## 开发与验证

```bash
python3 -m py_compile skills/pdf-watermark/references/watermark.py
```

唯一实现是 `skills/pdf-watermark/references/watermark.py`；CLI 与 skill 调用同一份脚本，不要另存副本。行为变更还需用临时 PDF 验证居中/满铺、中文字体、透明度、旋转、错误输入以及输入输出同路径拒绝；检查页数与输出可打开。未做视觉检查必须明确说明。

## 文档与核心契约入口

| 入口 | 回答什么问题 |
|------|-------------|
| [`AGENTS.md`](./AGENTS.md) | Agent 边界：不可信 PDF 处理、同路径拒绝要求、验证、文档与 Git 纪律 |
| [`skills/pdf-watermark/SKILL.md`](./skills/pdf-watermark/SKILL.md) | 触发条件、交互流程与 skill 参数 |
| [`skills/pdf-watermark/references/watermark.py`](./skills/pdf-watermark/references/watermark.py) | 唯一可执行实现（CLI 与 skill 共用） |
| [`doc/README.md`](./doc/README.md) | 文档导航：现行正文、证据与历史 |
| [`doc/references/`](./doc/references/) | 来源、验证记录与历史快照 —— 不是现行权威 |

## 🤝 贡献

欢迎 PR！功能请求或 bug 请直接开 issue。

- 本 README 有两个语言版本：[`README.md`](./README.md)（英文）与 [`README-zh.md`](./README-zh.md)（中文）。改动请在同一次提交里更新两份，语义必须保持同步。
- 贡献与协作规则见 [`AGENTS.md`](./AGENTS.md) 与 [`doc/README.md`](./doc/README.md)。
- 日常用中文在本仓记录用户可感知的变化，准备发布时按版本同步英文。两份日志都随 npm 包发布，不倒填历史版本。[中文日志](./CHANGELOG-zh.md) · [英文日志](./CHANGELOG.md)
- 未获维护者明确批准，不执行 commit、push、tag 或 `npm publish`。

## 📄 许可证

[MIT](LICENSE) © ssdiwu
