# patent-spec-builder

将技术交底书或技术论文转换为标准**专利说明书**格式的 Claude Code Skill。

输出两份符合 CNIPA 投稿规范的 Word 文档：
- **说明书摘要** — 一段式，200-400字
- **说明书** — 完整格式（技术领域、背景技术、发明内容、附图说明、具体实施方式），含 Word 原生 OMath 公式

## 功能特点

- 📝 标准专利说明书章节结构（无编号前缀的节标题）
- 📊 Word 原生 OMath 公式（LaTeX 自动转换）
- 📋 实验数据表格（基线对比、消融实验）
- 🖼️ 图片嵌入（系统框图、流程图）
- 🔀 从交底书到说明书的智能内容映射

## 使用方式

### 作为 Claude Code Skill 使用

将本目录放置于 `~/.claude/skills/patent-spec-builder/` 下，在对话中提及「专利说明书」或「说明书生成」即可触发。

### 输出格式

说明书结构：

```
[发明名称]
技术领域
背景技术
发明内容（含S1-Sn步骤、公式、系统模块、有益效果）
附图说明
具体实施方式
  实施例1（方法实现）
  实施例2（系统架构）
  应用例（实验数据对比）
```

## 文件结构

```
patent-spec-builder/
├── skill.json                    # Skill 定义
├── prompts/
│   ├── entry.md                  # 入口指令
│   └── spec_builder.md           # 格式规范与映射规则
└── tools/
    └── omath_converter.py        # LaTeX → Word OMath 转换器
```

## 依赖

- `python-docx`
- `lxml`

```bash
pip install python-docx lxml
```

## 示例输出

参考 `outputs/` 目录中的示例文件。

## License

MIT
