#!/usr/bin/env python3
"""Perplexity Sonar search via Perplexity API or OpenRouter."""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def load_env(env_path):
    """Parse a .env file into a dict. Supports KEY=value and KEY='value' formats."""
    env = {}
    if not env_path.exists():
        return env
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Strip surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            env[key] = value
    return env


def resolve_provider(env):
    """Determine which API provider and key to use.

    Returns (api_url, model, api_key, provider_name) or exits with error.
    """
    perplexity_key = env.get("PERPLEXITY_API_KEY", "").strip()
    openrouter_key = env.get("OPENROUTER_APIKEY_RESEARCH", "").strip()
    prefer_openrouter = env.get("RESEARCH_PREFER_OPENROUTER", "").strip() == "1"

    has_perplexity = bool(perplexity_key)
    has_openrouter = bool(openrouter_key)

    if not has_perplexity and not has_openrouter:
        print(
            "ERROR: No API key found.\n\n"
            "Create ~/.claude/.env with at least one of:\n"
            "  PERPLEXITY_API_KEY='pplx-...'\n"
            "  OPENROUTER_APIKEY_RESEARCH='sk-or-v1-...'\n\n"
            "If both are set, Perplexity is preferred unless:\n"
            "  RESEARCH_PREFER_OPENROUTER=1",
            file=sys.stderr,
        )
        sys.exit(1)

    if has_perplexity and (not has_openrouter or not prefer_openrouter):
        return (
            "https://api.perplexity.ai/chat/completions",
            "sonar-pro",
            perplexity_key,
            "Perplexity",
        )
    else:
        return (
            "https://openrouter.ai/api/v1/chat/completions",
            "perplexity/sonar-pro",
            openrouter_key,
            "OpenRouter",
        )


def search(query, api_url, model, api_key, provider_name):
    """Send a search query and return the response text and citations."""
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a research assistant. Provide thorough, accurate, "
                    "and well-cited answers. Include specific version numbers, "
                    "dates, and links where relevant. Be concise but complete."
                ),
            },
            {"role": "user", "content": query},
        ],
        "max_tokens": 4096,
        "temperature": 0.1,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    if provider_name == "OpenRouter":
        headers["HTTP-Referer"] = "https://github.com/perplexity-research"
        headers["X-Title"] = "perplexity-research"

    data = json.dumps(payload).encode()
    req = urllib.request.Request(api_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"ERROR: HTTP {e.code} from {provider_name}\n{body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: Could not reach {provider_name}: {e.reason}", file=sys.stderr)
        sys.exit(1)

    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    citations = result.get("citations", [])

    return content, citations


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Usage: search.py <query>", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]

    # Load env from ~/.claude/.env, then overlay actual environment variables
    env = load_env(Path.home() / ".claude" / ".env")
    for key in ("PERPLEXITY_API_KEY", "OPENROUTER_APIKEY_RESEARCH", "RESEARCH_PREFER_OPENROUTER"):
        val = os.environ.get(key)
        if val:
            env[key] = val

    api_url, model, api_key, provider_name = resolve_provider(env)

    content, citations = search(query, api_url, model, api_key, provider_name)

    print(content)

    if citations:
        print("\n---\nSources:")
        for i, url in enumerate(citations, 1):
            print(f"  [{i}] {url}")


if __name__ == "__main__":
    main()
