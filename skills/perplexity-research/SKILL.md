---
name: perplexity-research
description: MUST use for ALL online research. NEVER use WebSearch or WebFetch -- this skill replaces them entirely. Triggers when discussing software, hardware, libraries, frameworks, APIs, tools, current events, or ANY topic where up-to-date information matters. Triggers on versions, compatibility, release dates, comparisons, recommendations, troubleshooting, or current state of technology. If there is even a 5% chance the answer depends on information newer than training data, use this skill.
---

# Perplexity Research

Search the web using Perplexity Sonar for current, cited information.

<HARD-RULE>
## DO NOT use WebSearch or WebFetch. EVER.

This skill REPLACES WebSearch and WebFetch entirely. You MUST use this skill's search.py script for ALL online research. No exceptions.

**If you are about to call WebSearch or WebFetch, STOP. Use this skill instead.**
</HARD-RULE>

## Red Flags -- STOP and Use This Skill

If you catch yourself thinking any of these, you are about to violate this rule:

| Thought | Reality |
|---------|---------|
| "WebSearch is faster/easier" | search.py is one command. Same effort, better results with citations. |
| "I'll just quickly check with WebSearch" | No. Run search.py instead. Same speed. |
| "This is a simple lookup, not research" | All online lookups go through this skill. No size threshold. |
| "I need WebFetch to read a specific URL" | Search for the topic instead. If you truly need a specific URL's content, ask the user. |
| "The built-in tool is more reliable" | Sonar returns cited, current results. It is more reliable for factual queries. |

## When to Use

Use this skill when:
- User mentions ANY software, library, framework, tool, or API by name
- User asks about versions, compatibility, "how to" with specific tech
- User asks about hardware, devices, or products
- User asks about current events, recent changes, or "latest"
- User is debugging and the solution may depend on current library behavior
- User asks for recommendations or comparisons of tools/services
- ANY time your training data might be outdated for the topic
- You are writing code that depends on a specific API or library and need to verify current usage
- You need to look something up online for ANY reason

**Err on the side of searching.** If in doubt, search.

## How to Use

### 1. Construct a date-grounded query

ALWAYS prepend the current date context to your query. This ensures Sonar returns current results.

Format: `"As of {Month} {Year}, {your specific question}"`

Examples:
- `"As of March 2026, what is the latest stable version of Node.js and what are its key features?"`
- `"As of March 2026, does the Rust borrow checker support partial borrows?"`
- `"As of March 2026, what is the recommended way to handle authentication in Next.js 15?"`

### 2. Run the search

```bash
python3 SKILL_DIR/scripts/search.py "As of March 2026, your query here"
```

Replace `SKILL_DIR` with the absolute path to this skill's directory (the directory containing this SKILL.md file).

### 3. Present results

- Summarize the key findings for the user
- Include relevant citations from the sources
- If the results are insufficient, run additional focused searches

### Tips

- **Break broad topics into focused queries.** Instead of "tell me about React", search for the specific aspect: "As of March 2026, what are the breaking changes in React 19?"
- **Run multiple searches** if the user's question spans multiple topics
- **Always include the date grounding** -- never skip it
- **Verify surprising claims** with a follow-up search if needed

## Setup

Requires `~/.claude/.env` with at least one API key:

```
PERPLEXITY_API_KEY='pplx-...'
OPENROUTER_APIKEY_RESEARCH='sk-or-v1-...'
```

If both are set, Perplexity is used by default. Set `RESEARCH_PREFER_OPENROUTER=1` to prefer OpenRouter instead.
