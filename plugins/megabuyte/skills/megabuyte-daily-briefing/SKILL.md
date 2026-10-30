---
name: megabuyte-daily-briefing
description: Daily briefing of everything Megabuyte published in the last day (research, news, deals, people moves) with a summary, from the Megabuyte MCP. Use for today's or yesterday's briefing, a morning or daily update, "what's new on Megabuyte", what Megabuyte published on a date or this week, scheduled runs, or a briefing narrowed to sectors or companies the user names. Prefer megabuyte-company-brief for one company's news over time, when installed.
---

# Megabuyte daily briefing

A short, scannable digest of what Megabuyte published in the briefing window: an overall summary, then company research (including people moves), market research and deals.

**Read `references/conventions.md` first.** This briefing answers in chat.

## Window and as-of date

- **As-of date:** today by default.
  - If the user names a date, use it.
  - If the archive's newest article is older than the as-of date (`latest_article_for_filters` on the news call), say so: the archive is a snapshot refreshed daily, so a gap usually means the refresh hasn't run yet, not a quiet day.
- **Window:** the previous business day up to the as-of date. On a Monday, cover Friday to Sunday. If the user says "this week" or "since my last briefing" with a date, use that range.
- **Always state the window and each source's newest date.** A quiet day must be distinguishable from a data delay.

## Scope

- **Default:** everything. Megabuyte publishes roughly 5–12 pieces a day; page the news call (`next_offset`) until it's null, so a busy day isn't cut at 25.
- **Narrowed:** if the user names sectors, peer groups or specific companies, filter to those. Megabuyte platform watchlists can't be read through the MCP. If the user asks for "my watchlist", say so in one line and ask them to name the companies or sectors. The sectors and companies they name may be remembered between briefings.

## Workflow

1. **Plan.** Call `plan_query` with `intent: "news_and_signals"`, the question as asked, and `period_from`/`period_to` set to the window as YYYY-MM-DD. "Last 24 hours" isn't parsed, so always send explicit dates.

2. **Collect, in parallel**, each filtered to the window:
   - **News:** `get_news_articles` with `published_since`/`published_until`, `include_text: false`, `limit: 25`. Page if `next_offset` is set (rarely needed). Tags tell you which items are M&A, people moves, results and so on.
   - **People moves:** the news rows tagged "People Moves". There is no separate call; `search_people` can't filter by day. They go under Company research, as company news.
   - **Reports** (go in Market research): `get_reports` with `published_since`/`published_until`.
   - **Company Analysis** (goes in Company research): `get_analysis` with `analysis_type: "company"`, `published_after`/`published_before`.
   - **Market Analysis** (goes in Market research): `get_analysis` with `analysis_type: "market"`, the same dates.
   - **Deals:** `get_deals` with `announced_from`/`announced_to`, plus the news articles tagged M&A, Private Equity, Venture & Growth Capital or Capital Markets. Deal records are now current (within a day of announcement), but an article can still come before its record, or vice versa. Use both, and merge each deal into one item.

3. **Drop test records.** Skip any row whose title looks like a test, in news or deals, e.g. "News 100", "QA NEWS…", "Publish Test" or "Test Company 203 acquires Test Company 202", and any article whose body is only its title. Never date the archive from one. The real newest date is the newest item left after removing them.

4. **Read enough to summarise.** One `get_news_articles` call with the window's article ids (`article_id`, up to 10) and `max_text_chars` around 1,500 each, for the items you'll summarise. Read reports only via `semantic_search` passages or the report text if one is short; never summarise a report from its title.

5. **Write.**
   - **Summary: every item gets a mention, in prose, within 200 words.** Every article, Company Analysis, Market Analysis, report and deal in the window is named at least once, by company or title, however minor. No selection.
     - **Paragraphs only:** one to three short paragraphs of continuous prose. No bullet points, numbered lists, line-per-item layouts or sub-headings inside the summary.
     - **200 words is an absolute ceiling, not a target.** Use as few words as the day allows while still naming every item, bringing out the key themes and reading naturally. A quiet day may need only 60–100 words. Spend words in proportion: the most significant items get a clause and a key figure, minor ones just their name and a few words, and related items share a sentence. On a very busy day, fold minor items into their theme in a few words rather than dropping any. Never exceed 200.
     - **Group by part of the market or by theme, not by content type.** Build each paragraph or sentence around a market area (e.g. HR and HCM software, IT services and the channel, cyber and security, data centres and telecoms, software valuations) or a cross-cutting theme (e.g. AI investment, consolidation, leadership change).
       - Within a theme, mix the content freely: a deal, a set of results, a Company Analysis and a Market Analysis on the same area belong together.
       - Never organise the summary as "results… deals… new analyses… market research…".
       - The sections below the summary stay organised by content type; only the summary is thematic.
     - Lead with the most significant theme, and draw out threads that run across areas (e.g. AI investment showing up in several companies' results) where they exist.
     - **Before finishing, check all four:** every item listed in the sections below is named in the summary; the summary is 200 words or fewer and couldn't be shorter without losing an item, a key theme or clarity; it is prose, with no bullets or lists; and it is grouped by market area or theme, not by content type. Fix any that fail.
   - **Items:** one line each, in your own words.

## Output structure

**Provenance labels** (conventions §4): the opening summary is **AI analysis**. Company research, Market research and Deals are summaries of Megabuyte articles and analyses, so all three sections are labelled **Megabuyte research (AI summary)**. That includes people moves and deals taken from articles. A deal known only from its deal record, with no article, is marked "(deal record)" inline, as Megabuyte data.

1. **Header**: "Megabuyte briefing · [window]". Newest held: news [date], deal records [date], research [date].
2. **Summary**: every item published in the window, mentioned briefly in one to three prose paragraphs, as short as the day allows and never more than 200 words (step 5).
3. **Company research**: company news (results and trading, contract wins, strategy, **people moves**) and **every Company Analysis** published in the window. A Company Analysis always goes here, even when it discusses the company's market.
4. **Market research**: **only** Market Analyses and reports (peer-group quarterlies, corporate activity reports) published in the window. Nothing else goes here.
5. **Deals**: from M&A, Private Equity, Venture & Growth Capital and Capital Markets articles, enriched from deal records (parties, type, value or "not disclosed", disclosed multiple).

**Every item is led by its title as a link** to the source, using the Link exactly as returned, then the date, then one line in your own words. For example:

> **[Article title as published](Link as returned)** · 13 Oct 2026. One line, in your own words, on what happened and why it matters.

- Companies named in the line link to their Megabuyte profiles (conventions §4).
- An item belongs in one section only. An article that is both a deal and results goes under Deals.
- An empty section reads "None published in the window".
- End with a one-line coverage note giving the newest date held per source, e.g. "News to 28 Oct, deal records to 27 Oct."

Keep the whole briefing scannable.

## Watch-outs

- Don't count the same story twice: an M&A article and its deal record are one item. Put it under Deals and link the article.
- Ordinary commercial news (contract wins, launches, awards) isn't a signal of a sale or distress. Don't frame it as one.
- If the window is empty in every source but the archive has newer items, the window is wrong. Check the dates before reporting a quiet day.
