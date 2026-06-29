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
- 🔄 同时支持 Claude Code 和 Codex

## 环境准备

```bash
# 1. 安装 Python 依赖
pip install python-docx lxml

# 2. 克隆仓库
git clone https://github.com/coloreyes/patent-spec-builder.git
cd patent-spec-builder
```

## 使用方式

### Claude Code

```bash
# 方式 1: 安装为 Skill
git clone https://github.com/coloreyes/patent-spec-builder.git ~/.claude/skills/patent-spec-builder

# 启动 Claude Code
claude

# 在对话中触发（任选其一）:
# - 输入：专利说明书
# - 输入：说明书生成
# - 输入：patent-spec

# 方式 2: 直接使用
claude "请根据 ./专利/你的交底书.md 生成专利说明书"
```

### Codex 详细使用指南

#### 1. 使用入口脚本（最简单）

```bash
# 安装依赖
pip install python-docx lxml

# 运行入口脚本
python3 shared/entry.py \
  --input ./专利/你的交底书.md \
  --output ./专利/你的案件/
```

#### 2. 使用 API 调用示例脚本

```bash
# 设置 API Key
export OPENAI_API_KEY=your_api_key_here

# 运行示例脚本
bash examples/codex_api_example.sh \
  ./专利/你的交底书.md \
  ./专利/你的案件/
```

#### 3. 直接使用 curl 调用 API

```bash
# 设置变量
export OPENAI_API_KEY=your_api_key_here
INPUT_FILE="./专利/你的交底书.md"

# 读取 spec_builder.md 作为系统提示
SYSTEM_PROMPT=$(cat prompts/spec_builder.md)

# 读取输入文件内容
INPUT_CONTENT=$(cat "$INPUT_FILE")

# 调用 Codex API
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"o3\",
    \"messages\": [
      {\"role\": \"system\", \"content\": \"$SYSTEM_PROMPT\"},
      {\"role\": \"user\", \"content\": \"请根据以下交底书内容生成专利说明书（含说明书摘要和说明书两份Word文档）:\n\n$INPUT_CONTENT\"}
    ]
  }"
```

#### 4. 使用 Python 脚本调用

```python
import openai
import os

# 设置 API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 读取系统提示
with open("prompts/spec_builder.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 读取输入文件
with open("./专利/你的交底书.md", "r", encoding="utf-8") as f:
    input_content = f.read()

# 调用 API
response = openai.chat.completions.create(
    model="o3",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"请根据以下交底书内容生成专利说明书:\n\n{input_content}"}
    ]
)

# 输出结果
print(response.choices[0].message.content)
```

#### 5. 在 Codex CLI 中使用

```bash
# 启动 Codex CLI
codex

# 在对话中输入:
# 请将 prompts/spec_builder.md 的内容作为系统提示，
# 然后根据 ./专利/你的交底书.md 生成专利说明书

# 或者直接运行入口脚本:
python3 shared/entry.py \
  --input ./专利/你的交底书.md \
  --output ./专利/你的案件/
```

#### 6. 完整工作流（推荐）

```bash
# 步骤 1: 克隆仓库
git clone https://github.com/coloreyes/patent-spec-builder.git
cd patent-spec-builder

# 步骤 2: 安装依赖
pip install python-docx lxml

# 步骤 3: 设置 API Key
export OPENAI_API_KEY=your_api_key_here

# 步骤 4: 准备输入文件
mkdir -p ./专利/你的案件/
cp ./你的交底书.md ./专利/你的案件/

# 步骤 5: 生成说明书
bash examples/codex_api_example.sh \
  ./专利/你的案件/交底书.md \
  ./专利/你的案件/

# 步骤 6: 查看输出
ls ./专利/你的案件/*说明书*.docx
```

#### 7. 注意事项

- **模型选择**: 推荐使用 `o3` 或 `o4-mini` 模型，它们对复杂指令的理解能力更强
- **上下文长度**: 交底书较长时，确保模型支持足够的上下文长度
- **依赖安装**: 生成 Word 文档需要 `python-docx` 和 `lxml`，请提前安装
- **输出路径**: 输出文件默认保存在 `--output` 指定的目录中
- **API 限流**: 如果交底书较大，可能会触发 API 限流，建议分段处理或增加重试机制

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

# 步骤 4: 生成说明书
# Claude Code:
claude  # 输入：专利说明书

# Codex:
python3 shared/entry.py \
  --input ./专利/你的案件/交底书.md \
  --output ./专利/你的案件/

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
├── skill.json                    # Claude Code Skill 定义
├── codex_skill.json              # Codex Skill 定义
├── README.md                     # 本文档
├── requirements.txt              # Python 依赖
├── shared/
│   └── entry.py                  # 统一入口脚本（双平台）
├── prompts/
│   ├── entry.md                  # Claude Code 入口指令
│   └── spec_builder.md           # 格式规范与映射规则（共享）
├── tools/
│   └── omath_converter.py        # LaTeX → Word OMath 转换器（共享）
└── examples/
    └── codex_api_example.sh      # Codex API 调用示例
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
| 触发方式 | 自然语言（如「专利说明书」） | API 调用 / CLI 脚本 |
| 提示词加载 | 自动读取 `prompts/` | 手动传入 system prompt |
| 工具调用 | 内置 `python-docx` | 需配置外部脚本 |
| 输出格式 | `.docx` Word 文档 | 相同，需安装依赖 |
| 配置入口 | `skill.json` | `codex_skill.json` |

## 示例输出

参考 `outputs/` 目录中的示例文件（如有）。

## License

MIT
