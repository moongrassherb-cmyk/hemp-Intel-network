# Hemp & Cannabis Intelligence Digest

Twice-daily automated research digest covering hemp/cannabis law & politics,
business, science, and consumer trends — built for picking show stories and,
eventually, feeding a public "Hemp Intelligence Network" site.

## What it does

Every run:
1. Searches the web across 4 categories (politics/regulation, business,
   science, consumer/culture) using multiple targeted queries per category.
2. Has Claude summarize the genuinely new, relevant items — headline, short
   summary, source link, and a one-line "why it matters."
3. Saves the result as a dated markdown file in `digests/`.

Runs automatically via GitHub Actions, ~7am and ~4pm ET, and commits the
digest straight into this repo so you have a running archive of every edition.

## One-time setup (about 10 minutes)

1. **Create a GitHub account** if you don't have one (github.com — free).
2. **Create a new repository** and upload these files (or use `git push`)
   — keep it **private** if you'd rather the digests not be public.
3. **Get an Anthropic API key**: console.anthropic.com → Settings → API Keys
   → Create Key. (This is billed separately from your claude.ai
   subscription — usage for this script is small, a few cents to low
   dollars per day depending on run frequency.)
4. In your repo: **Settings → Secrets and variables → Actions → New
   repository secret**
   - Name: `ANTHROPIC_API_KEY`
   - Value: (paste your key)
5. **Settings → Actions → General** — make sure Actions are enabled and
   "Read and write permissions" is selected under Workflow permissions
   (needed so the workflow can commit digest files back to the repo).
6. That's it. It'll run automatically on schedule. To test it right away:
   go to the **Actions** tab → "Hemp & Cannabis Intelligence Digest" →
   **Run workflow** (this uses the `workflow_dispatch` trigger).

## Adjusting the schedule

Edit the `cron` lines in `.github/workflows/hemp-digest.yml`. Cron times are
in UTC — use a tool like crontab.guru to convert to your local time, and
remember to nudge it for daylight saving if that matters to you.

## Adjusting what it searches for

Edit the `CATEGORIES` dict in `hemp_digest.py` — add, remove, or narrow the
seed queries per category (e.g. add `"hemp beverage state ban news"` if
that's a story thread you're tracking closely).

## Running it locally / manually anytime

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python hemp_digest.py
```

This writes straight into `digests/`.

## Where this goes next

This repo is intentionally just the data-gathering layer. Natural next
steps once you're happy with the digest quality:
- A simple site (could be GitHub Pages, directly off this repo) that
  renders the digests nicely and lets you flag/star stories for the show.
- The public-facing **Hemp Intelligence Network** site — resource library,
  sourcing, and a "contact your rep" action tool — as a separate, later
  build once the news pipeline is proven out.
