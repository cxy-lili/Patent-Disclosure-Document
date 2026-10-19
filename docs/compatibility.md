# 客户端适配与依据

目录规则于2026年10月19日核对。宿主升级、组织策略及本地／云端会话可能改变加载行为；安装后在实际客户端确认能发现 `patent-disclosure`。

## 原生 Agent Skills

| 客户端 | 本包采用的个人根目录 | 本包采用的项目根目录 | 官方依据 |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills` | `.agents/skills` | [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `~/.claude/skills` | `.claude/skills` | [Extend Claude with skills](https://code.claude.com/docs/en/skills) |
| Cursor | `~/.cursor/skills` | `.cursor/skills` | [Skills](https://cursor.com/help/customization/skills) |
| GitHub Copilot | `~/.copilot/skills` | `.github/skills` | [Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) |

安装器在根目录下创建 `patent-disclosure/` 并复制完整技能资源。部分客户端还支持其他目录，但本包选择一条明确路径，不同时安装多个别名。

- Codex 可以显式使用 `$patent-disclosure`；界面元数据保存在技能的 `agents/openai.yaml`。其他宿主主要读取 `SKILL.md` 和所需参考。
- Claude Code 可以用 `/patent-disclosure` 调用，其个人技能目录与云端会话的加载范围不同。
- Cursor 支持其原生目录和其他兼容目录。本包选 `.cursor/skills`，避免依赖兼容目录的历史行为。
- Copilot 需在支持 Agent Skills 的会话中使用。仓库中存在技能目录不意味着它能操作远程不可见的本地 Word 文档。

## 无原生技能功能的助手

使用[通用提示词](../adapters/generic-prompt.md)，或上传 `SKILL.md` 及本次任务需要的 `references/` 文件。没有自动文件读取时，必须显式提供相关参考；不假设附件目录内所有内容都会自动加载。

通用提示词不是某个产品的插件或服务器，不会替助手增加文件系统、联网、OCR 或 Office 权限。

## 安装与运行测试边界

安装器仅依赖 Python 3.10+ 标准库，使用 `pathlib` 生成本机路径、在目标同一文件系统暂存，并在替换失败时恢复旧目录。更新备份保留在默认技能扫描根的上一级 `.patent-disclosure-backups/` 中；自定义位置以脚本输出为准。

本次开发在 Windows 验证了实际安装、拒绝覆盖、保留备份、失败恢复及中文路径。macOS／Linux 的目录规则由官方文档和跨平台代码支持，尚未逐机执行测试；也未声称所有客户端的文档自动化能力相同。
