# Patent Disclosure Document

面向专利技术交底书的 Agent Skill：编纂、原位修订、提交前审查、方案比较、篇幅统计，以及技术附图规划与可编辑绘图。

**一套核心内容，适配 Codex、Claude Code、Cursor、GitHub Copilot，并提供通用助手使用方式。**

An agent skill for drafting, reviewing and revising patent technical disclosures. It preserves technical meaning, editable equations and document structure, and supports both document comparison and figure workflows. The default instructions are in Chinese; English and bilingual output can be requested.

## 能做什么

| 任务 | 交付 |
| --- | --- |
| 依据项目材料编纂交底书 | 按模板组织问题、方案、效果、实施例和附图说明 |
| 判断已有审查建议并修改 | 核对每项意见，直接落实合理且已授权的修改 |
| 在 Word 原文件中定点修改 | 保留公式、附图、样式及非目标内容，核对实际保存结果 |
| 提交前审查或复审 | 结论、评分、问题位置、替换内容、待确认项及检查清单 |
| 比较两份交底书 | 技术机制差异，或同口径的全文／章节字数差额 |
| 规划、审查或重绘附图 | 精确到框名和连线的意见、绘图提示词或原生 draw.io 图元 |

可用于软件／AI、机械装置、电子控制、材料工艺及跨领域方案，按实际技术内容选检查项。项目专用技术设计、原始交底书、企业材料和个人工作区路径不包含在此公开包中。

## 快速安装

需要 Git 和 Python 3.10 或以上版本。安装脚本仅使用 Python 标准库，不需要 `pip install`。

```bash
git clone https://github.com/Cby2005/Patent-Disclosure-Document.git
cd Patent-Disclosure-Document

# 预览 Codex 个人安装位置，不修改文件
python scripts/install.py --client codex --scope user --dry-run

# 安装
python scripts/install.py --client codex --scope user
```

Windows 可以把 `python` 替换为 `py -3`；macOS／Linux 可以替换为 `python3`。选择已有且符合版本要求的 Python。

其他客户端：

```bash
python scripts/install.py --client claude --scope user
python scripts/install.py --client cursor --scope user
python scripts/install.py --client copilot --scope user
```

按实际使用的客户端选择即可。已有同名 skill 时默认拒绝覆盖；确认需要更新后加 `--replace`，脚本会保留旧目录备份，并输出备份路径。标准目录安装时，备份位于技能扫描根目录之外，避免重复发现。

### 项目安装与自定义位置

```bash
# 将下面路径换成你的实际项目根目录
python scripts/install.py --client claude --scope project --project ./my-project

# 其他宿主配置的技能目录，参数指向最终的 skill 文件夹
python scripts/install.py --client codex --destination ./my-skills/patent-disclosure --dry-run
```

安装脚本只复制 `skills/patent-disclosure/`，不会读取、转换或修改专利文档，也不会更改客户端权限配置。若同名技能已安装在其他位置，先检查实际加载位置，避免安装重复副本。

## 多客户端适配

下表为安装脚本采用的目录；`~` 表示用户主目录。

| 客户端 | 个人目录 | 项目目录 | 使用方式 |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/patent-disclosure/` | `.agents/skills/patent-disclosure/` | `$patent-disclosure` 或说明要处理交底书 |
| Claude Code | `~/.claude/skills/patent-disclosure/` | `.claude/skills/patent-disclosure/` | `/patent-disclosure` 或自然语言请求 |
| Cursor | `~/.cursor/skills/patent-disclosure/` | `.cursor/skills/patent-disclosure/` | 自然语言请求加载该 skill |
| GitHub Copilot | `~/.copilot/skills/patent-disclosure/` | `.github/skills/patent-disclosure/` | 在支持 Agent Skills 的会话中请求使用该 skill |
| 通用助手 | 不依赖安装目录 | 上传或粘贴所需说明 | 使用[通用提示词](adapters/generic-prompt.md) |

目录和调用依据见[兼容性与官方文档](docs/compatibility.md)。本地个人安装不意味着云端会话自动获得同一目录；远程环境应按客户端说明提供项目技能和材料。

这些适配覆盖目录、提示入口和安装流程。未对全部客户端执行 Office 文档端到端测试；实际文件读写能力取决于所在环境提供的工具。

## 使用示例

把以下请求中的文件名换成实际文件，并确保助手能访问对应材料。

**编纂：**

> 使用 patent-disclosure。依据项目方案、参考论文和交底书模板编纂一份中文技术交底书。区分材料事实、可借鉴机制和本方案设计选择；缺少真实实验时不要补造结果。

**原位修订：**

> 根据我给出的审查意见，逐项判断是否合理。合理的直接在指定交底书原文件中修改，保留核心方案、原生公式和其他章节，不另交付一个修订版。

**提交前审查：**

> 全面审查这份交底书能否交给代理机构。核对正文、所有公式、实施例和附图，区分提交前应改与可选优化。本轮只给意见，不改文件。

**篇幅比较：**

> 按相同的应用字数口径比较交底书A和B，列出全文差额，并指出主要在哪些章节增加。统计当前打开内容，说明未保存状态，不修改文档。

**附图：**

> 检查最新框架图与正文是否一致。引用现有框名，明确需要调整的连线、方向和标签；只给可直接复制的绘图提示词。

**其他技术领域或语言：**

> 本项目是机械装置。按部件、连接、动作顺序和运行条件审查，不增加算法训练模块。按我提供的英文模板输出，保留参数和图号的一致性。

## 文件与环境支持

- **DOCX**：用可用的文档工具或 OOXML 处理，保护可编辑数学公式、图片关系、表格和节设置。
- **旧 DOC**：先识别实际格式；转换和回存取决于环境，不将新格式文件冒充已修改原稿。
- **PDF／扫描件**：用于核对；OCR 数字和公式需要回看原图。
- **Markdown／纯文本**：可以直接修改和比较，字符计数应与 Word 应用字数区分。
- **draw.io／图像／PPTX**：区分源图元、截图和正文引用，按实际可读能力审查。

Windows 下可使用已授权的 Word／WPS 接口；macOS、Linux 和容器环境可采用可用的文档库及渲染器。仅聊天环境可以提供审查和替换稿，但不能声称已保存本机原文件。详细说明见 skill 内的[环境适配](skills/patent-disclosure/references/environment.md)。

## 仓库结构

```text
skills/patent-disclosure/
  SKILL.md                    核心入口，按任务读取参考
  agents/openai.yaml          Codex 界面元数据
  references/
    submission-review.md      审查与已有意见处理
    in-place-editing.md       原位编辑与对象保护
    length-comparison.md      全文及章节篇幅比较
    figures.md                附图与可编辑绘图
    environment.md            文件格式和运行环境
    domains.md                技术领域及语言
adapters/generic-prompt.md     无原生 skill 的助手入口
docs/compatibility.md         客户端与官方依据
scripts/install.py            跨平台安装器
scripts/validate.py           包结构与本地引用校验
tests/test_install.py         安装、备份及失败恢复测试
```

## 验证与维护

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

校验器检查本包约定的元数据格式、UTF-8、Markdown 本地引用和技能自包含性；安装测试只在临时目录运行，不改个人 skill。它们不验证具体发明的正确性，也不替代实际文档渲染与内容审查。

修改通用规则时维护一套核心文件，不按客户端复制五份正文。专业实现、私人写作偏好和项目材料应保存在用户自己的工作区，避免把某个案例变成所有交底书的固定方案。
