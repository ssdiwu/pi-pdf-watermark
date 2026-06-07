"""
PDF 水印工具 — 可独立命令行运行，也可被 agent import 调用。

用法:
  python3 watermark.py <input.pdf> <水印文字> [选项]

示例:
  python3 watermark.py input.pdf "模力无限"
  python3 watermark.py input.pdf "机密" --mode center --angle 30 --opacity 0.2
  python3 watermark.py input.pdf "内部资料" --mode tile --font-size 36
"""

import io
import math
import argparse
import os
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter


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
        # Windows
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for fp in candidates:
        try:
            pdfmetrics.registerFont(TTFont("ChineseFont", fp))
            return fp
        except Exception:
            continue
    # 尝试 fc-list
    try:
        result = subprocess.run(
            ["fc-list", ":lang=zh", "-f", "%{file}\n"],
            capture_output=True, text=True, timeout=5,
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
    raise RuntimeError(
        "未找到可用的中文字体，请安装中文字体包（如 fonts-wqy-zenhei）"
    )


def create_watermark_page(text, mode, angle, font_size, opacity, color, w, h):
    """生成一页水印，返回 PdfReader 的 page 对象"""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(w, h))
    c.setFillColor(Color(*color, alpha=opacity))
    c.setFont("ChineseFont", font_size)

    if mode == "center":
        c.saveState()
        c.translate(w / 2, h / 2)
        c.rotate(angle)
        c.drawCentredString(0, 0, text)
        c.restoreState()
    else:  # tile
        text_width = font_size * len(text) * 1.0
        text_height = font_size * 1.4
        step_x = text_width + 80
        step_y = text_height + 100
        diag = math.sqrt(w**2 + h**2)
        rows = int((diag * 2) // step_y) + 2
        cols = int((diag * 2) // step_x) + 2

        c.saveState()
        c.translate(w / 2, h / 2)
        c.rotate(angle)
        start_x = -diag
        start_y = -diag
        for row in range(int(rows)):
            for col in range(int(cols)):
                x = start_x + col * step_x
                y = start_y + row * step_y
                c.drawCentredString(x, y, text)
        c.restoreState()

    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def add_watermark(src_path, text, **kwargs):
    """
    给 PDF 添加水印。

    参数:
      src_path: 输入 PDF 路径
      text: 水印文字
      mode: "center" 或 "tile"（默认 tile）
      angle: 旋转角度（默认 45）
      font_size: 字号（默认 42）
      opacity: 透明度 0~1（默认 0.15）
      color: RGB 元组（默认 (0.55, 0.55, 0.55)）
      dst_path: 输出路径（默认 自动加 _水印版 后缀）

    返回:
      输出文件路径
    """
    mode = kwargs.get("mode", "tile")
    angle = kwargs.get("angle", 45)
    font_size = kwargs.get("font_size", 42)
    opacity = kwargs.get("opacity", 0.15)
    color = kwargs.get("color", (0.55, 0.55, 0.55))
    dst_path = kwargs.get("dst_path")

    find_chinese_font()

    if dst_path is None:
        base, ext = os.path.splitext(src_path)
        dst_path = f"{base}_水印版{ext}"

    reader = PdfReader(src_path)
    writer = PdfWriter()

    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        wm_page = create_watermark_page(text, mode, angle, font_size, opacity, color, w, h)
        page.merge_page(wm_page)
        writer.add_page(page)

    with open(dst_path, "wb") as f:
        writer.write(f)

    return dst_path


def main():
    parser = argparse.ArgumentParser(
        description="PDF 水印工具 — 给 PDF 文件添加自定义文字水印",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 watermark.py input.pdf "模力无限"
  python3 watermark.py input.pdf "机密" --mode center --angle 30 --opacity 0.2
  python3 watermark.py input.pdf "内部资料" --mode tile --font-size 36
        """,
    )
    parser.add_argument("input", help="输入 PDF 文件路径")
    parser.add_argument("text", help="水印文字")
    parser.add_argument("--mode", choices=["center", "tile"], default="tile",
                        help="水印模式: center=居中单个, tile=满铺整页 (默认: tile)")
    parser.add_argument("--angle", type=float, default=45,
                        help="旋转角度，单位度 (默认: 45)")
    parser.add_argument("--font-size", type=int, default=42,
                        help="字号 (默认: 42)")
    parser.add_argument("--opacity", type=float, default=0.15,
                        help="透明度 0~1 (默认: 0.15)")
    parser.add_argument("--output", "-o", default=None,
                        help="输出文件路径 (默认: 原文件名_水印版.pdf)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"❌ 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 解析颜色（暂不暴露为 CLI 参数，保持简洁）
    color = (0.55, 0.55, 0.55)

    dst = add_watermark(
        args.input,
        args.text,
        mode=args.mode,
        angle=args.angle,
        font_size=args.font_size,
        opacity=args.opacity,
        color=color,
        dst_path=args.output,
    )

    print(f"✅ 水印添加完成！")
    print(f"   输出: {dst}")
    print(f"   文字: 「{args.text}」| 模式: {args.mode} | 角度: {args.angle}° | 字号: {args.font_size} | 透明度: {args.opacity}")


if __name__ == "__main__":
    main()
