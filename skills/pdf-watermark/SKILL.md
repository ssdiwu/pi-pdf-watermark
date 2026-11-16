---
name: pdf-watermark
description: "PDF 水印工具：给 PDF 文件添加文字水印。当用户提到「打水印」「加水印」「PDF 水印」「给 PDF 加标记」「满铺水印」「斜体水印」等关键词时触发。支持居中单字水印和整页平铺重复水印，可自定义文字、角度、字号、透明度、颜色、模式等参数。"
---

# PDF Watermark

给 PDF 文件添加自定义文字水印。

## 交互流程（必须遵守）

**默认模式：满铺整页（tile）。**

用户说「打水印」时：
1. **如果用户没有给出水印文字** → 必须先询问：
   > 请问要打什么水印文字？
2. **如果用户一句话中同时给了文件和文字**（例如「给这个 PDF 打上"机密"水印」）→ 直接执行，默认满铺。
3. **用户明确要求居中模式**时才用 `center`，否则一律 `tile` 满铺。

收到文字回复后，使用默认满铺模式执行加水印操作。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `text` | （必填，需向用户确认） | 水印文字 |
| `mode` | `tile`（默认，无需询问） | 水印模式：`center`（居中单个） / `tile`（满铺整页）。**默认满铺，用户明确要求居中时才用 center** |
| `angle` | `45` | 旋转角度（度） |
| `font_size` | `42` | 字号（tile 模式） / `48`（center 模式） |
| `opacity` | `0.15` | 透明度 0~1，越小越淡 |
| `color` | `(0.55, 0.55, 0.55)` | RGB 颜色三元组 |
| `output` | 自动在原文件名后加 `_水印版` | 输出文件路径 |

## 执行方式

唯一实现是 [`references/watermark.py`](references/watermark.py)，直接运行，不要再复制一份脚本：

```bash
python3 skills/pdf-watermark/references/watermark.py <输入.pdf> "<水印文字>" [--mode center|tile] [--angle 45] [--font-size 42] [--opacity 0.15] [-o 输出.pdf]
```

脚本会自动检测系统中文字体（macOS / Linux / Windows 常见路径，找不到时回退 `fc-list`）并按每页尺寸生成水印。

`color` 目前固定为 `(0.55, 0.55, 0.55)`，命令行未暴露该参数，需要改色时在代码里调用 `add_watermark(..., color=...)`。

原先内嵌在本文的脚本模板已与现行实现漂移，移到 [`doc/references/历史-SKILL内嵌脚本模板.md`](../../doc/references/历史-SKILL内嵌脚本模板.md)，仅作历史追溯，不要照它执行。

## 注意事项

1. **依赖安装**：需要 `pypdf` 和 `reportlab`，缺失时自动安装：
   ```bash
   pip3 install pypdf reportlab --break-system-packages
   ```
2. **字体**：脚本内置 macOS/Linux/Windows 常见中文字体检测，跨平台兼容。
3. **默认输出为新文件**：未指定输出时写到 `原文件名_水印版.pdf`。但脚本不会拦截显式指定的输入输出同路径，也不是原子写入；调用前先比较真实路径，相同则不要执行。
4. **大文件处理**：百页以上 PDF 可能较慢，属正常现象。
