# patent-spec-builder

将技术交底书或技术论文转换为标准**专利说明书**格式，同时支持 **Claude Code** 和 **Codex**。

输出两份符合 CNIPA 投稿规范的 Word 文档：
- **说明书摘要** — 一段式，200-400字
- **说明书** — 完整格式（技术领域、背景技术、发明内容、附图说明、具体实施方式），含 Word 原生 OMath 公式

## 功能特点

- 📝 标准专利说明书章节结构（无编号前缀的节标题）
- 📊 Word 原生 OMath 公式（LaTeX 自动转换）
- 📋 实验数据表格（基线对比、消融实验）
- 🖼️ 图片嵌入（系统框图、流程图）
- 🔀 从交底书到说明书的智能内容映射
- 📚 内联引用格式（术语/数据集/基线后跟随完整参考文献）
- 🔄 同时支持 Claude Code 和 Codex（Agent 自动判断触发）

## 环境准备

```bash
# 安装 Python 依赖
pip install python-docx lxml

# 克隆仓库
git clone https://github.com/coloreyes/patent-spec-builder.git
cd patent-spec-builder
```

## 使用方式

### Claude Code

```bash
# 安装为 Skill
git clone https://github.com/coloreyes/patent-spec-builder.git ~/.claude/skills/patent-spec-builder

# 启动 Claude Code
claude

# 在对话中触发（Agent 自动判断）:
# - 输入：专利说明书
# - 输入：说明书生成
# - 输入：patent-spec
# - 或直接提供文件：请根据 ./专利/交底书.md 生成说明书
```

### Codex（Agent 自动触发）

Codex Agent 会**自动判断**何时使用此 Skill，无需手动调用脚本。

#### 配置方式 1: 使用 OpenAI Agents SDK

```python
from openai import OpenAI
from agents import Agent, Runner

# 创建专利说明书生成 Agent
patent_agent = Agent(
    name="patent-spec-builder",
    instructions=open("prompts/spec_builder.md").read(),
    triggers=["专利说明书", "说明书生成", "generate patent specification"]
)

# 运行 - Agent 自动判断是否使用此 Skill
result = Runner.run(
    agent=patent_agent,
    input="请根据 ./专利/交底书.md 生成专利说明书"
)
```

#### 配置方式 2: 使用 MCP（Model Context Protocol）

```bash
# 启动 Codex 时加载 MCP 配置
codex --mcp-config mcp_config.json

# 在对话中输入（Agent 自动触发 Skill）:
# 请生成专利说明书
```

#### 配置方式 3: 使用 Custom Instructions

在 Codex 设置中添加：
```
当用户提及"专利说明书"、"说明书生成"或提供交底书文件时，
自动加载 prompts/spec_builder.md 作为系统提示。
```

#### 自动触发逻辑

```
用户输入 → Codex Agent 分析意图
  ↓
是否匹配触发关键词？
  ├─ 是 → 自动加载 Skill
  │   ↓
  │   1. 读取 prompts/spec_builder.md
  │   2. 分析输入文件（交底书）
  │   3. 按照规则生成说明书
  │   4. 使用 omath_converter.py 转换公式
  │   5. 输出两份 Word 文档
  │
  └─ 否 → 继续正常对话
```

#### 触发关键词

- 专利说明书
- 说明书生成
- 生成专利
- 专利交底书转换
- patent specification
- generate patent

### 完整工作流（推荐）

```bash
# 步骤 1: 克隆仓库
git clone https://github.com/coloreyes/patent-spec-builder.git
cd patent-spec-builder

# 步骤 2: 安装依赖
pip install python-docx lxml

# 步骤 3: 准备输入文件
mkdir -p ./专利/你的案件/
cp ./你的交底书.md ./专利/你的案件/

# 步骤 4: 生成说明书（Agent 自动触发）
# Claude Code:
claude  # 输入：专利说明书

# Codex:
codex  # 输入：专利说明书（Agent 自动加载 Skill）

# 步骤 5: 查看输出
ls ./专利/你的案件/*说明书*.docx
```

## 输出格式

### 说明书结构

```
[发明名称]（首行，居中，黑体16pt加粗）

技术领域
背景技术
发明内容（含S1-Sn步骤、公式、系统模块、有益效果）
附图说明
具体实施方式
  术语解释（每个术语含完整引用）
  实施例1（方法实现）
  实施例2（系统架构）
  应用例（实验数据对比、基线方法、数据集）
```

### 引用格式示例

```
多智能体系统（Multi-Agent System, MAS）：指由多个自治智能体组成的计算系统...
其相关研究可参考文献【L. Panait and S. Luke. Cooperative multi-agent learning: The state of the art. Autonomous agents and multi-agent systems, 11(3): 387–434, 2005.】
```

## 文件结构

```
patent-spec-builder/
├── skill.json              # Claude Code Skill 定义
├── codex_skill.yaml        # Codex 自动触发配置
├── CODEX_SETUP.md          # Codex 详细配置指南
├── README.md               # 本文档
├── requirements.txt        # Python 依赖
├── prompts/
│   ├── entry.md            # Claude Code 入口指令
│   └── spec_builder.md     # 格式规范与映射规则（共享）
└── tools/
    └── omath_converter.py  # LaTeX → Word OMath 转换器（共享）
```

## 依赖

- `python-docx >= 1.0.0` — Word 文档生成
- `lxml >= 4.9.0` — OMath XML 处理

```bash
pip install python-docx lxml
```

## 平台对比

| 特性 | Claude Code | Codex |
|------|-------------|-------|
| 触发方式 | 自然语言（Agent 自动判断） | 自然语言（Agent 自动判断） |
| 提示词加载 | 自动读取 `prompts/` | 自动读取 `codex_skill.yaml` |
| 工具调用 | 内置 `python-docx` | 内置 `python-docx` |
| 输出格式 | `.docx` Word 文档 | `.docx` Word 文档 |
| 配置入口 | `skill.json` | `codex_skill.yaml` |

## 示例输出

参考 `outputs/` 目录中的示例文件（如有）。

## License

MIT
