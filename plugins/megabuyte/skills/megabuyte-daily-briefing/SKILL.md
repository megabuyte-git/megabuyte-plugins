---
name: megabuyte-daily-briefing
description: Produce a daily intelligence briefing of everything Megabuyte published in the last day — research, news, deals and people moves — with an overarching summary, using the Megabuyte MCP. Use this whenever the user asks for today's or yesterday's briefing, a morning or daily update, "what's new on Megabuyte", "what did Megabuyte publish today/this week", or runs it on a schedule. Also use for a briefing on a specific date ("briefing for 3 October") or narrowed to their sectors or watchlist. Not for what changed at one named company over a longer period (megabuyte-company-brief).
---

# Megabuyte daily briefing

A short, scannable digest of what Megabuyte published in the briefing window: an overall summary, then research, deals, people moves and other news.

**Read `references/conventions.md` first.** This briefing answers in chat only. Never create a file unless the user asks for one in the conversation (conventions §8): a scheduled run makes no files.

## Window and as-of date

- **As-of date:** today by default.
  - If the user names a date, use it.
  - If the archive's newest article is older than the as-of date (`latest_article_for_filters` on the news call), say so. While Megabuyte runs on a fixed test dataset, this will be the case: offer the briefing for the newest date held, or produce it for that date if the user asked for "the latest".
- **Window:** the previous business day up to the as-of date. On a Monday, cover Friday to Sunday. If the user says "this week" or "since my last briefing" with a date, use that range.
- **Always state the window and each source's newest date.** A quiet day must be distinguishable from a data delay.

## Scope

- **Default:** everything (Megabuyte publishes roughly 4–10 pieces a day).
- **Narrowed:** if the user names sectors, peer groups or a watchlist of companies, filter to those. The user's sectors and watchlist company names may be remembered between briefings, but never Megabuyte content (conventions §10).

## Workflow

1. **Plan.** Call `plan_query` with `intent: "news_and_signals"`, the question as asked, and `period_from`/`period_to` set to the window as YYYY-MM-DD. "Last 24 hours" isn't parsed, so always send explicit dates.

2. **Collect, in parallel**, each filtered to the window:
   - **News:** `get_news_articles` with `published_since`/`published_until`, `include_text: false`, `limit: 25`. Page if `next_offset` is set (rarely needed). Tags tell you which items are M&A, people moves, results and so on.
   - **People moves:** the news rows tagged "People Moves". There is no separate call; `search_people` can't filter by day.
   - **Reports** (go in Market research): `get_reports` with `published_since`/`published_until`.
   - **Company Analysis** (goes in Company research): `get_analysis` with `analysis_type: "company"`, `published_after`/`published_before`.
   - **Market Analysis** (goes in Market research): `get_analysis` with `analysis_type: "market"`, the same dates.
   - **Deals:** take the deals from the news first: articles tagged M&A, Private Equity, Venture & Growth Capital or Capital Markets. Deal records are added to the archive later than the news (tested: the newest deal record trailed the news by over a week), so `get_deals` with `announced_from`/`announced_to` is a supplement for values, multiples and parties. A window with no deal records but M&A-tagged articles is normal; never report "no deals" on deal records alone.

3. **Drop test records.** Skip any row whose title looks like a test, in news or deals, e.g. "News 100", "QA NEWS…", "Publish Test" or "Test Company 203 acquires Test Company 202", and any article whose body is only its title. Never date the archive from one. The real newest date is the newest item left after removing them.

4. **Read enough to summarise.** One `get_news_articles` call with the window's article ids (`article_id`, up to 10) and `max_text_chars` around 1,500 each, for the items you'll summarise. Read reports only via `semantic_search` passages or the report text if one is short; never summarise a report from its title.

5. **Write.**
   - **Summary:** 3–5 sentences on the day's main threads (e.g. "two cyber acquisitions, a run of HCM results with AI investment as the common theme, and a CEO change at…"). It's your synthesis of the dated items, so keep it factual.
   - **Items:** one line each, in your own words.

## Output structure

1. **Header**: "Megabuyte briefing · [window]". Newest held: news [date], deal records [date], research [date].
2. **Summary**: 3–5 sentences on the day's main threads.
3. **Company research**: company news (results and trading, contract wins, strategy) and **every Company Analysis** published in the window. A Company Analysis always goes here, even when it discusses the company's market.
4. **Market research**: **only** Market Analyses and reports (peer-group quarterlies, corporate activity reports) published in the window. Nothing else goes here.
5. **Deals**: from M&A, Private Equity, Venture & Growth Capital and Capital Markets articles, enriched from deal records (parties, type, value or "not disclosed", disclosed multiple).
6. **People moves**: from articles tagged People Moves.

**Every item is led by its title as a link** to the source, using the Link exactly as returned, then the date, then one line in your own words. For example:

> **[Article title as published](Link as returned)** · 13 Oct 2026. One line, in your own words, on what happened and why it matters.

- Companies named in the line link to their Megabuyte profiles (conventions §4).
- An item belongs in one section only. An article that is both a deal and results goes under Deals.
- An empty section reads "None published in the window".
- End with a one-line coverage note, e.g. "Deal records are added after the news, so deals are taken from the articles."

Keep the whole briefing scannable.

## Watch-outs

- Don't count the same story twice: an M&A article and its deal record are one item. Put it under Deals and link the article.
- Ordinary commercial news (contract wins, launches, awards) isn't a signal of a sale or distress. Don't frame it as one.
- If the window is empty in every source but the archive has newer items, the window is wrong. Check the dates before reporting a quiet day.
