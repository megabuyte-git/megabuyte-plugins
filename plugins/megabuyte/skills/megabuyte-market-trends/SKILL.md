---
name: megabuyte-market-trends
description: Summarise what Megabuyte's research says about a theme or trend in UK technology, within one sector or across several, using the Megabuyte MCP. Use this whenever the user asks what Megabuyte thinks, is seeing or has written about a theme ("what does Megabuyte think about AI in software?", "how is consolidation playing out in MSPs?", "what are the drivers and risks in cyber?", "has Megabuyte's view on payments changed?", "outlook for UK IT services"). Also use for drafting a market or sector section from Megabuyte research, and when they want it exported to Word. Not for numeric trends in deal volumes or multiples (megabuyte-deal-precedents) or for who the players are (megabuyte-market-map).
---

# Megabuyte market trends

Summarises Megabuyte's published research on a theme: the view, its drivers and risks, and how it has shifted, quoted and dated.

**Read `references/conventions.md` first.** For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Workflow

1. **Plan.** Call `plan_query` with `intent: "sector_research"` (or `ic_market_section` when the user wants a drafted section), the question as asked, and the sector word in `theme`. Follow the plan's calls (conventions §2).
   - If no sector is named and the theme is clearly cross-sector ("AI across UK tech"), use both sectors and say so.
   - If it's unclear which sector is meant, ask one short question.

2. **Window.** Default to the last 18 months unless the user gives one, and say so. For "has the view changed", also read the year before the start of that window.

3. **Read the research.** Make these calls in parallel:
   - `get_reports`, `report_family: "PeerGroupQuarterly"`, per relevant peer group, `limit: 3`: the newest quarterlies, and the research library's latest date.
   - `semantic_search` with the question, `sectors` (the theme groups plus the group the quarterlies are filed under), `report_families: ["PeerGroupQuarterly","CorporateActivity"]` and `since` the window start.
   - `semantic_search` with the theme words in the question, `sources: ["news","market_analysis"]` and the window. News passages about one company are examples, not the sector view.
   - `get_analysis`, `analysis_type: "market"`, per peer group, `published_after` the window start. Open the most relevant one whole.
   - **Company-level views:** `semantic_search` with `sources: ["company_analysis","news"]` and the theme in the question. Company Analyses and the analyst comment in news articles (Megabuyte's view on a company's results or deal) often carry the sharpest views on a theme. Aggregate across companies: "several analyses of MSPs note…", with examples, never a count.
   - **Adjacent areas:** themes cross the taxonomy (MSP consolidation also runs through Telecoms Services and IT Consulting). Use `search_companies` with `keywords` and `find_similar_companies` on 2–3 companies central to the theme to find which other peer groups are involved. Add those groups to `sectors` in the searches above, and say you widened.

4. **Supporting numbers (optional, and few).** At most two or three population statistics from `benchmark_financials` (e.g. median organic growth in the segment), each with its n and date. Leave trend lines in deal volumes or multiples to the deal precedents skill, and offer it.

5. **Write.** Summarise in your own words. Attribute each point to a dated source (report title and date, or article and date). Where fewer than two dated passages support a point, say the research says little on it.

6. **Check** with `check_answer` if any figures are quoted, then answer.

## Output structure

1. **Headline view**: 2–3 sentences on what Megabuyte's research says, with the date range read.
2. **Themes**: 3–5 short sections (e.g. drivers, risks, winners and losers by segment, AI impact), each grounded in dated sources, combining sector research with the company-level views.
3. **How the view has shifted**: only if asked, or if the research clearly changed within the window. Compare earlier and later statements with their dates.
4. **Supporting data**: optional, at most three population statistics.
5. **What the research doesn't cover**: e.g. no market sizing or forecasts held.
6. **Sources**: the reports, analyses and articles read, with dates and links.

Word exports follow the same structure.

## Watch-outs

- No company lists: name companies only as examples the research itself gives.
- Never present a forecast, market size or ranking as Megabuyte's unless a dated passage says it. The server holds no forecasts or TAM.
- Never attribute a theme or risk to Megabuyte from general knowledge.
- Skip boilerplate passages (Company Contact lists, disclaimers, "About Megabuyte").
- Read peer-group quarterlies before older Barometer reports when newer quarterlies exist.
- If semantic search reports `reranking_refused` or `lexicalOnly`, say so once (conventions §5).
