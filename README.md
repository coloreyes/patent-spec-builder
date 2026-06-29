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
- 📚 内联引用格式（术语/数据集/基线后跟随完整参考文献）

## 环境准备

### 1. 安装 Python 依赖

```bash
pip install python-docx lxml
```

### 2. 安装 Skill 到 Claude Code

```bash
# 从 GitHub 克隆到本地
git clone https://github.com/coloreyes/patent-spec-builder.git ~/.claude/skills/patent-spec-builder

# 验证安装
ls ~/.claude/skills/patent-spec-builder/
# 应显示: prompts/  skill.json  tools/  README.md
```

## 使用方式

### 方式一：作为 Claude Code Skill 使用

```bash
# 1. 进入你的项目目录
cd /path/to/your/project

# 2. 启动 Claude Code
claude

# 3. 在对话中触发 Skill（任选其一）
#    - 输入：专利说明书
#    - 输入：说明书生成
#    - 输入：patent-spec
```

### 方式二：直接调用生成脚本

```bash
# 1. 准备输入文件（交底书或论文）
#    支持格式：.md, .docx

# 2. 运行生成脚本（需自行编写或使用 Claude Code）
python3 generate_spec.py \
  --input ./专利/你的交底书.md \
  --output ./输出目录/

# 3. 查看输出
ls ./输出目录/
# 应显示: 案件名_时间戳-说明书.docx
#         案件名_时间戳-说明书摘要.docx
```

### 方式三：完整工作流（推荐）

```bash
# 步骤 1: 克隆 Skill
git clone https://github.com/coloreyes/patent-spec-builder.git ~/.claude/skills/patent-spec-builder

# 步骤 2: 安装依赖
pip install python-docx lxml

# 步骤 3: 准备输入文件
# 将你的交底书或论文放入项目目录
mkdir -p ./专利/你的案件/
cp ./你的交底书.md ./专利/你的案件/

# 步骤 4: 启动 Claude Code 并生成
claude
# 在对话中输入：专利说明书
# 或提供文件路径后说：请根据这个文件生成专利说明书

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
├── skill.json                    # Skill 定义（触发词配置）
├── README.md                     # 本文档
├── requirements.txt              # Python 依赖
├── .gitignore                    # Git 忽略规则
├── prompts/
│   ├── entry.md                  # 入口指令（5步流程）
│   └── spec_builder.md           # 格式规范与映射规则（142行）
└── tools/
    └── omath_converter.py        # LaTeX → Word OMath 转换器（148行）
```

## 依赖

- `python-docx >= 1.0.0` — Word 文档生成
- `lxml >= 4.9.0` — OMath XML 处理

```bash
pip install python-docx lxml
```

## Codex 兼容性

### 是否可用于 OpenAI Codex？

**当前不可直接用于 Codex**，原因如下：

1. **Skill 架构差异**：本 Skill 使用 Claude Code 的 `skill.json` 触发机制和 `prompts/` 目录结构，这是 Claude Code 特有的 Skill 系统，Codex 没有对应的 Skill 加载机制。

2. **交互方式不同**：
   - Claude Code：通过自然语言触发（如「专利说明书」），Agent 自动读取 prompts/ 文件并执行
   - Codex：需要通过 API 调用或 CLI 指令，需手动编写提示词

3. **工具调用不同**：本 Skill 依赖 `python-docx` 和 `lxml` 生成 Word 文档，Codex 环境中需要额外配置这些依赖。

### 如何在 Codex 中使用核心功能？

若需在 Codex 中实现类似功能，可采用以下方案：

```bash
# 方案 1: 使用转换脚本直接调用
# 将 spec_builder.md 中的规则转换为 Codex 提示词
python3 tools/omath_converter.py  # OMath 转换器可独立使用

# 方案 2: 将 prompts/spec_builder.md 作为系统提示
# 在 Codex API 调用中将 spec_builder.md 内容作为 system prompt
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "o3",
    "messages": [
      {"role": "system", "content": "$(cat prompts/spec_builder.md)"},
      {"role": "user", "content": "请根据以下交底书生成专利说明书..."}
    ]
  }'

# 方案 3: 将本 Skill 适配为 Codex Skill 格式
# 需要编写 codex_skill.json 并调整 prompts 格式
```

### 适配建议

| 组件 | Claude Code | Codex 适配方案 |
|------|-------------|----------------|
| skill.json | 触发词配置 | 改为 codex_skill.json，定义触发指令 |
| prompts/ | Agent 自动读取 | 改为系统提示词，在 API 调用时传入 |
| tools/ | Python 脚本 | 保持不变，Codex 可调用外部脚本 |
| 输出格式 | .docx Word 文档 | 相同，需安装 python-docx |

## 示例输出

参考 `outputs/` 目录中的示例文件（如有）。

## License

MIT
