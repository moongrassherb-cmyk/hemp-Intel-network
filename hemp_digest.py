#!/usr/bin/env python3
"""
Hemp & Cannabis Intelligence Digest
------------------------------------
Runs a set of targeted web searches (via Claude's web_search tool) across
the hemp/cannabis industry and compiles a single organized markdown digest.

Categories covered:
  1. Law, regulation & politics (federal, state, DEA/FDA, farm bill, hemp-derived THC rules)
  2. Business & industry (deals, new products, market moves, major players)
  3. Science & technique (cultivation, extraction, genetics, research studies)
  4. Consumer / culture (trends, brands, public opinion)

Output: digests/YYYY-MM-DD_AM.md or _PM.md (an editable markdown file)

Setup:
  1. pip install anthropic
  2. export ANTHROPIC_API_KEY=sk-ant-...
  3. python hemp_digest.py
"""

import os
import sys
import datetime
import anthropic

MODEL = "claude-sonnet-4-6"  # update as needed

CATEGORIES = {
    "Law, Regulation & Politics": [
        "hemp derived THC law news",
        "cannabis policy federal legislation news",
        "state hemp regulation news",
        "DEA FDA hemp cannabis rule news",
    ],
    "Business & Industry": [
        "hemp industry business news",
        "cannabis company deal acquisition news",
        "hemp derived THC beverage market news",
    ],
    "Science & Technique": [
        "cannabis hemp cultivation research news",
        "hemp extraction technology news",
        "cannabinoid science study news",
    ],
    "Consumer & Culture": [
        "hemp THC drinks consumer trend news",
        "cannabis industry public opinion news",
    ],
}

SYSTEM_PROMPT = """You are a research assistant compiling a news digest for a \
hemp and cannabis industry broadcaster. For the given category, use web search \
to find genuinely recent, newsworthy items (prioritize the last 1-3 days). \
For each item found, return a short markdown bullet with:
- **Headline** (your own words, not copied from the source)
- One or two sentence summary in your own words (never quote more than a \
  few words verbatim, and never string multiple short quotes together)
- Source name and link
- Why it matters for a hemp/cannabis show or industry watcher (one line)

Skip anything that isn't genuinely new or is a duplicate of common knowledge. \
If you find fewer than 3 solid items, that's fine — don't pad with weak ones. \
Do not use direct quotations of 15+ words from any single source, and quote \
each source at most once. Respond only with the markdown bullets, no preamble."""


def run_category(client: anthropic.Anthropic, category: str, queries: list[str]) -> str:
    query_block = "\n".join(f"- {q}" for q in queries)
    user_prompt = (
        f"Category: {category}\n\n"
        f"Run web searches using these seed queries (reformulate/narrow as needed):\n"
        f"{query_block}\n\n"
        f"Compile the best 3-6 genuinely recent items for this category."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )

    text_parts = [block.text for block in response.content if block.type == "text"]
    return "\n".join(text_parts).strip()


def build_digest() -> str:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_slot = "Morning" if now.hour < 14 else "Afternoon"

    lines = [
        f"# Hemp & Cannabis Intelligence Digest",
        f"### {time_slot} Edition — {date_str}",
        "",
    ]

    for category, queries in CATEGORIES.items():
        print(f"Searching: {category}...", file=sys.stderr)
        lines.append(f"## {category}")
        lines.append("")
        try:
            result = run_category(client, category, queries)
            lines.append(result if result else "_No notable items found this cycle._")
        except Exception as e:
            lines.append(f"_Error fetching this category: {e}_")
        lines.append("")

    return "\n".join(lines)


def main():
    digest = build_digest()

    now = datetime.datetime.now()
    time_slot = "AM" if now.hour < 14 else "PM"
    filename = f"digests/{now.strftime('%Y-%m-%d')}_{time_slot}.md"

    os.makedirs("digests", exist_ok=True)
    with open(filename, "w") as f:
        f.write(digest)

    print(f"Digest written to {filename}", file=sys.stderr)


if __name__ == "__main__":
    main()
