---
name: gemini-api-dev
description: Develop Gemini APIs with current SDKs and models.
version: 1.0.0
author: Google Gemini
platforms: [linux, macos, windows]
metadata:
  gemini:
    tags: [gemini, api, sdk, python, typescript, agents, streaming, functions]
    homepage: https://github.com/google-gemini/gemini-skills
---

# Gemini API Development

Use the current `google-genai` Python SDK (>= 2.3.0) or `@google/genai` TypeScript SDK (>= 2.3.0). Never use legacy `google-generativeai` or `@google/generative-ai`.

## Model Selection

- Simple or balanced text: `gemini-3.8-flash`
- Fast low-cost high-throughput: `gemini-3.5-flash-lite`
- Complex reasoning, coding, and research: `gemini-3.1-pro-preview`
- Lightweight high-frequency work: `gemini-3.1-flash-lite`
- Images: `gemini-3.1-flash-image` or `gemini-3-pro-image`
- Speech: `gemini-3.1-flash-tts-preview`
- Video: `gemini-omni-1.1-flash`
- Embeddings: `gemini-embedding-2`

Do not use deprecated `gemini-2.x` or `gemini-1.x` models.

## Python Quick Start

```python
from google import genai

client = genai.Client()
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain Gemini API interactions.",
)
print(interaction.output_text)
```

## TypeScript Quick Start

```typescript
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({});
const interaction = await client.interactions.create({
  model: "gemini-3.8-flash",
  input: "Explain Gemini API interactions.",
});
console.log(interaction.output_text);
```

## Important Rules

- Fetch the relevant official documentation before writing code.
- Set `store=False` when previous interactions or paid-tier retention are not required.
- Re-specify interaction-scoped tools, system instructions, and generation configuration each turn.
- Use `previous_interaction_id` for server-side stateful conversations.
- Managed agents require a remote environment.
- Read the migration guide before changing model or API scope.

## Installation

```bash
pip install -U google-genai
# or
npm install @google/genai
```

Official resources:
- https://ai.google.dev/gemini-api/docs/
- https://github.com/google-gemini/gemini-skills
