#!/usr/bin/env python3
"""
Calculate token sizes for all JSON files in data/existing_static_tools
"""
import os
import json
import tiktoken
from pathlib import Path

def get_token_count(text):
    """Calculate token count using GPT-4 encoding"""
    encoder = tiktoken.encoding_for_model("gpt-4")
    return len(encoder.encode(text))

def main():
    tools_dir = Path("data/existing_static_tools")

    if not tools_dir.exists():
        print(f"Error: Directory {tools_dir} does not exist")
        return

    # Get all JSON files
    json_files = sorted(tools_dir.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {tools_dir}")
        return

    results = []
    total_tokens = 0

    print(f"Calculating token sizes for {len(json_files)} tools...\n")

    for json_file in json_files:
        with open(json_file, 'r') as f:
            content = f.read()

        token_count = get_token_count(content)
        total_tokens += token_count
        results.append((json_file.name, token_count))
        print(f"{json_file.name:45} {token_count:6} tokens")

    print("\n" + "="*60)
    print(f"Total: {len(json_files)} tools")
    print(f"Total tokens: {total_tokens}")
    print(f"Average tokens per tool: {total_tokens // len(json_files)}")
    print("="*60)

if __name__ == "__main__":
    main()
