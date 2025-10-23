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

## Stripe mcp response sizes

### Using 3-metatool design (list-api-endpoints, get-api-endpoint-schema, invoke-api-endpoint)

#### list-api-endpoints
1. Return only the names of the tools
903 tokens

2. Return name and brief description
to-be-added

3. Return name and full description
to-be-added

#### get-api-endpoint-schema (PostProducts)
1. Return a subset of the OpenAPI schema
to-be-added

2. Return the full OpenAPI schema
2873

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
| gemini-2.5-pro | 1048k | 65k |
| gemini-2.5-flash | 1048k | 65k |

TODO: add more older models
| claude-sonnet-4-0 | 200k | 64k |
| claude-opus-4-0 | 200k | 32k |
| gemini-2.0-flash | 1048k | 8k |
| gemini-2.0-flash-lite | 1048k | 8k |

[OpenAI](https://platform.openai.com/docs/models)
[Anthropic](https://docs.claude.com/en/docs/about-claude/models/overview)
[DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)
[Cursor](https://cursor.com/docs/models)

## Model deprecation timelines
[Anthropic](https://docs.claude.com/en/docs/about-claude/model-deprecations): average ~1-1.5 years
[OpenAI](https://platform.openai.com/docs/deprecations): average ~1.5-3 years