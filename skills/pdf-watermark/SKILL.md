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

将以下脚本写入临时文件后用 `python3` 执行，或直接通过 `exec()` 方式内联运行。脚本会自动检测系统字体并适配每页尺寸。

### 脚本模板

```python
import io, math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

# ============ 用户参数（由 agent 根据用户需求填写）============
TEXT = "模力无限"       # 水印文字
MODE = "tile"            # "center" 或 "tile"
ANGLE = 45               # 旋转角度
FONT_SIZE = 42           # 字号
OPACITY = 0.15           # 透明度 0~1
COLOR = (0.55, 0.55, 0.55)  # RGB
SRC = "/path/to/input.pdf"   # 输入文件（agent 填写实际路径）
DST = None                   # 输出文件（None 则自动加 _水印版 后缀）
# ==============================================================

def find_chinese_font():
    """自动检测系统中可用的中文字体"""
    candidates = [
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        # Linux
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        # Windows (常见路径)
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    import subprocess
    for fp in candidates:
        try:
            pdfmetrics.registerFont(TTFont("ChineseFont", fp))
            return fp
        except Exception:
            continue
    # 尝试 fc-list 查找
    try:
        result = subprocess.run(
            ["fc-list", ":lang=zh", "-f", "%{file}\n"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                try:
                    pdfmetrics.registerFont(TTFont("ChineseFont", line.strip()))
                    return line.strip()
                except Exception:
                    continue
    except Exception:
        pass
    raise RuntimeError("未找到可用的中文字体，请安装中文字体包（如 fonts-wqy-zenhei）")

def create_watermark_page(w, h):
    """生成一页水印"""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(w, h))
    c.setFillColor(Color(*COLOR, alpha=OPACITY))
    c.setFont("ChineseFont", FONT_SIZE)

    if MODE == "center":
        # 居中单个水印
        c.saveState()
        c.translate(w / 2, h / 2)
        c.rotate(ANGLE)
        c.drawCentredString(0, 0, TEXT)
        c.restoreState()
    else:
        # tile 满铺模式
        text_width = FONT_SIZE * len(TEXT) * 1.0
        text_height = FONT_SIZE * 1.4
        step_x = text_width + 80
        step_y = text_height + 100
        diag = math.sqrt(w**2 + h**2)
        rows = int((diag * 2) // step_y) + 2
        cols = int((diag * 2) // step_x) + 2

        c.saveState()
        c.translate(w / 2, h / 2)
        c.rotate(ANGLE)
        start_x = -diag
        start_y = -diag
        for row in range(int(rows)):
            for col in range(int(cols)):
                x = start_x + col * step_x
                y = start_y + row * step_y
                c.drawCentredString(x, y, TEXT)
        c.restoreState()

    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

# 主流程
find_chinese_font()

if DST is None:
    import os
    base, ext = os.path.splitext(SRC)
    DST = f"{base}_水印版{ext}"

reader = PdfReader(SRC)
writer = PdfWriter()

for page in reader.pages:
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)
    wm_page = create_watermark_page(w, h)
    page.merge_page(wm_page)
    writer.add_page(page)

with open(DST, "wb") as f:
    writer.write(f)

print(f"✅ 水印添加完成！")
print(f"   输出: {DST}")
print(f"   文字: 「{TEXT}」| 模式: {MODE} | 角度: {ANGLE}° | 字号: {FONT_SIZE} | 透明度: {OPACITY}")
print(f"   页数: {len(reader.pages)}")
```

## 注意事项

1. **依赖安装**：需要 `pypdf` 和 `reportlab`，缺失时自动安装：
   ```bash
   pip3 install pypdf reportlab --break-system-packages
   ```
2. **字体**：脚本内置 macOS/Linux/Windows 常见中文字体检测，跨平台兼容。
3. **输出不覆盖原文件**：默认输出为 `原文件名_水印版.pdf`。
4. **大文件处理**：百页以上 PDF 可能较慢，属正常现象。
