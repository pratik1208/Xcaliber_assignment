"""Single LLM entry point. OpenAI by default; set LLM_PROVIDER=anthropic to use Claude."""
import json
import os
import re

from app.config import LLM_MODEL


def complete(system: str, user: str, max_tokens: int = 1200) -> str:
    if os.getenv("LLM_PROVIDER", "openai") == "anthropic":
        import anthropic

        r = anthropic.Anthropic().messages.create(
            model=LLM_MODEL, max_tokens=max_tokens, system=system,
            messages=[{"role": "user", "content": user}])
        return "".join(b.text for b in r.content if b.type == "text")
    from openai import OpenAI

    r = OpenAI().chat.completions.create(
        model=LLM_MODEL, max_tokens=max_tokens, temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    return r.choices[0].message.content


def parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"No JSON in LLM output: {text[:200]}")
    return json.loads(m.group(0))
