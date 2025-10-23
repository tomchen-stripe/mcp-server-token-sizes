# token-size

A Python project for token size utilities.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python get_size.py
```

## Model context sizes
| model | input context window | max output token |
|-------|----------------------|------------------|
| GPT-5 | 400k | 128k |
| GPT-5 mini | 400k | 128k |
| GPT-5 nano | 400k | 128k |
| GPT-4.1 | 1047k | 32k |
| GPT-oss-120b | 131k | 131k |
| GPT-oss-20b | 131k | 131k |
| GPT-5 Chat | 128k | 16k |
| ChatGPT-4o | 128k | 16k |
| claude-sonnet-4-5 | 200k | 64k |
| claude-haiku-4-5 | 200k | 64k |
| claude-opus-4-1 | 200k | 32k |

# TODO: add older models

[OpenAI](https://platform.openai.com/docs/models)
[Anthropic](https://docs.claude.com/en/docs/about-claude/models/overview)
[DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)
[Cursor](https://cursor.com/docs/models)

## Model deprecation timelines
[Anthropic](https://docs.claude.com/en/docs/about-claude/model-deprecations)
[OpenAI](https://platform.openai.com/docs/deprecations)