# pi-pdf-watermark — Agent 规范

## 文件职责与阅读顺序

- 文档入口是 `doc/README.md`，只做导航。
- 本文件只记录 PDF 水印 skill 的长期安全与交付边界；参数、安装和用法以 `README.md`、`skills/pdf-watermark/SKILL.md` 和当前脚本为准。
- 修改前读取 `skills/pdf-watermark/references/watermark.py`、字体探测和输出路径逻辑。
- 来源、验证记录和历史快照在 `doc/references/`，不是现行依据。

## 文件安全边界

- 输入 PDF 视为不可信文件，显式处理损坏、加密、权限不足、空页和超大文件；错误不能留下伪成功输出。
- 默认参数会派生新文件，但当前脚本不会拦截显式指定的输入输出同路径，也不是原子写入。每次调用前必须先解析并比较真实路径；相同则停止，不能把当前实现笼统称为“非破坏性”。
- 修改输出逻辑时应在实现层加入同路径拒绝、临时文件验证和原子移动；在这些保护真正落地并有测试前，调用方不得覆盖输入或任何未确认的现有文件。
- 字体使用当前平台可用字体并提供中文失败提示，不硬编码个人绝对路径。
- 不上传 PDF，不把文档内容、路径或元数据写进日志和测试夹具。
- 调试先用最小脱敏 PDF 重放，连续两次同类失败且范围未缩小时停止原路径。

## 验证

```bash
python3 -m py_compile skills/pdf-watermark/references/watermark.py
```

行为变更还需用临时 PDF 验证居中、平铺、中文字体、透明度、旋转、错误输入和“输入输出同路径拒绝”；检查页数与输出可打开。未做视觉检查时明确说明。

## 文档与 Git

- 参数、默认输出、字体选择、安全或安装行为变化时同步 README 与 SKILL；文档角色或位置变化时同步 `doc/README.md`。
- 未经用户明确要求，不执行 commit、push、tag 或 npm publish。

## 双语与发布约定

- `README.md`（英文）与 `README-zh.md`（中文）是同一份公开说明的两版，改动时同一次提交内同步，语义必须一致；公开贡献说明以两版 README 与 `doc/README.md` 的导航为准，不得只改一版。
- 两份变更日志都在本 GitHub 仓库维护。`CHANGELOG.md` 是英文发布记录，`CHANGELOG-zh.md` 是中文日常记录。两份只写用户可感知事实，不倒填未发布版本。
- 日常用中文把已完成的用户可感知变化写入 `CHANGELOG-zh.md`；准备发布（release）时按版本把同一版本的用户可感知条目同步进英文 `CHANGELOG.md`，两份都保留该版本记录，并核对版本、日期与 issue 链接。
- `README.md` 是英文默认版（npm 默认展示），`README-zh.md` 是同包附带的中文版；两份 README 与两份 changelog 都随 npm 包发布。发布前用 `npm pack --dry-run --ignore-scripts --json` 核对清单包含 `README.md`、`README-zh.md`、`CHANGELOG.md`、`CHANGELOG-zh.md`。
- `doc/` 下的内部资料可用中文，与公开 README 的语言无关；`doc/README.md` 顶部保留英文贡献导航，中文原文留在其后。
