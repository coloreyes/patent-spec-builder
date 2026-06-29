#!/usr/bin/env python3
"""Unified entry point for patent-spec-builder.

Works with both Claude Code and Codex.

Usage:
    # Claude Code (via skill triggers):
    claude  # 输入：专利说明书

    # Codex (via CLI or API):
    python3 shared/entry.py --input 交底书.md --output ./输出/

    # Direct usage:
    python3 shared/entry.py \
        --input ./专利/你的案件/交底书.md \
        --output ./专利/你的案件/ \
        --spec-builder ./prompts/spec_builder.md \
        --omath-converter ./tools/omath_converter.py
"""

import argparse
import os
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description='将技术交底书转换为标准专利说明书格式'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='输入文件路径（.md 或 .docx）'
    )
    parser.add_argument(
        '--output', '-o',
        required=False,
        help='输出目录路径（默认与输入文件同目录）'
    )
    parser.add_argument(
        '--spec-builder',
        default=None,
        help='spec_builder.md 路径（默认自动查找）'
    )
    parser.add_argument(
        '--omath-converter',
        default=None,
        help='omath_converter.py 路径（默认自动查找）'
    )
    args = parser.parse_args()

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    spec_builder_path = args.spec_builder or os.path.join(base_dir, 'prompts', 'spec_builder.md')
    omath_converter_path = args.omath_converter or os.path.join(base_dir, 'tools', 'omath_converter.py')
    output_dir = args.output or os.path.dirname(os.path.abspath(args.input))

    # Verify files exist
    for path, name in [(args.input, '输入文件'), (spec_builder_path, 'spec_builder.md'), (omath_converter_path, 'omath_converter.py')]:
        if not os.path.exists(path):
            print(f"错误: {name} 不存在: {path}")
            sys.exit(1)

    print(f"输入文件: {args.input}")
    print(f"输出目录: {output_dir}")
    print(f"spec_builder: {spec_builder_path}")
    print(f"omath_converter: {omath_converter_path}")
    print("\n说明: 此脚本提供路径解析和参数验证。")
    print("实际生成需通过 Claude Code Skill 或 Codex API 调用。")
    print("\n使用方式:")
    print("  Claude Code: claude  # 输入：专利说明书")
    print("  Codex API: 将 spec_builder.md 作为 system prompt 传入")

if __name__ == '__main__':
    main()
