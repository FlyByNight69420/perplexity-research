# perplexity-research

Claude Code plugin that replaces web search with Perplexity Sonar for current, cited research results.

## Install

```bash
npx skills add FlyByNight69420/perplexity-research
```

Or from a local clone:

```bash
git clone https://github.com/FlyByNight69420/perplexity-research.git
npx skills add ./perplexity-research
```

## Configuration

Add at least one API key to `~/.claude/.env`:

```bash
# Option 1: Perplexity directly (preferred)
PERPLEXITY_API_KEY='pplx-...'

# Option 2: OpenRouter
OPENROUTER_APIKEY_RESEARCH='sk-or-v1-...'

# Optional: prefer OpenRouter when both keys are set
# RESEARCH_PREFER_OPENROUTER=1
```

## How it works

The skill triggers whenever Claude discusses software, hardware, libraries, or anything needing up-to-date information. It runs a Python script that queries Perplexity's Sonar Pro model with date-grounded queries (e.g., "As of March 2026, ...") and returns cited results.

## Requirements

- Python 3.6+ (uses only stdlib)
- A Perplexity API key or OpenRouter API key

## Provider Priority

| Keys Available | Provider Used |
|---|---|
| Only `PERPLEXITY_API_KEY` | Perplexity |
| Only `OPENROUTER_APIKEY_RESEARCH` | OpenRouter |
| Both | Perplexity (default) |
| Both + `RESEARCH_PREFER_OPENROUTER=1` | OpenRouter |
