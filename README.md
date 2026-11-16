# pi-pdf-watermark

[![pi-package](https://img.shields.io/badge/pi-package-skill-blue)](https://pi.dev/packages)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Pi Skill** — Add customizable text watermarks to PDF files. Center or tiled, with adjustable angle, font size, opacity, and color.

## ✨ Features

- **Two watermark modes**: Single centered stamp or full-page tiled repeat
- **Fully customizable**: Text content, rotation angle, font size, opacity, color
- **Auto page-size detection**: Handles A4, Letter, and any custom page dimensions
- **Cross-platform**: Auto-detects Chinese fonts on macOS / Linux / Windows
- **Defaults to a new file**: Without `-o` it writes `原文件名_水印版.pdf`. It does not yet refuse an output path that resolves to the input, and the write is not atomic — don't point `-o` at the input or any file you need to keep

## 🚀 Install

```bash
# Via npm (recommended)
pi install npm:pi-pdf-watermark

# Or via GitHub
pi install git:github.com/ssdiwu/pi-pdf-watermark
```

## 📖 Usage

Once installed, just say:

> "给这个 PDF 打水印"

The skill will ask you what text to use, then generate the watermarked PDF.

### Examples

| What you say | What happens |
|---|---|
| "给 report.pdf 打水印" | Asks for text → defaults to tiled mode |
| "给 report.pdf 打上「机密」水印" | Runs immediately, tiled |
| "打一个居中的 30° 水印" | Uses center mode, 30° angle |

### Command Line (standalone)

You can also run `watermark.py` directly without Pi:

```bash
# Install dependencies
pip3 install pypdf reportlab

# Basic usage (tiled by default)
python3 skills/pdf-watermark/references/watermark.py input.pdf "模力无限"

# Center mode
python3 skills/pdf-watermark/references/watermark.py input.pdf "CONFIDENTIAL" --mode center --angle 30 --opacity 0.2

# Custom font size & opacity
python3 skills/pdf-watermark/references/watermark.py input.pdf "DRAFT" --mode tile --font-size 36 --opacity 0.1

# Custom output path
python3 skills/pdf-watermark/references/watermark.py input.pdf "内部资料" -o output.pdf
```

#### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `input` | *(required)* | Input PDF file path |
| `text` | *(required)* | Watermark text |
| `--mode` | `tile` | `center` (single) or `tile` (full-page) |
| `--angle` | `45` | Rotation angle in degrees |
| `--font-size` | `42` | Font size |
| `--opacity` | `0.15` | Opacity (0–1) |
| `--output`, `-o` | `*_水印版.pdf` | Output file path |

## 🔧 How It Works

```
User says "打水印"
       ↓
Skill asks: "请问要打什么水印文字？"
       ↓
User replies: "模力无限"
       ↓
Script runs with default tile mode → outputs *_水印版.pdf
```

**Default behavior:**
- Mode: **Tiled (满铺)** — covers entire page at 45°
- Only asks for **watermark text**, everything else uses sensible defaults
- Switches to **center mode** only when user explicitly requests it

## 📦 Dependencies

- [pypdf](https://pypdf.readthedocs.io/) — PDF reading/writing
- [reportlab](https://www.reportlab.com/) — PDF generation (for watermark layer)

Both are installed automatically when running via Pi, or manually via:
```bash
pip3 install pypdf reportlab
```

## 🏗️ Package Structure

```
pi-pdf-watermark/
├── package.json              # Pi manifest + npm metadata
├── README.md                 # This file (usage)
├── doc/README.md             # Doc entry point (navigation only)
├── LICENSE                   # MIT License
└── skills/
    └── pdf-watermark/
        ├── SKILL.md          # Skill definition (Pi reads this)
        └── references/
            └── watermark.py   # Watermark script (CLI-ready)
```

## 🤝 Contributing

PRs welcome! Feel free to open issues for feature requests or bugs.

## 📄 License

[MIT](LICENSE) © ssdiwu
