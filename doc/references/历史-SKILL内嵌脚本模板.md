# 历史快照：SKILL.md 内嵌脚本模板

> 状态：**历史**。这是原 `skills/pdf-watermark/SKILL.md` 里内嵌的可执行脚本模板副本，已与现行实现漂移，保留仅作追溯。**不要照此执行**，现行实现见 [`../../skills/pdf-watermark/references/watermark.py`](../../skills/pdf-watermark/references/watermark.py)。

## 与现行实现的差异

| 项 | 本模板（历史） | 现行 `references/watermark.py` |
|---|---|---|
| 命令行入口 | 无，纯脚本顶部常量 | 有 `argparse`，支持 `--mode/--angle/--font-size/--opacity/--output` |
| 参数化 | `TEXT/MODE/ANGLE/...` 为文件级常量 | `create_watermark_page(text, mode, angle, font_size, opacity, color, w, h)` |
| 复用方式 | 复制到临时文件后执行 | 可直接 `python3` 运行，也可 `import` 调用 `add_watermark()` |
| 字体回退 | 候选列表 + `fc-list` 回退 | 候选列表 + `fc-list` 回退（`subprocess` 导入位置不同，行为一致） |
| 输出保护 | 无 | 无（输入输出同路径不会被拦截，非原子写入） |

## 原文（历史副本）

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

## 来源

- 取自本仓库 `skills/pdf-watermark/SKILL.md` 的「脚本模板」代码块（2026-08 前的内容，采集自工作区现状）。
- 采集时该代码块仍位于 `SKILL.md` 正文；本次整改把它移出正文、存为历史快照，正文改为指向现行实现 `skills/pdf-watermark/references/watermark.py`。
