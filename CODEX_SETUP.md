# Codex Skill 自动触发配置指南

## 目标

使 Codex Agent 能够像 Claude Code 一样，**自动判断**何时使用此 Skill，而非手动调用脚本。

## 配置方式

### 方式 1: 使用 OpenAI Agents SDK（推荐）

```python
from openai import OpenAI
from agents import Agent, Runner

# 创建专利说明书生成 Agent
patent_agent = Agent(
    name="patent-spec-builder",
    instructions=open("prompts/spec_builder.md").read(),
    tools=[
        # 注册 omath_converter 工具
        Tool(
            name="omath_converter",
            description="将 LaTeX 公式转换为 Word OMath 格式",
            function=open("tools/omath_converter.py").read()
        )
    ],
    triggers=["专利说明书", "说明书生成", "generate patent specification"]
)

# 运行 Agent
result = Runner.run(
    agent=patent_agent,
    input="请根据 ./专利/交底书.md 生成专利说明书"
)
```

### 方式 2: 使用 MCP（Model Context Protocol）

```json
// mcp_config.json
{
  "mcpServers": {
    "patent-spec-builder": {
      "command": "python3",
      "args": ["tools/omath_converter.py"],
      "env": {
        "SPEC_BUILDER_PROMPT": "prompts/spec_builder.md"
      }
    }
  }
}
```

启动 Codex 时加载配置：
```bash
codex --mcp-config mcp_config.json
```

### 方式 3: 使用 Codex Custom Instructions

在 Codex 设置中添加自定义指令：
```
当用户提及"专利说明书"、"说明书生成"或提供交底书文件时，
自动加载 prompts/spec_builder.md 作为系统提示，
并使用 tools/omath_converter.py 处理公式转换。
```

## 自动触发逻辑

```
用户输入 → Codex Agent 分析意图
  ↓
是否匹配触发条件？
  ├─ 是 → 自动加载 Skill
  │   ↓
  │   1. 读取 prompts/spec_builder.md
  │   2. 分析输入文件（交底书）
  │   3. 按照 spec_builder.md 规则生成说明书
  │   4. 使用 omath_converter.py 转换公式
  │   5. 输出两份 Word 文档
  │
  └─ 否 → 继续正常对话
```

## 触发关键词

- 专利说明书
- 说明书生成
- 生成专利
- 专利交底书转换
- patent specification
- generate patent

## 文件结构

```
patent-spec-builder/
├── skill.json              # Claude Code 配置
├── codex_skill.yaml        # Codex 自动触发配置
├── prompts/
│   └── spec_builder.md     # 系统提示（共享）
└── tools/
    └── omath_converter.py  # 工具（共享）
```
