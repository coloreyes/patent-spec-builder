#!/bin/bash
# Codex API 调用示例
# 使用前设置环境变量: export OPENAI_API_KEY=your_key

INPUT_FILE="${1:-./交底书.md}"
OUTPUT_DIR="${2:-./输出/}"

# 读取 spec_builder.md 作为系统提示
SYSTEM_PROMPT=$(cat "$(dirname "$0")/../prompts/spec_builder.md")

# 读取输入文件内容
INPUT_CONTENT=$(cat "$INPUT_FILE")

# 调用 Codex API
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "o3",
    "messages": [
      {"role": "system", "content": "'"$SYSTEM_PROMPT"'"},
      {"role": "user", "content": "请根据以下交底书内容生成专利说明书（含说明书摘要和说明书两份Word文档）:\n\n'"$INPUT_CONTENT"'"}
    ]
  }'

echo "\n输出将保存在: $OUTPUT_DIR"
